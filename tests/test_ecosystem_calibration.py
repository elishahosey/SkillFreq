import copy
from pathlib import Path
import unittest

import yaml

from skillfreq.configuration import validate_grading_settings
from skillfreq.score.grading import GradingContext, grade_job


class EcosystemCalibrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = {j['name']: j for j in yaml.safe_load(
            (Path(__file__).parent/'fixtures/ecosystem_jobs.yml').read_text())}

    def test_role_and_counterweight_cases(self):
        for name, job in self.jobs.items():
            with self.subTest(name=name):
                grade = grade_job(job, self.context)
                if job.get('not_target'):
                    self.assertNotEqual(grade.role_lane, 'target_lane')
                else:
                    self.assertEqual(grade.role_lane, job['lane'])

    def test_modern_platforms_are_not_enterprise_specialization(self):
        for name in ('palantir_data','modern_stack'):
            grade = grade_job(self.jobs[name], self.context)
            self.assertFalse(grade.policy_flags['ecosystem_role_concentration'])
            self.assertFalse(any(e['rule_id']=='ecosystem_usage_penalty' for e in grade.triggered_rules))

    def test_same_declared_flags_drive_fit_and_lane_audit(self):
        grade = grade_job(self.jobs['transferable_specialist'], self.context)
        self.assertTrue(grade.policy_flags['ecosystem_role_concentration'])
        self.assertTrue(grade.policy_flags['transferable_data_strong'])
        self.assertIn('ecosystem_specialization_review', grade.review_flags)
        self.assertNotIn('ecosystem_ownership_gap', grade.blocking_reasons)
        self.assertTrue(any(e['rule_id']=='ecosystem_transferable_specialist_fit' for e in grade.triggered_rules))
        self.assertEqual(grade.to_dict()['policy_flags'], grade.policy_flags)

    def test_accepting_specialization_needs_only_configuration(self):
        context = copy.deepcopy(self.context)
        next(r for r in context.roles['eligibility_rules'] if r['id']=='ecosystem_identity_guard')['active']=False
        before = grade_job(self.jobs['transferable_specialist'], self.context)
        after = grade_job(self.jobs['transferable_specialist'], context)
        self.assertEqual(before.role_lane,'secondary_lane')
        self.assertEqual(after.role_lane,'target_lane')
        self.assertIn('ecosystem_specialization_review',after.review_flags)

    def test_unknown_cross_stage_flag_rejected(self):
        settings = copy.deepcopy(self.context.settings)
        next(r for r in settings['fit']['rules'] if r['id']=='ecosystem_dependence')['when']['field']='flags.misspelled'
        with self.assertRaisesRegex(ValueError,'Unknown policy field'):
            validate_grading_settings(settings,self.context.roles)
