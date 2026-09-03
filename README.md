# SkillFreq

SkillFreq is a Python CLI for turning job descriptions into market signals: recurring skills, profile alignment, missing requirements, and CSV outputs you can use to make a job search less guessy.

I originally built this for myself after getting frustrated with job boards, vague recommendations, and roles that looked relevant until the requirements told a different story. The goal is simple: collect job descriptions, extract the signals, and use the evidence to decide what to study, skip, tailor, or apply to.

Instead of guessing what to study next, SkillFreq helps surface the technologies, patterns, and skill gaps that show up most often in real roles.

> Note: SkillFreq is currently heavily personalized around my own job search, target roles, resume variants, and local workflow. Parts of it may be useful to others, but it is not a polished general-purpose product yet.

---

## Why I Built This

I got tired of manually searching through jobs and constantly running into roles that *looked* like a fit at first glance, but then hit me with things like:

- 10+ years required
- random legacy tech stacks
- platform tools I barely touch
- titles that sound right but are actually totally off-lane

Even when job boards try to recommend roles, they often miss the bigger picture.

After getting burned out by the process before, I wanted to build my own **job-search system**.

Partly out of frustration, partly out of curiosity, and honestly... partly because I was bored and wanted something useful to build.

SkillFreq currently works as a command-line workflow:

```text
Job postings or JobSpy CSVs -> SkillFreq -> scored CSVs + skill frequency outputs
```

It can:

- read job links or JobSpy-style CSV exports
- fetch and normalize job URLs
- parse job descriptions from supported platforms
- extract skills using YAML keyword buckets
- score job descriptions against a local profile and weights
- classify roles based on score and requirement flags
- count repeated job titles in a CSV
- load Excel sheets into PostgreSQL staging or target tables
- route jobs toward resume variants when role configuration is available
- export results, failures, logs, and extracted skill summaries

## Repository Layout

```text
configs/       YAML configuration for skills, weights, profile, resume signals, and roles
data/          local inputs and outputs
Jobspy/        helper scripts and expected JobSpy cleaned CSV location
logging/       timestamped run logs
skillfreq/     SkillFreq package and CLI
Dockerfile     container image definition
```

## Configuration

The main configuration files live in `configs/`:

- `skills.yml`: skill names, aliases, and keyword buckets
- `weights.yml`: scoring weights and penalties
- `profile.yml`: local skill/profile alignment settings
- `resume_signal.yml`: resume signal extraction settings
- `roles.yml`: role routing configuration

Local environment settings can live in `.env`. Do not commit machine-specific paths or secrets.

Useful environment variables:

```text
JOBSPY_DATA_PATH=/app/Jobspy
PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
```

## Local Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv-skillfreq
.\.venv-skillfreq\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Show the CLI help:

```powershell
python -m skillfreq.cli --help
```

All commands show timestamped lifecycle and phase diagnostics by default:

```powershell
python -m skillfreq.cli refresh-job-skills
```

By default this processes every row in `public.clean_jobs`. For a recent window
or a faster development run, scope the refresh explicitly:

```powershell
# Jobs posted during the last 90 days
python -m skillfreq.cli refresh-job-skills --since-days 90

# The 1,000 newest jobs in that window
python -m skillfreq.cli refresh-job-skills --since-days 90 --limit 1000
```

The selected jobs are persisted in `public.job_skill_scope`. Prevalence uses
that same scope as its denominator, so jobs skipped by `--since-days` or
`--limit` are not incorrectly counted as jobs with no skill mentions. A later
refresh replaces the previous scope.

Database-backed commands also use bounded connection, statement, and lock waits.
Override their defaults when troubleshooting:

```powershell
python -m skillfreq.cli `
  --db-connect-timeout 10 `
  --db-statement-timeout 120 `
  --db-lock-timeout 10 `
  refresh-job-skills
```

## CLI Commands

Fetch usable links from a JobSpy-style CSV:

```powershell
python -m skillfreq.cli fetch --input Jobspy/jobs.csv --output data/inputs/links.txt
```

Run SkillFreq against links or JobSpy data:

```powershell
python -m skillfreq.cli run --input data/inputs/links.txt --out data/outputs/results.csv
```

By default, `run` treats each line in the input file as a URL and tries to scrape the job description. To skip URL scraping and read descriptions from the cleaned JobSpy CSV path instead, pass:

```powershell
python -m skillfreq.cli run --input data/inputs/links.txt --out data/outputs/results.csv --no-scrape
```

The `--no-scrape` path reads a cleaned JobSpy CSV from `JOBSPY_DATA_PATH` or `../JobSpy`.

### JobSpy to PostgreSQL intake workflow

For a quick end-to-end test, scrape exactly one real job and move the dated CSV into the JobSpy intake folder:

```powershell
cd C:\Users\ehose\Development\JobSpy
python scrape_one_job.py
.\move_to_import.ps1 -Execute
```

Then load the CSV files from that intake folder into PostgreSQL:

