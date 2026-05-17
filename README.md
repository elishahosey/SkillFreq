# SkillFreq

SkillFreq is a Python CLI for turning job descriptions into market signals: recurring skills, profile alignment, missing requirements, and CSV outputs you can use to make a job search less guessy.

I originally built this for myself after getting frustrated with job boards, vague recommendations, and roles that looked relevant until the requirements told a different story. The goal is simple: collect job descriptions, extract the signals, and use the evidence to decide what to study, skip, tailor, or apply to.

## What It Does

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

Count job titles in a CSV:

```powershell
python -m skillfreq.cli titles data/outputs/results.csv --title-col title
```

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

## Coming Soon

These areas are in progress or belong to active branch work:

- stronger resume variant routing
- cleaner prompt and evaluation workflows
- Notion-oriented application tracking
- outreach and recruiter-finder workflows
- richer dashboards and trend reports
- polished Docker usage with documented bind mounts for inputs, outputs, configs, and logs

## Status

Active hobby project. The main branch is usable as a local CLI workflow, while newer job-search, routing, and evaluation ideas are still being shaped.
