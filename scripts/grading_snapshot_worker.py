"""Internal, archived worker for grading_snapshot.py; run in an isolated process."""
import csv
import hashlib
from importlib.metadata import distributions
import json
from pathlib import Path
import platform
import sys


def runtime():
    return dict(python=platform.python_version(), dependencies={
        d.metadata['Name'].lower().replace('_', '-'): d.version
        for d in distributions() if d.metadata['Name']})


def runtime_differences(saved, actual):
    drift = []
    if actual['python'] != saved['python']:
        drift.append('Python version differs')
    for package, version in saved['dependencies'].items():
        if actual['dependencies'].get(package) != version:
            drift.append(f'{package}: expected {version}, found {actual["dependencies"].get(package)}')
    return drift


def main():
    root, operation, *args = sys.argv[1:]
    sys.path.insert(0, root)
    from skillfreq.score.grading import GradingContext
    context = GradingContext.load()
    if operation == 'inspect':
        Path(args[0]).write_text(json.dumps(dict(
            grading_version=context.grading_version,
            taxonomy_version=context.taxonomy_version,
            configuration=context.snapshot, runtime=runtime()), indent=2), encoding='utf-8')
        return

    source, market_path, output, manifest_path, allow_drift = args
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    expected = manifest['grader']
    if (context.grading_version, context.taxonomy_version) != (
            expected['grading_version'], expected['taxonomy_version']):
        raise ValueError('Saved grader version does not match the loaded code/configuration')
    actual_runtime = runtime()
    drift = runtime_differences(expected['runtime'], actual_runtime)
    if drift and allow_drift != 'yes':
        raise ValueError('Saved runtime differs. Restore it or explicitly use --allow-runtime-drift: ' + '; '.join(drift))

    market_bytes = Path(market_path).read_bytes()
    market = json.loads(market_bytes)
    if market['taxonomy_version'] != context.taxonomy_version:
        raise ValueError('Market and grader taxonomy versions differ; choose a compatible market snapshot')
    from skillfreq.pipeline import build_job_result, finish_grading
    csv.field_size_limit(10_000_000)
    results, seen = [], set()
    with Path(source).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not {'title', 'description'} <= set(reader.fieldnames or []):
            raise ValueError('Jobs CSV must contain title and description')
        for row in reader:
            job = {key: row.get(key, '') for key in (
                'id', 'source', 'source_site', 'title', 'description',
                'search_lane', 'search_term_used', 'review_priority')}
            job['id'] = (row.get('id') or row.get('job_id') or row.get('source_row_id')
                         or row.get('source_job_id') or '').strip()
            job['source'] = (row.get('source') or row.get('job_url') or row.get('url') or '').strip()
            job['source_site'] = (row.get('source_site') or row.get('site') or '').strip()
            key = (job['source_site'], job['id'] or job['source'])
            if not key[1] or key in seen:
                raise ValueError(f'Missing or duplicate job identity: {key}')
            seen.add(key)
            results.append(build_job_result(job, context, market['prevalence'], market['context']))
            if len(results) % 500 == 0:
                print(f'Graded {len(results)} jobs', flush=True)
    if not results:
        raise ValueError('Jobs CSV is empty')
    output_keys = [(r.source_site, r.id or r.source) for r in results]
    if len(set(output_keys)) != len(results) or set(output_keys) != seen:
        raise ValueError('Grader changed or collapsed input identities')
    output = Path(output)
    finish_grading(output, results, context)
    output.with_suffix('.run.json').write_text(json.dumps(dict(
        grading_version=context.grading_version, taxonomy_version=context.taxonomy_version,
        jobs=len(results), identities=sorted(seen), runtime=actual_runtime, runtime_drift=drift,
        market_sha256=hashlib.sha256(market_bytes).hexdigest()), indent=2), encoding='utf-8')
    print(f'Wrote {len(results)} jobs: {output.name}', flush=True)


if __name__ == '__main__':
    main()
