# Grading comparison against 766f50c

Learning uses illustrative prevalence (Airflow 27%, AWS 30%, Snowflake/Spark 20%). These are test inputs, not measured market statistics.

| Job | Old lane | New lane | Old alignment | New alignment | Fit | Learning | Confidence | AI review | Old apply | New apply |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| obvious_target | target_lane | target_lane | 47.4 | 47.40 | 98.26 | 0 | 0.805 | False | apply_now | apply_now |
| sql_integration | target_lane | target_lane | 47.71 | 47.71 | 97.74 | 0 | 0.812 | False | apply_now | apply_now |
| data_backend | secondary_lane | secondary_lane | 43.17 | 43.17 | 85 | 0 | 0.9 | False | manual_review | manual_review |
| analyst_bridge | bridge_lane | bridge_lane | 34.29 | 34.29 | 65 | 0.0 | 0.791 | False | manual_review | manual_review |
| survival | survival_lane | survival_lane | 0.0 | 0.00 | 0 | 0.0 | 0.55 | True | skip | skip |
| frontend | wrong_lane | wrong_lane | 45.0 | 45.00 | 15 | 0.0 | 0.97 | False | skip | skip |
| ml | wrong_lane | wrong_lane | 38.5 | 38.50 | 15 | 0.0 | 0.97 | False | skip | skip |
| platform | wrong_lane | wrong_lane | 2.5 | 2.50 | 15 | 0.0 | 0.85 | False | skip | skip |
| erp | wrong_lane | wrong_lane | 50.0 | 50.00 | 15 | 0.0 | 0.9 | False | skip | skip |
| dashboards | wrong_lane | wrong_lane | 0.0 | 0.00 | 0 | 0.0 | 0.85 | False | skip | skip |
| generic_software_data | bridge_lane | secondary_lane | 49.33 | 49.33 | 85 | 0 | 0.9 | False | manual_review | manual_review |
| misleading_title | wrong_lane | wrong_lane | 0.0 | 0.00 | 0 | 0.0 | 0.53 | True | skip | skip |
| learning_opportunity | target_lane | target_lane | 32.6 | 28.27 | 83.0 | 94.03 | 0.812 | False | manual_review | apply_now |
| ambiguous | target_lane | secondary_lane | 56.0 | 56.00 | 85 | 0 | 0.457 | True | skip | manual_review |

The raw alignment score retains its historic scale. Fit and learning are distinct 0–100 heuristics. Confidence is not a calibrated probability.

Grading version: `809dc743062dee89`. Atomic taxonomy version: `31d08964f877`.
