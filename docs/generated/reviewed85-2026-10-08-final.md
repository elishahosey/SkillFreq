# Reviewed 85-job calibration comparison

Human labels remain historical; lower scores and more skips do not establish correctness. New score-quality and requirement-interpretation counts require human re-review.

Before: `data\outputs\results-db-90-days-requirement-semantics.csv`. After: `data\outputs\results-reviewed85-2026-10-08-final.csv`. Reviews: `data\outputs\calibration_review_2026-09-25.xlsx`.

Exact reviewed membership and exported input fields checked; frozen market context checked.
This is a re-evaluation of retained exports, not a proven lossless original-input replay.

```json
{
  "jobs": 85,
  "before": {
    "apply_decision": {
      "skip": 10,
      "manual_review": 69,
      "apply_now": 6
    },
    "role_lane": {
      "target_lane": 31,
      "secondary_lane": 53,
      "bridge_lane": 1
    },
    "fit_quality": {
      "weak_fit": 10,
      "good_fit": 13,
      "possible_fit": 62
    },
    "grading_version": {
      "3678ae1f5835169c": 85
    },
    "taxonomy_version": {
      "31d08964f877": 85
    }
  },
  "after": {
    "apply_decision": {
      "skip": 35,
      "manual_review": 49,
      "apply_now": 1
    },
    "role_lane": {
      "target_lane": 31,
      "secondary_lane": 42,
      "wrong_lane": 11,
      "bridge_lane": 1
    },
    "fit_quality": {
      "weak_fit": 29,
      "possible_fit": 48,
      "good_fit": 8
    },
    "grading_version": {
      "5e01f710d103c4c0": 85
    },
    "taxonomy_version": {
      "31d08964f877": 85
    }
  },
  "historical": {
    "apply_decision": {
      "manual_review": 73,
      "skip": 4,
      "apply_now": 8
    },
    "role_lane": {
      "target_lane": 31,
      "secondary_lane": 53,
      "bridge_lane": 1
    },
    "fit_quality": {
      "possible_fit": 60,
      "good_fit": 21,
      "weak_fit": 4
    },
    "grading_version": {
      "5b4f855d2cdf0292": 85
    },
    "taxonomy_version": {
      "31d08964f877": 85
    }
  },
  "decisions": {
    "skip -> skip": 7,
    "apply_now -> manual_review": 3,
    "skip -> manual_review": 3,
    "manual_review -> skip": 26,
    "manual_review -> manual_review": 43,
    "apply_now -> skip": 2,
    "apply_now -> apply_now": 1
  },
  "human_labels": {
    "review_rating": {
      "1": 39,
      "3": 31,
      "2": 15
    },
    "score_quality": {
      "reasonable": 36,
      "unclear": 2,
      "too_high": 32,
      "unanswered": 15
    },
    "requirement_interpretation": {
      "correct": 33,
      "incorrect": 14,
      "unclear": 23,
      "unanswered": 15
    }
  },
  "too_high_score_movement": {
    "lower": 15,
    "unchanged": 14,
    "higher": 3
  },
  "bad_decisions_before": {
    "apply_now": 5,
    "manual_review": 26
  },
  "bad_decisions_after": {
    "manual_review": 18,
    "skip": 13
  },
  "good_decision_changes": [
    "li-3835714098",
    "li-4427377748",
    "li-4428782487",
    "li-4428785426",
    "li-4430133938",
    "li-4430716870",
    "li-4418874694",
    "li-4418890226",
    "li-4429364899",
    "in-3976624db34e9d92",
    "in-76539d0ffaf6c48e"
  ],
  "good_lane_changes": [
    "in-a2232dcbee24f494"
  ],
  "atomic_disappearance_cases": 22,
  "learning_changes": 2
}
```

