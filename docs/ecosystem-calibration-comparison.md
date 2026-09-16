# Ecosystem concentration calibration

Before: `data\outputs\results-db-90-days-domain.csv`. After: `data\outputs\results-db-90-days-ecosystem.csv`.
Exact replay of 8,692 saved DB jobs; all identities and title/description hashes match.
The date advanced between passes, so the frozen DB export supplies job inputs. The existing DB prevalence view is loaded once; old grades are never used as scoring inputs.
Grading: `['3f42ddb8add0fbd8']` → `['6e4fcaeb3b0f4851']`. Taxonomy: `['31d08964f877']`.
Jobs with changed recorded prevalence percentages: 0.

## Aggregate comparison

| Metric | Before | After |
|---|---:|---:|
| jobs | 8692 | 8692 |
| average_fit | 31.32 | 31.21 |
| average_learning | 2.45 | 2.45 |
| nonzero_learning | 886 | 886 |
| unavailable_learning | 0 | 0 |
| ai_review_pct | 37.39 | 37.37 |
| bridge_lane | 700 | 700 |
| secondary_lane | 1476 | 1472 |
| target_lane | 266 | 264 |
| wrong_lane | 6250 | 6256 |
| apply_now | 101 | 99 |
| manual_review | 2266 | 2257 |
| skip | 6325 | 6336 |
| good_fit | 887 | 861 |
| possible_fit | 1492 | 1506 |
| weak_fit | 6313 | 6325 |

## Ecosystem-related titles

`{"count": 327, "target_before": 26, "target_after": 24, "moved_to": {"target_lane": 0, "secondary_lane": 2, "bridge_lane": 0, "wrong_lane": 6}}`
Title cohort uses configured enterprise-product or data-platform title evidence. Counts cover all audited title-cohort records; the examples below are the detailed inspection sample. Moved-to counts include any lane change, not only departures from TARGET.

## Representative ecosystem postings

