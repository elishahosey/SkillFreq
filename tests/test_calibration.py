import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from skillfreq.configuration import load_roles, validate_grading_settings
from skillfreq.score.grading import GradingContext, grade_job
from skillfreq.score.policy import evaluate_rules, validate_rules


class CalibrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = yaml.safe_load((Path(__file__).parent/'fixtures/calibration_jobs.yml').read_text())
        cls.prevalence = {'Airflow':2.3,'AWS':27.9,'Snowflake':4.7,'Databricks':3.7,'Docker':6.5}

    def test_career_policy_regressions(self):
        for job in self.jobs:
            with self.subTest(job=job['name']):
                grade = grade_job(job,self.context,prevalence=self.prevalence)
                self.assertEqual(grade.role_lane,job['expected_lane'])
                if 'expected_decision' in job:
                    self.assertEqual(grade.apply_decision,job['expected_decision'])
                if job.get('learning'):
                    self.assertGreater(grade.learning_score,0)
                if job.get('blocker'):
                    self.assertIn(job['blocker'],grade.blocking_reasons)
                if job.get('ai'):
                    self.assertTrue(grade.ai_review_required)
                if job.get('no_platform_evidence'):
                    self.assertFalse(any(e.get('category')=='platform_heavy_terms' for e in grade.matched_role_signals))

    def test_atomic_profile_is_explicit_and_independent(self):
        context = copy.deepcopy(self.context)
        context.profile_config['atomic_skills'].update({'SQL Server':0.8,'PostgreSQL':0.7})
        job = dict(title='SQL Developer',description='Build ETL data integration. Required: SQL Server, PostgreSQL and MySQL.')
        grade = grade_job(job,context)
        self.assertEqual(grade.missing_required_skills['atomic_skills'],['MySQL'])
        self.assertIn('sql',grade.matched_capability_concepts)

    def test_high_fit_blocker_explains_skip_without_relabeling_score(self):
        facts = dict(always=True,fit_score=96,role_lane='target_lane',blockers=['explicit_gate'],
                     review_flags=[],ai_review_required=False,search_lane='')
        evidence = evaluate_rules(facts,self.context.settings['quality_rules'],'decision')
        evidence += evaluate_rules(facts,self.context.settings['decision_rules'],'decision')
        self.assertEqual(facts['fit_quality'],'good_fit')
        self.assertEqual(facts['apply_decision'],'skip')
        self.assertEqual(evidence[-1]['rule_id'],'configured_hard_blocker')
        facts['blockers']=[]
        evaluate_rules(facts,self.context.settings['decision_rules'],'decision')
        self.assertEqual(facts['apply_decision'],'apply_now')

    def test_threshold_change_requires_only_configuration(self):
        context = copy.deepcopy(self.context)
        rule = next(r for r in context.settings['decision_rules'] if r['id']=='strong_primary_fit')
        rule['when']['all'][1]['value']=100
        job=self.jobs[0]
        before=grade_job(job,self.context,prevalence=self.prevalence)
        after=grade_job(job,context,prevalence=self.prevalence)
        self.assertEqual(before.apply_decision,'apply_now')
        self.assertEqual(after.apply_decision,'manual_review')
        self.assertEqual(before.fit_score,after.fit_score)

    def test_market_failure_is_null_and_loaded_once_per_run(self):
        from skillfreq.pipeline import grade_database
        with tempfile.TemporaryDirectory() as directory, \
             patch('skillfreq.pipeline.load_jobs_for_grading',return_value=[self.jobs[0]]*3), \
             patch('skillfreq.pipeline.load_prevalence',side_effect=RuntimeError('timeout')) as load:
            with self.assertLogs(level='WARNING') as logs:
                results=grade_database(Path(directory)/'grades.csv',context=self.context)
            load.assert_called_once()
            self.assertIn('NULL',logs.output[0])
            self.assertTrue(all(r.deterministic_grade['learning_score'] is None for r in results))

    def test_degree_equivalence_and_preferred_years_do_not_create_gates(self):
        job=dict(self.jobs[0])
        job['description'] += '\nRequired qualifications: BS or equivalent experience.\nPreferred: 10 years experience.'
        grade=grade_job(job,self.context,prevalence=self.prevalence)
        self.assertFalse(grade.ai_review_required)
        self.assertIsNone(grade.seniority_signals['years_required'])

    def test_optional_search_context_is_audited(self):
        grade=grade_job(self.jobs[0],self.context)
        self.assertEqual(grade.input_context['search_lane'],dict(value='',available=False))

    def test_explicit_required_experience_is_numeric_evidence(self):
        job=dict(self.jobs[0])
        job['description'] += '\nExperience Required: 10 & Above'
        grade=grade_job(job,self.context,prevalence=self.prevalence)
        self.assertEqual(grade.seniority_signals['years_required'],10)
        self.assertIn('overlevel_experience',grade.review_flags)
        self.assertEqual(grade.apply_decision,'manual_review')

    def test_cached_matcher_preserves_boundary_evidence(self):
        import re
        from skillfreq.skills.text import term_counts, normalize_text
        terms=['sql','postgres','c++','data pipeline','aws','python','SQL','']
        for text in ['Postgres and PostgreSQL; postgres twice.','NOSQL SQL sql_server',
                     'C++ and data\n pipeline, AWS Python','nothing applicable', 'AWSome']:
            normalized=normalize_text(text)
            expected={}
            for term in dict.fromkeys(normalize_text(t) for t in terms):
                if term:
                    n=len(re.findall(r'(?<!\w)'+re.escape(term)+r'(?!\w)',normalized))
                    if n: expected[term]=n
            self.assertEqual(term_counts(text,terms),expected)

    def test_invalid_policies_fail_at_load(self):
        base=copy.deepcopy(self.context.settings)
        mutations = [
            lambda w: w['decision_rules'][0]['when'].update(op='execute'),
            lambda w: w['decision_rules'][0]['actions'][0].update(op='call_python'),
            lambda w: w['decision_rules'].append(copy.deepcopy(w['decision_rules'][0])),
            lambda w: w['fit']['lane_caps'].update(unknown_lane=80),
            lambda w: w['confidence'].update(review_below=1.1),
            lambda w: w['learning'].update(prevalence_saturation_pct=0),
            lambda w: w['fit']['rules'][0]['actions'][0].update(value=-30),
            lambda w: w['quality_rules'][0]['when'].update(value=101),
            lambda w: w['decision_rules'][0]['actions'].append(copy.deepcopy(w['decision_rules'][0]['actions'][0])),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                w=copy.deepcopy(base); mutate(w)
                with self.assertRaises(ValueError): validate_grading_settings(w,self.context.roles)

    def test_invalid_role_patterns_and_references(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'roles.yml'
            for change in ('pattern','group','cycle','lane'):
                r=copy.deepcopy(self.context.snapshot['roles'])
                if change=='pattern':
                    next(x for x in r['lane_rules'] if 'title_pattern' in x)['title_pattern']={'any':['qa']}
                elif change=='group': r['lane_rules'][0]['group']='missing'
                elif change=='cycle': r['term_groups']['cycle']='cycle'
                else: r['lane_rules'][0]['lane']='primary'
                path.write_text(yaml.safe_dump(r))
                with self.subTest(change=change), self.assertRaises(ValueError): load_roles(path)

    def test_inactive_policy_does_not_act(self):
        facts=dict(always=True,fit_score=90)
        rule=dict(id='disabled',priority=1,active=False,
                  when=dict(field='always',op='equals',value=True),
                  actions=[dict(op='subtract_score',field='fit_score',value=30)])
        validate_rules([rule],set(facts),dict(fit_score='score'))
        self.assertEqual(evaluate_rules(facts,[rule],'fit'),[])
        self.assertEqual(facts['fit_score'],90)
