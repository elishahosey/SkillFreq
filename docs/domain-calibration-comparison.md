# Focused domain calibration: 90-day DB comparison

Before: `data\outputs\results-db-90-days-calibrated.csv`. After: `data\outputs\results-db-90-days-domain.csv`.
All 8,692 source identities match; no title or description changed.
Grading versions: `['809dc743062dee89']` → `['3f42ddb8add0fbd8']`.
Market taxonomy unchanged: `['31d08964f877']`. Original exports and snapshots are preserved.

## Aggregate results

| Metric | Before | After |
|---|---:|---:|
| jobs | 8692 | 8692 |
| average_fit | 31.34 | 31.32 |
| average_learning | 2.45 | 2.45 |
| nonzero_learning | 888 | 886 |
| unavailable_learning | 0 | 0 |
| ai_review_pct | 37.95 | 37.39 |
| bridge_lane | 725 | 700 |
| secondary_lane | 1475 | 1476 |
| target_lane | 255 | 266 |
| wrong_lane | 6237 | 6250 |
| apply_now | 94 | 101 |
| manual_review | 2282 | 2266 |
| skip | 6316 | 6325 |
| good_fit | 868 | 887 |
| possible_fit | 1519 | 1492 |
| weak_fit | 6305 | 6313 |

## Apply decisions by lane

| Lane | Decision | Before count (%) | After count (%) |
|---|---|---:|---:|
| bridge_lane | apply_now | 0 (0.0%) | 0 (0.0%) |
| bridge_lane | manual_review | 698 (96.28%) | 671 (95.86%) |
| bridge_lane | skip | 27 (3.72%) | 29 (4.14%) |
| secondary_lane | apply_now | 0 (0.0%) | 0 (0.0%) |
| secondary_lane | manual_review | 1438 (97.49%) | 1440 (97.56%) |
| secondary_lane | skip | 37 (2.51%) | 36 (2.44%) |
| target_lane | apply_now | 94 (36.86%) | 101 (37.97%) |
| target_lane | manual_review | 146 (57.25%) | 155 (58.27%) |
| target_lane | skip | 15 (5.88%) | 10 (3.76%) |
| wrong_lane | apply_now | 0 (0.0%) | 0 (0.0%) |
| wrong_lane | manual_review | 0 (0.0%) | 0 (0.0%) |
| wrong_lane | skip | 6237 (100.0%) | 6250 (100.0%) |

## Integration title cohort

`{"total": 34, "before_target": 13, "after_target": 5, "retained_target": 5, "new_lanes": {"target_lane": 5, "wrong_lane": 19, "secondary_lane": 5, "bridge_lane": 5}}`

Cohort membership uses the phrase “integration engineer” in the title only for reporting. Grading uses configured title patterns and description evidence.

## Integration Engineer examples

