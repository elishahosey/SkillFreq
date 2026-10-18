# Focused deterministic calibration, 2026-10-18

Branch: `refactor/pre-ai-grading-engine`. Starting commit:
`204488c38ab2afcd052e8d3ff13e363337da720a`. Starting grading version:
`434d61fbf4dfe7b9`. Final grading version: `f5a6db2023ed3e15`.
Final taxonomy version: `d61671304446`. The completion message identifies the
final Git commit containing this report and the implementation.

This iteration changes deterministic requirement representation, experience-gap
policy, and two bounded sources of positive role evidence. Global quality and
application thresholds, general required-skill penalties, lane caps, profile
strengths, hard occupation exclusions, and WRONG weights are unchanged.

## Evidence and root causes, established before editing

The retained workbook is
`data/outputs/comparison-boomi-specialization-2026-10-10/calibration_review_2026-10-10.xlsx`,
sheet `Reviews`, rows 2–26. It exactly matches the supplied counts: 14 Good,
5 Neutral, 6 Bad; 17 reasonable, 6 too high, 2 too low; 17 correct, 4 incorrect,
4 unclear. Its NEW grading version matches the starting checkout. Source job
descriptions and grades come from the adjacent `new.csv`. Historical workbook,
OLD/NEW exports, snapshots, and comparison artifacts were read, not overwritten.

| Representative case | Classification | Root cause |
|---|---|---|
| Senior Software Engineer, Backend (`li-4464115321`) | Extraction/representation | `What We Look For` was not a qualification heading. AWS/MySQL/Kubernetes requirements never reached the structured parser. Python/Kotlin is an actual alternative, not two missing mandates. |
| Adobe AJO Architect (`in-47c6f7305590d7b1`) | Vocabulary/representation and years-parsing bug | No AJO/AEP atomic vocabulary. Sentence-wide `including`/`or` could obscure mandatory named products. The five-year domain clause had no nearby experience token, so only three years was exposed. The vendor was absent from existing ecosystem-product references. |
| NOVOS Support Engineer (`li-4456996188`) | Extraction bug and capability vocabulary | Bare `Qualifications` was unrecognized. `Preferred experience ...` was treated as a section heading, leaking preference to later bullets. Networking architecture and firewall administration had no capability concepts. |
| Junior Java Developer (`in-09ab93a10bfe3e1b`) | Vocabulary/representation; partial intended semantics | Controlled atomics omitted the Java/web/test stack; the examples reduced to known generic SQL. Azure DevOps reduced to known Azure. The capability before a tool-example list disappeared. CI/CD and its tools actually occur under Preferred and stay there. `2 or more years` was also missed. |
| Eight-year Manager – Global Data Management and Analyst, Senior Systems | Seniority policy | Eight years and a four-year gap were already correct. The fixed eight-point penalty was weak and often hidden above the BRIDGE cap. Manager title and team ownership did not block until a six-year gap. |
| Seven-year Principal Data & Analytics Engineer | Seniority policy | Seven years, principal rank, and a three-year gap were detected. The score remained 57.8/manual_review because ownership and experience did not combine strongly enough. |
| Five-year architect/specialist and Senior Data Engineer | Parsing/policy, with moderate growth preserved | A one-year gap is modest relative to the confirmed 3–4-year range. Add a small penalty/review, not a blanket senior/architect rejection. Adobe's vendor mismatch supplies the additional consequence through existing ecosystem policy. |
| Data Engineer II, Data Products (`in-0956df6b9b35d51d`) | Lane taxonomy and scoped requirement grammar | Streaming/replication/data-contract work was absent from core-data evidence; a Python-local alternative made the entire Kafka/SQL/cloud requirement ambiguous. |
| Engineer I-Software Development (`li-4474550134`) | Lane eligibility/taxonomy | Software work was recognized, but this title form and programming work could not independently qualify SECONDARY without data/backend evidence. No exclusion actually fired. |
| ETL Engineer lakehouse posting, two sources | Requirement semantics | `PySpark experience a strong plus` did not match preferred modality. It is now preferred; healthy TARGET/apply_now survives. |
| Healthcare supply-chain consultant | Domain representation and section-boundary bug | Healthcare supply-chain experience had no concept. Generic `requirements` inside prose reset a Preferred section, making federal-health experience look mandatory. Federal health is preferred in the posting. |

## Requirement changes and regression risks

