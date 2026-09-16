"""Compare the preserved baseline commit with current deterministic grading.

No legacy classifier is shipped in the application. This developer-only report
loads trusted repository source from Git and executes its pure grading functions.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from skillfreq.score.grading import GradingContext, grade_job

BASELINE = '766f50c'


def baseline():
    def source(path):
        return subprocess.check_output(['git','show',f'{BASELINE}:{path}'],cwd=ROOT,text=True,encoding='utf-8')
    skills = yaml.safe_load(source('configs/skills.yml'))
    profile = yaml.safe_load(source('configs/profile.yml'))['skills']
    weights = yaml.safe_load(source('configs/weights.yml'))
    namespace = {'__name__': 'baseline_grading'}
    for path in ['skillfreq/skills/match.py','skillfreq/skills/extract.py',
                 'skillfreq/score/similarity.py','skillfreq/score/lane_classifier.py',
                 'skillfreq/score/decision_layer.py']:
        text = source(path).replace('import spacy', '').replace('nlp = spacy.load("en_core_web_sm")', 'nlp = None')
        text = text.replace('from .lane_classifier import classify_role_lane', '')
        exec(compile(text, f'{BASELINE}:{path}', 'exec'), namespace)
    def evaluate(job):
        desc = job.get('description') or ''
        counts = namespace['match_skills'](desc, skills)
        flags = namespace['extract_requirement_flags'](desc, skills, profile)
        score, matched, total, missing = namespace['weighted_alignment_score'](counts, profile, weights['weights'],weights['penalties'],desc,flags)
        payload = dict(job, score=score,matched=matched,required_total=total,reason_codes=';'.join(flags['reason_codes']))
        return dict(lane=namespace['classify_role_lane'](job),alignment=round(score,2),
                    fit_quality=namespace['derive_fit_quality'](payload),apply_decision=namespace['decide_apply_bucket'](payload))
    return evaluate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=Path)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--out', type=Path, default=ROOT/'docs/grading-comparison.md')
    args = parser.parse_args()
    old, context = baseline(), GradingContext.load()
    jobs = yaml.safe_load((ROOT/'tests/fixtures/lane_jobs.yml').read_text())
    if args.csv:
        import pandas as pd
        jobs = pd.read_csv(args.csv).fillna('').to_dict('records')
    if args.limit:
        jobs = jobs[:args.limit]
    lines = [f'# Grading comparison against {BASELINE}', '',
             'Learning uses illustrative prevalence (Airflow 27%, AWS 30%, Snowflake/Spark 20%). These are test inputs, not measured market statistics.', '',
             '| Job | Old lane | New lane | Old alignment | New alignment | Fit | Learning | Confidence | AI review | Old apply | New apply |',
             '|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
    examples = {}
    for job in jobs:
        previous = old(job)
        grade = grade_job(job, context, prevalence={'Airflow':27,'AWS':30,'Snowflake':20,'Spark':20})
        name = str(job.get('name') or job.get('title')).replace('|','/')
        lines.append(f"| {name} | {previous['lane']} | {grade.role_lane} | {previous['alignment']} | {grade.alignment_score:.2f} | {grade.fit_score} | {grade.learning_score} | {grade.confidence} | {grade.ai_review_required} | {previous['apply_decision']} | {grade.apply_decision} |")
        if job.get('name') in ['obvious_target','frontend','data_backend','ambiguous','learning_opportunity']:
            examples[job['name']] = grade.to_dict()
    lines += ['', 'The raw alignment score retains its historic scale. Fit and learning are distinct 0–100 heuristics. Confidence is not a calibrated probability.',
              '', f'Grading version: `{context.grading_version}`. Atomic taxonomy version: `{context.taxonomy_version}`.']
    args.out.parent.mkdir(exist_ok=True,parents=True)
    args.out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if examples:
        args.out.with_name('grading-examples.yml').write_text(yaml.safe_dump(examples,sort_keys=False),encoding='utf-8')
    print(f'Compared {len(jobs)} jobs: {args.out}')


if __name__ == '__main__':
    main()
