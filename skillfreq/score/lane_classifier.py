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
    - target_lane: core DE / ETL / SQL / integration roles
    - secondary_lane: adjacent SWE/data/platform-flavored roles that can still preserve mobility
    - bridge_lane: survival/bridge roles where SQL, integrations, APIs, support, reporting, consulting, or troubleshooting are central enough to be useful
    - wrong_lane: roles that are too far away, too senior, too platform/admin-heavy, too ML/AI-heavy, or too implementation/configuration-heavy
    """

    title = _safe_text(row.get("title", ""))
    desc = _safe_text(row.get("description", ""))
    search_lane = _safe_text(row.get("search_lane", ""))
    text = f"{title} {desc}"

    hard_wrong_title_terms = [
        "qa engineer",
        "quality assurance",
        "automation tester",
        "test engineer",
        "test analyst",
        "etl tester",
        "frontend engineer",
        "frontend developer",
        "ui engineer",
        "ui developer",
        "full stack engineer",
        "full stack developer",
        ".net full stack",
        "data scientist",
        "applied scientist",
        "ml engineer",
        "machine learning engineer",
        "ai engineer",
        "ai automation analyst",
        "cloud infrastructure engineer",
        "security engineer",
        "detection engineer",
        "detection engineering",
        "customer engineer",
        "solutions engineer",
        "solution engineer",
        "sales engineer",
        "forward deployed engineer",
        "data center technician",
        "hardware engineer",
        "iam engineer",
        "identity access",
        "identity and access",
        "quality engineer",
        "validation engineer",
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
        "data pipeline engineer",
        "data ingestion engineer",
        "data quality engineer",
    ]

    secondary_title_terms = [
        "backend engineer",
        "backend developer",
        "software engineer",
        "software developer",
        "python engineer",
        "python developer",
        "java engineer",
        "java developer",
        "data platform engineer",
        "platform engineer",
        "application engineer",
        "analytics engineer",
        "bi engineer",
        "business intelligence engineer",
        "cloud data engineer",
        "pl/sql developer",
        "database engineer",
        "systems engineer",
        "enterprise systems engineer",
        "site reliability engineer",
        "sre",
        "devops engineer",
    ]

    bridge_title_terms = [
        "systems analyst",
        "system analyst",
        "application analyst",
        "business systems analyst",
        "technical systems analyst",
        "production support analyst",
        "production support engineer",
        "application support analyst",
        "application support engineer",
        "software support analyst",
        "software support engineer",
        "technical support engineer",
        "technical support analyst",
        "sql analyst",
        "data analyst",
        "data quality analyst",
        "data operations analyst",
        "data integrity analyst",
        "reporting analyst",
        "integration analyst",
        "interface analyst",
        "api support engineer",
        "etl support analyst",
        "database analyst",
    ]

    consultant_title_terms = [
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

    bad_consultant_title_terms = [
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

    # These titles may contain useful SQL/API/data words, but their role identity is not core data/ETL.
    # They should never become target_lane. At best, they become secondary_lane or bridge_lane.
    non_target_title_terms = [
        "software engineer",
        "software developer",
        "python developer",
        "python engineer",
        "java developer",
        "java engineer",
        "backend engineer",
        "backend developer",
        "backend programmer",
        "application engineer",
        "systems engineer",
        "enterprise systems engineer",
        "atlassian developer",
        "jira developer",
        ".net developer",
        "c# developer",
        "devops engineer",
        "site reliability engineer",
        "sre",
        "platform engineer",
        "cloud engineer",
        "administrator",
        "admin",
        "developer",
        "programmer",
        "technician",
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
        "apis",
        "rest",
        "soap",
        "sftp",
        "file transfer",
        "oracle pl/sql",
        "pl/sql",
        "production support",
        "root cause",
        "troubleshooting",
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
        "stored procedure",
        "stored procedures",
        "logs",
        "logging",
        "incident",
        "root cause analysis",
        "production issue",
        "ticket",
        "tickets",
    ]

    bridge_positive_signals = [
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
        "rest",
        "xml",
        "json",
        "sftp",
        "integration",
        "integrations",
        "interface",
        "interfaces",
        "production support",
        "application support",
        "technical support",
        "troubleshooting",
        "root cause",
        "incident",
        "log analysis",
        "data operations",
        "data integrity",
        "operational workflows",
        "client data",
        "client systems",
        "client integrations",
        "requirements gathering",
        "data mapping",
        "mapping documents",
        "technical configuration",
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

    platform_admin_title_terms = [
        "database administrator",
        "sql server administrator",
        "dba",
        "cloud support engineer",
        "cloud engineer",
        "infrastructure engineer",
        "systems administrator",
        "network administrator",
        "mft administrator",
        "managed file transfer",
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
    secondary_title = _contains_any(title, secondary_title_terms)
    bridge_title = _contains_any(title, bridge_title_terms)
    consultant_title = _contains_any(title, consultant_title_terms)
    bad_consultant_title = _contains_any(title, bad_consultant_title_terms)
    non_target_title = _contains_any(title, non_target_title_terms)

    core_data_count = _count_hits(text, core_data_signals)
    backend_data_count = _count_hits(text, backend_data_signals)
    support_count = _count_hits(text, support_signals)
    bridge_count = _count_hits(text, bridge_positive_signals)
    analytics_count = _count_hits(text, analytics_terms)
    wrong_desc_count = _count_hits(desc, wrong_desc_terms)
    platform_heavy_count = _count_hits(text, platform_heavy_terms)
    low_signal_count = _count_hits(text, low_signal_terms)

    if _contains_any(title, platform_admin_title_terms):
        if bridge_count < 4 or core_data_count < 2:
            return "wrong_lane"

    if wrong_desc_count >= 2 and core_data_count == 0 and backend_data_count == 0:
        return "wrong_lane"

    if low_signal_count >= 2 and not strong_target_title:
        return "wrong_lane"

    # Consultant roles are allowed only as controlled bridge roles.
    # They should not become target_lane/apply_now just because they mention SQL or integration.
    if consultant_title:
        if bad_consultant_title and not (
            bridge_count >= 7
            and support_count >= 2
            and core_data_count >= 3
            and platform_heavy_count <= 2
        ):
            return "wrong_lane"

        if (
            bridge_count >= 5
            and support_count >= 2
            and platform_heavy_count <= 3
            and wrong_desc_count == 0
        ):
            return "bridge_lane"

        if (
            core_data_count >= 3
            and support_count >= 2
            and platform_heavy_count <= 2
            and wrong_desc_count == 0
        ):
            return "bridge_lane"

        return "wrong_lane"

    if _contains_any(title, ["business intelligence engineer", "bi engineer", "analytics engineer"]):
        if core_data_count >= 3 and support_count >= 2:
            return "secondary_lane"
        if bridge_count >= 4 and support_count >= 2:
            return "bridge_lane"
        return "wrong_lane"

    # Strong target titles are allowed into target_lane only when the JD has real data/ETL overlap.
    if strong_target_title:
        if core_data_count >= 2:
            return "target_lane"
        if core_data_count >= 1 and support_count >= 2:
            return "target_lane"

    # Non-target titles may still be useful, but should not become target_lane.
    # This prevents generic software/systems/platform/admin/dev titles from being over-promoted.
    if non_target_title:
        if (
            search_lane in ("bridge", "contract_bridge")
            and bridge_count >= 4
            and support_count >= 2
            and platform_heavy_count <= 3
        ):
            return "bridge_lane"

        if (
            bridge_count >= 5
            and support_count >= 2
            and platform_heavy_count <= 3
        ):
            return "bridge_lane"
        
        if(
            search_lane in ("survival", "contract_survival")
        ):
            return "survival_lane"

        if (
            platform_heavy_count <= 3
            and (
                core_data_count >= 2
                or backend_data_count >= 2
                or bridge_count >= 4
            )
        ):
            return "secondary_lane"

        return "wrong_lane"

    if secondary_title:
        if (
            analytics_count == 0
            and platform_heavy_count <= 2
            and (
                (core_data_count >= 3 and support_count >= 2)
                or (backend_data_count >= 3 and support_count >= 1)
            )
        ):
            return "secondary_lane"

        if platform_heavy_count <= 3 and (
            core_data_count >= 2
            or backend_data_count >= 2
            or bridge_count >= 4
        ):
            return "secondary_lane"

        if search_lane in ("bridge", "contract_bridge") and bridge_count >= 4 and support_count >= 2:
            return "bridge_lane"

        return "wrong_lane"

    if bridge_title:
        if bridge_count >= 4 and support_count >= 2 and platform_heavy_count <= 3:
            return "bridge_lane"
        if core_data_count >= 3 and support_count >= 2 and platform_heavy_count <= 2:
            return "secondary_lane"
        return "wrong_lane"

    if (
        core_data_count >= 3
        and support_count >= 2
        and analytics_count == 0
        and platform_heavy_count <= 2
    ):
        return "target_lane"

    if (
        search_lane in ("bridge", "contract_bridge")
        and bridge_count >= 4
        and support_count >= 2
        and platform_heavy_count <= 3
    ):
        return "bridge_lane"

    if core_data_count >= 2 or backend_data_count >= 2:
        return "secondary_lane"

    if bridge_count >= 4 and support_count >= 2:
        return "bridge_lane"

    return "wrong_lane"