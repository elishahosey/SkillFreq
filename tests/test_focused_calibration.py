"""Focused post-refresh calibration: representation, experience and identity."""
import copy
from pathlib import Path
import unittest

import yaml

from skillfreq.score.grading import GradingContext, grade_job


class FocusedCalibrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = {j['name']: j for j in yaml.safe_load(
            (Path(__file__).parent / 'fixtures/focused_calibration_jobs.yml').read_text())}

    def grade(self, name, context=None):
        return grade_job(self.jobs[name], context or self.context)

    def test_backend_heading_and_alternative(self):
        g = self.grade('backend_requirements')
        self.assertEqual(set(g.missing_required_skills['atomic_skills']), {'AWS', 'MySQL', 'Kubernetes'})
        alternatives = [x for x in g.missing_required_skills['requirement_groups'] if x['type'] == 'any_of']
        self.assertEqual(alternatives[0]['skills'], ['Python', 'Kotlin'])
        self.assertTrue(alternatives[0]['satisfied'])

    def test_vendor_products_are_not_generic_cloud_or_examples(self):
        g = self.grade('vendor_requirements')
        self.assertTrue({'Adobe Journey Optimizer', 'Adobe Experience Platform'} <=
                        set(g.missing_required_skills['atomic_skills']))
        self.assertNotIn('Adobe Journey Optimizer Decisioning', g.missing_required_skills['atomic_skills'])
        self.assertIn('Adobe Journey Optimizer Decisioning', g.missing_preferred_skills['atomic_skills'])
        self.assertEqual(g.seniority_signals['years_required'], 5)
        self.assertNotIn('extreme_seniority_experience_gap', g.blocking_reasons)
        self.assertIn('ecosystem_specific_experience', g.review_flags)

    def test_inline_preference_does_not_change_following_requirements(self):
        g = self.grade('networking_requirements')
        self.assertTrue({'network_architecture', 'firewall_administration'} <=
                        set(g.missing_required_skills['capability_concepts']))
        self.assertIn('Linux', g.missing_required_skills['atomic_skills'])
        self.assertNotIn('AWS', g.missing_required_skills['atomic_skills'])
        self.assertIn('AWS', g.missing_preferred_skills['atomic_skills'])
        g = grade_job({'description': 'Responsibilities:\nNetworking architecture and firewall administration is a must.'}, self.context)
        self.assertIn('firewall_administration', g.missing_required_skills['capability_concepts'])

    def test_java_examples_and_preferred_cicd(self):
        g = self.grade('java_web_requirements')
        self.assertEqual(g.seniority_signals['years_required'], 2)
        self.assertIn('Spring', g.missing_required_skills['atomic_skills'])
        group = g.missing_required_skills['unsatisfied_groups'][0]
        self.assertEqual(group['type'], 'any_of')
        self.assertTrue({'Java', 'CSS', 'HTML', 'XSLT', 'JavaScript', 'JUnit', 'Oracle Database'} <= set(group['skills']))
        preferred = g.missing_preferred_skills
        self.assertIn('ci_cd', preferred['capability_concepts'])
        self.assertTrue(any('Azure DevOps' in x['skills'] and not x['satisfied'] for x in preferred['unsatisfied_groups']))
        self.assertNotIn('ci_cd', g.missing_required_skills['capability_concepts'])
        self.assertIn('concurrent_programming', g.missing_required_skills['capability_concepts'])

    def test_domain_preference_and_prose_requirements_word(self):
        g = self.grade('domain_requirements')
        self.assertIn('healthcare_supply_chain', g.missing_required_skills['capability_concepts'])
        self.assertNotIn('federal_health', g.missing_required_skills['capability_concepts'])
        self.assertIn('federal_health', g.missing_preferred_skills['capability_concepts'])
        self.assertIsNone(g.seniority_signals['years_required'])

    def test_streaming_identity_and_scoped_alternatives(self):
        g = self.grade('streaming_data_identity')
        self.assertEqual(g.role_lane, 'target_lane')
        self.assertIn('Kafka', g.missing_required_skills['atomic_skills'])
        self.assertNotIn('AWS', g.missing_required_skills['atomic_skills'])
        self.assertNotIn('Google Cloud', g.missing_required_skills['atomic_skills'])
        groups = g.missing_required_skills['requirement_groups']
        self.assertTrue(any(x['type'] == 'equivalent' and x['skills'] == ['Python'] for x in groups))
        self.assertTrue(any(x['type'] == 'any_of' and 'Azure' in x['skills'] and x['satisfied'] for x in groups))

    def test_software_identity_and_preferred_storage(self):
        g = self.grade('software_development_identity')
        self.assertEqual(g.role_lane, 'secondary_lane')
        self.assertEqual(set(g.missing_required_skills['atomic_skills']), {'C++', 'Bash', 'Linux'})
        self.assertIn('concurrent_programming', g.missing_required_skills['capability_concepts'])
        self.assertTrue({'memory_management', 'storage_technologies'} <= set(g.missing_preferred_skills['capability_concepts']))
        sparse = grade_job({'title': 'Engineer I-Software Development', 'description': 'Python systems and APIs.'}, self.context)
        self.assertEqual(sparse.role_lane, 'wrong_lane')

    def test_healthy_target_and_strong_plus(self):
        g = self.grade('healthy_target')
        self.assertEqual(g.role_lane, 'target_lane')
        self.assertEqual(g.apply_decision, 'apply_now')
        self.assertGreaterEqual(g.fit_score, 80)
        self.assertNotIn('Spark', g.missing_required_skills['atomic_skills'])
        self.assertIn('Spark', g.missing_preferred_skills['atomic_skills'])

    def test_inline_heading_and_unknown_alternative_remain_scoped(self):
        g = grade_job({'description': 'Required: SQL\nPreferred: AWS\nKubernetes'}, self.context)
        self.assertEqual(set(g.missing_preferred_skills['atomic_skills']), {'AWS', 'Kubernetes'})
        self.assertEqual(g.missing_required_skills['atomic_skills'], [])
        g = grade_job({'description': 'Required: Java or another JVM language.'}, self.context)
        self.assertEqual(g.missing_required_skills['atomic_skills'], [])
        self.assertEqual(g.missing_required_skills['requirement_groups'][0]['type'], 'any_of')

    def test_url_extensions_are_not_web_skill_requirements(self):
        g = grade_job({'description': 'Required: See https://example.test/apply.html\nJavaScript experience.'}, self.context)
        self.assertEqual(g.missing_required_skills['atomic_skills'], ['JavaScript'])
        self.assertNotIn('HTML', [m['canonical_skill'] for m in g.matched_atomic_skills])
        g = grade_job({'description': 'Required: HTML and JavaScript. See https://example.test/apply.html'}, self.context)
        self.assertEqual(set(g.missing_required_skills['atomic_skills']), {'HTML', 'JavaScript'})

    def test_monotonic_experience_policy_and_profile_range(self):
        for title in ('Data Engineer', 'Senior Data Engineer', 'Principal Data Engineer'):
            grades = [grade_job({'title': title, 'description':
                f'Build SQL ETL data pipelines and data integration with Python.\nRequired qualifications:\n{years} years of experience.'}, self.context)
                for years in range(4, 11)]
            scores = [g.fit_score for g in grades]
            self.assertEqual(scores, sorted(scores, reverse=True))
            self.assertEqual(grades[1].apply_decision, 'manual_review')
            self.assertEqual(grades[2].apply_decision, 'manual_review')
            self.assertFalse(grades[2].blocking_reasons)
            self.assertLessEqual(grades[4].fit_score, 54)
            if title.startswith('Principal'):
                self.assertEqual(grades[3].apply_decision, 'skip')
        context = copy.deepcopy(self.context)
        context.profile_config['experience_years'] = [7, 9]
        suitable = grade_job({'title': 'Principal Data Engineer', 'description':
                             'SQL ETL data pipelines. Required qualifications: 8 years of experience.'}, context)
        self.assertFalse(suitable.blocking_reasons)
        self.assertEqual(suitable.seniority_signals['experience_gap'], 0)

    def test_ownership_combines_with_years_and_preferred_years_do_not(self):
        base = 'Build SQL ETL data pipelines. Lead engineering teams.\nRequired qualifications:\n'
        large = grade_job({'title': 'Data Engineer', 'description': base + '7 years of experience.'}, self.context)
        self.assertIn('extreme_seniority_experience_gap', large.blocking_reasons)
        modest = grade_job({'title': 'Data Engineer', 'description': base + '6 years of experience.'}, self.context)
        self.assertNotIn('extreme_seniority_experience_gap', modest.blocking_reasons)
        preferred = grade_job({'title': 'Senior Data Engineer', 'description':
                              'SQL ETL data pipelines.\nPreferred qualifications:\n8 years of experience.'}, self.context)
        self.assertIsNone(preferred.seniority_signals['experience_gap'])

    def test_wrong_occupations_still_win_over_new_positive_evidence(self):
        text = ('SQL Python cloud APIs systems. Build streaming pipelines and data contracts. '
                'Software developer with programming experience. Develop automated tests.')
        for title in ('Relief Valve Engineer', 'Chief Inspector', 'Fixed Equipment Specialist',
                      'QA Software Development Engineer', 'Test Automation Engineer',
                      'Sanctions Screening Director', 'Epic Payer Platform Lead'):
            with self.subTest(title=title):
                g = grade_job({'title': title, 'description': text}, self.context)
                self.assertEqual(g.role_lane, 'wrong_lane')
                self.assertEqual(g.apply_decision, 'skip')


if __name__ == '__main__':
    unittest.main()
