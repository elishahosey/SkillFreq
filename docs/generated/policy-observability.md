# SkillFreq policy observability report

Generated from the loaded policy snapshot. Policy remains authored in YAML; this is an inspection view.

## Validation and quality findings

- {"classification": "unclear", "groups": ["ecosystem.products", "ecosystem.title"], "kind": "equivalent_term_groups", "severity": "info"}
- {"explanation": "The DB grading view does not provide search_lane; policy is structurally reachable when that context is supplied.", "field": "search_lane", "input_context": "db", "kind": "input_contract_unavailable", "lane": "survival_lane", "rules": ["bridge_eligibility", "survival_context"], "severity": "info"}

## Derived flag dependencies

### `data_ok`

Produced by: data_evidence, database_and_data_stack_evidence, database_development_evidence
Consumed by: description_exclusion_guard, positive_and_exclusion_signals, secondary_eligibility, survival_context, target_eligibility, target_title_weak_data_content
Downstream: role_lane

### `backend_ok`

Produced by: backend_evidence
Consumed by: description_exclusion_guard, positive_and_exclusion_signals, secondary_eligibility, survival_context
Downstream: role_lane

### `bridge_ok`

Produced by: bridge_evidence
Consumed by: admin_ownership_guard, analytics_bridge, bridge_eligibility, support_bridge, survival_context
Downstream: role_lane

### `data_identity`

Produced by: transferable_data_identity
Consumed by: bridge_title_guard, target_eligibility
Downstream: role_lane

### `integration_data_ok`

Produced by: integration_data_evidence
Consumed by: integration_requires_data_domain, supported_integration_target
Downstream: role_lane

### `transferable_data_strong`

Produced by: transferable_data_counterweight
Consumed by: ecosystem_admin_evidence, ecosystem_concentration_evidence, ecosystem_limited_transfer_fit, ecosystem_low_transfer_admin_guard, ecosystem_transferable_specialist_fit
Downstream: fit, role_lane

### `ecosystem_specialized`

Produced by: ecosystem_specialization_evidence
Consumed by: ecosystem_concentration_evidence, ecosystem_limited_transfer_fit, ecosystem_transferable_specialist_fit
Downstream: fit, role_lane

### `ecosystem_role_concentration`

Produced by: ecosystem_concentration_evidence
Consumed by: ecosystem_identity_guard, ecosystem_low_transfer_specialist_guard
Downstream: role_lane

### `ecosystem_admin_identity`

Produced by: ecosystem_admin_evidence
Consumed by: ecosystem_admin_fit_gate, ecosystem_concentration_evidence, ecosystem_low_transfer_admin_guard
Downstream: fit, role_lane

### `ecosystem_ownership_gate`

Produced by: ecosystem_ownership_evidence
Consumed by: ecosystem_concentration_evidence, ecosystem_dependence, ecosystem_limited_transfer_fit, ecosystem_transferable_specialist_fit
Downstream: fit, role_lane

## Rule dependency index

