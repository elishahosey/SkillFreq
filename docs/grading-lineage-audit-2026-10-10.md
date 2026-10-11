# Historical grading comparison lineage audit

Audit date: October 10, 2026 (America/Chicago). **PASS.**

This is a provenance-only audit and comparison of saved results. No grader was run on jobs, no grading logic was edited, and no historical comparison artifact was regenerated. Saving the current runnable snapshot used its inspection worker only.

## Verified lineage

Retained directory: `C:\Users\ehose\Development\SkillFreq\data\outputs\comparison-requirement-semantics-refreshed-2026-10-09`.

| Check | Result |
|---|---|
| OLD CSV | All 141 CSV and nested grade versions are `3678ae1f5835169c`. |
| NEW CSV | All 141 CSV and nested grade versions are `5e01f710d103c4c0`. |
| Cohort | Both CSVs and `jobs.csv` contain the same 141 unique `(source_site, id)` identities. Titles, descriptions, URLs and search/review context match exactly. |
| Market | Both run records reference the exact retained `market.json` SHA-256. Every grade has the same full market provenance and the matching percentages for its atomic skills. |
| Configuration YAML | Each `.grading.yml` exactly matches its own archive’s configuration, grading version and taxonomy version. |
| Runnable archives | Both inventories and all 48 payload hashes per archive pass. The six configuration files, implementation fingerprints and recomputed grader IDs agree. The replay worker is present. |
| Standalone archives | Retained OLD equals `graders/requirement-semantics-3678ae1f5835169c.zip`; retained NEW equals `graders/grader-2026-10-09-baseline.zip`, byte for byte. |
| Comparison metadata | All 10 checksums in `comparison.json` pass; its version pair, job count and runtime-drift records agree with both runs. |
| Runtime | Both recorded Python 3.12.3 and the same 131 package versions; neither reports runtime drift. |
| Preservation | All 11 historical files, including `comparison.json`, have unchanged hashes before/after the audit and current-snapshot save. |

Market SHA-256: `fdabc9861213addc5b710b395239f941e09a4a1e5b2f3f4b7d84d926e684d2b9`.

Market provenance: taxonomy `31d08964f877`, extraction run `3`, population `extraction_snapshot`, 141 total market jobs, captured `2026-10-10T03:17:42.158254+00:00` (October 9 at 10:17:42 PM America/Chicago). The retained comparison was created `2026-10-10T03:18:48.125036+00:00` (October 9 at 10:18:48 PM America/Chicago).

These checks establish internal provenance and integrity against the saved manifests; they are not a fresh replay or independent proof of the original execution. The historical archive records its recovery runtime, not proof that the earlier original runtime was recovered.

The grade columns already present in `jobs.csv` are input-file baggage, not the definition of OLD. The saved worker selects job inputs and ignores those grade columns. Historical OLD remains `old.grader.zip` / `old.csv`; historical NEW remains `new.grader.zip` / `new.csv`.

## OLD → NEW across all 141 jobs

Headline fields are lane, fit score, fit quality, application decision, AI-review boolean and AI-review reasons. **24 jobs changed at least one headline field; 117 changed none.** Counts below overlap.

| Field | Jobs changed | Transition |
|---|---:|---|
| Lane | 13 | All `secondary_lane` → `wrong_lane` |
| Fit score | 19 | 18 decreased; 1 increased; 122 unchanged |
| Fit quality | 12 | 8 `good_fit` → `weak_fit`; 4 `possible_fit` → `weak_fit` |
| Application decision | 14 | All `manual_review` → `skip` |
| AI-review boolean | 0 | 61 true and 80 false on both sides |
| AI-review reasons | 5 | Removed `low_heuristic_confidence`; another reason remains |
| Confidence | 13 | Heuristic values changed |
| Blocking reasons | 22 | Evidence/decision detail; not 22 decision changes |
| Review flags | 73 | Additional/changed review evidence; not AI-review booleans |

