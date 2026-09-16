"""Compare the focused domain pass against its preserved calibrated DB cohort.

This is reporting only: it neither grades jobs nor recomputes market prevalence.
"""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re

from compare_calibration import load, metrics


def enriched(path):
    rows = load(path)
    with path.open(encoding='utf-8', newline='') as stream:
        for raw in csv.DictReader(stream):
            row = rows[(raw['source_site'], raw['id'] or raw['source'])]
            grade = json.loads(raw['grade_json'])
            row['signals'] = {e['category']: e['matched_terms'] for e in grade['matched_role_signals']}
            row['missing_atomic'] = grade['missing_required_skills']['atomic_skills']
            row['preferred_atomic'] = grade['missing_preferred_skills']['atomic_skills']
            row['atomic'] = [e['canonical_skill'] for e in grade['matched_atomic_skills']]
            row['policy_flags'] = grade.get('policy_flags', {})
            row['fit_rules'] = list(dict.fromkeys(e['rule_id'] for e in grade['triggered_rules'] if e['kind']=='fit'))
    return rows


def report(before, after, output):
    a, b = enriched(before), enriched(after)
    common = sorted(a.keys() & b.keys())
    changed_text = sum(a[k]['text_digest'] != b[k]['text_digest'] for k in common)
    if a.keys() != b.keys() or changed_text:
        raise ValueError('Comparison requires the same source identities and unchanged job text; freeze the baseline cohort before comparing.')
    am, bm = metrics(list(a.values())), metrics(list(b.values()))
    summary = dict(before=am, after=bm, matched=len(common), changed_job_text=changed_text)
    lines = ['# Focused domain calibration: 90-day DB comparison', '',
             f'Before: `{before}`. After: `{after}`.',
             f'All {len(common):,} source identities match; no title or description changed.',
             f'Grading versions: `{am["grading_versions"]}` → `{bm["grading_versions"]}`.',
             f'Market taxonomy unchanged: `{bm["taxonomy_versions"]}`. Original exports and snapshots are preserved.', '',
             '## Aggregate results', '', '| Metric | Before | After |', '|---|---:|---:|']
    for field in ('jobs', 'average_fit', 'average_learning', 'nonzero_learning', 'unavailable_learning', 'ai_review_pct'):
        lines.append(f'| {field} | {am[field]} | {bm[field]} |')
    for field in ('role_lane', 'apply_decision', 'fit_quality'):
        for outcome in sorted(am[field].keys() | bm[field].keys()):
            lines.append(f'| {outcome} | {am[field].get(outcome,0)} | {bm[field].get(outcome,0)} |')
    lines += ['', '## Apply decisions by lane', '', '| Lane | Decision | Before count (%) | After count (%) |', '|---|---|---:|---:|']
    for lane in sorted(am['by_lane'].keys() | bm['by_lane'].keys()):
        for decision in ('apply_now', 'manual_review', 'skip'):
            x, y = am['by_lane'].get(lane, {}), bm['by_lane'].get(lane, {})
            lines.append(f'| {lane} | {decision} | {x.get("decisions",{}).get(decision,0)} ({x.get("decision_pct",{}).get(decision,0)}%) | {y.get("decisions",{}).get(decision,0)} ({y.get("decision_pct",{}).get(decision,0)}%) |')

    integration = [k for k in common if re.search(r'\bintegration engineer\b', b[k]['title'], re.I)]
    ecosystem = [k for k in common if b[k]['signals'].get('ecosystem_terms') or b[k]['signals'].get('ecosystem_title')]
    database = [k for k in common if re.search(r'\bsql\b|plsql|database|postgres', b[k]['title'], re.I)
                or {'SQL Server','PostgreSQL'} & set(b[k]['atomic'])]
    summary['integration'] = dict(total=len(integration), before_target=sum(a[k]['role_lane']=='target_lane' for k in integration),
        after_target=sum(b[k]['role_lane']=='target_lane' for k in integration),
        retained_target=sum(a[k]['role_lane']==b[k]['role_lane']=='target_lane' for k in integration),
        new_lanes=dict(Counter(b[k]['role_lane'] for k in integration)))
    lines += ['', '## Integration title cohort', '', f'`{json.dumps(summary["integration"])}`', '',
              'Cohort membership uses the phrase “integration engineer” in the title only for reporting. Grading uses configured title patterns and description evidence.']

    changed = lambda k: a[k]['role_lane'] != b[k]['role_lane']
    delta = lambda k: abs(b[k]['fit']-a[k]['fit'])
    def choose(pool, required=(), retained=2):
        ordered = [k for title in required for k in sorted(pool, key=lambda k:(b[k]['role_lane']!='target_lane',-delta(k),k)) if b[k]['title']==title]
        ordered += sorted((k for k in pool if a[k]['role_lane']==b[k]['role_lane']=='target_lane'), key=lambda k:(-b[k]['fit'],k))[:retained]
        ordered += sorted(pool, key=lambda k:(not changed(k),-delta(k),k))
        result, seen = [], set()
        for k in ordered:
            if b[k]['title'] in seen: continue
            seen.add(b[k]['title']); result.append(k)
            if len(result)==10: break
        if len(result)<10: raise ValueError('Fewer than ten distinct representative titles')
        return result

    selected = {
        'Integration Engineer examples': choose(integration, ['Application Security Integration Engineer','Flight Controls Integration Engineer','Windchill Integration Engineer','Integration Engineer']),
        'Ecosystem examples': choose([k for k in ecosystem if b[k]['signals'].get('ecosystem_title')
            or a[k]['role_lane']==b[k]['role_lane']=='target_lane' or b[k]['title']=='Data Engineer - Oracle PL/SQL'],
            ['Informatica MDM Support & Data Operations Specialist','Data Engineer - Oracle PL/SQL','Windchill Integration Engineer',
             'Senior SAP Cloud ALM, Integration & ABAP Engineer','Senior Integration Boomi Engineer']),
        'Database / SQL examples': choose([k for k in database if re.search(r'sql|database|postgres',b[k]['title'],re.I)
            or re.search(r'data.*engineer|etl.*developer',b[k]['title'],re.I)],
            ['Data Engineer - Oracle PL/SQL','SQL Developer','Database Developer']),
    }
    def safe(value): return str(value).replace('|','/').replace('\n',' ')
    summary['examples'] = {}
    for heading, keys in selected.items():
        lines += ['', f'## {heading}', '',
                  '| Title / ID | Old lane | New lane | Old fit | New fit | Old decision | New decision | Main triggered policy rules |',
                  '|---|---|---|---:|---:|---|---|---|']
        summary['examples'][heading] = []
        for k in keys:
            x,y = a[k],b[k]
            primary = [r for r in y['rules'] if r not in ('data_evidence','secondary_eligibility','bridge_evidence','transferable_data_identity','ai_review_gate')]
            evidence = list(dict.fromkeys(primary + y['blockers']))
            lines.append(f'| {safe(y["title"])} ({y["id"]}) | {x["role_lane"]} | {y["role_lane"]} | {x["fit"]} | {y["fit"]} | {x["apply_decision"]} | {y["apply_decision"]} | {safe(", ".join(evidence))} |')
            summary['examples'][heading].append(dict(title=y['title'],id=y['id'],old_lane=x['role_lane'],new_lane=y['role_lane'],old_fit=x['fit'],new_fit=y['fit'],old_decision=x['apply_decision'],new_decision=y['apply_decision'],rules=evidence,signals=y['signals'],old_missing_atomic=x['missing_atomic'],new_missing_atomic=y['missing_atomic']))

    lines += ['', '## Evidence behind the examples', '',
              'Boundary-matched terms below are facts extracted from the actual stored descriptions/titles. The full grade JSON preserves action traces, raw scores, excluded lanes, confidence, requirements and provenance.']
    for k in dict.fromkeys(k for keys in selected.values() for k in keys):
        x,y=a[k],b[k]
        facts={category:terms for category,terms in y['signals'].items() if category.startswith('ecosystem') or category in {
            'database_development','integration_data','database_usage','integration_title_identity','security_title_identity','hardware_title_identity','hardware_responsibilities','data_stack_usage'}}
        lines += ['', f'### {safe(y["title"])} ({y["id"]})', '',
                  f'- Identity/development evidence: `{safe(json.dumps(facts,ensure_ascii=False))}`',
                  f'- AI review required: `{x["ai"]}` → `{y["ai"]}`.',
                  f'- Required atomic gaps: `{x["missing_atomic"]}` → `{y["missing_atomic"]}`.',
                  f'- Preferred atomic gaps: `{x["preferred_atomic"]}` → `{y["preferred_atomic"]}`.']

    summary['atomic_gaps']={}
    lines += ['', '## Confirmed database experience', '', '| Atomic technology | Required gaps before → after | Preferred gaps before → after |', '|---|---:|---:|']
    for skill in ('SQL Server','PostgreSQL','MySQL'):
        counts={field:[sum(skill in rows[k][field] for k in common) for rows in (a,b)] for field in ('missing_atomic','preferred_atomic')}
        summary['atomic_gaps'][skill]=counts
        lines.append(f'| {skill} | {counts["missing_atomic"][0]} → {counts["missing_atomic"][1]} | {counts["preferred_atomic"][0]} → {counts["preferred_atomic"][1]} |')
    summary['ecosystem_target_removed']=sum(a[k]['role_lane']=='target_lane' and b[k]['role_lane']!='target_lane' and 'ecosystem_identity_guard' in b[k]['rules'] for k in ecosystem)
    lines += ['', '## Interpretation and remaining manual checks', '',
              f'{summary["ecosystem_target_removed"]} previously TARGET ecosystem postings now lose TARGET with `ecosystem_identity_guard` evidence.',
              'The actual Oracle PL/SQL posting asks for Oracle SQL and PLSQL development, Informatica PowerCenter ETL and production support. PLSQL spelling was absent from the evidence model; this is a reusable database-development gap, not a title exception. Mentoring/leadership still warrants manual review.',
              'SQL Server 1.0 and PostgreSQL 0.7 reflect candidate-confirmed experience. They are no longer fully missing; MySQL is still independent. Known PostgreSQL no longer earns missing-skill learning value. Therefore a lower aggregate learning score can be correct.',
              'Modern data technologies remain positive/neutral tool evidence, separate from infrastructure ownership. The new SQL + data-stack rule requires supporting signals; a technology alone cannot establish a lane.',
              'Short or conflicting descriptions can still request AI review even with high fit. Confidence is heuristic, not a calibrated probability. No AI was called.',
              'Inspect security title scope, embedded/control-system titles, PLM/CAD ownership wording and borderline vendor titles. Title-pattern co-occurrence is intentionally simple and can overmatch compound titles. Change YAML policy when career preferences differ.',
              'Specific manual check: Senior Integration Boomi Engineer (li-4428703372) stays a plausible transferable integration role, but explicitly requests 3–5+ years of Dell Boomi. It becomes TARGET/APPLY NOW under current policy. Confirm whether that product experience should be a gate; the retained ecosystem experience rule begins at five required years and the role does not claim platform administration. This is not evidence that the candidate already knows Boomi.',
              'Other inspected boundaries: Python/React Developer (li-4430708650) becomes SECONDARY/MANUAL REVIEW because of database/query-optimization work, despite substantial frontend work. Business Strategy Analyst Lead (li-4426877231) becomes BRIDGE/MANUAL REVIEW with SQL/Python/Snowflake analytics evidence; its senior strategic responsibilities still deserve scrutiny. Integration Specialist (li-4427839411) contains transferable SQL/EDI/data-exchange work but lists a German work location, outside this domain-only calibration.',
              'Search lane/review priority remain optional and absent from this DB view. The market population is the existing extraction scope rather than this 90-day job cohort.',
              f'After market provenance: `{json.dumps(next(iter(b.values()))["market"])}`.',
              'No grading evaluator, fit/decision engine, schema, canonical taxonomy or prevalence calculation changed in this pass. Config snapshots identify the exact profile and policy that produced every grade.']
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    output.with_suffix('.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='examples'},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--before',type=Path,default=Path('data/outputs/results-db-90-days-calibrated.csv'))
    parser.add_argument('--after',type=Path,default=Path('data/outputs/results-db-90-days-domain.csv'))
    parser.add_argument('--out',type=Path,default=Path('docs/domain-calibration-comparison.md'))
    args=parser.parse_args()
    report(args.before,args.after,args.out)
