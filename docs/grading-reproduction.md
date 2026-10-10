# Preserve and reproduce a grading run

Keep the results CSV and its matching `.grading.yml` together for any run you
want to explain, compare or reproduce later. They are part of the audit trail.
The YAML alone is not a complete backup: it records configuration contents and
code fingerprints, but does not archive source code, job inputs or dependencies.

For new runs, [runnable grading snapshots](grading-snapshots.md) archive source
and configuration together and let OLD/NEW graders share one job and market
snapshot. Use that workflow for future comparisons on refreshed data. The
historical recovery details below still apply to exports saved before that workflow.

## What to keep

| Artifact | Why it matters |
|---|---|
| Original input CSV, or an export of the exact database rows graded | Preserves job identities, titles, descriptions and other input fields |
| Results CSV, including complete `grade_json` values | Preserves grades, evidence and the market values used for each job |
| Matching `.grading.yml` | Preserves configuration contents, implementation hashes and version identifiers |
| Git commit and any uncommitted source changes, or an exact source archive | Makes the old implementation available; hashes cannot reconstruct files |
| Original `configs/` files, including any custom profile | Preserves settings and the exact taxonomy file bytes |
| Python version and installed dependency versions | Helps reconstruct the runtime used for grading |
| Run notes with the command, date, input paths and offline/market mode | Records how the inputs and settings were selected |

For database grading, preserve the selected input rows at the time of the run.
Repeating `grade-db --since-days 90` later uses a moving date window and potentially
changed database contents. A results CSV retains useful job fields, but is not a
guaranteed lossless archive of every original input column.

Record runtime and revision information while the original environment is active:

```powershell
git rev-parse HEAD
git status --short
python --version
python -m pip freeze
```

Save these outputs in the run's archive. A commit ID alone does not preserve
uncommitted edits or untracked files; retain those files too. Keep a recoverable
copy of the repository or source, not just its commit ID.

Use a distinct output basename for each retained run, such as
`results-2026-10-08-offline.csv`. Reusing `--out` replaces both that CSV and its
adjacent snapshot. Archive important runs before rerunning a command that uses
the same output path, including the default DB grading task. Store archives
outside the `import/` intake tree, which is scanned recursively by folder imports.

Database persistence is useful additional history, but does not replace the
source/input archive. `--persist-grades` saves grades and configuration; it does
not preserve a copy of the Python source or import the original jobs.

## What the hashes mean

Each value under `configuration.implementation` is the SHA-256 hash of a Python
file's raw bytes, with its path relative to `skillfreq/`. These values identify
file contents, not scores or Git commits. Comments, whitespace and line-ending
changes also change the hash without necessarily changing grading behavior.

The `grading_version` combines the saved configuration with implementation hashes
and the market taxonomy version. The `taxonomy_version` is derived from the raw
bytes of `market_skills.yml`. Rewriting identical taxonomy definitions with
different YAML formatting can therefore change both version identifiers.

Neither version identifies the job population or historical market percentages.
Matching versions are necessary for an exact replay, but do not by themselves
prove that the inputs or results match.

## Reproduce an offline run

1. Restore the original code in a separate checkout or source directory. Restore
   any source changes that were not committed. Recreate the original Python and
   dependency environment using the saved version information.
2. Restore the original configuration files: `skills.yml`, `profile.yml`,
   `weights.yml`, `roles.yml`, `market_skills.yml` and `requirements.yml`. Restore
   a custom profile to the path used by the command, if applicable. The snapshot's
   `configuration` section contains their parsed contents if the files are lost,
   but reconstructing YAML does not recover the original formatting or byte hashes.
3. Check the implementation hashes against the saved snapshot. For example, run
   this from the restored repository root and compare it with
   `configuration.implementation["score/grading.py"]`:

   ```powershell
   (Get-FileHash skillfreq/score/grading.py -Algorithm SHA256).Hash.ToLower()
   ```

   Repeat for the other listed files. If a hash differs, investigate the source
   or line endings; do not edit the saved hashes to make the check pass.
4. Grade the saved input CSV and write to a new output path:

   ```powershell
   python -m skillfreq.cli grade-csv `
     --input archive/original-jobs.csv `
     --out data/outputs/reproduced.csv `
     --offline-grading
   ```

   Replace the example input path with the archived CSV. Supply `--profile` if
   the original run used a custom profile. This command applies when the original
   run explicitly used offline grading.
5. Compare the new snapshot's `grading_version` and `taxonomy_version` with the
   originals. Match jobs by identity and compare the parsed `grade_json` records,
   including lanes, scores, decisions, reasons and evidence. Compare structured
   values rather than CSV quoting or JSON key order.

## Reproduce a run that used market data

Restore the same code, configuration, runtime and input rows as above. Reading
today's `public.skill_prevalence` is not an exact historical replay: a market
refresh can change learning scores even with an unchanged `grading_version`.

Each result's `grade_json.market_context` records market provenance and a
`prevalence_pct` mapping for that job's extracted skills. A replay script can
pass those saved values to the existing Python grader for each original job:

```python
# context: GradingContext loaded from the restored configuration files
# original_job: the archived input row
# saved_grade: the parsed grade_json for the same job
market = saved_grade["market_context"]
prevalence = {
    skill: pct
    for skill, pct in market["prevalence_pct"].items()
    if pct is not None
}
replayed = grade_job(
    original_job,
    context,
    prevalence=prevalence,
    market_context=market,
)
```

Import `GradingContext` and `grade_job` from `skillfreq.score.grading` in that
script. Null percentages mean no value was available for that skill; omit them
from the supplied mapping. If the original run had no market data at all, pass
`prevalence=None` and its saved market context instead. An empty mapping and
`None` have different meanings: available data with no values versus unavailable
data. Preserve the saved market metadata, including read time and extraction run
IDs, when comparing the complete grade record.

The current CLI has no snapshot-replay option and does not automatically load a
`.grading.yml` as grading configuration. Exact historical market replay requires
a script using these API inputs, or a restored historical database with the same
market values. A fresh database read produces new read-time metadata even if the
scores match. Running with `--offline-grading` does not reproduce a market-backed
run's learning results.

If source, input rows or market values are missing, keep the remaining artifacts
for inspection, but describe any new run as a re-evaluation rather than claiming
an exact reproduction.