| Missed text or mechanism | Representation/fix | Risk and protection |
|---|---|---|
| `What We Look For`, `Who You Are`, bare `Qualifications`, education/experience headings | Qualification headings in requirements config; normalize escaped Markdown before parsing | A heading may contain broad prose. Headings are bounded; duties and explicit section terminators remain separate. Ordinary prose containing `requirements` no longer changes section. |
| `Preferred experience with Linux ... AWS` followed by `Proficiency in SQL, Linux, Python` | Inline preference stays clause-local; explicit `Preferred: ...` still starts a section | Avoid preference leaking across bullets while preserving inline heading syntax. Both directions have fixtures. |
| `AWS, MySQL and Kubernetes`; `Python or Kotlin` | Atomic all_of plus satisfied any_of | Missing heading repair must not turn all languages into mandates. Alternative satisfaction is tested. |
| `3+ years ... Adobe Journey Optimizer`; `2+ years ... Adobe Experience Platform` | AJO, AEP and AJO Decisioning atomics; product-before-elaboration clauses remain mandatory; product aliases reuse existing ecosystem policy | Acronyms are controlled exact tokens and can still be ambiguous outside context. No job/company/title exception or new vendor penalty. Decisioning remains preferred in the reviewed source. |
| `networking architecture and firewall administration is a must` | Separate capability concepts, not invented atomic products | These concepts have zero fit weight: representation improves without silently altering general alignment. They do not automatically become hard blockers. NOVOS remains manual review. |
| Java, CSS, HTML, XSLT, JavaScript, JUnit, Oracle SQL; Spring framework | Controlled atomics; Oracle SQL belongs to Oracle Database rather than generic SQL; Spring is an independent mandatory gap | `such as` still uses the established any_of example model. This heterogeneous list is visibly unsatisfied, not seven asserted hard mandates. Individual example proficiency remains unresolved. |
| `CI/CD ... tools such as Git, Azure DevOps, Ansible` | Retain independent CI/CD capability prefix, keep tool alternatives in preferred groups; Azure DevOps is distinct from Azure | Broad Azure skill must not satisfy Azure DevOps. Existing explicit atomic-profile policy remains: broad Java/Git strength is not silently copied into atomic proficiency. Profile reconciliation may be useful separately. |
| `multi-threaded environments`; preferred memory management / RAID / SCSI | Concurrent-programming, memory-management and storage capability concepts | Preserve required/preferred section context; do not invent specific storage-product mastery. Zero general fit weight. |
| `healthcare supply chain ... or medical/surgical purchasing`; preferred federal health | Domain concepts in capability evidence | The domain requirement is visible but no universal industry hard filter is invented. Full Boolean satisfaction for non-atomic domain alternatives remains a limitation. |
| `Kafka, ... Python (or similar), SQL, ... (AWS/GCP/Azure)` | Separate only explicit parenthesized alternatives from outer conjuncts; Kafka all_of, Python equivalent, SQL all_of, cloud any_of | Unparenthesized mixed `and`/`or` stays ambiguous. Plain slash notation outside a parenthesized list is not globally reinterpreted. Unknown alternative text remains conservative. |
| `a strong plus`; `2 or more years`; `5+ years in ...` | Preferred phrase coverage; years syntax and required-section context | Preferred years and company-history numbers remain excluded. Required-section domain-years fallback is bounded. |
| URLs ending in `.html` | Mask URL targets for atomic requirement and market matching, preserving character offsets | New HTML vocabulary exposed this false positive in an old Boomi fixture. Explicit HTML prose still matches. |

The controlled vocabulary adds 18 atomic entries and eight capability concepts.
No confidence in a requirement gap should be inferred from an empty
`atomic_skills` list alone: inspect unsatisfied groups, ambiguous groups,
capability concepts, and source evidence. The all_of, any_of, equivalent and
ambiguous structures are retained. No new LLM grading is used.

## Experience policy

Experience gap remains `max(0, required minimum - candidate upper bound)`.
The candidate range remains `[3, 4]`; ranges use their minimum requirement.
Rules are configuration-owned and retain per-rule evidence.

| Gap above upper bound | Cumulative experience-only deduction | Additional policy |
|---|---:|---|
| 0 or unknown | 0 | Existing title/ownership review still applies |
| 1 year | 3 | Growth-gap review; no experience blocker |
| 2 years | 8 | Reviewable moderate-growth opportunity |
| 3 years | 16 | If title rank ≥3 or ownership evidence exists: cap at 54 and explicit seniority/experience blocker |
| 4+ years | 24 | Cap at 54 regardless of title; ownership/rank blocker also applies when present |

