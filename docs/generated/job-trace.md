# Lead Analyst Data Engineer

target_lane: eligibility established by target_eligibility; selected by eligible lane scores. Title evidence: data engineer, data, engineer. Capability evidence: sql, etl, integration_workflows, azure, aws, python. Review flags: lead_responsibility, overlevel_experience, multiple_required_gaps. Fit 56.5; manual_review by configured_review_gate.

Grading `5b4f855d2cdf0292`; taxonomy `31d08964f877`.

## Role evidence

- `strong_target_title_terms` (title, group `lane.strong_target_title_terms`): data engineer; target_lane +30
- `core_data_signals` (description, group `lane.core_data_signals`): data pipelines, data integration, pl/sql; target_lane +18
- `backend_data_signals` (description, group `lane.backend_data_signals`): postgresql; secondary_lane +6
- `support_signals` (description, group `lane.support_signals`): sql, python, git, pl/sql; bridge_lane +8
- `bridge_positive_signals` (description, group `lane.bridge_positive_signals`): sql, power bi, integration; bridge_lane +9
- `analytics_terms` (description, group `lane.analytics_terms`): power bi; bridge_lane +2
- `secondary_core_overlap` (description, group `lane.core_data_signals`): data pipelines, data integration, pl/sql; secondary_lane +9
- `data_title_identity` (title, group `None`): data, engineer; target_lane +0
- `database_development` (description, group `identity.database_development`): pl/sql; target_lane +6
- `integration_data` (description, group `identity.integration_data`): data pipelines, data integration; target_lane +0
- `database_usage` (description, group `identity.database_usage`): sql, sql server, postgresql; target_lane +0
- `data_stack_usage` (description, group `identity.data_stack`): databricks, redshift, pyspark; target_lane +8
- `data_platform_terms` (description, group `ecosystem.data_platforms`): databricks, redshift; target_lane +0
- `transferable_data` (description, group `ecosystem.transferable`): sql, sql server, postgresql, python, data pipelines, data integration, pl/sql; target_lane +0

Counts: {"analytics_terms": 1, "analytics_title_terms": 0, "backend_data_signals": 1, "bad_consultant_title_terms": 0, "bridge_positive_signals": 3, "bridge_title_terms": 0, "consultant_title_terms": 0, "core_data_signals": 3, "data_platform_specialization": 0, "data_platform_terms": 2, "data_platform_title": 0, "data_stack_usage": 3, "data_title_identity": 2, "database_development": 1, "database_usage": 3, "ecosystem_admin_title": 0, "ecosystem_administration": 0, "ecosystem_ownership": 0, "ecosystem_specialization": 0, "ecosystem_terms": 0, "ecosystem_title": 0, "hard_wrong_title_terms": 0, "hardware_responsibilities": 0, "hardware_title_identity": 0, "infrastructure_title_identity": 0, "integration_data": 2, "integration_title_identity": 0, "low_signal_terms": 0, "non_target_title_terms": 0, "operational_title_identity": 0, "ownership_exclusion": 0, "platform_admin_title_terms": 0, "platform_heavy_terms": 0, "qa_title_identity": 0, "secondary_core_overlap": 3, "secondary_title_terms": 0, "security_title_identity": 0, "strong_target_title_terms": 1, "support_signals": 4, "support_title_identity": 0, "test_title_identity": 0, "transferable_data": 7, "wrong_desc_terms": 0}

Atomic skills: [{"canonical_skill": "SQL", "matched_terms": ["sql"], "mention_count": 5}, {"canonical_skill": "Python", "matched_terms": ["python"], "mention_count": 1}, {"canonical_skill": "PostgreSQL", "matched_terms": ["postgresql"], "mention_count": 1}, {"canonical_skill": "SQL Server", "matched_terms": ["sql server"], "mention_count": 1}, {"canonical_skill": "Databricks", "matched_terms": ["databricks"], "mention_count": 4}, {"canonical_skill": "Spark", "matched_terms": ["pyspark"], "mention_count": 1}, {"canonical_skill": "AWS", "matched_terms": ["aws"], "mention_count": 4}, {"canonical_skill": "Azure", "matched_terms": ["azure"], "mention_count": 1}, {"canonical_skill": "Redshift", "matched_terms": ["redshift"], "mention_count": 1}, {"canonical_skill": "Power BI", "matched_terms": ["power bi"], "mention_count": 1}]

