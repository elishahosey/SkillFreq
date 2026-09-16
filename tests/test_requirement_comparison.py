import copy
import csv
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from scripts.compare_requirements import compare
from skillfreq.score.grading import GradingContext, grade_job


class RequirementComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grade = grade_job({'title': 'Data Engineer', 'description':
                              'SQL ETL data pipelines.\nRequired qualifications: AWS and Spark.'},
                             GradingContext.load(), prevalence={}).to_dict()

    def run_comparison(self, after, description='same frozen description'):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory)/name for name in ('before.csv', 'after.csv')]
            for path, grade, text in zip(paths, (self.grade, after), ('same frozen description', description)):
                with path.open('w', encoding='utf-8', newline='') as stream:
                    writer = csv.DictWriter(stream, fieldnames=['id', 'source_site', 'title', 'description', 'grade_json'])
                    writer.writeheader()
                    writer.writerow(dict(id='one', source_site='fixture', title='Data Engineer', description=text,
                                         grade_json=json.dumps(grade)))
            with redirect_stdout(io.StringIO()):
                return compare(*paths, Path(directory)/'report.md')

    def test_atomic_order_is_not_a_semantic_change(self):
        after = copy.deepcopy(self.grade)
        after['missing_required_skills']['atomic_skills'].reverse()
        self.assertEqual(self.run_comparison(after)['changed_jobs'], 0)

    def test_same_id_with_changed_description_is_not_same_cohort(self):
        with self.assertRaisesRegex(ValueError, 'inputs differ'):
            self.run_comparison(self.grade, 'different text')

    def test_lane_drift_fails_even_if_counts_could_cancel_out(self):
        after = copy.deepcopy(self.grade)
        after['role_lane'] = 'wrong_lane'
        with self.assertRaisesRegex(ValueError, 'drift'):
            self.run_comparison(after)

    def test_unattributed_score_change_fails(self):
        after = copy.deepcopy(self.grade)
        after['fit_score'] -= 1
        with self.assertRaisesRegex(ValueError, 'unattributed'):
            self.run_comparison(after)


if __name__ == '__main__':
    unittest.main()