| Title / ID | Ecosystem | Lane before → after | Fit before → after | Decision before → after | Title hits | Specialization hits | Ownership hits | Transferable hits | Main policy rules |
|---|---|---|---:|---|---:|---:|---:|---:|---|
| Senior Integration Boomi Engineer (li-4428703372) | boomi | target_lane → secondary_lane | 92.32 → 74.32 | apply_now → manual_review | 1 | 2 | 0 | 5 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Informatica Developer (li-4429971018) | informatica | secondary_lane → wrong_lane | 85.0 → 15.0 | manual_review → skip | 1 | 4 | 0 | 3 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, ecosystem_low_transfer_specialist_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Informatica Senior Developer (li-4429397454) | informatica | secondary_lane → secondary_lane | 85.0 → 79.0 | manual_review → manual_review | 1 | 2 | 0 | 2 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Senior Informatica Administrator (li-4426859552) | informatica | secondary_lane → wrong_lane | 85.0 → 15.0 | manual_review → skip | 1 | 0 | 0 | 5 | ecosystem_admin_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, ecosystem_low_transfer_admin_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_admin_fit_gate |
| Data Engineer (Palantir) (li-4429057139) | palantir | target_lane → target_lane | 90.85 → 90.85 | apply_now → apply_now | 1 | 4 | 0 | 7 | transferable_data_identity, strong_primary_fit |
| Workday Integration Engineer (li-4429681155) | workday | secondary_lane → secondary_lane | 83.36 → 65.36 | manual_review → manual_review | 1 | 10 | 0 | 4 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Salesforce Developer (in-53cf60cece176e00) | salesforce | secondary_lane → wrong_lane | 85.0 → 15.0 | manual_review → skip | 1 | 6 | 0 | 2 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, ecosystem_low_transfer_specialist_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| ServiceNow Developer (li-4427860069) | servicenow | secondary_lane → wrong_lane | 69.0 → 15.0 | manual_review → skip | 1 | 5 | 0 | 3 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, ecosystem_low_transfer_specialist_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_specific_experience, ecosystem_limited_transfer_fit |
| MDM Engineer (in-0470c187b383c0b2) | mdm | bridge_lane → bridge_lane | 59.0 → 59.0 | skip → skip | 1 | 0 | 4 | 7 | transferable_data_identity, ecosystem_ownership_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_dependence |
| Informatica MDM Support & Data Operations Specialist (li-4429364893) | informatica, mdm | bridge_lane → bridge_lane | 59.0 → 59.0 | skip → skip | 2 | 0 | 3 | 5 | transferable_data_identity, ecosystem_ownership_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_dependence |
| Senior Workday Integration Developer - Extend (in-3fd4d35537a37358) | workday | secondary_lane → secondary_lane | 80.12 → 62.12 | manual_review → manual_review | 1 | 5 | 0 | 5 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Salesforce Administrator (li-4427352776) | salesforce | secondary_lane → secondary_lane | 85.0 → 67.93 | manual_review → manual_review | 1 | 2 | 0 | 5 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Informatica Platform Administrator (li-4426883422) | informatica | wrong_lane → wrong_lane | 15.0 → 15.0 | skip → skip | 1 | 0 | 1 | 2 | ecosystem_ownership_evidence, ecosystem_admin_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, ecosystem_low_transfer_admin_guard, configured_hard_blocker, ecosystem_usage_penalty, ecosystem_admin_fit_gate, ecosystem_dependence |
| ServiceNow Integration Hub Developer (li-4429663482) | servicenow | secondary_lane → secondary_lane | 85.0 → 85.0 | manual_review → manual_review | 1 | 0 | 0 | 3 | ecosystem_usage_penalty |
| Senior Boomi Integration Engineer -Remote (li-4429363929) | boomi | secondary_lane → secondary_lane | 77.38 → 77.38 | manual_review → manual_review | 1 | 0 | 0 | 9 | transferable_data_counterweight, ecosystem_usage_penalty |
| Data Engineer (Databricks + Informatica + Azure) (li-4429994053) | informatica, databricks | target_lane → target_lane | 75.93 → 75.93 | manual_review → manual_review | 2 | 0 | 0 | 10 | transferable_data_identity, transferable_data_counterweight, ecosystem_usage_penalty |
| Informatica IICS/PowerCenter Engineer( Snowflake & ETL) (li-4427330488) | informatica, iics, snowflake | bridge_lane → bridge_lane | 65.0 → 65.0 | manual_review → manual_review | 3 | 0 | 0 | 10 | transferable_data_counterweight, ecosystem_usage_penalty |
| Senior Workday Developer (li-4390663708) | workday | secondary_lane → secondary_lane | 83.59 → 65.59 | manual_review → manual_review | 1 | 4 | 0 | 5 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Salesforce Data Cloud Engineer III (Memphis TN or Remote in the USA) (li-4419561688) | salesforce | bridge_lane → bridge_lane | 49.48 → 31.48 | skip → skip | 1 | 2 | 0 | 7 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, ecosystem_usage_penalty, ecosystem_specific_experience, ecosystem_limited_transfer_fit |
| ServiceNow Platform Engineer (li-4390268709) | servicenow | secondary_lane → secondary_lane | 85.0 → 74.2 | manual_review → manual_review | 1 | 2 | 0 | 2 | ecosystem_specialization_evidence, ecosystem_concentration_evidence, ecosystem_identity_guard, configured_review_gate, ecosystem_usage_penalty, ecosystem_limited_transfer_fit |
| Boomi Integration Lead Engineer (li-4419550540) | boomi | secondary_lane → secondary_lane | 67.39 → 67.39 | manual_review → manual_review | 1 | 0 | 0 | 4 | transferable_data_identity, configured_review_gate, ecosystem_usage_penalty |
| Platform Engineer - Palantir (in-74450422ec001fb7) | palantir | wrong_lane → wrong_lane | 15.0 → 15.0 | skip → skip | 1 | 2 | 0 | 3 | configured_hard_blocker |

