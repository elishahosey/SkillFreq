"""Replay saved DB inputs through the existing pipeline, preserving exact cohort membership."""
import argparse
import csv
import json
import hashlib
import platform
from importlib.metadata import distributions
import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.pipeline import build_job_result, finish_grading, grading_market
from skillfreq.score.grading import GradingContext


def replay(source, output, frozen_market=False, reviews_path=None):
    if source.resolve() == output.resolve():
        raise ValueError('Use a separate output; preserve the baseline')
    artifacts = [output, output.with_suffix('.grading.yml'), output.with_suffix('.manifest.json'),
                 output.with_suffix('.source.patch')]
    if any(path.exists() for path in artifacts):
        raise FileExistsError('Use a new output basename; retained artifacts must not be overwritten')
    from skillfreq.calibration_review import load_reviews, identity
    reviews = load_reviews(reviews_path) if reviews_path else None
    csv.field_size_limit(10_000_000)
    context = GradingContext.load()
    prevalence, market = (None, None) if frozen_market else grading_market(context)
    if prevalence is None and not frozen_market:
        raise RuntimeError('Comparison requires available market data; see the prevalence diagnostic')
    results = []
    seen = set()
    with source.open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            key = identity(row)
            if reviews is not None and key not in reviews:
                continue
            if key in seen:
                raise ValueError(f'Duplicate source identity: {key}')
            seen.add(key)
            if frozen_market:
                previous = json.loads(row['grade_json'])
                market = previous['market_context']
                prevalence = (None if previous['learning_status'] == 'unavailable' else
                              {k:v for k,v in market['prevalence_pct'].items() if v is not None})
                if reviews and reviews[key].get('new_grading_version') != previous['grading_version']:
                    raise ValueError(f'Review version does not match source grade: {key}')
            job = {k:row[k] for k in ('id','source','source_site','title','description',
                    'search_lane','search_term_used','review_priority')}
            results.append(build_job_result(job, context, prevalence, market))
            if len(results) % 500 == 0:
                print(f'Graded {len(results)} frozen-cohort jobs', flush=True)
    if reviews is not None and seen != set(reviews):
        raise ValueError(f'Missing {len(set(reviews)-seen)} reviewed source identities')
    output.parent.mkdir(parents=True, exist_ok=True)
    finish_grading(output, results, context)
    def digest(path):
        with path.open('rb') as stream:
            return hashlib.file_digest(stream, 'sha256').hexdigest()
    sources = [source, source.with_suffix('.grading.yml')]
    if reviews_path:
        sources.append(reviews_path)
    patch = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'])
    output.with_suffix('.source.patch').write_bytes(patch)
    manifest = dict(comparison_kind='re-evaluation of retained result inputs; not a proven lossless historical replay',
                    git_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    git_status=subprocess.check_output(['git', 'status', '--short'], text=True),
                    python=platform.python_version(), frozen_market=frozen_market,
                    dependencies={d.metadata['Name']: d.version for d in distributions() if d.metadata['Name']},
                    grading_version=context.grading_version, taxonomy_version=context.taxonomy_version,
                    cohort=sorted(seen), jobs=len(results),
                    sources={str(p): digest(p) for p in sources if p.exists()},
                    outputs={str(p): digest(p) for p in (output, output.with_suffix('.grading.yml'),
                                                        output.with_suffix('.source.patch'))})
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f'Wrote {len(results)} jobs, grading version {context.grading_version}: {output}', flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path('data/outputs/results-db-90-days-domain.csv'))
    parser.add_argument('--out', type=Path, default=Path('data/outputs/results-db-90-days-ecosystem.csv'))
    parser.add_argument('--frozen-market', action='store_true', help='Reuse saved per-job prevalence for an isolated semantic comparison')
    parser.add_argument('--reviews', type=Path, help='Select exactly the identities in a retained human review workbook')
    args = parser.parse_args()
    replay(args.input,args.out,args.frozen_market,args.reviews)
