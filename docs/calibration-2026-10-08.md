# Reviewed-cohort calibration: 2026-10-08

This iteration stays on `refactor/pre-ai-grading-engine`, starting at
`fd73dee3598e38c41d1430666f77c445c5d885ca`. It improves deterministic extraction,
visibility and eligibility in the existing architecture. No taxonomy change,
AI integration, database write, global score reduction or title blacklist was added.

## Evidence and classification before implementation

The retained workbook `data/outputs/calibration_review_2026-09-25.xlsx` contains
exactly 85 reviews: 39 Good, 15 Neutral, 31 Bad. Its comparisons reference the
`results-db-90-days-requirements` and `results-db-90-days-requirement-semantics`
exports and matching snapshots. All 85 identities exist in both exports.

| Class | Finding and action |
|---|---|
| Implementation bugs | Repeated Markdown escaping prevented years extraction. Broad years scans accepted employer history (200). `seniority_signals` read `lead_terms`. Inline modality only recognized preferred. Fixed these mechanisms. |
| Representation | The review table removed unsatisfied/ambiguous groups. Preserve compact type/options summaries, leaving full sources in the existing expander. |
| Intended behavior | Alternatives satisfied by a known option do not create missing atomics. Unsatisfied alternatives already incur one configured group penalty. Preserve this model. |
| Policy/configuration | Strengthen secondary technical identity, configure clearance evidence and candidate-relative seniority. Candidate confirmed 3–4 industry years; use 4 for gap calculations. |
| Regressions | Compact extraction, group visibility, years, seniority, clearance, unfamiliar-role, Good-case and cohort-integrity checks. |
| No justified change | Keep taxonomy, all_of/any_of/equivalent/ambiguous, group penalty magnitude, fit bands, apply thresholds, market formulas and architectural boundaries. |

The inspection covered the current grader, policy/configuration, extraction,
review UI, replay/comparison scripts and the prior calibration, reproduction,
requirement-semantics, requirement-testing and grading-example documentation.

## Historical interpretation and reconstruction limits

Historical OLD grading version: `5b4f855d2cdf0292`.
Human-reviewed baseline version: `3678ae1f5835169c`.
Final grading version: `5e01f710d103c4c0`.
Taxonomy before and after: `31d08964f877`.

The starting Git implementation's parsed configuration matches the baseline
snapshot, but seven implementation hashes differ even allowing LF/CRLF conversion:
`score/decision_layer.py`, `score/grading.py`, `score/lane_classifier.py`,
`score/similarity.py`, `skills/extract.py`, `skills/job_market.py`, `skills/match.py`.
An isolated Git archive of the starting commit was therefore run against the same
85 retained rows and frozen market context. Its version is `28e7925e66fcc565`
(Git archive file bytes); all 85 lanes, fit scores, decisions, requirement gaps,
seniority signals and learning scores match the human-reviewed baseline.
This demonstrates behavioral parity for the checked cohort, not full historical
source reconstruction or equality of every hidden metadata field.

The final run reuses exact reviewed membership, exported title/description/source
and search fields, and saved per-job market context. The comparison rejects changed
input fields, extra/missing/duplicate identities, review-version mismatch and
market-context drift. Original DB inputs were not independently archived/proven
lossless, so this is a **re-evaluation**, not an exact historical replay.

## Changes

- Optional wording is configurable: preferred, a plus, nice-to-have, bonus,
  desired/desirable, optional and good to have. It works inside required sections,
  headless prose and responsibilities. Sentence/semicolon/bullet/“but” boundaries
  prevent preference from swallowing subsequent independent requirements.
- Years parsing consumes repeated escapes, numeric ranges/dashes and parenthetical
  numerals. It requires local experience context, excludes preferred wording and
  sections, retains evidence, and surfaces invalid ranges/values above 50. A range
  uses its minimum requirement; among independent requirements the strongest
  minimum is retained. The Product Manager 200-year anomaly becomes 7.
- Title evidence explicitly distinguishes Senior/Sr, Lead, Staff, Principal,
  Manager, Architect, Director and VP. Senior alone triggers review, not a blocker.
  Description seniority and lead-like evidence remain separate.
- The existing eight-point overlevel penalty/review now uses a gap of at least
  three years from the profile upper bound (still seven required years for this
  candidate). After structural reruns, a gap of at least five years adds another
  eight points of penalty. A gap of at least six years plus lead-or-higher title
  or ownership evidence is blocker-capable. These are explicit tuning choices,
  not learned probabilities or claims of measured optimality.
- Secondary eligibility still needs the prior data/backend evidence plus a
  recognized technical title, database development, software-work evidence,
  integration with database/data-stack evidence, or backend plus database usage.
  Generic data, systems, API and validation alone cannot rescue an unknown title.
  Existing integration-title evidence and real software-development duties protect
  unfamiliar but relevant roles.
