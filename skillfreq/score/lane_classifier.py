from __future__ import annotations

from typing import Any, Dict


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def classify_role_lane(row: Dict[str, Any]) -> str:
    """
    Returns one of:
    - target_lane
    - adjacent_lane
    - wrong_lane
    """

    title = _safe_text(row.get("title", ""))
    desc = _safe_text(row.get("description", ""))
    text = f"{title} {desc}"

    hard_wrong_title_terms = [
        "qa engineer",
        "quality assurance",
        "automation tester",
        "test engineer",
        "frontend engineer",
        "frontend developer",
        "ui engineer",
        "ui developer",
        "full stack engineer",
        "full stack developer",
        "data scientist",
        "applied scientist",
        "ml engineer",
        "machine learning engineer",
        "ai engineer",
        "ai automation analyst",
        "associate consultant",
        "implementation consultant",
        "consultant",
        "cloud infrastructure engineer",
    ]

    if _contains_any(title, hard_wrong_title_terms):
        return "wrong_lane"

    strong_target_title_terms = [
        "data engineer",
        "etl engineer",
        "elt engineer",
        "data integration engineer",
        "integration engineer",
        "data warehouse engineer",
        "data systems engineer",
        "sql developer",
        "data developer",
    ]

    adjacent_title_terms = [
        "backend engineer",
        "backend developer",
        "software engineer",
        "software developer",
        "python engineer",
        "data platform engineer",
        "platform engineer",
        "application engineer",
        "analytics engineer",
        "bi engineer",
        "business intelligence engineer",
        "cloud data engineer",
        "pl/sql developer",
    ]

    core_data_signals = [
        "etl",
        "elt",
        "data pipeline",
        "data pipelines",
        "data ingestion",
        "data integration",
        "data quality",
        "validation",
        "reconciliation",
        "data transformation",
        "data warehouse",
        "data modeling",
        "source to target",
        "stored procedures",
        "xml",
        "json",
        "api",
        "rest",
        "oracle pl/sql",
        "production support",
        "root cause",
    ]

    backend_data_signals = [
        "fastapi",
        "flask",
        "postgresql",
        "sqlalchemy",
        "microservices",
        "batch data processing",
        "real-time and batch data processing",
        "csv parsing",
        "xml processing",
        "message brokers",
        "distributed task processing",
        "pytest",
        "docker",
    ]

    support_signals = [
        "sql",
        "python",
        "git",
        "query optimization",
        "pl/sql",
    ]

    analytics_terms = [
        "dashboard",
        "dashboards",
        "tableau",
        "power bi",
        "quicksight",
        "looker",
        "business intelligence",
        "obiee",
        "olap",
        "semantic layer",
        "ad hoc reporting",
        "reporting and analysis",
        "executive reporting",
        "dbt",
        "snowflake",
        "facts",
        "dimensions",
        "scd",
        "snapshots",
    ]

    wrong_desc_terms = [
        "selenium",
        "robot framework",
        "bdd frameworks",
        "functional testing",
        "regression testing",
        "prompt engineering",
        "langchain",
        "openai api",
        "anthropic api",
        "ai agents",
        "forecasting models",
        "predictive analytics",
        "statistical modeling",
        "machine learning",
        "deep learning",
        "nlp",
        "scada",
        "wastewater",
        "sewer",
        "gis",
        "arcgis",
        "aveva pi",
        "pi system",
    ]

    platform_heavy_terms = [
        "azure data factory",
        "databricks",
        "bigquery",
        "dataflow",
        "dataproc",
        "kubernetes",
        "terraform",
        "cloud infrastructure",
        "infrastructure-as-code",
        "cloudwatch",
        "ansible",
        "helm",
        "serverless",
        "observability",
        "monitoring and alerting",
        "high availability",
        "capacity planning",
        "database administration",
        "dba",
        "redshift",
        "glue",
        "emr",
        "kinesis",
        "lambda",
    ]

    low_signal_terms = [
        "no prior experience required",
        "training provided",
        "willing to relocate",
        "fresh graduates",
        "associate data engineer program",
        "passion for data",
        "eager to learn",
        "entry level",
        "recent graduates",
        "technical recruiter",
        "someone in your network",
    ]

    strong_target_title = _contains_any(title, strong_target_title_terms)
    adjacent_title = _contains_any(title, adjacent_title_terms)

    core_data_count = _count_hits(text, core_data_signals)
    backend_data_count = _count_hits(text, backend_data_signals)
    support_count = _count_hits(text, support_signals)
    analytics_count = _count_hits(text, analytics_terms)
    wrong_desc_count = _count_hits(desc, wrong_desc_terms)
    platform_heavy_count = _count_hits(text, platform_heavy_terms)
    low_signal_count = _count_hits(text, low_signal_terms)

    if wrong_desc_count >= 2 and core_data_count == 0 and backend_data_count == 0:
        return "wrong_lane"

    if low_signal_count >= 2 and not strong_target_title:
        return "wrong_lane"

    if _contains_any(title, ["business intelligence engineer", "bi engineer", "analytics engineer"]):
        return "adjacent_lane"

    if strong_target_title:
        if core_data_count >= 2:
            return "target_lane"
        if core_data_count >= 1 and support_count >= 2:
            return "target_lane"

    if adjacent_title:
        if (
            analytics_count == 0
            and platform_heavy_count <= 2
            and (
                (core_data_count >= 3 and support_count >= 2)
                or (backend_data_count >= 3 and support_count >= 1)
            )
        ):
            return "target_lane"
        return "adjacent_lane"

    if (
        core_data_count >= 3
        and support_count >= 2
        and analytics_count == 0
        and platform_heavy_count <= 2
    ):
        return "target_lane"

    if core_data_count >= 1 or backend_data_count >= 1 or support_count >= 2:
        return "adjacent_lane"

    return "wrong_lane"