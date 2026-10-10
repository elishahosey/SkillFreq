# Save grading versions and compare them on fresh data

A saved **grader** contains its code, configuration and runtime version record.
The **jobs** and **market data** are separate inputs. You can therefore use an old
grader and a new grader on the same fresh jobs and refreshed market data without
confusing rule changes with changes in the input population.

Run these commands from the repository root with the SkillFreq environment active.

## Concepts behind the workflow

A grading result depends on four things:

```text
result = grade(grader code + configuration, job inputs, market snapshot, runtime)
```

**OLD and NEW identify grader versions, not the age of the jobs.** An old grader
can evaluate today's jobs using today's market percentages. The market snapshot
contains aggregate skill percentages and provenance; it is separate from the
individual jobs selected for grading. Refreshing the database does not update a
previously exported CSV or its YAML.

| Concept | What it means here |
|---|---|
| Controlled comparison | Hold jobs, market data and runtime fixed while changing the grader. Differences can then be attributed to the combined code/configuration change. To isolate configuration alone, keep the code fixed too. |
| Confounding | If both the grader and market data change, a changed result does not by itself tell you which caused it. Comparing unrelated job sets introduces another source of variation. |
| Fixed cohort | Save the exact job identities and input text. Repeating a rolling 90-day database query later does not guarantee the same jobs or descriptions. |
| Versioning | Give saved grader configurations and implementations an identity. A `grading_version` does not identify the job cohort or market percentages. |
| Reproducibility | Retain the code, configuration, inputs and environment information needed to run the calculation again. Recording dependency versions is not the same as archiving their installable packages. |
| Provenance | Record where the inputs and results came from: source artifacts, market extraction run, versions and checksums. |
| Integrity check | A hash can verify that file contents match a recorded fingerprint. It cannot reconstruct a missing file or prove that a grade is correct. |

Choose which question you want to answer before rerunning:

| Question | Grader | Jobs | Market |
|---|---|---|---|
| Can I reproduce the earlier result? | Same saved version | Same saved inputs | Same saved values |
| Did the grading changes improve results? | OLD versus NEW | One shared cohort | One shared snapshot |
| What did the market refresh change? | One saved version | One shared cohort | Earlier versus refreshed snapshot |
| How do both graders handle new jobs? | OLD versus NEW | One shared new cohort | One shared snapshot |

Keep the runtime fixed for these comparisons as well. Re-evaluating an old grader
on refreshed data is a new run, not a reproduction of the old results. Human
calibration review still determines whether the outputs are justified by the
postings; reproducibility alone does not establish correctness.

## Save each version before changing its rules or code

```powershell
python scripts/grading_snapshot.py save --out data/outputs/graders/baseline.zip
```

After changing the configuration or grading implementation, save another version:

```powershell
python scripts/grading_snapshot.py save --out data/outputs/graders/candidate.zip
```

Each ZIP contains the exact Python source under `skillfreq/`, the six grading
configuration files (including the profile and taxonomy), the replay worker,
`requirements.txt` when present, file checksums, grading/taxonomy versions and
the Python/package versions used to validate the snapshot. Uncommitted source
edits are preserved. Database credentials, `.env`, jobs and market values are
not included. Keep these ZIPs as retained artifacts; the output directory is
Git-ignored. Snapshots cannot overwrite existing files.

## Capture the refreshed market once

After the normal market refresh:

```powershell
python scripts/grading_snapshot.py capture-market --out data/outputs/market-current.json
```

This makes one read of the existing database prevalence view and stores the full
mapping and its provenance. It does not refresh the database. Use a new filename
for each capture. A full mapping is needed because different graders may extract
different skills; per-job values in old exports are not a full market backup.

## Run both versions on identical jobs and market data

The input can be an existing grading export or a jobs CSV with `title`,
`description`, an ID or source URL, and preferably `source_site`. IDs remain text.
Existing grade columns are ignored. Saved exports retain useful job inputs but
are not guaranteed lossless archives of the original database records.

```powershell
python scripts/grading_snapshot.py compare `
  --old data/outputs/graders/baseline.zip `
  --new data/outputs/graders/candidate.zip `
  --input data/outputs/results-db-90-days-requirements.csv `
  --market data/outputs/market-current.json `
  --out-dir data/outputs/comparison-current
