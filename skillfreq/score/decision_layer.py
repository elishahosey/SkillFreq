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

    reason_codes = {code.strip() for code in reason_codes_raw.split(";") if code.strip()}
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
        "apis",
        "rest",
        "soap",
        "sftp",
        "oracle pl/sql",
        "pl/sql",
        "stored procedures",
        "production support",
        "root cause",
        "troubleshooting",
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

    bridge_terms = [
        "systems analyst",
        "application support",
        "production support",
        "technical support",
        "troubleshooting",
        "root cause",
        "incident",
        "ticket",
        "tickets",
        "sql",
        "queries",
        "stored procedures",
        "data validation",
        "data quality",
        "reconciliation",
        "reporting",
        "reports",
        "dashboard",
        "dashboards",
        "power bi",
        "tableau",
        "api",
        "apis",
        "xml",
        "json",
        "sftp",
        "integration",
        "integrations",
        "interface",
        "interfaces",
        "data operations",
        "data integrity",
        "client data",
        "client systems",
        "client integrations",
        "requirements gathering",
        "data mapping",
        "mapping documents",
        "technical configuration",
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
        "database administration",
        "dba",
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

    low_signal_or_training_terms = [
        "associate data engineer role",
        "fresh graduates",
        "recent graduates",
        "training provided",
        "willing to relocate",
        "passion for data",
        "eager to learn",
        "someone in your network",
        "technical recruiter",
    ]

    consultant_terms = [
        "consultant",
        "technical consultant",
        "data consultant",
        "sql consultant",
        "integration consultant",
        "interface consultant",
        "api consultant",
        "application consultant",
        "reporting consultant",
        "data quality consultant",
        "data integration consultant",
        "business intelligence consultant",
        "bi consultant",
        "implementation consultant",
    ]

    bad_consultant_terms = [
        "configuration consultant",
        "functional consultant",
        "business process consultant",
        "customer success consultant",
        "training consultant",
        "erp consultant",
        "salesforce consultant",
        "workday consultant",
        "sap consultant",
        "peoplesoft consultant",
        "servicenow consultant",
    ]

    target_hits = _count_hits(full_text, target_terms)
    backend_hits = _count_hits(full_text, backend_data_terms)
    bridge_hits = _count_hits(full_text, bridge_terms)
    analytics_hits = _count_hits(full_text, analytics_terms)
    platform_hits = _count_hits(full_text, platform_heavy_terms)
    leadership_hits = _count_hits(full_text, leadership_terms)
    low_signal_hits = _count_hits(full_text, low_signal_or_training_terms)
    consultant_hits = _count_hits(title, consultant_terms)
    bad_consultant_hits = _count_hits(title, bad_consultant_terms)

    resume_unsupported_gap = _has_resume_unsupported_central_gap(full_text)

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
        and "oracle pl/sql" not in full_text
    )

    if hard_missing:
        return "weak_fit"

    if low_signal_hits >= 1 and target_hits <= 5:
        return "weak_fit"

    # Consultant roles are allowed only when they behave like SQL/data/integration/support bridge roles.
    # They should not become good_fit/apply_now.
    if consultant_hits >= 1:
        strong_consultant_overlap = (
            matched >= 4
            and bridge_hits >= 5
            and support_like_overlap(full_text)
            and platform_hits <= 3
        )

        very_strong_bad_consultant_exception = (
            bad_consultant_hits >= 1
            and matched >= 5
            and bridge_hits >= 7
            and target_hits >= 3
            and platform_hits <= 2
            and support_like_overlap(full_text)
        )

        if bad_consultant_hits >= 1 and not very_strong_bad_consultant_exception:
            return "weak_fit"

        if lane == "bridge_lane" and strong_consultant_overlap:
            return "possible_fit"

        if target_hits >= 4 and matched >= 4 and platform_hits <= 2:
            return "possible_fit"

        return "weak_fit"

    if lead_like or overleveled_years:
        if target_hits >= 5 and analytics_hits == 0 and platform_hits <= 1:
            return "possible_fit"
        return "weak_fit"

    if central_analytics_mismatch or central_platform_mismatch or central_bi_stack_gap:
        if lane == "target_lane" and target_hits >= 5 and matched >= 5:
            return "possible_fit"
        if lane == "bridge_lane" and bridge_hits >= 6 and matched >= 5 and platform_hits <= 2:
            return "possible_fit"
        return "weak_fit"

    if lane == "target_lane":
        if (
            score >= 28
            and matched >= 5
            and target_hits >= 5
            and analytics_hits <= 2
            and platform_hits <= 2
            and not resume_unsupported_gap
        ):
            return "good_fit"

        if matched >= 4 and (target_hits >= 3 or backend_hits >= 2):
            return "possible_fit"

    if lane == "secondary_lane":
        if matched >= 4 and (target_hits >= 3 or backend_hits >= 2):
            return "possible_fit"
        return "weak_fit"

    if lane == "bridge_lane":
        # Bridge can be a useful survival lane, but it should not be treated as core-fit.
        # Require several practical overlap signals so generic support/reporting does not sneak in.
        if matched >= 4 and bridge_hits >= 5 and (target_hits >= 2 or backend_hits >= 1):
            return "possible_fit"
        if matched >= 5 and bridge_hits >= 6:
            return "possible_fit"
        return "weak_fit"

    if matched >= 4:
        return "possible_fit"

    return "weak_fit"


