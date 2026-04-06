from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
import os
from pathlib import Path
from typing import Iterable

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
import csv


def create_file(filename: str | Path, content: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
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
    source: str
    score: float
    label: str
    matched: int
    required_total: int
    missing: str
    matches_json: str  

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
    profile_path: Path=Path("configs/profile.yml"),
    weight_path: Path=Path("configs/weights.yml"),
    min_score: float = 0.0,
    no_scrape: bool = True, #read from csv for descriptions instead of scraping from url. Either due to laziness or because the urls are bad and we already have the descriptions in a csv (e.g. from joblist.py)
) -> list[tuple[str, str]]: 
    skills = load_skill_dictionary(skills_path)
    lines = [ln for ln in read_lines(input_path) if ln]

    results: list[JobResult] = []
    failures: list[FailureRecord] = []
    jdParsedObject=[]
    
    if no_scrape:
        # If no scraping, we expect the input file to be a CSV with 'job_url' and 'description' columns
        df = pd.read_csv(os.getenv("JOBSPY_DATA_PATH")+f"/cleaned_jobs-{datetime.now().month}-{datetime.now().day}-{datetime.now().strftime('%y')}.csv")
        print(f"Loaded {len(df)} job descriptions from CSV for processing.")
        
        for _, row in df.iterrows():
            url = row['job_url']
            id = row['id']
            description = row['description']
            jdParsedObject.append((id,url, description))
        
        #for each job, grab the skills and signals from the description, then score against the profile and weights, then classify and save results
        for id, url, description in jdParsedObject:
            try:
                counts = match_skills(description, skills)
                profile=load_profile(profile_path)
                weights,penalties=load_weights(weight_path)
                flags = extract_requirement_flags(description, skills, profile)
                score, matched, required_total, missing = weighted_alignment_score(counts, profile, weights,penalties)
                label = classify(score,flags)

                if score >= min_score:
                    results.append(
                        JobResult(
                            source=url,
                            score=score,
                            label=label,
                            matched=matched,
                            required_total=required_total,
                            missing=";".join(missing),
                            matches_json=str(counts),
                        )
                    )

            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
    else:
        for line in lines:
            try:
                source = line
                text = extract_text_from_url(line)
                if text is None:
                    failures.append(FailureRecord(source=line, reason="Extraction failed", error=""))
                    continue
                jdParsedObject.append((line,text))
                description = text['description'] if isinstance(text, dict) else text
                
                #grab skill counts for this job description
                counts = match_skills(description, skills)
                profile=load_profile(profile_path)
                weights,penalties=load_weights(weight_path)
                flags = extract_requirement_flags(description, skills, profile)

                score, matched, required_total, missing = weighted_alignment_score(counts, profile, weights,penalties)
                # label = classify(score)
                # if flags["has_hard_requirement_blockers"]:
                #     label = "Skip"
                # else:
                label = classify(score,flags)

                if score >= min_score:
                    results.append(
                        JobResult(
                            source=source,
                            score=score,
                            label=label,
                            matched=matched,
                            required_total=required_total,
                            missing=";".join(missing),
                            matches_json=str(counts),
                        )
                    )


            except Exception as e:
                print(f"Error processing {line}: {e}")
                continue
            except FetchBlocked as e:
                failures.append(FailureRecord(source=line, reason="blocked", error=str(e)))
                continue

    write_results_csv(out_csv_path, results)
    write_failures_csv(out_csv_path.parent / "failures.csv", failures)

    return jdParsedObject


def write_results_csv(path: Path, results: Iterable[JobResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "score", "label", "matched", "required_total", "missing", "matches"])
        for r in results:
            w.writerow([r.source, f"{r.score:.3f}", r.label, r.matched, r.required_total, r.missing, r.matches_json])

def write_failures_csv(path: Path, failures: Iterable[FailureRecord]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "reason", "error"])
        for r in failures:
            w.writerow([r.source, r.reason, r.error])
         