| Title / ID | Old lane | New lane | Old fit | New fit | Old decision | New decision | Main triggered policy rules |
|---|---|---|---:|---:|---|---|---|
| Application Security Integration Engineer (li-4430114690) | target_lane | wrong_lane | 86.79 | 15.0 | apply_now | skip | integration_requires_data_domain, security_domain_identity_guard, weak_fit_score, configured_hard_blocker, wrong_role_identity |
| Flight Controls Integration Engineer (li-4429969524) | target_lane | wrong_lane | 73.03 | 15.0 | manual_review | skip | integration_requires_data_domain, integration_hardware_domain_guard, hard_exclusion_override, weak_fit_score, configured_hard_blocker, wrong_role_identity |
| Windchill Integration Engineer (li-4429666992) | target_lane | secondary_lane | 88.43 | 58.43 | apply_now | skip | integration_requires_data_domain, ecosystem_identity_guard, possible_fit_score, configured_hard_blocker, ecosystem_ownership_gap |
| Integration Engineer (li-4430454590) | target_lane | target_lane | 83.3 | 86.3 | apply_now | apply_now | integration_data_evidence, supported_integration_target, bridge_eligibility, good_fit_score, strong_primary_fit |
| Data & Integration Engineer (li-4430448809) | target_lane | target_lane | 92.98 | 92.98 | apply_now | apply_now | integration_data_evidence, supported_integration_target, bridge_eligibility, good_fit_score, strong_primary_fit |
| Data Integration Engineer (in-07e05dd5a314ee99) | target_lane | target_lane | 89.99 | 89.99 | manual_review | manual_review | database_and_data_stack_evidence, integration_data_evidence, target_eligibility, supported_integration_target, good_fit_score, ambiguous_role_review |
| Robotic Systems Integration Engineer (li-4429779333) | secondary_lane | wrong_lane | 85.0 | 15.0 | manual_review | skip | backend_evidence, integration_requires_data_domain, hard_exclusion_override, weak_fit_score, configured_hard_blocker, wrong_role_identity |
| Integration Engineer or Senior Integration Engineer, Texas Institute for Electronics, Cockrell School of Engineering (li-4424947815) | target_lane | wrong_lane | 80.56 | 15.0 | manual_review | skip | integration_requires_data_domain, hard_exclusion_override, weak_fit_score, configured_hard_blocker, wrong_role_identity |
| Senior Boomi Integration Engineer -Remote (li-4429363929) | target_lane | secondary_lane | 76.88 | 77.38 | manual_review | manual_review | integration_requires_data_domain, possible_fit_score, ambiguous_role_review |
| Boomi Integration Engineer (li-4419531662) | target_lane | secondary_lane | 74.62 | 74.62 | manual_review | manual_review | bridge_eligibility, integration_requires_data_domain, possible_fit_score, configured_review_gate |

## Ecosystem examples

| Title / ID | Old lane | New lane | Old fit | New fit | Old decision | New decision | Main triggered policy rules |
|---|---|---|---:|---:|---|---|---|
| Informatica MDM Support & Data Operations Specialist (li-4429364893) | target_lane | bridge_lane | 59.0 | 59.0 | skip | skip | integration_data_evidence, target_eligibility, bridge_eligibility, ecosystem_identity_guard, possible_fit_score, configured_hard_blocker, ecosystem_ownership_gap |
| Data Engineer - Oracle PL/SQL (in-1393eac0b7e7e3be) | wrong_lane | target_lane | 15.0 | 78.75 | skip | manual_review | database_development_evidence, integration_data_evidence, target_eligibility, possible_fit_score, configured_review_gate |
| Windchill Integration Engineer (li-4429666992) | target_lane | secondary_lane | 88.43 | 58.43 | apply_now | skip | integration_requires_data_domain, ecosystem_identity_guard, possible_fit_score, configured_hard_blocker, ecosystem_ownership_gap |
| Senior SAP Cloud ALM, Integration & ABAP Engineer (li-4430986127) | bridge_lane | secondary_lane | 62.4 | 47.4 | manual_review | skip | integration_data_evidence, supported_integration_target, bridge_eligibility, ecosystem_identity_guard, weak_fit_score, configured_hard_blocker, ecosystem_ownership_gap |
| Senior Integration Boomi Engineer (li-4428703372) | secondary_lane | target_lane | 85.0 | 92.32 | manual_review | apply_now | integration_data_evidence, supported_integration_target, good_fit_score, strong_primary_fit |
| ETL Developer (3 Days in OFFICE :: W2 ONLY) (li-4428087682) | target_lane | target_lane | 94.0 | 97.0 | apply_now | apply_now | database_development_evidence, integration_data_evidence, target_eligibility, good_fit_score, strong_primary_fit |
| Databricks Data Engineer - Data & AI (li-4427380802) | target_lane | target_lane | 91.29 | 91.29 | apply_now | apply_now | database_and_data_stack_evidence, integration_data_evidence, target_eligibility, good_fit_score, strong_primary_fit |
| Remote - Senior PeopleSoft Security Analyst (li-4428072762) | bridge_lane | wrong_lane | 65.0 | 15.0 | manual_review | skip | integration_data_evidence, bridge_eligibility, security_domain_identity_guard, weak_fit_score, configured_hard_blocker, wrong_role_identity |
| Sr SAP Enterprise Integration Developer (li-4429980324) | bridge_lane | secondary_lane | 65.0 | 85.0 | manual_review | manual_review | integration_data_evidence, supported_integration_target, bridge_eligibility, generic_software_guard, good_fit_score, ambiguous_role_review |
| Master Data Management  Engineer (li-4429674619) | target_lane | bridge_lane | 67.0 | 65.0 | skip | skip | integration_data_evidence, target_eligibility, bridge_eligibility, ecosystem_identity_guard, possible_fit_score, configured_hard_blocker, ecosystem_ownership_gap |

