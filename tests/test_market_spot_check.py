"""Five reviewed market jobs: one vocabulary fix, no broad recalibration."""
import copy
from pathlib import Path
import unittest

import yaml

from skillfreq.score.grading import GradingContext, grade_job


class MarketSpotCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = {row['id']: row for row in yaml.safe_load(
            (Path(__file__).parent / 'fixtures/market_spot_check_jobs.yml').read_text(encoding='utf-8'))}
        cls.before = copy.deepcopy(cls.context)
        terms = cls.before.roles['resolved_groups']['ecosystem.specialization']
        for term in ('core boomi components', 'code within the boomi environment'):
            terms.remove(term)

    def test_required_vendor_development_uses_existing_specialization_policy(self):
        job = self.jobs['in-12212552d5d9b1fa']
        before = grade_job(job, self.before)
        after = grade_job(job, self.context)
        # Expanded requirement vocabulary now captures required JavaScript.
        # Keep the specialization comparison isolated from that shared change.
        self.assertIn('JavaScript', before.missing_required_skills['atomic_skills'])
        self.assertEqual(before.fit_score, 81.82)
        self.assertEqual(before.apply_decision, 'apply_now')
        self.assertFalse(before.policy_flags['ecosystem_specialized'])
        self.assertEqual(after.role_lane, 'target_lane')
        self.assertEqual(after.fit_score, 73.82)
        self.assertEqual(before.fit_score - after.fit_score, 8)
        self.assertEqual(after.fit_quality, 'possible_fit')
        self.assertEqual(after.apply_decision, 'manual_review')
        self.assertTrue(after.policy_flags['ecosystem_specialized'])
        self.assertTrue(after.policy_flags['transferable_data_strong'])
        self.assertFalse(after.policy_flags['ecosystem_role_concentration'])
        self.assertFalse(after.blocking_reasons)
        self.assertEqual(after.review_flags, ['ecosystem_specialization_review'])
        self.assertEqual(before.missing_required_skills, after.missing_required_skills)
        self.assertEqual(before.missing_preferred_skills, after.missing_preferred_skills)
        evidence = next(e for e in after.matched_role_signals
                        if e['category'] == 'ecosystem_specialization')
        self.assertEqual(set(evidence['matched_terms']),
                         {'core boomi components', 'code within the boomi environment'})
        self.assertTrue(any(e['rule_id'] == 'ecosystem_transferable_specialist_fit'
                            and e['contribution'] == -8 for e in after.triggered_rules))

    def test_incidental_usage_and_one_repeated_cue_do_not_establish_specialization(self):
        base = 'Build SQL Python ETL data pipelines APIs XML JSON data mapping. Boomi is an integration tool. '
        for detail in ('', 'Connectors and components run in an environment. ',
                       'Know core Boomi components. ' * 3,
                       'Write custom code within the Boomi environment. ' * 3):
            with self.subTest(detail=detail):
                job = dict(title='Data Integration Engineer', description=base + detail)
                before = grade_job(job, self.before)
                after = grade_job(job, self.context)
                self.assertFalse(after.policy_flags['ecosystem_specialized'])
                self.assertEqual(after.role_lane, 'target_lane')
                self.assertEqual(after.fit_score, before.fit_score)
                self.assertEqual(after.apply_decision, before.apply_decision)
                self.assertNotIn('ecosystem_specialization_review', after.review_flags)

    def test_known_good_role_exclusions_remain_intact(self):
        for job_id in ('in-7fb8f90cfca11195', 'li-4459650362', 'li-4446676420'):
            with self.subTest(job_id=job_id):
                job = self.jobs[job_id]
                before = grade_job(job, self.before)
                after = grade_job(job, self.context)
                self.assertEqual(after.to_dict(), before.to_dict())
                self.assertEqual(after.role_lane, 'wrong_lane')
                self.assertEqual(after.fit_score, 15)
                self.assertEqual(after.apply_decision, 'skip')
                self.assertIn('wrong_role_identity', after.blocking_reasons)
                self.assertTrue(after.confidence_evidence['hard_exclusion_override'])
        devops = grade_job(self.jobs['li-4446676420'], self.context)
        self.assertEqual(devops.seniority_signals['experience_gap'], 4)
        self.assertTrue({'lead_responsibility', 'overlevel_experience', 'clearance_eligibility_review'}
                        <= set(devops.review_flags))

    def test_mixed_ai_automation_remains_an_explicit_policy_question(self):
        job = self.jobs['in-85165dc0ecbc4c68']
        grade = grade_job(job, self.context)
        self.assertEqual(grade.to_dict(), grade_job(job, self.before).to_dict())
        exclusion = next(e for e in grade.matched_role_signals if e['category'] == 'wrong_desc_terms')
        self.assertEqual(set(exclusion['matched_terms']),
                         {'prompt engineering', 'ai agents', 'machine learning'})
        self.assertEqual(exclusion['contribution'], 36)
        self.assertEqual(set(grade.lane_resolution['eligible']), {'wrong_lane', 'bridge_lane'})
        self.assertEqual(grade.lane_scores['bridge_lane'], 22)
        self.assertEqual(grade.role_lane, 'wrong_lane')
        self.assertEqual(grade.fit_score, 15)
        self.assertEqual(grade.apply_decision, 'skip')
        self.assertEqual(grade.confidence, .466)
        self.assertTrue(grade.ai_review_required)
        self.assertEqual(grade.blocking_reasons, ['wrong_role_identity'])
        self.assertFalse(grade.confidence_evidence.get('hard_exclusion_override'))
        self.assertIn('positive_and_exclusion_signals', grade.ai_review_reasons)
        self.assertFalse(any(e['rule_id'] == 'description_exclusion_guard' for e in grade.triggered_rules))


if __name__ == '__main__':
    unittest.main()