```powershell
cd C:\Users\ehose\Development\SkillFreq
python -m skillfreq.cli excel-load `
  --folder ..\JobSpy\import `
  --table staging.jobs `
  --mode append `
  --log-file logging/excel_to_db_log/jobs_folder_load.log
```

The database connection is read from SkillFreq's `.env`. Because `--mode append` processes every CSV in the folder, archive or remove successfully imported files before the next run to avoid loading them again.

Count job titles in a CSV:

```powershell
python -m skillfreq.cli titles data/outputs/results.csv --title-col title
```

### Job-skill prevalence

Build the normalized `public.job_skills` table from `public.clean_jobs` and create
the baseline `public.skill_prevalence` view:

```powershell
python -m skillfreq.cli refresh-job-skills
```

`configs/market_skills.yml` is the reporting taxonomy. Its keys are canonical
dashboard labels and its values are spelling/product aliases. Keep related but
distinct tools separate so, for example, a PySpark mention does not automatically
count as a Python mention. The refresh is atomic: a failure leaves the previous
successful result intact.

Query the all-jobs baseline:

```sql
SELECT canonical_skill, jobs_mentioning_skill, total_jobs, prevalence_pct
FROM public.skill_prevalence;
```

#### Interpretation and intended scope

The primary SkillFreq metric is broad-spectrum prevalence across the current
job scope. This is intentional: the collected jobs represent a realistic range
of adjacent roles rather than one narrowly targeted title. The baseline helps
identify portable skills that preserve options across data engineering,
analytics, backend/integration, cloud, and platform work.

A practical way to read the ranking is:

```text
broad core       = SQL + Python + a major cloud
platform support = Docker + Kubernetes + Terraform
selective depth  = Snowflake / Spark / Databricks / Airflow / dbt
```

Future role-family prevalence should be treated as a comparison layer, not as a
replacement for the broad baseline. It can explain where specialized tools are
concentrated without limiting the primary analysis to one role.

Prevalence percentages overlap and must not be added together. A job mentioning
both SQL and Python contributes to each skill's individual prevalence. Future
skill-combination analysis can measure portfolio coverage, co-occurrence,
support, confidence, and lift across bundles of skills.

#### Connect metrics to decisions

The first version is intended to answer:

> Across the job market I collected, which individual skills appear most often
> and therefore deserve consideration for what I should learn, strengthen, or
> keep interview-ready next?

This is a valid market-priority signal, especially while preserving options
across a spectrum of related roles. It is not yet a complete personalized study
prescription. A highly prevalent skill may already be a strength, and several
high-prevalence skills may occur in the same jobs.

Each later metric should be added only to answer a distinct question:

| Analysis layer | Question it answers |
| --- | --- |
| Individual prevalence | What does this collected market mention most? |
| Role-family prevalence | Where is each skill concentrated across adjacent roles? |
| Required/preferred classification | Is the skill expected, preferred, or merely mentioned? |
| Skill combinations | Which skills and recognizable stacks occur together? |
| Portfolio coverage | How many unique jobs mention at least one or several skills I possess? |
| Incremental coverage | Which additional skill reaches jobs my current portfolio does not? |
| Personal proficiency | Which market-relevant skills are genuine gaps for me? |
| Learning cost | Which gap offers the best return for the time required? |

The interpretation should progress without invalidating earlier results:

```text
Version 1: What does the market mention most?
    -> combination analysis: Which stacks cover distinct jobs?
    -> proficiency analysis: Which of those skills am I actually missing?
    -> learning-cost analysis: Which gap should I address first?
```

For example, high SQL prevalence could mean “learn SQL” for a beginner, but for
someone already strong in SQL it may mean “keep SQL sharp, practice interview
problems, and present the evidence more clearly.” The data is the same; the
decision depends on the question and personal context.

For dashboards, query `public.job_skill_prevalence_input`. It contains every
`(clean job, configured skill)` pair, including a `mentions_skill = false` row
when the job does not mention that skill. Apply relevance filters first, then
aggregate. This makes the filtered rows the single population for both numerator
and denominator and keeps configured skills with zero mentions visible:

```sql
WITH relevant_jobs AS (
    SELECT *
    FROM public.job_skill_prevalence_input
    WHERE date_posted >= CURRENT_DATE - INTERVAL '90 days'
      -- Optional comparison slice:
      -- AND title ILIKE '%data engineer%'
)
SELECT
    canonical_skill,
    COUNT(*) FILTER (WHERE mentions_skill) AS jobs_mentioning_skill,
    COUNT(*) AS total_jobs,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE mentions_skill)
        / NULLIF(COUNT(*), 0),
        1
    ) AS prevalence_pct
FROM relevant_jobs
GROUP BY canonical_skill
ORDER BY prevalence_pct DESC, canonical_skill;
```

In a BI tool, map dashboard controls to columns on this view, group by
`canonical_skill`, and calculate `AVG(mentions_skill::integer) * 100`. Show
`total_jobs` beside the percentage so changes in the population are visible.

Load an Excel sheet into PostgreSQL:

