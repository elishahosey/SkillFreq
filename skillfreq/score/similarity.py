from __future__ import annotations

from email.mime import text
from typing import Dict, Tuple, List

def keyword_count(text: str, keywords: List[str]) -> int:
    text = text.lower()
    return sum(1 for kw in keywords if kw in text)


def weighted_alignment_score(
    skill_counts: Dict[str, int],
    profile: Dict[str, float],
    weights: Dict[str, float],
    penalties: Dict[str, float] | None = None,
    description: str = "",
    flags: Dict[str, object] | None = None,
) -> Tuple[float, int, int, List[str]]:

    penalties = penalties or {}
    flags = flags or {}
    
    score = 0.0
    matched = 0
    total = 0
    missing: List[str] = []

    for skill, count in skill_counts.items():
        if count <= 0:
            continue

        presence = 1 if count > 0 else 0
        total += 1
        profile_strength = profile.get(skill, 0.0)

        # handle penalties
        if skill in penalties:
            score += count * penalties[skill]
            continue

        weight = weights.get(skill, 1.0)
        contribution = presence * profile_strength * weight

        capped_skills = {
            "systems": 1.5,
            "dev_practices": 1.0,
            "software_engineering": 1.0,
            "operations": 1.5,
            "testing": 1.0,
        }

        if skill in capped_skills:
            contribution = min(contribution, capped_skills[skill])

        score += contribution
        if skill == "dev_practices":
            continue  # ignore completely

        if profile_strength > 0:
            matched += 1
        else:
            missing.append(skill)

        # -----------------------------
    # JD pattern boosts / penalties
    # -----------------------------
    desc = (description or "").lower()

    pipeline_keywords = [
        "etl", "elt", "data pipeline", "data pipelines",
        "ingestion", "data ingestion",
        "transformation", "data transformation",
        "data integration",
        "data quality", "validation", "reconciliation",
    ]
    pipeline_score = keyword_count(desc, pipeline_keywords)

    # Strong DE alignment boost
    if pipeline_score >= 4 and skill_counts.get("sql", 0) > 0:
        score += 3.0
    elif pipeline_score >= 4:
        score += 2.0
    elif pipeline_score >= 2:
        score += 1.0

    integration_keywords = [
        "multiple source systems",
        "api", "rest", "json", "xml",
        "data integration",
        "external systems",
        "semi-structured",
        "structured and semi-structured",
    ]
    if keyword_count(desc, integration_keywords) >= 2:
        score += 1.5

    if any(x in desc for x in [
        "no prior experience",
        "0-2 years",
        "1-3 years",
        "junior",
        "early career",
    ]):
        score += 1.5
        
    if "no prior experience" in description or "0-2 years" in description:
        score += 5.0
        
    if skill_counts.get("etl", 0) >= 3 and skill_counts.get("sql", 0) > 0:
        score += 4.0

    if any(x in desc for x in [
        "analytics", "reporting",
        "datasets for analytics",
        "business insights",
        "support analytics",
        "analytics platform",
    ]):
        score += 1.0

    modern_heavy = ["kafka", "spark", "hadoop", "flink"]
    modern_count = keyword_count(desc, modern_heavy)

    aws_count = skill_counts.get("aws", 0)

    if aws_count >= 8:
        score -= 6.0
    elif aws_count >= 4:
        score -= 3.0

    if modern_count >= 2:
        score -= 3.0
    elif modern_count == 1:
        score -= 1.5

    ml_keywords = ["machine learning", "model", "training", "nlp", "classification", "regression"]
    if keyword_count(desc, ml_keywords) >= 2:
        score -= 3.0
    
    ai_ml_count = skill_counts.get("ai_ml", 0)
    if skill_counts.get("ai_ml", 0) >= 2:
        score -= 8.0
    if "llm" in description or "agent" in description or "prompt engineering" in description:
        score -= 6.0
    if ai_ml_count >= 2:
        score -= 6.0
    elif ai_ml_count == 1:
        score -= 3.0
        
    if (
        skill_counts.get("etl", 0) >= 2 and
        skill_counts.get("sql", 0) >= 1
    ):
        score += 5.0
     # -----------------------------
    # Post-score alignment penalties from flags
    # -----------------------------
    mandatory_missing = flags.get("mandatory_missing_skills", [])
    modern_required_missing = flags.get("modern_required_missing_skills", [])
    modern_preferred_missing = flags.get("modern_preferred_missing_skills", [])
    is_lead_like = flags.get("is_lead_like", False)
    years_required = flags.get("years_required")

    # Harder penalties for real mismatches
    score -= 2.5 * len(mandatory_missing)
    score -= 3.0 * len(modern_required_missing)
    score -= 1.5 * len(modern_preferred_missing)

    if is_lead_like:
        score -= 12.0

    max_years = None
    if isinstance(years_required, tuple):
        max_years = years_required[1]
    elif isinstance(years_required, int):
        max_years = years_required

    if max_years is not None:
        if max_years >= 7:
            score -= 5.0
        elif max_years >= 5:
            score -= 3.0
        elif max_years >= 4:
            score -= 1.5
    if total > 0:
        score = score / total * 10
        
        
    
    return score, matched, total, missing