Mean fit: **42.0751 → 36.1613**. Largest decrease: 70 points. Sole increase: 8 points for Lead Software Engineer – Java Full stack, Agentic AI (`in-bb6f3064c67718cf`), 66.34 → 74.34.

| Distribution | OLD | NEW |
|---|---:|---:|
| bridge_lane | 23 | 23 |
| secondary_lane | 32 | 19 |
| target_lane | 13 | 13 |
| wrong_lane | 73 | 86 |
| good_fit | 22 | 14 |
| possible_fit | 43 | 39 |
| weak_fit | 76 | 88 |
| apply_now | 4 | 4 |
| manual_review | 61 | 47 |
| skip | 76 | 90 |

### Every job with a headline change

A single value in a column means unchanged. AI-review booleans are unchanged for every row.

| Job ID | Title | Lane OLD → NEW | Fit OLD → NEW | Quality OLD → NEW | Decision OLD → NEW | AI-reason change |
|---|---|---|---|---|---|---|
| `in-36e96846f61e5df7` | Senior Product Engineer | secondary_lane → wrong_lane | 85 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `in-4d2f3b2d703b9a73` | Project Manager- Nat. Gas Capital Projects | secondary_lane → wrong_lane | 83.12 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `in-8f76dfe457c2942a` | Lab Manager | secondary_lane → wrong_lane | 83.71 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `in-9c5eb5cfcb3b38f0` | IBM MAS (Maximo Application Suite) Technical Architect Manager | bridge_lane | 65 → 59.92 | possible_fit | manual_review → skip | none |
| `in-bb6f3064c67718cf` | Lead Software Engineer - Java Full stack, Agentic AI | secondary_lane | 66.34 → 74.34 | possible_fit | manual_review | none |
| `in-c4a8e1cf902c2012` | Accenture Construct â€“ Manager Digital Solutions (Energy), ANS | secondary_lane → wrong_lane | 58.03 → 15 | possible_fit → weak_fit | manual_review → skip | none |
| `in-c9fbd773c6b9399e` | Engineer I-Software Development | wrong_lane | 15 | weak_fit | skip | Removed low_heuristic_confidence; retained ambiguous_requirements |
| `in-fd34801e32bf1c9b` | Analyst, Lead Data Engineering | secondary_lane | 50.97 → 42.97 | weak_fit | skip | none |
| `li-4452853921` | Sustaining Software Engineer | secondary_lane | 79.57 → 79.07 | possible_fit | manual_review | none |
| `li-4453686031` | Data Analysis Professional - Supply Chain | wrong_lane | 15 | weak_fit | skip | Removed low_heuristic_confidence; retained positive_and_exclusion_signals |
| `li-4463898600` | Engineer, Operations (Mont Belvieu, TX) | secondary_lane → wrong_lane | 85 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `li-4464128808` | Slalom Flex (Project Based)- Data Migration Engineer | target_lane | 91.44 → 83.44 | good_fit | manual_review | none |
| `li-4466252215` | Technical Product Owner (O&G background w/SAFe Agile exp) | secondary_lane → wrong_lane | 85 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `li-4467125314` | SAP S/4HANA Data Migration Lead | secondary_lane → wrong_lane | 47.0 → 15 | weak_fit | skip | none |
| `li-4472843239` | Software Development Engineer | secondary_lane → wrong_lane | 79.14 → 15 | possible_fit → weak_fit | manual_review → skip | none |
| `li-4472854693` | Sr. Advisor II, Commercial Data Engineering | secondary_lane → wrong_lane | 79.39 → 15 | possible_fit → weak_fit | manual_review → skip | none |
| `li-4472920517` | Specialist, Business Analyst (Commercial) | secondary_lane → wrong_lane | 85 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `li-4472954109` | IBM Sterling Order Management Technical Lead | secondary_lane → wrong_lane | 71.96 → 15 | possible_fit → weak_fit | manual_review → skip | none |
| `li-4474550134` | Engineer I-Software Development | wrong_lane | 15 | weak_fit | skip | Removed low_heuristic_confidence; retained ambiguous_requirements |
| `li-4474830217` | Principal AI Data Engineer | target_lane | 69.94 → 61.94 | possible_fit | manual_review → skip | none |
| `li-4475707621` | Engineer, Staff Fixed Equipment (Mont Belvieu, TX) | secondary_lane → wrong_lane | 83.0 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `li-4475725980` | Data and Product Analyst- Nonprofit | secondary_lane → wrong_lane | 81.91 → 15 | good_fit → weak_fit | manual_review → skip | none |
| `li-4475763388` | Manager, AI Risk & Validation | wrong_lane | 15 | weak_fit | skip | Removed low_heuristic_confidence; retained positive_and_exclusion_signals |
| `li-4477419320` | Senior Platforms Engineer | wrong_lane | 15 | weak_fit | skip | Removed low_heuristic_confidence; retained ambiguous_requirements |

