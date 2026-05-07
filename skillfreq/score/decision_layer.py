from __future__ import annotations

from typing import Any, Dict

from .lane_classifier import classify_role_lane


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)


def derive_fit_quality(row: Dict[str, Any]) -> str:
    """
    Convert raw score + JD language into a realistic fit bucket.

    Returns:
    - good_fit
    - possible_fit
    - weak_fit
    """

    title = _safe_text(row.get("title", ""))
    desc = _safe_text(row.get("description", ""))
    reason_codes_raw = _safe_text(row.get("reason_codes", ""))

    score = float(row.get("score", 0) or 0)
    matched = int(row.get("matched", 0) or 0)
    required_total = int(row.get("required_total", 0) or 0)
    missing_raw = _safe_text(row.get("missing", ""))

    reason_codes = {code.strip() for code in reason_codes_raw.split(";") if code.strip()}
    missing = {item.strip() for item in missing_raw.split(";") if item.strip()}
    full_text = f"{title} {desc}"
    lane = classify_role_lane(row)

    target_terms = [
        "etl",
        "elt",
        "data pipeline",
        "data pipelines",
        "data integration",
        "ingestion",
        "transformation",
        "data quality",
        "validation",
        "reconciliation",
        "sql",
        "xml",
        "json",
        "api",
        "rest",
        "oracle pl/sql",
        "stored procedures",
        "production support",
        "root cause",
    ]

    backend_data_terms = [
        "fastapi",
        "flask",
        "postgresql",
        "sqlalchemy",
        "microservices",
        "batch data processing",
        "csv parsing",
        "xml processing",
        "message brokers",
        "distributed task processing",
        "pytest",
        "docker",
    ]

    analytics_terms = [
        "business intelligence",
        "bi engineer",
        "analytics engineer",
        "dashboard",
        "dashboards",
        "tableau",
        "power bi",
        "quicksight",
        "looker",
        "obiee",
        "olap",
        "semantic layer",
        "ad hoc reporting",
        "reporting and analysis",
        "reporting layer",
        "trusted, business-ready datasets",
        "student outcomes",
        "silver and gold",
        "dbt models",
        "dbt tests",
        "facts, dimensions",
        "facts and dimensions",
        "scd",
        "snapshots",
    ]

    platform_heavy_terms = [
        "terraform",
        "kubernetes",
        "databricks",
        "bigquery",
        "glue",
        "emr",
        "lambda",
        "kinesis",
        "redshift",
        "snowflake",
        "azure data factory",
        "lakehouse",
        "infrastructure-as-code",
        "cloud infrastructure",
    ]

    leadership_terms = [
        "mentor junior",
        "mentor other engineers",
        "evaluate and make decisions",
        "drive best practices in source teams",
        "set technical direction",
        "architecture ownership",
        "architectural decisions",
        "system design leadership",
        "staff-level",
    ]

    consulting_or_training_terms = [
        "associate data engineer role",
        "fresh graduates",
        "recent graduates",
        "training provided",
        "willing to relocate",
        "passion for data",
        "eager to learn",
        "someone in your network",
        "technical recruiter",
        "implementation consultant",
        "consulting",
    ]

    target_hits = _count_hits(full_text, target_terms)
    backend_hits = _count_hits(full_text, backend_data_terms)
    analytics_hits = _count_hits(full_text, analytics_terms)
    platform_hits = _count_hits(full_text, platform_heavy_terms)
    leadership_hits = _count_hits(full_text, leadership_terms)
    consulting_hits = _count_hits(full_text, consulting_or_training_terms)

    if lane == "wrong_lane":
        return "weak_fit"

    if matched <= 2 or required_total <= 2:
        return "weak_fit"

    hard_missing = "core_required_missing" in reason_codes
    lead_like = "lead_like" in reason_codes or leadership_hits > 0
    overleveled_years = "years_present" in reason_codes and (
        "5+ years" in full_text
        or "6+ years" in full_text
        or "7+ years" in full_text
        or "8+ years" in full_text
        or "10+ years" in full_text
        or "seven years" in full_text
    )

    central_analytics_mismatch = analytics_hits >= 3 and target_hits <= 3 and backend_hits <= 1
    central_platform_mismatch = platform_hits >= 3 and target_hits <= 2
    central_bi_stack_gap = (
        any(term in full_text for term in ["obiee", "olap", "oracle"])
        and not any(term in full_text for term in ["oracle pl/sql"])
    )

    if hard_missing:
        return "weak_fit"

    if consulting_hits >= 1 and target_hits <= 5:
        return "weak_fit"

    if lead_like or overleveled_years:
        if target_hits >= 5 and analytics_hits == 0 and platform_hits <= 1:
            return "possible_fit"
        return "weak_fit"

    if central_analytics_mismatch or central_platform_mismatch or central_bi_stack_gap:
        if lane == "target_lane" and target_hits >= 5 and matched >= 5:
            return "possible_fit"
        return "weak_fit"

    if lane == "target_lane":
        if (
            score >= 28
            and matched >= 5
            and target_hits >= 5
            and analytics_hits <= 2
            and platform_hits <= 2
        ):
            return "good_fit"

        if matched >= 4 and (target_hits >= 3 or backend_hits >= 2):
            return "possible_fit"

    if lane == "adjacent_lane":
        if matched >= 4 and (target_hits >= 3 or backend_hits >= 2):
            return "possible_fit"
        return "weak_fit"

    if matched >= 4:
        return "possible_fit"

    return "weak_fit"


def decide_apply_bucket(row: Dict[str, Any]) -> str:
    """
    Final decision layer:
    - weak fit => skip
    - wrong lane => skip
    - target + good => apply_now
    - target + possible => manual_review
    - adjacent => manual_review at best
    """

    fit_quality = derive_fit_quality(row)
    lane = classify_role_lane(row)

    if fit_quality == "weak_fit":
        return "skip"

    if lane == "wrong_lane":
        return "skip"

    if lane == "target_lane":
        if fit_quality == "good_fit":
            return "apply_now"
        return "manual_review"

    if lane == "adjacent_lane":
        return "manual_review"

    return "skip"