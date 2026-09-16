# Requirement group semantics — frozen-cohort impact

Before: `data\outputs\results-db-90-days-requirements.csv`
After: `data\outputs\results-db-90-days-requirement-semantics.csv`

Saved market prevalence is reused. Atomic gap order is ignored. Each input row and description is checked before comparison.

Changed jobs (including new explicit group-gap representation): **1635**.

| Metric | Before | After |
|---|---|---|
| jobs | 8692 | 8692 |
| role_lane | Counter({'wrong_lane': 6256, 'secondary_lane': 1472, 'bridge_lane': 700, 'target_lane': 264}) | Counter({'wrong_lane': 6256, 'secondary_lane': 1472, 'bridge_lane': 700, 'target_lane': 264}) |
| apply_decision | Counter({'skip': 6314, 'manual_review': 2273, 'apply_now': 105}) | Counter({'skip': 6320, 'manual_review': 2269, 'apply_now': 103}) |
| fit_quality | Counter({'weak_fit': 6303, 'possible_fit': 1485, 'good_fit': 904}) | Counter({'weak_fit': 6309, 'possible_fit': 1497, 'good_fit': 886}) |
| average_fit | 31.35295 | 31.295492 |
| average_learning | 2.450728 | 2.450728 |
| nonzero_learning | 886 | 886 |
| ai_review_rate_pct | 37.3677 | 38.127 |

## Changed fields

| Field | Jobs |
|---|---:|
| required_atomic_gaps | 442 |
| preferred_atomic_gaps | 331 |
| required_group_gaps | 615 |
| preferred_group_gaps | 403 |
| fit_score | 287 |
| fit_quality | 52 |
| apply_decision | 22 |
| ai_review_required | 66 |
| role_lane | 0 |
| learning_score | 0 |
| alignment_score | 1004 |
| label | 35 |

Unattributed changes: 0.

Protected configuration parity: {"roles": true, "skills": true, "profile": true, "market_skills": true, "weights_except_new_group_penalty": true}.

Inline-preferred boundary effects on years/section-scoped alignment: 190 jobs. These are included under legacy/group reconciliation with source lines and before/after evidence in JSON; they are not threshold changes.

Group-gap counts compare the old absent gap representation against explicit gaps; previously `satisfied=false` alone did not generate a penalty.

The JSON companion retains source groups, penalty ledgers and attribution for every changed job. Categories overlap; they identify observed semantic changes, not isolated counterfactual effects.

## Representative changed cases

### Senior Data Engineer (`li-4317952467`)

- Changed: required_atomic_gaps, required_group_gaps, fit_score, apply_decision, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 64.93 → 79.93; decision: manual_review → apply_now
- Required atomic gaps: ['Snowflake', 'Redshift', 'BigQuery', 'Airflow', 'dbt', 'Terraform', 'Spark', 'AWS'] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 3

- Source (required): build and tune big data pipelines using sql, python, and distributed processing frameworks.
  - Before: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']; grammar=conjunction_or_enumeration
- Source (required): strong sql skills and experience with cloud warehouses (e.g.: snowflake, bigquery, redshift).
  - Before: all_of ['SQL', 'Snowflake', 'Redshift', 'BigQuery']; satisfied=False; known=['SQL']
  - After: any_of ['SQL', 'Snowflake', 'BigQuery', 'Redshift']; satisfied=True; known=['SQL']; grammar=examples
- Source (required): hands\\-on experience with transformation and orchestration tools (e.g.: dbt, airflow, dagster).
  - Before: all_of ['Airflow', 'dbt']; satisfied=False; known=[]
  - After: any_of ['dbt', 'Airflow']; satisfied=False; known=[]; grammar=examples
- Source (required): comfort with python or other scripting languages for etl and automation.
  - Before: any_of ['Python']; satisfied=True; known=['Python']
  - After: any_of ['Python']; satisfied=True; known=['Python']; grammar=alternatives
- Source (required): experience deploying and managing infrastructure as code (e.g.: terraform, pulumi).
  - Before: all_of ['Terraform']; satisfied=False; known=[]
  - After: any_of ['Terraform']; satisfied=False; known=[]; grammar=examples
- Source (required): experience with big data and distributed processing (e.g.: apache spark, aws emr, s3\\).
  - Before: all_of ['Spark', 'AWS']; satisfied=False; known=[]
  - After: any_of ['Spark', 'AWS']; satisfied=False; known=[]; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Redshift", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "BigQuery", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Terraform", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_3", "type": "any_of", "skills": ["dbt", "Airflow"], "source": "hands\\\\-on experience with transformation and orchestration tools (e.g.: dbt, airflow, dagster).", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_5", "type": "any_of", "skills": ["Terraform"], "source": "experience deploying and managing infrastructure as code (e.g.: terraform, pulumi).", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_6", "type": "any_of", "skills": ["Spark", "AWS"], "source": "experience with big data and distributed processing (e.g.: apache spark, aws emr, s3\\\\).", "contribution": -3}]`

### Product Manager [Multiple Positions Available] (`li-4419589094`)

- Changed: required_atomic_gaps, required_group_gaps, fit_score, fit_quality, apply_decision, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 47.29 → 62.29; decision: skip → manual_review
- Required atomic gaps: ['Snowflake', 'MySQL', 'Spark', 'Kafka', 'AWS', 'Tableau'] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 1

- Source (required): this position requires experience with the following: applying gaap and ifrs accounting principles to manage financial records and ensure regulatory compliance; designing and implementing seamless integrations across upstream and downstream applications using apache kafka (msk), json (javascript object notation) data structures, amazon simple storage service (s3\\), pyspark and aws glue including pricing, allocation, adjustment, payout, and reconciliation; applying gaap and ifrs accounting principles to manage financial records and ensuring regulatory compliance; integrating with sap general ledger using aws mysql based subledger and snowflake cloud based data platform to power reporting via snowflake snowsight and tableau; recording and reconciling sap journal entries in compliance with gaap, ifrs, sox, and regulatory
  - Before: all_of ['Snowflake', 'MySQL', 'Spark', 'Kafka', 'AWS', 'Tableau']; satisfied=False; known=[]
  - After: any_of ['Kafka', 'Spark', 'AWS', 'MySQL', 'Snowflake', 'Tableau']; satisfied=False; known=[]; grammar=examples
