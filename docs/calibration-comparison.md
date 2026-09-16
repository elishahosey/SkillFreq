# 90-day calibration comparison

Before: `data\outputs\results-db-90-days.csv`. After: `data\outputs\results-db-90-days-calibrated.csv`.
Matched 8,692 source identities; before-only 0, after-only 0.
Title/description changed for 0 matched jobs.
Grading versions: `['4a0e936190e2a822']` → `['809dc743062dee89']`. Taxonomy: `['31d08964f877']`.
The original CSV and configuration snapshot are preserved. Examples compare matched postings; aggregate tables describe each entire export.

## Overall results

| Metric | Before | After |
|---|---:|---:|
| jobs | 8692 | 8692 |
| average_fit | 30.64 | 31.34 |
| average_learning | 0.0 | 2.45 |
| nonzero_learning | 0 | 888 |
| unavailable_learning | 0 | 0 |
| market_unavailable_count | 8692 | 0 |
| ai_review_pct | 53.64 | 37.95 |

## role_lane counts

| Outcome | Before | After |
|---|---:|---:|
| bridge_lane | 640 | 725 |
| secondary_lane | 1368 | 1475 |
| target_lane | 298 | 255 |
| wrong_lane | 6386 | 6237 |

## apply_decision counts

| Outcome | Before | After |
|---|---:|---:|
| apply_now | 2 | 94 |
| manual_review | 1185 | 2282 |
| skip | 7505 | 6316 |

## fit_quality counts

| Outcome | Before | After |
|---|---:|---:|
| good_fit | 6 | 868 |
| possible_fit | 1181 | 1519 |
| weak_fit | 7505 | 6305 |

## Decisions within each lane

| Lane | Decision | Before count (%) | After count (%) |
|---|---|---:|---:|
| bridge_lane | apply_now | 0 (0.0%) | 0 (0.0%) |
| bridge_lane | manual_review | 350 (54.69%) | 698 (96.28%) |
| bridge_lane | skip | 290 (45.31%) | 27 (3.72%) |
| bridge_lane | fit quality | {'weak_fit': 290, 'possible_fit': 350} | {'possible_fit': 705, 'weak_fit': 20} |
| secondary_lane | apply_now | 0 (0.0%) | 0 (0.0%) |
| secondary_lane | manual_review | 581 (42.47%) | 1438 (97.49%) |
| secondary_lane | skip | 787 (57.53%) | 37 (2.51%) |
| secondary_lane | fit quality | {'possible_fit': 581, 'weak_fit': 787} | {'good_fit': 733, 'possible_fit': 706, 'weak_fit': 36} |
| target_lane | apply_now | 2 (0.67%) | 94 (36.86%) |
| target_lane | manual_review | 254 (85.23%) | 146 (57.25%) |
| target_lane | skip | 42 (14.09%) | 15 (5.88%) |
| target_lane | fit quality | {'weak_fit': 42, 'possible_fit': 250, 'good_fit': 6} | {'weak_fit': 12, 'possible_fit': 108, 'good_fit': 135} |
| wrong_lane | apply_now | 0 (0.0%) | 0 (0.0%) |
| wrong_lane | manual_review | 0 (0.0%) | 0 (0.0%) |
| wrong_lane | skip | 6386 (100.0%) | 6237 (100.0%) |
| wrong_lane | fit quality | {'weak_fit': 6386} | {'weak_fit': 6237} |

## 20 biggest classification changes (absolute fit change)

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Data Engineer (li-4428742832) | wrong_lane → target_lane | skip → apply_now | 15.0 → 93.53 | 32.57 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Systems Integration Engineer (UAV or robotics ) - Onsite in Austin, TX (li-4429356988) | target_lane → wrong_lane | manual_review → skip | 93.48 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Senior Tester (li-4429677691) | target_lane → wrong_lane | manual_review → skip | 91.13 → 15.0 | 0.0 | wrong_role_identity, bridge_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Data Engineer, AWS GDSP A&I (li-4390840079) | wrong_lane → target_lane | skip → apply_now | 15.0 → 89.74 | 30.49 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Sr Test Automation Engineer (in-785bff2b29d4f840) | target_lane → wrong_lane | manual_review → skip | 88.48 → 15.0 | 0.0 | wrong_role_identity, positive_and_exclusion_signals, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| GCP Data Engineer (In-Person Interview) (li-4428754413) | wrong_lane → target_lane | skip → manual_review | 15.0 → 88.44 | 8.62 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, good_fit_score, ambiguous_role_review |
| Mechanical Engineer (li-4429949900) | target_lane → wrong_lane | skip → skip | 86.67 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Asset Management Engineering - Associate Software Engineer (AI Engineering) - Dallas (in-252af71079fd2a98) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 33.84 | positive_and_exclusion_signals, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |
| Senior Production Support Electrical Engineer (in-549b2ef62fb5fe8b) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Head of Customer Support (in-b3a160c329f6b318) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 7.84 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Senior Cloud Engineer - Cloud Optimization (in-be33966e8afa5842) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 4.55 | bridge_eligibility, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |
| Software Engineer, Manufacturing Test (in-d03366b27b565075) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, generic_software_guard, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Electrical Engineer 2 - Energy & Industrial Group (in-db4fea4aa890b2ca) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr. Electrical Test and Reliability Engineer, Gateways (Starlink) (li-4380121005) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Electrical Test and Reliability Engineer, Gateways (Starlink) (li-4380163313) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Electrical Reliability Engineer (li-4398671438) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Electrical Engineer (li-4410823961) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Site Reliability Engineer (SRE) - Oracle EBS (li-4413353525) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, generic_software_guard, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Senior Automation Engineer (li-4417231159) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 2.08 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Mechanical Engineer (Fixed Equipment) (li-4418413656) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |

