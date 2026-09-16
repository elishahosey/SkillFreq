"""Same-cohort ecosystem evidence report; no grading or prevalence calculations."""
import argparse
from collections import Counter
import json
from pathlib import Path

from compare_domain_calibration import enriched
from compare_calibration import metrics


RETAINED_REVIEWS = {
    'li-4427707701': ('SQL, REST/SOAP, XML, HL7/FHIR, data exchange and mapping.',
        'Epic Bridges, Corepoint and managed file transfer; product-specific healthcare experience is preferred, not an exclusive prerequisite.',
        'No conflicting security/hardware role identity. Lead scope remains a review consideration.',
        'TARGET remains defensible: interoperability standards and interface delivery dominate. Review healthcare familiarity.'),
    'li-4430448809': ('SQL/Python, HL7/FHIR interoperability, data exchange and troubleshooting.',
        'Several interchangeable middleware engines are accepted: Mirth, Rhapsody, Cloverleaf and Azure integration services.',
        'No conflicting domain identity. Five years of healthcare integration and UK-oriented employment context need review.',
        'TARGET remains defensible; experience is tied to healthcare integration, not one proprietary runtime.'),
    'li-4430454590': ('Explicit T-SQL/SQL Server, Python, ETL, APIs, Kafka and microservices.',
        'Any API-management tool is accepted; no enterprise-platform specialization requirement.',
        'No conflicting domain identity. The posting is onsite in Geneva.',
        'TARGET is correct for technical career direction; location is a separate application constraint.'),
    'in-07e05dd5a314ee99': ('SQL, ETL, cloud pipelines, APIs, JSON/XML/SFTP, healthcare data standards and reconciliation.',
        'Boomi Atoms/Atom Clouds, AtomSphere monitoring and connector configuration are substantial; Boomi/Epic certifications are due within six months after hire. Equivalent integration-platform experience is accepted.',
        'No conflicting domain identity. Runtime management is mixed with broad interface/data engineering.',
        'Retain TARGET with specialization review and a fit penalty. Broad transferable work counters concentration without pretending the Boomi gap is absent.'),
    'li-4430133467': ('30% ADF ETL/integration and 20% warehouse work, plus SQL procedures, schema design and APIs/SFTP.',
        '25% Salesforce data operations/Data Cloud configuration, plus Tableau and team leadership.',
        'DB administrator title and capacity planning are mixed with strong data engineering. Eight years and team leadership remain review concerns.',
        'Retain TARGET/manual review. Salesforce is significant but does not dominate the entire role; a generic DBA title is not vendor-admin identity.'),
}

TITLES = [
    'Senior Integration Boomi Engineer','Informatica Developer','Informatica Senior Developer',
    'Senior Informatica Administrator','Data Engineer (Palantir)','Workday Integration Engineer',
    'Salesforce Developer','ServiceNow Developer','MDM Engineer',
    'Informatica MDM Support & Data Operations Specialist','Senior Workday Integration Developer - Extend',
    'Salesforce Administrator','Informatica Platform Administrator','ServiceNow Integration Hub Developer',
    'Senior Boomi Integration Engineer -Remote','Data Engineer (Databricks + Informatica + Azure)',
    'Informatica IICS/PowerCenter Engineer( Snowflake & ETL)','Senior Workday Developer',
    'Salesforce Data Cloud Engineer III (Memphis TN or Remote in the USA)',
    'ServiceNow Platform Engineer','Boomi Integration Lead Engineer','Platform Engineer - Palantir',
]


