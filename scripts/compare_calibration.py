"""Compare saved grading runs without recomputing scores or prevalence."""
import argparse
from collections import Counter
import csv
import json
import hashlib
from pathlib import Path
from statistics import mean

csv.field_size_limit(10_000_000)


def load(path):
    rows = {}
    with path.open(encoding='utf-8',newline='') as stream:
        for row in csv.DictReader(stream):
            grade=json.loads(row['grade_json'])
            key=(row['source_site'],row['id'] or row['source'])
            if key in rows: raise ValueError(f'Duplicate source identity: {key}')
            row['fit']=float(row['fit_score'])
            row['learning']=float(row['learning_score']) if row['learning_score'] else None
            row['ai']=row['ai_review_required'].lower()=='true'
            row['growth']=grade['growth_skills']
            row['blockers']=grade.get('blocking_reasons',[])
            row['rules']=list(dict.fromkeys(e['rule_id'] for e in grade['triggered_rules'] if e['kind'] in ('decision','override')))
            row['platform']=any(e.get('category')=='platform_heavy_terms' for e in grade['matched_role_signals'])
            row['market']=grade['market_context']
            row['text_digest']=hashlib.sha256((row['title']+'\0'+row['description']).encode()).hexdigest()
            row['description']=row['description'][:1600]
            del row['grade_json']
            rows[key]=row
    return rows


def metrics(rows):
    n=len(rows)
    result={'jobs':n}
    result['grading_versions']=sorted(set(r['grading_version'] for r in rows))
    result['taxonomy_versions']=sorted(set(r['taxonomy_version'] for r in rows))
    for field in ('role_lane','apply_decision','fit_quality'):
        result[field]=dict(Counter(r[field] for r in rows))
    result['average_fit']=round(mean(r['fit'] for r in rows),2) if n else None
    available=[r['learning'] for r in rows if r['learning'] is not None]
    result['average_learning']=round(mean(available),2) if available else None
    result['nonzero_learning']=sum((r['learning'] or 0)>0 for r in rows)
    result['unavailable_learning']=n-len(available)
    result['market_unavailable_count']=sum(r['market'].get('source') in {'unavailable','offline'} for r in rows)
    result['ai_review_pct']=round(100*sum(r['ai'] for r in rows)/n,2) if n else 0
    result['by_lane']={}
    for lane in sorted(set(r['role_lane'] for r in rows)):
        jobs=[r for r in rows if r['role_lane']==lane]
        result['by_lane'][lane]=dict(count=len(jobs),decisions=dict(Counter(r['apply_decision'] for r in jobs)),
            fit_quality=dict(Counter(r['fit_quality'] for r in jobs)),
            decision_pct={d:round(100*sum(r['apply_decision']==d for r in jobs)/len(jobs),2)
                          for d in ('apply_now','manual_review','skip')})
    return result


