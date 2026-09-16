# Representative deterministic traces

Source: `data\outputs\results-db-90-days-requirements.csv`

Each section is produced by the normal grader with trace capture enabled. No explanation is generated separately.

## clean TARGET data engineer: Lead Analyst Data Engineer

target_lane: eligibility established by target_eligibility; selected by eligible lane scores. Title evidence: data engineer, data, engineer. Capability evidence: sql, etl, integration_workflows, azure, aws, python. Review flags: lead_responsibility, overlevel_experience, multiple_required_gaps. Fit 56.5; manual_review by configured_review_gate.

- Job id: `in-1f5c8418605bc555`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 15.0, "survival_lane": 0, "target_lane": 62.0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `56.5` / `38.33` / `0.815`
- Decision / AI review: `manual_review` / `False`
- Lane owner: `target_eligibility`; decision owner: `configured_review_gate`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": true, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `integration_data_evidence` → `integration_data_ok`: retained
  - `target_eligibility` → `eligible`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `overlevel_penalty` → `fit_score`: retained
  - `lead_review_gate` → `review_flags`: retained
  - `overlevel_review_gate` → `review_flags`: retained
  - `many_required_gaps` → `review_flags`: retained
  - `possible_fit_score` → `fit_quality`: retained
  - `configured_review_gate` → `apply_decision`: retained

Matched role signals: strong_target_title_terms, core_data_signals, backend_data_signals, support_signals, bridge_positive_signals, analytics_terms, secondary_core_overlap, data_title_identity, database_development, integration_data, database_usage, data_stack_usage

## integration promoted by data evidence: Lead Integration Engineer, EPIC Bridges

target_lane: eligibility established by supported_integration_target; selected by eligible lane scores. Title evidence: integration, engineer. Capability evidence: data_formats, sql, apis, integration_workflows, systems, operations. Review flags: lead_responsibility. Fit 88; manual_review by configured_review_gate.

- Job id: `li-4427707701`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 20.0, "survival_lane": 0, "target_lane": 48.0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `88.0` / `0` / `0.754`
- Decision / AI review: `manual_review` / `False`
- Lane owner: `supported_integration_target`; decision owner: `configured_review_gate`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": true, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `integration_data_evidence` → `integration_data_ok`: retained
  - `supported_integration_target` → `eligible`: retained
  - `supported_integration_target` → `points.target_lane`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `lead_review_gate` → `review_flags`: retained
  - `good_fit_score` → `fit_quality`: retained
  - `configured_review_gate` → `apply_decision`: retained

Matched role signals: core_data_signals, support_signals, bridge_positive_signals, secondary_core_overlap, integration_data, database_usage, integration_title_identity, transferable_data

## integration rejected by domain conflict: Aircraft Systems Integration Engineer

wrong_lane: eligibility established by lane_policy.fallback_lane; selected by eligible lane scores. Title evidence: aircraft, engineer, integration. Capability evidence: integration_workflows, data_quality, systems, operations, dev_practices. Blockers: wrong_role_identity. Fit 15; skip by configured_hard_blocker.

- Job id: `li-4417640996`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 60.0}`
- Fit / learning / confidence: `15` / `0.0` / `0.97`
- Decision / AI review: `skip` / `False`
- Lane owner: `lane_policy.fallback_lane`; decision owner: `configured_hard_blocker`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": false, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": false, "transferable_data_strong": false}`
- Triggered action effects:
  - `wrong_role_gate` → `blockers`: retained
  - `weak_fit_score` → `fit_quality`: retained
  - `configured_hard_blocker` → `apply_decision`: retained

Matched role signals: core_data_signals, bridge_positive_signals, secondary_core_overlap, hardware_title_identity, integration_title_identity, hardware_responsibilities

## ecosystem-heavy vendor specialist: Senior Workday Integration Developer - Extend

secondary_lane: eligibility established by secondary_eligibility; selected by eligible lane scores. Title evidence: developer, workday, integration. Capability evidence: data_formats, etl, apis, integration_workflows, systems, operations. Review flags: ecosystem_specialization_review, lead_responsibility. Fit 62.12; manual_review by configured_review_gate.

