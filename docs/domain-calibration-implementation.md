# Focused domain calibration implementation

Policy belongs in configuration. Mechanism belongs in Python.

This pass builds on the already calibrated implementation. It does not replace
the policy engine or repeat the earlier architecture refactor. The previous
`results-db-90-days-calibrated.csv` and its configuration snapshot are the baseline.

## Changes in this pass

| File | Change |
|---|---|
| `configs/profile.yml` | Candidate-confirmed SQL Server 1.0 and PostgreSQL 0.7, with provenance notes; SQL 1.0, Python/Azure 0.8 retained |
| `configs/skills.yml` | Reusable SQL development terms: PL/SQL spellings, database development, schema design/development |
| `configs/roles.yml` | Generic integration title demotion; data-supported integration promotion; database-development and data-stack evidence; security/hardware domain guards; ecosystem ownership eligibility guard |
| `tests/fixtures/domain_calibration_jobs.yml` | Seventeen domain regression jobs, including all nine requested cases |
| `tests/test_domain_calibration.py` | Fixture assertions, real configured atomic proficiency, configuration-only ecosystem eligibility change, seven invalid configuration cases |
| `scripts/compare_domain_calibration.py` | Same-cohort comparison with 10 integration, 10 ecosystem and 10 database examples, atomic gap counts and aggregate metrics |
| `docs/career-policy.md` | Instructions for changing each new policy and confirmed atomic skills |
| `docs/commands.md` | Separate export and same-cohort comparison commands |
| `README.md` | Link to focused comparison |
| `docs/domain-calibration-comparison.md` and `.json` | Measured results and evidence from the completed DB run |

The existing mechanisms already express the required policy. No grading Python,
policy evaluator, SQL schema, atomic taxonomy or prevalence calculation changed.
The previous snapshot's grading implementation hashes match the current modules.
The changed configuration produces a new grading version while preserving the
market taxonomy version. The output's `.grading.yml` is the auditable profile and
policy snapshot. Historical database grades are not overwritten.

## Rules and semantics

- `integration_title_identity` contributes eight SECONDARY points, but existing
  data/backend eligibility still applies. A bare title is not enough to establish
  TARGET or a confident relevant lane.
- `integration_data_evidence` requires a substantive data anchor plus SQL/database
  evidence or a second data anchor. `supported_integration_target` adds TARGET
  eligibility and 24 points; `integration_requires_data_domain` guards promotion.
- `security_domain_identity_guard` and the expanded hardware title pattern protect
  role identity from incidental SQL. `integration_hardware_domain_guard` requires
  an integration title and at least two hardware responsibility terms.
- `ecosystem_identity_guard` removes TARGET when both vendor title and ownership
  evidence exist. Other eligible lane scores decide the result. Mere tool use
  remains distinct from ownership and still uses the existing fit policy.
- `database_development_evidence` handles SQL development without requiring modern
  pipeline terminology. `database_and_data_stack_evidence` recognizes database
  usage plus a controlled data technology and supporting signals. Neither treats
  modern tools as infrastructure ownership.

The Oracle posting was inspected in full: it asks for Oracle SQL and **PLSQL
development**, Informatica PowerCenter ETL, production support and mentoring.
The unrecognized PLSQL spelling was a reusable capability gap. It now becomes
TARGET, with manual review preserved for its other evidence.

Reviewing all 34 Integration Engineer postings caught an intermediate policy
mistake: unconditional SECONDARY eligibility promoted unrelated aircraft and
semiconductor work. That fallback was removed before the final run. The final
policy preserves relevant SQL/ETL integration and rejects unrelated physical
engineering identity through reusable evidence.

The representative review also found a SAP Cloud ALM role explicitly describing
itself as the platform owner. Adding the generic phrases `platform owner`,
`platform roadmap` and `platform-ownership` closes that ownership wording gap
through the same existing ecosystem guard and fit blocker. No SAP title exception
was added.

## Verification

The standard suite passes all 55 non-DB tests (57 discovered, two opt-in DB tests).
Both opt-in PostgreSQL tests also pass: audit round-trip and market scope/count
semantics. Their transactions roll back. The new domain fixture test exercises
17 jobs, and the configuration validation test exercises seven invalid inputs.
The report generator was smoke-tested against the baseline, then run against the
final export. It rejects differing source identities or job text.

The final report includes all requested lane/decision/learning/AI counts, lane
decision distributions, integration TARGET retention, ecosystem eligibility
changes, independent database skill gaps and 30 representative postings.

## Remaining judgment calls

Security engineering is currently WRONG policy. Hardware title patterns use simple
co-occurrence and may need adjustment for compound titles. Ecosystem ownership
phrases can appear in mixed responsibilities; inspect their matched evidence.
PLM/CAD integration and vendor data models are configured ownership signals, not
new market skills. Short descriptions and unusual seniority wording remain
heuristic inputs. Nothing in this pass claims calibrated confidence probabilities.
The report explicitly flags a Boomi role requiring 3–5+ product-specific years,
a mixed Python/React role, a senior strategy analyst and a German-location
integration role for manual inspection; their policy tradeoffs are not hidden.

Known PostgreSQL no longer receives missing-skill learning credit. This can lower
learning totals without breaking market retrieval. Search context remains optional
because the DB view does not supply it. See the measured comparison for exact
versions, market provenance and unresolved representative examples.
