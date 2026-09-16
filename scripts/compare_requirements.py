"""Compare saved requirement semantics; never reevaluate grading rules.

Stream paired rows, verify inputs, compare gap sets, retain every changed source.
"""
import argparse
from collections import Counter
import csv
from itertools import zip_longest
import json
import re
from pathlib import Path
import sys
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.score.trace import render_trace

csv.field_size_limit(10_000_000)
SCORES = ('fit_score', 'fit_quality', 'apply_decision', 'ai_review_required',
          'role_lane', 'learning_score', 'alignment_score', 'label')


def groups(grade, section='required'):
    return grade['missing_'+section+'_skills'].get('requirement_groups', [])


def signature(group):
    return (group['section'], group['source'], group['type'], tuple(sorted(group['skills'])))


def ledger(grade):
    return [e for e in grade['triggered_rules'] if e['rule_id'] in (
        'fit_missing_required_atomic', 'fit_missing_preferred_atomic', 'fit_unsatisfied_required_group',
        'fit_has_hard_requirement_blockers', 'fit_has_modern_stack_blockers',
        'alignment:mandatory_missing', 'alignment:modern_required', 'alignment:modern_preferred')]


def interpretation(grade):
    return dict(required=grade['missing_required_skills'], preferred=grade['missing_preferred_skills'],
                ledger=ledger(grade), ambiguity=grade['confidence_evidence']['requirement_ambiguity'],
                seniority=grade['seniority_signals'], section_alignment=section_alignment(grade),
                **{key:grade[key] for key in SCORES})


def section_alignment(grade):
    return [e for e in grade['triggered_rules'] if e['rule_id'] in (
        'alignment:years', 'alignment:early_career', 'alignment:no_experience')]


def section_changed(before, after):
    return (before['seniority_signals']['years_required'] != after['seniority_signals']['years_required']
            or section_alignment(before) != section_alignment(after))


def attribute(before, after):
    """Evidence-backed categories, not isolated counterfactual causal claims."""
    all_groups = groups(after) + groups(after, 'preferred')
    causes = []
    if any(g['type'] == 'any_of' and g['satisfied'] is False for g in all_groups):
        causes.append('unsatisfied alternative group')
    if any(g['type'] == 'any_of' and g['satisfied'] is True for g in all_groups):
        causes.append('satisfied alternative group')
    if any(g['type'] == 'equivalent' for g in all_groups):
        causes.append('equivalent requirement handling')
    if any(g['type'] == 'ambiguous' for g in all_groups):
        causes.append('mixed-grammar ambiguity')
    old = {signature(g) for s in ('required', 'preferred') for g in groups(before, s)}
    new = {signature(g) for g in all_groups}
    if old != new or ledger(before) != ledger(after) or section_changed(before, after):
        causes.append('legacy/group reconciliation')
    return causes


def aggregate():
    return dict(jobs=0, role_lane=Counter(), apply_decision=Counter(), fit_quality=Counter(),
                fit_sum=0, learning_sum=0, nonzero_learning=0, ai_review_count=0)


def add(state, grade):
    state['jobs'] += 1
    for key in ('role_lane', 'apply_decision', 'fit_quality'):
        state[key][grade[key]] += 1
    state['fit_sum'] += grade['fit_score']
    state['learning_sum'] += grade['learning_score'] or 0
    state['nonzero_learning'] += (grade['learning_score'] or 0) > 0
    state['ai_review_count'] += grade['ai_review_required']


def finish(state):
    state['average_fit'] = round(state.pop('fit_sum') / max(1, state['jobs']), 6)
    state['average_learning'] = round(state.pop('learning_sum') / max(1, state['jobs']), 6)
    state['ai_review_rate_pct'] = round(100*state['ai_review_count']/max(1, state['jobs']), 4)
    return state


def select_examples(changes, limit=30):
    selected = []
    for category in ('satisfied alternative group', 'unsatisfied alternative group', 'equivalent requirement handling',
                     'mixed-grammar ambiguity', 'legacy/group reconciliation'):
        candidates = sorted((c for c in changes if category in c['attribution']), key=lambda c: (
            'apply_decision' not in c['fields'], 'fit_score' not in c['fields'],
            -abs(c['after']['fit_score']-c['before']['fit_score'])))
        for candidate in candidates[:6]:
            if candidate not in selected:
                selected.append(candidate)
    for candidate in changes:
        if len(selected) >= limit:
            break
        if candidate not in selected:
            selected.append(candidate)
    return selected


