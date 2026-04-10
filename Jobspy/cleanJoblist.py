"""
Clean the job list by removing non-target jobs, duplicates, and irrelevant entries.
Reads raw job listings from jobs.csv, keeps relevant data/backend/integration roles,
and saves the cleaned list to cleaned_jobs.csv with a fit bucket.

Fit buckets:
- apply  -> strong fit, direct URL available
- review -> possible fit, but needs manual review or is a weaker secondary match
- skip   -> not aligned enough
"""

import re
import pandas as pd
from datetime import datetime

now = datetime.now()
date = f"{now.month}-{now.day}-{now.strftime('%y')}"
filename = f"jobs-{date}.csv"
clean_filename = f"cleaned_jobs-{date}.csv"

jobs_df = pd.read_csv(filename)
jobs_df.columns = jobs_df.columns.str.strip().str.lower()

processed_count = len(jobs_df)
print(f"Total jobs before cleaning: {processed_count}")

FALLBACK=False

# titles only for fallback
bridge_roles = [
    "backend engineer",
    "backend developer",
    "systems analyst",
    "automation engineer",
    "database engineer",
    "application engineer",
]

# Strong title matches: keep more easily
primary_keywords = [
    "data integration engineer",
    "data warehouse engineer",
    "data infrastructure engineer",
    "big data engineer",
    "data engineer",
    "data platform engineer",
    "etl engineer",
    "analytics engineer",
    "data pipeline engineer",
    "integration engineer",
    "data developer",
    "sql developer",
    "data systems engineer",
    "data quality engineer",
    "data integration developer",
    "data operations engineer",
    "data ingestion engineer",
    "software engineer data engineering",
    "database developer"
]

# Broader/adjacent roles: must earn entry with description evidence
secondary_keywords = [
    "backend engineer",
    "platform engineer",
    "software engineer data",
    "application engineer data",
    "systems engineer data",
    "reporting engineer",
    "business intelligence engineer",
    "data analyst sql",
     "associate developer",
    "junior developer",
    "software developer i",
    "application developer",
    "backend engineer sql",
    "backend engineer data",
    "data integration developer",
    "application developer data",
    "api developer",
    "api engineer",
]

# Description signals that support secondary roles
description_keywords = [
    "sql",
    "etl",
    "elt",
    "pipeline",
    "pipelines",
    "data warehouse",
    "data platform",
    "integration",
    "api",
    "python",
    "spark",
    "airflow",
    "dbt",
    "kafka",
    "microservices",
    "distributed systems",
    "event streaming",
    "data ingestion",
    "batch processing",
    "stream processing",
    "schema",
    "data modeling",
]

# Titles to exclude
exclude_keywords = [
    "senior",
    "sr",
    "lead",
    "principal",
    "staff",
    "vp",
    "director",
    "manager",
    "head",
    #"architect",
    "intern",

    # domain-specific exclusions
    "embedded",
    "firmware",
    "automotive",
    "ecu",
    "lin",
    "can bus",
    "flexray",
    "plc",
    "controls engineer",
    "gpu",
    
    #frontend specific exclusions
    "full stack",
    "front-end",
    "frontend",
    "ui",
    "front end",
    "ui developer",
    "web developer",
    "asp.net developer",
    ".net developer",
    "react developer",
    "angular developer",
    "javascript developer",
    "mobile developer",
    "ios developer",
    "android developer",
    
    #Space/defense specific exclusions
    "propulsion",
    "aerospace",
    "mechanical",
    "simulation",
    "aircraft",
    "UAS",
    "avionics"
    
    
    
    
]

SHORT_WORD_EXCLUDES = {"sr", "vp"}

def normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()

def contains_keyword(text, keyword):
    text = normalize_text(text)
    keyword = keyword.lower().strip()

    if keyword in SHORT_WORD_EXCLUDES:
        pattern = rf"\b{re.escape(keyword)}\b"
        return re.search(pattern, text) is not None

    return keyword in text

def has_direct_url(row):
    direct_url = normalize_text(row.get("job_url_direct", ""))
    return direct_url != ""