## Requirement and gap representation

The complete required-gap object changed for **8 jobs**; the complete preferred-gap object changed for **13 jobs**. These include source-span/group representation changes, not just newly missing skills. Group comparisons below ignore list order and generated group IDs, while preserving source text, grammar, type, skill alternatives, satisfaction and equivalent evidence.

| Section | Evidence | Jobs changed | Job IDs |
|---|---|---:|---|
| required | atomic_skills | 1 | `li-4475754566` |
| required | capability_concepts | 2 | `li-4475754566`, `li-4474532492` |
| required | requirement_groups | 7 | `li-4446676420`, `li-4475754566`, `li-4476205667`, `in-7fca3c9a5cdbe11b`, `li-4474324456`, `li-4474522110`, `li-4474526305` |
| required | unsatisfied_groups | 1 | `li-4476205667` |
| required | ambiguous_groups | 0 | none |
| preferred | atomic_skills | 4 | `li-4474826863`, `li-4474848563`, `li-4452853921`, `li-4465339847` |
| preferred | capability_concepts | 3 | `li-4452853921`, `li-4465339847`, `li-4472843239` |
| preferred | requirement_groups | 10 | `li-4446676420`, `li-4459650362`, `li-4468282056`, `li-4474826863`, `li-4474830217`, `li-4474848563`, `li-4437737649`, `li-4452853921`, `li-4465339847`, `li-4474522110` |
| preferred | unsatisfied_groups | 3 | `li-4446676420`, `li-4468282056`, `li-4437737649` |
| preferred | ambiguous_groups | 0 | none |

Seniority and requirement-flag objects have representation changes on all 141 jobs because NEW adds evidence fields, candidate experience, title levels and related context. This does **not** mean 141 changed qualification judgments. The extracted `years_required` value itself changes on 30 jobs. Full old/new evidence for each changed object is retained in the audit JSON.

### Five human-reviewed jobs

**All five have unchanged headline fields between `3678...` and `5e01...`. None is a completely identical grade record once supporting evidence and schema changes are included.**

| Job ID / role | Lane, fit, quality, decision on both sides | AI review on both sides | Supporting differences |
|---|---|---|---|
| `in-7fb8f90cfca11195` Robotics Engineer | `wrong_lane`, 15, `weak_fit`, `skip` | false; no reasons | Required experience changes from unavailable to 2 years; years-present evidence and newer audit fields added. |
| `li-4459650362` Quality Assurance Supervisor | `wrong_lane`, 15, `weak_fit`, `skip` | false; no reasons | Adds a satisfied preferred SQL / SQL Server / MySQL alternative group. Atomic gap sets stay unchanged. |
| `li-4446676420` Lead DevOps Engineer (GovCloud) | `wrong_lane`, 15, `weak_fit`, `skip` | false; no reasons | Python/Java desirable wording moves to preferred; Terraform must-have remains required. A preferred AWS/GCP certification alternative is recorded as unsatisfied. Adds title-seniority and clearance-eligibility review flags. Atomic gap sets stay unchanged. |
| `in-12212552d5d9b1fa` Integration Engineer | `target_lane`, 84.82, `good_fit`, `apply_now` | false; no reasons | Adds the seniority term `architect` and richer audit fields. Requirement-gap objects stay unchanged. The later Boomi correction is not in either historical side. |
| `in-85165dc0ecbc4c68` AI & Automation Development Intern | `wrong_lane`, 15, `weak_fit`, `skip` | true; `positive_and_exclusion_signals`, `low_heuristic_confidence` | SECONDARY eligibility is removed and its 12 points are suppressed. WRONG still wins 36 versus BRIDGE 22. Requirement-gap objects stay unchanged. |

