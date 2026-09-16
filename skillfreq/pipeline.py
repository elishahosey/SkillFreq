from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import logging
import os
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
from .scrape.fetch import process_empty_urls

from skillfreq.parse.parsers import FetchBlocked

from .io.loaders import read_lines
from .scrape.extract import extract_text_from_url
from .skills.resume_profile.extract import extract_resume_signals
import csv
import json
import yaml
from .score.grading import GradingContext, grade_job
from .skills.text import clean_text
from .io.grading_to_postgres import load_jobs_for_grading, load_prevalence, persist_grades as save_grades


def create_file(filename: str | Path, content: str, title: str | None = None) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        if title:
            f.write(f"{title}\n\n")
        f.write(content)

BASE_DIR = Path(__file__).resolve().parent.parent
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
filename = f"skillfreq_log_{timestamp}.log"

if not Path("./logging").exists():
    log_dir = BASE_DIR / "logging"
    log_dir.mkdir(exist_ok=True)
    
else:
    log_dir = Path("./logging")

log_file = log_dir / filename
log_file.open("w").close()  # create empty log file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

@dataclass
class JobResult:
    id:str
    source: str
    search_lane: str
    search_term_used: str
    review_priority: str
    score: float
    title: str
    label: str
    matched: int
    required_total: int
    missing: str
    matches_json: str
    description: str
    reason_codes: str
    apply_decision: str
    fit_quality: str
    role_lane: str
    source_site: str = ""
    deterministic_grade: dict = field(default_factory=dict)

@dataclass
class FailureRecord:
    source: str
    reason: str
    error: str 
    
@dataclass
class ResumeSuggestion:
    matched: list[str]
    missing: list[str]
    suggestions: list[str]
    
    
def fetch_links(input_path: Path, output_path: Path) -> None:
    jobspy_data = pd.read_csv(input_path)
    jd_urls = pd.DataFrame(jobspy_data, columns=['id','job_url','job_url_direct','title'])
    updated_urls = process_empty_urls(jd_urls)
    with output_path.open("w", encoding="utf-8") as f:
        for _, row in updated_urls.iterrows():
            url = row['job_url_direct'] if pd.notna(row['job_url_direct']) and row['job_url_direct'].strip() != "" else row['job_url']
            f.write(f"{url}\n")

def extract_links(file_path: str):
    extract_resume_signals(file_path)

def build_job_result(job, context, prevalence=None, market_context=None):
    grade = grade_job(job, context, prevalence=prevalence, market_context=market_context)
    return JobResult(
        id=grade.job_id, source=clean_text(job.get('url') or job.get('source') or job.get('job_url')),
        source_site=clean_text(job.get('source_site') or job.get('site')),
        search_lane=clean_text(job.get('search_lane')), search_term_used=clean_text(job.get('search_term_used')),
        review_priority=clean_text(job.get('review_priority')), score=grade.alignment_score,
        title=clean_text(job.get('title')), label=grade.label, matched=grade.matched,
        required_total=grade.required_total, missing=';'.join(grade.missing),
        matches_json=json.dumps(grade.counts), description=clean_text(job.get('description')),
        reason_codes=';'.join(grade.reason_codes), apply_decision=grade.apply_decision,
        fit_quality=grade.fit_quality, role_lane=grade.role_lane, deterministic_grade=grade.to_dict())


def grading_market(context, use_market_data=True):
    if not use_market_data:
        return None, {'source': 'offline'}
    try:
        return load_prevalence(context.taxonomy_version)
    except Exception as error:
        # Grading remains deterministic and usable offline, without fabricated prevalence.
        detail = str(error) if isinstance(error, ValueError) else type(error).__name__
        logging.warning('Market prevalence unavailable: %s; learning_score is NULL (unavailable), not zero. Check refresh-job-skills and db/job_skills.sql.', detail)
        return None, {'source': 'unavailable', 'error_type': type(error).__name__, 'detail': detail}


def finish_grading(out_csv_path, results, context, persist=False):
    write_results_csv(out_csv_path, results)
    # One complete versioned configuration snapshot per export, not per description.
    out_csv_path.with_suffix('.grading.yml').write_text(yaml.safe_dump({
        'grading_version': context.grading_version, 'taxonomy_version': context.taxonomy_version,
        'configuration': context.snapshot}, sort_keys=True), encoding='utf-8')
    if persist:
        save_grades(results, context)


