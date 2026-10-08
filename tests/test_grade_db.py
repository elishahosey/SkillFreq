import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from skillfreq.io.grading_to_postgres import load_jobs_for_grading
from skillfreq.pipeline import build_job_result, grade_database
from skillfreq.score.grading import GradingContext


class GradeDatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.job = dict(source_job_id='00042', source_site='indeed',
                       job_url='https://example.com/job/42', title='Data Engineer',
                       description='Build ETL data pipelines with PostgreSQL and Python. Maintain data quality.')

    def connection(self):
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = [self.job]
        return connection, cursor

    def test_read_only_source_query_preserves_identity_and_bounds(self):
        connection, cursor = self.connection()
        with patch('skillfreq.io.grading_to_postgres._connect', return_value=connection) as connect:
            jobs = load_jobs_for_grading(90, 3, connect_timeout=4, statement_timeout=20, lock_timeout=2)
        connect.assert_called_once_with(4, 20, 2)
        connection.set_session.assert_called_once_with(readonly=True)
        query, parameters = cursor.execute.call_args.args
        self.assertIn('FROM public.clean_jobs', query)
        self.assertIn('date_posted >= CURRENT_DATE - %s', query)
        self.assertIn('ORDER BY date_posted DESC', query)
        self.assertTrue(query.endswith('LIMIT %s'))
        self.assertEqual(parameters, [90, 3])
        self.assertEqual(jobs, [self.job])
        connection.close.assert_called_once()

    def test_default_query_has_no_job_limit(self):
        connection, cursor = self.connection()
        with patch('skillfreq.io.grading_to_postgres._connect', return_value=connection):
            load_jobs_for_grading()
        query, parameters = cursor.execute.call_args.args
        self.assertNotIn('LIMIT', query)
        self.assertEqual(parameters, [90])

    def test_query_failure_closes_connection(self):
        connection, cursor = self.connection()
        cursor.execute.side_effect = RuntimeError('missing view')
        with patch('skillfreq.io.grading_to_postgres._connect', return_value=connection):
            with self.assertRaisesRegex(RuntimeError, 'missing view'):
                load_jobs_for_grading()
        connection.close.assert_called_once()

    def test_invalid_bounds_do_not_connect(self):
        with patch('skillfreq.io.grading_to_postgres._connect') as connect:
            for days, limit in [(0, None), (-1, None), (90, 0), (90, -1)]:
                with self.subTest(days=days, limit=limit), self.assertRaises(ValueError):
                    load_jobs_for_grading(days, limit)
        connect.assert_not_called()

    def test_db_flow_uses_existing_grader_and_new_export(self):
        market = {'source': 'public.skill_prevalence'}
        prevalence = {'Python': 45.0, 'PostgreSQL': 30.0}
        expected = build_job_result(self.job, self.context, prevalence, market)
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'results-db-90-days.csv'
            original = Path(folder) / 'results.csv'
            original.write_text('keep existing results', encoding='utf-8')
            with patch('skillfreq.pipeline.load_jobs_for_grading', return_value=[self.job]), \
                 patch('skillfreq.pipeline.load_prevalence', return_value=(prevalence, market)), \
                 patch('skillfreq.pipeline.pd.read_csv') as read_csv, \
                 patch('skillfreq.pipeline.extract_text_from_url') as scrape, \
                 patch('skillfreq.pipeline.save_grades') as save:
                results = grade_database(output, context=self.context)
            self.assertEqual(results, [expected])
            self.assertEqual(results[0].id, '00042')
            self.assertEqual(results[0].search_lane, '')
            read_csv.assert_not_called()
            scrape.assert_not_called()
            save.assert_not_called()
            with output.open(encoding='utf-8', newline='') as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(json.loads(rows[0]['grade_json']), json.loads(json.dumps(expected.deterministic_grade)))
            self.assertTrue(output.with_suffix('.grading.yml').exists())
            self.assertEqual(original.read_text(encoding='utf-8'), 'keep existing results')

    def test_empty_scope_writes_headers_without_market_or_history_queries(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'empty.csv'
            with patch('skillfreq.pipeline.load_jobs_for_grading', return_value=[]), \
                 patch('skillfreq.pipeline.load_prevalence') as market, \
                 patch('skillfreq.pipeline.save_grades') as save:
                self.assertEqual(grade_database(output, context=self.context, persist_grades=True), [])
            market.assert_not_called()
            save.assert_not_called()
            with output.open(encoding='utf-8', newline='') as handle:
                reader = csv.DictReader(handle)
                self.assertIn('fit_score', reader.fieldnames)
                self.assertEqual(list(reader), [])

    def test_cli_forwards_database_options(self):
        from skillfreq.cli import main
        argv = ['skillfreq', '--db-statement-timeout', '25', 'grade-db', '--since-days', '30',
                '--limit', '5', '--out', 'db-test.csv', '--offline-grading', '--persist-grades']
        with patch('sys.argv', argv), patch('skillfreq.cli.CommandDiagnostics'), \
             patch('skillfreq.cli.grade_database', return_value=[]) as grade, patch('builtins.print'):
            main()
        args, options = grade.call_args
        self.assertEqual(args, (Path('db-test.csv'),))
        self.assertEqual(options['since_days'], 30)
        self.assertEqual(options['limit'], 5)
        self.assertEqual(options['statement_timeout'], 25)
        self.assertFalse(options['use_market_data'])
        self.assertTrue(options['persist_grades'])

    def test_grade_defaults_to_database_and_current_market(self):
        from skillfreq.cli import main
        with patch('sys.argv', ['skillfreq', 'grade']), patch('skillfreq.cli.CommandDiagnostics'), \
             patch('skillfreq.cli.grade_database', return_value=[]) as grade, \
             patch('skillfreq.cli.grade_csv') as csv_grade, patch('builtins.print'):
            main()
        args, options = grade.call_args
        self.assertTrue(options['use_market_data'])
        self.assertEqual(options['since_days'], 90)
        self.assertFalse(options['persist_grades'])
        self.assertEqual(args[0].parent, Path('data/outputs'))
        self.assertRegex(args[0].name, r'^results-db-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}-\d{6}\.csv$')
        csv_grade.assert_not_called()

    def test_grade_optional_csv_uses_current_market_and_output_override(self):
        from skillfreq.cli import main
        with patch('sys.argv', ['skillfreq', 'grade', '--input', 'jobs.csv', '--out', 'selected.csv']), \
             patch('skillfreq.cli.CommandDiagnostics'), patch('skillfreq.cli.grade_database') as database, \
             patch('skillfreq.cli.grade_csv', return_value=[]) as grade, patch('builtins.print'):
            main()
        args, options = grade.call_args
        self.assertEqual(args, (Path('jobs.csv'), Path('selected.csv')))
        self.assertTrue(options['use_market_data'])
        database.assert_not_called()

    def test_csv_output_is_optional_and_database_filters_are_rejected(self):
        from skillfreq.cli import main
        for command in ('grade', 'grade-csv'):
            with self.subTest(command=command), \
                 patch('sys.argv', ['skillfreq', command, '--input', 'jobs.csv']), \
                 patch('skillfreq.cli.CommandDiagnostics'), \
                 patch('skillfreq.cli.grade_csv', return_value=[]) as grade, patch('builtins.print'):
                main()
                self.assertTrue(grade.call_args.args[1].name.startswith('results-csv-'))
        with patch('sys.argv', ['skillfreq', 'grade', '--input', 'jobs.csv', '--limit', '5']), \
             patch('sys.stderr'), self.assertRaises(SystemExit):
            main()