Capability concepts: {"ai_ml": ["ml"], "aws": ["glue", "athena", "aws", "redshift"], "azure": ["azure sql", "azure"], "data_platforms": ["power query", "databricks", "power bi"], "data_quality": ["data governance", "compliance"], "etl": ["data pipelines", "data integration", "pipeline", "pipelines"], "git": ["git"], "integration_workflows": ["integration", "data integration"], "operations": ["support"], "python": ["pandas", "python", "pyspark"], "spark": ["pyspark"], "sql": ["pl/sql", "sql", "sql server", "postgresql"], "systems": ["integration"], "testing": ["testing"]}

## Requirements

Groups retain section, source sentence, grammar type and candidate satisfaction.

### required
- `required_group_1` `all_of`: 7–10 years of implementation experience in cloud data architecture, with at least 5 years in aws environments. — skills ["AWS"]; satisfied skills []; group satisfied: `False`
- `required_group_2` `any_of`: proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions. — skills ["AWS", "Redshift"]; satisfied skills []; group satisfied: `False`
- `required_group_3` `all_of`: extensive experience working with databricks. — skills ["Databricks"]; satisfied skills []; group satisfied: `False`
- `required_group_4` `all_of`: strong skills in sql (t\\-sql), python (pyspark/pandas), dax, power query (m), pl/sql. — skills ["SQL", "Python", "Spark"]; satisfied skills ["SQL", "Python"]; group satisfied: `False`
- `required_group_5` `any_of`: experience with databases: sql server, oracle, postgresql, azure sql, teradata. — skills ["SQL", "PostgreSQL", "SQL Server", "Azure"]; satisfied skills ["SQL", "PostgreSQL", "SQL Server", "Azure"]; group satisfied: `True`
- `required_group_6` `all_of`: skilled in power bi, git, visual studio code, ssms. — skills ["Power BI"]; satisfied skills []; group satisfied: `False`

### preferred
- `preferred_group_7` `all_of`: aws and databricks certifications. — skills ["Databricks", "AWS"]; satisfied skills []; group satisfied: `False`
- `preferred_group_8` `all_of`: designing and implementing scalable data architectures in aws and databricks. — skills ["Databricks", "AWS"]; satisfied skills []; group satisfied: `False`


Required gaps: {"atomic_skills": ["AWS", "Databricks", "Spark", "Power BI"], "capability_concepts": ["aws", "spark"], "requirement_groups": [{"candidate_satisfied_skills": [], "group_id": "required_group_1", "satisfied": false, "section": "required", "skills": ["AWS"], "source": "7–10 years of implementation experience in cloud data architecture, with at least 5 years in aws environments.", "source_span": "7–10 years of implementation experience in cloud data architecture, with at least 5 years in aws environments.", "type": "all_of"}, {"candidate_satisfied_skills": [], "group_id": "required_group_2", "satisfied": false, "section": "required", "skills": ["AWS", "Redshift"], "source": "proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions.", "source_span": "proficiency in aws services: glue, redshift, athena, lake formation, sagemaker, bedrock, step functions.", "type": "any_of"}, {"candidate_satisfied_skills": [], "group_id": "required_group_3", "satisfied": false, "section": "required", "skills": ["Databricks"], "source": "extensive experience working with databricks.", "source_span": "extensive experience working with databricks.", "type": "all_of"}, {"candidate_satisfied_skills": ["SQL", "Python"], "group_id": "required_group_4", "satisfied": false, "section": "required", "skills": ["SQL", "Python", "Spark"], "source": "strong skills in sql (t\\\\-sql), python (pyspark/pandas), dax, power query (m), pl/sql.", "source_span": "strong skills in sql (t\\\\-sql), python (pyspark/pandas), dax, power query (m), pl/sql.", "type": "all_of"}, {"candidate_satisfied_skills": ["SQL", "PostgreSQL", "SQL Server", "Azure"], "group_id": "required_group_5", "satisfied": true, "section": "required", "skills": ["SQL", "PostgreSQL", "SQL Server", "Azure"], "source": "experience with databases: sql server, oracle, postgresql, azure sql, teradata.", "source_span": "experience with databases: sql server, oracle, postgresql, azure sql, teradata.", "type": "any_of"}, {"candidate_satisfied_skills": [], "group_id": "required_group_6", "satisfied": false, "section": "required", "skills": ["Power BI"], "source": "skilled in power bi, git, visual studio code, ssms.", "source_span": "skilled in power bi, git, visual studio code, ssms.", "type": "all_of"}]}