- Candidate `active_clearance: false` reflects the retained review note. Required
  current active possession blocks; ability-to-obtain and unspecified eligibility
  go to review. Preferred/negated clearance does not block. An incidental active
  clearance mention outside requirement context is only review evidence.
- Re-evaluation refuses existing output basenames, selects reviewed identities,
  freezes available or unavailable market context, and writes provenance and a
  source patch alongside complete `grade_json` and the matching snapshot.

## Calibration comparison

| Measure | Reviewed baseline | Final |
|---|---:|---:|
| Apply now | 6 | 1 |
| Manual review | 69 | 49 |
| Skip | 10 | 35 |
| Bad: apply now | 5 | 0 |
| Bad: manual review | 26 | 18 |
| Bad: skip | 0 | 13 |
| Target lane | 31 | 31 |
| Secondary lane | 53 | 42 |
| Bridge lane | 1 | 1 |
| Wrong lane | 0 | 11 |
| Good fit band | 13 | 8 |
| Possible fit band | 62 | 48 |
| Weak fit band | 10 | 29 |

There are 34 decision changes: 26 manual-review → skip, two apply-now → skip,
three apply-now → manual-review, and three skip → manual-review. All five Bad
apply-now cases leave that bucket. The sole Good apply-now case, Python Data
Engineer `li-4427873184`, remains apply-now at 79.56.

All nine reviewed examples of Relief Valve Engineer/Technical Authority, Fixed
Equipment Specialist, Chief Inspector, Epic Payer Platform Lead and sanctions
Director move out of secondary into wrong lane. Product Manager and Accounts
Payable Analyst account for the other two lane changes. Learning changes only
for Product Manager and Chief Inspector because wrong lane is ineligible; market
values and the learning formula are unchanged.

The 32 historical `too_high` labels remain historical labels: 15 corresponding
scores decrease, 14 are unchanged and three increase. Two Hadoop postings rise
10.5 because cloud experience explicitly “is a plus”; Sr Software Engineer rises
8 because the stated 5–8-year range is correctly treated as a five-year minimum.
These are extraction corrections, not evidence that their new scores are adequate.
The new number of human-judged `too_high` outcomes is **not yet measured**.

Historical score-quality counts remain 36 reasonable, 32 too_high, two unclear,
zero too_low and 15 unanswered. Requirement interpretation remains 33 correct,
23 unclear, 14 incorrect and 15 unanswered until human re-review. Fifteen postings
change required-gap representation and fifteen change preferred-gap representation;
35 acquire previously missing numeric years, and 60 change years values overall.
Eleven still have no safely extracted numeric requirement.

### Requirement-group audit

Twenty-two reviewed jobs have OLD missing atomics but no baseline missing atomics.
Seven still have explicit unsatisfied required groups with existing penalty ledger
entries; the other fifteen retain structured satisfied choices/groups. The JSON
comparison stores their old atomics, baseline groups, satisfaction and penalties.
For example, Principal Data Platform/Backend retains separate unsatisfied choices
for Snowflake/Databricks, Spark/Kafka and Airflow/dbt. No flat-gap restoration or
duplicate alternative penalty was introduced. The review table now shows these
group gaps. This audit does not certify every long English clause as correctly
parsed; nested example lists remain a limitation below.

### Good-case preservation and adverse changes requiring re-review

The first structural candidate incorrectly removed a CVS Software Development
Engineer and two Kforce Senior Developer postings. Positive software-work evidence
repairs those regressions; their final lanes and decisions match the baseline.
The existing Integration Engineer regression also remains secondary.

Among the 39 Good-rated jobs, 28 decisions are unchanged, eight move from review
to skip, and three move from skip to review. The eight stricter decisions are:

- Senior Python/Snowflake: `li-4428785426`, `li-4430133938`, `li-4430716870` (12 years).
- Software Engineer, Lead: `li-4418874694`, `li-4418890226` (10 and 12 years).
- Data Engineer: `li-4429364899` (10 years).
- Principal AI Platform Engineer: `in-3976624db34e9d92` (10 years).
- Lead/Principal Software Engineer: `in-76539d0ffaf6c48e` (10 years).

Their original review notes already call out overlevel requirements or request a
lower score. Nevertheless, these are adverse changes to Good-rated records and
must be re-reviewed, not automatically declared improvements. The three Specialist
postings moving skip → review (`li-3835714098`, `li-4427377748`, `li-4428782487`)
use the five-year minimum of 5–8 years and also need renewed judgment.
The only Good-rated lane change is Accounts Payable Analyst `in-a2232dcbee24f494`;
the review note explicitly says it should not be secondary, and its decision
remains skip. “Good” judges grading, not necessarily suitability to apply.