## Database / SQL examples

| Title / ID | Old lane | New lane | Old fit | New fit | Old decision | New decision | Main triggered policy rules |
|---|---|---|---:|---:|---|---|---|
| Data Engineer - Oracle PL/SQL (in-1393eac0b7e7e3be) | wrong_lane | target_lane | 15.0 | 78.75 | skip | manual_review | database_development_evidence, integration_data_evidence, target_eligibility, possible_fit_score, configured_review_gate |
| SQL Developer (li-4429620240) | target_lane | target_lane | 96.5 | 99.5 | apply_now | apply_now | database_development_evidence, integration_data_evidence, target_eligibility, good_fit_score, strong_primary_fit |
| Database Developer (in-e732e85dd689c9bf) | bridge_lane | target_lane | 65.0 | 96.67 | manual_review | manual_review | database_development_evidence, integration_data_evidence, target_eligibility, positive_and_exclusion_signals, good_fit_score, ambiguous_role_review |
| Senior Software Engineer, Distributed Databases (li-4427861687) | wrong_lane | secondary_lane | 15.0 | 85.0 | skip | manual_review | database_development_evidence, generic_software_guard, good_fit_score, adjacent_or_moderate_fit |
| Lead Data Engineer (li-4429319112) | wrong_lane | target_lane | 15.0 | 82.87 | skip | manual_review | database_development_evidence, integration_data_evidence, target_eligibility, good_fit_score, configured_review_gate |
| Azure Data Engineer (li-4429992094) | wrong_lane | target_lane | 15.0 | 61.22 | skip | manual_review | database_and_data_stack_evidence, target_eligibility, possible_fit_score, configured_review_gate |
| SQL Database Developer (li-4427563193) | bridge_lane | target_lane | 65.0 | 93.71 | manual_review | apply_now | database_development_evidence, target_eligibility, good_fit_score, strong_primary_fit |
| Sr Cloud  Database developer (li-4429359161) | secondary_lane | target_lane | 85.0 | 90.81 | manual_review | manual_review | target_eligibility, good_fit_score, ambiguous_role_review |
| Database Developer with AI (li-4430475178) | secondary_lane | target_lane | 85.0 | 89.0 | manual_review | manual_review | backend_evidence, target_eligibility, good_fit_score, ambiguous_role_review |
| Lead Analyst Data Engineer (in-1f5c8418605bc555) | target_lane | target_lane | 47.5 | 53.5 | skip | skip | database_development_evidence, database_and_data_stack_evidence, integration_data_evidence, target_eligibility, weak_fit_score, insufficient_fit |

## Evidence behind the examples

Boundary-matched terms below are facts extracted from the actual stored descriptions/titles. The full grade JSON preserves action traces, raw scores, excluded lanes, confidence, requirements and provenance.

### Application Security Integration Engineer (li-4430114690)

