# Changing SkillFreq career policy

**Policy belongs in configuration. Mechanism belongs in Python.**

Edit the YAML files, validate, then rerun grading. No AI call, model training or
Python edit is needed for the changes below. The export's `.grading.yml` records
the complete configuration and grading/taxonomy versions. Existing grades stay
historical; changing configuration does not retroactively update them.

## Ownership and evaluation order

| File | Owns |
|---|---|
| `market_skills.yml` | Controlled atomic technologies and aliases; unchanged in this calibration |
| `skills.yml` | Capability concepts and their atomic references |
| `profile.yml` | Current capability strengths, explicit atomic proficiency and growth paths |
| `roles.yml` | Role vocabulary, term groups, title patterns, evidence weights and lane eligibility policy |
| `requirements.yml` | Required/preferred section patterns, experience and ambiguity cues, blocker groups |
| `weights.yml` | Fit penalties/caps, fit-quality bands, apply decisions, learning values and confidence settings |

The order is extraction → raw lane points → eligibility/ownership guards → lane →
fit penalties and gates → learning and confidence → AI-review flag → fit quality
and apply decision. The old alignment metric remains visible for historical
comparison; it does **not** set fit quality or apply decisions.

Atomic proficiency is never inferred across database products. `sql: 1` does not
grant SQL Server, PostgreSQL or MySQL proficiency. Modern technology mentions are
facts; ownership responsibilities determine whether platform policy applies.

## Change an apply-now threshold

In `weights.yml`, find `decision_rules` → `strong_primary_fit`. Change the
`fit_score` condition's value (currently 78):

```yaml
- id: strong_primary_fit
  priority: 700
  when:
    all:
      - {field: role_lane, op: equals, value: target_lane}
      - {field: fit_score, op: gte, value: 78}
  actions:
    - {op: set, field: apply_decision, value: apply_now}
  stop: true
```

Higher-priority rules first check explicit blockers, low fit, review flags,
ambiguity and fallback search context. One adjacent missing tool is not a gate.
The `many_required_gaps` fit rule currently requests manual review at four missing
required atomic technologies. Preferred gaps only incur their configured penalty.

Unsatisfied required `any_of`/`equivalent` groups are separate from atomic gaps.
Edit `fit.required_group_penalty` to change their one-per-group fit charge.
They do not automatically become hard blockers or independent missing options.
Explicit equivalent evidence belongs in `requirements.yml` → `equivalences`.
See [requirement semantics](requirement-semantics.md) for examples and limits.

`quality_rules` uses numerical bands: good at 80+, possible at 55+, weak below 55.
An explicit hard gate can produce **good_fit + skip**. The grade then exposes the
gate in `blocking_reasons`, `reason_codes` and `triggered_rules`; it does not
silently relabel a 96 as weak fit. Review-only gates appear in `review_flags`.

## Add a lane signal or wrong-role title pattern

Add a unique rule under `roles.yml` → `lane_rules`. Reference an existing term
group, or define a reusable title pattern:

```yaml
- id: example_testing_identity
  category: test_title_identity
  signal_type: title
  title_pattern:
    any: [test, testing]
    with: [engineer, automation, analyst]
  lane: wrong_lane
  weight: 100
  scope: title
  hard_exclusion: true
  active: true
  max_hits: 1
```

This example is already covered by the shipped test-identity rule; edit it rather
than adding a duplicate. `any` and `with` each need at least one boundary-matched
term anywhere in the title. They are not arbitrary noun-phrase classification.
Exactly one of `group`, `pattern` (regex), or `title_pattern` is allowed.
Inactive rules produce no evidence. A hard exclusion invokes the configured
`hard_exclusion_override`; incidental SQL cannot overturn QA identity.

Positive signals accumulate points first. `eligibility_rules` then applies
explicit identity protections using category counts such as
`hits.core_data_signals`. Add a derived Boolean flag to `derived_flags` if needed;
it starts false and can be set by an eligibility rule. All thresholds are in YAML.
Adding a new category exposes its `hits.<category>` count automatically.

## Adjust ecosystem or fit penalties

For the current specialization/concentration policy, see
[ecosystem policy controls](ecosystem-policy.md). This extends the ownership rules
below with transferable evidence and separately recorded data-platform signals.

`roles.yml` → `ecosystem.products`, `ecosystem.ownership`, and `ecosystem.title`
own the controlled ecosystem vocabulary. Presence contributes **zero wrong-lane
points** by itself. `weights.yml` → `fit.rules` currently applies:

- `ecosystem_usage_penalty`: 3 fit points for ecosystem usage.
- `ecosystem_dependence`: 30 points and an explicit gate when ownership evidence
  combines with a vendor-specific title, or multiple ownership cues occur.
- `ecosystem_specific_experience`: 12 points and review when a vendor-specific
  title requests five required years without separately matched ownership cues.

Change the rule's condition, subtraction, or blocker action to change that policy.
For example, replacing an `append` to `blockers` with an `append` to `review_flags`
makes it a review-only gate. SQL/ETL work using Informatica remains transferable;
MDM architecture, survivorship rules and product ownership are different facts.

The main `fit` settings also expose `base_score`, `coverage_scale`, `lane_caps`,
`required_atomic_penalty`, `preferred_atomic_penalty`, `flag_penalties`, and
`known_atomic_threshold`. The current overlevel rule subtracts eight points at
seven required years and requests review. Adjust those values in the rule.
Preferred experience and company-history numbers are not automatically required
years. Experience parsing remains a heuristic; inspect unusual wording.

## Change learning eligibility and priorities

Edit `weights.yml` → `learning.eligible_lanes`, `points_per_growth_skill`,
`prevalence_saturation_pct` and `max_score`. Edit the existing profile's growth paths:

```yaml
growth_paths:
  Airflow:
    adjacent_concepts: [etl, python]
    priority: 1.0
```

Points require an eligible lane, a mentioned weak/missing atomic skill, an
explicit path, nonzero adjacent capability strength, and positive prevalence.
The formula multiplies configured points by capped prevalence/saturation,
priority, strongest adjacency and novelty. Missing irrelevant technologies earn
nothing. A required missing technology can lower fit and still earn learning points.

Prevalence is loaded once per grading run from the existing `skill_prevalence`
view in a consistent read transaction. It counts existing `job_skills` in the
recorded `job_skill_scope`, including jobs with zero matches in the denominator.
It no longer reconstructs every clean job × technology pair for this broad query.
Filtered dashboard analysis still uses `job_skill_prevalence_input`.

The market population can be broader than the 90-day grading cohort. The grade
records population size, extraction run, taxonomy version, read time and the
percentages actually used. Market failures log a diagnostic and produce
`learning_score: null`, `learning_status: unavailable` and an explicit reason.
Successful analysis with no eligible growth evidence produces a real zero.

## Change AI-review confidence policy

Edit `weights.yml` → `confidence.review_below` (currently 0.65) and `close_margin`
(currently 0.15, a relative top-two lane margin). Other settings control base,
signal strength, weak-description and contradiction penalties. Boolean settings
control review on contradictions/requirement ambiguity and hard-exclusion
suppression. Confidence is a heuristic, **not a calibrated probability**.

AI review is a downstream flag; no provider is called. Missing AWS or an adjacent
growth gap alone does not trigger AI. Equivalent degree experience is not itself
a skill ambiguity, while “Airflow or equivalent experience” can be.

## Add candidate atomic proficiency

Edit `profile.yml` → `atomic_skills`, using exact canonical keys:

```yaml
atomic_skills:
  SQL: 1.0
  Python: 0.8
  Azure: 0.8
  SQL Server: 1.0  # Confirmed strong direct experience.
  PostgreSQL: 0.7  # Independent from SQL Server and broad SQL.
  Airflow: 0.2
  AWS: 0.0
```

Values range from 0 to 1. The candidate explicitly confirmed strong SQL Server
experience and intermediate PostgreSQL project experience; these are now 1.0 and
0.7, with provenance in `atomic_skill_notes`. SQL remains 1.0, Python and Azure
remain 0.8. This grants no MySQL experience. The same atomic profile drives
required/preferred gaps and learning novelty, independently of broad SQL fit.

## Calibrate integration, database and ecosystem identity

An Integration Engineer title supplies modest SECONDARY points through
`integration_title_identity`, but still needs data/backend evidence for eligibility.
A bare title stays unresolved (fallback lane with low confidence); it does not establish TARGET. `integration_data_evidence` requires a substantive data anchor from
`identity.integration_data` plus database evidence or a second data anchor.
`supported_integration_target` adds TARGET eligibility and 24 points when that
evidence accompanies an integration/interface engineering title. APIs, validation
and troubleshooting alone do not meet this requirement.