Preferred gaps: {"atomic_skills": [], "capability_concepts": [], "requirement_groups": [{"candidate_satisfied_skills": [], "group_id": "preferred_group_7", "satisfied": false, "section": "preferred", "skills": ["Databricks", "AWS"], "source": "aws and databricks certifications.", "source_span": "aws and databricks certifications.", "type": "all_of"}, {"candidate_satisfied_skills": [], "group_id": "preferred_group_8", "satisfied": false, "section": "preferred", "skills": ["Databricks", "AWS"], "source": "designing and implementing scalable data architectures in aws and databricks.", "source_span": "designing and implementing scalable data architectures in aws and databricks.", "type": "all_of"}]}

Seniority: {"terms": ["lead"], "years_required": 10}

## Derived flags and lane eligibility

Final flags: {"backend_ok": false, "bridge_ok": false, "data_identity": false, "data_ok": true, "ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_role_concentration": false, "ecosystem_specialized": false, "integration_data_ok": true, "transferable_data_strong": false}

Resolution: {"eligible": ["wrong_lane", "target_lane", "secondary_lane"], "fallback_lane": "wrong_lane", "fallback_used": false, "tie_order": ["target_lane", "secondary_lane", "bridge_lane", "survival_lane", "wrong_lane"], "tied_winners": ["target_lane"], "winner": "target_lane"}

Raw scores: {"bridge_lane": 19.0, "secondary_lane": 15.0, "survival_lane": 0.0, "target_lane": 62.0, "wrong_lane": 0.0}

Final scores: {"bridge_lane": 0, "secondary_lane": 15.0, "survival_lane": 0, "target_lane": 62.0, "wrong_lane": 0.0}

## Applied actions and surviving effects

Survival describes the written field, not every downstream consequence. Bounded fit contributions are not counterfactual marginal effects.

- `data_evidence`: {"field": "data_ok", "op": "set", "value": true}
  - Inputs: {"hits.core_data_signals": 3, "hits.support_signals": 4}
  - Before: false; after: true
  - Effect: retained; overridden by: None; bounded by: None
- `database_development_evidence`: {"field": "data_ok", "op": "set", "value": true}
  - Inputs: {"hits.database_development": 1, "hits.database_usage": 3, "hits.integration_data": 2}
  - Before: true; after: true
  - Effect: no_effect; overridden by: None; bounded by: None
- `database_and_data_stack_evidence`: {"field": "data_ok", "op": "set", "value": true}
  - Inputs: {"hits.data_stack_usage": 3, "hits.database_usage": 3, "hits.support_signals": 4}
  - Before: true; after: true
  - Effect: no_effect; overridden by: None; bounded by: None
- `integration_data_evidence`: {"field": "integration_data_ok", "op": "set", "value": true}
  - Inputs: {"hits.database_development": 1, "hits.database_usage": 3, "hits.integration_data": 2}
  - Before: false; after: true
  - Effect: retained; overridden by: None; bounded by: None
