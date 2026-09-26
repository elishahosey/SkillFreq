import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from openpyxl import Workbook
from streamlit.testing.v1 import AppTest

from skillfreq.calibration_review import (
    SUBGRADE_OPTIONS, build_queue, default_review_path, identity, load_comparison, load_reviews, save_review,
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
        save_review(self.output, row, 1, decision_quality='better', score_quality='reasonable',
                    requirement_interpretation='correct')
        save_review(self.output, row, 3, '=literal note', ['stack_mismatch'],
                    decision_quality='worse', score_quality='too_high', requirement_interpretation='incorrect')
        saved = load_reviews(self.output, row)
        self.assertEqual(len(saved), 1)
        review = saved[identity(row)]
        self.assertEqual(review['job_id'], '001')
        self.assertEqual(review['review_rating'], 3)
        self.assertEqual(review['new_fit_score'], 80)
        self.assertEqual(review['review_note'], '=literal note')
        self.assertEqual(review['issue_tags'], 'stack_mismatch')
        self.assertEqual(review['decision_quality'], 'worse')
        self.assertEqual(review['score_quality'], 'too_high')
        self.assertEqual(review['requirement_interpretation'], 'incorrect')
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

    def test_legacy_workbook_loads_and_gains_subgrades_without_losing_reviews(self):
        # An actual old-format workbook: no sub-grade columns, not even blank ones.
        legacy = dict(self.records[0], review_rating=2, review_note='Original note',
                      issue_tags='posting_ambiguity', reviewed=True, reviewed_at='2026-09-25T12:00:00+00:00')
        book = Workbook()
        book.active.append(list(legacy))
        book.active.append(list(legacy.values()))
        book.save(self.output)
        book.close()
        reviews = load_reviews(self.output)
        self.assertTrue(all(reviews[identity(self.records[0])][f] == '' for f in SUBGRADE_OPTIONS))
        app = self.app()
        next(w for w in app.selectbox if w.label == 'Review status').select('Reviewed')
        self.click(app, 'Load / rebuild queue')
        self.assertEqual(app.radio[0].value, 2)
        self.assertEqual(app.text_area[0].value, 'Original note')
        self.assertEqual(next(w for w in app.multiselect if w.label == 'Issue tags (optional)').value,
                         ['posting_ambiguity'])
        for label in ('Decision quality', 'Score quality', 'Requirement interpretation'):
            self.assertIsNone(next(w for w in app.selectbox if w.label == label).value)
        save_review(self.output, self.records[1], 1, decision_quality='same', score_quality='reasonable',
                    requirement_interpretation='correct')
        self.click(app, 'Save')
        reviews = load_reviews(self.output)
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[identity(self.records[0])]['review_note'], 'Original note')
        self.assertEqual(reviews[identity(self.records[0])]['issue_tags'], 'posting_ambiguity')
        self.assertEqual(reviews[identity(self.records[1])]['decision_quality'], 'same')
        self.assertEqual(reviews[identity(self.records[1])]['score_quality'], 'reasonable')
        self.assertEqual(reviews[identity(self.records[1])]['requirement_interpretation'], 'correct')

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
        labels = ('Decision quality', 'Score quality', 'Requirement interpretation')
        first_grades = ('better', 'reasonable', 'correct')
        for label, value in zip(labels, first_grades):
            widget = next(w for w in app.selectbox if w.label == label)
            self.assertIsNone(widget.value)
            widget.select(value)
        next(w for w in app.multiselect if w.label == 'Issue tags (optional)').select('requirement_semantics_issue')
        app.radio[0].set_value(1)
        self.click(app, 'Save + Next')
        self.assertEqual(app.subheader[0].value, 'Changed score')
        self.assertIsNone(app.radio[0].value)
        for label in labels:
            self.assertIsNone(next(w for w in app.selectbox if w.label == label).value)
        app.text_area[0].input('Unsaved draft')
        self.click(app, 'Previous')
        self.assertEqual(app.radio[0].value, 1)
        for label, value in zip(labels, first_grades):
            self.assertEqual(next(w for w in app.selectbox if w.label == label).value, value)
        self.assertEqual(next(w for w in app.multiselect if w.label == 'Issue tags (optional)').value,
                         ['requirement_semantics_issue'])
        updated_grades = ('worse', 'too_low', 'incorrect')
        for label, value in zip(labels, updated_grades):
            next(w for w in app.selectbox if w.label == label).select(value)
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
        reopened = self.app()
        next(w for w in reopened.selectbox if w.label == 'Review status').select('Reviewed')
        self.click(reopened, 'Load / rebuild queue')
        self.assertEqual(reopened.subheader[0].value, 'Changed decision')
        self.assertEqual(reopened.radio[0].value, 3)
        self.assertEqual(reopened.text_area[0].value, 'Decision needs correction')
        for label, value in zip(labels, updated_grades):
            self.assertEqual(next(w for w in reopened.selectbox if w.label == label).value, value)
        self.assertEqual(next(w for w in reopened.multiselect if w.label == 'Issue tags (optional)').value,
                         ['requirement_semantics_issue'])


if __name__ == '__main__':
    unittest.main()