def support_like_overlap(text: str) -> bool:
    """
    Consultant roles need practical overlap, not just vague client-facing language.
    This keeps implementation/configuration consulting from sneaking in unless the JD has real SQL/data/support signals.
    """

    support_like_terms = [
        "sql",
        "queries",
        "stored procedure",
        "stored procedures",
        "data validation",
        "data quality",
        "reconciliation",
        "api",
        "apis",
        "integration",
        "integrations",
        "interface",
        "interfaces",
        "xml",
        "json",
        "sftp",
        "production support",
        "application support",
        "troubleshooting",
        "root cause",
        "incident",
        "logs",
        "log analysis",
        "data mapping",
    ]

    return _count_hits(text, support_like_terms) >= 3


def _is_resume_grounded_target(full_text: str) -> bool:
    """
    apply_now should require evidence that the JD overlaps with skills actually supported
    by the base resumes: SQL, Python, ETL/data integration, validation, APIs, XML/JSON,
    SFTP, production support, logs/OpenSearch, CI/CD/Azure DevOps, Postman/SoapUI.
    """

    resume_supported_terms = [
        "sql",
        "sql server",
        "query optimization",
        "stored procedure",
        "stored procedures",
        "python",
        "java",
        "etl",
        "elt",
        "data pipeline",
        "data pipelines",
        "data integration",
        "integration",
        "integrations",
        "interface",
        "interfaces",
        "data quality",
        "validation",
        "reconciliation",
        "data transformation",
        "data warehouse",
        "data modeling",
        "api",
        "apis",
        "rest",
        "soap",
        "xml",
        "json",
        "http",
        "https",
        "sftp",
        "winscp",
        "postman",
        "soapui",
        "production support",
        "root cause",
        "troubleshooting",
        "logs",
        "log analysis",
        "opensearch",
        "azure devops",
        "ci/cd",
        "jira",
        "git",
    ]

    return _count_hits(full_text, resume_supported_terms) >= 5


def _has_resume_unsupported_central_gap(full_text: str) -> bool:
    """
    Block good_fit/apply_now when the JD appears centered on tools/ecosystems that are
    not strongly supported by the base resumes.

    These can still be manual_review if the role has enough SQL/data/integration overlap.
    """

    hard_ecosystem_gap_terms = [
        "salesforce",
        "workday",
        "sap",
        "peoplesoft",
        "servicenow",
        "palantir",
        "cerner",
        "epic",
        "mulesoft",
        "boomi",
        "informatica",
        "iics",
        "talend",
        "obiee",
        "olap",
    ]

    cloud_platform_gap_terms = [
        "databricks",
        "snowflake",
        "redshift",
        "bigquery",
        "aws glue",
        "glue",
        "emr",
        "kinesis",
        "lambda",
        "terraform",
        "kubernetes",
        "docker",
        "gcp",
        "azure data factory",
        "dataflow",
        "dataproc",
        "lakehouse",
        "cloud infrastructure",
        "infrastructure-as-code",
    ]

    analytics_ownership_gap_terms = [
        "power bi",
        "tableau",
        "looker",
        "quicksight",
        "dashboard ownership",
        "dashboard development",
        "semantic layer",
        "executive reporting",
    ]

    ml_ai_gap_terms = [
        "machine learning",
        "deep learning",
        "predictive modeling",
        "predictive analytics",
        "statistical modeling",
        "nlp",
        "llm",
        "rag",
        "langchain",
        "ai agents",
    ]

    hard_gap_count = _count_hits(full_text, hard_ecosystem_gap_terms)
    cloud_gap_count = _count_hits(full_text, cloud_platform_gap_terms)
    analytics_gap_count = _count_hits(full_text, analytics_ownership_gap_terms)
    ml_ai_gap_count = _count_hits(full_text, ml_ai_gap_terms)

    # One hard ecosystem term is enough to prevent clean apply_now.
    if hard_gap_count >= 1:
        return True

    # Multiple central platform/cloud terms indicate the role is probably not resume-grounded.
    if cloud_gap_count >= 2:
        return True

    # Analytics tools are acceptable when light, but not when several appear together.
    if analytics_gap_count >= 2:
        return True

    # ML/AI-centered roles are not resume-grounded for the current search.
    if ml_ai_gap_count >= 1:
        return True

    return False