```powershell
python -m skillfreq.cli excel-load --excel data/inputs/jobs.xlsx --table staging.jobs --mode replace
```

The loader reads connection settings from `.env`. Use either `DATABASE_URL` or the existing `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and optional `DB_PORT` variables. Excel headers are normalized to PostgreSQL-friendly column names like `Job Title` -> `job_title`.

Each run writes an import log to `logging/excel_load_*.log` with the source file, sheet, normalized columns, destination table, mode, and row count. To choose the log path:

```powershell
python -m skillfreq.cli excel-load --excel data/inputs/jobs.xlsx --table staging.jobs --log-file logging/jobs_excel_load.log
```

For incremental loads, use a normalized Excel column as a conflict key:

```powershell
python -m skillfreq.cli excel-load --excel data/inputs/jobs.xlsx --table staging.jobs --mode upsert --primary-key job_url
```

Import a full JobSpy + SkillFreq + AI review batch into the PostgreSQL tables from the pgModeler schema:

```powershell
python -m skillfreq.cli import-batch `
  --batch-id 2026-06-18 `
  --jobs-csv C:\Users\ehose\Development\JobSpy\jobs-6-18-26.csv `
  --scores-csv data\outputs\results-6-18-26.csv `
  --review-xlsx data\analyze\chatGPTFeedback\results-6-18-26-review.xlsx `
  --scoring-version skillfreq-local `
  --rules-version ai-review-2026-06-18 `
  --cleaning-version v1
```

This writes scraped jobs to `raw_jobs`, SkillFreq scoring rows to `skill_scores`, one review batch row to `calibration_runs`, and AI review labels/reasons from the workbook's `Base` sheet to `calibration_results`. Use `--batch-mode replace` to re-run the same batch id after clearing only that batch's rows.

Extract resume signals:

```powershell
python -m skillfreq.cli extract --file data/inputs/resume.pdf
```

Compare a folder of job descriptions against profile signals:

```powershell
python -m skillfreq.cli suggest --jds data/inputs/jds
```

Route jobs toward resume variants:

```powershell
python -m skillfreq.cli route --input data/inputs/jobs.csv --out data/outputs/routed_jobs.csv
```

## Docker

Docker support exists in the repo, but it is still being shaped and is not the recommended path yet. For now, use the local Python setup above.

## Outputs

Typical outputs include:

- `data/outputs/results.csv`: scored jobs
- `data/outputs/failures.csv`: failed or blocked fetches
- `logging/skillfreq_log_*.log`: run logs
- `extracted_skills_*.txt`: extracted skill frequency summaries

The main results CSV includes:

```text
source, score, label, matched, required_total, missing, matches
```

## Use Cases

- study planning based on repeated market signals
- resume tailoring based on actual job requirements
- filtering roles that are technically or strategically off-lane
- spotting repeated tools, platforms, and requirement patterns
- comparing job descriptions against a local profile

## Docker Usage

Docker support is still being shaped, but the current container can be tested as a short-lived CLI run.

Build the image:

```powershell
docker build -t skillfreq .
```

Current `--no-scrape` workflow:

Set `JOBSPY_REPO` to the local path of your JobSpy repo before running the container:

```powershell
$env:JOBSPY_REPO="C:\path\to\JobSpy"
```

```powershell
docker run --rm `
  -v ${PWD}\data:/app/data `
  -v ${PWD}\configs:/app/configs `
  -v ${PWD}\logging:/app/logging `
  -v ${env:JOBSPY_REPO}:/jobspy `
  -e JOBSPY_DATA_PATH=/jobspy `
  skillfreq run --input data/inputs/links.txt --out data/outputs/results.csv --no-scrape
```

This keeps the work inside Docker while persisting user-editable inputs, outputs, configs, logs, and JobSpy CSV data on the host machine. The `--no-scrape` path reads cleaned JobSpy CSV data from `/jobspy` and writes results to `/app/data`.

URL scraping workflow with `links.txt`:

```powershell
docker run --rm `
  -v ${PWD}\data:/app/data `
  -v ${PWD}\configs:/app/configs `
  -v ${PWD}\logging:/app/logging `
  skillfreq run --input data/inputs/links.txt --out data/outputs/results.csv
```

When the container exits, anything written only inside the container disappears. Bind mounts like `-v ${PWD}\data:/app/data` are what keep the files available after the run.

---

## Roadmap

- skill frequency by job title
- resume <-> JD comparison
- better NLP normalization
- line-level evidence extraction
- visualization dashboards
- Notion integration
- trend reports over time
- easier personalization so other users can bring their own skill buckets, profile weights, role lanes, and resume signals through YAML setup

- stronger resume variant routing
- cleaner prompt and evaluation workflows
- Notion-oriented application tracking
- outreach and recruiter-finder workflows
- richer dashboards and trend reports
- polished Docker usage with documented bind mounts for inputs, outputs, configs, and logs

## Status

Active hobby project focused on turning job search and upskilling into a **systems-driven workflow instead of guesswork**.