- Job id: `in-3fd4d35537a37358`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 23.0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `62.12` / `0` / `0.9`
- Decision / AI review: `manual_review` / `False`
- Lane owner: `secondary_eligibility`; decision owner: `configured_review_gate`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": true, "ecosystem_specialized": true, "integration_data_ok": false, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `ecosystem_specialization_evidence` → `ecosystem_specialized`: retained
  - `ecosystem_concentration_evidence` → `ecosystem_role_concentration`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `ecosystem_usage_penalty` → `fit_score`: retained
  - `ecosystem_limited_transfer_fit` → `fit_score`: retained
  - `ecosystem_limited_transfer_fit` → `review_flags`: retained
  - `lead_review_gate` → `review_flags`: retained
  - `possible_fit_score` → `fit_quality`: retained
  - `configured_review_gate` → `apply_decision`: retained

Matched role signals: non_target_title_terms, core_data_signals, support_signals, bridge_positive_signals, secondary_core_overlap, ecosystem_terms, ecosystem_title, integration_data, integration_title_identity, ecosystem_specialization, transferable_data

## data platform usage: Senior Analytics Engineer

secondary_lane: eligibility established by secondary_eligibility; selected by eligible lane scores. Title evidence: analytics engineer. Capability evidence: sql, etl, integration_workflows, airflow, python, devops. Review flags: multiple_required_gaps. Fit 72.64; manual_review by configured_review_gate.

- Job id: `in-435894c3393cdbf3`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 33.0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `72.64` / `6.53` / `0.9`
- Decision / AI review: `manual_review` / `False`
- Lane owner: `secondary_eligibility`; decision owner: `configured_review_gate`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": true, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `integration_data_evidence` → `integration_data_ok`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `ecosystem_usage_penalty` → `fit_score`: retained
  - `many_required_gaps` → `review_flags`: retained
  - `possible_fit_score` → `fit_quality`: retained
  - `configured_review_gate` → `apply_decision`: retained

Matched role signals: secondary_title_terms, core_data_signals, support_signals, bridge_positive_signals, analytics_terms, analytics_title_terms, secondary_core_overlap, ecosystem_terms, integration_data, database_usage, data_stack_usage, data_platform_terms

## SQL/PLSQL database role: Software Development Engineer

secondary_lane: eligibility established by secondary_eligibility; selected by eligible lane scores. Capability evidence: sql, apis, java, devops, software_engineering, operations. Fit 81.31; manual_review by ambiguous_role_review.

- Job id: `in-03552ccc928ad277`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 12.0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `81.31` / `4.55` / `0.75`
- Decision / AI review: `manual_review` / `True`
- Lane owner: `secondary_eligibility`; decision owner: `ambiguous_role_review`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": false, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `good_fit_score` → `fit_quality`: retained
  - `ambiguous_role_review` → `apply_decision`: retained

Matched role signals: core_data_signals, backend_data_signals, support_signals, bridge_positive_signals, secondary_core_overlap, database_usage, transferable_data

## QA/test role: Software Engineer, Manufacturing Test

wrong_lane: eligibility established by lane_policy.fallback_lane; selected by eligible lane scores. Title evidence: software engineer, test, engineer. Capability evidence: etl, kafka, python, git, devops, data_quality. Lane restrictions: hard_exclusion_override. Blockers: wrong_role_identity. Fit 15; skip by configured_hard_blocker.