def run_links(
    input_path: Path, skills_path: Path, out_csv_path: Path,
    profile_path: Path = Path('configs/profile.yml'),
    weight_path: Path = Path('configs/weights.yml'), min_score: float = 0.0,
    no_scrape: bool = True, use_market_data: bool = True, persist_grades: bool = False,
) -> list[dict[str, Any]]:
    context = GradingContext.load(skills_path=skills_path, profile_path=profile_path, weight_path=weight_path)
    prevalence, market = grading_market(context, use_market_data)
    results, failures = [], []
    if no_scrape:
        jobspy_path = Path(os.getenv('JOBSPY_DATA_PATH') or '../JobSpy')
        daily_path = jobspy_path / f"jobs-{datetime.now().month}-{datetime.now().day}-{datetime.now().strftime('%y')}.csv"
        jobs = pd.read_csv(daily_path, encoding='latin1', dtype={'id':str, 'source_job_id':str}).to_dict('records')
    else:
        jobs = [{'url': line} for line in read_lines(input_path) if line]
    for job in jobs:
        source = clean_text(job.get('job_url') or job.get('url'))
        try:
            if not no_scrape:
                payload = extract_text_from_url(source)
                if payload is None:
                    failures.append(FailureRecord(source, 'Extraction failed', ''))
                    continue
                job.update(payload if isinstance(payload, dict) else {'description': payload})
            result = build_job_result(job, context, prevalence, market)
            fallback = result.search_lane in {'survival', 'contract_survival'}
            if not no_scrape or result.score >= min_score or fallback:
                results.append(result)
        except FetchBlocked as error:
            failures.append(FailureRecord(source, 'blocked', str(error)))
        except Exception as error:
            failures.append(FailureRecord(source, 'grading_failed', str(error)))
    finish_grading(out_csv_path, results, context, persist_grades)
    write_failures_csv(out_csv_path.parent / 'failures.csv', failures)
    return [dict(id=r.id, source=r.source, title=r.title, label=r.label, description=r.description,
                 deterministic_grade=r.deterministic_grade) for r in results]


def grade_csv(input_path: Path, out_csv_path: Path, *, context=None,
              use_market_data=True, persist_grades=False):
    context = context or GradingContext.load()
    prevalence, market = grading_market(context, use_market_data)
    jobs = pd.read_csv(input_path, dtype={'id':str, 'source_job_id':str}).to_dict('records')
    results = [build_job_result(job, context, prevalence, market) for job in jobs]
    finish_grading(out_csv_path, results, context, persist_grades)
    return results


def grade_database(out_csv_path: Path, *, since_days=90, limit=None, context=None,
                   use_market_data=True, persist_grades=False, on_progress=None,
                   connect_timeout=10, statement_timeout=120, lock_timeout=10):
    """Grade stored descriptions through the same deterministic flow as CSV jobs."""
    context = context or GradingContext.load()
    if on_progress:
        on_progress(f'Reading jobs posted in the last {since_days} days from public.clean_jobs')
    jobs = load_jobs_for_grading(since_days, limit, connect_timeout=connect_timeout,
                                statement_timeout=statement_timeout, lock_timeout=lock_timeout)
    if on_progress:
        on_progress(f'Loaded {len(jobs)} jobs; preparing grading market context')
    prevalence, market = grading_market(context, use_market_data) if jobs else (None, {})
    results = []
    for index, job in enumerate(jobs, start=1):
        results.append(build_job_result(job, context, prevalence, market))
        if on_progress and (index % 100 == 0 or index == len(jobs)):
            on_progress(f'Graded {index}/{len(jobs)} jobs')
    finish_grading(out_csv_path, results, context, persist_grades and bool(results))
    return results


def write_results_csv(path: Path, results: Iterable[JobResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","source","title", "search_lane", "search_term_used", "review_priority", "score", "raw_match", "matched", "required_total",
                    "missing", "matches", "description", "reason_codes", "fit_quality", "role_lane", "apply_decision", "source_site", "fit_score", "learning_score", "pre_ai_score", "confidence", "ai_review_required", "grading_version", "taxonomy_version", "grade_json", "learning_status"])
        for r in results:
            w.writerow([r.id,r.source, r.title, r.search_lane, r.search_term_used, r.review_priority, f"{r.score:.3f}", r.label, r.matched, r.required_total, r.missing, r.matches_json, r.description, r.reason_codes, r.fit_quality, r.role_lane, r.apply_decision, r.source_site, *[r.deterministic_grade.get(k) for k in ("fit_score", "learning_score", "pre_ai_score", "confidence", "ai_review_required", "grading_version", "taxonomy_version")], json.dumps(r.deterministic_grade), r.deterministic_grade.get('learning_status')])

def write_failures_csv(path: Path, failures: Iterable[FailureRecord]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "reason", "error"])
        for r in failures:
            w.writerow([r.source, r.reason, r.error])
         
