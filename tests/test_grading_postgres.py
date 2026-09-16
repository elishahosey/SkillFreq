"""Optional integration test; all schema/row changes roll back.

Run with SKILLFREQ_TEST_DB=1 against the existing SkillFreq development database.
"""
import os
import unittest
from unittest.mock import patch

from skillfreq.io.grading_to_postgres import persist_grades, load_prevalence
from skillfreq.io.job_skills_to_postgres import _connect


@unittest.skipUnless(os.getenv('SKILLFREQ_TEST_DB') == '1', 'set SKILLFREQ_TEST_DB=1 for rollback-only PostgreSQL integration')
class PostgresGradingTest(unittest.TestCase):
    def test_prevalence_counts_snapshot_scope_including_zero_mentions(self):
        from pathlib import Path
        connection = _connect(5, 30, 5)
        try:
            with connection.cursor() as cursor:
                cursor.execute('CREATE TEMP TABLE market_skill_taxonomy (canonical_skill text PRIMARY KEY)')
                cursor.execute('CREATE TEMP TABLE job_skill_scope (job_key text PRIMARY KEY, extraction_run_id bigint)')
                cursor.execute('CREATE TEMP TABLE job_skills (job_key text, canonical_skill text, extraction_run_id bigint, PRIMARY KEY(job_key,canonical_skill))')
                cursor.execute("INSERT INTO pg_temp.market_skill_taxonomy VALUES ('SQL'),('Airflow'),('Python')")
                cursor.execute("INSERT INTO pg_temp.job_skill_scope VALUES ('a',2),('b',2),('c',2),('d',2)")
                cursor.execute("INSERT INTO pg_temp.job_skills VALUES ('a','SQL',2),('b','SQL',2),('a','Airflow',2),('outside','SQL',2),('c','Python',1)")
                sql = Path('db/job_skills.sql').read_text()
                cursor.execute(sql[sql.index('CREATE OR REPLACE VIEW public.skill_prevalence'):].replace('public.','pg_temp.'))
                cursor.execute('SELECT canonical_skill,jobs_mentioning_skill,total_jobs,prevalence_pct FROM pg_temp.skill_prevalence')
                rows = {r[0]:r[1:] for r in cursor.fetchall()}
                self.assertEqual(rows['SQL'],(2,4,50))
                self.assertEqual(rows['Airflow'],(1,4,25))
                self.assertEqual(rows['Python'],(0,4,0))
                cursor.execute('DELETE FROM pg_temp.job_skill_scope')
                cursor.execute('SELECT prevalence_pct FROM pg_temp.skill_prevalence')
                self.assertTrue(all(row[0] is None for row in cursor.fetchall()))
        finally:
            connection.rollback()
            connection.close()

    def test_migration_append_and_audit_round_trip_rollback(self):
        from skillfreq.score.grading import GradingContext
        from skillfreq.pipeline import build_job_result
        context = GradingContext.load()
        result = build_job_result(dict(id='grading-integration-fixture', site='test',
            title='Data Engineer', description='SQL ETL data pipelines and Python data quality.'), context)
        connection = _connect(5, 30, 5)

        class RollbackOnly:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def cursor(self, **kwargs):
                return connection.cursor(**kwargs)
            def close(self):
                pass

        try:
            with patch('skillfreq.io.grading_to_postgres._connect', return_value=RollbackOnly()):
                self.assertEqual(persist_grades([result], context), 1)
                # Idempotent migration, append-only results on repeated evaluation.
                self.assertEqual(persist_grades([result], context), 1)
            with connection.cursor() as cursor:
                cursor.execute('SELECT grading_version,taxonomy_version,deterministic_grade FROM public.job_grade_history WHERE job_id=%s',
                               (result.id,))
                rows = cursor.fetchall()
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0][0], context.grading_version)
                self.assertEqual(rows[0][1], context.taxonomy_version)
                self.assertEqual(rows[0][2]['role_lane'], result.role_lane)
                self.assertNotIn('description', rows[0][2])
                cursor.execute('SELECT configuration FROM public.grading_config_versions WHERE grading_version=%s', (context.grading_version,))
                self.assertEqual(cursor.fetchone()[0], context.snapshot)
                # The existing batch CSV importer writes the same audit fields.
                import json
                import pandas as pd
                from skillfreq.io.excel_to_postgres import insert_skill_scores
                frame = pd.DataFrame([dict(id='batch-fixture', title=result.title, source='https://example.test/batch',
                    source_site='test', grade_json=json.dumps(result.deterministic_grade),
                    matches=result.matches_json, score=result.score, fit_quality=result.fit_quality)])
                self.assertEqual(insert_skill_scores(cursor, frame, {}, pd.DataFrame(), 'grading-test', 'legacy'), 1)
                cursor.execute('SELECT grading_version FROM public.job_grade_history WHERE job_id=%s', ('batch-fixture',))
                self.assertEqual(cursor.fetchone()[0], context.grading_version)
        finally:
            connection.rollback()
            connection.close()