## 20 biggest apply-decision changes (decision distance, then fit change)

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Data Engineer (li-4428742832) | wrong_lane → target_lane | skip → apply_now | 15.0 → 93.53 | 32.57 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Data Engineer, AWS GDSP A&I (li-4390840079) | wrong_lane → target_lane | skip → apply_now | 15.0 → 89.74 | 30.49 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Senior Artificial Intelligence Data Engineer (li-4426169180) | wrong_lane → target_lane | skip → apply_now | 15.0 → 84.23 | 7.84 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Associate Data Engineer (li-4417247845) | wrong_lane → target_lane | skip → apply_now | 15.0 → 83.0 | 5.54 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Data Engineer II, Sales Planning and Compensation (SPC) (li-4411843140) | wrong_lane → target_lane | skip → apply_now | 15.0 → 82.39 | 30.49 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Senior Associate Data Engineer (li-4427383585) | target_lane → target_lane | skip → apply_now | 89.35 → 86.85 | 0.0 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| SQL Developer (li-4429620240) | target_lane → target_lane | skip → apply_now | 95.0 → 96.5 | 0.0 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Systems Integration Engineer (UAV or robotics ) - Onsite in Austin, TX (li-4429356988) | target_lane → wrong_lane | manual_review → skip | 93.48 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Senior Tester (li-4429677691) | target_lane → wrong_lane | manual_review → skip | 91.13 → 15.0 | 0.0 | wrong_role_identity, bridge_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr Test Automation Engineer (in-785bff2b29d4f840) | target_lane → wrong_lane | manual_review → skip | 88.48 → 15.0 | 0.0 | wrong_role_identity, positive_and_exclusion_signals, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| GCP Data Engineer (In-Person Interview) (li-4428754413) | wrong_lane → target_lane | skip → manual_review | 15.0 → 88.44 | 8.62 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, good_fit_score, ambiguous_role_review |
| Asset Management Engineering - Associate Software Engineer (AI Engineering) - Dallas (in-252af71079fd2a98) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 33.84 | positive_and_exclusion_signals, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |
| Head of Customer Support (in-b3a160c329f6b318) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 7.84 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Senior Cloud Engineer - Cloud Optimization (in-be33966e8afa5842) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 4.55 | bridge_eligibility, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |
| Electrical Engineer 2 - Energy & Industrial Group (in-db4fea4aa890b2ca) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Senior Automation Engineer (li-4417231159) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 2.08 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| IT Specialist (li-4418518139) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 85.0 | 0.0 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Product Lifecycle Mechanical Engineer, Data Center Mechanical Products & Services (li-4419544988) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Senior Product Lifecycle Mechanical Engineer, Data Center Mechanical Products & Services (li-4419565053) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr. Payload Integration & Test RF Communications System Engineer, Amazon Leo (li-4419844800) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |

