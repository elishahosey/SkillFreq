import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from skillfreq.configuration import CONFIG_DIR, evaluation_config, load_roles
from skillfreq.score.grading import GradingContext, grade_job, calculate_confidence, should_request_ai_review
from skillfreq.score.lane_classifier import score_lanes
from skillfreq.skills.extract import extract_sections
from skillfreq.skills.job_market import extract_market_skills


class GradingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = {j['name']: j for j in yaml.safe_load((Path(__file__).parent/'fixtures/lane_jobs.yml').read_text())}

    def grade(self, name, **kwargs):
        return grade_job(self.jobs[name], self.context, **kwargs)

    def test_lane_regressions_and_documented_changes(self):
        changed = []
        for name, job in self.jobs.items():
            with self.subTest(name=name):
                grade = self.grade(name)
                self.assertEqual(grade.role_lane, job['expected_lane'])
                if grade.role_lane != job['legacy_lane']:
                    changed.append(name)
        self.assertEqual(changed, ['generic_software_data', 'ambiguous'])

    def test_atomic_postgres_is_not_generic_sql(self):
        grade = grade_job({'description':'PostgreSQL and postgres'}, self.context)
        self.assertEqual([m['canonical_skill'] for m in grade.matched_atomic_skills], ['PostgreSQL'])
        self.assertIn('sql', grade.matched_capability_concepts)
        self.assertEqual(grade.matched_atomic_skills[0]['mention_count'], 2)

    def test_sql_server_aliases(self):
        matches = extract_market_skills('MSSQL and Microsoft SQL Server', self.context.taxonomy)
        self.assertEqual([m.canonical_skill for m in matches], ['SQL', 'SQL Server'])
        self.assertEqual(next(m for m in matches if m.canonical_skill=='SQL Server').matched_terms,
                         ('microsoft sql server', 'sql server', 'mssql'))

    def test_inactive_rules_are_ignored(self):
        config = copy.deepcopy(self.context.roles)
        config['lane_rules'] = [dict(id='test',category='test',signal_type='title',pattern='engineer',
            scope='title',lane='wrong_lane',weight=100,hard_exclusion=True,active=False,max_hits=1)]
        result = score_lanes({'title':'Engineer'}, config)
        self.assertEqual(result.hard_exclusions, [])
        self.assertFalse(any(e.get('rule_id')=='test' for e in result.triggered_rules))

    def test_hard_exclusion_beats_data_overlap(self):
        grade = self.grade('ml')
        self.assertEqual(grade.role_lane, 'wrong_lane')
        self.assertTrue(grade.confidence_evidence['hard_exclusion_override'])
        self.assertFalse(grade.ai_review_required)

    def test_search_origin_is_not_ground_truth(self):
        for lane in ['target','bridge','survival']:
            grade = grade_job(dict(self.jobs['frontend'], search_lane=lane), self.context)
            self.assertEqual(grade.role_lane, 'wrong_lane')
        grade = grade_job(dict(self.jobs['obvious_target'], search_lane='survival'), self.context)
        self.assertEqual(grade.role_lane, 'target_lane')
        self.assertEqual(grade.apply_decision, 'manual_review')

    def test_high_fit_low_learning_and_moderate_fit_high_learning(self):
        prevalence = {'Airflow':27, 'AWS':30, 'Snowflake':20, 'Spark':20}
        high = self.grade('obvious_target', prevalence=prevalence)
        growth = self.grade('learning_opportunity', prevalence=prevalence)
        self.assertGreater(high.fit_score, 90)
        self.assertEqual(high.learning_score, 0)
        self.assertLess(growth.fit_score, high.fit_score)
        self.assertGreater(growth.learning_score, 80)
        self.assertIn('Airflow', growth.missing_required_skills['atomic_skills'])
        self.assertTrue(any(e.get('skill')=='Airflow' and e.get('contribution',0)<0 for e in growth.triggered_rules))

    def test_prevalence_increases_learning_without_affecting_fit(self):
        low = self.grade('learning_opportunity', prevalence={'Airflow':3})
        high = self.grade('learning_opportunity', prevalence={'Airflow':30})
        self.assertGreater(high.learning_score, low.learning_score)
        self.assertEqual(high.fit_score, low.fit_score)

    def test_no_market_data_is_explicit(self):
        grade = self.grade('learning_opportunity')
        self.assertIsNone(grade.learning_score)
        self.assertEqual(grade.learning_status, 'unavailable')
        self.assertIn('market_prevalence_unavailable', grade.reason_codes)

    def test_missing_unaligned_or_non_adjacent_skills_are_not_rewarded(self):
        grade = grade_job({'title':'Data Engineer','description':'Build ETL data pipelines using SQL, Tableau and Kubernetes.'}, self.context,
                          prevalence={'Tableau':90,'Kubernetes':90})
        self.assertEqual(grade.learning_score, 0)
        context = copy.deepcopy(self.context)
        context.profile = {}
        grade = grade_job(self.jobs['learning_opportunity'], context, prevalence={'Airflow':90})
        self.assertEqual(grade.learning_score, 0)
        self.assertEqual(self.grade('ml', prevalence={'AWS':90}).learning_score, 0)

    def test_close_scores_reduce_confidence(self):
        lanes = score_lanes(self.jobs['obvious_target'], self.context.roles)
        settings = self.context.settings['confidence']
        wide, _ = calculate_confidence(lanes, self.jobs['obvious_target']['description'], False, settings)
        lanes.lane_scores.update(target_lane=51, secondary_lane=48)
        close, _ = calculate_confidence(lanes, self.jobs['obvious_target']['description'], False, settings)
        self.assertLess(close, wide)

    def test_ambiguity_requests_review_but_obvious_jobs_do_not(self):
        grade = self.grade('ambiguous')
        self.assertTrue(should_request_ai_review(grade))
        self.assertTrue(grade.ai_review_reasons)
        self.assertFalse(self.grade('obvious_target').ai_review_required)
        self.assertFalse(self.grade('frontend').ai_review_required)

    def test_requirement_ambiguity_is_a_review_reason(self):
        job = dict(self.jobs['obvious_target'])
        job['description'] += '\nRequired qualifications: Airflow or equivalent experience.'
        grade = grade_job(job, self.context)
        self.assertTrue(grade.ai_review_required)
        self.assertIn('ambiguous_requirements', grade.ai_review_reasons)

    def test_repeated_and_overlapping_section_headings(self):
        sections = extract_sections('Required qualifications: SQL\nPreferred qualifications: AWS\nRequired qualifications: Python')
        self.assertIn('sql', sections['required'])
        self.assertIn('python', sections['required'])
        self.assertIn('aws', sections['preferred'])
        self.assertNotIn('sql', sections['preferred'])

    def test_required_wins_over_preferred_without_double_penalty(self):
        job = dict(self.jobs['obvious_target'], description='Required: Airflow\nPreferred: Airflow')
        grade = grade_job(job, self.context)
        self.assertIn('Airflow', grade.missing_required_skills['atomic_skills'])
        self.assertNotIn('Airflow', grade.missing_preferred_skills['atomic_skills'])

    def test_lead_titles_and_escaped_years(self):
        job = dict(self.jobs['obvious_target'], title='Lead Data Engineer')
        job['description'] += '\nRequired qualifications: 5\\+ years of experience.'
        grade = grade_job(job, self.context)
        self.assertIn('lead', grade.seniority_signals['terms'])
        self.assertEqual(grade.seniority_signals['years_required'], 5)
        self.assertNotEqual(grade.apply_decision, 'apply_now')

    def test_versions_change_with_configuration_and_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'profile.yml'
            profile = copy.deepcopy(self.context.profile_config)
            profile['atomic_skills']['Airflow'] = 1
            path.write_text(yaml.safe_dump(profile))
            context = GradingContext.load(profile_path=path)
            grade = grade_job(self.jobs['learning_opportunity'], context, prevalence={'Airflow':30})
            self.assertNotEqual(context.grading_version, self.context.grading_version)
            self.assertEqual(context.taxonomy_version, self.context.taxonomy_version)
            self.assertNotIn('Airflow', grade.missing_required_skills['atomic_skills'])
            self.assertFalse(any(g['skill']=='Airflow' for g in grade.growth_skills))

    def test_invalid_reference_and_duplicate_rule_fail_fast(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'roles.yml'
            roles = copy.deepcopy(self.context.snapshot['roles'])
            roles['lane_rules'].append(roles['lane_rules'][0])
            path.write_text(yaml.safe_dump(roles))
            with self.assertRaisesRegex(ValueError, 'Duplicate rule'):
                load_roles(path)

    def test_point_ledgers_reconcile_and_grade_is_json_serializable(self):
        grade = self.grade('learning_opportunity', prevalence={'Airflow':30})
        self.assertAlmostEqual(sum(e['contribution'] for e in grade.triggered_rules if e['kind']=='alignment'), grade.alignment_score)
        self.assertAlmostEqual(sum(e['contribution'] for e in grade.triggered_rules if e['kind']=='fit'), grade.fit_score, places=2)
        self.assertEqual(grade.pre_ai_score, grade.fit_score)
        self.assertTrue(grade.grading_version)
        self.assertTrue(grade.taxonomy_version)
        self.assertTrue(any(e['kind']=='decision' for e in grade.triggered_rules))
        json.dumps(grade.to_dict(), allow_nan=False)

    def test_empty_and_nan_descriptions(self):
        grade = grade_job({'description':float('nan'), 'title':None}, self.context)
        self.assertEqual(grade.matched_atomic_skills, [])
        self.assertEqual(grade.fit_score, 0)
        self.assertTrue(grade.ai_review_required)

    def test_csv_export_keeps_legacy_columns_and_structured_grade(self):
        from skillfreq.pipeline import build_job_result, finish_grading
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'grades.csv'
            result = build_job_result(dict(self.jobs['obvious_target'], id='fixture', site='test'), self.context)
            finish_grading(path, [result], self.context)
            with path.open(newline='', encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream))
            grade = json.loads(rows[0]['grade_json'])
            self.assertEqual(rows[0]['role_lane'], grade['role_lane'])
            self.assertEqual(rows[0]['source_site'], 'test')
            self.assertIn('raw_match', rows[0])
            self.assertTrue(path.with_suffix('.grading.yml').exists())

    def test_resume_consumers_resolve_references(self):
        from skillfreq.resume_router import load_roles_config, suggest_resume_variant
        from skillfreq.skills.resume_profile.extract import load_resume_signal
        config = load_roles_config(CONFIG_DIR/'roles.yml')
        result = suggest_resume_variant('Data Engineer','SQL ETL pipelines',config)
        self.assertTrue(result.best_resume)
        signals = load_resume_signal(CONFIG_DIR/'resume_signal.yml')
        self.assertTrue(all(isinstance(term,str) for meta in signals.values() for term in meta['aliases']))

    def test_import_and_scrape_paths_use_the_same_grader(self):
        from skillfreq.pipeline import run_links
        import pandas as pd
        job = dict(self.jobs['obvious_target'], id='same-job', job_url='https://example.test/job')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            links = root/'links.txt'
            links.write_text(job['job_url'])
            with patch('skillfreq.pipeline.pd.read_csv', return_value=pd.DataFrame([job])):
                imported = run_links(links, CONFIG_DIR/'skills.yml', root/'import.csv', no_scrape=True, use_market_data=False)
            with patch('skillfreq.pipeline.extract_text_from_url', return_value=job):
                scraped = run_links(links, CONFIG_DIR/'skills.yml', root/'scrape.csv', no_scrape=False, use_market_data=False)
            self.assertEqual(imported[0]['deterministic_grade'], scraped[0]['deterministic_grade'])

    def test_grading_uses_no_spacy_or_ai_model(self):
        import skillfreq.skills.extract as extraction
        with patch.object(extraction, '_nlp', side_effect=AssertionError('NLP must be optional')):
            self.assertEqual(self.grade('obvious_target').role_lane, 'target_lane')

    def test_unrecognized_engineer_needs_strong_data_identity(self):
        grade = grade_job({'title':'Staff Engineer - JAVA', 'description':'SQL Python API and JSON services.'}, self.context)
        self.assertNotEqual(grade.role_lane, 'target_lane')

    def test_prevalence_must_be_percentages(self):
        with self.assertRaisesRegex(ValueError, 'Prevalence'):
            self.grade('learning_opportunity', prevalence={'AWS':101})

    def test_reads_existing_prevalence_view_without_recalculating(self):
        from skillfreq.io.grading_to_postgres import load_prevalence
        from unittest.mock import MagicMock
        connection, cursor = MagicMock(), MagicMock()
        connection.__enter__.return_value = connection
        connection.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = ('job_skill_scope',)
        cursor.fetchall.side_effect = [[(self.context.taxonomy_version,)], [('AWS',27.3,1000)], [(7,)]]
        with patch('skillfreq.io.grading_to_postgres._connect', return_value=connection):
            prevalence, metadata = load_prevalence(self.context.taxonomy_version)
        self.assertEqual(prevalence, {'AWS':27.3})
        self.assertEqual(metadata['extraction_run_ids'], [7])
        self.assertEqual(metadata['total_jobs'], 1000)
        self.assertTrue(any('FROM public.skill_prevalence' in str(call) for call in cursor.execute.call_args_list))
        self.assertTrue(connection.close.called)


if __name__ == '__main__':
    unittest.main()
