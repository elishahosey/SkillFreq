"""Compare a re-evaluated cohort to retained grades and human labels, without relabeling."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.calibration_review import identity, load_reviews


def selected_rows(path, keys, exact=False):
    csv.field_size_limit(10_000_000)
    result = {}
    with path.open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            key = identity(row)
            if key not in keys:
                if exact:
                    raise ValueError(f'Unexpected identity in re-evaluated cohort: {key}')
                continue
            if key in result:
                raise ValueError(f'Duplicate source identity: {key}')
            result[key] = row
    if result.keys() != keys:
        raise ValueError('Export is missing reviewed identities')
    return result


def compare(before, after, reviews_path, output, historical=None):
    if output.exists() or output.with_suffix('.json').exists():
        raise FileExistsError('Use a fresh report basename')
    reviews = load_reviews(reviews_path)
    keys = reviews.keys()
    a, b = selected_rows(before, keys), selected_rows(after, keys, exact=True)
    historic = selected_rows(historical, keys) if historical else None
    details = []
    for key, review in reviews.items():
        for field in ('title', 'description', 'source', 'search_lane', 'search_term_used', 'review_priority'):
            if a[key].get(field) != b[key].get(field):
                raise ValueError(f'Changed source input {key}: {field}')
        old, new = (json.loads(rows[key]['grade_json']) for rows in (a, b))
        if review['new_grading_version'] != old['grading_version']:
            raise ValueError('Review does not describe the supplied baseline version')
        if old['market_context'] != new['market_context']:
            raise ValueError('Frozen market context drift')
        fields = ('role_lane', 'apply_decision', 'fit_score', 'fit_quality', 'learning_score',
                  'missing_required_skills', 'missing_preferred_skills', 'seniority_signals',
                  'blocking_reasons', 'review_flags')
        row = dict(source_site=key[0], job_id=key[1], title=a[key]['title'],
                   human={f:review.get(f) for f in ('review_rating', 'score_quality',
                          'requirement_interpretation', 'decision_quality', 'review_note', 'issue_tags')},
                   before={f:old[f] for f in fields}, after={f:new[f] for f in fields},
                   delta=round(new['fit_score']-old['fit_score'], 2),
                   changed_fields=[f for f in fields if old[f] != new[f]],
                   new_fit_ledger=[e for e in new['triggered_rules'] if e['kind'] == 'fit'],
                   new_requirement_evidence=new['requirement_flags'],
                   new_lane_resolution=new['lane_resolution'])
        if historic:
            h = json.loads(historic[key]['grade_json'])
            row['historical'] = {f:h[f] for f in fields}
            row['historical_grading_version'] = h['grading_version']
            gaps = old['missing_required_skills']
            if h['missing_required_skills']['atomic_skills'] and not gaps['atomic_skills']:
                row['atomic_disappearance_audit'] = dict(
                    historical_atomics=h['missing_required_skills']['atomic_skills'],
                    baseline_groups=gaps['requirement_groups'],
                    baseline_unsatisfied_groups=gaps['unsatisfied_groups'],
                    baseline_penalties=[e for e in old['triggered_rules'] if e['rule_id'] == 'fit_unsatisfied_required_group'])
        details.append(row)
    def metrics(rows):
        return {field: dict(Counter(json.loads(r['grade_json'])[field] for r in rows.values()))
                for field in ('apply_decision', 'role_lane', 'fit_quality', 'grading_version', 'taxonomy_version')}
    summary = dict(jobs=len(details), before=metrics(a), after=metrics(b),
                   historical=metrics(historic) if historic else None,
                   decisions=dict(Counter(d['before']['apply_decision']+' -> '+d['after']['apply_decision'] for d in details)),
                   human_labels={f:dict(Counter(r.get(f) or 'unanswered' for r in reviews.values()))
                                 for f in ('review_rating', 'score_quality', 'requirement_interpretation')},
                   too_high_score_movement=dict(Counter('lower' if d['delta'] < 0 else 'higher' if d['delta'] > 0 else 'unchanged'
                                                       for d in details if d['human']['score_quality'] == 'too_high')),
                   bad_decisions_before=dict(Counter(d['before']['apply_decision'] for d in details if d['human']['review_rating'] == 3)),
                   bad_decisions_after=dict(Counter(d['after']['apply_decision'] for d in details if d['human']['review_rating'] == 3)),
                   good_decision_changes=[d['job_id'] for d in details if d['human']['review_rating'] == 1 and d['before']['apply_decision'] != d['after']['apply_decision']],
                   good_lane_changes=[d['job_id'] for d in details if d['human']['review_rating'] == 1 and d['before']['role_lane'] != d['after']['role_lane']],
                   atomic_disappearance_cases=sum('atomic_disappearance_audit' in d for d in details),
                   learning_changes=sum(d['before']['learning_score'] != d['after']['learning_score'] for d in details))
    payload = dict(sources=dict(before=str(before), after=str(after), reviews=str(reviews_path), historical=str(historical)),
                   interpretation='Human labels remain historical; lower scores and more skips do not establish correctness. New score-quality and requirement-interpretation counts require human re-review.',
                   summary=summary, jobs=details)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Reviewed 85-job calibration comparison', '', payload['interpretation'], '',
             f'Before: `{before}`. After: `{after}`. Reviews: `{reviews_path}`.', '',
             'Exact reviewed membership and exported input fields checked; frozen market context checked.',
             'This is a re-evaluation of retained exports, not a proven lossless original-input replay.', '',
             '```json', json.dumps(summary, indent=2), '```', '',
             '| Job | Human rating | Lane before → after | Decision before → after | Fit before → after |',
             '|---|---|---|---|---|']
    for d in details:
        old, new = d['before'], d['after']
        lines.append(f"| {d['title'].replace('|', '/')} ({d['job_id']}) | {d['human']['review_rating']} | "
                     f"{old['role_lane']} → {new['role_lane']} | {old['apply_decision']} → {new['apply_decision']} | "
                     f"{old['fit_score']} → {new['fit_score']} |")
    output.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ('before', 'after', 'reviews', 'out'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--historical', type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(args.before, args.after, args.reviews, args.out, args.historical), indent=2))
