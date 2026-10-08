"""Compact failure modes from the 85-job review, not a fixture per posting."""
import copy
import csv
from pathlib import Path
import tempfile
import unittest

from skillfreq.calibration_review import compact_requirement_evidence
from skillfreq.score.grading import GradingContext, grade_job
from scripts.regrade_saved_cohort import replay
from scripts.compare_reviewed_calibration import selected_rows


class ReviewedCalibrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()

    def grade(self, text, title='Data Engineer', context=None):
        return grade_job(dict(title=title, description=text), context or self.context, prevalence={})

    def test_inline_optional(self):
        for wording in ('is a plus', 'a plus', 'nice to have', 'nice-to-have',
                        'is desired', 'is a bonus', 'is preferred', 'good to have'):
            for heading in ('Required qualifications:\n', 'Responsibilities:\n', ''):
                with self.subTest(wording=wording, heading=heading):
                    grade = self.grade(heading + 'Experience with AWS ' + wording + '.\nSQL required.')
                    self.assertNotIn('AWS', grade.missing_required_skills['atomic_skills'])
                    self.assertIn('AWS', grade.missing_preferred_skills['atomic_skills'])

    def test_optional_does_not_swallow_following_required(self):
        grade = self.grade('Required qualifications:\nAWS is nice to have.\nSpark required.')
        self.assertIn('Spark', grade.missing_required_skills['atomic_skills'])
        grade = self.grade('Required qualifications:\nSQL required, but AWS is a plus.\nSpark required.')
        self.assertIn('Spark', grade.missing_required_skills['atomic_skills'])

    def test_years_escaped_ranges_and_context(self):
        for text, expected in [(r'12\\+ years of experience in Python.', 12),
                               (r'Seven (7\\+) years of progressive experience.', 7),
                               ('10–12 years of engineering experience.', (10, 12)),
                               ('3 to 5 years of experience.', (3, 5)),
                               ('Required qualifications: SQL.\nExperience Required: 10 & Above', 10),
                               ('Our history spans over 200 years.\n7 years of experience required.', 7),
                               ('Our business has 20 years of history.', None),
                               ('-2 years of experience.', None),
                               ('AWS experience is preferred for 12 years.', None),
                               ('Preferred qualifications:\n12 years of experience.', None)]:
            with self.subTest(text=text):
                self.assertEqual(self.grade(text).seniority_signals['years_required'], expected)
        grade = self.grade('200 years of experience required.')
        self.assertIsNone(grade.seniority_signals['years_required'])
        self.assertTrue(grade.seniority_signals['years_anomalies'])

    def test_senior_is_not_automatically_lead_or_blocked(self):
        grade = self.grade('Required qualifications: SQL Python ETL data pipelines.\n4 years of experience.', 'Senior Data Engineer')
        self.assertFalse(grade.requirement_flags['is_lead_like'])
        self.assertIn('senior', grade.seniority_signals['terms'])
        self.assertFalse(grade.blocking_reasons)
        self.assertEqual(grade.apply_decision, 'manual_review')

    def test_title_levels_and_candidate_range(self):
        for level in ('Sr.', 'Lead', 'Staff', 'Principal', 'Manager', 'Director', 'VP', 'Architect'):
            with self.subTest(level=level):
                grade = self.grade('SQL ETL data pipelines.\n8 years of experience.', level + ' Data Engineer')
                self.assertTrue(grade.seniority_signals['title_levels'])
                self.assertEqual(grade.seniority_signals['experience_gap'], 4)
                self.assertNotEqual(grade.apply_decision, 'apply_now')
        context = copy.deepcopy(self.context)
        context.profile_config['experience_years'] = [8, 10]
        self.assertEqual(self.grade('8 years of experience.', context=context).seniority_signals['experience_gap'], 0)

    def test_clearance_current_versus_obtain(self):
        base = 'SQL ETL data pipelines.\nRequired qualifications:\n'
        for requirement in ('An ACTIVE and MAINTAINED "SECRET" Federal or DoD security clearance.',
                            'Must currently possess a Top Secret clearance.'):
            grade = self.grade(base + requirement)
            self.assertIn('active_clearance_unavailable', grade.blocking_reasons)
            self.assertEqual(grade.apply_decision, 'skip')
        for requirement in ('Must be able to obtain an active Secret clearance.',
                            'Must be eligible for Top Secret clearance.'):
            grade = self.grade(base + requirement)
            self.assertNotIn('active_clearance_unavailable', grade.blocking_reasons)
            self.assertIn('clearance_eligibility_review', grade.review_flags)
        for requirement in ('No clearance required.', 'Active Secret clearance is preferred.'):
            self.assertFalse(self.grade(base + requirement).requirement_flags['clearance_evidence'])
        incidental = self.grade('Our customers hold active Secret security clearances. We build SQL ETL data pipelines.')
        self.assertNotIn('active_clearance_unavailable', incidental.blocking_reasons)
        context = copy.deepcopy(self.context)
        context.profile_config['active_clearance'] = True
        self.assertNotIn('active_clearance_unavailable', self.grade(base + 'Active Secret clearance required.', context=context).blocking_reasons)

    def test_seniority_mismatch_tiers(self):
        text = 'Build SQL ETL data pipelines and data integration with Python.\n'
        modest = self.grade(text + '6 years of experience.', 'Senior Data Engineer')
        self.assertNotIn('extreme_seniority_experience_gap', modest.blocking_reasons)
        substantial = self.grade(text + '9 years of experience.', 'Principal Data Engineer')
        self.assertIn('substantial_experience_gap', substantial.review_flags)
        self.assertNotIn('extreme_seniority_experience_gap', substantial.blocking_reasons)
        extreme = self.grade(text + '10 years of experience.', 'Principal Data Engineer')
        self.assertIn('extreme_seniority_experience_gap', extreme.blocking_reasons)
        self.assertEqual(extreme.apply_decision, 'skip')
        no_ownership = self.grade(text + '10 years of experience.', 'Senior Data Engineer')
        self.assertNotIn('extreme_seniority_experience_gap', no_ownership.blocking_reasons)
        context = copy.deepcopy(self.context)
        context.profile_config['experience_years'] = [8, 10]
        suitable = self.grade(text + '10 years of experience.', 'Principal Data Engineer', context)
        self.assertNotIn('extreme_seniority_experience_gap', suitable.blocking_reasons)

    def test_unrelated_and_unfamiliar_titles(self):
        for title in ('Relief Valve Engineer', 'Relief Valve Technical Authority', 'Chief Inspector',
                      'Fixed Equipment Specialist', 'Sanctions Screening Director', 'Epic Payer Platform Lead'):
            grade = self.grade('Data validation, systems, APIs and reconciliation. Manage data quality and data mapping.', title)
            self.assertEqual(grade.role_lane, 'wrong_lane', title)
        for text in ('Develop stored procedures, schema design and query optimization in SQL.',
                     'Build ETL data pipelines, data integration and SQL database applications with Python.'):
            self.assertIn(self.grade(text, 'Information Flow Specialist').role_lane, ('target_lane', 'secondary_lane'))
        # Good-rated CVS and Kforce failure modes from the first structural replay.
        for title, text in [('Software Development Engineer', 'SQL constructs, Snowflake and software engineering fundamentals. Data warehouse and REST APIs.'),
                            ('Senior Developer', 'API development, programming languages Python and Java. CI/CD pipeline, Azure, Git and scalable solutions.')]:
            with self.subTest(title=title):
                self.assertEqual(self.grade(text, title).role_lane, 'secondary_lane')

    def test_good_fit_and_group_visibility(self):
        grade = self.grade('Build SQL ETL data pipelines and data integration with Python.\nRequired qualifications:\nSQL and Python.')
        self.assertEqual(grade.role_lane, 'target_lane')
        self.assertEqual(grade.apply_decision, 'apply_now')
        grade = self.grade('Required qualifications:\nDatabricks or Snowflake required.')
        summary = compact_requirement_evidence(grade.missing_required_skills)
        self.assertEqual(summary['atomic_skills'], [])
        self.assertEqual(len(summary['unsatisfied_groups']), 1)
        self.assertEqual(len([e for e in grade.triggered_rules if e['rule_id'] == 'fit_unsatisfied_required_group']), 1)

    def test_replay_never_overwrites_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'retained.csv'
            snapshot = out.with_suffix('.grading.yml')
            snapshot.write_text('retained')
            with self.assertRaises(FileExistsError):
                replay(Path(temp) / 'source.csv', out, True)
            self.assertEqual(snapshot.read_text(), 'retained')

    def test_comparison_rejects_missing_extra_and_duplicate_identities(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'cohort.csv'
            for ids in (['1', '1'], ['1', '2'], []):
                with path.open('w', newline='', encoding='utf-8') as stream:
                    writer = csv.DictWriter(stream, fieldnames=['source_site', 'id'])
                    writer.writeheader()
                    writer.writerows(dict(source_site='test', id=value) for value in ids)
                with self.subTest(ids=ids), self.assertRaises(ValueError):
                    selected_rows(path, {('test', '1')}, exact=True)


if __name__ == '__main__':
    unittest.main()