## High fit retained while decision changed

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Data Engineer (li-4428781466) | target_lane → target_lane | skip → apply_now | 83.48 → 80.48 | 33.68 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Senior Associate Data Engineer (li-4427383585) | target_lane → target_lane | skip → apply_now | 89.35 → 86.85 | 0.0 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| SQL Developer (li-4429620240) | target_lane → target_lane | skip → apply_now | 95.0 → 96.5 | 0.0 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Sr./Principal - Engineer - Automation (I&C) (li-4428018025) | secondary_lane → secondary_lane | skip → manual_review | 85.0 → 80.0 | 0.0 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, configured_review_gate |
| Data Engineer II (li-4419524058) | target_lane → target_lane | manual_review → apply_now | 83.71 → 87.21 | 39.22 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Solutions Architecture Analyst – Assistant Vice President (li-4409375451) | secondary_lane → secondary_lane | skip → manual_review | 81.86 → 84.86 | 36.87 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, good_fit_score, ambiguous_role_review |
| Integration Engineer or Senior Integration Engineer, Texas Institute for Electronics, Cockrell School of Engineering (li-4424947815) | target_lane → target_lane | skip → manual_review | 83.56 → 80.56 | 0.0 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, configured_review_gate |
| Databricks Data Engineer - Data & AI (li-4427380802) | target_lane → target_lane | manual_review → apply_now | 94.29 → 91.29 | 7.84 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Senior Data Engineer (li-4428438379) | target_lane → target_lane | manual_review → apply_now | 84.61 → 87.61 | 4.39 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Sr Oracle CPQ Developer (li-4428725342) | secondary_lane → secondary_lane | skip → manual_review | 84.4 → 81.4 | 0.0 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Senior Data Analytics Architect (li-4429681401) | secondary_lane → secondary_lane | skip → manual_review | 84.57 → 81.57 | 0.0 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, configured_review_gate |
| Sr Endur Developer (li-4429691137) | secondary_lane → secondary_lane | skip → manual_review | 83.03 → 80.03 | 0.0 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Technical Customer Success (li-4429987716) | secondary_lane → secondary_lane | skip → manual_review | 83.33 → 80.33 | 0.0 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Platform Engineer (li-4408454948) | secondary_lane → secondary_lane | skip → manual_review | 85.0 → 82.3 | 6.63 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, configured_review_gate |
| Senior Software Engineer – Microservices / MBFF Platform (in-f5f4607632479b92) | secondary_lane → secondary_lane | skip → manual_review | 80.23 → 82.73 | 7.57 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |
| Windchill Integration Engineer (li-4429666992) | target_lane → target_lane | manual_review → apply_now | 90.93 → 88.43 | 0.0 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Senior Java Developer (in-453d2d1725c276ac) | secondary_lane → secondary_lane | skip → manual_review | 85.0 → 82.96 | 33.84 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |
| Specialist - Data Engineering (in-33bdef2c376004f0) | target_lane → target_lane | manual_review → apply_now | 81.14 → 83.14 | 6.53 | secondary_eligibility, bridge_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Senior Product Analyst (dbt) (in-779036aff43d924c) | secondary_lane → secondary_lane | skip → manual_review | 81.17 → 83.17 | 4.39 | data_evidence, secondary_eligibility, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Manufacturing Engineering Technician, Instruments (in-77f0329c508dca75) | secondary_lane → secondary_lane | skip → manual_review | 85.0 → 83.0 | 0.0 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, ambiguous_role_review |

## Learning becomes meaningful

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Senior Python Developer / Lead Python Engineer (li-4428748179) | secondary_lane → secondary_lane | skip → skip | 32.87 → 48.37 | 53.32 | secondary_eligibility, generic_software_guard, ai_review_gate, weak_fit_score, insufficient_fit |
| Data Engineer (li-4430189904) | target_lane → target_lane | manual_review → skip | 38.84 → 51.84 | 51.24 | target_eligibility, secondary_eligibility, ai_review_gate, weak_fit_score, insufficient_fit |
| Data Engineer with AWS // onsite in NJ, TX, AZ, RI // W2 (li-4429359989) | wrong_lane → target_lane | skip → manual_review | 15.0 → 64.64 | 51.06 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, possible_fit_score, configured_review_gate |
| Software Developer (li-4429965794) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 77.61 | 49.34 | secondary_eligibility, generic_software_guard, ai_review_gate, possible_fit_score, adjacent_or_moderate_fit |
| Analytics Engineer (li-4420433534) | secondary_lane → secondary_lane | manual_review → manual_review | 85.0 → 85.0 | 48.22 | analytics_identity_guard, analytics_bridge, ai_review_gate, good_fit_score, ambiguous_role_review |
| Databricks Data Engineer (li-4428726488) | wrong_lane → target_lane | skip → manual_review | 15.0 → 63.34 | 48.22 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, possible_fit_score, configured_review_gate |
| Azure Data Engineer (li-4428771569) | wrong_lane → target_lane | skip → manual_review | 15.0 → 75.5 | 45.75 | target_eligibility, secondary_eligibility, ai_review_gate, possible_fit_score, ambiguous_role_review |
| Senior Data Architect (li-4418276448) | secondary_lane → secondary_lane | skip → skip | 34.06 → 46.06 | 44.86 | backend_evidence, secondary_eligibility, ai_review_gate, weak_fit_score, insufficient_fit |
| Senior Python Developer with Snowflake (li-4430716870) | secondary_lane → secondary_lane | skip → manual_review | 50.02 → 64.52 | 44.77 | secondary_eligibility, generic_software_guard, ai_review_gate, possible_fit_score, configured_review_gate |
| Data engineer Architect (li-4428782435) | wrong_lane → target_lane | skip → skip | 15.0 → 43.62 | 43.81 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, weak_fit_score, insufficient_fit |

**Senior Python Developer / Lead Python Engineer**: [{"skill": "Snowflake", "prevalence_pct": 4.7, "adjacent_concepts": {"sql": 1.0, "data_modeling": 1.0}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "Airflow", "prevalence_pct": 2.3, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 1, "novelty": 0.8, "contribution": 2.147}, {"skill": "PostgreSQL", "prevalence_pct": 3.7, "adjacent_concepts": {"sql": 1.0}, "priority": 0.7, "novelty": 1, "contribution": 3.022}, {"skill": "Databricks", "prevalence_pct": 3.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 3.453}, {"skill": "Spark", "prevalence_pct": 4.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "AWS", "prevalence_pct": 27.9, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.9, "novelty": 1, "contribution": 29.295}, {"skill": "Docker", "prevalence_pct": 6.5, "adjacent_concepts": {"python": 0.8, "systems": 1.25}, "priority": 0.6, "novelty": 1, "contribution": 4.55}, {"skill": "Terraform", "prevalence_pct": 5.1, "adjacent_concepts": {"azure": 0.8, "systems": 1.25}, "priority": 0.35, "novelty": 1, "contribution": 2.082}]

