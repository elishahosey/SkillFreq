"""Runnable version isolation and fair comparisons on shared retained inputs."""
import copy
import csv
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import yaml

from scripts.grading_snapshot import (
    ROOT, capture_market, compare_snapshots, extract_snapshot, save_snapshot, validate_market,
)
from skillfreq.calibration_review import load_comparison
from scripts.grading_snapshot_worker import runtime_differences


class GradingSnapshotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.source = cls.root / 'source'
        shutil.copytree(ROOT / 'skillfreq', cls.source / 'skillfreq',
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / 'configs', cls.source / 'configs')
        cls.old = cls.root / 'old.zip'
        cls.saved = save_snapshot(cls.old, cls.source)
        # Subsequent configuration AND source edits must not alter the saved OLD.
        profile_path = cls.source / 'configs/profile.yml'
        profile = yaml.safe_load(profile_path.read_text(encoding='utf-8'))
        profile['experience_years'] = [10, 12]
        profile_path.write_text(yaml.safe_dump(profile), encoding='utf-8')
        grading_path = cls.source / 'skillfreq/score/grading.py'
        grading_path.write_text(grading_path.read_text(encoding='utf-8').replace(
            'pre_ai_score=fit,', 'pre_ai_score=fit + 1,'), encoding='utf-8')
        cls.new = cls.root / 'new.zip'
        save_snapshot(cls.new, cls.source)
        cls.market = dict(format_version=1, taxonomy_version=cls.saved['grader']['taxonomy_version'],
                          prevalence={'SQL': 50, 'Python': 40, 'AWS': 30},
                          context=dict(source='test-market', extraction_run_ids=['refresh-2'],
                                       taxonomy_versions=[cls.saved['grader']['taxonomy_version']]))

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.case.cleanup)
        self.path = Path(self.case.name)
        self.jobs = self.path / 'jobs.csv'
        self.write_jobs([dict(id='0007', source_site='test', title='Senior Data Engineer',
                             description='Build SQL ETL data pipelines with Python. 8 years of experience. AWS preferred.',
                             source='https://example.test/jobs/7'),
                         dict(id='', source_site='test', title='Data Engineer',
                              description='SQL Python ETL data pipelines.', source='https://example.test/jobs/8')])
        self.market_path = self.path / 'market.json'
        self.market_path.write_text(json.dumps(self.market), encoding='utf-8')

    def write_jobs(self, rows):
        with self.jobs.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=['id', 'source_site', 'title', 'description', 'source'])
            writer.writeheader()
            writer.writerows(rows)

    def compare(self, name='comparison', **kwargs):
        return compare_snapshots(self.old, self.new, self.jobs, self.market_path, self.path / name, **kwargs)

    def test_old_and_new_use_saved_code_config_and_identical_inputs(self):
        out = self.compare()
        rows, message = load_comparison(out / 'new.csv', out / 'old.csv')
        self.assertIn('2 matched records', message)
        self.assertIn('0 OLD-only and 0 NEW-only', message)
        self.assertIn('0007', {r['job_id'] for r in rows})
        grades = {}
        for side in ('old', 'new'):
            with (out / f'{side}.csv').open(encoding='utf-8', newline='') as stream:
                grades[side] = json.loads(next(csv.DictReader(stream))['grade_json'])
            grade = grades[side]
            self.assertEqual(grade['market_context']['extraction_run_ids'], ['refresh-2'])
            self.assertEqual(grade['market_context']['prevalence_pct']['AWS'], 30)
        self.assertEqual(grades['old']['seniority_signals']['candidate_experience_years'],
                         self.saved['grader']['configuration']['profile']['experience_years'])
        self.assertEqual(grades['new']['seniority_signals']['candidate_experience_years'], [10, 12])
        self.assertEqual(grades['old']['pre_ai_score'], grades['old']['fit_score'])
        self.assertEqual(grades['new']['pre_ai_score'], grades['new']['fit_score'] + 1)
        self.assertNotEqual(grades['old']['grading_version'], grades['new']['grading_version'])
        self.assertEqual((out / 'jobs.csv').read_bytes(), self.jobs.read_bytes())
        self.assertEqual((out / 'market.json').read_bytes(), self.market_path.read_bytes())
        again = self.compare('again')
        for side in ('old', 'new'):
            self.assertEqual((out / f'{side}.csv').read_bytes(), (again / f'{side}.csv').read_bytes())
        with self.assertRaises(FileExistsError):
            self.compare()

    def test_snapshot_inventory_integrity_and_no_overwrite(self):
        with zipfile.ZipFile(self.old) as archive:
            self.assertNotIn('.env', archive.namelist())
            self.assertNotIn('data', archive.namelist())
            self.assertFalse(any('__pycache__' in name for name in archive.namelist()))
            corrupted = self.path / 'corrupt.zip'
            with zipfile.ZipFile(corrupted, 'w') as changed:
                for name in archive.namelist():
                    changed.writestr(name, b'changed' if name == 'configs/profile.yml' else archive.read(name))
        with self.assertRaisesRegex(ValueError, 'checksum'):
            extract_snapshot(corrupted, self.path / 'extract')
        with self.assertRaises(FileExistsError):
            save_snapshot(self.old)

    def test_historical_yaml_requires_matching_source_and_configuration(self):
        expected = self.path / 'historical.grading.yml'
        expected.write_text(yaml.safe_dump(self.saved['grader']), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'historical'):
            save_snapshot(self.path / 'wrong.zip', self.source, expected)
        self.assertFalse((self.path / 'wrong.zip').exists())

    def test_failed_comparison_does_not_publish_partial_results(self):
        self.write_jobs([dict(id='1', title='Data Engineer', description='SQL'),
                         dict(id='1', title='Data Engineer', description='Python')])
        with self.assertRaises(subprocess.CalledProcessError):
            self.compare()
        self.assertFalse((self.path / 'comparison').exists())

    def test_market_taxonomy_must_match_both_graders(self):
        market = copy.deepcopy(self.market)
        market['taxonomy_version'] = 'different'
        market['context']['taxonomy_versions'] = ['different']
        self.market_path.write_text(json.dumps(market), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'taxonomy'):
            self.compare()
        self.assertFalse((self.path / 'comparison').exists())

    def test_capture_reads_market_once_and_preserves_full_mapping(self):
        out = self.path / 'captured.json'
        with patch('skillfreq.io.grading_to_postgres.load_prevalence',
                   return_value=(self.market['prevalence'], self.market['context'])) as read:
            captured = capture_market(out)
            read.assert_called_once_with(self.market['taxonomy_version'])
        self.assertEqual(captured, self.market)
        self.assertEqual(json.loads(out.read_text()), self.market)

    def test_invalid_market_values_are_rejected(self):
        for value in (-1, 101, float('nan'), True, '20'):
            market = copy.deepcopy(self.market)
            market['prevalence']['SQL'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_market(market)

    def test_runtime_drift_detects_changed_or_missing_dependencies(self):
        saved = dict(python='3.12.3', dependencies={'pyyaml': '6.0.3', 'pandas': '3.0.1'})
        actual = copy.deepcopy(saved)
        actual['dependencies']['extra'] = '1.0'
        self.assertEqual(runtime_differences(saved, actual), [])
        actual['python'] = '3.13.0'
        actual['dependencies']['pyyaml'] = '6.0.2'
        del actual['dependencies']['pandas']
        self.assertEqual(len(runtime_differences(saved, actual)), 3)

    def test_traversal_is_rejected_before_extraction(self):
        archive = self.path / 'unsafe.zip'
        for name in ('../escape.py', '/escape.py', 'C:/escape.py', '..\\escape.py'):
            with zipfile.ZipFile(archive, 'w') as output:
                output.writestr(name, 'bad')
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'path'):
                extract_snapshot(archive, self.path / 'extract')


if __name__ == '__main__':
    unittest.main()