- `target_eligibility`: {"field": "eligible", "op": "append", "value": "target_lane"}
  - Inputs: {"data_identity": false, "data_ok": true, "hits.bridge_title_terms": 0, "hits.consultant_title_terms": 0, "hits.data_title_identity": 2, "hits.non_target_title_terms": 0, "hits.strong_target_title_terms": 1}
  - Before: ["wrong_lane"]; after: ["wrong_lane", "target_lane"]
  - Effect: retained; overridden by: None; bounded by: None
- `secondary_eligibility`: {"field": "eligible", "op": "append", "value": "secondary_lane"}
  - Inputs: {"backend_ok": false, "data_ok": true, "hits.platform_heavy_terms": 0}
  - Before: ["wrong_lane", "target_lane"]; after: ["wrong_lane", "target_lane", "secondary_lane"]
  - Effect: retained; overridden by: None; bounded by: None
- `overlevel_penalty`: {"field": "fit_score", "op": "subtract_score", "value": 8}
  - Inputs: {"years_required": 10}
  - Before: 64.5; after: 56.5
  - Effect: retained; overridden by: None; bounded by: None
- `lead_review_gate`: {"field": "review_flags", "op": "append", "value": "lead_responsibility"}
  - Inputs: {"is_lead_like": true}
  - Before: []; after: ["lead_responsibility"]
  - Effect: retained; overridden by: None; bounded by: None
- `overlevel_review_gate`: {"field": "review_flags", "op": "append", "value": "overlevel_experience"}
  - Inputs: {"years_required": 10}
  - Before: ["lead_responsibility"]; after: ["lead_responsibility", "overlevel_experience"]
  - Effect: retained; overridden by: None; bounded by: None
- `many_required_gaps`: {"field": "review_flags", "op": "append", "value": "multiple_required_gaps"}
  - Inputs: {"missing_required_atomic": ["AWS", "Databricks", "Spark", "Power BI"]}
  - Before: ["lead_responsibility", "overlevel_experience"]; after: ["lead_responsibility", "overlevel_experience", "multiple_required_gaps"]
  - Effect: retained; overridden by: None; bounded by: None
- `possible_fit_score`: {"field": "fit_quality", "op": "set", "value": "possible_fit"}
  - Inputs: {"fit_score": 56.5}
  - Before: null; after: "possible_fit"
  - Effect: retained; overridden by: None; bounded by: None
- `configured_review_gate`: {"field": "apply_decision", "op": "set", "value": "manual_review"}
  - Inputs: {"review_flags": ["lead_responsibility", "overlevel_experience", "multiple_required_gaps"]}
  - Before: null; after: "manual_review"
  - Effect: retained; overridden by: None; bounded by: None

## Fit and decision

- `fit_profile_coverage`: contribution +88.5; {"aws": {"profile_strength": 0.0, "weight": 0.5}, "azure": {"profile_strength": 0.8, "weight": 2.0}, "data_quality": {"profile_strength": 1.0, "weight": 4.0}, "etl": {"profile_strength": 1.0, "weight": 6.0}, "git": {"profile_strength": 0.8, "weight": 1.0}, "integration_workflows": {"profile_strength": 1.0, "weight": 4.0}, "operations": {"profile_strength": 1.0, "weight": 1.0}, "python": {"profile_strength": 0.8, "weight": 3.0}, "spark": {"profile_strength": 0, "weight": 1}, "sql": {"profile_strength": 1.0, "weight": 5.0}, "systems": {"profile_strength": 1.25, "weight": 1.5}, "testing": {"profile_strength": 0.25, "weight": 1.0}}
- `fit_base`: contribution +0; ""
- `fit_missing_required_atomic`: contribution -3; "AWS"
- `fit_missing_required_atomic`: contribution -3; "Databricks"
- `fit_missing_required_atomic`: contribution -3; "Spark"
- `fit_missing_required_atomic`: contribution -3; "Power BI"
- `fit_is_lead_like`: contribution -12; ""
- `overlevel_penalty`: contribution -8; ""
- `lead_review_gate`: contribution +0; ""
- `overlevel_review_gate`: contribution +0; ""
- `many_required_gaps`: contribution +0; ""
- `fit_lane_cap_and_bounds`: contribution +0; ""