- Source (required): ; designing and optimizing financial data flows and structures using lucid to support transaction processing, reconciliations, and anomaly detection; designing and implementing cross\\-border payment processing and foreign exchange operations by applying iso8583 and iso20022 standards with openapi specifications, and interpreting payment network regulations for visa, mastercard, and nacha and compliance mandates including pci, ecb, and federal reserve to ensure regulatory alignment; performing financial analysis, reporting, and data visualization by utilizing tools including sap, excel, tableau, snowflake, sql, aws cloudwatch, splunk, and alteryx; developing and designing financial accounting data flows and structures optimized for transaction volumes within international organizations to enable accurate revenue and fee reporting using snowflake, snowsight and tableau.
  - Before: all_of ['SQL', 'Snowflake', 'AWS', 'Tableau']; satisfied=False; known=['SQL']
  - After: any_of ['Tableau', 'Snowflake', 'SQL', 'AWS']; satisfied=True; known=['SQL']; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "MySQL", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kafka", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Tableau", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -9, "skills": ["aws", "kafka", "spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "any_of", "skills": ["Kafka", "Spark", "AWS", "MySQL", "Snowflake", "Tableau"], "source": "this position requires experience with the following: applying gaap and ifrs accounting principles to manage financial records and ensure regulatory compliance; designing and implementing seamless integrations across upstream and downstream applications using apache kafka (msk), json (javascript object notation) data structures, amazon simple storage service (s3\\\\), pyspark and aws glue including pricing, allocation, adjustment, payout, and reconciliation; applying gaap and ifrs accounting principles to manage financial records and ensuring regulatory compliance; integrating with sap general ledger using aws mysql based subledger and snowflake cloud based data platform to power reporting via snowflake snowsight and tableau; recording and reconciling sap journal entries in compliance with gaap, ifrs, sox, and regulatory", "contribution": -3}]`

### Senior Software Engineer Specialist - United States (`li-4428782487`)

- Changed: required_group_gaps, fit_score, fit_quality, apply_decision, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, equivalent requirement handling, legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 57.51 → 51.51; decision: manual_review → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 2

- Source (required): experience building scalable, event\\-driven, or asynchronous architectures (e.g., kafka, rabbitmq, or equivalent)
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (required): experience with relational and/or nosql databases (e.g., postgresql, mysql, mongodb)
  - Before: any_of ['PostgreSQL', 'MySQL']; satisfied=True; known=['PostgreSQL']
  - After: any_of ['PostgreSQL', 'MySQL']; satisfied=True; known=['PostgreSQL']; grammar=examples
- Source (required): experience with gitops and kubernetes (helm, kustomize, or similar tooling)
  - Before: any_of ['Kubernetes']; satisfied=False; known=[]
  - After: any_of ['Kubernetes']; satisfied=False; known=[]; grammar=alternatives

Requirement penalty ledger before: `[{"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["kafka"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "equivalent", "skills": ["Kafka"], "source": "experience building scalable, event\\\\-driven, or asynchronous architectures (e.g., kafka, rabbitmq, or equivalent)", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_3", "type": "any_of", "skills": ["Kubernetes"], "source": "experience with gitops and kubernetes (helm, kustomize, or similar tooling)", "contribution": -3}]`

### Senior Software Engineer Specialist (`li-3835714098`)

- Changed: required_group_gaps, fit_score, fit_quality, apply_decision, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, equivalent requirement handling, legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 57.51 → 51.51; decision: manual_review → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 2

- Source (required): • experience building scalable, event\\-driven, or asynchronous architectures (e.g., kafka, rabbitmq, or equivalent)
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (required): • experience with relational and/or nosql databases (e.g., postgresql, mysql, mongodb)
  - Before: any_of ['PostgreSQL', 'MySQL']; satisfied=True; known=['PostgreSQL']
  - After: any_of ['PostgreSQL', 'MySQL']; satisfied=True; known=['PostgreSQL']; grammar=examples
- Source (required): • experience with gitops and kubernetes (helm, kustomize, or similar tooling)
  - Before: any_of ['Kubernetes']; satisfied=False; known=[]
  - After: any_of ['Kubernetes']; satisfied=False; known=[]; grammar=alternatives

Requirement penalty ledger before: `[{"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["kafka"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "equivalent", "skills": ["Kafka"], "source": "• experience building scalable, event\\\\-driven, or asynchronous architectures (e.g., kafka, rabbitmq, or equivalent)", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_3", "type": "any_of", "skills": ["Kubernetes"], "source": "• experience with gitops and kubernetes (helm, kustomize, or similar tooling)", "contribution": -3}]`

### Data Engineer - Senior Associate (`li-4369126870`)

- Changed: required_atomic_gaps, fit_score, fit_quality, apply_decision
- Attribution: satisfied alternative group, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 78.0 → 84.0; decision: manual_review → apply_now
- Required atomic gaps: ['Snowflake', 'Databricks', 'AWS', 'Google Cloud'] → ['AWS', 'Google Cloud']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): certification in cloud platforms \\[e.g., aws solutions architect, aws data engineer, google professional cloud architect, gcp data engineer microsoft azure solutions architect, azure data engineer associate, snowflake core, snowflake databricks data engineer associate] is a plus
  - Before: all_of ['Snowflake', 'Databricks', 'AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']
  - After: any_of ['AWS', 'Google Cloud', 'Azure', 'Snowflake', 'Databricks']; satisfied=True; known=['Azure']; grammar=examples
- Source (required): developing and deploying scalable data storage solutions using aws, azure and gcp services
  - Before: all_of ['AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']
  - After: all_of ['AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']; grammar=conjunction_or_enumeration
- Source (required): implementing data integration solutions using aws glue, aws lambda, azure data factory, azure functions, gcp functions, gcp dataproc, dataflow
  - Before: all_of ['AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']
  - After: all_of ['AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Google Cloud", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Google Cloud", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}]`

### Data Engineering Solutions Lead (`li-4370559928`)

- Changed: required_atomic_gaps, required_group_gaps, fit_score, fit_quality, apply_decision, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, mixed-grammar ambiguity, legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 58.43 → 52.43; decision: manual_review → skip
- Required atomic gaps: ['Spark', 'Kafka', 'Databricks', 'Airflow', 'AWS'] → ['Databricks', 'AWS', 'Spark', 'Kafka']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 3

- Source (required): design and implement scalable and reliable data pipelines to ingest, process, and store diverse data at scale, using technologies such as apache spark, hadoop, and kafka.
  - Before: all_of ['Spark', 'Kafka']; satisfied=False; known=[]
  - After: any_of ['Spark', 'Kafka']; satisfied=False; known=[]; grammar=examples
- Source (required): work within cloud environments like aws or azure to leverage services including but not limited to ec2, rds, s3, lambda, and azure data lake for efficient data handling and processing.
  - Before: any_of ['AWS', 'Azure']; satisfied=True; known=['Azure']
  - After: ambiguous ['AWS', 'Azure']; satisfied=None; known=['Azure']; grammar=mixed_conjunction_alternative
- Source (required): develop and optimize data models and storage solutions (databricks, data lakehouses) to support operational and analytical applications, ensuring data quality and accessibility.
  - Before: all_of ['Databricks']; satisfied=False; known=[]
  - After: all_of ['Databricks']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): utilize etl tools and frameworks (e.g., apache airflow, fivetran) to automate data workflows, ensuring efficient data integration and timely availability of data for analytics.
  - Before: all_of ['Airflow']; satisfied=False; known=[]
  - After: any_of ['Airflow']; satisfied=False; known=[]; grammar=examples
- Source (required): collaborate closely with data scientists, providing the data infrastructure and tools needed for complex analytical models, leveraging python or r for data processing scripts.
  - Before: any_of ['Python']; satisfied=True; known=['Python']
  - After: any_of ['Python']; satisfied=True; known=['Python']; grammar=alternatives
- Source (required): demonstrated experience designing and implementing medallion architecture in a databricks lakehouse environment, including layer transitions, data quality enforcement, and optimization strategies.
  - Before: all_of ['Databricks']; satisfied=False; known=[]
  - After: any_of ['Databricks']; satisfied=False; known=[]; grammar=examples
- Source (required): comprehensive knowledge of platforms and services like databricks, dataiku, and aws native data offerings required
  - Before: all_of ['Databricks', 'AWS']; satisfied=False; known=[]
  - After: all_of ['Databricks', 'AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): solid experience with big data technologies (apache spark, hadoop, kafka) and cloud services (aws, azure) related to data processing and storage required
  - Before: all_of ['Spark', 'Kafka', 'AWS', 'Azure']; satisfied=False; known=['Azure']
  - After: all_of ['Spark', 'Kafka', 'AWS', 'Azure']; satisfied=False; known=['Azure']; grammar=conjunction_or_enumeration
- Source (required): strong experience in aws cloud services, with hands\\-on experience in integrating cloud storage and compute services with databricks required
  - Before: all_of ['Databricks', 'AWS']; satisfied=False; known=[]
  - After: all_of ['AWS', 'Databricks']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): proficient in sql and programming languages relevant to data engineering (python, java, scala) required
  - Before: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']; grammar=conjunction_or_enumeration