| Rule | Stage | Priority | Reads | Writes | Term group |
|---|---|---:|---|---|---|
| hard_wrong_title_terms | lane_signal | None |  |  | lane.hard_wrong_title_terms |
| strong_target_title_terms | lane_signal | None |  |  | lane.strong_target_title_terms |
| secondary_title_terms | lane_signal | None |  |  | lane.secondary_title_terms |
| bridge_title_terms | lane_signal | None |  |  | lane.bridge_title_terms |
| consultant_title_terms | lane_signal | None |  |  | lane.consultant_title_terms |
| bad_consultant_title_terms | lane_signal | None |  |  | lane.bad_consultant_title_terms |
| non_target_title_terms | lane_signal | None |  |  | lane.non_target_title_terms |
| core_data_signals | lane_signal | None |  |  | lane.core_data_signals |
| backend_data_signals | lane_signal | None |  |  | lane.backend_data_signals |
| support_signals | lane_signal | None |  |  | lane.support_signals |
| bridge_positive_signals | lane_signal | None |  |  | lane.bridge_positive_signals |
| analytics_terms | lane_signal | None |  |  | lane.analytics_terms |
| wrong_desc_terms | lane_signal | None |  |  | lane.wrong_desc_terms |
| platform_heavy_terms | lane_signal | None |  |  | lane.platform_heavy_terms |
| platform_admin_title_terms | lane_signal | None |  |  | lane.platform_admin_title_terms |
| low_signal_terms | lane_signal | None |  |  | lane.low_signal_terms |
| analytics_title_terms | lane_signal | None |  |  | lane.analytics_title_terms |
| explicit_unrelated_ownership | lane_signal | None |  |  | pattern |
| secondary_core_overlap | lane_signal | None |  |  | lane.core_data_signals |
| ecosystem_terms | lane_signal | None |  |  | ecosystem.products |
| ecosystem_ownership | lane_signal | None |  |  | ecosystem.ownership |
| ecosystem_title | lane_signal | None |  |  | ecosystem.title |
| qa_title_identity | lane_signal | None |  |  | pattern |
| test_title_identity | lane_signal | None |  |  | pattern |
| infrastructure_title_identity | lane_signal | None |  |  | pattern |
| support_title_identity | lane_signal | None |  |  | pattern |
| operational_title_identity | lane_signal | None |  |  | pattern |
| data_title_identity | lane_signal | None |  |  | pattern |
| hardware_title_identity | lane_signal | None |  |  | pattern |
| database_development | lane_signal | None |  |  | identity.database_development |
| integration_data | lane_signal | None |  |  | identity.integration_data |
| database_usage | lane_signal | None |  |  | identity.database_usage |
| integration_title_identity | lane_signal | None |  |  | pattern |
| security_title_identity | lane_signal | None |  |  | pattern |
| data_stack_usage | lane_signal | None |  |  | identity.data_stack |
| hardware_responsibilities | lane_signal | None |  |  | identity.hardware_responsibilities |
| ecosystem_specialization | lane_signal | None |  |  | ecosystem.specialization |
| ecosystem_administration | lane_signal | None |  |  | ecosystem.administration |
| ecosystem_admin_title | lane_signal | None |  |  | ecosystem.admin_titles |
| data_platform_terms | lane_signal | None |  |  | ecosystem.data_platforms |
| data_platform_title | lane_signal | None |  |  | ecosystem.data_platforms |
| data_platform_specialization | lane_signal | None |  |  | ecosystem.data_specialization |
| transferable_data | lane_signal | None |  |  | ecosystem.transferable |
| data_evidence | eligibility | 1000 | hits.core_data_signals, hits.support_signals | data_ok |  |
| backend_evidence | eligibility | 990 | hits.backend_data_signals | backend_ok |  |
| bridge_evidence | eligibility | 980 | hits.bridge_positive_signals, hits.support_signals | bridge_ok |  |
| transferable_data_identity | eligibility | 970 | hits.analytics_terms, hits.core_data_signals, hits.platform_heavy_terms, hits.support_signals | data_identity |  |
| target_eligibility | eligibility | 900 | data_identity, data_ok, hits.bridge_title_terms, hits.consultant_title_terms, hits.data_title_identity, hits.non_target_title_terms, hits.strong_target_title_terms | eligible |  |
| secondary_eligibility | eligibility | 890 | backend_ok, data_ok, hits.platform_heavy_terms | eligible |  |
| bridge_title_guard | eligibility | 880 | data_identity, hits.bridge_title_terms | eligible |  |
| bridge_eligibility | eligibility | 870 | bridge_ok, hits.bridge_title_terms, hits.consultant_title_terms, hits.platform_heavy_terms, hits.secondary_title_terms, hits.strong_target_title_terms, search_lane | eligible |  |
| survival_context | eligibility | 860 | backend_ok, bridge_ok, data_ok, hits.non_target_title_terms, hits.platform_heavy_terms, search_lane | eligible, points.survival_lane |  |
| target_title_weak_data_content | eligibility | 800 | data_ok, hits.strong_target_title_terms | contradictions |  |
| target_secondary_title_conflict | eligibility | 790 | hits.secondary_title_terms, hits.strong_target_title_terms | contradictions |  |
| positive_and_exclusion_signals | eligibility | 780 | backend_ok, data_ok, hits.wrong_desc_terms | contradictions |  |
| target_title_platform_ownership | eligibility | 770 | hits.platform_heavy_terms, hits.strong_target_title_terms | contradictions |  |
| analytics_identity_guard | eligibility | 700 | hits.analytics_title_terms | eligible |  |
| analytics_bridge | eligibility | 690 | bridge_ok, hits.analytics_title_terms, hits.platform_heavy_terms | eligible |  |
| consultant_identity | eligibility | 600 | hits.consultant_title_terms | eligible |  |
| consultant_bridge_exception | eligibility | 590 | hits.bad_consultant_title_terms, hits.bridge_positive_signals, hits.consultant_title_terms, hits.core_data_signals, hits.platform_heavy_terms, hits.support_signals, hits.wrong_desc_terms | eligible |  |
| admin_ownership_guard | eligibility | 500 | bridge_ok, hits.core_data_signals, hits.platform_admin_title_terms | eligible |  |
| description_exclusion_guard | eligibility | 490 | backend_ok, data_ok, hits.wrong_desc_terms | eligible |  |
| low_signal_guard | eligibility | 480 | hits.low_signal_terms, hits.strong_target_title_terms | eligible |  |
| generic_software_guard | eligibility | 470 | hits.non_target_title_terms, hits.strong_target_title_terms | eligible |  |
| support_identity_guard | eligibility | 460 | hits.support_title_identity | eligible |  |
| support_secondary_guard | eligibility | 450 | hits.support_title_identity | eligible |  |
| support_bridge | eligibility | 440 | bridge_ok, hits.support_title_identity | eligible |  |
| platform_ownership_guard | eligibility | 100 | hits.infrastructure_title_identity, hits.platform_heavy_terms | eligible |  |
| hard_exclusion_override | eligibility | 0 | hard_exclusions | eligible |  |
| database_development_evidence | eligibility | 995 | hits.database_development, hits.database_usage, hits.integration_data | data_ok |  |
| integration_data_evidence | eligibility | 960 | hits.database_development, hits.database_usage, hits.integration_data | integration_data_ok |  |
| supported_integration_target | eligibility | 895 | hits.integration_title_identity, integration_data_ok | eligible, points.target_lane |  |
| integration_requires_data_domain | eligibility | 430 | hits.integration_title_identity, integration_data_ok | eligible |  |
| security_domain_identity_guard | eligibility | 210 | hits.security_title_identity | eligible |  |
| ecosystem_identity_guard | eligibility | 200 | ecosystem_role_concentration | eligible |  |
| database_and_data_stack_evidence | eligibility | 994 | hits.data_stack_usage, hits.database_usage, hits.support_signals | data_ok |  |
| integration_hardware_domain_guard | eligibility | 205 | hits.hardware_responsibilities, hits.integration_title_identity | eligible |  |
| transferable_data_counterweight | eligibility | 958 | hits.transferable_data | transferable_data_strong |  |
| ecosystem_specialization_evidence | eligibility | 956 | hits.ecosystem_specialization, hits.ecosystem_terms, hits.ecosystem_title | ecosystem_specialized |  |
| ecosystem_ownership_evidence | eligibility | 954 | hits.ecosystem_ownership, hits.ecosystem_terms, hits.ecosystem_title | ecosystem_ownership_gate |  |
| ecosystem_admin_evidence | eligibility | 952 | hits.ecosystem_admin_title, hits.ecosystem_administration, hits.ecosystem_terms, hits.ecosystem_title, transferable_data_strong | ecosystem_admin_identity |  |
| ecosystem_concentration_evidence | eligibility | 950 | ecosystem_admin_identity, ecosystem_ownership_gate, ecosystem_specialized, hits.ecosystem_specialization, hits.ecosystem_title, transferable_data_strong | ecosystem_role_concentration |  |
| ecosystem_low_transfer_admin_guard | eligibility | 194 | ecosystem_admin_identity, transferable_data_strong | eligible |  |
| ecosystem_low_transfer_specialist_guard | eligibility | 193 | ecosystem_role_concentration, hits.ecosystem_specialization, hits.transferable_data | eligible |  |
| overlevel_penalty | fit | 100 | years_required | fit_score |  |
| ecosystem_usage_penalty | fit | 90 | hits.ecosystem_terms | fit_score |  |
| ecosystem_dependence | fit | 80 | ecosystem_ownership_gate | fit_score, blockers |  |
| required_core_gate | fit | 70 | has_hard_requirement_blockers | blockers |  |
| lead_review_gate | fit | 60 | is_lead_like | review_flags |  |
| overlevel_review_gate | fit | 50 | years_required | review_flags |  |
| many_required_gaps | fit | 40 | missing_required_atomic | review_flags |  |
| wrong_role_gate | fit | 30 | role_lane | blockers |  |
| ecosystem_specific_experience | fit | 85 | hits.ecosystem_ownership, hits.ecosystem_title, years_required | fit_score, review_flags |  |
| ecosystem_transferable_specialist_fit | fit | 84 | ecosystem_ownership_gate, ecosystem_specialized, transferable_data_strong | fit_score, review_flags |  |
| ecosystem_limited_transfer_fit | fit | 83 | ecosystem_ownership_gate, ecosystem_specialized, transferable_data_strong | fit_score, review_flags |  |
| ecosystem_admin_fit_gate | fit | 82 | ecosystem_admin_identity | blockers |  |
| good_fit_score | quality | 100 | fit_score | fit_quality |  |
| possible_fit_score | quality | 90 | fit_score | fit_quality |  |
| weak_fit_score | quality | 0 | always | fit_quality |  |
| configured_hard_blocker | decision | 1000 | blockers | apply_decision |  |
| insufficient_fit | decision | 950 | fit_score | apply_decision |  |
| configured_review_gate | decision | 900 | review_flags | apply_decision |  |
| ambiguous_role_review | decision | 850 | ai_review_required | apply_decision |  |
| fallback_search_context | decision | 800 | search_lane | apply_decision |  |
| strong_primary_fit | decision | 700 | fit_score, role_lane | apply_decision |  |
| adjacent_or_moderate_fit | decision | 0 | always | apply_decision |  |

