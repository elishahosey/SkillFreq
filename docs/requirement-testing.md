# Requirement semantics: testing handoff

This guide accompanies the requirement-group semantic fix. The bundle contains
the edited files, the requirement fixture and the generated validation reports.
Apply the files to the existing SkillFreq repository; the bundle is not a
standalone replacement for the repository and its dependencies.

## Verified results from the implementation pass

The full suite ran **95 tests: 93 passed and 2 optional PostgreSQL integration
tests were skipped**. Packaging these files did not rerun the tests or cohort.

The frozen replay compared **8,692 jobs** using saved market prevalence:

| Check | Result |
|---|---:|
| Changed lanes | 0 |
| Changed learning scores | 0 |
| Changed required atomic gaps | 442 |
| Changed preferred atomic gaps | 331 |
| Newly explicit required group gaps | 615 |
| Newly explicit preferred group gaps | 403 |
| Changed fit scores | 287 |
| Changed fit quality | 52 |
| Changed apply decisions | 22 |
| Changed AI-review flags | 66 |
| Unattributed changed jobs | 0 |

The changed-field counts overlap. There are 1,635 changed rows when newly exposed
group-gap evidence is included. Inline-preferred section-boundary corrections
affect experience/section-scoped alignment in 190 rows; the report exposes these
effects rather than treating them as group penalties.

Before grading version: `5b4f855d2cdf0292`.
After grading version: `3678ae1f5835169c`.
Role rules, profile, atomic taxonomy and all existing scoring settings match the
baseline configuration. The new required-group penalty is 3 points.

## Run the tests

Run commands from the repository root. These PowerShell examples use the existing
virtual environment. On another machine, substitute its configured Python
interpreter after installing the repository's dependencies.

Focused requirement extraction, satisfaction, scoring, trace and validation tests:

```powershell
.\.venv-skillfreq\Scripts\python.exe -m unittest discover -s tests -p test_requirements.py -v
```

Frozen-comparison integrity tests:

```powershell
.\.venv-skillfreq\Scripts\python.exe -m unittest discover -s tests -p test_requirement_comparison.py -v
```

Full existing suite, including lane/domain/ecosystem regressions:

```powershell
.\.venv-skillfreq\Scripts\python.exe -m unittest discover -s tests -v
```

The two PostgreSQL tests require the existing development database configuration.
Their test transactions roll back. They were **not run** in this semantic pass.
To opt in separately:

```powershell
$env:SKILLFREQ_TEST_DB = '1'
try {
    .\.venv-skillfreq\Scripts\python.exe -m unittest discover -s tests -p test_grading_postgres.py -v
} finally {
    Remove-Item Env:SKILLFREQ_TEST_DB
}
```

## What the focused tests prove

| Scenario | Assertion |
|---|---|
| AWS AND Spark | Two individual gaps; no group charge |
| AWS, Azure OR GCP; Azure known | Satisfied choice; no missing AWS legacy charge |
| Databricks OR Snowflake; neither known | One explicit gap and exactly one configurable fit charge |
| Airflow OR equivalent | Explicit configured evidence can satisfy the group; otherwise one gap |
| Power BI preferred | Preferred only, including an inline sentence in a required section |
| SQL Server AND PostgreSQL | Separate atomic operands; known experience satisfies them |
| One or more database options | One known option suffices; generic SQL alone cannot substitute |
| SQL AND (AWS OR Azure) | Ambiguous; no mandatory gap charge; existing AI-review gate sees ambiguity |
| Databases such as ... | Example group, not three independent requirements |
| Services: ... | Colon alone does not create an alternative |
| Unstructured ETL sentence | Legacy fallback retained, even alongside a structured cloud choice |
| Separate AWS mandatory sentence | Still required even when another cloud alternative is satisfied |
| Known atomic / missing broad concept | Known atomic mention cannot become a contradictory core blocker |
| Preferred alternative | No required-group penalty or independent-option legacy charge |
| Trace rendering | Real group contribution and fallback routing are visible |
| Configuration errors | Invalid penalties and equivalent references fail clearly |
| Comparison integrity | Ignores atomic ordering; rejects changed inputs, lane drift and unexplained score drift |

The original section-aware fixtures are in `tests/fixtures/requirements_jobs.yml`.
Additional semantic cases are inline in `tests/test_requirements.py`. The broader
lane/domain/ecosystem tests remain in the existing repository.

## Reproduce the frozen-cohort comparison

Required local baseline inputs:

- `data/outputs/results-db-90-days-requirements.csv`
- `data/outputs/results-db-90-days-requirements.grading.yml`

The large CSV exports are not included in the handoff bundle. Copy these inputs
from the original workspace if the next chat needs to rerun the cohort. The
included reports are sufficient to inspect the recorded comparison, but do not
replace the original job descriptions and saved market data needed for replay.

Use fresh output paths to preserve the verified exports and reports:

```powershell
.\.venv-skillfreq\Scripts\python.exe scripts/regrade_saved_cohort.py `
  --input data/outputs/results-db-90-days-requirements.csv `
  --out data/outputs/results-db-90-days-requirement-semantics-recheck.csv `
  --frozen-market

.\.venv-skillfreq\Scripts\python.exe scripts/compare_requirements.py `
  --before data/outputs/results-db-90-days-requirements.csv `
  --after data/outputs/results-db-90-days-requirement-semantics-recheck.csv `
  --out docs/generated/recheck/requirement-semantics.md
```

`--frozen-market` uses saved per-job prevalence and makes no DB prevalence query.
Replay uses the real production grading path and writes a configuration snapshot.
The comparison checks ordered row identity, descriptions and search context;
compares atomic gaps as sets; verifies protected configuration from snapshots;
and fails on lane/learning drift or unattributed changes. It is a dry replay and
does not append grades to PostgreSQL.

## Included evidence to read in the next chat

1. `docs/requirement-semantics.md`: implementation, configuration, limits and files changed.
2. `docs/generated/requirement-semantics.md`: aggregate results and 30 changed examples.
3. `docs/generated/requirement-semantics.json`: all 1,635 changed rows, source groups,
   before/after penalties and attribution. This larger file is included in the ZIP.
4. `docs/generated/lead-analyst-requirement-audit.md`: source-by-source audit of
   Databricks, Spark, AWS, Redshift and Power BI.
5. `docs/generated/lead-analyst-requirement-trace.md`: actual deterministic trace.

Lead Analyst remains TARGET; Redshift's restored individual penalty changes fit
from 56.5 to 53.5 and the decision from manual review to skip. Parenthetical slash
wording such as `PySpark/Pandas`, unrelated OR clauses and multi-line alternative
headers remain documented parser limits. These are inspection points, not proof
that all requirement language is fully understood.
