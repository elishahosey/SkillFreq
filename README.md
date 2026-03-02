
SkillFreq

SkillFreq is a Python-based job description analysis tool that extracts, classifies, and ranks technical skills across large volumes of job postings.

It helps engineers make data-driven upskilling decisions by identifying high-frequency technologies and market gaps.

🚀 Why I Built This

Modern job searches are noisy and subjective. Instead of manually reading dozens of job descriptions and guessing what to study, I built SkillFreq to:

Parse job descriptions at scale

Extract skill mentions using configurable YAML dictionaries

Rank skills by frequency and relevance

Identify strategic upskilling targets

This project turns job market analysis into a repeatable, measurable process.

🧠 What It Does

Scrapes or ingests job descriptions (Ashby, Lever, etc.)

Tokenizes and normalizes text

Matches skills using YAML-defined keyword buckets

Computes frequency counts and classification labels

Outputs ranked skill lists to guide learning priorities

🏗 Architecture Overview

SkillFreq is built around a modular parsing architecture:

BaseParser
  ├── AshbyParser
  ├── LeverParser
  └── (Extensible for new platforms)

Skill classification is driven by a YAML configuration file, allowing:

Easy addition of new technologies (Kafka, Airflow, Spark, etc.)

Concept grouping (e.g., Event Streaming → Kafka, Pub/Sub)

Customizable market targeting (data engineering, backend, etc.)

🛠 Tech Stack

Python

CLI interface

YAML-based configuration

Basic NLP preprocessing (tokenization + normalization)

CSV export for downstream analysis

📊 Example Use Case

Collect 50 data engineering job descriptions

Run SkillFreq

Identify top recurring skills (e.g., SQL, Kafka, Airflow)

Update learning roadmap based on objective frequency data

🎯 Roadmap

Add concept-level rollups (e.g., Event Streaming vs specific tools)

Add evidence extraction (line-level skill matches)

Improve NLP preprocessing and normalization

Add visualization support

Optional streaming ingestion for large-scale market scans

📌 Status

Active hobby project focused on data engineering market analysis and skill prioritization.



SkillFreq is an analysis tool that extracts technical skills from job descriptions, which can help us align study plans to ACTUAL market demands rather than grinding at the wrong place.

Input:
- extract technical skills from text
- Normalize common aliases
- Filters out soft skills (just be a cool human, and you should be fine lol)

Output:
- Frequency table of technical skills
- Per role breakdown

Use cases:
- Resume optimization: Validate your resume emphasizes skills the market actually wants.
- Job filtering: Quickly spot roles that dont match your core skill set.
- Study planning: Focus learning time on skills with highest return
- Market Sensing: Detect patterns across job titles and companies


Roadmap:
- Skill frequency based on job title
- Resume <-> JD comparison
- Integration with Notion or other job-tracking tools

Environments:
- .venv        → parsing (pydparser, python-dateutil==2.8.2)
- .venv-scrape → scraping (trafilatura, htmldate)
