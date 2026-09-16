"""Replay saved DB inputs through the existing pipeline, preserving exact cohort membership."""
import argparse
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.pipeline import build_job_result, finish_grading, grading_market
from skillfreq.score.grading import GradingContext


def replay(source, output, frozen_market=False):
    if source.resolve() == output.resolve():
        raise ValueError('Use a separate output; preserve the baseline')
    csv.field_size_limit(10_000_000)
    context = GradingContext.load()
    prevalence, market = (None, None) if frozen_market else grading_market(context)
    if prevalence is None and not frozen_market:
        raise RuntimeError('Comparison requires available market data; see the prevalence diagnostic')
    results = []
    with source.open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            if frozen_market:
                previous = json.loads(row['grade_json'])
                market = previous['market_context']
                if previous['learning_status'] == 'unavailable':
                    raise ValueError('Frozen baseline has unavailable prevalence')
                prevalence = {k:v for k,v in market['prevalence_pct'].items() if v is not None}
            job = {k:row[k] for k in ('id','source','source_site','title','description',
                    'search_lane','search_term_used','review_priority')}
            results.append(build_job_result(job, context, prevalence, market))
            if len(results) % 500 == 0:
                print(f'Graded {len(results)} frozen-cohort jobs', flush=True)
    finish_grading(output, results, context)
    print(f'Wrote {len(results)} jobs, grading version {context.grading_version}: {output}', flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path('data/outputs/results-db-90-days-domain.csv'))
    parser.add_argument('--out', type=Path, default=Path('data/outputs/results-db-90-days-ecosystem.csv'))
    parser.add_argument('--frozen-market', action='store_true', help='Reuse saved per-job prevalence for an isolated semantic comparison')
    args = parser.parse_args()
    replay(args.input,args.out,args.frozen_market)
