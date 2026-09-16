"""Generate compact, deterministic traces for representative saved jobs."""
import argparse, csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.pipeline import grading_market
from skillfreq.score.grading import GradingContext, grade_job

csv.field_size_limit(10_000_000)

def choose(rows, context, prevalence, market):
    graded = {}
    def grade(row):
        if row['id'] not in graded:
            graded[row['id']] = grade_job(row, context, prevalence=prevalence, market_context=market)
        return graded[row['id']]
    def signal_ids(g): return {e.get('rule_id') for e in g.matched_role_signals}
    def rule_ids(g): return signal_ids(g) | {e.get('rule_id') for e in g.triggered_rules}
    def has_any(g, names): return bool(rule_ids(g).intersection(names))
    patterns = [
        ('clean TARGET data engineer', lambda g: g.role_lane == 'target_lane' and g.apply_decision in ('apply_now','manual_review') and not g.blocking_reasons),
        ('integration promoted by data evidence', lambda g: g.role_lane == 'target_lane' and g.observability['owners']['final_lane_rule'] == 'supported_integration_target'),
        ('integration rejected by domain conflict', lambda g: g.role_lane != 'target_lane' and 'integration_title_identity' in signal_ids(g) and has_any(g, {'security_domain_identity_guard','integration_hardware_domain_guard','hard_exclusion_override'})),
        ('ecosystem-heavy vendor specialist', lambda g: any(g.policy_flags.get(x) for x in ('ecosystem_role_concentration','ecosystem_specialized','ecosystem_ownership_gate'))),
        ('data platform usage', lambda g: g.category_hits.get('data_platform_terms',0) > 0 and not g.policy_flags.get('ecosystem_role_concentration')),
        ('SQL/PLSQL database role', lambda g: g.category_hits.get('database_development',0) > 0 or g.category_hits.get('database_usage',0) > 0),
        ('QA/test role', lambda g: has_any(g, {'qa_title_identity','test_title_identity'})),
        ('infrastructure/platform role', lambda g: g.category_hits.get('infrastructure_title_identity',0) > 0 or g.category_hits.get('platform_heavy_terms',0) > 0),
        ('bridge/support role', lambda g: g.role_lane == 'bridge_lane' and (g.category_hits.get('support_signals',0) + g.category_hits.get('bridge_positive_signals',0) > 0)),
        ('ambiguous/manual-review role', lambda g: g.apply_decision == 'manual_review' and g.ai_review_required),
    ]
    selected=[]; used=set()
    for label, predicate in patterns:
        for row in rows:
            if row.get('id') not in used and predicate(grade(row)):
                selected.append((label,row)); used.add(row.get('id')); break
    return selected

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,required=True); p.add_argument('--out',type=Path,default=Path('docs/generated/representative-traces.md')); a=p.parse_args()
    with a.input.open(encoding='utf-8-sig',newline='') as stream: rows=list(csv.DictReader(stream))
    context=GradingContext.load(); prevalence,market=grading_market(context)
    lines=['# Representative deterministic traces','',f'Source: `{a.input}`','',
           'Each section is produced by the normal grader with trace capture enabled. No explanation is generated separately.', '']
    selected = choose(rows, context, prevalence, market)
    for label,row in selected:
        grade=grade_job(row,context,prevalence=prevalence,market_context=market,trace=True)
        obs=grade.observability
        lines += [f'## {label}: {row.get("title")}', '', obs['summary'], '',
                  f"- Job id: `{grade.job_id}`", f"- Lane scores: `{json.dumps(grade.lane_scores,sort_keys=True)}`",
                  f"- Fit / learning / confidence: `{grade.fit_score}` / `{grade.learning_score}` / `{grade.confidence}`",
                  f"- Decision / AI review: `{grade.apply_decision}` / `{grade.ai_review_required}`",
                  f"- Lane owner: `{obs['owners']['final_lane_rule']}`; decision owner: `{obs['owners']['final_apply_decision_rule']}`",
                  f"- Policy flags: `{json.dumps(grade.policy_flags,sort_keys=True)}`", '- Triggered action effects:']
        for effect in obs['action_effects']:
            if effect['changed'] or effect['final_effect'] != 'no_effect':
                lines.append(f"  - `{effect['rule_id']}` → `{effect['field']}`: {effect['final_effect']}")
        lines += ['', 'Matched role signals: '+', '.join(e['rule_id'] for e in grade.matched_role_signals[:12]) or 'none', '']
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(f'Wrote {len(selected)} traces: {a.out}')

if __name__=='__main__': main()