**Data Engineer**: [{"skill": "Snowflake", "prevalence_pct": 4.7, "adjacent_concepts": {"sql": 1.0, "data_modeling": 1.0}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "Airflow", "prevalence_pct": 2.3, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 1, "novelty": 0.8, "contribution": 2.147}, {"skill": "PostgreSQL", "prevalence_pct": 3.7, "adjacent_concepts": {"sql": 1.0}, "priority": 0.7, "novelty": 1, "contribution": 3.022}, {"skill": "Databricks", "prevalence_pct": 3.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 3.453}, {"skill": "Spark", "prevalence_pct": 4.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "AWS", "prevalence_pct": 27.9, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.9, "novelty": 1, "contribution": 29.295}, {"skill": "Docker", "prevalence_pct": 6.5, "adjacent_concepts": {"python": 0.8, "systems": 1.25}, "priority": 0.6, "novelty": 1, "contribution": 4.55}]

**Data Engineer with AWS // onsite in NJ, TX, AZ, RI // W2**: [{"skill": "Snowflake", "prevalence_pct": 4.7, "adjacent_concepts": {"sql": 1.0, "data_modeling": 1.0}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "Airflow", "prevalence_pct": 2.3, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 1, "novelty": 0.8, "contribution": 2.147}, {"skill": "PostgreSQL", "prevalence_pct": 3.7, "adjacent_concepts": {"sql": 1.0}, "priority": 0.7, "novelty": 1, "contribution": 3.022}, {"skill": "Spark", "prevalence_pct": 4.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "AWS", "prevalence_pct": 27.9, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.9, "novelty": 1, "contribution": 29.295}, {"skill": "Redshift", "prevalence_pct": 1.7, "adjacent_concepts": {"sql": 1.0, "etl": 1.0}, "priority": 0.6, "novelty": 1, "contribution": 1.19}, {"skill": "Docker", "prevalence_pct": 6.5, "adjacent_concepts": {"python": 0.8, "systems": 1.25}, "priority": 0.6, "novelty": 1, "contribution": 4.55}, {"skill": "Terraform", "prevalence_pct": 5.1, "adjacent_concepts": {"azure": 0.8, "systems": 1.25}, "priority": 0.35, "novelty": 1, "contribution": 2.082}]

**Software Developer**: [{"skill": "Snowflake", "prevalence_pct": 4.7, "adjacent_concepts": {"sql": 1.0, "data_modeling": 1.0}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "Databricks", "prevalence_pct": 3.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 3.453}, {"skill": "Spark", "prevalence_pct": 4.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "AWS", "prevalence_pct": 27.9, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.9, "novelty": 1, "contribution": 29.295}, {"skill": "Redshift", "prevalence_pct": 1.7, "adjacent_concepts": {"sql": 1.0, "etl": 1.0}, "priority": 0.6, "novelty": 1, "contribution": 1.19}, {"skill": "Docker", "prevalence_pct": 6.5, "adjacent_concepts": {"python": 0.8, "systems": 1.25}, "priority": 0.6, "novelty": 1, "contribution": 4.55}, {"skill": "Terraform", "prevalence_pct": 5.1, "adjacent_concepts": {"azure": 0.8, "systems": 1.25}, "priority": 0.35, "novelty": 1, "contribution": 2.082}]

**Analytics Engineer**: [{"skill": "Snowflake", "prevalence_pct": 4.7, "adjacent_concepts": {"sql": 1.0, "data_modeling": 1.0}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "Airflow", "prevalence_pct": 2.3, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 1, "novelty": 0.8, "contribution": 2.147}, {"skill": "Databricks", "prevalence_pct": 3.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 3.453}, {"skill": "Spark", "prevalence_pct": 4.7, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.8, "novelty": 1, "contribution": 4.387}, {"skill": "AWS", "prevalence_pct": 27.9, "adjacent_concepts": {"etl": 1.0, "python": 0.8}, "priority": 0.9, "novelty": 1, "contribution": 29.295}, {"skill": "Docker", "prevalence_pct": 6.5, "adjacent_concepts": {"python": 0.8, "systems": 1.25}, "priority": 0.6, "novelty": 1, "contribution": 4.55}]