- Previous source (required), removed/resegmented: aws certified solution architect (all_of)
- Source (preferred): aws certified solution architect preferred
  - Before: no matching sentence-level group
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): databricks certified associate developer for apache spark preferred
  - Before: no matching sentence-level group
  - After: all_of ['Databricks', 'Spark']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Previous source (preferred), removed/resegmented: databricks certified associate developer for apache spark (all_of)

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kafka", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -9, "skills": ["aws", "kafka", "spark"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kafka", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "any_of", "skills": ["Spark", "Kafka"], "source": "design and implement scalable and reliable data pipelines to ingest, process, and store diverse data at scale, using technologies such as apache spark, hadoop, and kafka.", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_4", "type": "any_of", "skills": ["Airflow"], "source": "utilize etl tools and frameworks (e.g., apache airflow, fivetran) to automate data workflows, ensuring efficient data integration and timely availability of data for analytics.", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_6", "type": "any_of", "skills": ["Databricks"], "source": "demonstrated experience designing and implementing medallion architecture in a databricks lakehouse environment, including layer transitions, data quality enforcement, and optimization strategies.", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -9, "skills": ["aws", "kafka", "spark"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -3.0, "skills": ["aws", "spark"]}]`

### Senior Software Engineer Specialist - United States (`li-4427377748`)

- Changed: required_group_gaps, fit_score, fit_quality, apply_decision, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, equivalent requirement handling, legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 57.51 → 51.51; decision: manual_review → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 2

- Source (required): experience building scalable, event\\-driven, or asynchronous architectures (e.g., kafka, rabbitmq, or equivalent)
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (required): experience with relational and/or nosql databases (e.g., postgresql, mysql, mongodb)
  - Before: any_of ['PostgreSQL', 'MySQL']; satisfied=True; known=['PostgreSQL']
  - After: any_of ['PostgreSQL', 'MySQL']; satisfied=True; known=['PostgreSQL']; grammar=examples
- Source (required): experience with gitops and kubernetes (helm, kustomize, or similar tooling)
  - Before: any_of ['Kubernetes']; satisfied=False; known=[]
  - After: any_of ['Kubernetes']; satisfied=False; known=[]; grammar=alternatives

Requirement penalty ledger before: `[{"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["kafka"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "equivalent", "skills": ["Kafka"], "source": "experience building scalable, event\\\\-driven, or asynchronous architectures (e.g., kafka, rabbitmq, or equivalent)", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_3", "type": "any_of", "skills": ["Kubernetes"], "source": "experience with gitops and kubernetes (helm, kustomize, or similar tooling)", "contribution": -3}]`

### Data Engineer (`li-4428735984`)

- Changed: required_group_gaps, fit_score, apply_decision, alignment_score
- Attribution: equivalent requirement handling, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 78.92 → 75.92; decision: apply_now → manual_review
- Required atomic gaps: ['Airflow', 'dbt'] → ['dbt', 'Airflow']
- Preferred atomic gaps: ['AWS', 'Google Cloud'] → ['AWS', 'Google Cloud']
- Required group gaps: 0 → 1

- Source (required): strong sql expertise with experience in handling large, complex data sets.
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): hands\\-on experience with data warehousing platforms (snowflake, redshift, bigquery, teradata, or equivalent).
  - Before: equivalent ['Snowflake', 'Redshift', 'BigQuery']; satisfied=False; known=[]
  - After: equivalent ['Snowflake', 'Redshift', 'BigQuery']; satisfied=False; known=[]; grammar=or_equivalent
- Source (required): proficiency in etl/elt tools (informatica, dbt, airflow, talend, etc.).
  - Before: all_of ['Airflow', 'dbt']; satisfied=False; known=[]
  - After: all_of ['dbt', 'Airflow']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): strong programming skills in python/scala/java for data processing.
  - Before: all_of ['Python']; satisfied=True; known=['Python']
  - After: all_of ['Python']; satisfied=True; known=['Python']; grammar=conjunction_or_enumeration
- Source (required): strong hands\\-on experience with sql and relational databases; familiarity with nosql databases is a plus
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (preferred): cloud platform knowledge (aws/google cloud platform/azure).
  - Before: all_of ['AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']
  - After: all_of ['AWS', 'Google Cloud', 'Azure']; satisfied=False; known=['Azure']; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "AWS", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Google Cloud", "contribution": -0.5}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "AWS", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Google Cloud", "contribution": -0.5}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_2", "type": "equivalent", "skills": ["Snowflake", "Redshift", "BigQuery"], "source": "hands\\\\-on experience with data warehousing platforms (snowflake, redshift, bigquery, teradata, or equivalent).", "contribution": -3}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

### Lead Data Engineer (`in-83644ce3aae8e9c6`)

- Changed: required_group_gaps, preferred_group_gaps, fit_score, alignment_score
- Attribution: unsatisfied alternative group, equivalent requirement handling, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 78.5 → 66.5; decision: manual_review → manual_review
- Required atomic gaps: [] → []
- Preferred atomic gaps: ['Spark', 'Tableau', 'dbt'] → ['Spark', 'Tableau', 'dbt']
- Required group gaps: 0 → 4

- Source (required): support both batch and streaming data architectures using technologies such as kafka, event hub, or equivalent.
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (required): advanced sql skills and proficiency with data transformation techniques.
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): strong python programming skills for data processing and automation.
  - Before: all_of ['Python']; satisfied=True; known=['Python']
  - After: all_of ['Python']; satisfied=True; known=['Python']; grammar=conjunction_or_enumeration
- Source (required): hands\\-on experience with snowflake, including:
  - Before: any_of ['Snowflake']; satisfied=False; known=[]
  - After: any_of ['Snowflake']; satisfied=False; known=[]; grammar=examples
- Source (required): experience migrating from bigquery or similar columnar data warehouse technologies.
  - Before: any_of ['BigQuery']; satisfied=False; known=[]
  - After: any_of ['BigQuery']; satisfied=False; known=[]; grammar=alternatives
- Source (required): experience with batch and streaming data processing platforms such as kafka, event hub, or equivalent.
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (preferred): experience with databricks, including:
  - Before: any_of ['Databricks']; satisfied=False; known=[]
  - After: any_of ['Databricks']; satisfied=False; known=[]; grammar=examples
- Source (preferred): + spark\\-based pipelines
  - Before: all_of ['Spark']; satisfied=False; known=[]
  - After: all_of ['Spark']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): experience with spark, scala, or pyspark.
  - Before: any_of ['Spark']; satisfied=False; known=[]
  - After: any_of ['Spark']; satisfied=False; known=[]; grammar=alternatives
- Source (preferred): familiarity with tableau.
  - Before: all_of ['Tableau']; satisfied=False; known=[]
  - After: all_of ['Tableau']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): experience with dbt (data build tool) for transformation layer management.
  - Before: all_of ['dbt']; satisfied=False; known=[]
  - After: all_of ['dbt']; satisfied=False; known=[]; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Spark", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Tableau", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "dbt", "contribution": -0.5}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["kafka"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Spark", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Tableau", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "dbt", "contribution": -0.5}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "equivalent", "skills": ["Kafka"], "source": "support both batch and streaming data architectures using technologies such as kafka, event hub, or equivalent.", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_4", "type": "any_of", "skills": ["Snowflake"], "source": "hands\\\\-on experience with snowflake, including:", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_5", "type": "any_of", "skills": ["BigQuery"], "source": "experience migrating from bigquery or similar columnar data warehouse technologies.", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_6", "type": "equivalent", "skills": ["Kafka"], "source": "experience with batch and streaming data processing platforms such as kafka, event hub, or equivalent.", "contribution": -3}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["spark"]}]`

### Lead Data Engineer (`in-b8c9a5b25683858c`)

