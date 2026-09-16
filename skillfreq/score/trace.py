"""Read the real action ledger; never re-evaluate a grading condition.

Survival is field-state provenance, not a counterfactual causal claim. A flag
overwritten later may already have been consumed by another rule.
"""
import json


def action_effects(events):
    effects = []
    for index, event in enumerate(events):
        action = event.get('action')
        if not action:
            continue
        field, op = action['field'], action['op']
        changed = event['before'] != event['result']
        effect = dict(event_index=index, rule_id=event['rule_id'], field=field,
                      changed=changed, final_effect='retained' if changed else 'no_effect',
                      overridden_by=None, bounded_by=None)
        if changed:
            for later in events[index+1:]:
                next_action = later.get('action', {})
                if next_action.get('field') != field or later.get('before') == later.get('result'):
                    continue
                if op in ('append', 'remove'):
                    item = action['value']
                    wanted = op == 'append'
                    # A later reset/remove/add must actually reverse THIS membership.
                    reversed_membership = (item in (later['result'] or [])) != wanted
                    if not reversed_membership:
                        continue
                elif next_action['op'] in ('cap_score', 'floor_score'):
                    effect.update(final_effect='bounded', bounded_by=later['rule_id'])
                    continue
                elif next_action['op'] != 'set':
                    continue
                effect.update(final_effect='overridden', overridden_by=later['rule_id'])
                break
        effects.append(effect)
    return effects


def build_observability(grade, resolution, category_hits, settings):
    events = grade.triggered_rules
    effects = action_effects(events)
    winner = grade.role_lane
    membership_owner = 'lane_policy.fallback_lane' if winner == resolution['fallback_lane'] else None
    for event in events:
        action = event.get('action', {})
        if action.get('field') == 'eligible':
            before, after = event['before'] or [], event['result'] or []
            if winner in after and winner not in before:
                membership_owner = event['rule_id']
            elif winner not in after:
                membership_owner = None
    lane_support = [e['rule_id'] for e in events if
                    (e.get('lane') == winner and e.get('contribution', 0) > 0)
                    or (e.get('action', {}).get('field') in ('eligible', 'points.'+winner)
                        and e.get('changed'))]
    def last_writer(field):
        return next((e['rule_id'] for e in reversed(events)
                     if e.get('action', {}).get('field') == field), None)
    owners = dict(
        final_lane_rule=membership_owner,
        final_lane_resolver='maximum score among eligible lanes; canonical lane order breaks ties',
        lane_supporting_contributors=list(dict.fromkeys(lane_support)),
        lane_overridden_contributors=[e for e in effects if e['field'] == 'eligible' and e['final_effect'] == 'overridden'],
        final_fit_modifiers=[e for e in effects if e['field']=='fit_score' and e['changed']],
        final_apply_decision_rule=last_writer('apply_decision'),
        final_ai_review_rule='ai_review_gate')
    title_terms = list(dict.fromkeys(t for e in grade.matched_role_signals if e['scope']=='title' for t in e['matched_terms']))
    concepts = list(grade.matched_capability_concepts)
    restrictions = list(dict.fromkeys(e['rule_id'] for e in events
                                     if e.get('action', {}).get('field')=='eligible'
                                     and set(e['before'] or []) - set(e['result'] or [])))
    parts = [f"{winner}: eligibility established by {membership_owner or 'configured fallback'}; selected by eligible lane scores."]
    if title_terms:
        parts.append('Title evidence: '+', '.join(title_terms[:5])+'.')
    if concepts:
        parts.append('Capability evidence: '+', '.join(concepts[:6])+'.')
    if restrictions:
        parts.append('Lane restrictions: '+', '.join(restrictions)+'.')
    if grade.blocking_reasons:
        parts.append('Blockers: '+', '.join(grade.blocking_reasons)+'.')
    elif grade.review_flags:
        parts.append('Review flags: '+', '.join(grade.review_flags)+'.')
    parts.append(f"Fit {grade.fit_score:g}; {grade.apply_decision} by {owners['final_apply_decision_rule']}.")
    return dict(schema_version=1, owners=owners, action_effects=effects,
                lane_resolution=resolution, category_hits=category_hits,
                confidence_policy=settings['confidence'], summary=' '.join(parts),
                provenance_scope='Field-state survival; overwritten flags can have earlier downstream effects. Lane owner establishes eligibility, resolver selects the winner.')


