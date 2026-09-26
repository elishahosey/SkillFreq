import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from openpyxl import Workbook
from streamlit.testing.v1 import AppTest

from skillfreq.calibration_review import (
    build_queue, default_review_path, identity, load_comparison, load_reviews, save_review,
)


class CalibrationReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.source = self.directory / 'comparison.csv'
        self.rows = [dict(id='001', source_site='site', title='Changed decision', company='Example',
                         description='Build pipelines', old_lane='target', new_lane='target',
                         old_score=80, new_score=80, old_decision='skip', new_decision='apply_now'),
                     dict(id='002', source_site='site', title='Changed score', company='', description='',
                          old_lane='target', new_lane='target', old_score=50, new_score=65,
                          old_decision='skip', new_decision='skip'),
                     dict(id='003', source_site='site', title='Unchanged', company='', description='',
                          old_lane='target', new_lane='target', old_score=50, new_score=50,
                          old_decision='skip', new_decision='skip')]
        with self.source.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=self.rows[0])
            writer.writeheader()
            writer.writerows(self.rows)
        self.records, _ = load_comparison(self.source)
        self.output = self.directory / 'calibration_review_2026-09-25.xlsx'

    def test_save_update_and_resume_preserve_source_and_literal_notes(self):
        original = self.source.read_bytes()
        row = self.records[0]
        save_review(self.output, row, 1)
        save_review(self.output, row, 3, '=literal note', ['stack_mismatch'])
        saved = load_reviews(self.output, row)
        self.assertEqual(len(saved), 1)
        review = saved[identity(row)]
        self.assertEqual(review['job_id'], '001')
        self.assertEqual(review['review_rating'], 3)
        self.assertEqual(review['new_fit_score'], 80)
        self.assertEqual(review['review_note'], '=literal note')
        self.assertEqual(review['issue_tags'], 'stack_mismatch')
        self.assertTrue(review['reviewed'])
        self.assertTrue(review['reviewed_at'])
        self.assertEqual(default_review_path(row), self.output)
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual([r['job_id'] for r in build_queue(self.records, saved, unchanged_sample=0)], ['002'])

    def test_queue_filters_priorities_thresholds_and_sampling(self):
        self.assertEqual([r['job_id'] for r in build_queue(self.records, {}, unchanged_sample=0)], ['001', '002'])
        self.assertEqual([r['job_id'] for r in build_queue(self.records, {}, threshold=20, unchanged_sample=0)], ['001'])
        self.assertEqual([r['job_id'] for r in build_queue(self.records, {}, signals=[], unchanged_sample=5)], ['003'])
        reviewed = {identity(self.records[0]): {}}
        self.assertEqual([r['job_id'] for r in build_queue(self.records, reviewed, status='Reviewed')], ['001'])
        self.assertEqual([r['job_id'] for r in build_queue(self.records, reviewed, status='All', unchanged_sample=0)], ['002', '001'])
        self.records[2]['new_role_lane'] = 'secondary'
        self.assertEqual([r['job_id'] for r in build_queue(self.records, {}, signals=['Lane changed'], unchanged_sample=0)], ['003'])
        self.records[2]['new_ai_review_required'] = 'True'
        self.assertEqual([r['job_id'] for r in build_queue(self.records, {}, signals=['AI review changed'], unchanged_sample=0)], ['003'])

    def test_excel_named_fields_and_missing_context(self):
        path = self.directory / 'input.xlsx'
        book = Workbook()
        book.active.append(['new_fit_score', 'source_row_id', 'old_fit_score'])
        book.active.append([90, '0007', 50])
        book.save(path)
        book.close()
        original = path.read_bytes()
        rows, _ = load_comparison(path)
        self.assertEqual(rows[0]['job_id'], '0007')
        self.assertEqual(rows[0]['company'], '')
        with self.assertRaisesRegex(ValueError, 'separate'):
            save_review(path, rows[0], 1)
        self.assertEqual(path.read_bytes(), original)

    def test_two_exports_match_source_identity_and_read_grade_evidence(self):
        import json
        paths = [self.directory / 'old.csv', self.directory / 'new.csv']
        for path, lane in zip(paths, ['target', 'secondary']):
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=['id', 'source_site', 'title', 'grade_json'])
                writer.writeheader()
                writer.writerow(dict(id='001', source_site='site', title='Engineer',
                                     grade_json=json.dumps(dict(role_lane=lane, fit_score=50,
                                         blocking_reasons=['experience'], grading_version=lane))))
        rows, _ = load_comparison(paths[1], paths[0])
        self.assertEqual(rows[0]['old_role_lane'], 'target')
        self.assertEqual(rows[0]['new_role_lane'], 'secondary')
        self.assertIn('experience', rows[0]['new_blocking_reasons'])
        self.assertEqual(rows[0]['new_grading_version'], 'secondary')

    def test_duplicate_input_and_unrelated_output_rejected(self):
        with self.source.open('a', encoding='utf-8', newline='') as stream:
            csv.DictWriter(stream, fieldnames=self.rows[0]).writerow(self.rows[0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            load_comparison(self.source)
        save_review(self.output, self.records[0], 1)
        other = dict(self.records[0], comparison_after='different.csv')
        with self.assertRaisesRegex(ValueError, 'different comparison'):
            save_review(self.output, other, 2)
        self.assertEqual(load_reviews(self.output)[identity(self.records[0])]['review_rating'], 1)

    def test_failed_replace_keeps_saved_review(self):
        save_review(self.output, self.records[0], 1)
        with patch('pathlib.Path.replace', side_effect=PermissionError('locked')):
            with self.assertRaises(PermissionError):
                save_review(self.output, self.records[0], 3)
        self.assertEqual(load_reviews(self.output)[identity(self.records[0])]['review_rating'], 1)
        self.assertEqual(list(self.directory.glob('*.xlsx')), [self.output])

    def app(self):
        app = AppTest.from_file(Path(__file__).resolve().parents[1] / 'scripts/review_calibration.py',
                                default_timeout=15).run()
        app.selectbox[0].select('One comparison file')
        app.text_input[1].input(str(self.source))
        app.text_input[2].input('')  # Discover dated progress on a new session.
        app.button[0].click().run()
        self.assertFalse(app.exception)
        return app

    def click(self, app, label):
        next(button for button in app.button if button.label == label).click().run()
        self.assertFalse(app.exception)

    def test_ui_save_navigate_update_and_restart(self):
        app = self.app()
        self.assertEqual(app.subheader[0].value, 'Changed decision')
        self.click(app, 'Save + Next')
        self.assertTrue(app.error)
        self.assertEqual(app.subheader[0].value, 'Changed decision')
        self.assertFalse(list(self.directory.glob('calibration_review_*.xlsx')))
        app.radio[0].set_value(1)
        self.click(app, 'Save + Next')
        self.assertEqual(app.subheader[0].value, 'Changed score')
        self.assertIsNone(app.radio[0].value)
        app.text_area[0].input('Unsaved draft')
        self.click(app, 'Previous')
        self.assertEqual(app.radio[0].value, 1)
        app.radio[0].set_value(3)
        app.text_area[0].input('Decision needs correction')
        self.click(app, 'Save')
        path = default_review_path(self.records[0])
        self.assertEqual(len(load_reviews(path)), 1)
        self.assertEqual(load_reviews(path)[identity(self.records[0])]['review_rating'], 3)
        restarted = self.app()
        self.assertEqual(restarted.subheader[0].value, 'Changed score')
        self.assertEqual(restarted.text_area[0].value, '')
        restarted.radio[0].set_value(2)
        self.click(restarted, 'Save + Next')
        self.assertTrue(any('Consider adding' in info.value for info in restarted.info))
        self.assertEqual(len(load_reviews(path)), 2)


if __name__ == '__main__':
    unittest.main()