Fit: 56.5; quality: possible_fit; apply: manual_review.

Blockers: []

Review flags: ["lead_responsibility", "overlevel_experience", "multiple_required_gaps"]

Owners: {"final_ai_review_rule": "ai_review_gate", "final_apply_decision_rule": "configured_review_gate", "final_fit_modifiers": [{"bounded_by": null, "changed": true, "event_index": 29, "field": "fit_score", "final_effect": "retained", "overridden_by": null, "rule_id": "overlevel_penalty"}], "final_lane_resolver": "maximum score among eligible lanes; canonical lane order breaks ties", "final_lane_rule": "target_eligibility", "lane_overridden_contributors": [], "lane_supporting_contributors": ["strong_target_title_terms", "core_data_signals", "database_development", "data_stack_usage", "target_eligibility", "secondary_eligibility"]}

## Learning

Score: 38.33; status: eligible.

[{"adjacent_concepts": {"etl": 1.0, "python": 0.8}, "contribution": 3.453, "novelty": 1, "prevalence_pct": 3.7, "priority": 0.8, "skill": "Databricks"}, {"adjacent_concepts": {"etl": 1.0, "python": 0.8}, "contribution": 4.387, "novelty": 1, "prevalence_pct": 4.7, "priority": 0.8, "skill": "Spark"}, {"adjacent_concepts": {"etl": 1.0, "python": 0.8}, "contribution": 29.295, "novelty": 1, "prevalence_pct": 27.9, "priority": 0.9, "skill": "AWS"}, {"adjacent_concepts": {"etl": 1.0, "sql": 1.0}, "contribution": 1.19, "novelty": 1, "prevalence_pct": 1.7, "priority": 0.6, "skill": "Redshift"}]

## Confidence and AI review

Confidence: 0.815 (heuristic, not probability); AI review: False.

{"contradictions": [], "heuristic_not_probability": true, "margin": 0.758, "requirement_ambiguity": false, "signal_count": 14, "weak_description": false}

Configuration: {"ambiguity_penalty": 0.15, "base": 0.3, "close_margin": 0.15, "contradiction_penalty": 0.22, "hard_exclusion_confidence": 0.97, "margin_weight": 0.35, "review_below": 0.65, "review_on_contradictions": true, "review_on_requirement_ambiguity": true, "signal_saturation": 5, "signal_weight": 0.25, "suppress_review_on_hard_exclusion": true, "weak_description_penalty": 0.2, "weak_description_words": 12}

Review reasons: []

## Full policy evaluation history

Unmatched/inactive/stopped rules are recorded by the same evaluator; stopped rules were not evaluated.