def is_excluded_title(row):
    title = normalize_text(row.get("title", ""))
    return any(contains_keyword(title, keyword) for keyword in exclude_keywords)

def description_signal_count(row):
    description = normalize_text(row.get("description", ""))
    return sum(1 for keyword in description_keywords if keyword in description)

def title_type(row):
    title = normalize_text(row.get("title", ""))

    if any(keyword in title for keyword in primary_keywords):
        return "primary"

    if any(keyword in title for keyword in secondary_keywords):
        return "secondary"
    
    if FALLBACK and any(keyword in title for keyword in bridge_roles):
        return "bridge"

    return "other"

def assign_fit_bucket(row):
    if row["is_excluded"]:
        return "skip"

    role_type = row["title_type"]
    signal_count = row["description_signal_count"]
    direct_url = row["has_direct_url"]

    # Primary roles are aligned by title
    if role_type == "primary":
        return "apply" if direct_url else "review"

    # Secondary roles must earn entry
    if role_type == "secondary":
        if signal_count >= 3:
            return "apply" if direct_url else "review"
        if signal_count >= 2:
            return "review"
        return "skip"

    # Bridge roles are a fallback with lower standards
    if role_type == "bridge":
        if signal_count >= 4:
            return "apply" if direct_url else "review"
        if signal_count >= 3:
            return "review"
        return "skip"

    return "skip"

# Dedupe key: combination of columns that define uniqueness.
def build_dedupe_key(row):
    direct_url = normalize_text(row.get("job_url_direct", ""))
    job_url = normalize_text(row.get("job_url", ""))
    title = normalize_text(row.get("title", ""))
    company = normalize_text(row.get("company", ""))
    description=normalize_text(row.get("description", ""))
    
    if description:
        return f"description::{description}"

    if direct_url:
        return f"direct::{direct_url}"
    if job_url:
        return f"url::{job_url}"
    return f"title_company::{title}::{company}::{description}"

# Compute flags
jobs_df["title_type"] = jobs_df.apply(title_type, axis=1)
jobs_df["description_signal_count"] = jobs_df.apply(description_signal_count, axis=1)
jobs_df["is_excluded"] = jobs_df.apply(is_excluded_title, axis=1)
jobs_df["has_direct_url"] = jobs_df.apply(has_direct_url, axis=1)
jobs_df["fit_bucket"] = jobs_df.apply(assign_fit_bucket, axis=1)

print("\nFit bucket counts before dedupe:")
print(jobs_df["fit_bucket"].value_counts(dropna=False))

# Keep only rows that are actionable
cleaned_jobs_df = jobs_df[jobs_df["fit_bucket"].isin(["apply", "review"])].copy()

print(
    f"\nTotal jobs after fit filtering: {len(cleaned_jobs_df)} "
    f"({len(cleaned_jobs_df) / processed_count:.2%} of original)"
)

# Safer dedupe logic
cleaned_jobs_df["dedupe_key"] = cleaned_jobs_df.apply(build_dedupe_key, axis=1)
cleaned_jobs_df = cleaned_jobs_df.drop_duplicates(subset=["dedupe_key"], keep="first")

# Manual review flag
cleaned_jobs_df["manual_review"] = cleaned_jobs_df["fit_bucket"] == "review"

print("\nFit bucket counts after dedupe:")
print(cleaned_jobs_df["fit_bucket"].value_counts(dropna=False))
print(f"Manual review jobs: {cleaned_jobs_df['manual_review'].sum()}")

# Sort apply first, then review
bucket_order = {"apply": 0, "review": 1}
cleaned_jobs_df["bucket_sort"] = cleaned_jobs_df["fit_bucket"].map(bucket_order)
cleaned_jobs_df = cleaned_jobs_df.sort_values(
    by=["bucket_sort", "description_signal_count", "company", "title"],
    ascending=[True, False, True, True]
).drop(columns=["bucket_sort"])

# Optional cleanup
cleaned_jobs_df = cleaned_jobs_df.drop(columns=["dedupe_key"])

cleaned_jobs_df.to_csv(clean_filename, index=False)
print(f"\nSaved cleaned jobs to {clean_filename}")