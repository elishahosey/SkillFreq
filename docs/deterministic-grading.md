# Deterministic grading consolidation

SkillFreq was refactored in place. The atomic market taxonomy, scraper/import paths,
profile model, weighted alignment, conservative application decisions and market
semantic views remain the foundation. No AI provider, embeddings, ORM or generic
rules engine was introduced.

## Architecture found before implementation

The CSV and scraped-link branches of `pipeline.py` repeated the same sequence:
broad skill counts → requirement flags → weighted alignment → threshold label →
fit quality/apply bucket → categorical lane → CSV. Lane classification used ordered
early returns and substring lists; the decision layer scanned overlapping lists
again. `roles.yml` was a separate resume-routing vocabulary. `resume_signal.yml`
independently described resume evidence.

Atomic market extraction was already separate and well bounded: controlled aliases,
validation against ambiguous owners, canonical labels, evidence, mention counts and
a taxonomy hash. PostgreSQL already had canonical taxonomy, extraction runs,
normalized job skills and prevalence views. The repository schema also defines the
extraction scope needed for a correct denominator.

The live schema inspection found existing `skill_scores` history, `raw_jobs`, and
calibration tables. A new independent grading-history table would duplicate these.
The inspected installation had not yet applied the repository's `job_skill_scope`
evolution; its `skill_scores.id` was also a plain bigint without an insert default.

## Vocabulary ownership and configuration decisions

| Source | Decision | Responsibility |
|---|---|---|
| `market_skills.yml` | Keep YAML → existing PostgreSQL taxonomy refresh | Atomic labels and aliases; unchanged taxonomy |
| `skills.yml` | Keep YAML; archive with grade configuration | Capability phrases and explicit atomic-to-capability relations |
| `roles.yml` | Keep direct YAML authoring/loading; archive immutable DB snapshots | Role phrase registry, reusable term groups, lane rules, exclusions and resume routing |
| `profile.yml` | Keep existing YAML profile; archive exact grading input | Capability strengths; optional atomic overrides and intentional growth paths |
| `weights.yml` | Keep YAML; archive exact version | Existing weights/penalties, alignment adjustments/caps, thresholds, fit, learning and confidence parameters |
| `resume_signal.yml` | Keep domain metadata, replace duplicate alias definitions with references | Supplemental resume evidence; never a second atomic taxonomy |
| `requirements.yml` | Centralize extracted configuration in YAML | Section headings, blocker groups, seniority cues and ambiguity patterns |

For one developer, editable files plus immutable PostgreSQL snapshots are simpler
than relational rule editing and synchronization. SQL can query the snapshot JSON;
runtime DB rule edits are deliberately not another authoring path. PostgreSQL owns
persistent results, extraction scope, prevalence and history. Python owns evaluation.

Representative ownership mappings (the larger pre-migration inventory is in
[vocabulary-inventory.md](vocabulary-inventory.md)):

| Existing term | Previous locations | Owner after consolidation |
|---|---|---|
| data engineer | roles.yml, lane classifier, decision layer | Role/title vocabulary in roles.yml, referenced by consumers |
| airflow | skills.yml, market_skills.yml, resume router tie-break | Atomic Airflow; capability relation retains broader orchestration phrases |
| postgresql / postgres | market_skills.yml, skills.yml, roles.yml, decision layer, resume_signal.yml | Atomic PostgreSQL, referenced by SQL/Python-related capability or role evidence |
| SQL / stored procedures | skills.yml, roles.yml, lane/decision lists, resume_signal.yml | SQL aliases belong to atomic SQL; stored procedures remain a capability phrase |
| data integration / ETL | skills.yml, roles.yml, lane/decision/alignment lists | Capability phrase owner; role and scoring groups reference it |
| staff / principal / lead | skills.yml, roles.yml, extract.py, decision layer | Seniority configuration; separate from capability output |
| platform/cloud terms | market_skills.yml, skills.yml, roles.yml, lane/decision lists | Atomic technology references plus explicit role/exclusion meaning |
| configuration consultant | roles.yml, lane and decision lists | Role/exclusion vocabulary |