- Identity/development evidence: `{"integration_title_identity": ["integration", "engineer"], "security_title_identity": ["security", "engineer"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `['Terraform']` → `['Terraform']`.
- Preferred atomic gaps: `[]` → `[]`.

### Flight Controls Integration Engineer (li-4429969524)

- Identity/development evidence: `{"hardware_title_identity": ["flight controls", "controls", "engineer"], "integration_title_identity": ["integration", "engineer"], "hardware_responsibilities": ["flight control", "aircraft", "avionics", "control systems"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Windchill Integration Engineer (li-4429666992)

- Identity/development evidence: `{"ecosystem_terms": ["sap", "boomi", "mulesoft", "windchill"], "ecosystem_ownership": ["cad integrations", "plm integration", "windchill data model"], "ecosystem_title": ["windchill"], "database_usage": ["sql"], "integration_title_identity": ["integration", "engineer"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `['Kafka']` → `['Kafka']`.

### Integration Engineer (li-4430454590)

- Identity/development evidence: `{"integration_data": ["etl"], "database_usage": ["sql", "sql server"], "integration_title_identity": ["integration", "engineer"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `['SQL Server', 'Kafka']` → `['Kafka']`.
- Preferred atomic gaps: `[]` → `[]`.

### Data & Integration Engineer (li-4430448809)

- Identity/development evidence: `{"integration_data": ["data exchange"], "database_usage": ["sql"], "integration_title_identity": ["integration", "engineer"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `['AWS']` → `['AWS']`.

### Data Integration Engineer (in-07e05dd5a314ee99)

- Identity/development evidence: `{"ecosystem_terms": ["boomi", "mulesoft"], "ecosystem_ownership": ["atomsphere"], "integration_data": ["etl", "data pipeline", "data pipelines", "data integration", "data exchange"], "database_usage": ["sql"], "integration_title_identity": ["integration", "engineer"], "data_stack_usage": ["snowflake"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Robotic Systems Integration Engineer (li-4429779333)

- Identity/development evidence: `{"hardware_title_identity": ["robotic", "engineer"], "database_usage": ["postgres"], "integration_title_identity": ["integration", "engineer"], "hardware_responsibilities": ["semiconductor"]}`
- AI review required: `True` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Integration Engineer or Senior Integration Engineer, Texas Institute for Electronics, Cockrell School of Engineering (li-4424947815)

- Identity/development evidence: `{"ecosystem_terms": ["workday"], "hardware_title_identity": ["electronics", "engineer", "engineering"], "integration_title_identity": ["integration", "engineer"], "hardware_responsibilities": ["semiconductor"]}`
- AI review required: `True` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Senior Boomi Integration Engineer -Remote (li-4429363929)

- Identity/development evidence: `{"ecosystem_terms": ["boomi", "mulesoft"], "ecosystem_title": ["boomi"], "database_usage": ["sql", "sql server"], "integration_title_identity": ["integration", "engineer"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `['Kafka', 'AWS']` → `['Kafka', 'AWS']`.
- Preferred atomic gaps: `['Google Cloud', 'SQL Server']` → `['Google Cloud']`.

### Boomi Integration Engineer (li-4419531662)

- Identity/development evidence: `{"ecosystem_terms": ["mdm", "sap", "salesforce", "boomi", "mulesoft"], "ecosystem_title": ["boomi"], "integration_data": ["data mapping"], "integration_title_identity": ["integration", "engineer"]}`
- AI review required: `False` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Informatica MDM Support & Data Operations Specialist (li-4429364893)

- Identity/development evidence: `{"ecosystem_terms": ["informatica", "mdm", "master data management", "servicenow"], "ecosystem_ownership": ["hub console", "matchmerge rules", "provisioning tool"], "ecosystem_title": ["informatica", "mdm"], "integration_data": ["etl", "data pipeline"], "database_usage": ["sql"]}`
- AI review required: `False` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Data Engineer - Oracle PL/SQL (in-1393eac0b7e7e3be)

- Identity/development evidence: `{"ecosystem_terms": ["informatica"], "database_development": ["plsql"], "integration_data": ["etl"], "database_usage": ["sql"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Senior SAP Cloud ALM, Integration & ABAP Engineer (li-4430986127)

- Identity/development evidence: `{"ecosystem_terms": ["sap", "salesforce"], "ecosystem_ownership": ["platform owner", "platform roadmap"], "ecosystem_title": ["sap"], "integration_data": ["etl"], "database_usage": ["sql", "postgresql"], "integration_title_identity": ["integration", "engineer"], "hardware_responsibilities": ["rocket"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `['PostgreSQL']` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Senior Integration Boomi Engineer (li-4428703372)

- Identity/development evidence: `{"ecosystem_terms": ["informatica", "boomi", "mulesoft"], "ecosystem_title": ["boomi"], "integration_data": ["data mapping"], "database_usage": ["sql"], "integration_title_identity": ["integration", "engineer"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `['Kafka']` → `['Kafka']`.

### ETL Developer (3 Days in OFFICE :: W2 ONLY) (li-4428087682)

- Identity/development evidence: `{"ecosystem_terms": ["workday"], "database_development": ["stored procedures"], "integration_data": ["etl", "data exchange"], "database_usage": ["sql", "sql server"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `['SQL Server']` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Databricks Data Engineer - Data & AI (li-4427380802)

- Identity/development evidence: `{"ecosystem_terms": ["informatica"], "integration_data": ["etl"], "database_usage": ["sql", "sql server"], "data_stack_usage": ["snowflake", "databricks", "azure databricks"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Remote - Senior PeopleSoft Security Analyst (li-4428072762)

- Identity/development evidence: `{"ecosystem_terms": ["peoplesoft"], "ecosystem_title": ["peoplesoft"], "integration_data": ["data integration"], "database_usage": ["sql"], "security_title_identity": ["security", "analyst"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Sr SAP Enterprise Integration Developer (li-4429980324)

- Identity/development evidence: `{"ecosystem_terms": ["sap"], "ecosystem_title": ["sap"], "integration_data": ["etl", "data pipelines", "data integration"], "database_usage": ["sql"], "integration_title_identity": ["integration", "developer"]}`
- AI review required: `False` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Master Data Management  Engineer (li-4429674619)

- Identity/development evidence: `{"ecosystem_terms": ["informatica", "mdm", "servicenow"], "ecosystem_ownership": ["hub console", "match/merge rules", "provisioning tool", "match/merge"], "ecosystem_title": ["master data management"], "integration_data": ["etl", "data pipeline"], "database_usage": ["sql"]}`
- AI review required: `False` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### SQL Developer (li-4429620240)

- Identity/development evidence: `{"database_development": ["stored procedures"], "integration_data": ["etl"], "database_usage": ["sql", "sql server", "microsoft sql server"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `['SQL Server']` → `[]`.
- Preferred atomic gaps: `['Power BI']` → `['Power BI']`.

### Database Developer (in-e732e85dd689c9bf)

- Identity/development evidence: `{"database_development": ["stored procedures", "schema design", "query tuning"], "integration_data": ["etl"], "database_usage": ["sql", "sql server"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Senior Software Engineer, Distributed Databases (li-4427861687)

- Identity/development evidence: `{"database_development": ["schema design"], "database_usage": ["sql"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Lead Data Engineer (li-4429319112)

- Identity/development evidence: `{"database_development": ["schema design"], "integration_data": ["data pipelines"], "database_usage": ["sql", "postgresql"]}`
- AI review required: `True` → `False`.
- Required atomic gaps: `['PostgreSQL']` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Azure Data Engineer (li-4429992094)

- Identity/development evidence: `{"ecosystem_terms": ["informatica"], "database_usage": ["sql", "sql server"], "data_stack_usage": ["snowflake", "databricks", "azure databricks", "spark", "pyspark"]}`
- AI review required: `True` → `False`.
- Required atomic gaps: `['Snowflake', 'SQL Server', 'Databricks', 'Spark', 'Terraform', 'Power BI', 'Tableau']` → `['Snowflake', 'Databricks', 'Spark', 'Terraform', 'Power BI', 'Tableau']`.
- Preferred atomic gaps: `[]` → `[]`.

### SQL Database Developer (li-4427563193)

- Identity/development evidence: `{"database_development": ["stored procedures"], "database_usage": ["sql", "sql server"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Sr Cloud  Database developer (li-4429359161)

- Identity/development evidence: `{"database_usage": ["sql", "sql server", "postgres"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `['AWS']` → `['AWS']`.
- Preferred atomic gaps: `[]` → `[]`.

### Database Developer with AI (li-4430475178)

- Identity/development evidence: `{"database_usage": ["sql", "sql server", "postgresql", "mysql"]}`
- AI review required: `True` → `True`.
- Required atomic gaps: `[]` → `[]`.
- Preferred atomic gaps: `[]` → `[]`.

### Lead Analyst Data Engineer (in-1f5c8418605bc555)

- Identity/development evidence: `{"database_development": ["pl/sql"], "integration_data": ["data pipelines", "data integration"], "database_usage": ["sql", "sql server", "postgresql"], "data_stack_usage": ["databricks", "redshift", "pyspark"]}`
- AI review required: `False` → `False`.
- Required atomic gaps: `['PostgreSQL', 'SQL Server', 'Databricks', 'Spark', 'AWS', 'Redshift', 'Power BI']` → `['Databricks', 'Spark', 'AWS', 'Redshift', 'Power BI']`.
- Preferred atomic gaps: `[]` → `[]`.

## Confirmed database experience

| Atomic technology | Required gaps before → after | Preferred gaps before → after |
|---|---:|---:|
| SQL Server | 171 → 0 | 89 → 0 |
| PostgreSQL | 145 → 0 | 58 → 0 |
| MySQL | 65 → 65 | 33 → 33 |

## Interpretation and remaining manual checks

4 previously TARGET ecosystem postings now lose TARGET with `ecosystem_identity_guard` evidence.
The actual Oracle PL/SQL posting asks for Oracle SQL and PLSQL development, Informatica PowerCenter ETL and production support. PLSQL spelling was absent from the evidence model; this is a reusable database-development gap, not a title exception. Mentoring/leadership still warrants manual review.
SQL Server 1.0 and PostgreSQL 0.7 reflect candidate-confirmed experience. They are no longer fully missing; MySQL is still independent. Known PostgreSQL no longer earns missing-skill learning value. Therefore a lower aggregate learning score can be correct.
Modern data technologies remain positive/neutral tool evidence, separate from infrastructure ownership. The new SQL + data-stack rule requires supporting signals; a technology alone cannot establish a lane.
Short or conflicting descriptions can still request AI review even with high fit. Confidence is heuristic, not a calibrated probability. No AI was called.
Inspect security title scope, embedded/control-system titles, PLM/CAD ownership wording and borderline vendor titles. Title-pattern co-occurrence is intentionally simple and can overmatch compound titles. Change YAML policy when career preferences differ.
Specific manual check: Senior Integration Boomi Engineer (li-4428703372) stays a plausible transferable integration role, but explicitly requests 3–5+ years of Dell Boomi. It becomes TARGET/APPLY NOW under current policy. Confirm whether that product experience should be a gate; the retained ecosystem experience rule begins at five required years and the role does not claim platform administration. This is not evidence that the candidate already knows Boomi.
Other inspected boundaries: Python/React Developer (li-4430708650) becomes SECONDARY/MANUAL REVIEW because of database/query-optimization work, despite substantial frontend work. Business Strategy Analyst Lead (li-4426877231) becomes BRIDGE/MANUAL REVIEW with SQL/Python/Snowflake analytics evidence; its senior strategic responsibilities still deserve scrutiny. Integration Specialist (li-4427839411) contains transferable SQL/EDI/data-exchange work but lists a German work location, outside this domain-only calibration.
Search lane/review priority remain optional and absent from this DB view. The market population is the existing extraction scope rather than this 90-day job cohort.
After market provenance: `{"source": "public.skill_prevalence", "taxonomy_versions": ["31d08964f877"], "extraction_run_ids": [2], "total_jobs": 127801, "read_at": "2026-09-14T04:36:15.687252+00:00", "population": "extraction_snapshot", "prevalence_pct": {"SQL": 25.8, "Python": 28.1, "PostgreSQL": 3.7, "SQL Server": 4.1, "Databricks": 3.7, "Spark": 4.7, "AWS": 27.9, "Azure": 14.6, "Redshift": 1.7, "Power BI": 5.9}}`.
No grading evaluator, fit/decision engine, schema, canonical taxonomy or prevalence calculation changed in this pass. Config snapshots identify the exact profile and policy that produced every grade.