- Changed: required_group_gaps, preferred_group_gaps, fit_score, alignment_score
- Attribution: unsatisfied alternative group, equivalent requirement handling, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 78.5 → 66.5; decision: manual_review → manual_review
- Required atomic gaps: [] → []
- Preferred atomic gaps: ['Spark', 'Tableau', 'dbt'] → ['Spark', 'Tableau', 'dbt']
- Required group gaps: 0 → 4

- Source (required): support both batch and streaming data architectures using technologies such as kafka, event hub, or equivalent.
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (required): advanced sql skills and proficiency with data transformation techniques.
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): strong python programming skills for data processing and automation.
  - Before: all_of ['Python']; satisfied=True; known=['Python']
  - After: all_of ['Python']; satisfied=True; known=['Python']; grammar=conjunction_or_enumeration
- Source (required): hands\\-on experience with snowflake, including:
  - Before: any_of ['Snowflake']; satisfied=False; known=[]
  - After: any_of ['Snowflake']; satisfied=False; known=[]; grammar=examples
- Source (required): experience migrating from bigquery or similar columnar data warehouse technologies.
  - Before: any_of ['BigQuery']; satisfied=False; known=[]
  - After: any_of ['BigQuery']; satisfied=False; known=[]; grammar=alternatives
- Source (required): experience with batch and streaming data processing platforms such as kafka, event hub, or equivalent.
  - Before: equivalent ['Kafka']; satisfied=False; known=[]
  - After: equivalent ['Kafka']; satisfied=False; known=[]; grammar=or_equivalent
- Source (preferred): experience with databricks, including:
  - Before: any_of ['Databricks']; satisfied=False; known=[]
  - After: any_of ['Databricks']; satisfied=False; known=[]; grammar=examples
- Source (preferred): + spark\\-based pipelines
  - Before: all_of ['Spark']; satisfied=False; known=[]
  - After: all_of ['Spark']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): experience with spark, scala, or pyspark.
  - Before: any_of ['Spark']; satisfied=False; known=[]
  - After: any_of ['Spark']; satisfied=False; known=[]; grammar=alternatives
- Source (preferred): familiarity with tableau.
  - Before: all_of ['Tableau']; satisfied=False; known=[]
  - After: all_of ['Tableau']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): experience with dbt (data build tool) for transformation layer management.
  - Before: all_of ['dbt']; satisfied=False; known=[]
  - After: all_of ['dbt']; satisfied=False; known=[]; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Spark", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Tableau", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "dbt", "contribution": -0.5}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["kafka"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Spark", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Tableau", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "dbt", "contribution": -0.5}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "equivalent", "skills": ["Kafka"], "source": "support both batch and streaming data architectures using technologies such as kafka, event hub, or equivalent.", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_4", "type": "any_of", "skills": ["Snowflake"], "source": "hands\\\\-on experience with snowflake, including:", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_5", "type": "any_of", "skills": ["BigQuery"], "source": "experience migrating from bigquery or similar columnar data warehouse technologies.", "contribution": -3}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_6", "type": "equivalent", "skills": ["Kafka"], "source": "experience with batch and streaming data processing platforms such as kafka, event hub, or equivalent.", "contribution": -3}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["spark"]}]`

### Data Engineer (Databricks + Informatica + Azure) (`li-4429994053`)

- Changed: required_group_gaps, fit_score, apply_decision, ai_review_required, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, mixed-grammar ambiguity, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 84.93 → 81.93; decision: apply_now → manual_review
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 1

- Source (required): strong experience with databricks or similar distributed data processing platforms
  - Before: any_of ['Databricks']; satisfied=False; known=[]
  - After: any_of ['Databricks']; satisfied=False; known=[]; grammar=alternatives
- Source (required): strong proficiency in sql, python, and pyspark (or equivalent distributed processing languages) for data transformation and processing
  - Before: equivalent ['SQL', 'Python', 'Spark']; satisfied=True; known=['SQL', 'Python']
  - After: ambiguous ['SQL', 'Python', 'Spark']; satisfied=None; known=['SQL', 'Python']; grammar=mixed_conjunction_alternative
- Source (required): solid knowledge of cloud and hybrid relational database systems such as ms sql server, postgresql, oracle, azure sql, aws rds, or comparable engines
  - Before: any_of ['SQL', 'PostgreSQL', 'SQL Server', 'AWS', 'Azure']; satisfied=True; known=['SQL', 'PostgreSQL', 'SQL Server', 'Azure']
  - After: any_of ['SQL Server', 'PostgreSQL', 'Azure', 'SQL', 'AWS']; satisfied=True; known=['SQL Server', 'PostgreSQL', 'Azure', 'SQL']; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "any_of", "skills": ["Databricks"], "source": "strong experience with databricks or similar distributed data processing platforms", "contribution": -3}]`

### Global Data Engineer (`li-4430112480`)

- Changed: required_group_gaps, fit_score, fit_quality, apply_decision, ai_review_required
- Attribution: unsatisfied alternative group, mixed-grammar ambiguity, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 80.12 → 77.12; decision: apply_now → manual_review
- Required atomic gaps: ['Snowflake', 'Power BI'] → ['Snowflake', 'Power BI']
- Preferred atomic gaps: ['Airflow', 'dbt'] → ['Airflow', 'dbt']
- Required group gaps: 0 → 1

- Source (required): partner with cross\\-functional teams to manage and continuously improve a snowflake\\-based data warehouse.
  - Before: all_of ['Snowflake']; satisfied=False; known=[]
  - After: all_of ['Snowflake']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): develop well\\-structured, accessible datasets to deliver custom power bi dashboards.
  - Before: all_of ['Power BI']; satisfied=False; known=[]
  - After: all_of ['Power BI']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): proficiency in sql, and one or more data related languages such as r or python.
  - Before: any_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: ambiguous ['SQL', 'Python']; satisfied=None; known=['SQL', 'Python']; grammar=mixed_conjunction_alternative
- Source (required): skilled in creating dashboards and reports using tools such as power bi, tableau, or looker.
  - Before: no matching sentence-level group
  - After: any_of ['Power BI', 'Tableau']; satisfied=False; known=[]; grammar=examples
- Previous source (required), removed/resegmented: hands\\-on experience with cloud\\-based data platforms (snowflake (all_of)
- Source (preferred): hands\\-on experience with cloud\\-based data platforms (snowflake preferred), dbt, and orchestration tools like airflow.
  - Before: no matching sentence-level group
  - After: all_of ['Snowflake', 'dbt', 'Airflow']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Previous source (preferred), removed/resegmented: ), dbt, and orchestration tools like airflow. (all_of)
- Previous source (preferred), removed/resegmented: skilled in creating dashboards and reports using tools such as power bi, tableau, or looker. (any_of)

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Airflow", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "dbt", "contribution": -0.5}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Airflow", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "dbt", "contribution": -0.5}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_5", "type": "any_of", "skills": ["Power BI", "Tableau"], "source": "skilled in creating dashboards and reports using tools such as power bi, tableau, or looker.", "contribution": -3}]`

### Senior Data Engineer (`li-4420401901`)

- Changed: apply_decision, ai_review_required
- Attribution: satisfied alternative group, mixed-grammar ambiguity, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 92.0 → 92.0; decision: apply_now → manual_review
- Required atomic gaps: ['Power BI'] → ['Power BI']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): establish a comprehensive powerbi\\-based reporting framework to effectively narrate the story behind data.
  - Before: all_of ['Power BI']; satisfied=False; known=[]
  - After: all_of ['Power BI']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): experience: 3\\-6 years of hands\\-on experience as a data engineer, preferably working with the microsoft azure cloud platform.
  - Before: all_of ['Azure']; satisfied=True; known=['Azure']
  - After: all_of ['Azure']; satisfied=True; known=['Azure']; grammar=conjunction_or_enumeration
