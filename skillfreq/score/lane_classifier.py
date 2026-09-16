from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from skillfreq.configuration import default_roles
from skillfreq.skills.text import normalize_text, term_counts

from .policy import LANES, evaluate_rules


@dataclass
class LaneResult:
    role_lane: str
    lane_scores: dict[str, float]
    raw_lane_scores: dict[str, float]
    triggered_rules: list[dict]
    category_hits: dict[str, int]
    contradictions: list[str]
    hard_exclusions: list[str]
    policy_flags: dict[str, bool] = field(default_factory=dict)
    resolution: dict = field(default_factory=dict)


def extract_role_signals(row: dict[str, Any], config: dict) -> list[dict]:
    fields = {key: normalize_text(row.get(key)) for key in ('title', 'description')}
    fields['both'] = fields['title'] + ' ' + fields['description']
    evidence = []
    for rule in config['lane_rules']:
        if not rule['active']:
            continue
        text = fields[rule['scope']]
        if rule.get('title_pattern'):
            pattern = rule['title_pattern']
            left = list(term_counts(text, pattern['any']))
            right = list(term_counts(text, pattern['with']))
            hits = list(dict.fromkeys(left + right)) if left and right else []
        elif rule.get('pattern'):
            hits = list(dict.fromkeys(m.group(0) for m in re.finditer(rule['pattern'], text)))
        else:
            hits = list(term_counts(text, config['resolved_groups'][rule['group']]))
        if hits:
            count = min(len(hits), rule['max_hits'])
            evidence.append(dict(rule_id=rule['id'], kind='signal', category=rule['category'],
                                 scope=rule['scope'], signal_type=rule['signal_type'],
                                 matched_terms=hits, lane=rule['lane'],
                                 weight=rule['weight'], contribution=count*rule['weight'],
                                 term_group=rule.get('group'),
                                 hard_exclusion=rule['hard_exclusion']))
    return evidence


def score_lanes(row: dict[str, Any], config: dict | None = None) -> LaneResult:
    """Accumulate evidence, then apply explicit eligibility protections and choose.

    Scores are heuristic points, not percentages. All suppression and overrides
    are retained; a search origin alone cannot establish a role identity.
    """
    config = config if config is not None else default_roles()
    policy = config['lane_policy']
    evidence = extract_role_signals(row, config)
    scores = dict.fromkeys(LANES, 0.0)
    hits = {rule['category']: 0 for rule in config['lane_rules']}
    for match in evidence:
        scores[match['lane']] += match['contribution']
        hits[match['category']] += len(match['matched_terms'])
    raw = scores.copy()
    hard = [e['rule_id'] for e in evidence if e['hard_exclusion']]
    facts = dict(always=True, eligible=[policy['fallback_lane']], contradictions=[],
                 hard_exclusions=hard, search_lane=normalize_text(row.get('search_lane')))
    facts.update({'hits.'+name: count for name,count in hits.items()})
    facts.update({'points.'+lane: value for lane,value in scores.items()})
    # Flags are derived by authored evidence rules, not career-specific branches.
    for rule in config['eligibility_rules']:
        for action in rule['actions']:
            if isinstance(action['value'], bool):
                facts.setdefault(action['field'], False)
    evidence.extend(evaluate_rules(facts, config['eligibility_rules'], 'override'))
    scores = {lane: facts['points.'+lane] for lane in LANES}
    eligible = facts['eligible'] or [policy['fallback_lane']]
    for lane in LANES:
        if lane not in eligible:
            evidence.append(dict(rule_id='lane_eligibility:'+lane, kind='penalty', lane=lane,
                                 contribution=-scores[lane], reason='configured_eligibility_rules'))
            scores[lane] = 0
    if max(scores[lane] for lane in eligible) <= 0:
        lane = policy['fallback_lane'] if policy['fallback_lane'] in eligible else eligible[0]
        scores[lane] = policy['fallback_score']
        evidence.append(dict(rule_id='no_supported_lane', kind='override', lane=lane,
                             contribution=policy['fallback_score']))
    winner = max((lane for lane in LANES if lane in eligible), key=lambda lane:scores[lane])
    return LaneResult(winner, scores, raw, evidence, hits, facts['contradictions'], hard,
                      {name: facts.get(name, False) for name in config.get('derived_flags', [])},
                      dict(eligible=eligible, winner=winner, tie_order=list(LANES),
                           tied_winners=[lane for lane in eligible if scores[lane] == scores[winner]],
                           fallback_lane=policy['fallback_lane'],
                           fallback_used=any(e['rule_id']=='no_supported_lane' for e in evidence)))


def classify_role_lane(row: dict[str, Any]) -> str:
    """Compatibility API used by CSV consumers and the existing decision layer."""
    return score_lanes(row).role_lane
