from pathlib import Path
import re
from skillfreq.skills.profile import load_profile
from skillfreq.skills.resume_profile.extract import load_yaml, load_resume_signal


def extract_jd_signals(jd_path: Path, skills_path: Path) -> set[str]:
    jd_text = jd_path.read_text(encoding="utf-8", errors="ignore").lower()
    skills_map = load_yaml(skills_path)

    detected_skills = set()

    for skill, terms in skills_map.items():
        for term in terms:
            pattern = r"\b" + re.escape(term) + r"\b"

            if re.search(pattern, jd_text):
                detected_skills.add(skill)
                break

    return detected_skills


def process_all_jobs(jd_folder: Path, skills_path: Path):
    txt_files = [p for p in jd_folder.rglob("*.txt") if p.is_file()]

    for jd_file in txt_files:
        try:
            print(f"Processing:{jd_file}")

            jd_signals = extract_jd_signals(jd_file, skills_path)
            profile_path = Path("configs/profile.yml")
            resume_signal_path = Path("configs/resume_signal.yml")

            result = compare_job_to_profile(
                jd_signals,
                profile_path,
                resume_signal_path
            )

            print(f"\n=== {jd_file.name} ===")
            print("Matched:", ", ".join(result["matched"]))
            print("Missing:", ", ".join(result["missing"]))
            print("Suggestions:")

            if result["suggestions"]:
                for s in result["suggestions"]:
                    print(f"- {s}")
            else:
                print("- No immediate resume tweak suggested")

        except Exception as e:
            print(f"Failed: {jd_file} -> {e}")


def compare_job_to_profile(jd_signals, profile_path: Path, resume_signal_path: Path) -> dict:
    SUGGESTION_MAP = {
        "data_quality": "Add 'data validation and reconciliation logic' to ETL pipeline bullet",
        "api": "Mention REST API integration (endpoints, payload validation, Postman)",
        "data_modeling": "Add wording around schema design, normalized tables, or mapping source data into structured SQL models",
        "sql": "Strengthen SQL mention with joins, aggregations, or query optimization",
        "etl": "Use stronger phrasing like 'designed and maintained ETL pipelines'",
        "airflow": "If applicable, mention workflow orchestration or scheduled pipelines",
        "seniority": "Add wording around ownership of end-to-end solutions, driving technical decisions, independently resolving complex issues, and delivering production-ready systems with measurable impact",
        "systems": "Add wording around pipeline lifecycle, dependency handling, failure recovery, or end-to-end data flow between systems"
    }

    DO_NOT_FORCE = {"aws", "kafka", "spark"}

    profile_skills = load_profile(profile_path)
    resume_signal_skills = load_resume_signal(resume_signal_path)

    weak = []
    matched = []
    missing = []

    for skill in jd_signals:
        if skill in resume_signal_skills:
            matched.append(skill)
        elif skill in profile_skills and profile_skills[skill] > 0:
            matched.append(skill)
        elif skill in profile_skills and skill not in resume_signal_skills:
            weak.append(skill)
        else:
            missing.append(skill)

    suggestions = []

    for skill in missing:
        if skill in DO_NOT_FORCE:
            suggestions.append(f"{skill}: only add if you can confidently speak to it")
        elif skill in SUGGESTION_MAP:
            suggestions.append(SUGGESTION_MAP[skill])

    suggestions = list(dict.fromkeys(suggestions))

    return {
        "matched": matched,
        "missing": missing,
        "suggestions": suggestions
    }