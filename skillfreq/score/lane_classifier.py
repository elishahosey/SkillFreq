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

    # -----------------------------
    # Hard wrong-lane titles
    # -----------------------------
    hard_wrong_title_terms = [
        "qa engineer",
        "quality assurance",
        "automation tester",
        "test engineer",
        "application qa",
        "frontend engineer",
        "frontend developer",
        "ui engineer",
        "ui developer",
        "full stack engineer",
        "full stack developer",
        "aem engineer",
        "data analyst",
        "business analyst",
        "reporting analyst",
        "data scientist",
        "applied scientist",
        "ml engineer",
        "machine learning engineer",
        "ai engineer",
        "ai automation analyst",
        "consultant",
        "associate consultant",
        "cloud infrastructure engineer",
    ]

    if _contains_any(title, hard_wrong_title_terms):
        return "wrong_lane"

    # -----------------------------
    # Title buckets
    # -----------------------------
    strong_target_title_terms = [
        "data engineer",
        "etl engineer",
        "elt engineer",
        "data integration engineer",
        "integration engineer",
        "data warehouse engineer",
        "analytics engineer",
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
        "bi engineer",
        "business intelligence engineer",
        "cloud data engineer",
        "pl/sql developer",
    ]

    senior_platform_title_terms = [
        "data platform engineer",
        "cloud data engineer",
        "platform engineer",
        "pl/sql developer",
    ]

    # -----------------------------
    # Description signals
    # -----------------------------
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
        "record processing",
        "xml",
        "json",
    ]

    backend_data_signals = [
        "fastapi",
        "flask",
        "postgresql",
        "sqlalchemy",
        "rest api",
        "microservices",
        "batch data processing",
        "real-time and batch data processing",
        "csv parsing",
        "xml processing",
        "message brokers",
        "distributed task processing",
        "redis",
        "alembic",
        "pytest",
        "docker",
    ]

    support_signals = [
        "sql",
        "python",
        "git",
        "query optimization",
        "snowflake",
        "oracle pl/sql",
        "pl/sql",
    ]

    wrong_desc_terms = [
        "selenium",
        "robot framework",
        "bdd frameworks",
        "functional testing",
        "regression testing",
        "adobe experience platform",
        "touch ui",
        "classic ui",
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
        "power bi",
        "tableau",
        "looker",
        "dashboard development",
        "executive reporting",
        "self-service analytics",
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
        "iac",
        "observability",
        "monitoring and alerting",
        "high availability",
        "capacity planning",
        "backup and recovery",
        "database administration",
        "dba",
        "sql server environments",
        "data lake",
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
    ]

    strong_target_title = _contains_any(title, strong_target_title_terms)
    adjacent_title = _contains_any(title, adjacent_title_terms)

    core_data_count = _count_hits(text, core_data_signals)
    backend_data_count = _count_hits(text, backend_data_signals)
    support_count = _count_hits(text, support_signals)
    wrong_desc_count = _count_hits(desc, wrong_desc_terms)
    platform_heavy_count = _count_hits(text, platform_heavy_terms)

    # -----------------------------
    # Hard wrong-lane descriptions
    # -----------------------------
    if wrong_desc_count >= 2 and core_data_count == 0 and backend_data_count == 0:
        return "wrong_lane"

    # -----------------------------
    # Platform / DBA / cloud drift guard
    # -----------------------------
    if _contains_any(title, senior_platform_title_terms):
        if platform_heavy_count >= 2 or wrong_desc_count >= 1:
            return "adjacent_lane"

    # -----------------------------
    # Strong target detection
    # -----------------------------
    is_strong_target = False

    # Real DE/integration/data titles should have an easier path
    if strong_target_title and (core_data_count >= 2 or backend_data_count >= 2):
        is_strong_target = True

    elif strong_target_title and core_data_count >= 1:
        is_strong_target = True

    elif strong_target_title and support_count >= 2:
        is_strong_target = True

    # Backend/software-ish titles can still become target if clearly data/backend shaped
    elif adjacent_title and (
        (core_data_count >= 2 and support_count >= 2)
        or (backend_data_count >= 3 and support_count >= 1)
    ):
        if wrong_desc_count == 0 and platform_heavy_count <= 2:
            is_strong_target = True

    # Description-only target catch
    elif core_data_count >= 3 and support_count >= 2 and wrong_desc_count == 0 and platform_heavy_count <= 2:
        is_strong_target = True

    elif backend_data_count >= 3 and support_count >= 2 and wrong_desc_count == 0:
        is_strong_target = True

    # -----------------------------
    # Low-signal downrank
    # -----------------------------
    if is_strong_target and _contains_any(desc, low_signal_terms):
        return "adjacent_lane"

    # -----------------------------
    # Final target decision
    # -----------------------------
    if is_strong_target:
        return "target_lane"

    # -----------------------------
    # Adjacent lane
    # -----------------------------
    if adjacent_title:
        return "adjacent_lane"

    if core_data_count >= 1 or backend_data_count >= 1 or support_count >= 2:
        return "adjacent_lane"

    return "wrong_lane"