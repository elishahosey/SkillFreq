"""Domain policy regression: mechanisms remain shared with all other grading."""
import copy
from pathlib import Path
import tempfile
import unittest

import yaml

from skillfreq.configuration import load_roles
from skillfreq.score.grading import GradingContext, grade_job


class DomainCalibrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = yaml.safe_load((Path(__file__).parent / 'fixtures/domain_calibration_jobs.yml').read_text())

    def test_domain_cases(self):
        for job in self.jobs:
            with self.subTest(job=job['name']):
                grade = grade_job(job, self.context, prevalence={'AWS':27, 'Airflow':4})
                self.assertEqual(grade.role_lane, job['expected_lane'])
                if job['name'] == 'modern_data':
                    self.assertGreater(grade.learning_score, 0)
                    self.assertFalse(any(e.get('category') == 'platform_heavy_terms'
                                         for e in grade.matched_role_signals))

    def test_confirmed_atomic_experience_not_inferred_to_mysql(self):
        job = dict(title='Database Developer', description=(
            'Build stored procedures and ETL. Required: SQL Server, PostgreSQL and MySQL.'))
        grade = grade_job(job, self.context)
        self.assertEqual(grade.missing_required_skills['atomic_skills'], ['MySQL'])
        self.assertEqual(self.context.profile_config['atomic_skills']['SQL Server'], 1)
        self.assertEqual(self.context.profile_config['atomic_skills']['PostgreSQL'], .7)
        self.assertIn('Candidate-confirmed', self.context.snapshot['profile']['atomic_skill_notes']['PostgreSQL'])
        job['description'] = ('Build SQL ETL data pipelines. '
                              'Preferred: SQL Server, PostgreSQL and MySQL.')
        grade = grade_job(job, self.context, prevalence={'PostgreSQL':20})
        self.assertEqual(grade.missing_preferred_skills['atomic_skills'], ['MySQL'])
        self.assertEqual(grade.learning_score, 0)

    def test_ecosystem_eligibility_is_configuration_owned(self):
        job = next(j for j in self.jobs if j['name'] == 'ecosystem_with_data')
        context = copy.deepcopy(self.context)
        next(r for r in context.roles['eligibility_rules'] if r['id'] == 'ecosystem_identity_guard')['active'] = False
        self.assertEqual(grade_job(job, self.context).role_lane, 'secondary_lane')
        self.assertEqual(grade_job(job, context).role_lane, 'target_lane')

    def test_identity_configuration_errors_fail_at_load(self):
        mutations = {
            'unknown_identity': lambda r: next(x for x in r['eligibility_rules'] if x['id'] == 'database_and_data_stack_evidence')['when']['all'][0].update(field='hits.missing_identity'),
            'unknown_group': lambda r: r['lane_rules'][-1].update(group='identity.missing'),
            'malformed_pattern': lambda r: next(x for x in r['lane_rules'] if 'title_pattern' in x).update(title_pattern={'any':['qa']}),
            'invalid_action': lambda r: r['eligibility_rules'][-1]['actions'][0].update(op='execute'),
            'invalid_operator': lambda r: next(x for x in r['eligibility_rules'] if x['id'] == 'database_and_data_stack_evidence')['when']['all'][0].update(op='approximately'),
            'duplicate_id': lambda r: r['eligibility_rules'].append(copy.deepcopy(r['eligibility_rules'][-1])),
            'invalid_lane': lambda r: r['lane_rules'][-1].update(lane='primary_lane'),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'roles.yml'
            for name, mutate in mutations.items():
                config = copy.deepcopy(self.context.snapshot['roles'])
                mutate(config)
                path.write_text(yaml.safe_dump(config), encoding='utf-8')
                with self.subTest(name=name), self.assertRaises(ValueError):
                    load_roles(path)
