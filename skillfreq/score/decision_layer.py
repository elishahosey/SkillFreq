from __future__ import annotations

from .lane_classifier import classify_role_lane
from typing import Any, Dict


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
    Converts raw weighted overlap into a more honest fit assessment.

    Returns one of:
    - good_fit
    - possible_fit
    - weak_fit
    """

    title = _safe_text(row.get("title", ""))
    desc = _safe_text(row.get("description", ""))
    reason_codes_raw = _safe_text(row.get("reason_codes", ""))
    raw_match = _safe_text(row.get("raw_match", row.get("label", "")))

    score = float(row.get("score", 0) or 0)
    matched = int(row.get("matched", 0) or 0)
    required_total = int(row.get("required_total", 0) or 0)
    missing = _safe_text(row.get("missing", ""))

    reason_codes = {code.strip() for code in reason_codes_raw.split(";") if code.strip()}
    full_text = f"{title} {desc}"

    # -----------------------------
    # Hard wrong-lane skips
    # -----------------------------
    wrong_lane_title_terms = [
        "qa engineer",
        "quality assurance",
        "automation tester",
        "test engineer",
        "application qa",
        "full stack developer",
        "full stack engineer",
        "frontend developer",
        "frontend engineer",
        "ui developer",
        "ui engineer",
        "aem engineer",
        "data analyst",
        "business analyst",
        "reporting analyst",
        "ai automation analyst",
        "data scientist",
        "applied scientist",
        "ml engineer",
        "machine learning engineer",
    ]

    wrong_lane_desc_terms = [
        "selenium",
        "robot framework",
        "test automation strategy",
        "automation frameworks",
        "bdd frameworks",
        "functional testing",
        "regression testing",
        "quality assurance and testing",
        "adobe experience platform",
        "aem",
        "touch ui",
        "classic ui",
        "langchain",
        "prompt engineering",
        "openai api",
        "anthropic api",
        "build and deploy reusable ai agents",
        "dashboards to track key business metrics",
        "forecasting models",
        "power bi required",
        "looker dashboard development required",
        "tableau required",
        "wastewater",
        "sewer",
        "scada",
        "gis tools",
        "arcgis",
        "aveva pi",
        "pi system",
        "lookml",
        "executive reporting",
        "self-service analytics platform",
    ]

    if _contains_any(title, wrong_lane_title_terms):
        return "weak_fit"

    if _contains_any(desc, wrong_lane_desc_terms):
        return "weak_fit"

    # -----------------------------
    # Signal groups
    # -----------------------------
    de_terms = [
        "data pipeline",
        "data pipelines",
        "etl",
        "elt",
        "ingestion",
        "data ingestion",
        "transformation",
        "data integration",
        "data quality",
        "validation",
        "reconciliation",
        "medallion",
        "bronze",
        "silver",
        "gold",
        "structured and semi-structured",
        "semi-structured",
        "curated datasets",
        "data warehouse",
        "warehousing",
        "source to target",
        "pipeline performance",
    ]

    backend_data_terms = [
        "fastapi",
        "flask",
        "postgresql",
        "sqlalchemy",
        "rest api",
        "microservices",
        "data processing",
        "csv parsing",
        "xml processing",
        "batch data processing",
        "real-time and batch data processing",
        "alembic",
        "pytest",
        "redis",
        "message brokers",
        "task queues",
        "jwt",
        "docker",
    ]

    analyst_terms = [
        "dashboard",
        "dashboards",
        "power bi",
        "tableau",
        "looker",
        "reporting",
        "visualization",
        "visualisation",
        "business insights",
        "ad hoc reports",
        "executive summary",
        "forecast analysis",
        "forecasting accuracy",
        "operational teams",
        "business-friendly insights",
        "present findings",
    ]

    scientist_terms = [
        "data scientist",
        "applied scientist",
        "machine learning",
        "deep learning",
        "forecasting",
        "pricing models",
        "predictive",
        "optimization",
        "statistical analysis",
        "predictive analytics",
        "ai agents",
        "prompt engineering",
        "langchain",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "nlp",
        "classification",
        "regression",
        "ml engineer",
        "machine learning engineer",
    ]

    platform_heavy_terms = [
        "snowflake administration",
        "terraform",
        "fivetran",
        "airbyte",
        "dbt",
        "lakehouse",
        "databricks",
        "azure data factory",
        "redshift",
        "glue",
        "emr",
        "kinesis",
        "lambda",
        "mwaa",
        "gcp composer",
        "dataflow",
        "dataproc",
        "bigquery",
        "cloud functions",
        "cloud run",
        "infra-as-code",
        "infrastructure-as-code",
        "observability",
        "monitoring and alerting",
        "rbac",
    ]

    de_hits = _count_hits(full_text, de_terms)
    backend_data_hits = _count_hits(full_text, backend_data_terms)
    analyst_hits = _count_hits(full_text, analyst_terms)
    scientist_hits = _count_hits(full_text, scientist_terms)
    platform_heavy_hits = _count_hits(full_text, platform_heavy_terms)

    entry_friendly_terms = [
        "no prior experience required",
        "0-2 years",
        "1-3 years",
        "junior",
        "with guidance from senior engineers",
        "relevant internship/project experience",
        "willingness to learn",
        "eagerness to learn",
        "entry level",
        "training",
        "academy",
    ]
    entry_friendly = _contains_any(desc, entry_friendly_terms)

    # -----------------------------
    # Tiny-signal false positives
    # -----------------------------
    if matched <= 2 or required_total <= 2:
        return "weak_fit"

    # -----------------------------
    # Soft red-flag accumulation
    # -----------------------------
    weak_signals = 0

    # Modern stack gaps should not dominate unless the role is clearly platform-heavy
    modern_penalty = 0
    if "modern_required_missing" in reason_codes:
        modern_penalty += 1
    if "modern_preferred_missing" in reason_codes:
        modern_penalty += 1
    if modern_penalty >= 2 and platform_heavy_hits >= 3:
        weak_signals += 1

    if "years_present" in reason_codes and not entry_friendly:
        weak_signals += 1

    # lead_like is soft, not fatal
    if "lead_like" in reason_codes and not entry_friendly:
        weak_signals += 1

    # Scientist / AI-heavy roles should drop if they are not clearly DE-shaped
    if scientist_hits >= 2 and de_hits == 0 and backend_data_hits == 0:
        weak_signals += 2
    elif scientist_hits >= 2 and not entry_friendly:
        weak_signals += 1

    if "ai_ml" in missing:
        weak_signals += 1

    # Only weak-fit if there are multiple problems AND overall signal is weak
    if weak_signals >= 2 and (matched < 5 and score < 15):
        return "weak_fit"

    # -----------------------------
    # Strong fit conditions
    # -----------------------------
    if (
        score >= 22
        and matched >= 6
        and scientist_hits == 0
        and analyst_hits <= 2
        and platform_heavy_hits <= 3
        and weak_signals <= 1
        and (
            de_hits >= 3
            or backend_data_hits >= 3
            or (entry_friendly and (de_hits >= 2 or backend_data_hits >= 2))
        )
    ):
        return "good_fit"

    # -----------------------------
    # Viable but mixed
    # -----------------------------
    if matched >= 5 and score >= 15:
        return "possible_fit"

    if matched >= 4 and (de_hits >= 2 or backend_data_hits >= 2):
        return "possible_fit"

    if raw_match in {"high match", "moderate match", "low match"} and matched >= 4:
        return "possible_fit"

    if matched >= 4:
        return "possible_fit"

    return "weak_fit"


def decide_apply_bucket(row: Dict[str, Any]) -> str:
    """
    Final decision layer:
    - lane first
    - then fit quality
    - then light threshold check for possible fits
    """

    fit_quality = derive_fit_quality(row)
    lane = classify_role_lane(row)

    matched = int(row.get("matched", 0) or 0)
    required_total = int(row.get("required_total", 0) or 0)

    # Hard stop
    if fit_quality == "weak_fit":
        return "skip"

    if lane == "wrong_lane":
        return "skip"

    if lane == "target_lane":
        if fit_quality == "good_fit":
            return "apply_now"

        if fit_quality == "possible_fit":
            if required_total > 0 and matched >= (required_total * 0.5):
                return "apply_now"
            return "manual_review"

        return "skip"

    # adjacent_lane: keep survivable, but do not auto-apply
    if lane == "adjacent_lane":
        if fit_quality == "good_fit":
            return "manual_review"

        if fit_quality == "possible_fit":
            return "manual_review"

        return "skip"

    return "skip"