- Source (required): technical skills: proficient with the azure data stack, including azure databricks or snowflake, adls gen2 \\- lakehouse, azure data factory, sql server and power bi.
  - Before: any_of ['SQL', 'Snowflake', 'SQL Server', 'Databricks', 'Azure', 'Power BI']; satisfied=True; known=['SQL', 'SQL Server', 'Azure']
  - After: ambiguous ['Azure', 'Databricks', 'Snowflake', 'SQL Server', 'Power BI']; satisfied=None; known=['Azure', 'SQL Server']; grammar=mixed_conjunction_alternative
- Source (required): programming skills: skilled in python, sql, or scala for data manipulation and transformation.
  - Before: any_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: any_of ['Python', 'SQL']; satisfied=True; known=['Python', 'SQL']; grammar=alternatives

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}]`

### Data Engineer (Palantir) (`li-4429057139`)

- Changed: apply_decision, ai_review_required, alignment_score, label
- Attribution: mixed-grammar ambiguity, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 93.85 → 93.85; decision: apply_now → manual_review
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): good to excellent knowledge of python (ideally experience with pyspark or pandas) and are highly proficient in sql.
  - Before: any_of ['SQL', 'Python', 'Spark']; satisfied=True; known=['SQL', 'Python']
  - After: ambiguous ['Python', 'Spark', 'SQL']; satisfied=None; known=['Python', 'SQL']; grammar=mixed_conjunction_alternative

Requirement penalty ledger before: `[{"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["spark"]}]`

Requirement penalty ledger after: `[]`

### Data & Integration Engineer (`li-4430448809`)

- Changed: apply_decision, ai_review_required
- Attribution: mixed-grammar ambiguity, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 92.98 → 92.98; decision: apply_now → manual_review
- Required atomic gaps: [] → []
- Preferred atomic gaps: ['AWS'] → ['AWS']
- Required group gaps: 0 → 0

- Previous source (required), removed/resegmented: strong sql and scripting skills (python or javascript (any_of)
- Source (preferred): strong sql and scripting skills (python or javascript preferred).
  - Before: no matching sentence-level group
  - After: ambiguous ['SQL', 'Python']; satisfied=None; known=['SQL', 'Python']; grammar=mixed_conjunction_alternative
- Source (preferred):  experience with cloud\\-based integration (azure, aws).
  - Before: all_of ['AWS', 'Azure']; satisfied=False; known=['Azure']
  - After: all_of ['Azure', 'AWS']; satisfied=False; known=['Azure']; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "AWS", "contribution": -0.5}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "AWS", "contribution": -0.5}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

### Data Engineer with AWS || onsite in NJ, TX, AZ, RI || W2 (`li-4429359989`)

- Changed: required_atomic_gaps, preferred_atomic_gaps, fit_score, fit_quality, apply_decision, alignment_score
- Attribution: legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 65.64 → 53.14; decision: manual_review → skip
- Required atomic gaps: ['AWS', 'Redshift', 'Spark', 'Kafka', 'Airflow'] → ['AWS', 'Redshift', 'Spark', 'Kafka', 'Airflow', 'MySQL', 'Snowflake', 'Terraform', 'Docker', 'Kubernetes']
- Preferred atomic gaps: ['Docker', 'Kubernetes', 'MySQL', 'Snowflake', 'Terraform'] → []
- Required group gaps: 0 → 0

- Source (required): aws cloud services
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): aws glue, amazon s3, aws lambda, amazon redshift, amazon emr, amazon athena, aws lake formation, aws step functions, amazon kinesis, amazon rds, amazon dynamodb, amazon cloudwatch, aws iam, aws data pipeline
  - Before: all_of ['AWS', 'Redshift']; satisfied=False; known=[]
  - After: all_of ['AWS', 'Redshift']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): apache spark (pyspark/spark sql)
  - Before: all_of ['SQL', 'Spark']; satisfied=False; known=['SQL']
  - After: all_of ['Spark', 'SQL']; satisfied=False; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): apache kafka
  - Before: all_of ['Kafka']; satisfied=False; known=[]
  - After: all_of ['Kafka']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): apache airflow
  - Before: all_of ['Airflow']; satisfied=False; known=[]
  - After: all_of ['Airflow']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): python (advanced)
  - Before: all_of ['Python']; satisfied=True; known=['Python']
  - After: all_of ['Python']; satisfied=True; known=['Python']; grammar=conjunction_or_enumeration
- Source (required): sql (expert level)
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): sql server
  - Before: no matching sentence-level group
  - After: all_of ['SQL Server']; satisfied=True; known=['SQL Server']; grammar=conjunction_or_enumeration
- Source (required): postgresql
  - Before: no matching sentence-level group
  - After: all_of ['PostgreSQL']; satisfied=True; known=['PostgreSQL']; grammar=conjunction_or_enumeration
- Source (required): mysql
  - Before: no matching sentence-level group
  - After: all_of ['MySQL']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): snowflake
  - Before: no matching sentence-level group
  - After: all_of ['Snowflake']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): redshift
  - Before: no matching sentence-level group
  - After: all_of ['Redshift']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): snowflake schema
  - Before: no matching sentence-level group
  - After: all_of ['Snowflake']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): terraform
  - Before: no matching sentence-level group
  - After: all_of ['Terraform']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): docker
  - Before: no matching sentence-level group
  - After: all_of ['Docker']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): kubernetes
  - Before: no matching sentence-level group
  - After: all_of ['Kubernetes']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): 5\\+ years of hands\\-on aws cloud experience.
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): advanced sql and python programming skills.
  - Before: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']; grammar=conjunction_or_enumeration
- Previous source (preferred), removed/resegmented: sql server (all_of)
- Previous source (preferred), removed/resegmented: postgresql (all_of)
- Previous source (preferred), removed/resegmented: mysql (all_of)
- Previous source (preferred), removed/resegmented: snowflake (all_of)
- Previous source (preferred), removed/resegmented: redshift (all_of)
- Previous source (preferred), removed/resegmented: snowflake schema (all_of)
- Previous source (preferred), removed/resegmented: terraform (all_of)
- Previous source (preferred), removed/resegmented: docker (all_of)
- Previous source (preferred), removed/resegmented: kubernetes (all_of)

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Redshift", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kafka", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Docker", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Kubernetes", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "MySQL", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -0.5}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Terraform", "contribution": -0.5}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -9, "skills": ["aws", "kafka", "spark"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Redshift", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kafka", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "MySQL", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Terraform", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Docker", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kubernetes", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -9, "skills": ["aws", "kafka", "spark"]}]`

### Senior Accounts Payable Analyst (`in-a2232dcbee24f494`)

- Changed: fit_score, fit_quality, apply_decision, alignment_score
- Attribution: legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 56.43 → 48.43; decision: manual_review → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Inline-preferred section-boundary correction also affected experience/section-scoped alignment.
- Years required: None → 7.
- Section alignment events: [] → [{'rule_id': 'alignment:years', 'kind': 'alignment', 'contribution': -5, 'years': 7}].
- Section context source: * High school diploma or general educational degree (GED) is required. Bachelor’s degree in accounting, finance, or related field is preferred. A combination of alternative education and experience may be considered in lieu of the formal education requirements.
- Section context source: * Certified Accounts Payable Professional (CAPP), Accredited Payables Specialist (APS), or Accredited Payables Manager (APM) through IOFM certification is preferred.
- Section context source: * Minimum of 7 years of experience in processive accounts payable and general accounting is required.
- Section context source: * Minimum of 3 years of experience in senior individual contributor capacity owning the full AP function in healthcare or regulated industry is preferred.
- Section context source: * Experience with at least one AP automation/invoice capture platform (Bill.com, Concure Invoice, etc.) is preferred.
- Section context source: * Working knowledge of Medicare cost reporting and CMS reimbursement principles is preferred.
- Section context source: * 7 year(s): Experience in processive accounts payable and general accounting

Requirement penalty ledger before: `[]`

Requirement penalty ledger after: `[]`

### Principal Data Engineer (`li-4430985604`)

- Changed: required_atomic_gaps, fit_score, fit_quality, apply_decision
- Attribution: legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 60.61 → 54.61; decision: manual_review → skip
- Required atomic gaps: ['Snowflake', 'dbt', 'Airflow'] → ['AWS', 'Airflow', 'Kafka', 'Snowflake', 'dbt']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): aws data services: s3, glue, athena, mwaa (airflow), kafka (msk), lambda, emr, cloudwatch; aws certification a plus
  - Before: any_of ['Airflow', 'Kafka', 'AWS']; satisfied=False; known=[]
  - After: all_of ['AWS', 'Airflow', 'Kafka']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): snowflake data cloud: account administration, virtual warehouse strategies, role\\-based access control, data sharing, time travel, and zero\\-copy cloning
  - Before: all_of ['Snowflake']; satisfied=False; known=[]
  - After: all_of ['Snowflake']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): dbt: managing multi\\-repository projects, authoring and maintaining models, macros, incremental strategies, testing frameworks, and semantic layer / semantic model development
  - Before: all_of ['dbt']; satisfied=False; known=[]
  - After: all_of ['dbt']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): proficiency in sql and python
  - Before: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: all_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']; grammar=conjunction_or_enumeration
- Previous source (required), removed/resegmented: orchestration and scheduling tools (airflow / mwaa (all_of)
- Source (preferred): orchestration and scheduling tools (airflow / mwaa preferred)
  - Before: no matching sentence-level group
  - After: all_of ['Airflow']; satisfied=False; known=[]; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "kafka"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kafka", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Snowflake", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "kafka"]}]`

