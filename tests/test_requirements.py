import unittest
import copy
import tempfile
from pathlib import Path
import yaml

from skillfreq.score.grading import GradingContext, grade_job
from skillfreq.skills.extract import extract_requirement_flags
from skillfreq.score.trace import render_trace
from skillfreq.configuration import validate_grading_settings


class RequirementGroupsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.jobs = {j['name']: j for j in yaml.safe_load((Path(__file__).parent/'fixtures/requirements_jobs.yml').read_text())}

    def group(self, name):
        config = dict(self.context.requirements, _taxonomy=self.context.taxonomy)
        flags = extract_requirement_flags(self.jobs[name]['description'], self.context.skills,
                                          self.context.profile, config)
        return flags['requirement_groups'][0]

    def test_all_of_requires_each_skill(self):
        self.assertEqual(self.group('all_of')['type'], 'all_of')
        self.assertEqual(set(self.group('all_of')['skills']), {'AWS', 'Spark'})

    def test_or_and_examples_are_any_of(self):
        self.assertEqual(self.group('cloud_alternatives')['type'], 'any_of')
        self.assertEqual(self.group('cloud_examples')['type'], 'any_of')
        self.assertEqual(self.group('platform_alternative')['type'], 'any_of')
        self.assertEqual(self.group('one_database')['type'], 'any_of')

    def test_equivalent_is_distinct(self):
        self.assertEqual(self.group('equivalent')['type'], 'equivalent')

    def test_preferred_is_section_aware(self):
        grade = grade_job(self.jobs['preferred'], self.context)
        self.assertIn('Power BI', grade.missing_preferred_skills['atomic_skills'])
        self.assertNotIn('Power BI', grade.missing_required_skills['atomic_skills'])

    def test_any_of_does_not_create_one_gap_per_option(self):
        grade = grade_job(self.jobs['cloud_alternatives'], self.context)
        self.assertNotIn('AWS', grade.missing_required_skills['atomic_skills'])
        self.assertNotIn('Azure', grade.missing_required_skills['atomic_skills'])
        self.assertNotIn('Google Cloud', grade.missing_required_skills['atomic_skills'])
        self.assertEqual(grade.missing_required_skills['requirement_groups'][0]['type'], 'any_of')

    def test_early_career_signal_is_scoped_to_requirements(self):
        job = {'title': 'Lead Data Engineer',
               'description': 'Responsibilities: mentor junior engineers and set technical direction.\nRequired qualifications: 7+ years of experience.'}
        grade = grade_job(job, self.context)
        early = [e for e in grade.triggered_rules if e.get('rule_id') == 'alignment:early_career']
        self.assertFalse(early)

    def semantic_grade(self, sentence, context=None):
        return grade_job({'title': 'Data Engineer', 'description': 'SQL ETL data pipelines.\nRequired qualifications:\n'+sentence},
                         context or self.context, prevalence={})

    def test_required_alternative_has_one_configurable_penalty(self):
        context = copy.deepcopy(self.context)
        context.settings['fit']['required_group_penalty'] = 7
        grade = self.semantic_grade('Databricks or Snowflake required.', context)
        gaps = grade.missing_required_skills
        self.assertEqual(gaps['atomic_skills'], [])
        self.assertEqual(len(gaps['unsatisfied_groups']), 1)
        events = [e for e in grade.triggered_rules if e['rule_id'] == 'fit_unsatisfied_required_group']
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['contribution'], -7)
        self.assertFalse(grade.requirement_flags['has_hard_requirement_blockers'])
        self.assertFalse(grade.requirement_flags['has_modern_stack_blockers'])
        self.assertEqual(grade.requirement_flags['modern_required_missing_skills'], [])
        context.settings['fit']['required_group_penalty'] = 0
        control = self.semantic_grade('Databricks or Snowflake required.', context)
        self.assertEqual(control.fit_score - grade.fit_score, 7)
        self.assertEqual(control.role_lane, grade.role_lane)

    def test_all_of_is_atomic_only_and_legacy_consistent(self):
        grade = self.semantic_grade('AWS and Spark required.')
        self.assertEqual(set(grade.missing_required_skills['atomic_skills']), {'AWS', 'Spark'})
        self.assertEqual(grade.missing_required_skills['unsatisfied_groups'], [])
        self.assertEqual(set(grade.requirement_flags['modern_required_missing_skills']), {'aws', 'spark'})
        self.assertEqual(len([e for e in grade.triggered_rules if e['rule_id'] == 'fit_missing_required_atomic']), 2)
        self.assertFalse(any(e['rule_id'] == 'fit_unsatisfied_required_group' for e in grade.triggered_rules))

    def test_satisfied_cloud_alternative_has_no_legacy_penalty(self):
        grade = self.semantic_grade('AWS, Azure, or GCP required.')
        self.assertEqual(grade.missing_required_skills['unsatisfied_groups'], [])
        self.assertEqual(grade.missing_required_skills['atomic_skills'], [])
        self.assertEqual(grade.requirement_flags['modern_required_missing_skills'], [])
        self.assertFalse(any(e['rule_id'] == 'alignment:modern_required' for e in grade.triggered_rules))
        group = grade.missing_required_skills['requirement_groups'][0]
        self.assertEqual(group['candidate_satisfied_skills'], ['Azure'])
        self.assertTrue(group['satisfied'])

    def test_equivalent_requires_explicit_acceptable_evidence(self):
        context = copy.deepcopy(self.context)
        sentence = 'Airflow or equivalent orchestration tool.'
        unknown = self.semantic_grade(sentence, context)
        self.assertEqual(len(unknown.missing_required_skills['unsatisfied_groups']), 1)
        self.assertNotIn('Airflow', unknown.missing_required_skills['atomic_skills'])
        # Test an explicitly authored capability equivalence; production config
        # deliberately does NOT assume ETL implies orchestration experience.
        context.requirements['equivalences'] = {'Airflow': {'capability_concepts': ['etl']}}
        known = self.semantic_grade(sentence, context)
        self.assertEqual(known.missing_required_skills['unsatisfied_groups'], [])
        self.assertTrue(known.missing_required_skills['requirement_groups'][0]['equivalent_evidence'])
        self.assertEqual(known.requirement_flags['modern_required_missing_skills'], [])

    def test_inline_preferred_overrides_required_section(self):
        for description in ('Power BI preferred.', 'Required qualifications:\nPower BI preferred.'):
            grade = grade_job({'description': description}, self.context)
            self.assertEqual(grade.missing_required_skills['atomic_skills'], [])
            self.assertEqual(grade.missing_preferred_skills['atomic_skills'], ['Power BI'])

    def test_known_databases_are_not_missing_and_generic_sql_is_not_an_option(self):
        grade = self.semantic_grade('SQL Server and PostgreSQL required.')
        group = grade.missing_required_skills['requirement_groups'][0]
        self.assertEqual(set(group['skills']), {'SQL Server', 'PostgreSQL'})
        self.assertTrue(group['satisfied'])
        context = copy.deepcopy(self.context)
        context.profile_config['atomic_skills'] = {'SQL': 1}
        grade = self.semantic_grade('One or more of SQL Server, PostgreSQL, MySQL.', context)
        self.assertEqual(len(grade.missing_required_skills['unsatisfied_groups']), 1)
        grade = self.semantic_grade('One or more of SQL Server, PostgreSQL, MySQL.')
        self.assertEqual(grade.missing_required_skills['unsatisfied_groups'], [])

    def test_mixed_grammar_is_ambiguous_and_requests_review(self):
        grade = self.semantic_grade('SQL required and experience with AWS or Azure.')
        group = grade.missing_required_skills['requirement_groups'][0]
        self.assertEqual(group['type'], 'ambiguous')
        self.assertIsNone(group['satisfied'])
        self.assertEqual(grade.missing_required_skills['atomic_skills'], [])
        self.assertEqual(grade.missing_required_skills['unsatisfied_groups'], [])
        self.assertEqual(grade.requirement_flags['modern_required_missing_skills'], [])
        self.assertTrue(grade.confidence_evidence['requirement_ambiguity'])
        self.assertTrue(grade.ai_review_required)
        self.assertIn('ambiguous_requirements', grade.ai_review_reasons)

    def test_and_or_is_not_mixed_and_verbs_before_list_do_not_confuse_it(self):
        for sentence in ('AWS and/or Azure required.', 'Design and develop with AWS or Azure.'):
            grade = self.semantic_grade(sentence)
            self.assertEqual(grade.missing_required_skills['requirement_groups'][0]['type'], 'any_of')

    def test_examples_are_distinct_from_colon_enumeration(self):
        grade = self.semantic_grade('Experience with databases such as PostgreSQL, MySQL, or SQL Server.')
        self.assertEqual(grade.missing_required_skills['requirement_groups'][0]['grammar'], 'examples')
        self.assertEqual(grade.missing_required_skills['atomic_skills'], [])
        grade = self.semantic_grade('Proficiency in AWS services: Glue, Redshift, Athena.')
        self.assertEqual(grade.missing_required_skills['requirement_groups'][0]['type'], 'all_of')
        self.assertIn('Redshift', grade.missing_required_skills['atomic_skills'])

    def test_fallback_is_per_sentence_not_entire_section(self):
        context = copy.deepcopy(self.context)
        context.profile['etl'] = 0
        grade = self.semantic_grade('AWS, Azure, or GCP required.\nETL required.', context)
        self.assertIn('etl', grade.requirement_flags['mandatory_missing_skills'])
        self.assertEqual(grade.requirement_flags['modern_required_missing_skills'], [])
        self.assertTrue(any(e['mode'] == 'legacy_mention_fallback' for e in grade.requirement_flags['requirement_interpretation']))

    def test_separate_mandatory_mention_survives_satisfied_alternative(self):
        grade = self.semantic_grade('AWS or Azure required.\nAWS required.')
        self.assertEqual(grade.missing_required_skills['atomic_skills'], ['AWS'])
        self.assertEqual(grade.requirement_flags['modern_required_missing_skills'], ['aws'])

    def test_known_atomic_requirement_cannot_become_legacy_core_blocker(self):
        context = copy.deepcopy(self.context)
        context.profile['sql'] = 0
        grade = self.semantic_grade('SQL Server and PostgreSQL required.', context)
        self.assertEqual(grade.missing_required_skills['atomic_skills'], [])
        self.assertEqual(grade.requirement_flags['mandatory_missing_skills'], [])
        self.assertFalse(grade.requirement_flags['has_hard_requirement_blockers'])
        context.profile_config['atomic_skills'] = {}
        missing = self.semantic_grade('SQL Server and PostgreSQL required.', context)
        self.assertTrue(missing.requirement_flags['has_hard_requirement_blockers'])

    def test_satisfied_preferred_alternative_has_no_legacy_charge(self):
        grade = grade_job({'description': 'Preferred qualifications:\nAWS or Azure.'}, self.context)
        self.assertEqual(grade.missing_preferred_skills['unsatisfied_groups'], [])
        self.assertEqual(grade.requirement_flags['modern_preferred_missing_skills'], [])

    def test_preferred_alternative_never_gets_required_group_penalty(self):
        grade = grade_job({'description': 'Preferred qualifications:\nDatabricks or Snowflake.'}, self.context)
        self.assertEqual(len(grade.missing_preferred_skills['unsatisfied_groups']), 1)
        self.assertFalse(any(e['rule_id'] == 'fit_unsatisfied_required_group' for e in grade.triggered_rules))
        self.assertEqual(grade.requirement_flags['modern_preferred_missing_skills'], [])

    def test_trace_contains_real_group_effect_and_fallback(self):
        grade = self.semantic_grade('Databricks or Snowflake required.\nETL required.')
        trace = render_trace(grade)
        self.assertIn('Unsatisfied requirement groups:', trace)
        self.assertIn('group fit contribution: -3', trace)
        self.assertIn('legacy_mention_fallback', trace)
        self.assertIn('Individual gaps:', trace)

    def test_legacy_api_without_taxonomy_keeps_fallback(self):
        flags = extract_requirement_flags('Required qualifications: AWS and Spark.',
                                           self.context.skills, self.context.profile, self.context.requirements)
        self.assertEqual(flags['requirement_groups'], [])
        self.assertEqual(set(flags['modern_required_missing_skills']), {'aws', 'spark'})

    def test_group_penalty_validation(self):
        for value in (-1, 101, True, float('nan'), 'three'):
            settings = copy.deepcopy(self.context.settings)
            settings['fit']['required_group_penalty'] = value
            with self.assertRaisesRegex(ValueError, 'required_group_penalty'):
                validate_grading_settings(settings, self.context.roles)

    def test_equivalence_references_are_validated(self):
        for mapping in ({'unknown': {}}, {'Airflow': {'capability_concepts': ['unknown']}},
                        {'Airflow': {'atomic_skills': 'Azure'}}, {'Airflow': {'execute': 'anything'}}):
            config = dict(self.context.requirements, equivalences=mapping)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory)/'requirements.yml'
                path.write_text(yaml.safe_dump(config), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'equivalence'):
                    GradingContext.load(requirements_path=path)


if __name__ == '__main__':
    unittest.main()
