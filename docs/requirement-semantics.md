# Requirement groups and scoring

Policy belongs in configuration. Mechanism belongs in Python.

The extractor resolves candidate satisfaction once. Atomic gaps, capability flags,
fit, alignment, blocker checks and review evidence use that interpretation.
Lane rules, ecosystem rules and score thresholds are unchanged by this fix.

| Grammar | Missing evidence | Fit treatment | Legacy required flags |
|---|---|---|---|
| `all_of` | Each unknown atomic skill | Existing per-atomic penalty, deduplicated across sentences | Missing capability evidence remains eligible for existing blocker/alignment policy |
| `any_of`, satisfied | None | Zero | Options are not independently missing |
| `any_of`, unsatisfied | One explicit group gap | One configured group penalty | No individual-option penalties or automatic hard blocker |
| `equivalent` | Group gap unless a named skill or configured equivalent is known | Same required-group penalty | No mandatory penalty for the named product alone |
| `ambiguous` | Source, operands and review flag | No atomic/group penalty | Sentence excluded from mandatory fallback |
| Unstructured sentence | Existing capability mentions | Existing behavior | Mention fallback, explicitly recorded |

`missing_required_skills` and `missing_preferred_skills` retain their existing
`atomic_skills`, `capability_concepts` and `requirement_groups`, and add
`unsatisfied_groups` and `ambiguous_groups`. Groups retain source section, source
sentence, grammar, candidate matches and equivalent evidence. `satisfied: null`
means unresolved grammar, not a satisfied or definitely missing requirement.

`requirement_flags` exposes the reconciled legacy flags, per-skill source evidence
and interpretation routing. Existing JSON export and PostgreSQL JSONB persistence
carry these fields without a database migration. The cohort replay writes a new
CSV and snapshot; it does not append production DB grades.

## Configure penalties and equivalence

In `configs/weights.yml`:

```yaml
fit:
  required_atomic_penalty: 3
  required_group_penalty: 3
```

The initial group charge equals one existing atomic charge. This is a new unit
of missing evidence, not a new apply threshold. Each unsatisfied required group
gets one `fit_unsatisfied_required_group` ledger event with its ID, options,
source and contribution. Normal score bounds still apply, so a -3 contribution
may not change the final bounded score. `all_of` never gets this group charge.
Preferred group gaps are observable but retain zero group penalty.

In `configs/requirements.yml`, `equivalences: {}` deliberately starts empty.
To allow an equivalent, add a canonical skill key with `atomic_skills` and/or
`capability_concepts` lists referencing the existing controlled vocabularies.
Only do so after confirming that those skills/capabilities really qualify.

For example, **only if the candidate's ETL experience includes acceptable
orchestration experience**, an explicit authoring choice could be:

```yaml
equivalences:
  Airflow:
    capability_concepts: [etl]
```

This example is not enabled by default. Broad ETL does not automatically imply
Airflow proficiency. The existing `known_atomic_threshold` also applies to
explicit equivalent evidence. Unknown references or malformed equivalences fail
configuration loading; group penalties must be numeric and between 0 and 100.
Equivalence is one-hop evidence lookup, not recursive inference.

## Routing and conservative grammar

Required/preferred section context is retained. Inline “preferred” overrides a
required section for that sentence; “Power BI preferred” is not a heading that
discards Power BI. Explicit headless requirement snippets are recognized by
`unscoped_requirement_patterns` and retain `source_section: unknown`.

The parser distinguishes conjunctions/enumerations, OR/one-of lists, explicit
example cues and “or equivalent”. A colon alone is not evidence for OR. When AND
and OR connect atomic operands in the same sentence, the parser records
`ambiguous` rather than inventing a Boolean tree. `and/or` is treated as a single
alternative connector. A verb phrase before the operands (such as “design and
develop with AWS or Azure”) does not create a mixed-grammar flag.

For requirement operands, the longest controlled alias owns its span: SQL Server
does not create an additional generic SQL alternative. Market-skill extraction
and the taxonomy remain unchanged.

Only structured `all_of` evidence and sentences without a safely extracted atomic
group reach the legacy missing-capability scan. Known atomic mentions are masked
in the all-of legacy text so they cannot become missing merely because a broad
concept profile differs. Independent non-atomic requirements, such as ETL, still
use the fallback. A separate “AWS required” sentence remains mandatory even if
another sentence says “AWS or Azure”.

