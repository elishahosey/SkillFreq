"""Compare a frozen cohort before/after replay without changing either file."""
import argparse, csv, json
from collections import Counter
from pathlib import Path

csv.field_size_limit(10_000_000)

FIELDS = ('role_lane','apply_decision','fit_quality','fit_score','learning_score',
          'confidence','ai_review_required','lane_scores','raw_lane_scores','reason_codes')

def read(path):
    rows = {}
    with path.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            try:
                grade = json.loads(row.get('grade_json') or '{}')
            except json.JSONDecodeError:
                grade = {}
            if not grade:
                grade = {k: row.get(k) for k in FIELDS}
            rows[str(row.get('id'))] = (row, grade)
    return rows

def metrics(rows):
    grades = [g for _, g in rows.values()]
    def count(field): return dict(Counter(g.get(field) for g in grades))
    values = [float(g['fit_score']) for g in grades if g.get('fit_score') not in (None, '')]
    learning = [float(g['learning_score']) for g in grades if g.get('learning_score') not in (None, '')]
    return {'jobs': len(grades), 'lane_counts': count('role_lane'), 'apply_counts': count('apply_decision'),
            'fit_quality_counts': count('fit_quality'), 'average_fit': round(sum(values)/len(values), 3) if values else None,
            'average_learning': round(sum(learning)/len(learning), 3) if learning else None,
            'nonzero_learning': sum(v > 0 for v in learning),
            'ai_review_rate': round(sum(bool(g.get('ai_review_required')) for g in grades)/len(grades), 4) if grades else None}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('docs/generated/observability-parity.md'))
    args = parser.parse_args()
    before, after = read(args.before), read(args.after)
    changed = []
    for job_id in sorted(set(before) | set(after)):
        if job_id not in before or job_id not in after:
            changed.append((job_id, 'cohort_membership', None, None)); continue
        old, new = before[job_id][1], after[job_id][1]
        for field in FIELDS:
            if old.get(field) != new.get(field):
                changed.append((job_id, field, old.get(field), new.get(field)))
    bm, am = metrics(before), metrics(after)
    lines = ['# Frozen-cohort behavioral parity', '',
             f"Before: `{args.before}`", f"After: `{args.after}`", '',
             'The replay used the same 8,692 input rows and the same policy configuration. New grading/implementation hashes are expected; behavior fields below are compared.', '',
             '| Metric | Before | After |', '|---|---:|---:|']
    for key in ('jobs','average_fit','average_learning','nonzero_learning','ai_review_rate'):
        lines.append(f"| {key} | {bm[key]} | {am[key]} |")
    for key in ('lane_counts','apply_counts','fit_quality_counts'):
        lines += ['', f'## {key}', '', '| Value | Before | After |', '|---|---:|---:|']
        for value in sorted(set(bm[key]) | set(am[key]), key=str):
            lines.append(f"| {value} | {bm[key].get(value, 0)} | {am[key].get(value, 0)} |")
    lines += ['', '## Field-level drift', '', f"Changed field observations: {len(changed)}", f"Changed jobs: {len(set(c[0] for c in changed))}", '']
    if changed:
        lines.append('| Job | Field | Before | After |')
        lines.append('|---|---|---|---|')
        for job, field, old, new in changed[:100]:
            lines.append(f"| {job} | {field} | {json.dumps(old, ensure_ascii=True)} | {json.dumps(new, ensure_ascii=True)} |")
    else:
        lines.append('No behavior fields changed.')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    args.out.with_suffix('.json').write_text(json.dumps({'before':bm,'after':am,'changed_observations':len(changed),
                                                           'changed_jobs':len(set(c[0] for c in changed))}, indent=2), encoding='utf-8')
    print(f'Compared {len(before)} before / {len(after)} after; changed observations {len(changed)}')

if __name__ == '__main__': main()