def explain(change):
    before, after = change['before'], change['after']
    lines = [f"### {change['title']} (`{change['id']}`)", '',
             '- Changed: '+', '.join(change['fields']), '- Attribution: '+', '.join(change['attribution']),
             f"- Lane: {before['role_lane']} → {after['role_lane']}; fit: {before['fit_score']} → {after['fit_score']}; decision: {before['apply_decision']} → {after['apply_decision']}",
             f"- Required atomic gaps: {before['required']['atomic_skills']} → {after['required']['atomic_skills']}",
             f"- Preferred atomic gaps: {before['preferred']['atomic_skills']} → {after['preferred']['atomic_skills']}",
             f"- Required group gaps: {len(before['required'].get('unsatisfied_groups', []))} → {len(after['required'].get('unsatisfied_groups', []))}", '']
    if change.get('section_context_changes'):
        lines += ['- Inline-preferred section-boundary correction also affected experience/section-scoped alignment.',
                  f"- Years required: {before['seniority']['years_required']} → {after['seniority']['years_required']}.",
                  f"- Section alignment events: {before['section_alignment']} → {after['section_alignment']}."]
        lines.extend('- Section context source: '+source for source in change['section_context_changes'])
    for section in ('required', 'preferred'):
        old = {g['source']:g for g in before[section].get('requirement_groups', [])}
        for group in after[section].get('requirement_groups', []):
            previous = old.pop(group['source'], None)
            summary = lambda g: f"{g['type']} {g['skills']}; satisfied={g.get('satisfied')}; known={g.get('candidate_satisfied_skills', [])}"
            lines += [f"- Source ({section}): {group['source']}",
                      f"  - Before: {summary(previous) if previous else 'no matching sentence-level group'}",
                      f"  - After: {summary(group)}; grammar={group.get('grammar')}"]
        for group in old.values():
            lines.append(f"- Previous source ({section}), removed/resegmented: {group['source']} ({group['type']})")
    for name, value in (('before', before), ('after', after)):
        lines += ['', f'Requirement penalty ledger {name}: `'+json.dumps(value['ledger'], ensure_ascii=False)+'`']
    return lines+['']


def lead_audit(row, before, after, path):
    lines = ['# Lead Analyst Data Engineer — requirement audit', '', f"Job `{row['id']}`.", '',
             'Sources are lowercased extractor spans from the frozen JD. Contributions are pre-cap fit ledger entries, not hypothetical marginal scores.', '',
             f"Lane: {before['role_lane']} → {after['role_lane']}; fit: {before['fit_score']} → {after['fit_score']}; apply: {before['apply_decision']} → {after['apply_decision']}.", '',
             'The previous colon heuristic treated “services:” and “databases:” as alternatives without an OR/example cue. A colon alone does not establish alternatives. AWS is charged once despite appearing in two required sentences.', '']
    for skill in ('Databricks', 'Spark', 'AWS', 'Redshift', 'Power BI'):
        penalty = lambda grade: sum(e.get('contribution', 0) for e in grade['triggered_rules']
                                    if e['rule_id'] == 'fit_missing_required_atomic' and e.get('skill') == skill)
        lines += [f'## {skill}', '', f'Individual required fit contribution: {penalty(before):+g} → {penalty(after):+g}.', '']
        for group in groups(after):
            if skill not in group['skills']:
                continue
            previous = next((g for g in groups(before) if g['source'] == group['source']), None)
            lines += [f"- Source: {group['source']}", f"- Section: {group['source_section']}; type: {previous['type'] if previous else 'absent'} → {group['type']}; grammar: {group['grammar']}.",
                      f"- Individually required: {group['type'] == 'all_of'}; alternative/example: {group['type'] in ('any_of','equivalent')}.",
                      f"- Candidate matched: {group['candidate_satisfied_skills']}; whole group satisfied: {group['satisfied']}."]
    lines += ['', '## Interpretation limits', '',
              'PySpark maps to Spark under the unchanged taxonomy. Parenthetical “PySpark/Pandas” remains all-of under the bounded grammar; whether that slash permits Pandas alone deserves manual review. No Pandas equivalence was invented.', '',
              '“Mentoring junior architects and engineers” appears under preferred qualifications. The existing early-career section-scope correction remains intact.', '',
              'Not every listed AWS service or database is modeled in the taxonomy. No new taxonomy entries or candidate experience were inferred.', '']
    path.write_text('\n'.join(lines), encoding='utf-8')
    path.with_name('lead-analyst-requirement-trace.md').write_text(render_trace(after, row['title']), encoding='utf-8')