### Lead Analyst Data Engineer (`in-1f5c8418605bc555`)

- Changed: required_atomic_gaps, fit_score, fit_quality, apply_decision
- Attribution: legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 56.5 → 53.5; decision: manual_review → skip
- Required atomic gaps: ['AWS', 'Databricks', 'Spark', 'Power BI'] → ['AWS', 'Redshift', 'Databricks', 'Spark', 'Power BI']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): 7–10 years of implementation experience in cloud data architecture, with at least 5 years in aws environments.
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions.
  - Before: any_of ['AWS', 'Redshift']; satisfied=False; known=[]
  - After: all_of ['AWS', 'Redshift']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): extensive experience working with databricks.
  - Before: all_of ['Databricks']; satisfied=False; known=[]
  - After: all_of ['Databricks']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): strong skills in sql (t\\-sql), python (pyspark/pandas), dax, power query (m), pl/sql.
  - Before: all_of ['SQL', 'Python', 'Spark']; satisfied=False; known=['SQL', 'Python']
  - After: all_of ['SQL', 'Python', 'Spark']; satisfied=False; known=['SQL', 'Python']; grammar=conjunction_or_enumeration
- Source (required): experience with databases: sql server, oracle, postgresql, azure sql, teradata.
  - Before: any_of ['SQL', 'PostgreSQL', 'SQL Server', 'Azure']; satisfied=True; known=['SQL', 'PostgreSQL', 'SQL Server', 'Azure']
  - After: all_of ['SQL Server', 'PostgreSQL', 'Azure', 'SQL']; satisfied=True; known=['SQL Server', 'PostgreSQL', 'Azure', 'SQL']; grammar=conjunction_or_enumeration
- Source (required): skilled in power bi, git, visual studio code, ssms.
  - Before: all_of ['Power BI']; satisfied=False; known=[]
  - After: all_of ['Power BI']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): aws and databricks certifications.
  - Before: all_of ['Databricks', 'AWS']; satisfied=False; known=[]
  - After: all_of ['AWS', 'Databricks']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): designing and implementing scalable data architectures in aws and databricks.
  - Before: all_of ['Databricks', 'AWS']; satisfied=False; known=[]
  - After: all_of ['AWS', 'Databricks']; satisfied=False; known=[]; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "spark"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Redshift", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "spark"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

### Forward Deployed AI Engineer (`in-07070bc3c705ab9f`)

- Changed: preferred_group_gaps
- Attribution: unsatisfied alternative group, satisfied alternative group, legacy/group reconciliation
- Lane: wrong_lane → wrong_lane; fit: 15 → 15; decision: skip → skip
- Required atomic gaps: ['Kubernetes', 'AWS', 'Google Cloud', 'Terraform'] → ['Kubernetes', 'AWS', 'Google Cloud', 'Terraform']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): kubernetes
  - Before: all_of ['Kubernetes']; satisfied=False; known=[]
  - After: all_of ['Kubernetes']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): cloud environments (aws/gcp and azure)
  - Before: all_of ['AWS', 'Azure', 'Google Cloud']; satisfied=False; known=['Azure']
  - After: all_of ['AWS', 'Google Cloud', 'Azure']; satisfied=False; known=['Azure']; grammar=conjunction_or_enumeration
- Source (required): infrastructure\\-as\\-code (like terraform/pulumi)
  - Before: all_of ['Terraform']; satisfied=False; known=[]
  - After: all_of ['Terraform']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): building kubernetes and cloud native applications
  - Before: all_of ['Kubernetes']; satisfied=False; known=[]
  - After: all_of ['Kubernetes']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): experience with deploying applications on kubernetes inside of air\\-gapped or secure environments.
  - Before: any_of ['Kubernetes']; satisfied=False; known=[]
  - After: any_of ['Kubernetes']; satisfied=False; known=[]; grammar=alternatives
- Source (preferred): experience with information retrieval fundamentals including knowledge of keyword and vector based search, document parsing and chunking, document reranking, and sql/nosql search engines.
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: any_of ['SQL']; satisfied=True; known=['SQL']; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kubernetes", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Google Cloud", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Terraform", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kubernetes", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Google Cloud", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Terraform", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}]`

### Senior Buyer (`in-14bc808042da3c3f`)

- Changed: alignment_score
- Attribution: legacy/group reconciliation
- Lane: wrong_lane → wrong_lane; fit: 15 → 15; decision: skip → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Inline-preferred section-boundary correction also affected experience/section-scoped alignment.
- Years required: None → 8.
- Section alignment events: [] → [{'rule_id': 'alignment:years', 'kind': 'alignment', 'contribution': -5, 'years': 8}].
- Section context source: In this position, you will develop and execute multi\\-year, cross\\-functional (e.g. product line leaders, material managers, engineers, operations, and quality) supply chain strategies. You will minimize total landed cost (material cost, freight, duties, inventory, etc.) impact by containing costs through supply base management processes and strategies working with suppliers and the company. This role will also facilitate cross\\-functional communications to drive optimized sourcing strategies supporting new product development programs.
- Section context source: * Bachelor’s degree in Business Administration, Engineering, Materials, Procurement, Supply Chain Management, or related degree. MBA is preferred, but not required.
- Section context source: * Minimum of 8 years of progressive experience in buying and sourcing Capital expenditures or test equipment in the Aerospace industry is required. Space specific industry experience preferred.
- Section context source: * Bachelor’s degree in Business Administration, Engineering, Materials, Procurement, Supply Chain Management, or related degree. MBA is preferred, but not required.
- Section context source: * Minimum of 8 years of progressive experience in buying and sourcing Capital expenditures or test equipment in the Aerospace industry.

Requirement penalty ledger before: `[]`

Requirement penalty ledger after: `[]`

### Logistics Systems Administrator (`in-17ac43279752afd3`)

- Changed: required_atomic_gaps, required_group_gaps
- Attribution: unsatisfied alternative group, legacy/group reconciliation
- Lane: wrong_lane → wrong_lane; fit: 15 → 15; decision: skip → skip
- Required atomic gaps: ['Power BI'] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 1

- Source (required): proficiency with sql databases, interface engines, and edi platforms
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): experience with sql databases, interface engines, and edi platforms
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): experience with process automation and reporting tools (e.g., power bi)
  - Before: all_of ['Power BI']; satisfied=False; known=[]
  - After: any_of ['Power BI']; satisfied=False; known=[]; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Power BI", "contribution": -3}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_3", "type": "any_of", "skills": ["Power BI"], "source": "experience with process automation and reporting tools (e.g., power bi)", "contribution": -3}]`

