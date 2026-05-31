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
