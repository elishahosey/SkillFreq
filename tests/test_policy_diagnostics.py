import copy
import unittest

import yaml

from skillfreq.policy_diagnostics import dependency_graph, inspect_policy, normalize_field
from skillfreq.score.grading import GradingContext, grade_job
from skillfreq.score.policy import evaluate_rules


class PolicyDiagnosticsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = GradingContext.load()
        cls.job = yaml.safe_load((__import__('pathlib').Path(__file__).parent / 'fixtures/ecosystem_jobs.yml').read_text())[4]

    def test_dependency_graph_reports_flag_producers_and_consumers(self):
        graph = dependency_graph(self.context)
        info = graph['derived_flags']['ecosystem_role_concentration']
        self.assertIn('ecosystem_concentration_evidence', info['produced_by'])
        self.assertIn('ecosystem_identity_guard', info['consumed_by'])
        self.assertIn('role_lane', info['downstream'])
        self.assertEqual(normalize_field('flags.ecosystem_ownership_gate'), 'ecosystem_ownership_gate')
        self.assertIn('ecosystem_dependence', dependency_graph(self.context)['derived_flags']['ecosystem_ownership_gate']['consumed_by'])

    def test_static_report_marks_conservative_findings(self):
        report = inspect_policy(self.context)
        self.assertEqual(report['validation'], 'passed')
        self.assertTrue(any(i['kind'] == 'input_contract_unavailable' for i in report['issues']))
        self.assertFalse(any(i.get('kind') == 'duplicate_equivalent_rule' and i.get('rule') == 'secondary_core_overlap' for i in report['issues']))

    def test_noop_and_overridden_actions_are_observable(self):
        facts = {'always': True, 'items': ['x'], 'value': 4}
        rules = [
            {'id': 'first', 'priority': 20, 'when': {'field': 'always', 'op': 'equals', 'value': True},
             'actions': [{'op': 'append', 'field': 'items', 'value': 'x'}]},
            {'id': 'second', 'priority': 10, 'when': {'field': 'always', 'op': 'equals', 'value': True},
             'actions': [{'op': 'set', 'field': 'items', 'value': []}]},
        ]
        events = evaluate_rules(facts, rules, 'override')
        self.assertEqual(events[0]['changed'], False)
        self.assertEqual(events[1]['changed'], True)

    def test_grade_contains_owner_and_effect_metadata(self):
        grade = grade_job(self.job, self.context)
        self.assertIn('owners', grade.observability)
        self.assertIsNotNone(grade.observability['owners']['final_apply_decision_rule'])
        self.assertTrue(grade.observability['action_effects'])

    def test_trace_captures_unmatched_and_stopped_rules(self):
        grade = grade_job(self.job, self.context, trace=True)
        statuses = {event['status'] for event in grade.observability['evaluations']}
        self.assertIn('not_matched', statuses)
        self.assertIn('not_evaluated', statuses)