## Term-group overlap

- alignment.ai_terms ↔ lane.wrong_desc_terms: 1 shared; unclear
- alignment.analytics ↔ lane.bridge_positive_signals: 1 shared; unclear
- alignment.early_career ↔ alignment.no_experience: 2 shared; unclear
- alignment.integration_keywords ↔ alignment.pipeline_keywords: 1 shared; unclear
- alignment.integration_keywords ↔ ecosystem.transferable: 5 shared; intentional reuse
- alignment.integration_keywords ↔ identity.integration_data: 1 shared; unclear
- alignment.integration_keywords ↔ lane.bridge_positive_signals: 4 shared; intentional reuse
- alignment.integration_keywords ↔ lane.core_data_signals: 5 shared; intentional reuse
- alignment.ml_keywords ↔ lane.wrong_desc_terms: 2 shared; unclear
- alignment.modern_heavy ↔ identity.data_stack: 3 shared; intentional reuse
- alignment.pipeline_keywords ↔ ecosystem.transferable: 9 shared; intentional reuse
- alignment.pipeline_keywords ↔ identity.integration_data: 7 shared; intentional reuse
- alignment.pipeline_keywords ↔ lane.bridge_positive_signals: 2 shared; unclear
- alignment.pipeline_keywords ↔ lane.core_data_signals: 10 shared; intentional reuse
- ecosystem.admin_titles ↔ lane.non_target_title_terms: 2 shared; potentially conflicting
- ecosystem.administration ↔ ecosystem.ownership: 1 shared; unclear
- ecosystem.data_platforms ↔ identity.data_stack: 6 shared; intentional reuse
- ecosystem.data_platforms ↔ lane.analytics_terms: 2 shared; potentially conflicting
- ecosystem.ownership ↔ lane.platform_heavy_terms: 1 shared; unclear
- ecosystem.products ↔ ecosystem.title: 13 shared; likely redundant
- ecosystem.transferable ↔ identity.database_development: 5 shared; intentional reuse
- ecosystem.transferable ↔ identity.database_usage: 10 shared; intentional reuse
- ecosystem.transferable ↔ identity.integration_data: 11 shared; intentional reuse
- ecosystem.transferable ↔ lane.backend_data_signals: 2 shared; potentially conflicting
- ecosystem.transferable ↔ lane.bridge_positive_signals: 14 shared; potentially conflicting
- ecosystem.transferable ↔ lane.core_data_signals: 21 shared; potentially conflicting
- ecosystem.transferable ↔ lane.support_signals: 9 shared; potentially conflicting
- identity.data_stack ↔ lane.analytics_terms: 2 shared; potentially conflicting
- identity.database_development ↔ lane.bridge_positive_signals: 1 shared; potentially conflicting
- identity.database_development ↔ lane.core_data_signals: 2 shared; potentially conflicting
- identity.database_development ↔ lane.support_signals: 4 shared; potentially conflicting
- identity.database_usage ↔ lane.backend_data_signals: 2 shared; potentially conflicting
- identity.database_usage ↔ lane.bridge_positive_signals: 4 shared; potentially conflicting
- identity.database_usage ↔ lane.support_signals: 4 shared; potentially conflicting
- identity.integration_data ↔ lane.bridge_positive_signals: 1 shared; potentially conflicting
- identity.integration_data ↔ lane.core_data_signals: 8 shared; potentially conflicting
- lane.analytics_terms ↔ lane.bridge_positive_signals: 5 shared; intentional reuse
- lane.analytics_title_terms ↔ lane.secondary_title_terms: 3 shared; potentially conflicting
- lane.bridge_positive_signals ↔ lane.core_data_signals: 12 shared; potentially conflicting
- lane.bridge_positive_signals ↔ lane.support_signals: 6 shared; intentional reuse
- lane.core_data_signals ↔ lane.support_signals: 2 shared; potentially conflicting
- lane.non_target_title_terms ↔ lane.platform_admin_title_terms: 1 shared; potentially conflicting
- lane.non_target_title_terms ↔ lane.secondary_title_terms: 15 shared; intentional reuse

## Ecosystem taxonomy recommendation

- Keep vendor ecosystems (Informatica, Workday, Salesforce, ServiceNow, Boomi, MuleSoft) separate from specialized domains (MDM) and data platforms (Palantir, Snowflake, Databricks, Redshift, BigQuery).
- Vendor groups primarily affect concentration, specialization, ownership and fit policy.
- MDM is a domain signal that can occur across products; merging it with a vendor obscures transferable data work.
- Data platforms are common implementation tools in data roles, so keeping them distinct reduces accidental wrong-lane penalties.