def render_trace(grade, title='Job'):
    """Render saved evidence, including optional full engine evaluation history."""
    data = grade.to_dict() if hasattr(grade, 'to_dict') else grade
    obs = data.get('observability')
    if not obs:
        raise ValueError('This grade predates trace instrumentation; explicitly regrade it with trace-job.')
    compact = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True)
    lines = [f'# {title}', '', obs['summary'], '',
             f"Grading `{data['grading_version']}`; taxonomy `{data['taxonomy_version']}`.", '',
             '## Role evidence', '']
    for event in data['matched_role_signals']:
        lines.append(f"- `{event['rule_id']}` ({event['scope']}, group `{event.get('term_group')}`): {', '.join(event['matched_terms'])}; {event['lane']} {event['contribution']:+g}")
    lines += ['', 'Counts: '+compact(obs['category_hits']), '', 'Atomic skills: '+compact(data['matched_atomic_skills']),
              '', 'Capability concepts: '+compact(data['matched_capability_concepts']),
              '', '## Requirements', '',
              'Groups retain section, source sentence, grammar type and candidate satisfaction.', '']
    for section, key in (('required', 'missing_required_skills'), ('preferred', 'missing_preferred_skills')):
        lines.append(f'### {section}')
        lines.append('Individual gaps: '+compact(data[key]['atomic_skills']))
        lines.append('Unsatisfied requirement groups: '+compact([g['group_id'] for g in data[key].get('unsatisfied_groups', [])]))
        for group in data[key].get('requirement_groups', []):
            impact = sum(e.get('contribution', 0) for e in data['triggered_rules']
                         if e.get('group_id') == group['group_id'] and e.get('kind') == 'fit')
            lines.append(f"- `{group['group_id']}` `{group['type']}` (source section: {group.get('source_section', section)}): {group['source']} — options {compact(group['skills'])}; satisfied skills {compact(group.get('candidate_satisfied_skills', []))}; equivalent evidence {compact(group.get('equivalent_evidence', []))}; group satisfied: `{group.get('satisfied')}`; group fit contribution: {impact:+g}")
            if group['type'] == 'all_of':
                lines.append('  - Individual missing skills are charged in the fit ledger; no additional group charge.')
            elif group['type'] == 'ambiguous':
                lines.append('  - Unresolved mixed grammar: review evidence, no individual or group charge.')
        if not data[key].get('requirement_groups'):
            lines.append('- No sentence-level requirement groups were extracted; legacy mention fallback applies.')
        lines.append('')
    lines += ['Interpretation routing: '+compact(data.get('requirement_flags', {}).get('requirement_interpretation', [])),
              '', 'Legacy flags consume structured all-of evidence and unstructured sentence fallback; alternatives and ambiguous sentences are excluded.',
              '', 'Requirement flags: '+compact({k:v for k,v in data.get('requirement_flags', {}).items()
                                                if k not in ('requirement_interpretation','requirement_evidence')}), '']
    lines += [
              '', 'Required gaps: '+compact(data['missing_required_skills']),
              '', 'Preferred gaps: '+compact(data['missing_preferred_skills']),
              '', 'Seniority: '+compact(data['seniority_signals']), '', '## Derived flags and lane eligibility', '',
              'Final flags: '+compact(data['policy_flags']), '', 'Resolution: '+compact(obs['lane_resolution']),
              '', 'Raw scores: '+compact(data['raw_lane_scores']), '', 'Final scores: '+compact(data['lane_scores']), '',
              '## Applied actions and surviving effects', '',
              'Survival describes the written field, not every downstream consequence. Bounded fit contributions are not counterfactual marginal effects.', '']
    effects = {e['event_index']: e for e in obs['action_effects']}
    for index, event in enumerate(data['triggered_rules']):
        if index not in effects:
            continue
        effect = effects[index]
        lines += [f"- `{event['rule_id']}`: {compact(event['action'])}",
                  f"  - Inputs: {compact(event.get('inputs', {}))}",
                  f"  - Before: {compact(event['before'])}; after: {compact(event['result'])}",
                  f"  - Effect: {effect['final_effect']}; overridden by: {effect['overridden_by']}; bounded by: {effect['bounded_by']}"]
    lines += ['', '## Fit and decision', '']
    for event in data['triggered_rules']:
        if event.get('kind') == 'fit':
            detail = event.get('skill') or event.get('group_id') or event.get('concepts') or ''
            lines.append(f"- `{event['rule_id']}`: contribution {event.get('contribution', 0):+g}; {compact(detail)}")
    lines += ['', f"Fit: {data['fit_score']}; quality: {data['fit_quality']}; apply: {data['apply_decision']}.",
              '', 'Blockers: '+compact(data['blocking_reasons']), '', 'Review flags: '+compact(data['review_flags']),
              '', 'Owners: '+compact(obs['owners']), '', '## Learning', '',
              f"Score: {data['learning_score']}; status: {data['learning_status']}.", '', compact(data['growth_skills']),
              '', '## Confidence and AI review', '',
              f"Confidence: {data['confidence']} (heuristic, not probability); AI review: {data['ai_review_required']}.",
              '', compact(data['confidence_evidence']), '', 'Configuration: '+compact(obs['confidence_policy']),
              '', 'Review reasons: '+compact(data['ai_review_reasons'])]
    if 'evaluations' in obs:
        lines += ['', '## Full policy evaluation history', '', 'Unmatched/inactive/stopped rules are recorded by the same evaluator; stopped rules were not evaluated.', '']
        for event in obs['evaluations']:
            lines.append(f"- `{event['stage']}:{event['rule_id']}`: {event['status']}; inputs {compact(event.get('inputs', {}))}" + (f"; stopped by `{event['stopped_by']}`" if event.get('stopped_by') else ''))
    return '\n'.join(lines)+'\n'