`skills.yml` entries now have `terms`, `atomic_skills` and `term_refs`. A PostgreSQL
hit can trigger the broad `sql` concept. It does **not** create an atomic SQL fact
by normalization, and does not imply that the candidate knows PostgreSQL.
Capability IDs such as `airflow`, `python` and `data_platforms` retain their old
broader scoring meaning for compatibility; the typed relation makes that explicit.

Role references use `atomic`, `concept_term`, `seniority` or `role_term`. A role
group is a selection of evidence with a particular purpose, not another alias owner.
Some evidence intentionally contributes to more than one role or capability.

## Evaluation and explanations

Both ingestion paths call `build_job_result()` and `grade_job()`:

1. Normalize scalar inputs and preserve description section boundaries.
2. Run the existing atomic extractor independently of broad capability matching.
3. Extract required/preferred sections, missing capabilities, years and seniority.
4. Match configured role rules and accumulate lane points.
5. Apply explicit role/content eligibility guards and hard exclusions.
6. Calculate fit, learning, heuristic confidence and the AI-review gate.
7. Preserve raw alignment, threshold labels and the existing fit/apply policy.
8. Export the expanded `JobResult`; optionally append an audited database grade.

Lane rules carry an ID, category, signal type, term-group or regex pattern, lane,
weight, title/description/both scope, active flag, hard-exclusion flag and hit cap.
Python retains explicit controls for generic software, weak target titles,
consultants, analysts, platform/admin dominance and search context. Inactive rules
generate no evidence. Hard exclusions override positive overlap. `search_lane`
can inform bridge/survival interpretation but never establishes the final lane.

`raw_lane_scores` contains accumulated signal points. `lane_scores` contains the
scores after eligibility penalties/context overrides. Each adjustment is recorded.
Scores are heuristic points and need not sum to 100. Matching multiple aliases can
retain overlapping mention counts, as in the existing market extractor; these are
not unique linguistic spans. Category caps bound lane contribution inflation.

`triggered_rules` contains matched terms, scopes, lane weights, penalties,
overrides, a raw alignment point ledger, a fit point ledger, and named fit/apply
decisions. Growth evidence records prevalence, adjacency, novelty and points.
Confidence evidence records the margin, signal count, contradictions, ambiguity
and weak-description adjustment. Explanations come from these records, not an LLM.

The legacy `score` remains raw alignment on its historical scale. The old
`required_total` name still means detected scoring channels, not explicit mandatory
requirements. Typed missing-required/preferred fields are the accurate requirement
outputs. `pre_ai_score` is explicitly an alias for fit, not an undocumented blend.

## Fit, learning, confidence and AI

Fit is weighted coverage of relevant current capabilities, bounded at 0–100,
minus explicit required/preferred atomic gaps and blocker/lead penalties, with a
lane-dependent maximum. Profile strengths above one remain available to legacy
alignment; fit coverage caps strength at one. Broad competence never grants every
technology in that concept. `atomic_skills` in the same profile explicitly owns
atomic proficiency. See [career policy](career-policy.md) for the calibration's
configured eligibility, fit and decision rules.

Learning uses only the existing `public.skill_prevalence` view. Python does not
recalculate prevalence or introduce another prevalence table. A skill earns points
only when it is missing/weak, the lane is target or secondary, an explicit growth
path exists, adjacent profile experience exists, and prevalence is positive.
The formula multiplies configured points by prevalence saturation, path priority,
adjacency strength and novelty, then caps the total. Required Airflow may therefore
reduce fit and increase learning. Missing Terraform does not automatically earn
points without an eligible configured path. Missing/obsolete market data produces
`learning_score: null` and `learning_status: unavailable`, with a visible diagnostic.