## Current grader preserved separately

Saved artifact: `C:\Users\ehose\Development\SkillFreq\data\outputs\graders\grader-boomi-specialization-434d61fbf4dfe7b9.zip`.

Grading version: `434d61fbf4dfe7b9`. SHA-256: `8c824a2636fb6dfd29304c7b207c4b6d469d7d8462ca1fd64623e58c6106854c`.

All 48 archived payload hashes, parsed configurations, implementation fingerprints and recomputed grader identity pass verification. The saved worker was executed in inspection mode during save. Only `configs/roles.yml` differs from the retained `5e01...` archive payload; all Python code and the recorded runtime match. Dependencies are version-recorded, not bundled installable packages.

## Safe next comparison — prepared, not run

For the next comparison, OLD must be the **historical NEW archive** (`5e01...`), and NEW must be the separately saved `434d...` archive. Reuse the historical `jobs.csv` and `market.json` directly. Do not capture fresh market data or use a rolling database query.

```powershell
$ErrorActionPreference = 'Stop'
$root = 'C:\Users\ehose\Development\SkillFreq'
$retained = 'C:\Users\ehose\Development\SkillFreq\data\outputs\comparison-requirement-semantics-refreshed-2026-10-09'
& "$root\.venv-skillfreq\Scripts\python.exe" "$root\scripts\grading_snapshot.py" compare `
  --old "$retained\new.grader.zip" `
  --new "$root\data\outputs\graders\grader-boomi-specialization-434d61fbf4dfe7b9.zip" `
  --input "$retained\jobs.csv" `
  --market "$retained\market.json" `
  --out-dir 'C:\Users\ehose\Development\SkillFreq\data\outputs\comparison-boomi-specialization-5e01f710d103c4c0-to-434d61fbf4dfe7b9'
if ($LASTEXITCODE -ne 0) { throw 'Comparison failed; inspect the diagnostic above.' }
```

The command is also saved as `data/outputs/lineage-audit-2026-10-10/compare-baseline-to-boomi.ps1` for later use. The comparison tool refuses an existing output directory and does not allow runtime drift unless explicitly requested; the prepared command supplies no such override.

The new directory will contain `old.csv`, `new.csv`, `old.grading.yml`, `new.grading.yml`, `old.run.json`, `new.run.json`, `old.grader.zip`, `new.grader.zip`, `jobs.csv`, `market.json`, and `comparison.json`. In that directory only, OLD means `5e01...` and NEW means `434d...`.

Use a separate review workbook for that later comparison. The existing five-row workbook remains a current-state spot check of `5e01...`; its OLD input was the historical `new.csv`, paired with the equivalent refreshed export. It is not a human-rated `3678...` → `5e01...` comparison.

## Retained audit evidence

- `data/outputs/lineage-audit-2026-10-10/audit.json`: all 141 identities, outcomes, changed evidence, summaries, and all 11 original file hashes.
- `data/outputs/lineage-audit-2026-10-10/snapshot-preservation.json`: separately saved current snapshot version/hash and verification.
- `data/outputs/lineage-audit-2026-10-10/audit.py`: provenance-only checker; imports no grading implementation and uses exclusive output creation.

Changes here are descriptive differences in retained outputs, not claims of human-validated improvement.