```

The input can also be a newer job export: both graders will evaluate that new
job set. No jobs are fetched or selected by a moving date window during replay.

The comparison folder retains:

- `old.csv` and `new.csv`, with their `.grading.yml` and `.run.json` records.
- Both runnable grader ZIPs, the exact shared `jobs.csv` and `market.json`.
- `comparison.json`, with input/output checksums, versions and the job count.

Load `old.csv` as OLD and `new.csv` as NEW in the existing calibration review UI.
The two sides have the same job identities. Each grader runs in a separate Python
process using its saved source/configuration; the active checkout's grading rules
are not substituted. Replay does not query the database or persist grades there.
The comparison directory is published only after both runs succeed.

Both graders must have the same taxonomy version as the captured market. A
taxonomy change needs an explicitly compatible market extraction; the tool fails
instead of silently mixing incompatible percentages. Python and saved package
versions are checked as well. Restore the recorded environment for reproducible
runs. `--allow-runtime-drift` permits an intentional environment change and records
the differences in the run/comparison manifests; it does not claim exact runtime
reproduction. Extra installed packages are allowed. Dependencies are recorded,
not bundled or automatically installed. Only execute grader ZIPs you trust: they
contain Python source. Checksums detect changed files, not their trustworthiness.

## Existing exports with only a `.grading.yml`

Historical YAML files contain parsed configuration and source fingerprints,
not the source itself. They cannot recreate a missing historical implementation.
Restore the matching source and original configuration in a separate checkout,
then save and verify it:

```powershell
python scripts/grading_snapshot.py save `
  --source-root C:/path/to/restored-checkout `
  --expect-snapshot data/outputs/results-db-90-days-requirements.grading.yml `
  --out data/outputs/graders/historical-requirements.zip
```

The check rejects any configuration or implementation that differs from that
export. It verifies grader identity, not the unavailable historical runtime;
the bundle records the environment used to create it. If only the parsed YAML
configuration remains, recreating it under today's code is a new grading variant,
not proof that the historical grader was restored. See
[grading reproduction](grading-reproduction.md) for recovery details.

The new snapshot workflow works prospectively without historical reconstruction:
save today's grader, change it, save the candidate, and run both on whichever
shared jobs and market snapshot you want to evaluate.

## Worked comparison: requirement semantics on the refreshed cohort

On **October 9, 2026 (America/Chicago)**, the requirement-semantics grader was
recovered and applied to the jobs in the latest export. These are retained local
artifacts under `data/outputs/`; they are Git-ignored and are not distributed with
the repository.

| Input | Retained value |
|---|---|
| Historical configuration | `results-db-90-days-requirement-semantics.grading.yml` |
| OLD grader version | `3678ae1f5835169c` |
| NEW grader version | `5e01f710d103c4c0` |
| Shared jobs | The 141 rows from `results-db-2026-10-08_17-08-54-691977.csv` |
| Shared market | Extraction run `3`, taxonomy `31d08964f877` |
| Runtime | Python `3.12.3`; neither saved bundle reported runtime drift |
| Comparison directory | `comparison-requirement-semantics-refreshed-2026-10-09/` |

Recovery used the matching changed Python files from
`skillfreq-requirement-semantics-with-tests.zip` and the unchanged current files
whose hashes still matched the historical YAML. The saved configuration values
were restored separately. `save --expect-snapshot` verified the reconstructed
grader against the historical configuration and implementation fingerprints.
The runnable OLD archive is
`graders/requirement-semantics-3678ae1f5835169c.zip`. This validates the saved
grader identity; it does not prove that the original historical Python/package
environment was recovered. The bundle records the environment used for recovery.

The comparison was checked as follows:

- All 141 jobs matched between OLD and the latest NEW export, with zero excluded
  records on either side.
- Every market percentage recorded in the latest export matched the refreshed
  database snapshot, and both referenced extraction run `3`.
- The generated `old.grading.yml` exactly matched the historical
  requirement-semantics YAML, including configuration and implementation hashes.
- Every regenerated NEW `grade_json` matched the latest export after excluding
  the market read timestamp. Capturing the same values again changes that timestamp.
- All file checksums in `comparison.json` were verified.

For this review, set **OLD export path** to:

```text
C:\Users\ehose\Development\SkillFreq\data\outputs\comparison-requirement-semantics-refreshed-2026-10-09\old.csv
```

Set **NEW export / comparison path** to either the adjacent `new.csv` or the
verified latest export:

```text
C:\Users\ehose\Development\SkillFreq\data\outputs\results-db-2026-10-08_17-08-54-691977.csv
```

Use the same pair of paths when resuming saved human reviews: the review workbook
uses input paths to identify the comparison. The OLD field takes the generated
CSV, not its `.grading.yml`. That YAML describes the grader; it does not contain
the newly calculated per-job results or the full market snapshot.

To repeat the comparison without querying the database, use the artifacts already
retained inside the comparison directory and choose a new destination:

```powershell
$comparison = 'data/outputs/comparison-requirement-semantics-refreshed-2026-10-09'
python scripts/grading_snapshot.py compare `
  --old "$comparison/old.grader.zip" `
  --new "$comparison/new.grader.zip" `
  --input "$comparison/jobs.csv" `
  --market "$comparison/market.json" `
  --out-dir data/outputs/comparison-requirement-semantics-replay
```

To evaluate a later refresh, capture a new market snapshot and select the desired
jobs instead. Preserve the existing comparison directory for review history.