Growth paths for Airflow, AWS, Snowflake, Spark and PostgreSQL were seeded as an
editable assumption based on the requested data/backend direction. No new
technology was asserted as known. Review these priorities in `profile.yml`.

Confidence is an explainable heuristic, **not a statistically calibrated probability**.
Close scores, weak content, contradictions and ambiguous requirements can trigger
`should_request_ai_review()`. Strong hard exclusions and clear deterministic
matches do not require AI. The function only requests adjudication; no provider is
called. Existing manual/AI calibration imports remain supported. If review is
needed, an otherwise `apply_now` result is capped at `manual_review`.

## Database and versioning

[grading.sql](../db/grading.sql) evolves **existing `skill_scores`** with job identity,
grading/taxonomy versions, lane scores, fit, learning, confidence, the AI gate and
structured evidence. `job_grade_history` is a view over that history, not a second
table. `grading_config_versions` stores immutable configuration snapshots and
implementation hashes. No descriptions are duplicated. Job keys reuse `make_job_key()`.

The migration also adds an identity default to `skill_scores.id` only on installations
where neither an identity nor an insert default exists; existing IDs are preserved.
It is rerunnable. Persistence appends grades in a transaction. Existing CSV batch
imports recognize `grade_json` and its adjacent `.grading.yml` snapshot. Legacy
exports still import through the existing fields. Explicit batch replacement keeps
its historical semantics; ordinary persistence appends.

The grading hash covers effective authoring inputs, taxonomy version and evaluator
implementation hashes. Profile changes therefore change the grading version.
Atomic aliases and market taxonomy hashing are unchanged. Each market-backed grade
records extraction run IDs, scope size, read time and the prevalence values used.
Keep the Git revision/code available as well as the configuration snapshot to rerun
an old implementation; hashes identify code but do not archive its source.

The grading migration and direct/batch inserts were tested in rollback-only
transactions. `--persist-grades` applies the grading migration when first used.
The calibration pass deployed an optimized definition of the existing
`skill_prevalence` view: it reads extraction scope and canonical job-skill rows
directly. No new tables or taxonomy were added. The existing populated scope now
supplies live learning data; dashboard slices retain their separate semantic view.

## Use and validation

```powershell
# An existing job CSV; preserves the old output columns and adds grade_json.
python -m skillfreq.cli grade-csv --input jobs.csv --out data/outputs/grades.csv --offline-grading

# Use existing PostgreSQL prevalence and append a versioned grade history.
python -m skillfreq.cli grade-csv --input jobs.csv --out data/outputs/grades.csv --persist-grades

# Existing market refresh; choose its normal scope flags deliberately.
python -m skillfreq.cli refresh-job-skills

python -m unittest discover -s tests -v
$env:SKILLFREQ_TEST_DB='1'
python -m unittest discover -s tests -p test_grading_postgres.py -v
python scripts/compare_grading.py
```

`run` retains its existing JobSpy/date-based import and URL scraping behavior,
and accepts `--offline-grading` and `--persist-grades`. Free-form spaCy extraction
is now opt-in with `--nlp-diagnostics`; noun phrases never update the taxonomy.
`grade-csv` provides a direct path for an explicitly chosen CSV without scraping.

See [grading-comparison.md](grading-comparison.md) for all representative fixtures,
[grading-examples.yml](grading-examples.yml) for complete machine-readable examples,
and [grading-historical-sample.md](grading-historical-sample.md) for a 100-job
historical comparison. The comparison script loads the trusted baseline classifier
from Git commit `766f50c`; no obsolete classifier remains in application code.

The tests cover atomic alias normalization/ambiguity, concept relationships,
inactive rules, hard exclusions, search context, lane fixtures, close margins,
requirement ambiguity, repeated sections, profile/version changes, aligned learning,
prevalence reuse, JSON/CSV output, both pipeline branches, optional NLP, and
PostgreSQL schema/history/configuration round trips.