- Job id: `in-d03366b27b565075`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 40.0}`
- Fit / learning / confidence: `15` / `0.0` / `0.97`
- Decision / AI review: `skip` / `False`
- Lane owner: `lane_policy.fallback_lane`; decision owner: `configured_hard_blocker`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": false, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `secondary_eligibility` → `eligible`: overridden
  - `hard_exclusion_override` → `eligible`: retained
  - `wrong_role_gate` → `blockers`: retained
  - `weak_fit_score` → `fit_quality`: retained
  - `configured_hard_blocker` → `apply_decision`: retained

Matched role signals: secondary_title_terms, non_target_title_terms, core_data_signals, backend_data_signals, support_signals, secondary_core_overlap, test_title_identity, integration_data, transferable_data

## infrastructure/platform role: Senior Software Development Engineer (Site Reliability)

wrong_lane: eligibility established by lane_policy.fallback_lane; selected by eligible lane scores. Title evidence: site reliability, engineer. Capability evidence: etl, apis, integration_workflows, azure, python, git. Lane restrictions: hard_exclusion_override. Blockers: wrong_role_identity. Fit 15; skip by configured_hard_blocker.

- Job id: `in-297ddc2108f979e1`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 68.0}`
- Fit / learning / confidence: `15` / `0.0` / `0.97`
- Decision / AI review: `skip` / `False`
- Lane owner: `lane_policy.fallback_lane`; decision owner: `configured_hard_blocker`
- Policy flags: `{"backend_ok": false, "bridge_ok": true, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": false, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `bridge_evidence` → `bridge_ok`: retained
  - `secondary_eligibility` → `eligible`: overridden
  - `bridge_eligibility` → `eligible`: overridden
  - `hard_exclusion_override` → `eligible`: retained
  - `wrong_role_gate` → `blockers`: retained
  - `weak_fit_score` → `fit_quality`: retained
  - `configured_hard_blocker` → `apply_decision`: retained

Matched role signals: core_data_signals, support_signals, bridge_positive_signals, analytics_terms, platform_heavy_terms, secondary_core_overlap, operational_title_identity, transferable_data

## bridge/support role: API Analyst

bridge_lane: eligibility established by bridge_eligibility; selected by eligible lane scores. Capability evidence: data_formats, sql, apis, integration_workflows, kafka, systems. Fit 65; manual_review by ambiguous_role_review.

- Job id: `in-13c17d2f098489fd`
- Lane scores: `{"bridge_lane": 22.0, "secondary_lane": 18.0, "survival_lane": 0, "target_lane": 0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `65` / `0.0` / `0.614`
- Decision / AI review: `manual_review` / `True`
- Lane owner: `bridge_eligibility`; decision owner: `ambiguous_role_review`
- Policy flags: `{"backend_ok": false, "bridge_ok": true, "data_identity": true, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": false, "transferable_data_strong": false}`
- Triggered action effects:
  - `data_evidence` → `data_ok`: retained
  - `bridge_evidence` → `bridge_ok`: retained
  - `transferable_data_identity` → `data_identity`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `bridge_eligibility` → `eligible`: retained
  - `ecosystem_usage_penalty` → `fit_score`: retained
  - `possible_fit_score` → `fit_quality`: retained
  - `ambiguous_role_review` → `apply_decision`: retained

Matched role signals: core_data_signals, support_signals, bridge_positive_signals, secondary_core_overlap, ecosystem_terms, database_usage, transferable_data

## ambiguous/manual-review role: Data Engineer - Oracle PL/SQL

target_lane: eligibility established by target_eligibility; selected by eligible lane scores. Title evidence: data engineer, data, engineer. Capability evidence: sql, etl, data_quality, monitoring. Review flags: lead_responsibility. Fit 78.75; manual_review by configured_review_gate.

- Job id: `in-1393eac0b7e7e3be`
- Lane scores: `{"bridge_lane": 0, "secondary_lane": 3.0, "survival_lane": 0, "target_lane": 42.0, "wrong_lane": 0.0}`
- Fit / learning / confidence: `78.75` / `0` / `0.725`
- Decision / AI review: `manual_review` / `True`
- Lane owner: `target_eligibility`; decision owner: `configured_review_gate`
- Policy flags: `{"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": true, "transferable_data_strong": false}`
- Triggered action effects:
  - `database_development_evidence` → `data_ok`: retained
  - `integration_data_evidence` → `integration_data_ok`: retained
  - `target_eligibility` → `eligible`: retained
  - `secondary_eligibility` → `eligible`: retained
  - `ecosystem_usage_penalty` → `fit_score`: retained
  - `lead_review_gate` → `review_flags`: retained
  - `possible_fit_score` → `fit_quality`: retained
  - `configured_review_gate` → `apply_decision`: retained

Matched role signals: strong_target_title_terms, core_data_signals, support_signals, bridge_positive_signals, secondary_core_overlap, ecosystem_terms, data_title_identity, database_development, integration_data, database_usage, transferable_data