- `override:data_evidence`: fired; inputs {"hits.core_data_signals": 3, "hits.support_signals": 4}
- `override:database_development_evidence`: fired; inputs {"hits.database_development": 1, "hits.database_usage": 3, "hits.integration_data": 2}
- `override:database_and_data_stack_evidence`: fired; inputs {"hits.data_stack_usage": 3, "hits.database_usage": 3, "hits.support_signals": 4}
- `override:backend_evidence`: not_matched; inputs {"hits.backend_data_signals": 1}
- `override:bridge_evidence`: not_matched; inputs {"hits.bridge_positive_signals": 3, "hits.support_signals": 4}
- `override:transferable_data_identity`: not_matched; inputs {"hits.analytics_terms": 1, "hits.core_data_signals": 3, "hits.platform_heavy_terms": 0, "hits.support_signals": 4}
- `override:integration_data_evidence`: fired; inputs {"hits.database_development": 1, "hits.database_usage": 3, "hits.integration_data": 2}
- `override:transferable_data_counterweight`: not_matched; inputs {"hits.transferable_data": 7}
- `override:ecosystem_specialization_evidence`: not_matched; inputs {"hits.ecosystem_specialization": 0, "hits.ecosystem_terms": 0, "hits.ecosystem_title": 0}
- `override:ecosystem_ownership_evidence`: not_matched; inputs {"hits.ecosystem_ownership": 0, "hits.ecosystem_terms": 0, "hits.ecosystem_title": 0}
- `override:ecosystem_admin_evidence`: not_matched; inputs {"hits.ecosystem_admin_title": 0, "hits.ecosystem_administration": 0, "hits.ecosystem_terms": 0, "hits.ecosystem_title": 0, "transferable_data_strong": false}
- `override:ecosystem_concentration_evidence`: not_matched; inputs {"ecosystem_admin_identity": false, "ecosystem_ownership_gate": false, "ecosystem_specialized": false, "hits.ecosystem_specialization": 0, "hits.ecosystem_title": 0, "transferable_data_strong": false}
- `override:target_eligibility`: fired; inputs {"data_identity": false, "data_ok": true, "hits.bridge_title_terms": 0, "hits.consultant_title_terms": 0, "hits.data_title_identity": 2, "hits.non_target_title_terms": 0, "hits.strong_target_title_terms": 1}
- `override:supported_integration_target`: not_matched; inputs {"hits.integration_title_identity": 0, "integration_data_ok": true}
- `override:secondary_eligibility`: fired; inputs {"backend_ok": false, "data_ok": true, "hits.platform_heavy_terms": 0}
- `override:bridge_title_guard`: not_matched; inputs {"data_identity": false, "hits.bridge_title_terms": 0}
- `override:bridge_eligibility`: not_matched; inputs {"bridge_ok": false, "hits.bridge_title_terms": 0, "hits.consultant_title_terms": 0, "hits.platform_heavy_terms": 0, "hits.secondary_title_terms": 0, "hits.strong_target_title_terms": 1, "search_lane": ""}
- `override:survival_context`: not_matched; inputs {"backend_ok": false, "bridge_ok": false, "data_ok": true, "hits.non_target_title_terms": 0, "hits.platform_heavy_terms": 0, "search_lane": ""}
- `override:target_title_weak_data_content`: not_matched; inputs {"data_ok": true, "hits.strong_target_title_terms": 1}
- `override:target_secondary_title_conflict`: not_matched; inputs {"hits.secondary_title_terms": 0, "hits.strong_target_title_terms": 1}
- `override:positive_and_exclusion_signals`: not_matched; inputs {"backend_ok": false, "data_ok": true, "hits.wrong_desc_terms": 0}
- `override:target_title_platform_ownership`: not_matched; inputs {"hits.platform_heavy_terms": 0, "hits.strong_target_title_terms": 1}
- `override:analytics_identity_guard`: not_matched; inputs {"hits.analytics_title_terms": 0}
- `override:analytics_bridge`: not_matched; inputs {"bridge_ok": false, "hits.analytics_title_terms": 0, "hits.platform_heavy_terms": 0}
- `override:consultant_identity`: not_matched; inputs {"hits.consultant_title_terms": 0}
- `override:consultant_bridge_exception`: not_matched; inputs {"hits.bad_consultant_title_terms": 0, "hits.bridge_positive_signals": 3, "hits.consultant_title_terms": 0, "hits.core_data_signals": 3, "hits.platform_heavy_terms": 0, "hits.support_signals": 4, "hits.wrong_desc_terms": 0}
- `override:admin_ownership_guard`: not_matched; inputs {"bridge_ok": false, "hits.core_data_signals": 3, "hits.platform_admin_title_terms": 0}
- `override:description_exclusion_guard`: not_matched; inputs {"backend_ok": false, "data_ok": true, "hits.wrong_desc_terms": 0}
- `override:low_signal_guard`: not_matched; inputs {"hits.low_signal_terms": 0, "hits.strong_target_title_terms": 1}
- `override:generic_software_guard`: not_matched; inputs {"hits.non_target_title_terms": 0, "hits.strong_target_title_terms": 1}
- `override:support_identity_guard`: not_matched; inputs {"hits.support_title_identity": 0}
- `override:support_secondary_guard`: not_matched; inputs {"hits.support_title_identity": 0}
- `override:support_bridge`: not_matched; inputs {"bridge_ok": false, "hits.support_title_identity": 0}
- `override:integration_requires_data_domain`: not_matched; inputs {"hits.integration_title_identity": 0, "integration_data_ok": true}
- `override:security_domain_identity_guard`: not_matched; inputs {"hits.security_title_identity": 0}
- `override:integration_hardware_domain_guard`: not_matched; inputs {"hits.hardware_responsibilities": 0, "hits.integration_title_identity": 0}
- `override:ecosystem_identity_guard`: not_matched; inputs {"ecosystem_role_concentration": false}
- `override:ecosystem_low_transfer_admin_guard`: not_matched; inputs {"ecosystem_admin_identity": false, "transferable_data_strong": false}
- `override:ecosystem_low_transfer_specialist_guard`: not_matched; inputs {"ecosystem_role_concentration": false, "hits.ecosystem_specialization": 0, "hits.transferable_data": 7}
- `override:platform_ownership_guard`: not_matched; inputs {"hits.infrastructure_title_identity": 0, "hits.platform_heavy_terms": 0}
- `override:hard_exclusion_override`: not_matched; inputs {"hard_exclusions": []}
- `fit:overlevel_penalty`: fired; inputs {"years_required": 10}
- `fit:ecosystem_usage_penalty`: not_matched; inputs {"hits.ecosystem_terms": 0}
- `fit:ecosystem_specific_experience`: not_matched; inputs {"hits.ecosystem_ownership": 0, "hits.ecosystem_title": 0, "years_required": 10}
- `fit:ecosystem_transferable_specialist_fit`: not_matched; inputs {"flags.ecosystem_ownership_gate": false, "flags.ecosystem_specialized": false, "flags.transferable_data_strong": false}
- `fit:ecosystem_limited_transfer_fit`: not_matched; inputs {"flags.ecosystem_ownership_gate": false, "flags.ecosystem_specialized": false, "flags.transferable_data_strong": false}
- `fit:ecosystem_admin_fit_gate`: not_matched; inputs {"flags.ecosystem_admin_identity": false}
- `fit:ecosystem_dependence`: not_matched; inputs {"flags.ecosystem_ownership_gate": false}
- `fit:required_core_gate`: not_matched; inputs {"has_hard_requirement_blockers": false}
- `fit:lead_review_gate`: fired; inputs {"is_lead_like": true}
- `fit:overlevel_review_gate`: fired; inputs {"years_required": 10}
- `fit:many_required_gaps`: fired; inputs {"missing_required_atomic": ["AWS", "Databricks", "Spark", "Power BI"]}
- `fit:wrong_role_gate`: not_matched; inputs {"role_lane": "target_lane"}
- `quality:good_fit_score`: not_matched; inputs {"fit_score": 56.5}
- `quality:possible_fit_score`: fired; inputs {"fit_score": 56.5}
- `quality:weak_fit_score`: not_evaluated; inputs {}; stopped by `possible_fit_score`
- `apply:configured_hard_blocker`: not_matched; inputs {"blockers": []}
- `apply:insufficient_fit`: not_matched; inputs {"fit_score": 56.5}
- `apply:configured_review_gate`: fired; inputs {"review_flags": ["lead_responsibility", "overlevel_experience", "multiple_required_gaps"]}
- `apply:ambiguous_role_review`: not_evaluated; inputs {}; stopped by `configured_review_gate`
- `apply:fallback_search_context`: not_evaluated; inputs {}; stopped by `configured_review_gate`
- `apply:strong_primary_fit`: not_evaluated; inputs {}; stopped by `configured_review_gate`
- `apply:adjacent_or_moderate_fit`: not_evaluated; inputs {}; stopped by `configured_review_gate`