The 54 ceilings are specific to material experience mismatch. They avoid the
old situation where a deduction above a lane cap had no visible effect, and
work with the unchanged skip-below-55 decision rule. Senior alone is rank 1,
not an automatic skip. Principal/manager/architect alone also do not trigger
the gap blocker without the required years gap. Existing lead-like penalties
are unchanged. Tests check monotonic scores from four through ten required
years for ordinary, senior and principal titles, plus a stronger candidate
profile and ownership without a senior title.

## Exact false-WRONG audit

**Data Engineer II:** raw TARGET 30 (data-engineer title), SECONDARY 6 (Docker),
BRIDGE 12 (SQL/Python/incident support and bridge signals), WRONG 8 (`cloud
infrastructure`). Core-data hits were zero; backend hits were one. Thus
`data_ok` and `backend_ok` were false, TARGET and SECONDARY failed eligibility,
and bridge evidence did not meet its threshold. No hard exclusion or platform
ownership override fired. Four streaming/replication/data-contract phrases
now feed the existing core-data group. The existing TARGET gate admits the
posting; platform and hard-exclusion guards retain precedence. Outcome:
TARGET / 80.73 / manual_review, with Kafka missing and a one-year experience
gap. Infrastructure duties still warrant human attention.

**Engineer I:** raw TARGET 0, SECONDARY 0, BRIDGE 2 (Python), WRONG 0.
`software components` supplied one recognized software-work hit at zero
weight. No title/description exclusion fired; `no_supported_lane` supplied
the fallback WRONG score of eight. SECONDARY required data/backend evidence
that this programming role lacks. A compositional software-development
title signal plus at least two independent programming-work phrases now
admits SECONDARY. A bare title with incidental Python/APIs still fails.
QA/test/hardware/infrastructure exclusions still run afterward. Outcome:
SECONDARY / 62.92 / manual_review, with C++/Bash/Linux and concurrency gaps.
This remains adjacent C++ storage-test software, not a claimed data-engineering
match; the QA-heavy scope should be considered in human review.

## Validation and retained-cohort comparison

- Full suite: `python -m unittest discover -s tests -v` — 153 tests run,
  151 passed, two optional PostgreSQL integration tests skipped, no failures.
  The sandbox run encountered Windows `os.replace` permission errors in
  existing workbook tests; the complete run outside the sandbox passed.
- Focused parser/vocabulary/legacy checks: 46 passed after the URL regression
  fix. The final complete suite includes all 13 new focused tests.
- `git diff --check`: passed.
- No database refresh, database write, or optional PostgreSQL integration test
  was performed. Logs are retained in `data/outputs/review25-validation-tests.log`.

The compact fixture file contains eight representative excerpts, with
parameterized moderate/severe experience tests and adversarial wrong-role
tests. It does not retain all 25 jobs as fixtures. Existing calibration,
domain, ecosystem, market spot-check and wrong-role fixtures remain active.
Three old assertions were adjusted only for intentional policy/vocabulary
effects: a ten-year requirement, a nine-year principal, and newly recognized
required JavaScript in the Boomi comparison. The Boomi specialization delta
remains exactly eight points and its lane/decision protections remain intact.

The exact 25 reviewed identities were regraded to a fresh basename:
`data/outputs/reviewed25-2026-10-18-validated.csv`, with adjacent `.grading.yml`,
`.manifest.json`, and `.source.patch` provenance. Detailed comparison:
`data/outputs/reviewed25-2026-10-18-validated-comparison.json`.
The replay is a re-evaluation of retained exported inputs, not a claim of
lossless reconstruction of original scraped inputs. Identity, title,
description, search context, market metadata and all previously stored
prevalence values were checked. Newly recognized technologies have null
prevalence; no refreshed market values were invented for the expanded taxonomy.
Source hashes match the replay manifest. Human labels remain historical and
must not be relabeled automatically from score movement.

- Too-high scores: five lower, one unchanged (healthcare consultant).
- Too-low scores: both higher, with the two supported lane rescues.
- All 10 Good-rated WRONG/skip jobs remain WRONG/skip at 15. The Neutral-rated
  AI intern also remains WRONG/skip.
- None of the 14 Good-rated jobs changes lane or application decision.
- TARGET/SECONDARY/BRIDGE/WRONG counts: 3/3/6/13 → 4/4/6/11.
- Apply-now/manual-review/skip counts: 2/10/13 → 2/8/15. Two former skips become
  reviewable; four large-gap/vendor cases become skips. More skips is not used
  as the success metric.

## Remaining limits and threshold recommendation

Keep global thresholds unchanged. This small, selected cohort does not show
that global retuning is warranted. Backend remains 84.89 and Junior Java
82.03 despite substantially better evidence. Existing three-point penalties
and example-list semantics may still understate breadth of missing stack
experience. Treat this as a targeted follow-up recommendation requiring
human re-review, not justification for a global offset.

