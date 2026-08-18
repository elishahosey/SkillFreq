import csv, json, re
from collections import Counter
from datetime import datetime

PATH = r"C:\Users\ehose\Downloads\jobs.csv"
NULLS = {"", "NULL", "null", "None", "N/A", "NA"}

with open(PATH, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    cols = reader.fieldnames or []
    missing = Counter(); values = {c: Counter() for c in cols}
    rows = malformed = 0
    ids = set(); urls = set(); dup_id = dup_url = 0
    bad_salary = neg_salary = reversed_salary = 0
    date_min = date_max = None; bad_date = 0
    whitespace = Counter(); boolean_bad = Counter()
    for row in reader:
        rows += 1
        if None in row or len(row) != len(cols):
            malformed += 1
            continue
        for c in cols:
            v = row[c]
            if v in NULLS:
                missing[c] += 1
            else:
                if len(values[c]) < 2000 or v in values[c]: values[c][v] += 1
                if v != v.strip(): whitespace[c] += 1
        jid = row.get("id", "")
        if jid not in NULLS:
            if jid in ids: dup_id += 1
            else: ids.add(jid)
        url = row.get("job_url", "")
        if url not in NULLS:
            if url in urls: dup_url += 1
            else: urls.add(url)
        mn, mx = row.get("min_amount", ""), row.get("max_amount", "")
        try:
            mnv = None if mn in NULLS else float(mn); mxv = None if mx in NULLS else float(mx)
            if (mnv is not None and mnv < 0) or (mxv is not None and mxv < 0): neg_salary += 1
            if mnv is not None and mxv is not None and mnv > mxv: reversed_salary += 1
        except ValueError: bad_salary += 1
        ds = row.get("date_posted", "")
        if ds not in NULLS:
            try:
                d = datetime.fromisoformat(ds)
                date_min = d if date_min is None or d < date_min else date_min
                date_max = d if date_max is None or d > date_max else date_max
            except ValueError: bad_date += 1
        for c in ("is_remote", "is_contract"):
            v = row.get(c, "")
            if v not in NULLS and v.lower() not in {"true", "false", "0", "1", "t", "f"}: boolean_bad[c] += 1

result = {
    "rows": rows, "columns": len(cols), "malformed_rows": malformed,
    "duplicate_nonnull_id_rows": dup_id, "duplicate_nonnull_job_url_rows": dup_url,
    "date_min": date_min.isoformat() if date_min else None, "date_max": date_max.isoformat() if date_max else None,
    "bad_dates": bad_date, "bad_salary_values": bad_salary, "negative_salary_rows": neg_salary,
    "min_greater_than_max_rows": reversed_salary, "boolean_bad": boolean_bad,
    "whitespace_counts": whitespace,
    "columns_profile": {}
}
for c in cols:
    nonnull = rows - missing[c]
    result["columns_profile"][c] = {
        "missing": missing[c], "missing_pct": round(missing[c] * 100 / rows, 2) if rows else 0,
        "sampled_distinct_at_least": len(values[c]), "top_values": values[c].most_common(8)
    }
print(json.dumps(result, indent=2, default=dict))