def compare(before_path, after_path, output):
    states, versions = [aggregate(), aggregate()], [set(), set()]
    changes, counts, unexplained = [], Counter(), []
    output.parent.mkdir(parents=True, exist_ok=True)
    lead = None
    with before_path.open(encoding='utf-8-sig', newline='') as left, after_path.open(encoding='utf-8-sig', newline='') as right:
        for position, pair in enumerate(zip_longest(csv.DictReader(left), csv.DictReader(right)), 1):
            if any(row is None for row in pair):
                raise ValueError('Cohort row counts differ')
            old_row, new_row = pair
            identity = ('id', 'source_site', 'source', 'title', 'description', 'search_lane', 'review_priority')
            if any(old_row.get(k) != new_row.get(k) for k in identity):
                raise ValueError(f'Cohort inputs differ at row {position}')
            before, after = [json.loads(row['grade_json']) for row in pair]
            for index, grade in enumerate((before, after)):
                add(states[index], grade)
                versions[index].add(grade['grading_version'])
            if old_row['title'] == 'Lead Analyst Data Engineer':
                lead = (old_row, before, after)
            fields = []
            for section in ('required', 'preferred'):
                old_gaps, new_gaps = [g['missing_'+section+'_skills'] for g in (before, after)]
                if set(old_gaps['atomic_skills']) != set(new_gaps['atomic_skills']):
                    fields.append(section+'_atomic_gaps')
                if {signature(g) for g in old_gaps.get('unsatisfied_groups', [])} != {signature(g) for g in new_gaps.get('unsatisfied_groups', [])}:
                    fields.append(section+'_group_gaps')
            fields.extend(key for key in SCORES if before[key] != after[key])
            if not fields:
                continue
            counts.update(fields)
            attribution = attribute(before, after)
            if not attribution:
                unexplained.append(old_row['id'])
            changes.append(dict(id=old_row['id'], source_site=old_row['source_site'], title=old_row['title'],
                                fields=fields, attribution=attribution, before=interpretation(before), after=interpretation(after),
                                section_context_changes=[line.strip() for line in old_row['description'].splitlines()
                                    if re.search(r'\bpreferred\b|\byears?\b', line, re.I)] if section_changed(before, after) else []))
    summary = dict(before=finish(states[0]), after=finish(states[1]), versions=[sorted(v) for v in versions],
                   changed_jobs=len(changes), changed_fields=dict(counts), unexplained=unexplained,
                   input_parity='identical ordered identities, titles, descriptions and search context')
    summary['section_boundary_effect_jobs'] = sum(bool(c['section_context_changes']) for c in changes)
    snapshots = [p.with_suffix('.grading.yml') for p in (before_path, after_path)]
    if all(p.exists() for p in snapshots):
        old_config, new_config = [yaml.safe_load(p.read_text(encoding='utf-8'))['configuration'] for p in snapshots]
        protected = {key:old_config[key] == new_config[key] for key in ('roles','skills','profile','market_skills')}
        for config in (old_config, new_config):
            config['weights']['fit'].pop('required_group_penalty', None)
        protected['weights_except_new_group_penalty'] = old_config['weights'] == new_config['weights']
        summary['protected_configuration_parity'] = protected
    lines = ['# Requirement group semantics — frozen-cohort impact', '', f'Before: `{before_path}`', f'After: `{after_path}`', '',
             'Saved market prevalence is reused. Atomic gap order is ignored. Each input row and description is checked before comparison.', '',
             f'Changed jobs (including new explicit group-gap representation): **{len(changes)}**.', '',
             '| Metric | Before | After |', '|---|---|---|']
    for key in ('jobs', 'role_lane', 'apply_decision', 'fit_quality', 'average_fit', 'average_learning', 'nonzero_learning', 'ai_review_rate_pct'):
        lines.append(f"| {key} | {summary['before'][key]} | {summary['after'][key]} |")
    lines += ['', '## Changed fields', '', '| Field | Jobs |', '|---|---:|']
    for key in ('required_atomic_gaps', 'preferred_atomic_gaps', 'required_group_gaps', 'preferred_group_gaps') + SCORES:
        lines.append(f'| {key} | {counts[key]} |')
    lines += ['', f'Unattributed changes: {len(unexplained)}.', '',
              'Protected configuration parity: '+json.dumps(summary.get('protected_configuration_parity', 'snapshots unavailable'))+'.', '',
              f"Inline-preferred boundary effects on years/section-scoped alignment: {summary['section_boundary_effect_jobs']} jobs. These are included under legacy/group reconciliation with source lines and before/after evidence in JSON; they are not threshold changes.", '',
              'Group-gap counts compare the old absent gap representation against explicit gaps; previously `satisfied=false` alone did not generate a penalty.', '',
              'The JSON companion retains source groups, penalty ledgers and attribution for every changed job. Categories overlap; they identify observed semantic changes, not isolated counterfactual effects.', '',
              '## Representative changed cases', '']
    for change in select_examples(changes):
        lines.extend(explain(change))
    output.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    output.with_suffix('.json').write_text(json.dumps(dict(summary, changes=changes), ensure_ascii=False, indent=2), encoding='utf-8')
    if lead:
        lead_audit(*lead, output.with_name('lead-analyst-requirement-audit.md'))
    print(json.dumps(summary, indent=2))
    if counts['role_lane'] or counts['learning_score'] or unexplained or not all(summary.get('protected_configuration_parity', {}).values()):
        raise ValueError('Unexpected lane/learning drift or unattributed changes; inspect report')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('docs/generated/requirements-impact.md'))
    args = parser.parse_args()
    compare(args.before, args.after, args.out)