NOVOS and healthcare remain 65/manual_review: their missing capability/domain
requirements are now visible but are not automatic atomic penalties or hard
filters. Further domain gating needs explicit candidate domain evidence and
policy. The technology vocabulary remains bounded (for example, not every
Adobe subproduct or SAP-specific management tool was added). Unknown alternatives
and heterogeneous example lists remain conservative. The atomic profile still
does not assert Java/Git proficiency from broad concept strengths. Market
prevalence for new atomics needs a separate extraction refresh if desired.

## Files changed

- `configs/requirements.yml`: headings, modality and years-context vocabulary.
- `configs/market_skills.yml`: controlled technology aliases.
- `configs/skills.yml`: requirement capability/domain concepts.
- `configs/weights.yml`: zero general weights for new evidence-only concepts;
  graduated experience penalties and experience-specific ceilings/blocker.
- `configs/roles.yml`: streaming/data-contract evidence, bounded software
  title/work eligibility, and Adobe product references in existing ecosystem policy.
- `skillfreq/skills/extract.py`: scoped section and requirement parsing.
- `skillfreq/skills/text.py`, `skillfreq/skills/job_market.py`: URL masking for
  atomic evidence.
- `tests/fixtures/focused_calibration_jobs.yml`, `tests/test_focused_calibration.py`:
  compact targeted regression protections.
- `tests/test_calibration.py`, `tests/test_reviewed_calibration.py`,
  `tests/test_market_spot_check.py`: intentional expectation updates with
  existing policy protections preserved.
- This report. Local rerun artifacts remain in ignored `data/outputs/`.

## Full 25-job comparison

| Job | Human rating / score assessment | Lane before → after | Fit before → after | Decision before → after |
|---|---|---|---|---|
| ETL Engineer – Cloud Data Lakehouse & Pipeline Development | Good / reasonable | target_lane → target_lane | 81.41 → 83.91 | apply_now → apply_now |
| AI & Automation Development Intern | Neutral / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Project Engineer | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Engineer, Operations (Mont Belvieu, TX) | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Data Analysis Professional - Supply Chain | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Senior Infra and DevOps Cloud Engineer - Senior Delivery Consultant, Infrastructure Engineering Solutions | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Staff Engineer, Control Systems | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Healthcare Supply Chain & Data Analytics, Strategy, Growth and Transformation, Consultant | Neutral / too_high | bridge_lane → bridge_lane | 65 → 65 | manual_review → manual_review |
| Analyst, Senior Systems | Neutral / too_high | bridge_lane → bridge_lane | 65 → 53.88 | manual_review → skip |
| ETL Engineer – Cloud Data Lakehouse & Pipeline Development | Good / reasonable | target_lane → target_lane | 81.41 → 83.91 | apply_now → apply_now |
| Software Engineer | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Analyst-Application Dev II / SR | Good / reasonable | bridge_lane → bridge_lane | 65 → 65 | manual_review → manual_review |
| Senior Data Engineer | Good / reasonable | target_lane → target_lane | 81.72 → 75.72 | manual_review → manual_review |
| Manager – Global Data Management | Bad / reasonable | bridge_lane → bridge_lane | 65 → 51.73 | manual_review → skip |
| Senior Software Engineer, Backend (Partner Merchant Interface) | Bad / too_high | secondary_lane → secondary_lane | 85 → 84.89 | manual_review → manual_review |
| NOVOS Support Engineer | Neutral / reasonable | bridge_lane → bridge_lane | 65 → 65 | manual_review → manual_review |
| Specialist, Business Analyst (Commercial) | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Adobe AJO Architect | Bad / too_high | bridge_lane → bridge_lane | 65 → 50.5 | manual_review → skip |
| Data Engineer II, Data Products | Bad / too_low | wrong_lane → target_lane | 15 → 80.73 | skip → manual_review |
| Lead Infrastructure Engineer | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Rent Manager Specialist | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
| Principal Data & Analytics Engineer | Bad / too_high | secondary_lane → secondary_lane | 57.8 → 46.3 | manual_review → skip |
| Junior Java Developer | Neutral / too_high | secondary_lane → secondary_lane | 85 → 82.03 | manual_review → manual_review |
| Engineer I-Software Development | Bad / too_low | wrong_lane → secondary_lane | 15 → 62.92 | skip → manual_review |
| Stationary Engineer, Plant Operator (First Grade) | Good / reasonable | wrong_lane → wrong_lane | 15 → 15 | skip → skip |
