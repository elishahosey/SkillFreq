"""Bounded condition/action evaluation. No expressions, imports, loops or executable YAML."""
import math
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy

_evaluation_history = ContextVar('policy_evaluation_history', default=None)


def condition_fields(node):
    """Read references without interpreting policy a second time."""
    if 'field' in node:
        return {node['field']}
    return set().union(*(condition_fields(c) for c in next(iter(node.values()))))


@contextmanager
def capture_evaluations():
    history = []
    token = _evaluation_history.set(history)
    try:
        yield history
    finally:
        _evaluation_history.reset(token)

LANES = ('target_lane', 'secondary_lane', 'bridge_lane', 'survival_lane', 'wrong_lane')
OPERATORS = {'equals', 'not_equals', 'in', 'not_in', 'gte', 'lte', 'gt', 'lt',
             'contains', 'contains_any', 'contains_all', 'count_gte', 'count_lte',
             'empty', 'not_empty', 'exists', 'not_exists'}
ACTIONS = {'set', 'add_score', 'subtract_score', 'cap_score', 'floor_score', 'append', 'remove'}


def validate_rules(rules, fields, writable, *, lanes=LANES):
    seen = set()
    def condition(node, depth=0):
        if not isinstance(node, dict) or depth > 6:
            raise ValueError('Malformed policy condition or nesting exceeds six levels')
        if set(node) in ({'all'}, {'any'}):
            children = next(iter(node.values()))
            if not isinstance(children, list) or not children:
                raise ValueError('all/any needs a nonempty condition list')
            for child in children:
                condition(child, depth+1)
            return
        if set(node) != {'field', 'op', 'value'}:
            raise ValueError('Condition needs field, op and value')
        if node['field'] not in fields:
            raise ValueError(f"Unknown policy field: {node['field']}")
        if node['op'] not in OPERATORS:
            raise ValueError(f"Unknown operator: {node['op']}")
        value, op = node['value'], node['op']
        if op in {'gte','lte','gt','lt','count_gte','count_lte'}:
            if isinstance(value, bool) or not isinstance(value, (int,float)) or not math.isfinite(value) or value < 0:
                raise ValueError('Invalid threshold')
            if node['field'] == 'fit_score' and value > 100:
                raise ValueError('Invalid fit score threshold')
        if op in {'in','not_in','contains_any','contains_all'} and not isinstance(value, list):
            raise ValueError(f'{op} needs a list')
        if op in {'empty','not_empty','exists','not_exists'} and value is not True:
            raise ValueError(f'{op} requires value: true')
        if node['field'] == 'role_lane':
            values = value if isinstance(value,list) else [value]
            if any(v not in lanes for v in values):
                raise ValueError('Invalid lane')
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) - {'id','priority','active','when','actions','stop'}:
            raise ValueError('Malformed policy rule')
        if not rule.get('id') or rule['id'] in seen:
            raise ValueError(f"Duplicate rule ID or missing ID: {rule.get('id')}")
        seen.add(rule['id'])
        if not isinstance(rule.get('priority'), int) or not isinstance(rule.get('active', True), bool) or not isinstance(rule.get('stop',False), bool):
            raise ValueError('Invalid priority/active/stop')
        condition(rule['when'])
        if not isinstance(rule.get('actions'), list) or not rule['actions']:
            raise ValueError('Rule needs actions')
        written = set()
        for action in rule['actions']:
            if not isinstance(action, dict) or set(action) != {'op','field','value'}:
                raise ValueError('Malformed or conflicting action definition')
            op, field, value = action['op'], action['field'], action['value']
            if op not in ACTIONS:
                raise ValueError(f'Unknown action: {op}')
            if field not in writable:
                raise ValueError(f'Invalid action field: {field}')
            if field in written:
                raise ValueError(f'Conflicting action definition for {field}')
            written.add(field)
            kind = writable[field]
            if op in {'append','remove'} and kind != 'list':
                raise ValueError('append/remove requires a list field')
            if op not in {'set','append','remove'} and kind != 'score':
                raise ValueError('Score action requires a score field')
            if kind == 'score' and (isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 0 <= value <= 100):
                raise ValueError('Invalid score range')
            if kind == 'bool' and not isinstance(value,bool):
                raise ValueError('Flag needs a boolean')
            if field == 'eligible':
                values = value if isinstance(value,list) else [value]
                if any(v not in lanes for v in values):
                    raise ValueError('Invalid lane')
            if isinstance(kind, tuple) and value not in kind:
                raise ValueError(f'Invalid outcome for {field}')
            if kind == 'list' and op == 'set' and not isinstance(value,list):
                raise ValueError('List assignment requires a list')


def matches(facts, node):
    if 'all' in node:
        return all(matches(facts, child) for child in node['all'])
    if 'any' in node:
        return any(matches(facts, child) for child in node['any'])
    actual, value, op = facts.get(node['field']), node['value'], node['op']
    if op == 'exists': return actual is not None
    if op == 'not_exists': return actual is None
    if op == 'empty': return not actual
    if op == 'not_empty': return bool(actual)
    if op == 'equals': return actual == value
    if op == 'not_equals': return actual != value
    if actual is None: return False
    if op == 'in': return actual in value
    if op == 'not_in': return actual not in value
    if op == 'contains': return value in actual
    if op == 'contains_any': return bool(set(actual).intersection(value))
    if op == 'contains_all': return set(value).issubset(actual)
    if op == 'count_gte': return len(actual) >= value
    if op == 'count_lte': return len(actual) <= value
    if op == 'gte': return actual >= value
    if op == 'lte': return actual <= value
    if op == 'gt': return actual > value
    if op == 'lt': return actual < value
    raise ValueError(f'Unknown operator: {op}')


def evaluate_rules(facts, rules, kind, *, stage=None):
    """Higher priorities run first; stop ends this stage. Mutations are audited."""
    evidence = []
    history = _evaluation_history.get()
    stopped_by = None
    for rule in sorted(rules, key=lambda r: -r['priority']):
        active = rule.get('active', True)
        if stopped_by:
            if history is not None:
                history.append(dict(rule_id=rule['id'], stage=stage or kind,
                                    status='not_evaluated', stopped_by=stopped_by))
            continue
        matched = active and matches(facts, rule['when'])
        inputs = {field: deepcopy(facts.get(field)) for field in sorted(condition_fields(rule['when']))} if matched or history is not None else None
        if history is not None:
            history.append(dict(rule_id=rule['id'], stage=stage or kind,
                                status='fired' if matched else ('not_matched' if active else 'inactive'),
                                condition=rule['when'], inputs=inputs))
        if not matched:
            continue
        for action in rule['actions']:
            op, field, value = action['op'], action['field'], action['value']
            before = facts.get(field)
            after = before
            if op == 'set': after = value.copy() if isinstance(value,list) else value
            elif op == 'add_score': after = before + value
            elif op == 'subtract_score': after = before - value
            elif op == 'cap_score': after = min(before, value)
            elif op == 'floor_score': after = max(before, value)
            elif op == 'append': after = list(dict.fromkeys((before or []) + [value]))
            elif op == 'remove': after = [item for item in before if item != value]
            else: raise ValueError(f'Unknown action: {op}')
            facts[field] = after
            item = dict(rule_id=rule['id'], kind=kind, condition=rule['when'], action=action,
                        before=before, result=after, stage=stage or kind, inputs=inputs,
                        changed=before != after)
            if kind == 'fit': item['contribution'] = round(after-before, 3) if field == 'fit_score' else 0
            evidence.append(item)
        if rule.get('stop', False):
            if history is None:
                break
            stopped_by = rule['id']
    return evidence
