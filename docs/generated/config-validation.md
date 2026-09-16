# SkillFreq configuration validation

Status: **passed**

Schema validation is performed while loading the existing configuration. Unknown fields/operators/actions, invalid lanes, duplicate IDs, malformed patterns and invalid references fail the load.

Static quality findings (warnings/info):

- {"classification": "unclear", "groups": ["ecosystem.products", "ecosystem.title"], "kind": "equivalent_term_groups", "severity": "info"}
- {"explanation": "The DB grading view does not provide search_lane; policy is structurally reachable when that context is supplied.", "field": "search_lane", "input_context": "db", "kind": "input_contract_unavailable", "lane": "survival_lane", "rules": ["bridge_eligibility", "survival_context"], "severity": "info"}