def report(before, after, output):
    a,b=enriched(before),enriched(after)
    keys=sorted(a)
    if a.keys()!=b.keys() or any(a[k]['text_digest']!=b[k]['text_digest'] for k in keys):
        raise ValueError('Different cohort or changed job text; cannot attribute differences to policy')
    am,bm=metrics(list(a.values())),metrics(list(b.values()))
    pool=[k for k in keys if b[k]['signals'].get('ecosystem_title') or b[k]['signals'].get('data_platform_title')]
    transitions=Counter(b[k]['role_lane'] for k in pool if a[k]['role_lane']!=b[k]['role_lane'])
    summary=dict(before=am,after=bm,matched=len(keys),changed_job_text=0,
        changed_market_percentages=sum(a[k]['market'].get('prevalence_pct')!=b[k]['market'].get('prevalence_pct') for k in keys),
        ecosystem_titles=dict(count=len(pool),target_before=sum(a[k]['role_lane']=='target_lane' for k in pool),
            target_after=sum(b[k]['role_lane']=='target_lane' for k in pool),
            moved_to={lane:transitions[lane] for lane in ('target_lane','secondary_lane','bridge_lane','wrong_lane')}))
    lines=['# Ecosystem concentration calibration','',f'Before: `{before}`. After: `{after}`.',
        f'Exact replay of {len(keys):,} saved DB jobs; all identities and title/description hashes match.',
        'The date advanced between passes, so the frozen DB export supplies job inputs. The existing DB prevalence view is loaded once; old grades are never used as scoring inputs.',
        f'Grading: `{am["grading_versions"]}` → `{bm["grading_versions"]}`. Taxonomy: `{bm["taxonomy_versions"]}`.',
        f'Jobs with changed recorded prevalence percentages: {summary["changed_market_percentages"]}.',
        '', '## Aggregate comparison','','| Metric | Before | After |','|---|---:|---:|']
    for f in ('jobs','average_fit','average_learning','nonzero_learning','unavailable_learning','ai_review_pct'):
        lines.append(f'| {f} | {am[f]} | {bm[f]} |')
    for f in ('role_lane','apply_decision','fit_quality'):
        for value in sorted(am[f].keys()|bm[f].keys()):
            lines.append(f'| {value} | {am[f].get(value,0)} | {bm[f].get(value,0)} |')
    lines += ['', '## Ecosystem-related titles', '', f'`{json.dumps(summary["ecosystem_titles"])}`',
        'Title cohort uses configured enterprise-product or data-platform title evidence. Counts cover all audited title-cohort records; the examples below are the detailed inspection sample. Moved-to counts include any lane change, not only departures from TARGET.',
        '', '## Representative ecosystem postings', '',
        '| Title / ID | Ecosystem | Lane before → after | Fit before → after | Decision before → after | Title hits | Specialization hits | Ownership hits | Transferable hits | Main policy rules |',
        '|---|---|---|---:|---|---:|---:|---:|---:|---|']
    selected=[]
    for title in TITLES:
        candidates=[k for k in keys if b[k]['title']==title]
        if candidates: selected.append(sorted(candidates,key=lambda k:(a[k]['role_lane']==b[k]['role_lane'],-abs(a[k]['fit']-b[k]['fit']),k))[0])
    if len(selected)<20: raise ValueError('Need at least 20 available representative titles')
    summary['examples']=[]
    def safe(x): return str(x).replace('|','/').replace('\n',' ')
    for k in selected:
        x,y=a[k],b[k];s=y['signals']
        vendor=list(dict.fromkeys(s.get('ecosystem_title',[])+s.get('data_platform_title',[])))
        special=s.get('ecosystem_specialization',[])+s.get('data_platform_specialization',[])
        ownership=s.get('ecosystem_ownership',[])
        transfer=s.get('transferable_data',[])
        rules=[r for r in y['rules'] if r.startswith(('ecosystem','transferable')) or r in ('hard_exclusion_override','configured_hard_blocker','configured_review_gate','strong_primary_fit')]
        flags=y['policy_flags']
        rules += [r for r in y['fit_rules'] if r.startswith('ecosystem')]
        lines.append(f'| {safe(y["title"])} ({y["id"]}) | {safe(", ".join(vendor))} | {x["role_lane"]} → {y["role_lane"]} | {x["fit"]} → {y["fit"]} | {x["apply_decision"]} → {y["apply_decision"]} | {len(vendor)} | {len(special)} | {len(ownership)} | {len(transfer)} | {safe(", ".join(rules))} |')
        summary['examples'].append(dict(id=y['id'],title=y['title'],vendor=vendor,old_lane=x['role_lane'],new_lane=y['role_lane'],old_fit=x['fit'],new_fit=y['fit'],old_decision=x['apply_decision'],new_decision=y['apply_decision'],specialization=special,ownership=ownership,administration=s.get('ecosystem_administration',[]),transferable=transfer,policy_flags=flags,rules=rules))
    lines += ['', 'Specialization counts include separately labeled data-platform vocabulary for reporting. Foundry delivery components do not feed enterprise concentration by default.',
              '', '## Matched evidence for the inspection sample', '']
    for e in summary['examples']:
        lines += [f'### {safe(e["title"])} ({e["id"]})','',f'- Specialization: `{safe(e["specialization"])}`.',
            f'- Ownership: `{safe(e["ownership"])}`.',f'- Administration: `{safe(e["administration"])}`.',f'- Transferable data: `{safe(e["transferable"])}`.',
            f'- Concentration: `{e["policy_flags"].get("ecosystem_role_concentration")}`; strong transfer counterweight: `{e["policy_flags"].get("transferable_data_strong")}`.','']
    retained=[k for k in keys if 'integration engineer' in a[k]['title'].lower() and a[k]['role_lane']=='target_lane']
    if {b[k]['id'] for k in retained}!=set(RETAINED_REVIEWS): raise ValueError('Retained integration cohort differs from the five manually reviewed jobs')
    summary['retained_integration']=[]
    lines += ['', '## Manual review of all five retained TARGET integration jobs','']
    for k in retained:
        x,y=a[k],b[k];positive,ecosystem,conflict,judgment=RETAINED_REVIEWS[y['id']]
        lines += [f'### {safe(y["title"])} ({y["id"]})','',
            f'Lane: {x["role_lane"]} → {y["role_lane"]}; fit: {x["fit"]} → {y["fit"]}; decision: {x["apply_decision"]} → {y["apply_decision"]}.','',
            f'- Transferable evidence: {positive}',f'- Ecosystem evidence: {ecosystem}',f'- Conflicts/caveats: {conflict}',f'- Assessment: {judgment}','']
        summary['retained_integration'].append(dict(id=y['id'],title=y['title'],new_lane=y['role_lane'],assessment=judgment))
    lines += ['', '## Interpretation and remaining ambiguity','',
        'The actual Informatica Developer is an MDM Hub/360 implementation specialist (schema manager, stewardship workflows and landing/staging components), unlike the transferable SQL/ETL fixture with the same title. The actual Informatica Senior Developer mixes platform migration with PL/SQL and remains SECONDARY rather than automatically WRONG.',
        'The actual Palantir Data Engineer explicitly welcomes strong data engineers new to Foundry. Its Foundry Ontology/Code Repositories vocabulary is recorded separately and does not impose an enterprise-platform penalty. Zurich location remains a separate application constraint.',
        'The actual Senior Integration Boomi Engineer asks for hands-on Dell Boomi experience and centers delivery on it. It receives specialization review rather than an invented hard ownership blocker. Matched experience wording is evidence; this pass does not claim to parse product-specific numeric years or distinguish every preferred/required phrase.',
        'Counts are distinct matched phrases, not mention frequency, responsibility percentages, or statistically calibrated concentration. Long descriptions and boilerplate can add incidental signals. The explicit title/transfer counterweights reduce that risk; inspect mixed-platform work and ambiguous MDM terminology.',
        'Remaining vocabulary boundary: ServiceNow Integration Hub Developer describes Integration Hub spokes and Flow Designer, which are not yet in the specialization group. Inspect that posting despite its existing non-TARGET classification. Senior Boomi Integration Engineer -Remote mixes an explicit seven-year Boomi demand with equivalent-platform wording; the IICS/PowerCenter/Snowflake posting asks for eight years in multiple tools while still describing transferable data work. These require judgment about experience gates, not automatic rejection by product name.',
        'Existing fit caps, profile, canonical atomic taxonomy, market calculations, decision thresholds and domain guards remain in place. The only generic mechanism addition exports declared lane flags into the fit context and grade audit, avoiding duplicate concentration conditions across stages.',
        f'Final market context: `{json.dumps(next(iter(b.values()))["market"])}`.',
        'See [policy controls and implementation notes](ecosystem-policy.md) for thresholds, file changes, tests and how to accept a platform through configuration.']
    output.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    output.with_suffix('.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('examples','retained_integration')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--before',type=Path,default=Path('data/outputs/results-db-90-days-domain.csv'))
    parser.add_argument('--after',type=Path,default=Path('data/outputs/results-db-90-days-ecosystem.csv'))
    parser.add_argument('--out',type=Path,default=Path('docs/ecosystem-calibration-comparison.md'))
    args=parser.parse_args()
    report(args.before,args.after,args.out)