def _is_clean_apply_now_title(title: str) -> bool:
    """
    apply_now should be a clean-shot bucket.
    Risky or ambiguous titles should be capped at manual_review even when keyword score is high.
    """

    clean_apply_now_title_terms = [
        "data engineer",
        "etl engineer",
        "elt engineer",
        "etl developer",
        "data integration engineer",
        "integration engineer",
        "data pipeline engineer",
        "data ingestion engineer",
        "data quality engineer",
        "data warehouse engineer",
        "sql developer",
        "database developer",
    ]

    risky_apply_now_title_terms = [
        "customer engineer",
        "solutions engineer",
        "solution engineer",
        "sales engineer",
        "forward deployed engineer",
        "security engineer",
        "detection engineer",
        "detection engineering",
        "etl tester",
        "test analyst",
        "qa engineer",
        "quality assurance",
        "consultant",
        "analyst",
        "support",
        "platform engineer",
        "software engineer",
        "backend engineer",
        "application engineer",
        "business intelligence",
        "bi engineer",
        "analytics engineer",
    ]

    if _contains_any(title, risky_apply_now_title_terms):
        return False

    return _contains_any(title, clean_apply_now_title_terms)


def decide_apply_bucket(row: Dict[str, Any]) -> str:
    """
    Final decision layer:
    - weak fit => skip
    - wrong lane => skip
    - target + good + clean title + resume-grounded overlap => apply_now
    - target + possible => manual_review
    - secondary => manual_review at best
    - bridge => manual_review at best
    - bridge-search jobs => manual_review at best
    """

    fit_quality = derive_fit_quality(row)
    lane = classify_role_lane(row)

    title = _safe_text(row.get("title", ""))
    desc = _safe_text(row.get("description", ""))
    full_text = f"{title} {desc}"
    search_lane = _safe_text(row.get("search_lane", ""))
    reason_codes_raw = _safe_text(row.get("reason_codes", ""))
    reason_codes = {code.strip() for code in reason_codes_raw.split(";") if code.strip()}

    if fit_quality == "weak_fit":
        return "skip"

    if lane == "wrong_lane":
        return "skip"
    
    if search_lane in {"survival", "contract_survival"} or lane == "survival_lane":
        return "manual_review"

    # Bridge searches are noisy. Even when a bridge-search result looks strong,
    # keep it in manual_review so it does not pollute the clean-shot apply_now bucket.
    if search_lane in {"bridge", "contract_bridge"}:
        return "manual_review"

    # These reason codes mean the role may still be worth reviewing,
    # but it should not be auto-promoted into apply_now.
    apply_now_blocking_reasons = {
        "core_required_missing",
        "modern_required_missing",
        "lead_like",
    }

    if lane == "target_lane":
        if fit_quality == "good_fit":
            if reason_codes.intersection(apply_now_blocking_reasons):
                return "manual_review"

            if not _is_clean_apply_now_title(title):
                return "manual_review"

            if not _is_resume_grounded_target(full_text):
                return "manual_review"

            if _has_resume_unsupported_central_gap(full_text):
                return "manual_review"

            return "apply_now"

        return "manual_review"

    if lane in {"secondary_lane", "bridge_lane"}:
        return "manual_review"

    return "skip"