## QA/test/infrastructure/support corrections

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Senior Tester (li-4429677691) | target_lane → wrong_lane | manual_review → skip | 91.13 → 15.0 | 0.0 | wrong_role_identity, bridge_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr Test Automation Engineer (in-785bff2b29d4f840) | target_lane → wrong_lane | manual_review → skip | 88.48 → 15.0 | 0.0 | wrong_role_identity, positive_and_exclusion_signals, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Software Engineer, Manufacturing Test (in-d03366b27b565075) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, generic_software_guard, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr. Electrical Test and Reliability Engineer, Gateways (Starlink) (li-4380121005) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Electrical Test and Reliability Engineer, Gateways (Starlink) (li-4380163313) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr. Payload Integration & Test RF Communications System Engineer, Amazon Leo (li-4419844800) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Software Test Automation Engineer - Frisco, Texas (li-4426151491) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Software Engineer in Test (li-4427361766) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, generic_software_guard, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| IVR Tester (li-4429969097) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Cyara Tester (li-4429974093) | secondary_lane → wrong_lane | manual_review → skip | 85.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Security QA Analyst, Senior (in-40e03c1489137aac) | target_lane → wrong_lane | manual_review → skip | 84.63 → 15.0 | 0.0 | wrong_role_identity, positive_and_exclusion_signals, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Senior Python Developer – Kubernetes & Infrastructure Automation (li-4428728160) | wrong_lane → secondary_lane | skip → manual_review | 15.0 → 84.27 | 2.08 | secondary_eligibility, generic_software_guard, ai_review_gate, good_fit_score, adjacent_or_moderate_fit |
| Senior Database Tester (li-4430966622) | secondary_lane → wrong_lane | skip → skip | 83.42 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| QA Design Transfer Engineer I/II - Pearland, TX (li-4348173346) | secondary_lane → wrong_lane | skip → skip | 83.33 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Consulting EHR Support Analyst -PHARM (li-4408979006) | secondary_lane → wrong_lane | skip → skip | 81.48 → 15.0 | 0.0 | wrong_role_identity, support_identity_guard, support_secondary_guard, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Software Development Engineer in Test (SDET) (li-4428083074) | target_lane → wrong_lane | manual_review → skip | 81.03 → 15.0 | 0.0 | wrong_role_identity, positive_and_exclusion_signals, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Manufacturing Engineer, Generator Testing (li-4430133182) | secondary_lane → wrong_lane | manual_review → skip | 79.41 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Sr. Manufacturing Test Automation Engineer - Optical Systems (li-4428468739) | secondary_lane → wrong_lane | skip → skip | 79.19 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Test Development Engineer (li-4429964695) | secondary_lane → wrong_lane | skip → skip | 79.19 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |
| Software Test Development Engineer (in-85b9bbad6b496379) | secondary_lane → wrong_lane | skip → skip | 78.0 → 15.0 | 0.0 | wrong_role_identity, secondary_eligibility, hard_exclusion_override, ai_review_gate, weak_fit_score, configured_hard_blocker |

## Modern data roles released from platform penalties

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Data Engineer (li-4429051149) | wrong_lane → target_lane | skip → apply_now | 15.0 → 93.53 | 39.22 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Data Engineer, AWS GDSP A&I (li-4390840079) | wrong_lane → target_lane | skip → apply_now | 15.0 → 89.74 | 30.49 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| GCP Data Engineer (In-Person Interview) (li-4428754413) | wrong_lane → target_lane | skip → manual_review | 15.0 → 88.44 | 8.62 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, good_fit_score, ambiguous_role_review |
| Senior Artificial Intelligence Data Engineer (li-4426169180) | wrong_lane → target_lane | skip → apply_now | 15.0 → 84.23 | 7.84 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Associate Data Engineer (li-4417247845) | wrong_lane → target_lane | skip → apply_now | 15.0 → 83.0 | 5.54 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Data Engineer II, Sales Planning and Compensation (SPC) (li-4411843140) | wrong_lane → target_lane | skip → apply_now | 15.0 → 82.39 | 30.49 | target_eligibility, secondary_eligibility, ai_review_gate, good_fit_score, strong_primary_fit |
| Data Engineer, OIS/CXI Analytics (li-4419914606) | wrong_lane → target_lane | skip → manual_review | 15.0 → 78.58 | 34.87 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, possible_fit_score, ambiguous_role_review |
| Data Engineer - Senior Associate (li-4369126870) | wrong_lane → target_lane | skip → manual_review | 15.0 → 78.0 | 37.13 | target_eligibility, secondary_eligibility, ai_review_gate, possible_fit_score, configured_review_gate |
| Senior Data Engineer (li-4430980297) | wrong_lane → target_lane | skip → manual_review | 15.0 → 76.4 | 38.33 | target_eligibility, secondary_eligibility, ai_review_gate, possible_fit_score, configured_review_gate |
| Senior Staff Backline Engineer - Data & AI (in-880722f2cc8da2af) | wrong_lane → target_lane | skip → manual_review | 15.0 → 76.07 | 7.84 | secondary_eligibility, positive_and_exclusion_signals, ai_review_gate, possible_fit_score, configured_review_gate |

## Ecosystem ownership gates

Examples show distinct titles to avoid filling the report with syndicated copies. IDs identify the actual postings.

