# SkillFreq command reference

Copy the command for the action you need. Run SkillFreq commands from the repository
root in PowerShell. Replace example input paths with your files. For the order of
operations and how to interpret results, use the [workflow guide](workflow.md).

## Find a command

| I want to… | Command / section |
|---|---|
| Install or activate SkillFreq | [Setup](#setup) |
| Grade stored jobs from the last 90 days | [`grade-db` / VS Code task](#grade-jobs-from-postgresql) |
| Grade a specific job CSV | [`grade-csv`](#grade-a-csv) |
| Scrape one job with the sibling JobSpy project | [JobSpy helpers](#jobspy-helpers) |
| Grade jobs from URLs | [`fetch` and `run`](#fetch-links-and-grade-job-pages) |
| Import jobs into PostgreSQL | [`excel-load`](#load-data-into-postgresql) |
| Refresh market skills and prevalence | [`refresh-job-skills`](#refresh-market-prevalence) |
| Save source jobs, grades and review results as a batch | [`import-batch`](#import-a-review-batch) |
| Choose a resume variant or inspect resume signals | [`route` and `extract`](#resume-commands) |
| Count recurring job titles | [`titles`](#count-job-titles) |
| Check the implementation | [Tests and comparisons](#tests-and-comparisons) |
| Inspect policy dependencies | [`policy-report` and `policy-impact`](#policy-observability) |
| Explain one graded job | [`trace-job`](#policy-observability) |
| Try the container | [Docker](#docker) |

## Setup

Create an environment once:

```powershell
python -m venv .venv-skillfreq
.\.venv-skillfreq\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Activate it in a later session:

```powershell
.\.venv-skillfreq\Scripts\Activate.ps1
```

Install the browser used for URL scraping when needed:

```powershell
python -m playwright install chromium
```

Show available commands or the options for one command:

```powershell
python -m skillfreq.cli --help
python -m skillfreq.cli grade-csv --help
```

## Grade jobs from PostgreSQL

For the calibrated comparison export, choose **Grade DB Jobs - Calibrated 90 Days**.
It writes `data/outputs/results-db-90-days-calibrated.csv` and its snapshot.
See [career policy](career-policy.md) to change thresholds and rules without Python edits.

In VS Code, open **Terminal → Run Task → Grade DB Jobs - Last 90 Days**.
This task uses the SkillFreq virtual environment and your existing `.env` database
connection. It reads stored titles and descriptions directly from `public.clean_jobs`
and runs the deterministic grading flow, including available market prevalence.

Results go to `data/outputs/results-db-90-days.csv`, with the configuration snapshot
in `data/outputs/results-db-90-days.grading.yml`. Each run replaces these two DB
exports; the existing `results.csv` and CSV/scraping tasks remain available.

Equivalent command after activating the environment:

```powershell
python -m skillfreq.cli grade-db --since-days 90 --out data/outputs/results-db-90-days.csv
```

For a smaller test, add `--limit 10` to select the ten newest matching postings.
The cutoff uses `date_posted >= CURRENT_DATE - 90` in PostgreSQL, not import date.
Missing posting dates are excluded. An empty window produces a header-only CSV
and a clear terminal message. The existing view provides deduplicated jobs.

This task reads PostgreSQL; add `--persist-grades` explicitly to append grading
history. It does not scrape or require an input CSV. `--offline-grading` skips only
market data; the job source still requires PostgreSQL. Unavailable market data is
reported and learning scores are null/unavailable. Refresh prevalence separately
with [`refresh-job-skills`](#refresh-market-prevalence) when needed.

For the focused integration/ecosystem/database calibration, keep the previous
calibrated export and write a separate result:

```powershell
python -m skillfreq.cli grade-db --since-days 90 --out data/outputs/results-db-90-days-domain.csv
python scripts/compare_domain_calibration.py
```

The comparison requires identical job identities and descriptions. A later rolling
90-day window may change membership; it fails clearly rather than attributing
cohort changes to policy. See the [domain comparison](domain-calibration-comparison.md).

## Grade a CSV

**Offline fit grading:** no PostgreSQL connection or AI call is needed.

```powershell
python -m skillfreq.cli grade-csv --input data/inputs/jobs.csv --out data/outputs/results.csv --offline-grading
```

**Include market data:** reads the existing PostgreSQL prevalence view.

```powershell
python -m skillfreq.cli grade-csv --input data/inputs/jobs.csv --out data/outputs/results.csv
```

**Include market data and append grading history:**

```powershell
python -m skillfreq.cli grade-csv --input data/inputs/jobs.csv --out data/outputs/results.csv --persist-grades
```

**Use another profile:**

```powershell
python -m skillfreq.cli grade-csv --input data/inputs/jobs.csv --out data/outputs/results.csv --profile configs/profile.yml --offline-grading
```

The CSV needs job descriptions and preferably titles and source identity. Keep
`results.grading.yml` beside `results.csv`. Offline learning has no market
contribution. `--persist-grades` needs the existing base `skill_scores` table and
applies the grading migration; it does not import jobs or refresh prevalence.
Choose it or batch import as the persistence route for a run to avoid duplicate history.

## JobSpy helpers

These commands belong to the existing **sibling JobSpy repository** and use its
Python environment. The example scrapes one test job:

```powershell
Push-Location ..\JobSpy
python scrape_one_job.py --term "data engineer" --location "Texas"
.\move_to_import.ps1
Pop-Location
```

The move command above previews the matching dated CSVs. To perform those moves:

```powershell
Push-Location ..\JobSpy
.\move_to_import.ps1 -Execute
Pop-Location
```

Use your usual JobSpy scraper for a full search batch. The move helper can move
multiple dated CSVs, not just the latest test file.

## Fetch links and grade job pages

Extract usable URLs from a JobSpy CSV:

```powershell
New-Item -ItemType Directory -Force data/inputs | Out-Null
python -m skillfreq.cli fetch --input data/inputs/jobs.csv --output data/inputs/links.txt
```

Scrape and grade a file containing one URL per line:

```powershell
python -m skillfreq.cli run --input data/inputs/links.txt --out data/outputs/results.csv --offline-grading
```

Omit `--offline-grading` to use market data. Add `--persist-grades` to save history.
Fetch/grading failures are written beside the output as `failures.csv`.

Optional noun-phrase diagnostics:

```powershell
python -m skillfreq.cli run --input data/inputs/links.txt --out data/outputs/results.csv --offline-grading --nlp-diagnostics
```

Diagnostics need the spaCy model and write `extracted_skills_*.txt`; they do not
change the controlled taxonomy.

Legacy date-based CSV mode:

```powershell
$env:JOBSPY_DATA_PATH = "..\JobSpy"
python -m skillfreq.cli run --input data/inputs/links.txt --out data/outputs/results.csv --no-scrape --offline-grading
```

In this mode, `run` reads today's raw `jobs-M-D-YY.csv` from `JOBSPY_DATA_PATH`.
`--input` does not select that CSV. Prefer `grade-csv` for a specific file.
`run` also accepts `--skills`, `--weights` and `--profile`. Its legacy
`--min-score` filter uses raw alignment for CSV mode; it is not a 0–100 fit cutoff.

## Load data into PostgreSQL

Connection settings come from `.env`: `DATABASE_URL`, or `DB_NAME`, `DB_USER`,
`DB_PASSWORD`, `DB_HOST` and optional `DB_PORT`.

Import a JobSpy intake folder, including source filenames:

```powershell
python -m skillfreq.cli excel-load --table staging.jobs --mode append
```

The folder form defaults to `.\import`, which is the intake folder populated by
the JobSpy move helper. An explicit `--folder` can still be used for another intake
location.

Every CSV in that folder and its subfolders is loaded. Move processed inputs
outside the intake tree before another append run.

Load a single CSV or spreadsheet into a chosen table:

```powershell
python -m skillfreq.cli excel-load --excel data/inputs/jobs.csv --table staging.job_upload --mode append
python -m skillfreq.cli excel-load --excel data/inputs/jobs.xlsx --sheet Sheet1 --table staging.job_upload --mode append
```

Upsert using a conflict key:

```powershell
python -m skillfreq.cli excel-load --excel data/inputs/jobs.xlsx --table staging.job_upload --mode upsert --primary-key job_url
```

`--mode replace` replaces the destination table's contents. `--schema` defaults to
`public` when the table name omits a schema. Add `--log-file logging/jobs-import.log`
to choose the import log. For the market pipeline, use the folder intake into
`staging.jobs` and the existing `clean_jobs` view described in the workflow guide.

## Refresh market prevalence

Refresh across all current clean jobs:

```powershell
python -m skillfreq.cli refresh-job-skills
```

Choose a recent population or a smaller development scope:

```powershell
python -m skillfreq.cli refresh-job-skills --since-days 90
python -m skillfreq.cli refresh-job-skills --since-days 90 --limit 1000
```

Each successful refresh replaces the current extraction scope. The existing
`public.clean_jobs` view must be available. Defaults are
`--taxonomy configs/market_skills.yml` and `--schema-sql db/job_skills.sql`.

Adjust the import/refresh timeouts by placing global flags **before** the command:

```powershell
python -m skillfreq.cli --db-connect-timeout 10 --db-statement-timeout 180 --db-lock-timeout 10 refresh-job-skills
```

The grading market/history helpers currently use their own bounded waits.

## Import a review batch

Import original jobs and scored results:

```powershell
python -m skillfreq.cli import-batch --batch-id 2026-09-12 --jobs-csv data/inputs/jobs.csv --scores-csv data/outputs/results.csv
```

Include an existing review workbook:

```powershell
python -m skillfreq.cli import-batch --batch-id 2026-09-12 --jobs-csv data/inputs/jobs.csv --scores-csv data/outputs/results.csv --review-xlsx data/analyze/review.xlsx --review-sheet Base
```

These are alternative examples; running both appends twice. Keep the grading YAML
snapshot beside new-format results. The importer writes `raw_jobs` and
`skill_scores`, plus calibration records when a workbook is supplied. It does not
populate the separate `staging.jobs` market intake or call AI.

| Option | Purpose |
|---|---|
| `--batch-mode append` | Default; add batch records |
| `--batch-mode replace` | Clear and reload the selected batch |
| `--scoring-version`, `--rules-version`, `--cleaning-version` | Legacy scoring/calibration metadata; new grade rows preserve their exported grading version |
| `--run-name`, `--run-notes` | Review-run metadata |
| `--log-file` | Custom import log path |

## Resume commands

Recommend existing resume variants for graded jobs:

```powershell
$env:NOTION_TRACKER_PATH = (Get-Location).Path
python -m skillfreq.cli route --input data/outputs/results.csv --out data/outputs/routed-results.csv --title-col title --jd-col description
```

The router requires that input base directory. `--roles` defaults to
`configs/roles.yml`. It writes CSV recommendations; it does not send them to Notion.

Print evidence from a PDF or DOCX resume:

```powershell
python -m skillfreq.cli extract --file data/inputs/resume.pdf
```

This prints signals rather than automatically changing `profile.yml`.

The legacy `suggest --jds <folder>` command also exists, but its current reader
assumes the old flat skills dictionary. Use `grade-csv` for current grading.
Its advertised `--out` option is not wired to a CSV export.

## Count job titles

```powershell
python -m skillfreq.cli titles data/outputs/results.csv --title-col title
```

`count-titles` is an alias for `titles`. Counts are printed to the console.

## Tests and comparisons

```powershell
python -m unittest discover -s tests -v
python scripts/compare_grading.py
```

The comparison writes the fixture report and examples under `docs` using the
trusted baseline code in Git. Compare your own sample with a separate report:

```powershell
python scripts/compare_grading.py --csv data/inputs/jobs.csv --limit 100 --out data/outputs/comparison.md
```

Optional PostgreSQL integration test; test database changes are rolled back:

```powershell
$env:SKILLFREQ_TEST_DB = "1"
python -m unittest discover -s tests -p test_grading_postgres.py -v
Remove-Item Env:SKILLFREQ_TEST_DB
```

## Policy observability

Generate reports from the current YAML policy without changing it:

```powershell
python -m skillfreq.cli policy-report --out docs/generated/policy-observability.md
python -m skillfreq.cli policy-impact --rule ecosystem_identity_guard
```

The report includes rule/flag dependencies, conservative static findings,
term-group overlap and the ecosystem taxonomy recommendation. The impact report
shows upstream producers and possible downstream outputs for one rule. Schema
errors still fail during normal configuration loading.

Trace one job through the real evaluator and preserve its event history:

```powershell
python -m skillfreq.cli trace-job `
  --input data/outputs/results-db-90-days-ecosystem.csv `
  --id in-1f5c8418605bc555 `
  --out docs/generated/job-trace.md
```

This writes Markdown and JSON. It records matched evidence, derived flags,
before/after actions, no-op and overridden effects, final owners, confidence and
AI-gating history. It regrades the selected row with the current policy, so use
the saved `.grading.yml` and parity report when auditing historical decisions.

Compare requirement interpretation across a frozen cohort:

```powershell
python scripts/compare_requirements.py `
  --before data/outputs/results-db-90-days-ecosystem.csv `
  --after data/outputs/results-db-90-days-requirements.csv
```

The report lists changed required/preferred gaps, source sentences and any fit,
decision or AI-review movement.

Replay the frozen 8,692-job requirement cohort, keeping saved prevalence fixed:

```powershell
python scripts/regrade_saved_cohort.py `
  --input data/outputs/results-db-90-days-requirements.csv `
  --out data/outputs/results-db-90-days-requirement-semantics.csv `
  --frozen-market
python scripts/compare_requirements.py `
  --before data/outputs/results-db-90-days-requirements.csv `
  --after data/outputs/results-db-90-days-requirement-semantics.csv `
  --out docs/generated/requirement-semantics.md
```

This replay needs no DB query and preserves the baseline. The comparison checks
row/description identity, reports atomic and group gaps, retains source evidence
for every changed job in JSON, and fails on lane or learning drift. See
[requirement semantics](requirement-semantics.md) for penalties and equivalents.

## Docker

Try offline grading with mounted local input/output folders:

```powershell
docker build -t skillfreq .
docker run --rm `
  -v "${PWD}/data:/app/data" `
  -v "${PWD}/configs:/app/configs" `
  -v "${PWD}/logging:/app/logging" `
  skillfreq grade-csv --input data/inputs/jobs.csv --out data/outputs/results.csv --offline-grading
```

The current image omits the `db` directory. Use local Python for database migrations
and persistence. See the [workflow guide](workflow.md) for prerequisites and outputs.
