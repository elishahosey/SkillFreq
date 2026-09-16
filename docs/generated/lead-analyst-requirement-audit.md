# Lead Analyst Data Engineer — requirement audit

Job `in-1f5c8418605bc555`.

Sources are lowercased extractor spans from the frozen JD. Contributions are pre-cap fit ledger entries, not hypothetical marginal scores.

Lane: target_lane → target_lane; fit: 56.5 → 53.5; apply: manual_review → skip.

The previous colon heuristic treated “services:” and “databases:” as alternatives without an OR/example cue. A colon alone does not establish alternatives. AWS is charged once despite appearing in two required sentences.

## Databricks

Individual required fit contribution: -3 → -3.

- Source: extensive experience working with databricks.
- Section: required; type: all_of → all_of; grammar: conjunction_or_enumeration.
- Individually required: True; alternative/example: False.
- Candidate matched: []; whole group satisfied: False.
## Spark

Individual required fit contribution: -3 → -3.

- Source: strong skills in sql (t\\-sql), python (pyspark/pandas), dax, power query (m), pl/sql.
- Section: required; type: all_of → all_of; grammar: conjunction_or_enumeration.
- Individually required: True; alternative/example: False.
- Candidate matched: ['SQL', 'Python']; whole group satisfied: False.
## AWS

Individual required fit contribution: -3 → -3.

- Source: 7–10 years of implementation experience in cloud data architecture, with at least 5 years in aws environments.
- Section: required; type: all_of → all_of; grammar: conjunction_or_enumeration.
- Individually required: True; alternative/example: False.
- Candidate matched: []; whole group satisfied: False.
- Source: proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions.
- Section: required; type: any_of → all_of; grammar: conjunction_or_enumeration.
- Individually required: True; alternative/example: False.
- Candidate matched: []; whole group satisfied: False.
## Redshift

Individual required fit contribution: +0 → -3.

- Source: proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions.
- Section: required; type: any_of → all_of; grammar: conjunction_or_enumeration.
- Individually required: True; alternative/example: False.
- Candidate matched: []; whole group satisfied: False.
## Power BI

Individual required fit contribution: -3 → -3.

- Source: skilled in power bi, git, visual studio code, ssms.
- Section: required; type: all_of → all_of; grammar: conjunction_or_enumeration.
- Individually required: True; alternative/example: False.
- Candidate matched: []; whole group satisfied: False.

## Interpretation limits

PySpark maps to Spark under the unchanged taxonomy. Parenthetical “PySpark/Pandas” remains all-of under the bounded grammar; whether that slash permits Pandas alone deserves manual review. No Pandas equivalence was invented.

“Mentoring junior architects and engineers” appears under preferred qualifications. The existing early-career section-scope correction remains intact.

Not every listed AWS service or database is modeled in the taxonomy. No new taxonomy entries or candidate experience were inferred.