| Job | Lane before → after | Decision before → after | Fit before → after | Learning after | Configured evidence |
|---|---|---|---:|---:|---|
| Informatica Platform Administrator (li-4429981441) | secondary_lane → wrong_lane | skip → skip | 85.0 → 15.0 | 0.0 | ecosystem_ownership_gap, wrong_role_identity, secondary_eligibility, generic_software_guard, ai_review_gate, weak_fit_score, configured_hard_blocker |
| MDM Engineer (in-0470c187b383c0b2) | target_lane → bridge_lane | manual_review → skip | 100.0 → 59.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Master Data Management_Informatica  at Dallas, TX (li-4430769122) | target_lane → bridge_lane | manual_review → skip | 100.0 → 59.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Senior Informatica MDM Support Engineer (li-4427841402) | target_lane → bridge_lane | manual_review → skip | 100.0 → 59.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Informatica MDM Support & Data Operations Specialist (li-4429364893) | target_lane → target_lane | manual_review → skip | 100.0 → 59.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Informatica MDM -Master Data Management (li-4430496381) | target_lane → bridge_lane | manual_review → skip | 100.0 → 65.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Master Data Management_Informatica (MDM) Lead / Architect (li-4429335197) | target_lane → bridge_lane | manual_review → skip | 88.0 → 55.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Dell Boomi Integration Engineer (li-4429690071) | target_lane → target_lane | skip → skip | 92.44 → 59.44 | 0.0 | ecosystem_ownership_gap, target_eligibility, secondary_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Master Data Management  Engineer (li-4429674619) | target_lane → target_lane | manual_review → skip | 100.0 → 67.0 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, possible_fit_score, configured_hard_blocker |
| Salesforce Apex Technical Lead - Lightning framework and administration (in-b7e11e61c9911414) | target_lane → bridge_lane | manual_review → skip | 82.49 → 49.49 | 0.0 | ecosystem_ownership_gap, secondary_eligibility, bridge_eligibility, ai_review_gate, weak_fit_score, configured_hard_blocker |

## Representative responsibility excerpts

These excerpts come from the stored descriptions. Inspect the complete description and grade_json in the CSV before acting; title alone is not the policy input.

### Senior Tester (li-4429677691)

Hi Greetings from Tekgence!       I am having an urgent opening for the below mentioned project. Kindly share your resume at rupal.jain@tekgence.com              **Role: Kafka Teste**      **rLocation: Strongsville/Pittsburgh/Dallas. 100% ONSITE FROM DAY**               1       Apache Kafka: Deep understanding of Kafka's architecture, components, and functionalit       y.SQL: Experience with No SQL database for data validation and debugging. Experience with Mongo DB neede       d.Test Automation: Experience in developing and maintaining automated tests for data pipelines using Kara                       te           Role Descriptions: Data Pipeline Testing: Designing and executing test cases for ETL (Extract\\/ Transform\\/ Load) workflows and data validation\\/ focusing on both batch and streaming data. Data Validation: Validating data ingestion\\/ transformation\\/ and loading processes within Kafka\\/ ensuring data quality\\/ consistency\\/ and completeness across systems. Kafka Expertise: Hands\\-on experience with Apache Kafka for data streaming validation\\/ including working with producers\\/ consumers\\/ and understanding Kafkas architecture and concepts. Scripting and Automation: Proficiency in Python or other scripting languages for automating testing of data pipelines and maintaining test scripts. Issue Resolution: Collaborating with developers to identify\\/ analyze\\/ and resolve data issues\\/ performing root cause analysis\\/ and proposing solutions. Performance Testing: Evaluating the performance and scalability of Kafka\\-based systems\\/ ensuring they can 

### Sr Test Automation Engineer (in-785bff2b29d4f840)

**Work Schedule**   Standard (Mon\\-Fri)**Environmental Conditions**   Office**Job Description**   As part of the Thermo Fisher Scientific team, you’ll discover meaningful work that makes a positive impact on a global scale. Join our colleagues in bringing our Mission to life every single day to enable our customers to make the world healthier, cleaner and safer. We provide our global teams with the resources needed to achieve individual career goals while helping to take science a step beyond by developing solutions for some of the world’s toughest challenges, like protecting the environment, making sure our food is safe or helping find cures for cancer.        DESCRIPTION:    Join our team at Thermo Fisher Scientific and help make the world healthier, cleaner, and safer through innovative software solutions. As a Sr Test Automation Engineer, you'll work on next\\-generation cloud\\-based architectures and platforms, ensuring the quality and reliability of our scientific software products. You'll collaborate with teams to design, develop, and maintain comprehensive test automation frameworks while driving adoption of best practices across the organization. This role offers opportunities to work with advanced technologies in cloud computing, laboratory automation, and scientific instrumentation, directly impacting research and healthcare outcomes worldwide.  **Location:** Morrisville, NC. Relocation assistance is NOT provided.  **Key Responsibilities:**  * Design, develop, and maintain scalable and reliable automated test frameworks across UI, API, and performance layers. *

### Software Engineer, Manufacturing Test (in-d03366b27b565075)