Validation completed with 33 passing tests, including the optional PostgreSQL test,
plus CLI smoke runs with offline and unavailable-market paths. The 14 fixtures
retain 12 original lanes and all original apply decisions. Thirteen raw alignment
scores are unchanged; the Spark-aware learning fixture changes as described below.
The 100-job historical sample retains 76 lanes, changes 24 lanes and changes 17
apply decisions; both versions produce one `apply_now`. This is a behavior comparison,
not a labeled accuracy evaluation. The original repository's one-job import sample
also retains its secondary lane and skip decision.

## Intentional retained behavior and manual inspection

Raw alignment still uses historical mention-sensitive penalties, overlapping
substring boosts and both accumulated AI dampeners. It remains separate from the
new normalized fit score. Application buckets remain conservative and use the
existing policy, even where a new fit score is high. Consultant exceptions, bridge
and survival search caps, required/preferred distinctions and year parsing remain.

Review the platform hit threshold: it is still a conservative technology/phrase
density heuristic, not proof of infrastructure ownership. The new scored policy
can downgrade target-sounding jobs that the old early target return promoted.
Review mixed analyst/support jobs, expanded atomic-alias relationships, the chosen
growth paths, and threshold settings using the saved historical comparison.
Literal matching does not fully resolve negation, alternative requirements or
ownership semantics; ambiguous/clipped descriptions should receive manual/AI review.

The fixture changes are deliberate: generic software/data overlap becomes secondary
instead of bridge; mixed Data Engineer/Backend Engineer evidence provisionally selects
secondary and requests adjudication. Spark now has an explicit capability relation,
fixing the previous blocker group referencing a capability absent from `skills.yml`.
That changes alignment for the learning fixture without changing its apply bucket.

## Changed components

| Area | Files |
|---|---|
| Shared configuration and matching | `skillfreq/configuration.py`, `skills/text.py`, `skills/dictionary.py`, `skills/match.py`, `skills/job_market.py` |
| Grading | `score/grading.py`, `score/lane_classifier.py`, `score/decision_layer.py`, `score/similarity.py`, `score/thresholds.py`, `skills/extract.py` |
| Integration | `pipeline.py`, `cli.py`, `resume_router.py`, `skills/resume_profile/extract.py`, `io/grading_to_postgres.py`, `io/excel_to_postgres.py` |
| Authoring | `configs/skills.yml`, `roles.yml`, `requirements.yml`, `profile.yml`, `weights.yml`, `resume_signal.yml` |
| Database | `db/grading.sql`; existing market SQL/taxonomy untouched |
| Validation and reports | `tests/test_grading.py`, `tests/test_grading_postgres.py`, `tests/test_job_market_skills.py`, `tests/fixtures/lane_jobs.yml`, comparison/migration scripts and these docs |

Large lane, decision and alignment vocabulary lists were removed from Python.
Section headings, seniority and blocker groups moved to requirements configuration;
alignment caps/points and label thresholds moved to weights. Small algorithmic
branches remain ordinary Python. The supplemental NLP stop-phrase filters remain
with their diagnostic code because they do not determine canonical skills or grades.
## Requirement evidence

Requirement extraction is deterministic and section-aware. Each sentence in a
required or preferred section is retained as a requirement group with its source
text and one of `all_of`, `any_of`, `equivalent`, or `ambiguous` grammar. Comma lists introduced
as examples (for example, “cloud platforms such as AWS, Azure, or GCP”) are kept
as alternatives rather than independent missing technologies. Candidate
satisfaction is recorded on the group, so an Azure match can satisfy an any-of
cloud group without reporting AWS and GCP as separate gaps. Unsatisfied required
alternatives produce one group gap and one configured fit penalty. All-of gaps
retain individual penalties. Mixed AND/OR grammar requests review without a
mandatory penalty. Legacy flags consume these same semantics; only unstructured
sentences use mention-based fallback.

Use `trace-job` to inspect these groups and their source sentences for one job.
See [requirement semantics](requirement-semantics.md) for configuration and limits.
