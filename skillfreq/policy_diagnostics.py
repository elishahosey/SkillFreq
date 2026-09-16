"""Static policy inspection and report generation.

This module deliberately inspects the existing bounded policy structures. It does
not evaluate jobs or introduce another policy language.
"""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any

from .configuration import read_config, load_roles, validate_grading_settings, CONFIG_DIR
from .score.policy import condition_fields
from .score.grading import GradingContext, grade_job
from .score.trace import render_trace


def normalize_field(field):
    """Canonicalize cross-stage flag aliases for analysis only."""
    return field[6:] if isinstance(field, str) and field.startswith('flags.') else field


def _walk(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def policy_rules(context: GradingContext):
    roles, settings = context.roles, context.settings
    return ([('lane_signal', r) for r in roles['lane_rules']]
            + [('eligibility', r) for r in roles['eligibility_rules']]
            + [('fit', r) for r in settings['fit']['rules']]
            + [('quality', r) for r in settings['quality_rules']]
            + [('decision', r) for r in settings['decision_rules']])


def _rule_fields(rule):
    when = rule.get('when')
    return sorted(condition_fields(when)) if isinstance(when, dict) else []


def dependency_graph(context: GradingContext):
    rules = policy_rules(context)
    producers = defaultdict(list)
    consumers = defaultdict(list)
    for stage, rule in rules:
        for action in rule.get('actions', []):
            producers[normalize_field(action['field'])].append(rule['id'])
        for field in _rule_fields(rule):
            consumers[normalize_field(field)].append(rule['id'])
        if stage == 'lane_signal' and rule.get('group'):
            consumers['term_group:' + rule['group']].append(rule['id'])
    groups = defaultdict(list)
    for stage, rule in rules:
        group = rule.get('group')
        if group:
            groups[group].append(rule['id'])
    downstream = {
        'eligible': ['role_lane'], 'points.target_lane': ['role_lane'],
        'points.secondary_lane': ['role_lane'], 'points.bridge_lane': ['role_lane'],
        'points.survival_lane': ['role_lane'], 'points.wrong_lane': ['role_lane'],
        'fit_score': ['fit', 'fit_quality', 'apply_decision'],
        'blockers': ['apply_decision'], 'review_flags': ['apply_decision'],
        'ai_review_required': ['ai_review'],
    }
    stage_outputs = {'eligibility': 'role_lane', 'fit': 'fit', 'quality': 'fit_quality',
                     'decision': 'apply_decision'}
    flags = {}
    for name in context.roles.get('derived_flags', []):
        key = name
        flags[name] = {
            'produced_by': sorted(producers.get(name, [])),
            'consumed_by': sorted(consumers.get(name, [])),
            'downstream': sorted(set(downstream.get(name, []) +
                                     [stage_outputs.get(stage) for stage, rule in rules
                                      if rule['id'] in consumers.get(name, [])
                                      and stage in stage_outputs])),
        }
    resolved = context.roles.get('resolved_groups', {})
    overlaps = []
    names = sorted(resolved)
    group_lanes = defaultdict(set)
    for stage, rule in rules:
        if rule.get('group'):
            group_lanes[rule['group']].add(rule.get('lane'))
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            common = sorted(set(resolved[left]).intersection(resolved[right]))
            if not common:
                continue
            exact = set(resolved[left]) == set(resolved[right])
            if exact:
                classification = 'likely redundant'
            elif group_lanes[left] and group_lanes[right] and group_lanes[left] != group_lanes[right]:
                classification = 'potentially conflicting'
            elif len(common) >= 3:
                classification = 'intentional reuse'
            else:
                classification = 'unclear'
            overlaps.append(dict(left=left, right=right, shared_terms=common, classification=classification))
    return {
        'rules': [dict(id=r['id'], stage=stage, priority=r.get('priority'), active=r.get('active', True),
                       reads=[normalize_field(x) for x in _rule_fields(r)], writes=[normalize_field(a['field']) for a in r.get('actions', [])],
                       term_group=r.get('group') or ('pattern' if r.get('pattern') or r.get('title_pattern') else None)) for stage, r in rules],
        'fields': {field: {'produced_by': sorted(set(producers[field])),
                           'consumed_by': sorted(set(consumers[field])),
                           'downstream': downstream.get(field, [])}
                   for field in sorted(set(producers) | set(consumers))},
        'derived_flags': flags,
        'term_groups': {name: sorted(ids) for name, ids in sorted(groups.items())},
        'term_overlaps': overlaps,
    }


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def _impossible(node):
    """Small contradiction check; intentionally not a theorem prover."""
    if 'all' in node:
        leaves = [c for c in node['all'] if 'field' in c]
        by_field = defaultdict(list)
        for leaf in leaves:
            by_field[leaf['field']].append(leaf)
        for conditions in by_field.values():
            equals = {c['value'] for c in conditions if c['op'] == 'equals'}
            if len(equals) > 1:
                return True
            lows = [c['value'] for c in conditions if c['op'] in ('gte','gt')]
            highs = [c['value'] for c in conditions if c['op'] in ('lte','lt')]
            if lows and highs and max(lows) > min(highs):
                return True
        return any(_impossible(c) for c in node['all'])
    if 'any' in node:
        # An any branch is impossible only when every branch is independently impossible.
        return bool(node['any']) and all(_impossible(c) for c in node['any'])
    return False


def inspect_policy(context: GradingContext, *, input_context='db'):
    graph = dependency_graph(context)
    rules = policy_rules(context)
    issues = []
    seen = {}
    for stage, rule in rules:
        key = _canonical({k: rule.get(k) for k in (
            'when', 'actions', 'stop', 'active', 'scope', 'lane', 'weight',
            'max_hits', 'hard_exclusion', 'signal_type', 'category', 'group',
            'pattern', 'title_pattern')})
        if key in seen:
            issues.append(dict(kind='duplicate_equivalent_rule', severity='warning', rule=rule['id'], equivalent_to=seen[key]))
        seen[key] = rule['id']
    for name, info in graph['derived_flags'].items():
        if not info['produced_by']:
            issues.append(dict(kind='orphan_derived_flag', severity='warning', flag=name))
        if not info['consumed_by']:
            issues.append(dict(kind='unconsumed_derived_flag', severity='warning', flag=name))
    for stage, rule in rules:
        if rule.get('when') and _impossible(rule['when']):
            issues.append(dict(kind='possibly_never_fires', severity='warning', rule=rule['id'], reason='contradictory condition'))
        if not rule.get('active', True):
            issues.append(dict(kind='inactive_rule', severity='info', rule=rule['id']))
        if rule.get('stop') and rule.get('when') == {'field': 'always', 'op': 'equals', 'value': True}:
            later = [r['id'] for s, r in rules if s == stage and r.get('priority', 0) < rule.get('priority', 0) and r.get('active', True)]
            if later:
                issues.append(dict(kind='possibly_shadowed', severity='warning', rule=rule['id'], later_rules=later))
    raw_roles = context.snapshot.get('roles', {})
    referenced = set()
    for key, value in _walk(raw_roles):
        if key == 'group' and isinstance(value, str):
            referenced.add(value)
        if isinstance(value, str) and value.startswith('alignment.'):
            referenced.add(value)
    # Alias groups and alignment groups are rooted in their consumers; avoid falsely
    # calling authoring groups dead just because their reference is nested.
    for name, refs in raw_roles.get('term_groups', {}).items():
        if isinstance(refs, str):
            referenced.add(refs)
    for name in raw_roles.get('term_groups', {}):
        if name not in referenced and name not in graph['term_groups'] and not name.startswith('alignment.'):
            issues.append(dict(kind='possibly_unused_term_group', severity='info', group=name))
    groups_by_terms = defaultdict(list)
    for name, terms in context.roles.get('resolved_groups', {}).items():
        groups_by_terms[_canonical(sorted(terms))].append(name)
    for names in groups_by_terms.values():
        if len(names) > 1:
            issues.append(dict(kind='equivalent_term_groups', severity='info', groups=sorted(names), classification='unclear'))
    lanes = {r['lane'] for r in context.roles['lane_rules']}
    produced_lanes = set(lanes)
    for _, rule in rules:
        for action in rule.get('actions', []):
            if action.get('field') == 'eligible':
                produced_lanes.update(action.get('value', []) if isinstance(action.get('value'), list) else [action.get('value')])
            if action.get('field') == 'points.survival_lane':
                produced_lanes.add('survival_lane')
    for lane in ('target_lane','secondary_lane','bridge_lane','survival_lane','wrong_lane'):
        if lane not in produced_lanes:
            issues.append(dict(kind='possibly_unreachable_lane', severity='warning', lane=lane))
    if 'survival_lane' in produced_lanes and input_context == 'db':
        survival_rules = [r['id'] for s, r in rules if s == 'eligibility' and 'search_lane' in _rule_fields(r)]
        if survival_rules:
            issues.append(dict(kind='input_contract_unavailable', severity='info', lane='survival_lane',
                                input_context='db', field='search_lane', rules=survival_rules,
                                explanation='The DB grading view does not provide search_lane; policy is structurally reachable when that context is supplied.'))
    return dict(schema_version=1, validation='passed', input_context=input_context, issues=issues, graph=graph,
                notes=['Unknown references and malformed policy fail during GradingContext.load.',
                       'Shadowing and reachability checks are conservative and labeled possibly.',
                       'Term overlap is reported; policy terms are not automatically deduplicated.'])


def render_policy_report(report):
    lines = ['# SkillFreq policy observability report', '',
             'Generated from the loaded policy snapshot. Policy remains authored in YAML; this is an inspection view.', '',
             '## Validation and quality findings', '']
    if not report['issues']:
        lines.append('- No static findings.')
    for issue in report['issues']:
        lines.append('- '+json.dumps(issue, ensure_ascii=False, sort_keys=True))
    lines += ['', '## Derived flag dependencies', '']
    for flag, info in report['graph']['derived_flags'].items():
        lines += [f"### `{flag}`", '', f"Produced by: {', '.join(info['produced_by']) or 'none'}",
                  f"Consumed by: {', '.join(info['consumed_by']) or 'none'}",
                  f"Downstream: {', '.join(info['downstream']) or 'none'}", '']
    lines += ['## Rule dependency index', '', '| Rule | Stage | Priority | Reads | Writes | Term group |',
              '|---|---|---:|---|---|---|']
    for rule in report['graph']['rules']:
        lines.append('| {id} | {stage} | {priority} | {reads} | {writes} | {group} |'.format(
            id=rule['id'], stage=rule['stage'], priority=rule['priority'], reads=', '.join(rule['reads']),
            writes=', '.join(rule['writes']), group=rule.get('term_group') or ''))
    lines += ['', '## Term-group overlap', '']
    overlap = report['graph'].get('term_overlaps', [])
    lines += [f"- {item['left']} ↔ {item['right']}: {len(item['shared_terms'])} shared; {item['classification']}"
              for item in overlap] or ['- No overlapping resolved groups found.']
    lines += ['', '## Ecosystem taxonomy recommendation', '',
              '- Keep vendor ecosystems (Informatica, Workday, Salesforce, ServiceNow, Boomi, MuleSoft) separate from specialized domains (MDM) and data platforms (Palantir, Snowflake, Databricks, Redshift, BigQuery).',
              '- Vendor groups primarily affect concentration, specialization, ownership and fit policy.',
              '- MDM is a domain signal that can occur across products; merging it with a vendor obscures transferable data work.',
              '- Data platforms are common implementation tools in data roles, so keeping them distinct reduces accidental wrong-lane penalties.']
    return '\n'.join(lines)+'\n'


def impact_report(context, rule_id=None):
    graph = dependency_graph(context)
    rules = {r['id']: r for r in graph['rules']}
    selected = [r for r in graph['rules'] if rule_id is None or r['id'] == rule_id]
    if rule_id is not None and not selected:
        raise KeyError(f'Unknown policy rule: {rule_id}')
    result = []
    for rule in selected:
        downstream = set()
        for field in rule['writes']:
            info = graph['fields'].get(field, {})
            downstream.update(info.get('consumed_by', []))
            downstream.update(info.get('downstream', []))
        outputs = {x for f in rule['writes'] for x in graph['fields'].get(f, {}).get('downstream', [])}
        result.append(dict(rule=rule, downstream_rules=sorted(x for x in downstream if x in rules),
                           possible_outputs=sorted(outputs),
                           upstream_rules=sorted({producer for field in rule['reads']
                                                  for producer in graph['fields'].get(field, {}).get('produced_by', [])})))
    return result


def render_impact(context, rule_id=None):
    rows = impact_report(context, rule_id)
    lines = ['# SkillFreq policy impact', '',
             'This is a static dependency view. It identifies possible downstream effects; it does not predict a job count.', '']
    for row in rows:
        rule = row['rule']
        lines += [f"## `{rule['id']}`", '', f"Stage: `{rule['stage']}`; priority: `{rule['priority']}`",
                  f"Reads: {', '.join(rule['reads']) or 'none'}", f"Writes: {', '.join(rule['writes']) or 'none'}",
                  f"Downstream rules: {', '.join(row['downstream_rules']) or 'none'}",
                  f"Upstream producers: {', '.join(row['upstream_rules']) or 'none'}",
                  f"Possible outputs: {', '.join(row['possible_outputs']) or 'none'}", '']
    return '\n'.join(lines)


def write_policy_report(out: Path, *, context=None, input_context='db'):
    context = context or GradingContext.load()
    report = inspect_policy(context, input_context=input_context)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_policy_report(report), encoding='utf-8')
    out.with_suffix('.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    validation_lines = ['# SkillFreq configuration validation', '', f"Status: **{report['validation']}**", '',
                        'Schema validation is performed while loading the existing configuration. Unknown fields/operators/actions, invalid lanes, duplicate IDs, malformed patterns and invalid references fail the load.', '',
                        'Static quality findings (warnings/info):', '']
    validation_lines.extend('- '+json.dumps(issue, ensure_ascii=False, sort_keys=True) for issue in report['issues'])
    out.with_name('config-validation.md').write_text('\n'.join(validation_lines)+'\n', encoding='utf-8')
    quality = ['# Dead and shadowed policy findings', '',
               'Static checks are conservative. “Possibly” findings are candidates for review, not proof that a rule is unreachable.', '']
    findings = [i for i in report['issues'] if i['kind'] in ('possibly_never_fires','possibly_shadowed','possibly_unreachable_lane',
                                                             'unconsumed_derived_flag','orphan_derived_flag','possibly_unused_term_group')]
    quality.extend('- '+json.dumps(issue, ensure_ascii=False, sort_keys=True) for issue in findings)
    if not findings:
        quality.append('- No dead or shadowed candidates found.')
    out.with_name('dead-shadowed-rules.md').write_text('\n'.join(quality)+'\n', encoding='utf-8')
    return report


def trace_csv(input_path: Path, job_id: str, out: Path, *, context=None, prevalence=None, market_context=None):
    import csv
    csv.field_size_limit(10_000_000)
    context = context or GradingContext.load()
    with input_path.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            if str(row.get('id') or row.get('source_job_id')) == str(job_id):
                grade = grade_job(row, context, prevalence=prevalence, market_context=market_context, trace=True)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(render_trace(grade, row.get('title') or job_id), encoding='utf-8')
                out.with_suffix('.json').write_text(json.dumps(grade.to_dict(), indent=2, ensure_ascii=False), encoding='utf-8')
                return grade
    raise KeyError(f'Job id not found in {input_path}: {job_id}')
