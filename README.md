# SkillFreq

SkillFreq turns scraped job descriptions into evidence for what to apply to, skip,
and learn next. It is a personal Python CLI built around my job search, profile,
and resume variants.

```text
Scrape jobs → Job CSV → Deterministic grading → Review results → Apply or learn
                             ↑
                Optional PostgreSQL market data
```

**Start with the [workflow guide](docs/workflow.md)** for the complete process,
from JobSpy scraping through grading, market analysis, review and saved history.

## What it produces

- A role lane and an apply decision for each job.
- Separate fit and learning scores, plus explainable confidence.
- Matched technologies, broader capabilities, requirement gaps and rule evidence.
- A results CSV and versioned configuration snapshot.
- Optional PostgreSQL market prevalence and grading history.

Explicit terminology is matched deterministically. Atomic technologies stay
separate from broader fit concepts. AI review is requested only for ambiguity;
SkillFreq does not call AI automatically.

## Quick start

1. [Set up the Python environment](docs/commands.md#setup).
2. [Grade stored PostgreSQL jobs from a VS Code task](docs/commands.md#grade-jobs-from-postgresql),
   or [grade a CSV](docs/commands.md#grade-a-csv).
3. Review the exported results CSV and keep its `.grading.yml` snapshot beside it.

Offline grading requires no database. Follow the [workflow guide](docs/workflow.md)
to add market data, scrape URLs or save history. Use the
[command reference](docs/commands.md) for copyable commands and options.

## Configuration

Start with `configs/profile.yml` for your strengths and growth priorities.
`market_skills.yml` owns atomic technologies; `skills.yml` owns broader capability
concepts. Role rules, requirements and scoring settings live in the other YAML
files under `configs/`.

## Documentation

- [Change career policy through configuration](docs/career-policy.md)
- [90-day calibration comparison](docs/calibration-comparison.md)
- [Manual calibration review UI](docs/calibration-review.md)
- [Focused domain calibration: integration, ecosystems and databases](docs/domain-calibration-comparison.md)
- [Ecosystem concentration policy and comparison](docs/ecosystem-policy.md)
- [Usage workflow: scraped jobs to results](docs/workflow.md)
- [Command reference](docs/commands.md)
- [Grading architecture, configuration and migrations](docs/deterministic-grading.md)
- [Preserve the audit trail and reproduce a grading run](docs/grading-reproduction.md)
- [Example grades with full evidence](docs/grading-examples.yml)
- [Representative grading comparisons](docs/grading-comparison.md)
- [Historical job comparison](docs/grading-historical-sample.md)

Local Python is the main workflow; Docker usage is covered in the command reference.
