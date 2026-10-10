"""Save runnable graders and compare them on one retained job/market snapshot."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
WORKER = Path(__file__).with_name('grading_snapshot_worker.py')
CONFIGS = ('skills', 'profile', 'weights', 'roles', 'market_skills', 'requirements')


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False), encoding='utf-8')


def worker(root, operation, *args):
    # -I ignores the active checkout/PYTHONPATH; only the saved package is imported.
    subprocess.run([sys.executable, '-I', '-B', str(root / 'worker.py'), str(root),
                    operation, *map(str, args)], cwd=root, check=True)


def new_destination(path):
    path = Path(path).resolve()
    if path.exists():
        raise FileExistsError(f'Choose a new path; retained artifacts are never overwritten: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_snapshot(output, source_root=ROOT, expected_snapshot=None):
    """Capture exact source/config bytes, including edits not committed to Git."""
    output = new_destination(output)
    source_root = Path(source_root).resolve()
    if output.suffix.lower() != '.zip':
        raise ValueError('Grader snapshot must end in .zip')
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        paths = list((source_root / 'skillfreq').rglob('*.py'))
        paths += [source_root / 'configs' / f'{name}.yml' for name in CONFIGS]
        if (source_root / 'requirements.txt').exists():
            paths.append(source_root / 'requirements.txt')
        for path in paths:
            target = root / path.relative_to(source_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        shutil.copyfile(WORKER, root / 'worker.py')
        payload = [p for p in root.rglob('*') if p.is_file()]
        worker(root, 'inspect', root / 'grader.json')
        grader = json.loads((root / 'grader.json').read_text(encoding='utf-8'))
        if expected_snapshot:
            import yaml
            expected = yaml.safe_load(Path(expected_snapshot).read_text(encoding='utf-8'))
            if any(grader.get(key) != expected.get(key) for key in (
                    'grading_version', 'taxonomy_version', 'configuration')):
                raise ValueError('Source/configuration does not match the historical .grading.yml; restore its original source and config first')
        manifest = dict(format_version=1, created_at=datetime.now(timezone.utc).isoformat(),
                        grader=grader, files={p.relative_to(root).as_posix(): digest(p) for p in payload})
        write_json(root / 'manifest.json', manifest)
        # Build completely before exclusively creating the retained artifact.
        archive_path = root / 'snapshot.zip'
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in payload + [root / 'manifest.json']:
                archive.write(path, path.relative_to(root).as_posix())
        with output.open('xb') as target, archive_path.open('rb') as source:
            shutil.copyfileobj(source, target)
    return manifest


def extract_snapshot(path, root):
    """Verify retained files before executing their saved worker/code."""
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate paths in grader snapshot')
        for name in names:
            parts = PurePosixPath(name).parts
            if not parts or any(p in ('.', '..') or ':' in p for p in parts) or '\\' in name or name.startswith('/'):
                raise ValueError('Unsafe path in grader snapshot')
            if (root / name).resolve().is_relative_to(root.resolve()) is False:
                raise ValueError('Grader snapshot path escapes destination')
        manifest = json.loads(archive.read('manifest.json'))
        if manifest['format_version'] != 1:
            raise ValueError('Unsupported grader snapshot format')
        if set(names) != set(manifest['files']) | {'manifest.json'}:
            raise ValueError('Grader snapshot file inventory differs from manifest')
        for name, expected in manifest['files'].items():
            data = archive.read(name)
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError(f'Grader snapshot checksum mismatch: {name}')
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        write_json(root / 'manifest.json', manifest)
    return manifest


def validate_market(market):
    if market.get('format_version') != 1 or not isinstance(market.get('taxonomy_version'), str):
        raise ValueError('Invalid market snapshot format')
    prevalence = market.get('prevalence')
    if not isinstance(prevalence, dict) or not prevalence:
        raise ValueError('Market snapshot requires available prevalence data')
    for skill, value in prevalence.items():
        if (not isinstance(skill, str) or isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or not 0 <= value <= 100):
            raise ValueError(f'Invalid market prevalence: {skill}')
    if not isinstance(market.get('context'), dict):
        raise ValueError('Market snapshot requires provenance context')
    if market['context'].get('taxonomy_versions') != [market['taxonomy_version']]:
        raise ValueError('Market provenance taxonomy does not match the snapshot')


def capture_market(output):
    output = new_destination(output)
    sys.path.insert(0, str(ROOT))
    from skillfreq.io.grading_to_postgres import load_prevalence
    from skillfreq.skills.job_market import taxonomy_version
    version = taxonomy_version(ROOT / 'configs/market_skills.yml')
    prevalence, context = load_prevalence(version)
    market = dict(format_version=1, taxonomy_version=version, prevalence=prevalence, context=context)
    validate_market(market)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(market, stream, indent=2, allow_nan=False)
    return market


def compare_snapshots(old, new, source, market_path, output, allow_runtime_drift=False):
    """Retain shared inputs and only publish a complete successful comparison."""
    output = new_destination(output)
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        stage = Path(temp)
        result = stage / 'comparison'
        result.mkdir()
        for source_path, name in ((source, 'jobs.csv'), (market_path, 'market.json'),
                                  (old, 'old.grader.zip'), (new, 'new.grader.zip')):
            shutil.copyfile(source_path, result / name)
        market = json.loads((result / 'market.json').read_text(encoding='utf-8'))
        validate_market(market)
        graders = {}
        for side in ('old', 'new'):
            root = stage / side
            root.mkdir()
            manifest = extract_snapshot(result / f'{side}.grader.zip', root)
            if manifest['grader']['taxonomy_version'] != market['taxonomy_version']:
                raise ValueError(f'{side.upper()} grader and market taxonomy versions differ; use compatible snapshots')
            graders[side] = manifest['grader']['grading_version']
            worker(root, 'grade', result / 'jobs.csv', result / 'market.json',
                   result / f'{side}.csv', root / 'manifest.json', 'yes' if allow_runtime_drift else 'no')
        old_run, new_run = [json.loads((result / f'{side}.run.json').read_text(encoding='utf-8'))
                            for side in ('old', 'new')]
        if old_run['identities'] != new_run['identities']:
            raise ValueError('Saved graders produced different job cohorts')
        write_json(result / 'comparison.json', dict(
            format_version=1, created_at=datetime.now(timezone.utc).isoformat(),
            grading_versions=graders, jobs=old_run['jobs'],
            files={p.name: digest(p) for p in result.iterdir()},
            runtime_drift={side: run['runtime_drift'] for side, run in (('old', old_run), ('new', new_run))}))
        if output.exists():
            raise FileExistsError(f'Comparison already exists: {output}')
        result.rename(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    save = commands.add_parser('save', help='Archive a runnable grading version')
    save.add_argument('--out', type=Path, required=True)
    save.add_argument('--source-root', type=Path, default=ROOT,
                      help='Checkout containing the code and configuration to preserve')
    save.add_argument('--expect-snapshot', type=Path,
                      help='Require the restored checkout to match this historical .grading.yml')
    market = commands.add_parser('capture-market', help='Read current DB prevalence once for both graders')
    market.add_argument('--out', type=Path, required=True)
    compare = commands.add_parser('compare', help='Run saved OLD/NEW graders on identical jobs and market data')
    compare.add_argument('--old', type=Path, required=True)
    compare.add_argument('--new', type=Path, required=True)
    compare.add_argument('--input', type=Path, required=True)
    compare.add_argument('--market', type=Path, required=True)
    compare.add_argument('--out-dir', type=Path, required=True)
    compare.add_argument('--allow-runtime-drift', action='store_true',
                         help='Explicitly permit changed Python/package versions and record differences')
    args = parser.parse_args()
    try:
        if args.command == 'save':
            saved = save_snapshot(args.out, args.source_root, args.expect_snapshot)
            print(f'Saved grader {saved["grader"]["grading_version"]}: {args.out}')
        elif args.command == 'capture-market':
            capture_market(args.out)
            print(f'Saved market snapshot: {args.out}')
        else:
            path = compare_snapshots(args.old, args.new, args.input, args.market,
                                     args.out_dir, args.allow_runtime_drift)
            print(f'Load {path / "old.csv"} and {path / "new.csv"} in calibration review')
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