### Manager - Financial Planning and Analysis (`in-1b2d73ace8b12a7b`)

- Changed: ai_review_required
- Attribution: mixed-grammar ambiguity, legacy/group reconciliation
- Lane: wrong_lane → wrong_lane; fit: 15 → 15; decision: skip → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (preferred): working knowledge or willingness to learn sql and data tools (e.g., power bi, quickbase).
  - Before: any_of ['SQL', 'Power BI']; satisfied=True; known=['SQL']
  - After: ambiguous ['SQL', 'Power BI']; satisfied=None; known=['SQL']; grammar=mixed_conjunction_alternative

Requirement penalty ledger before: `[]`

Requirement penalty ledger after: `[]`

### Senior Software Development Engineer (Site Reliability) (`in-297ddc2108f979e1`)

- Changed: required_atomic_gaps
- Attribution: satisfied alternative group, legacy/group reconciliation
- Lane: wrong_lane → wrong_lane; fit: 15 → 15; decision: skip → skip
- Required atomic gaps: ['Kubernetes'] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): cloud platforms, preferably azure, including aks and kubernetes
  - Before: all_of ['Azure', 'Kubernetes']; satisfied=False; known=['Azure']
  - After: any_of ['Azure', 'Kubernetes']; satisfied=True; known=['Azure']; grammar=examples
- Source (required): scripting experience with python, bash, or powershell.
  - Before: any_of ['Python']; satisfied=True; known=['Python']
  - After: any_of ['Python']; satisfied=True; known=['Python']; grammar=alternatives

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kubernetes", "contribution": -3}]`

Requirement penalty ledger after: `[]`

### Engineer III, Software/Web Development (`in-38cc50c3291fa355`)

- Changed: required_group_gaps
- Attribution: unsatisfied alternative group, legacy/group reconciliation
- Lane: bridge_lane → bridge_lane; fit: 65 → 65; decision: manual_review → manual_review
- Required atomic gaps: ['AWS'] → ['AWS']
- Preferred atomic gaps: ['Terraform'] → ['Terraform']
- Required group gaps: 0 → 1

- Source (required): develops application services on aws, integrating with cloud\\-native services (e.g., lambda, s3, dynamodb) to deliver scalable, secure, and cost\\-effective solutions.
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: any_of ['AWS']; satisfied=False; known=[]; grammar=examples
- Source (required): 3\\+ years of working with sql and nosql databases
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): 3\\+ years working with the following aws services (ec2, lambda, s3, dynamodb, cloudwatch
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): familiar with infrastructure\\-as\\-code and terraform.
  - Before: all_of ['Terraform']; satisfied=False; known=[]
  - After: all_of ['Terraform']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): familiarity with event\\-driven architectures on aws, pub/sub (sns/sqs), message queues, and streaming data ingestion, and the tradeoffs between these patterns.
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Terraform", "contribution": -0.5}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Terraform", "contribution": -0.5}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "any_of", "skills": ["AWS"], "source": "develops application services on aws, integrating with cloud\\\\-native services (e.g., lambda, s3, dynamodb) to deliver scalable, secure, and cost\\\\-effective solutions.", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

### Senior Analytics Engineer (`in-435894c3393cdbf3`)

- Changed: required_atomic_gaps, required_group_gaps, fit_score, fit_quality, alignment_score, label
- Attribution: unsatisfied alternative group, satisfied alternative group, legacy/group reconciliation
- Lane: secondary_lane → secondary_lane; fit: 72.64 → 81.64; decision: manual_review → manual_review
- Required atomic gaps: ['BigQuery', 'Airflow', 'Spark', 'Kubernetes'] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 1

- Source (required): 7\\+ years of experience writing expert level sql within database systems such as bigquery, sap hana, teradata
  - Before: all_of ['SQL', 'BigQuery']; satisfied=False; known=['SQL']
  - After: any_of ['SQL', 'BigQuery']; satisfied=True; known=['SQL']; grammar=examples
- Source (required): 5\\+ years of experience with python or other object\\-oriented languages in an analytics engineering setting
  - Before: any_of ['Python']; satisfied=True; known=['Python']
  - After: any_of ['Python']; satisfied=True; known=['Python']; grammar=alternatives
- Source (required): 5\\+ years of experience with data, orchestration, and pipeline engineering services such as airflow, spark, kubernetes, preferably composer / dataproc
  - Before: all_of ['Airflow', 'Spark', 'Kubernetes']; satisfied=False; known=[]
  - After: any_of ['Airflow', 'Spark', 'Kubernetes']; satisfied=False; known=[]; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "BigQuery", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Airflow", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Spark", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Kubernetes", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["spark"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_3", "type": "any_of", "skills": ["Airflow", "Spark", "Kubernetes"], "source": "5\\\\+ years of experience with data, orchestration, and pipeline engineering services such as airflow, spark, kubernetes, preferably composer / dataproc", "contribution": -3}]`

### Senior Data Engineer (`in-45738cf915b51235`)

- Changed: required_atomic_gaps, fit_score, alignment_score
- Attribution: satisfied alternative group, mixed-grammar ambiguity, legacy/group reconciliation
- Lane: target_lane → target_lane; fit: 82.38 → 85.38; decision: manual_review → manual_review
- Required atomic gaps: ['AWS'] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): proven experience as a data engineer or similar role with a focus on big data technologies such as hadoop, spark, hive, and azure data lake.
  - Before: any_of ['Spark', 'Azure']; satisfied=True; known=['Azure']
  - After: ambiguous ['Spark', 'Azure']; satisfied=None; known=['Azure']; grammar=mixed_conjunction_alternative
- Source (required): strong proficiency in sql (including microsoft sql server and oracle), python, java, bash (unix shell), shell scripting, and vba for automation and analysis tasks.
  - Before: all_of ['SQL', 'Python', 'SQL Server']; satisfied=True; known=['SQL', 'Python', 'SQL Server']
  - After: any_of ['SQL', 'SQL Server', 'Python']; satisfied=True; known=['SQL', 'SQL Server', 'Python']; grammar=examples
- Source (required): familiarity with cloud platforms such as aws and azure for deploying large\\-scale data solutions.
  - Before: all_of ['AWS', 'Azure']; satisfied=False; known=['Azure']
  - After: any_of ['AWS', 'Azure']; satisfied=True; known=['Azure']; grammar=examples

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -6, "skills": ["aws", "spark"]}]`

Requirement penalty ledger after: `[]`

### Sr Engineer, Data - Finance Domain (`in-51c6cf515e58363e`)

- Changed: preferred_group_gaps, alignment_score
- Attribution: unsatisfied alternative group, satisfied alternative group, legacy/group reconciliation
- Lane: bridge_lane → bridge_lane; fit: 65 → 65; decision: manual_review → manual_review
- Required atomic gaps: ['dbt', 'Databricks'] → ['Databricks', 'dbt']
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Source (required): develop and maintain transformation logic and reusable data models using sql, python, databricks, dbt, and related data engineering tools.
  - Before: all_of ['SQL', 'Python', 'dbt', 'Databricks']; satisfied=False; known=['SQL', 'Python']
  - After: all_of ['SQL', 'Python', 'Databricks', 'dbt']; satisfied=False; known=['SQL', 'Python']; grammar=conjunction_or_enumeration