def report(before,after,output):
    a,b=load(before),load(after)
    common=a.keys() & b.keys()
    if not common: raise ValueError('No matching source identities')
    am,bm=metrics(list(a.values())),metrics(list(b.values()))
    result=dict(before=am,after=bm,matched=len(common),only_before=len(a.keys()-b.keys()),only_after=len(b.keys()-a.keys()))
    result['changed_job_text']=sum(a[k]['text_digest'] != b[k]['text_digest'] for k in common)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    text=['# 90-day calibration comparison','',f'Before: `{before}`. After: `{after}`.',
          f'Matched {len(common):,} source identities; before-only {result["only_before"]}, after-only {result["only_after"]}.',
          f'Title/description changed for {result["changed_job_text"]} matched jobs.',
          f'Grading versions: `{am["grading_versions"]}` → `{bm["grading_versions"]}`. Taxonomy: `{bm["taxonomy_versions"]}`.',
          'The original CSV and configuration snapshot are preserved. Examples compare matched postings; aggregate tables describe each entire export.',
          '', '## Overall results','', '| Metric | Before | After |','|---|---:|---:|']
    for key in ('jobs','average_fit','average_learning','nonzero_learning','unavailable_learning','market_unavailable_count','ai_review_pct'):
        text.append(f'| {key} | {am[key]} | {bm[key]} |')
    for field in ('role_lane','apply_decision','fit_quality'):
        text.extend(['',f'## {field} counts','','| Outcome | Before | After |','|---|---:|---:|'])
        for k in sorted(am[field].keys() | bm[field].keys()):
            text.append(f'| {k} | {am[field].get(k,0)} | {bm[field].get(k,0)} |')
    text.extend(['','## Decisions within each lane','','| Lane | Decision | Before count (%) | After count (%) |','|---|---|---:|---:|'])
    for lane in sorted(am['by_lane'].keys() | bm['by_lane'].keys()):
        x,y=am['by_lane'].get(lane,{}),bm['by_lane'].get(lane,{})
        for d in ('apply_now','manual_review','skip'):
            text.append(f'| {lane} | {d} | {x.get("decisions",{}).get(d,0)} ({x.get("decision_pct",{}).get(d,0)}%) | {y.get("decisions",{}).get(d,0)} ({y.get("decision_pct",{}).get(d,0)}%) |')
        text.extend([f'| {lane} | fit quality | {x.get("fit_quality",{})} | {y.get("fit_quality",{})} |'])
    def safe(value): return str(value).replace('|','/').replace('\n',' ')
    def examples(title, keys, limit=20):
        text.extend(['',f'## {title}','','Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.',
                     '', '| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |',
                     '|---|---|---|---:|---:|---|'])
        seen=set(); selected=[]
        for k in keys:
            x,y=a[k],b[k]
            if y['title'] in seen: continue
            seen.add(y['title']); selected.append(k)
            evidence=y['blockers']+y['rules'][-5:]
            text.append(f'| {safe(y["title"])} ({safe(y["id"])}) | {x["role_lane"]} → {y["role_lane"]} | {x["apply_decision"]} → {y["apply_decision"]} | {x["fit"]} → {y["fit"]} | {y["learning"]} | {safe(", ".join(evidence))} |')
            if len(selected)>=limit: break
        if not selected: text.append('| No matching examples | | | | | |')
        return selected
    delta=lambda k:abs(b[k]['fit']-a[k]['fit'])
    lanes=sorted((k for k in common if a[k]['role_lane']!=b[k]['role_lane']),key=lambda k:(-delta(k),k))
    decision_rank={'skip':0,'manual_review':1,'apply_now':2}
    decisions=sorted((k for k in common if a[k]['apply_decision']!=b[k]['apply_decision']),
        key=lambda k:(-abs(decision_rank[a[k]['apply_decision']]-decision_rank[b[k]['apply_decision']]),-delta(k),k))
    examples('20 biggest classification changes (absolute fit change)',lanes)
    examples('20 biggest apply-decision changes (decision distance, then fit change)',decisions)
    examples('High fit retained while decision changed',[k for k in decisions if min(a[k]['fit'],b[k]['fit'])>=80])
    growth=examples('Learning becomes meaningful',sorted((k for k in common if (b[k]['learning'] or 0)>0),key=lambda k:-(b[k]['learning'] or 0)),10)
    for k in growth[:5]:
        text.extend(['',f'**{safe(b[k]["title"])}**: '+safe(json.dumps(b[k]['growth']))])
    corrected=examples('QA/test/infrastructure/support corrections',[k for k in lanes if any(t in b[k]['title'].lower() for t in ('qa','test','infrastructure','support analyst'))])
    modern=examples('Modern data roles released from platform penalties',sorted((k for k in common if a[k]['platform'] and not b[k]['platform'] and b[k]['role_lane']=='target_lane'),key=lambda k:-delta(k)),10)
    risk=examples('Ecosystem ownership gates',sorted((k for k in common if 'ecosystem_ownership_gap' in b[k]['blockers']),key=lambda k:-delta(k)),10)
    text.extend(['','## Representative responsibility excerpts','',
        'These excerpts come from the stored descriptions. Inspect the complete description and grade_json in the CSV before acting; title alone is not the policy input.'])
    for k in list(dict.fromkeys(corrected[:3]+modern[:3]+risk[:3])):
        text.extend(['',f'### {safe(b[k]["title"])} ({b[k]["id"]})','',safe(b[k]['description'])])
    text.extend(['','## Interpretation and limits','',
        'Before learning values were zero despite a QueryCanceled market failure. They are not evidence of low learning value. After values use the existing broad extraction scope, not only the 90-day grading cohort. Percentages for different skills overlap.',
        f'After market metadata: `{json.dumps(next(iter(b.values()))["market"])}`.',
        'Fit quality describes the numerical fit band. Apply decisions separately respect explicit blockers and review flags. The old alignment score is retained for historical diagnostics and does not decide applications.',
        'Search lane and review priority are optional because clean_jobs does not currently carry them. Missing context is recorded; it does not manufacture survival/bridge origin.',
        'SQL Server and PostgreSQL proficiency must be confirmed independently of broad SQL capability. The configuration snapshot records the exact assumptions used for this run.',
        'Counts are diagnostics, not optimization targets. QA identity, platform responsibility, ecosystem dependence, seniority wording and adjacent gaps should be reviewed through representative evidence.'])
    output.write_text('\n'.join(text)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--before',type=Path,default=Path('data/outputs/results-db-90-days.csv'))
    parser.add_argument('--after',type=Path,default=Path('data/outputs/results-db-90-days-calibrated.csv'))
    parser.add_argument('--out',type=Path,default=Path('docs/calibration-comparison.md'))
    args=parser.parse_args()
    report(args.before,args.after,args.out)