Specialization counts include separately labeled data-platform vocabulary for reporting. Foundry delivery components do not feed enterprise concentration by default.

## Matched evidence for the inspection sample

### Senior Integration Boomi Engineer (li-4428703372)

- Specialization: `['work within dell boomi', 'experience with dell boomi']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'api', 'rest', 'soap', 'data mapping']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Informatica Developer (li-4429971018)

- Specialization: `['mdm hub components', 'schema manager', 'stewardship workflows', 'landing/staging tables']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['etl', 'apis', 'data modeling']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Informatica Senior Developer (li-4429397454)

- Specialization: `['migration of informatica', 'migration of existing informatica workflows']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'pl/sql']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Senior Informatica Administrator (li-4426859552)

- Specialization: `[]`.
- Ownership: `[]`.
- Administration: `['system upgrades', 'platform performance', 'system configurations']`.
- Transferable data: `['sql', 'sql server', 'mysql', 'etl', 'data integration']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Data Engineer (Palantir) (li-4429057139)

- Specialization: `['foundry ontology', 'code repositories', 'pipeline builder', 'contour']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'python', 'etl', 'elt', 'data pipelines', 'data modeling', 'data quality']`.
- Concentration: `False`; strong transfer counterweight: `False`.

### Workday Integration Engineer (li-4429681155)

- Specialization: `['workday studio', 'studio integrations', 'eib', 'core connectors', 'peci', 'tenant configuration', 'tenant refresh', 'integration system users', 'workday business processes', 'workday extend']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['apis', 'rest', 'soap', 'data quality']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Salesforce Developer (in-53cf60cece176e00)

- Specialization: `['lightning web components', 'aura components', 'omniscripts', 'process builder', 'salesforce platform developer', 'service cloud implementation']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['rest', 'soap']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### ServiceNow Developer (li-4427860069)

- Specialization: `['glide', 'client scripts', 'ui policies', 'servicenow development', 'servicenow certified']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['apis', 'rest', 'soap']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### MDM Engineer (in-0470c187b383c0b2)

- Specialization: `[]`.
- Ownership: `['hub console', 'match/merge rules', 'provisioning tool', 'match/merge']`.
- Administration: `[]`.
- Transferable data: `['sql', 'etl', 'data pipeline', 'api', 'apis', 'rest', 'soap']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Informatica MDM Support & Data Operations Specialist (li-4429364893)

- Specialization: `[]`.
- Ownership: `['hub console', 'matchmerge rules', 'provisioning tool']`.
- Administration: `[]`.
- Transferable data: `['sql', 'etl', 'data pipeline', 'api', 'apis']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Senior Workday Integration Developer - Extend (in-3fd4d35537a37358)

- Specialization: `['workday studio', 'eib', 'core connectors', 'peci', 'workday extend']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['api', 'rest', 'soap', 'json', 'data exchange']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Salesforce Administrator (li-4427352776)

- Specialization: `['visualforce', 'apex']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'apis', 'rest', 'soap', 'data quality']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Informatica Platform Administrator (li-4426883422)

- Specialization: `[]`.
- Ownership: `['platform administration']`.
- Administration: `['platform administration', 'system configurations']`.
- Transferable data: `['sql', 'sql server']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### ServiceNow Integration Hub Developer (li-4429663482)

- Specialization: `[]`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['apis', 'rest', 'soap']`.
- Concentration: `False`; strong transfer counterweight: `False`.

### Senior Boomi Integration Engineer -Remote (li-4429363929)

- Specialization: `[]`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'sql server', 'api', 'apis', 'rest', 'soap', 'xml', 'json', 'sftp']`.
- Concentration: `False`; strong transfer counterweight: `True`.

### Data Engineer (Databricks + Informatica + Azure) (li-4429994053)