Change the conditions or point action in those rules to adjust promotion.
`integration_requires_data_domain` removes TARGET when the evidence is absent.
The reusable `security_title_identity` and `hardware_title_identity` patterns
protect against unrelated security, flight-control, embedded and hardware roles.
`integration_hardware_domain_guard` also recognizes combinations of hardware
responsibility terms in a generic integration role. These guards run after positive
eligibility, so incidental SQL cannot override role identity. Security engineering is currently a configured WRONG identity;
change `security_domain_identity_guard` if security work becomes a career goal.

`ecosystem_identity_guard` removes TARGET when both ecosystem title evidence and
ownership evidence occur. Edit its two count thresholds to adjust concentration
requirements. It preserves other eligible lanes; their scores choose the result.
An Informatica mention without ownership does not trigger this guard. Ownership
terms include MDM survivorship/match-merge, platform owner/roadmap wording, and
PLM/CAD integration responsibilities;
Windchill is a controlled ecosystem product, not a new canonical market skill.
Fit blockers remain separately owned by `weights.yml` because lane identity and
candidate suitability answer different questions.

`identity.database_development` references SQL capability terms in `skills.yml`,
including PLSQL/PL SQL/PL/SQL, stored procedures, schema work and optimization.
`database_development_evidence` accepts database-development work with SQL or
transformation evidence, even without modern pipeline terminology. A database
developer title is a strong TARGET title. These capability terms are not aliases
that equate Oracle, PostgreSQL or SQL Server in the atomic market taxonomy.

`database_and_data_stack_evidence` recognizes SQL/database usage plus a controlled
data-stack technology and supporting signals. Modern data tools supply positive
evidence; platform ownership remains a separate responsibility rule.

All these changes use the existing rule operators and actions. Unknown identity
categories (`hits.*`) and term groups fail validation, as do malformed title
patterns, duplicate rule IDs and invalid operators, actions or lanes.

Run a fresh DB export without overwriting the previous calibration:

```powershell
python -m skillfreq.cli grade-db --since-days 90 --out data/outputs/results-db-90-days-domain.csv
python scripts/compare_domain_calibration.py
```

See [the domain comparison](domain-calibration-comparison.md) for the measured
cohort and 10 examples each of integration, ecosystem and database roles.

## Optional search context

The DB view currently lacks `search_lane` and `review_priority`. Both are optional.
`input_context` records whether each was available. Without them, title and
description still determine role identity; no survival/bridge origin is assumed.
CSV rows that supply the context still use the configured fallback policy.

## Rule vocabulary and validation

Conditions are `field`, `op`, `value`, optionally combined with bounded `all`/`any`
lists (maximum six levels). Operators: `equals`, `not_equals`, `in`, `not_in`,
`gte`, `lte`, `gt`, `lt`, `contains`, `contains_any`, `contains_all`, `count_gte`,
`count_lte`, `empty`, `not_empty`, `exists`, `not_exists`. Empty/existence operators
use `value: true`.

Actions are `op`, `field`, `value`: `set`, `add_score`, `subtract_score`,
`cap_score`, `floor_score`, `append`, `remove`. Each stage has a small allowlist of
writable fields. Rules run by descending priority; `stop: true` ends that stage.
One rule cannot give conflicting actions to the same field. Quality and decision
stages require an unconditional final outcome. No imports, expressions, executable
YAML or third-party rules engine are supported.

Unknown operators/actions/fields, invalid lanes, duplicate IDs, missing/circular
term groups, malformed title patterns, invalid ranges and invalid thresholds fail
when the grading context loads. Validate without touching the DB:

```powershell
python -c "from skillfreq.score.grading import GradingContext; print(GradingContext.load().grading_version)"
python -m unittest discover -s tests -v
```

Then write a separate export and compare:

In the current VS Code workspace, choose **Grade DB Jobs - Calibrated 90 Days**.
The task configuration is local (`.vscode` is ignored by Git); these commands work
in any checkout:

```powershell
python -m skillfreq.cli grade-db --since-days 90 --out data/outputs/results-db-90-days-calibrated.csv
python scripts/compare_calibration.py
```

See [the measured comparison](calibration-comparison.md) for counts, representative
posting changes, learning evidence and remaining manual checks.
The [implementation notes](calibration-implementation.md) list changed components,
the database migration, retained behavior and assumptions.