| Job | Human rating | Lane before → after | Decision before → after | Fit before → after |
|---|---|---|---|---|
| Data Engineering Solutions Lead (li-4370559928) | 1 | secondary_lane → secondary_lane | skip → skip | 52.43 → 36.43 |
| Senior Data Engineer (li-4317952467) | 3 | target_lane → target_lane | apply_now → manual_review | 79.93 → 79.93 |
| Data Engineer with AWS // onsite in NJ, TX, AZ, RI // W2 (li-4429359989) | 1 | target_lane → target_lane | skip → skip | 53.14 → 37.14 |
| Senior Accounts Payable Analyst (in-a2232dcbee24f494) | 1 | secondary_lane → wrong_lane | skip → skip | 48.43 → 15 |
| Senior Software Engineer Specialist (li-3835714098) | 1 | secondary_lane → secondary_lane | skip → manual_review | 51.51 → 59.51 |
| Data Engineer - Senior Associate (li-4369126870) | 3 | target_lane → target_lane | apply_now → manual_review | 84.0 → 84.0 |
| Product Manager [Multiple Positions Available] (li-4419589094) | 2 | secondary_lane → wrong_lane | manual_review → skip | 62.29 → 15 |
| Senior Software Engineer Specialist - United States (li-4427377748) | 1 | secondary_lane → secondary_lane | skip → manual_review | 51.51 → 59.51 |
| Senior Software Engineer Specialist - United States (li-4428782487) | 1 | secondary_lane → secondary_lane | skip → manual_review | 51.51 → 59.51 |
| Principal Data Engineer (li-4430985604) | 1 | target_lane → target_lane | skip → skip | 54.61 → 38.61 |
| Sr. Data Engineer (li-4419553203) | 2 | target_lane → target_lane | manual_review → manual_review | 57.41 → 57.41 |
| Data Engineer (Databricks + Informatica + Azure) (li-4429994053) | 2 | target_lane → target_lane | manual_review → manual_review | 81.93 → 81.93 |
| Global Data Engineer (li-4430112480) | 1 | target_lane → target_lane | manual_review → manual_review | 77.12 → 77.12 |
| Senior Data Engineer (li-4420401901) | 3 | target_lane → target_lane | manual_review → manual_review | 92.0 → 92.0 |
| Data Engineer (Palantir) (li-4429057139) | 1 | target_lane → target_lane | manual_review → manual_review | 93.85 → 93.85 |
| Data & Integration Engineer (li-4430448809) | 2 | target_lane → target_lane | manual_review → manual_review | 92.98 → 92.98 |
| Data Engineer (in-414f29729894e258) | 3 | target_lane → target_lane | apply_now → skip | 81.93 → 73.93 |
| Data Engineer (li-4429717603) | 3 | target_lane → target_lane | apply_now → skip | 81.93 → 73.93 |
| Lead Analyst Data Engineer (in-1f5c8418605bc555) | 1 | target_lane → target_lane | skip → skip | 53.5 → 53.5 |
| Data Migration Engineer (li-4427846037) | 1 | target_lane → target_lane | manual_review → manual_review | 77.03 → 77.03 |
| Data Engineer (li-4428735984) | 1 | target_lane → target_lane | manual_review → manual_review | 75.92 → 75.92 |
| Python Data Engineer (li-4427873184) | 1 | target_lane → target_lane | apply_now → apply_now | 79.56 → 79.56 |
| Sr Data Engineer (li-4430980731) | 1 | target_lane → target_lane | manual_review → manual_review | 77.72 → 74.72 |
| Software Development Engineer (in-a7246bfe0658b1cb) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 68.39 → 68.39 |
| Lead Data Engineer (in-83644ce3aae8e9c6) | 1 | target_lane → target_lane | manual_review → manual_review | 66.5 → 58.5 |
| Lead Data Engineer (in-b8c9a5b25683858c) | 1 | target_lane → target_lane | manual_review → manual_review | 66.5 → 58.5 |
| Full Stack Java Developer - Vice President (li-4409376381) | 3 | secondary_lane → secondary_lane | manual_review → skip | 81.63 → 65.63 |
| GenAI Python Systems Engineer –Senior Manager (li-4419083896) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 69.66 → 69.66 |
| GenAI Python Systems Engineer –Senior Manager (li-4419098213) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 69.66 → 69.66 |
| GenAI Python Systems Engineer –Senior Manager (li-4419098214) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 69.66 → 69.66 |
| Hadoop Data Engineer (in-bfa4bf3c6bab3150) | 2 | target_lane → target_lane | manual_review → manual_review | 58.79 → 69.29 |
| Hadoop Data Engineer (li-4430728625) | 2 | target_lane → target_lane | manual_review → manual_review | 58.79 → 69.29 |
| Software Development Engineer - Gen AI (li-4414401628) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 64.72 → 64.72 |
| Software Development Engineer - Gen AI (li-4414417182) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 64.72 → 64.72 |
| Senior Python Developer with Snowflake (li-4428785426) | 1 | secondary_lane → secondary_lane | manual_review → skip | 59.02 → 46.02 |
| Senior Python Developer with Snowflake (li-4430133938) | 1 | secondary_lane → secondary_lane | manual_review → skip | 59.02 → 46.02 |
| Senior Python Developer with Snowflake (li-4430716870) | 1 | secondary_lane → secondary_lane | manual_review → skip | 59.02 → 46.02 |
| Senior Analytics Engineer (in-435894c3393cdbf3) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 81.64 → 73.64 |
| Senior Developer (li-4428432329) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 72.5 → 72.5 |
| Data Engineer Architect (li-4429352945) | 1 | target_lane → target_lane | skip → skip | 43.62 → 27.62 |
| Senior Boomi Integration Engineer -Remote (li-4429363929) | 2 | secondary_lane → secondary_lane | manual_review → skip | 71.88 → 51.88 |
| Senior Developer (li-4429718775) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 72.5 → 72.5 |
| Data Engineer (li-4430187912) | 2 | target_lane → target_lane | manual_review → manual_review | 60.84 → 60.84 |
| Data Engineer (li-4430189904) | 1 | target_lane → target_lane | manual_review → manual_review | 60.84 → 60.84 |
| Senior Analytics Engineer (li-4430909333) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 81.64 → 73.64 |
| Sr Software Engineer (li-4430979731) | 2 | secondary_lane → secondary_lane | manual_review → manual_review | 74.12 → 82.12 |
| Senior Data Engineer (li-4430980297) | 1 | target_lane → target_lane | manual_review → manual_review | 76.4 → 68.4 |
| Principal Engineer – Data Platform & Backend (li-4429040065) | 3 | bridge_lane → bridge_lane | manual_review → skip | 65 → 49.35 |
| Software Engineer (Early Career Professional) (in-09415ae61dac6086) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 66.91 → 66.91 |
| Software Engineer (Early Career Professional) (li-4428758366) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 66.91 → 66.91 |
| Sr. Software Engineer - AI Innovation Team (li-4429398771) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 74.33 → 74.33 |
| Relief Valve Engineer (in-0a1e348e36c48063) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.69 → 15 |
| Fixed Equipment Specialist (in-69310eb291c9a4c5) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.69 → 15 |
| Relief Valve Technical Authority (in-c2d0d4d677accb09) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.69 → 15 |
| Chief Inspector (in-c6188d4c1a92e972) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.85 → 15 |
| Epic Payer Platform Lead (in-e766d9e3ba528aa5) | 3 | secondary_lane → wrong_lane | manual_review → skip | 67.93 → 15 |
| Global Financial Crimes Digital Assets Sanctions Screening Director (li-4414152041) | 3 | secondary_lane → wrong_lane | manual_review → skip | 65.76 → 15 |
| Fixed Equipment Specialist (li-4426895315) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.69 → 15 |
| Relief Valve Engineer (li-4427314270) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.69 → 15 |
| Sr Software Engineer (li-4428068034) | 2 | secondary_lane → secondary_lane | manual_review → manual_review | 66.21 → 74.21 |
| Relief Valve Technical Authority (li-4430167739) | 3 | secondary_lane → wrong_lane | manual_review → skip | 76.69 → 15 |
| Sr Data Engineer (li-4430478817) | 1 | target_lane → target_lane | manual_review → manual_review | 65.47 → 73.47 |
| Software Engineer, Lead (li-4418874694) | 1 | secondary_lane → secondary_lane | manual_review → skip | 62.04 → 46.04 |
| Software Engineer, Lead (li-4418890226) | 1 | secondary_lane → secondary_lane | manual_review → skip | 62.04 → 46.04 |
| Manager, SRE Engineer - PxE ERM (li-4419854523) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 66.48 → 66.48 |
| Manager, SRE Engineer - PxE ERM (li-4419856401) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 66.48 → 66.48 |
| Manager, SRE Engineer - PxE ERM (li-4419858341) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 66.48 → 66.48 |
| Manager, SRE Engineer - PxE ERM (li-4419865253) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 66.48 → 66.48 |
| Manager, SRE Engineer - PxE ERM (li-4419868237) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 66.48 → 66.48 |
| Manager, SRE Engineer - PxE ERM (li-4419872155) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 66.48 → 66.48 |
| Data Engineer (li-4429364899) | 1 | target_lane → target_lane | manual_review → skip | 59.26 → 43.26 |
| Principal AI Platform Engineer (in-3976624db34e9d92) | 1 | secondary_lane → secondary_lane | manual_review → skip | 71.18 → 55.18 |
| Lead/Principal Software Engineer (AWS, Java/Python) (in-76539d0ffaf6c48e) | 1 | secondary_lane → secondary_lane | manual_review → skip | 55.76 → 39.76 |
| Data Engineering Lead (in-81f7a66c7bf61db7) | 2 | secondary_lane → secondary_lane | manual_review → skip | 79.94 → 63.94 |
| Sr. Data Engineer (li-4364366476) | 1 | target_lane → target_lane | skip → skip | 43.68 → 43.68 |
| Data Governance Platform Admin (li-4391198134) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 78.45 → 85 |
| Business Intelligence Developer- Operations (li-4404782234) | 1 | secondary_lane → secondary_lane | manual_review → manual_review | 78.23 → 78.23 |
| Remote Oncology Data Engineer - Precision Medicine - Dallas, Tx (li-4410789354) | 3 | target_lane → target_lane | manual_review → manual_review | 80.5 → 80.5 |
| Team Lead - Integrations (li-4410814992) | 3 | secondary_lane → secondary_lane | manual_review → manual_review | 79.39 → 79.39 |
| Lead Data Engineer (li-4416865142) | 1 | target_lane → target_lane | manual_review → manual_review | 72.92 → 72.92 |
| ServiceNow SRE Engineering Manager (li-4419862163) | 2 | secondary_lane → secondary_lane | manual_review → skip | 63.25 → 51.25 |
| Staff Software Engineer, Data Ingestion - Slack (li-4419905338) | 2 | secondary_lane → secondary_lane | manual_review → skip | 57.33 → 49.33 |
| Staff Software Engineer, Data Ingestion - Slack (li-4419945133) | 2 | secondary_lane → secondary_lane | manual_review → skip | 57.33 → 49.33 |
| Sr. Data Engineer (li-4420214409) | 3 | target_lane → target_lane | apply_now → manual_review | 80.78 → 77.78 |
| Data Engineering Lead (li-4427348914) | 2 | secondary_lane → secondary_lane | manual_review → skip | 81.59 → 65.59 |