- Source (required): 4\\-7 years developing cloud solutions using data series; experience with cloud platforms (amazon web services, azure, or google cloud) (required)
  - Before: any_of ['AWS', 'Azure', 'Google Cloud']; satisfied=True; known=['Azure']
  - After: any_of ['AWS', 'Azure', 'Google Cloud']; satisfied=True; known=['Azure']; grammar=alternatives
- Source (required): proven track record in sql, nosql, and/or relational database design and development (required)
  - Before: any_of ['SQL']; satisfied=True; known=['SQL']
  - After: any_of ['SQL']; satisfied=True; known=['SQL']; grammar=alternatives
- Source (required): 4\\-7 years advanced knowledge and experience in building sophisticated data pipelines with python, experience in languages such as sql, dax python, java, scala, and/or go (required)
  - Before: any_of ['SQL', 'Python']; satisfied=True; known=['SQL', 'Python']
  - After: any_of ['Python', 'SQL']; satisfied=True; known=['Python', 'SQL']; grammar=examples
- Source (required): experience developing scalable data models, transformation logic, and curated datasets using sql, python, databricks, or comparable data engineering technologies.
  - Before: any_of ['SQL', 'Python', 'Databricks']; satisfied=True; known=['SQL', 'Python']
  - After: any_of ['SQL', 'Python', 'Databricks']; satisfied=True; known=['SQL', 'Python']; grammar=alternatives
- Source (required): databricks dbrx (required)
  - Before: all_of ['Databricks']; satisfied=False; known=[]
  - After: all_of ['Databricks']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (required): dbt (data build tool) framework (required)
  - Before: all_of ['dbt']; satisfied=False; known=[]
  - After: all_of ['dbt']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): experience with azure data lake storage gen2, azure data factory, databricks workflows, delta lake, unity catalog, or delta live tables.
  - Before: any_of ['Databricks', 'Azure']; satisfied=True; known=['Azure']
  - After: any_of ['Azure', 'Databricks']; satisfied=True; known=['Azure']; grammar=alternatives
- Source (preferred): experience with dbt core, including model layering, testing, documentation, and lineage.
  - Before: all_of ['dbt']; satisfied=False; known=[]
  - After: any_of ['dbt']; satisfied=False; known=[]; grammar=examples
- Source (preferred): experience migrating legacy etl, reporting, or analytics workloads from tools such as alteryx, sas, ssis, informatica, ibm tm1, ssas, or on\\-premises sql server to modern cloud data platforms.
  - Before: any_of ['SQL', 'SQL Server']; satisfied=True; known=['SQL', 'SQL Server']
  - After: any_of ['SQL Server']; satisfied=True; known=['SQL Server']; grammar=examples
- Source (preferred): experience with gitlab ci/cd, azure devops, automated regression testing, or controlled promotion paths across environments.
  - Before: any_of ['Azure']; satisfied=True; known=['Azure']
  - After: any_of ['Azure']; satisfied=True; known=['Azure']; grammar=alternatives
- Source (preferred): familiarity with oracle erp, oracle ebpcs/bpm, snowflake, jira, confluence, microsoft teams, or related enterprise data and collaboration tools.
  - Before: any_of ['Snowflake']; satisfied=False; known=[]
  - After: any_of ['Snowflake']; satisfied=False; known=[]; grammar=alternatives
- Source (preferred): databricks, azure, aws, google cloud, or related cloud/data certification.
  - Before: any_of ['Databricks', 'AWS', 'Azure', 'Google Cloud']; satisfied=True; known=['Azure']
  - After: any_of ['Databricks', 'Azure', 'AWS', 'Google Cloud']; satisfied=True; known=['Azure']; grammar=alternatives
- Source (preferred): aws certified solutions architect, aws certified cloud practitioner or microsoft certified solutions associate (mcsa) (preferred)
  - Before: no matching sentence-level group
  - After: any_of ['AWS']; satisfied=False; known=[]; grammar=alternatives
- Source (preferred): dbt analytics or architect certification (preferred)
  - Before: no matching sentence-level group
  - After: any_of ['dbt']; satisfied=False; known=[]; grammar=alternatives
- Previous source (preferred), removed/resegmented: aws certified solutions architect, aws certified cloud practitioner or microsoft certified solutions associate (mcsa) ( (any_of)
- Previous source (preferred), removed/resegmented: dbt analytics or architect certification ( (any_of)

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "Databricks", "contribution": -3}, {"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "dbt", "contribution": -3}]`

### Lead HVAC Mechanic (`in-6797feb75732134a`)

- Changed: alignment_score
- Attribution: legacy/group reconciliation
- Lane: wrong_lane → wrong_lane; fit: 15 → 15; decision: skip → skip
- Required atomic gaps: [] → []
- Preferred atomic gaps: [] → []
- Required group gaps: 0 → 0

- Inline-preferred section-boundary correction also affected experience/section-scoped alignment.
- Years required: None → None.
- Section alignment events: [] → [{'rule_id': 'alignment:early_career', 'kind': 'alignment', 'contribution': 1.5}].
- Section context source: * Previous experience of 5\\+ years in chiller/HVAC maintenance, mechanical engineering, or other related fields.
- Section context source: * Electrical knowledge required and EPA Certification Preferred (i.e. HVAC Journeyman, Boiler Operator, Gas Installer, etc.)

Requirement penalty ledger before: `[]`

Requirement penalty ledger after: `[]`

### Engineer III, Software/Web Development (`in-766a159b0f392eb7`)

- Changed: required_group_gaps
- Attribution: unsatisfied alternative group, legacy/group reconciliation
- Lane: bridge_lane → bridge_lane; fit: 65 → 65; decision: manual_review → manual_review
- Required atomic gaps: ['AWS'] → ['AWS']
- Preferred atomic gaps: ['Terraform'] → ['Terraform']
- Required group gaps: 0 → 1

- Source (required): develops application services on aws, integrating with cloud\\-native services (e.g., lambda, s3, dynamodb) to deliver scalable, secure, and cost\\-effective solutions.
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: any_of ['AWS']; satisfied=False; known=[]; grammar=examples
- Source (required): 3\\+ years of working with sql and nosql databases
  - Before: all_of ['SQL']; satisfied=True; known=['SQL']
  - After: all_of ['SQL']; satisfied=True; known=['SQL']; grammar=conjunction_or_enumeration
- Source (required): 3\\+ years working with the following aws services (ec2, lambda, s3, dynamodb, cloudwatch
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): familiar with infrastructure\\-as\\-code and terraform.
  - Before: all_of ['Terraform']; satisfied=False; known=[]
  - After: all_of ['Terraform']; satisfied=False; known=[]; grammar=conjunction_or_enumeration
- Source (preferred): familiarity with event\\-driven architectures on aws, pub/sub (sns/sqs), message queues, and streaming data ingestion, and the tradeoffs between these patterns.
  - Before: all_of ['AWS']; satisfied=False; known=[]
  - After: all_of ['AWS']; satisfied=False; known=[]; grammar=conjunction_or_enumeration

Requirement penalty ledger before: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Terraform", "contribution": -0.5}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

Requirement penalty ledger after: `[{"rule_id": "fit_missing_required_atomic", "kind": "fit", "skill": "AWS", "contribution": -3}, {"rule_id": "fit_missing_preferred_atomic", "kind": "fit", "skill": "Terraform", "contribution": -0.5}, {"rule_id": "fit_unsatisfied_required_group", "kind": "fit", "group_id": "required_group_1", "type": "any_of", "skills": ["AWS"], "source": "develops application services on aws, integrating with cloud\\\\-native services (e.g., lambda, s3, dynamodb) to deliver scalable, secure, and cost\\\\-effective solutions.", "contribution": -3}, {"rule_id": "alignment:modern_required", "kind": "alignment", "contribution": -3, "skills": ["aws"]}, {"rule_id": "alignment:modern_preferred", "kind": "alignment", "contribution": -1.5, "skills": ["aws"]}]`

