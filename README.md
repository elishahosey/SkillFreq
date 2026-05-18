# SkillFreq

**SkillFreq** is a Python-based job description analysis tool that extracts, classifies, and ranks technical skills across large volumes of job postings.

I originally built this for myself after getting frustrated with the job-search process and wanting a more **data-driven way to understand the market**.

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

So SkillFreq became my way of answering:

- What does the market actually want?
- What technologies keep showing up?
- Where are my real gaps?
- What should I spend time learning?

Basically: **stop grinding in the wrong direction**.

---

## What It Does

SkillFreq currently works as:

`JobSpy -> SkillFreq -> market + alignment insights`

It can:

- ingest job descriptions from scraped URLs
- parse common job platforms (Ashby, Lever, and extensible parsers)
- extract technical skills using YAML keyword buckets
- normalize aliases and grouped concepts
- output ranked skill frequency lists
- compare roles against a personal skill profile
- help identify study priorities

For example, if Kafka, AWS, and Airflow keep appearing across roles, that is probably a stronger signal than randomly doom-scrolling articles.

Currently pairs well with [JobSpy](https://github.com/speedyapply/JobSpy) for ingestion.

---

## Architecture Overview

    BaseParser
      ├── AshbyParser
      ├── LeverParser
      └── Extensible for new platforms

Skill classification is YAML-driven, which makes it easy to:

- add new technologies
- group related concepts
- tune scoring logic
- personalize for target markets  
  (data engineering, backend, platform roles, etc.)

---

## Tech Stack

- Python
- CLI interface
- YAML configuration
- lightweight NLP preprocessing
- CSV export

---

## Configuration

The `configs/` folder contains the primary configuration files:

- `skills.yml` -> skill keyword buckets
- `weights.yml` -> scoring weights
- `profile.yml` -> alignment profile settings

These are intended as starter templates and can be adjusted for your use case.

Local environment settings are stored in `.env`.

Example:

`NLTK_PATH=/local/path`

Do not commit `.env` if it contains machine-specific paths or sensitive values.

---

## Use Cases

- **study planning**  
  focus learning time on skills with the highest market frequency

- **resume optimization**  
  validate whether resume bullets match real demand

- **job filtering**  
  quickly spot roles that do not actually align

- **market sensing**  
  identify hiring trends across companies and titles

---

## Example Workflow

1. Collect 50 data engineering job descriptions
2. Run SkillFreq
3. Identify recurring technologies
4. update study roadmap based on objective frequency data

Example recurring outputs might include:

- SQL
- Kafka
- Airflow
- AWS
- ETL tooling

---

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

---

## Status

Active hobby project focused on turning job search and upskilling into a **systems-driven workflow instead of guesswork**.