Unsatisfied alternatives are not automatically hard or modern-stack blockers.
Existing all-of/fallback blocker rules remain. Mixed grammar feeds the existing
requirement-ambiguity confidence/AI-review gate; it does not call an AI provider.
Existing hard-exclusion suppression of AI review is preserved.

## Trace and replay

Trace output separates individual gaps and group gaps, shows candidate matches
and explicit equivalents, and reads group contributions from the real fit ledger.
See the [commands](commands.md) for an isolated replay with frozen prevalence and
the [impact report](generated/requirement-semantics.md) for this cohort.

The comparison verifies ordered job identity, description and search context,
ignores atomic-list ordering, saves every changed job's before/after source groups
and ledgers, and fails on lane/learning drift or unattributed changes. Attribution
categories overlap; they are evidence-based explanations, not separate
counterfactual measurements of each change.

## Remaining limits

- Slash lists such as `PySpark/Pandas`, negation and nested clauses remain limited.
- OR referring to a degree or unrelated clause can still make a long sentence
  ambiguous or look like an alternative. Inspect the source before trusting it.
- A multi-line “one of the following” header is not a general Boolean scope parser.
- Explicit examples are represented as one capability-like choice; no arbitrary
  equivalent capability is inferred when all named examples are unknown.
- Candidate satisfaction covers the controlled taxonomy, not every English noun
  or every product in a sentence. Unknown technologies are not invented.
- Repeated separately extracted alternative sentences remain separate groups.
- Broad capability proficiency and atomic proficiency remain distinct. The
  legacy capability layer still uses its existing positive-proficiency rule;
  atomic satisfaction uses the configured threshold.

## Files in this semantic fix

- `skillfreq/skills/extract.py`: group resolution, mixed grammar, sentence routing,
  provenance and reconciliation of legacy flags.
- `skillfreq/score/grading.py`: group gap projection, configurable penalty and
  persisted requirement flags; validation of equivalent references.
- `skillfreq/score/trace.py`: actual group effects and interpretation routing.
- `skillfreq/configuration.py`, `configs/weights.yml`, `configs/requirements.yml`:
  penalty validation, explicit equivalent configuration and headless grammar.
- `scripts/regrade_saved_cohort.py`, `scripts/compare_requirements.py`: frozen
  prevalence replay and attributable, order-insensitive comparisons.
- `tests/test_requirements.py`, `tests/test_requirement_comparison.py`: semantic,
  fallback, trace, validation and comparison-integrity tests.
- This guide, `commands.md`, `career-policy.md`, `deterministic-grading.md` and
  generated audit reports.

## Verified frozen-cohort result

Grading version `5b4f855d2cdf0292` → `3678ae1f5835169c`; taxonomy unchanged.
All 8,692 ordered inputs match. Lane changes: **0**. Learning-score changes: **0**.
Role policy, profile, taxonomy and all prior weights/thresholds match their saved
configuration; only the new group penalty was added to scoring settings.

| Changed field | Jobs |
|---|---:|
| Required atomic gaps | 442 |
| Preferred atomic gaps | 331 |
| Explicit required group gaps | 615 |
| Explicit preferred group gaps | 403 |
| Fit score | 287 |
| Fit quality | 52 |
| Apply decision | 22 |
| AI-review flag | 66 |
| Legacy alignment score | 1,004 |

There are 1,635 changed rows including newly exposed group-gap evidence. Changes
overlap; these counts are not additive. The inline-preferred heading correction
also changes experience/section-based alignment evidence in 190 rows. The report
records those source lines and before/after events explicitly. For example,
“MBA is preferred” previously made a later required eight-year experience line
disappear into the preferred section. No experience thresholds were changed.

Apply-now/manual-review/skip counts move from 105/2,273/6,314 to
103/2,269/6,320. Average fit moves from 31.352950 to 31.295492. AI-review requests
move from 3,248 to 3,314; no provider is invoked. All 886 nonzero learning scores
remain unchanged.

Validation: **95 tests run, 93 passed, 2 optional PostgreSQL tests skipped**.
The report contains 30 representative cases, a source-level Lead Analyst audit,
and full before/after attribution for every changed row in its JSON companion.