**What to Expect** Come join the Manufacturing Test and Engineering software team and help us accelerate the world’s transition to sustainable energy. As a member of our team, you will develop software for in\\-house designed test equipment that is responsible for ensuring the functionality of products Tesla manufactures and sells to customers, collaborating closely with other engineering disciplines, design teams, and manufacturing teams. You will play a critical role in launching and ramping up the products that Tesla makes, ensuring that the product meets all specifications to delight customers around the world.    **What You'll Do*** Work in a fast\\-paced environment where you will have the opportunity to exercise your creative thinking skills to solve complex problems * Play a key role in all aspects of product design and validation, going beyond software development to make a meaningful impact on the company’s success * Write software in Go, LabVIEW, and/or Python to thoroughly validate Tesla products on a manufacturing line, communicating with various hardware devices such as data acquisition systems, mechanical actuators, PLCs, and Tesla products over CAN, UDS, etc. * Collaborate with other engineering disciplines to design test equipment that validate product functionality, optimizing accuracy, cost, cycle time, and other performance indicators * Develop software that enables our test equipment to be easily maintainable by 24/7 production teams, and drive continuous improvements to your software * Bring ideas and work on projects that advance our software tech sta

### Data Engineer (li-4429051149)

**Data Engineer**      **London · Hybrid (2 days in office) · Up to £75k \\+ Bonus**               A well established B2B SaaS business is hiring a Data Platform Engineer to help scale their lakehouse and build the infrastructure behind a new wave of data products.              **The setup**       You'd be working on the platform that powers analytics and AI across the business, building reusable foundations for other engineering teams, and contributing to a real modernisation programme that includes pulling data out of a legacy SQL Server monolith into the lakehouse.              **What you'd be doing**       Building and supporting the lakehouse, designing abstractions and templates that other teams rely on, writing ETL, contributing to data modelling for both internal analytics and external facing data products, and owning your work end to end from design to deployment.              **Stack**       Databricks, dbt, Fivetran, Python, SQL, AWS (Lambda, Kinesis, EventBridge, S3\\), Terraform, Kafka, ECS and Kubernetes.              **You'll fit if you:**     * Have strong Python and have built data infrastructure that other engineers or analysts depend on * Are comfortable with AWS and Terraform as the default way of working * Have hands on experience with Databricks, Snowflake or BigQuery, plus dbt and Fivetran * Have touched Kafka or similar streaming systems * Have solid SQL and a good sense for data modelling * Enjoy building tools and paved roads as much as shipping pipelines            **Package**     * Up to £70k base * Discretionary bonus up to 10 percent * 7\\.5 pe

### Data Engineer, AWS GDSP A&I (li-4390840079)

**Description**  Amazon Web Services (AWS) is a dynamic and rapidly growing business within Amazon and the leader in providing secure, reliable, scalable, and innovative services that help over a million businesses, governments, education, and not for profits across the globe scale and grow! AWS provides a wide set of scalable services to meet customer needs.           At AWS, the Global Deal Strategy and Programs (GDSP) team drives cloud adoption and business growth through innovative pricing strategies. The organization comprises two specialized teams: Strategic Customer Engagements, which guide \\*\\* transformative deals with industry leaders, and Private Pricing Programs \\& Experiences, which scales and optimizes pricing solutions across our diverse customer base. Within GDSP, you will develop deep expertise in cloud economics, hone your strategic thinking, and directly impact AWS's market leadership while working with latest technologies and global clients.           The AWS Global Deal Strategy and Programs (GDSP) organization is responsible for the Private Pricing Program. The Private Pricing Analytics and Insights (PPA\\&I) team owns building scalable analytical solutions that enable the GDSP organization with actionable insights to make data\\-driven decisions. This role will focus on Data Engineering, and Analytics related to the Private Pricing Program, requiring deep technical skills, strong business acumen and a deep analytical background to provide actionable data\\-driven insights and decision support.           As a Data Engineer on this team, you will dri

### GCP Data Engineer (In-Person Interview) (li-4428754413)

**Role: GCP Data Engineer**      **Location: Charlotte, NC or Irvine, TX or Edison, NJ or Phoenix, AZ**      **Employment type: Fulltime**               We are seeking a highly skilled GCP Data Engineer with strong Python expertise to design, build, and optimize scalable data solutions on Google Cloud Platform (GCP). The ideal candidate will have hands\\-on experience developing batch and real\\-time data pipelines, working with large\\-scale datasets, and enabling analytics and AI/ML use cases.              **Key Responsibilities**       Data Engineering \\& Pipeline Development       • Design, build, and maintain scalable batch and real\\-time data pipelines using GCP services such as Dataflow, Dataproc, and Pub/Sub       • Develop and optimize ETL/ELT workflows for structured and unstructured data processing       • Implement event\\-driven data processing using Cloud Functions and Pub/Sub       • Build and manage data ingestion frameworks for streaming and batch data sources       Data Storage \\& Processing       • Design and optimize data lakes and data warehouses using BigQuery and Cloud Storage       • Develop efficient data models to support analytics, reporting, and machine learning workloads       • Optimize performance and cost of data pipelines and queries       Development \\& Automation       • Develop reusable and scalable solutions using Python       • Automate workflows and orchestration using Cloud Composer (Airflow)       • Implement CI/CD pipelines and deployment automation       Collaboration \\& Support       • Collaborate with analytics, AI/ML, and b

### Informatica Platform Administrator (li-4429981441)

