"""Decision and fit-quality policy share one owner: weights.yml.

Legacy alignment remains an explanatory metric; it cannot override fit decisions.
"""
from skillfreq.configuration import scoring_config
from .policy import evaluate_rules


def derive_fit_quality(row, evidence=None):
    facts = dict(row, always=True)
    records = evaluate_rules(facts, scoring_config()['quality_rules'], 'decision', stage='quality')
    if evidence is not None:
        evidence.extend(records)
    return facts['fit_quality']


def decide_apply_bucket(row, evidence=None):
    facts = dict(row, always=True)
    records = evaluate_rules(facts, scoring_config()['decision_rules'], 'decision', stage='apply')
    if evidence is not None:
        evidence.extend(records)
    return facts['apply_decision']