- Specialization: `[]`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'sql server', 'postgresql', 'python', 'etl', 'elt', 'data pipelines', 'data integration', 'data transformation', 'data quality']`.
- Concentration: `False`; strong transfer counterweight: `True`.

### Informatica IICS/PowerCenter Engineer( Snowflake & ETL) (li-4427330488)

- Specialization: `[]`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'sql server', 'python', 'etl', 'data pipelines', 'data integration', 'apis', 'rest', 'soap', 'data modeling']`.
- Concentration: `False`; strong transfer counterweight: `True`.

### Senior Workday Developer (li-4390663708)

- Specialization: `['workday studio', 'eib', 'core connectors', 'workday extend']`.
- Ownership: `[]`.
- Administration: `['platform performance', 'system configurations']`.
- Transferable data: `['apis', 'rest', 'soap', 'data mapping', 'data modeling']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Salesforce Data Cloud Engineer III (Memphis TN or Remote in the USA) (li-4419561688)

- Specialization: `['data model objects', 'calculated insights']`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['sql', 'python', 'etl', 'elt', 'apis', 'rest', 'data quality']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### ServiceNow Platform Engineer (li-4390268709)

- Specialization: `['ui policies', 'servicenow development']`.
- Ownership: `[]`.
- Administration: `['platform performance']`.
- Transferable data: `['apis', 'rest']`.
- Concentration: `True`; strong transfer counterweight: `False`.

### Boomi Integration Lead Engineer (li-4419550540)

- Specialization: `[]`.
- Ownership: `[]`.
- Administration: `[]`.
- Transferable data: `['api', 'apis', 'json', 'data modeling']`.
- Concentration: `False`; strong transfer counterweight: `False`.

### Platform Engineer - Palantir (in-74450422ec001fb7)

- Specialization: `['code repositories', 'pipeline builder']`.
- Ownership: `[]`.
- Administration: `['platform admin', 'platform security']`.
- Transferable data: `['sql', 'python', 'api']`.
- Concentration: `False`; strong transfer counterweight: `False`.


## Manual review of all five retained TARGET integration jobs

### Data Integration Engineer (in-07e05dd5a314ee99)

Lane: target_lane → target_lane; fit: 89.99 → 81.99; decision: manual_review → manual_review.

- Transferable evidence: SQL, ETL, cloud pipelines, APIs, JSON/XML/SFTP, healthcare data standards and reconciliation.
- Ecosystem evidence: Boomi Atoms/Atom Clouds, AtomSphere monitoring and connector configuration are substantial; Boomi/Epic certifications are due within six months after hire. Equivalent integration-platform experience is accepted.
- Conflicts/caveats: No conflicting domain identity. Runtime management is mixed with broad interface/data engineering.
- Assessment: Retain TARGET with specialization review and a fit penalty. Broad transferable work counters concentration without pretending the Boomi gap is absent.

### Lead Integration Engineer, EPIC Bridges (li-4427707701)

Lane: target_lane → target_lane; fit: 88.0 → 88.0; decision: manual_review → manual_review.

- Transferable evidence: SQL, REST/SOAP, XML, HL7/FHIR, data exchange and mapping.
- Ecosystem evidence: Epic Bridges, Corepoint and managed file transfer; product-specific healthcare experience is preferred, not an exclusive prerequisite.
- Conflicts/caveats: No conflicting security/hardware role identity. Lead scope remains a review consideration.
- Assessment: TARGET remains defensible: interoperability standards and interface delivery dominate. Review healthcare familiarity.

### Database Administrator/ETL & Data Integration Engineer (li-4430133467)

Lane: target_lane → target_lane; fit: 73.85 → 65.85; decision: manual_review → manual_review.

- Transferable evidence: 30% ADF ETL/integration and 20% warehouse work, plus SQL procedures, schema design and APIs/SFTP.
- Ecosystem evidence: 25% Salesforce data operations/Data Cloud configuration, plus Tableau and team leadership.
- Conflicts/caveats: DB administrator title and capacity planning are mixed with strong data engineering. Eight years and team leadership remain review concerns.
- Assessment: Retain TARGET/manual review. Salesforce is significant but does not dominate the entire role; a generic DBA title is not vendor-admin identity.

### Data & Integration Engineer (li-4430448809)

Lane: target_lane → target_lane; fit: 92.98 → 92.98; decision: apply_now → apply_now.

- Transferable evidence: SQL/Python, HL7/FHIR interoperability, data exchange and troubleshooting.
- Ecosystem evidence: Several interchangeable middleware engines are accepted: Mirth, Rhapsody, Cloverleaf and Azure integration services.
- Conflicts/caveats: No conflicting domain identity. Five years of healthcare integration and UK-oriented employment context need review.
- Assessment: TARGET remains defensible; experience is tied to healthcare integration, not one proprietary runtime.

### Integration Engineer (li-4430454590)

Lane: target_lane → target_lane; fit: 86.3 → 86.3; decision: apply_now → apply_now.

- Transferable evidence: Explicit T-SQL/SQL Server, Python, ETL, APIs, Kafka and microservices.
- Ecosystem evidence: Any API-management tool is accepted; no enterprise-platform specialization requirement.
- Conflicts/caveats: No conflicting domain identity. The posting is onsite in Geneva.
- Assessment: TARGET is correct for technical career direction; location is a separate application constraint.


## Interpretation and remaining ambiguity

The actual Informatica Developer is an MDM Hub/360 implementation specialist (schema manager, stewardship workflows and landing/staging components), unlike the transferable SQL/ETL fixture with the same title. The actual Informatica Senior Developer mixes platform migration with PL/SQL and remains SECONDARY rather than automatically WRONG.
The actual Palantir Data Engineer explicitly welcomes strong data engineers new to Foundry. Its Foundry Ontology/Code Repositories vocabulary is recorded separately and does not impose an enterprise-platform penalty. Zurich location remains a separate application constraint.
The actual Senior Integration Boomi Engineer asks for hands-on Dell Boomi experience and centers delivery on it. It receives specialization review rather than an invented hard ownership blocker. Matched experience wording is evidence; this pass does not claim to parse product-specific numeric years or distinguish every preferred/required phrase.
Counts are distinct matched phrases, not mention frequency, responsibility percentages, or statistically calibrated concentration. Long descriptions and boilerplate can add incidental signals. The explicit title/transfer counterweights reduce that risk; inspect mixed-platform work and ambiguous MDM terminology.
Remaining vocabulary boundary: ServiceNow Integration Hub Developer describes Integration Hub spokes and Flow Designer, which are not yet in the specialization group. Inspect that posting despite its existing non-TARGET classification. Senior Boomi Integration Engineer -Remote mixes an explicit seven-year Boomi demand with equivalent-platform wording; the IICS/PowerCenter/Snowflake posting asks for eight years in multiple tools while still describing transferable data work. These require judgment about experience gates, not automatic rejection by product name.
Existing fit caps, profile, canonical atomic taxonomy, market calculations, decision thresholds and domain guards remain in place. The only generic mechanism addition exports declared lane flags into the fit context and grade audit, avoiding duplicate concentration conditions across stages.
Final market context: `{"source": "public.skill_prevalence", "taxonomy_versions": ["31d08964f877"], "extraction_run_ids": [2], "total_jobs": 127801, "read_at": "2026-09-15T02:07:59.277535+00:00", "population": "extraction_snapshot", "prevalence_pct": {"SQL": 25.8, "Python": 28.1, "PostgreSQL": 3.7, "SQL Server": 4.1, "Databricks": 3.7, "Spark": 4.7, "AWS": 27.9, "Azure": 14.6, "Redshift": 1.7, "Power BI": 5.9}}`.
See [policy controls and implementation notes](ecosystem-policy.md) for thresholds, file changes, tests and how to accept a platform through configuration.