🚨  **We're Hiring \\/ Informatica Platform Administrator**   🚨       We are seeking skilled professionals with strong expertise in Informatica platform administration and enterprise data management technologies.      **Key Skills Required:**       ✔ Informatica PowerCenter Administration       ✔ Informatica IDMC / IICS Administration       ✔ Data Integration Hub (DIH)       ✔ Informatica MDM, AXON, EDC, IDQ       ✔ Oracle, SQL Server, DB2       ✔ Linux/Unix Administration       ✔ Networking \\& Security Fundamentals       ✔ Production Support \\& Platform Management      **Preferred:**       ➕ Retail, Consumer Goods, or Logistics domain experience       📍 Location:  **\\/ Plano, TX**       If you have a passion for managing enterprise data platforms, ensuring system reliability, and driving data integration excellence, we'd love to connect with you.       📩 Interested candidates can share their updated resume at  **rahul.prakash@neerinfo.com**

### MDM Engineer (in-0470c187b383c0b2)

**Must Have Technical/Functional Skills**  · Monitor daily, weekly, and monthly MDM batch jobs for data loading and synchronization, resolving data pipeline failures, and identifying issues.  · Troubleshoot and fix issues/incidents related to data, failed batch jobs, data loading errors, and user\\-reported bugs.  · Analysis (RCA) of recurring production incidents and implement permanent, proactive fixes to prevent recurrence.  · Collaborate with business stakeholders and data stewards to understand data requirements and ensure alignment with data governance policies.  · Analyze large data sets to detect anomalies, data errors, and duplicates in the system. Prepare processes for data corrections in MDM.  · Monitor and maintain real\\-time and batch data interfaces between the MDM and its spoke systems using APIs, REST/SOAP services, SIF API, or IDQ /ETL tools.  **Skills:**  · Informatica: Strong experience in Informatica MDM Hub Console 10\\.5(good to have), IDD, SIF, Match/Merge rules, and provisioning tool, IDQ10\\.5(good to have), putty.  · SQL: Should be good in writing SQL queries (Oracle DB) as this will be needed for data analysis and troubleshooting.  · Scripting: Good to have UNIX Shell scripting knowledge as this will be required to analyze scripts for any IDQ or MDM job failures.  · Autosys and MFT: Experienced in third party scheduling tool like Autosys, and file transfer tools like IBM Sterling Integrator.  · Tools: Familiarity with ServiceNow or JIRA for incident tracking.  · Problem\\-Solving: Ability to troubleshoot and resolve complex technical issues under

### Master Data Management_Informatica  at Dallas, TX (li-4430769122)

**Role: Master Data Management\\_Informatica (MDM)           Dallas, TX** **Contract**  Experience Required: 10 \\& Above          **Responsibilities**  Monitor daily, weekly, and monthly MDM batch jobs for data loading and synchronization, resolving data pipeline failures, and identifying issues.           Troubleshoot and fix issues/incidents related to data, failed batch jobs, data loading errors, and user\\-reported bugs.           Analysis (RCA) of recurring production incidents and implement permanent, proactive fixes to prevent recurrence.           Collaborate with business stakeholders and data stewards to understand data requirements and ensure alignment with data governance policies.           Analyze large data sets to detect anomalies, data errors, and duplicates in the system. Prepare processes for data corrections in MDM.           Monitor and maintain real\\-time and batch data interfaces between the MDM and its spoke systems using APIs, REST/SOAP services, SIF API, or IDQ /ETL tools.          **Skills**  Informatica: Strong experience in Informatica MDM Hub Console 10\\.5(good to have), IDD, SIF, Match/Merge rules, and provisioning tool, IDQ10\\.5(good to have), putty.           SQL: Should be good in writing SQL queries (Oracle DB) as this will be needed for data analysis and troubleshooting.           Scripting: Good to have UNIX Shell scripting knowledge as this will be required to analyze scripts for any IDQ or MDM job failures.           Autosys and MFT: Experienced in third party scheduling tool like Autosys, and file transfer tools like IBM Sterling 

## Interpretation and limits

Before learning values were zero despite a QueryCanceled market failure. They are not evidence of low learning value. After values use the existing broad extraction scope, not only the 90-day grading cohort. Percentages for different skills overlap.
After market metadata: `{"source": "public.skill_prevalence", "taxonomy_versions": ["31d08964f877"], "extraction_run_ids": [2], "total_jobs": 127801, "read_at": "2026-09-14T02:50:42.387478+00:00", "population": "extraction_snapshot", "prevalence_pct": {"SQL": 25.8, "Python": 28.1, "PostgreSQL": 3.7, "SQL Server": 4.1, "Databricks": 3.7, "Spark": 4.7, "AWS": 27.9, "Azure": 14.6, "Redshift": 1.7, "Power BI": 5.9}}`.
Fit quality describes the numerical fit band. Apply decisions separately respect explicit blockers and review flags. The old alignment score is retained for historical diagnostics and does not decide applications.
Search lane and review priority are optional because clean_jobs does not currently carry them. Missing context is recorded; it does not manufacture survival/bridge origin.
SQL Server and PostgreSQL proficiency must be confirmed independently of broad SQL capability. The configuration snapshot records the exact assumptions used for this run.
Counts are diagnostics, not optimization targets. QA identity, platform responsibility, ecosystem dependence, seniority wording and adjacent gaps should be reviewed through representative evidence.