## Tests and files

Baseline: 111 tests, 109 passed, two optional PostgreSQL tests skipped.
Final: **122 tests, 120 passed, two optional PostgreSQL tests skipped**.
The new file adds eleven tests with parameterized subcases; the 24 requirement
tests also pass independently. PostgreSQL tests were not enabled because this
iteration changes no DB behavior; no production grades were persisted.

| Files | Purpose |
|---|---|
| `configs/profile.yml` | Confirmed experience range and clearance availability |
| `configs/requirements.yml` | Modality, context, levels, ownership and clearance evidence |
| `configs/roles.yml` | Positive technical identity for secondary eligibility |
| `configs/weights.yml` | Candidate-relative review, penalties and blockers |
| `skillfreq/skills/extract.py` | Shared deterministic extraction fixes |
| `skillfreq/score/grading.py`, `skillfreq/configuration.py` | Validated profile fields, facts and persisted evidence |
| `skillfreq/calibration_review.py`, `scripts/review_calibration.py` | Group-gap visibility |
| `scripts/regrade_saved_cohort.py` | Reviewed subset, non-overwrite guard, provenance |
| `scripts/compare_reviewed_calibration.py` | Input integrity and human-label comparison |
| `tests/test_reviewed_calibration.py` | Compact regressions and artifact integrity |
| This report and `docs/generated/reviewed85-2026-10-08-*.md` | Final and intermediate evidence |

## Preserved artifacts and commands

Original exports, both original snapshots and the human workbook were not written.
Their hashes are recorded in run/verification metadata. New artifacts are local
under `data/outputs/`, which is Git-ignored; back up this directory with the code.

The basename `results-reviewed85-2026-10-08-final` has `.csv`, `.grading.yml`,
`.manifest.json` and `.source.patch` companions. The CSV contains complete
`grade_json`; the manifest records Git HEAD, dirty status, dependencies, Python,
source/output hashes and all 85 identities. A separate source archive and
verification JSON preserve actual working file bytes and the final commit link.
`results-reviewed85-2026-10-08-retained-baseline.csv` is an exact selected-row
export with a copy of its matching snapshot. The `starting-commit`, `structural`,
`structural-v2` and `final-candidate` result/snapshot pairs also remain available;
earlier candidates were never overwritten.

`docs/generated/reviewed85-2026-10-08-final.md` lists every posting. Its local JSON
companion contains all before/after evidence, human labels, fit ledgers and the
22 atomic-disappearance audits. Existing older generated reports are untouched.

```powershell
.\.venv-skillfreq\Scripts\python.exe -m unittest discover -s tests
.\.venv-skillfreq\Scripts\python.exe scripts/regrade_saved_cohort.py `
  --input data/outputs/results-db-90-days-requirement-semantics.csv `
  --reviews data/outputs/calibration_review_2026-09-25.xlsx `
  --out data/outputs/results-reviewed85-NEXT.csv --frozen-market
.\.venv-skillfreq\Scripts\python.exe scripts/compare_reviewed_calibration.py `
  --before data/outputs/results-db-90-days-requirement-semantics.csv `
  --historical data/outputs/results-db-90-days-requirements.csv `
  --after data/outputs/results-reviewed85-NEXT.csv `
  --reviews data/outputs/calibration_review_2026-09-25.xlsx `
  --out docs/generated/reviewed85-NEXT.md
```

## Remaining issues and next approximately 25 reviews

Eighteen Bad jobs remain manual-review, including several SRE/GenAI managers,
oncology-specialized engineering and team-lead roles. Some fit scores remain high
(one Senior Data Engineer is 92 with a genuine 3–6-year range). Required content
without recognizable headings, nested examples joined with AND, unrelated OR
clauses, slash lists, unknown products, spelled-out years without numerals and
degree/experience alternatives still need focused evaluation. Clearance levels
are not a full credential hierarchy; `active_clearance: true` assumes the required
clearance is available. Existing broad lead terms can still match incidental prose.

Do not respond by globally reducing scores. Review 25 unique cases next: eight
Good-rated review → skip cases; three Good-rated skip → review cases; four
unchanged Good controls including the surviving apply-now and restored developer;
four remaining Bad manager/domain cases; three unsatisfied/nested/inline-preferred
requirement cases; two unrelated-role exclusions; and one clearance case. Select
distinct IDs, avoid syndicated duplicates where possible, retain new labels in a
new workbook, and judge both false exclusions and excessive permissiveness.
Use that evidence before changing required-group penalties or global thresholds.
