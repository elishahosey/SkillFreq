from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from skillfreq.parse.parsers import FetchBlocked

from .io.loaders import read_lines
from .scrape.extract import extract_text_from_url
from .skills.dictionary import load_skill_dictionary
from .skills.match import match_skills
from .score.similarity import overlap_score
from .score.similarity import profile_alignment_score
from .score.thresholds import classify
from .skills.profile import load_profile
import csv


@dataclass
class JobResult:
    source: str
    score: float
    label: str
    matched: int
    required_total: int
    missing: str
    matches_json: str  # simple string form for now

@dataclass
class FailureRecord:
    source: str
    reason: str
    error: str 

def run_links(
    input_path: Path,
    skills_path: Path,
    out_csv_path: Path,
    profile_path: Path=Path("configs/profile.yml"),
    min_score: float = 0.0,
    no_scrape: bool = False,
) -> None:
    skills = load_skill_dictionary(skills_path)
    lines = [ln for ln in read_lines(input_path) if ln]

    results: list[JobResult] = []
    failures: list[FailureRecord] = []
    for line in lines:
        try:
            if no_scrape:
                text = line
                source = "raw_text"
            else:
                source = line
            #returned object from job description, containing text and metadata
                text = extract_text_from_url(line) or ""

            #grab skill counts for this job description
            counts = match_skills(text, skills)
            profile=load_profile(profile_path)
            score, matched, required_total, missing = profile_alignment_score(counts, profile)
            label = classify(score)

            if score >= min_score:
                # keep MVP simple: store counts as a string
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
         
