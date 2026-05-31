from __future__ import annotations

from dataclasses import dataclass
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
from .skills.dictionary import load_skill_dictionary
from .skills.dictionary import load_weights
from .skills.match import match_skills
# from .score.similarity import overlap_score
# from .score.similarity import profile_alignment_score
from .score.similarity import weighted_alignment_score
#from .skills.resume_profile.resume_signal_check import *
from .skills.resume_profile.extract import extract_resume_signals
from .score.thresholds import classify
from .skills.profile import load_profile
from .skills.extract import extract_requirement_flags
from skillfreq.skills.resume_profile.extract import extract_resume_signals
from skillfreq.score.decision_layer import decide_apply_bucket, derive_fit_quality
from .score.lane_classifier import classify_role_lane
import csv


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

def run_links(
    input_path: Path,
    skills_path: Path,
    out_csv_path: Path,
    profile_path: Path = Path("configs/profile.yml"),
    weight_path: Path = Path("configs/weights.yml"),
    min_score: float = 0.0,
    no_scrape: bool = True,
) -> list[dict[str, Any]]:
    skills = load_skill_dictionary(skills_path)
    lines = [ln for ln in read_lines(input_path) if ln]

    results: list[JobResult] = []
    failures: list[FailureRecord] = []

    profile = load_profile(profile_path)
    weights, penalties = load_weights(weight_path)

    if no_scrape:
        jobspy_data_path = os.getenv("JOBSPY_DATA_PATH") or "../JobSpy"
        df = pd.read_csv(
            #WIDEN Search? uncomment for uncleaned_jobs
            #jobspy_data_path + f"/jobs-5-24-26.csv",

            jobspy_data_path + f"/jobs-{datetime.now().month}-{datetime.now().day}-{datetime.now().strftime('%y')}.csv",
           # jobspy_data_path + f"/cleaned_jobs-{datetime.now().month}-{datetime.now().day}-{datetime.now().strftime('%y')}.csv",
            encoding='latin1'
        ) #if encountering encoding issues, try 'latin1' or 'utf-8-sig'
        print(f"Loaded {len(df)} job descriptions from CSV for processing.")

        job_rows = []
        for _, row in df.iterrows():
            job_rows.append(
                {
                    "id": row.get("id", ""),
                    "url": row.get("job_url", ""),
                    "title": row.get("title", ""),
                    "description": row.get("description", ""),
                    "search_lane": row.get("search_lane", ""),
                    "search_term_used": row.get("search_term_used", ""),
                    "review_priority": row.get("review_priority", ""),
                }
            )

        for job in job_rows:
            try:
                url = job["url"]
                id = job["id"]
                title = job["title"]
                description = job["description"]
                search_lane = job["search_lane"]
                search_term_used = job["search_term_used"]
                review_priority = job["review_priority"]

                counts = match_skills(description, skills)
                flags = extract_requirement_flags(description, skills, profile)
                score, matched, required_total, missing = weighted_alignment_score(
                    counts,
                    profile,
                    weights,
                    penalties,
                    description=description,
                    flags=flags,
                )
                label = classify(score, flags)
                reason_codes = ";".join(flags.get("reason_codes", []))

                row_payload = {
                    "title": title,
                    "description": description,
                    "reason_codes": reason_codes,
                    "label": label,
                    "score": score,
                    "matched": matched,
                    "required_total": required_total,
                    "missing": ";".join(missing),
                    "search_lane": search_lane,
                }

                apply_decision = decide_apply_bucket(row_payload)
                fit_quality = derive_fit_quality(row_payload)
                role_lane = classify_role_lane(row_payload)

                include_fallback_lane = search_lane in {"survival", "contract_survival"}

                if score >= min_score or include_fallback_lane:
                    results.append(
                        JobResult(
                            id=id,
                            source=url,
                            search_lane=search_lane,
                            search_term_used=search_term_used,
                            review_priority=review_priority,
                            score=score,
                            title=title,
                            label=label,
                            matched=matched,
                            required_total=required_total,
                            missing=";".join(missing),
                            matches_json=str(counts),
                            description=description,
                            reason_codes=reason_codes,
                            apply_decision=apply_decision,
                            fit_quality=fit_quality,
                            role_lane=role_lane,
                        )
                    )

                print(f"{url} | id={id} |title={title}| score={score:.2f} | label={label} | reasons={flags.get('reason_codes', [])}")

            except Exception as e:
                print(f"Error processing {job.get('url', '')}: {e}")
                continue

    else:
        for line in lines:
            try:
                source = line
                text = extract_text_from_url(line)

                if text is None:
                    failures.append(FailureRecord(source=line, reason="Extraction failed", error=""))
                    continue

                description = text["description"] if isinstance(text, dict) else text
                id = text.get("id", "") if isinstance(text, dict) else ""
                title = text.get("title", "") if isinstance(text, dict) else ""

                counts = match_skills(description, skills)
                flags = extract_requirement_flags(description, skills, profile)
                score, matched, required_total, missing = weighted_alignment_score(
                    counts,
                    profile,
                    weights,
                    penalties,
                    description=description,
                    flags=flags,
                )
                label = classify(score, flags)
                reason_codes = ";".join(flags.get("reason_codes", []))

                row_payload = {
                    "title": title,
                    "description": description,
                    "reason_codes": reason_codes,
                    "label": label,
                    "score": score,
                    "matched": matched,
                    "required_total": required_total,
                    "missing": ";".join(missing),
                }

                apply_decision = decide_apply_bucket(row_payload)
                fit_quality = derive_fit_quality(row_payload)
                role_lane = classify_role_lane(row_payload)

                #if score >= min_score: #I'm including survival lane
                results.append(
                    JobResult(
                            id=id,
                        source=source,
                            title=title,
                        search_lane="",
                        search_term_used="",
                        review_priority="",
                        score=score,
                        label=label,
                        matched=matched,
                        required_total=required_total,
                        missing=";".join(missing),
                        matches_json=str(counts),
                        description=description,
                        reason_codes=reason_codes,
                        apply_decision=apply_decision,
                        fit_quality=fit_quality,
                        role_lane=role_lane,
                    )
                )

            except FetchBlocked as e:
                failures.append(FailureRecord(source=line, reason="blocked", error=str(e)))
                continue
            except Exception as e:
                print(f"Error processing {line}: {e}")
                continue

    write_results_csv(out_csv_path, results)
    write_failures_csv(out_csv_path.parent / "failures.csv", failures)

    return [
        {
            "id": r.id,
            "source": r.source,
            "title": r.title,
            "label": r.label,
            "description": r.description,
        }
        for r in results
    ]

def write_results_csv(path: Path, results: Iterable[JobResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","source","title", "search_lane", "search_term_used", "review_priority", "score", "raw_match", "matched", "required_total",
                    "missing", "matches", "description", "reason_codes", "fit_quality", "role_lane", "apply_decision"])
        for r in results:
            w.writerow([r.id,r.source, r.title, r.search_lane, r.search_term_used, r.review_priority, f"{r.score:.3f}", r.label, r.matched, r.required_total, r.missing, r.matches_json, r.description, r.reason_codes, r.fit_quality, r.role_lane, r.apply_decision])

def write_failures_csv(path: Path, failures: Iterable[FailureRecord]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "reason", "error"])
        for r in failures:
            w.writerow([r.source, r.reason, r.error])
         
