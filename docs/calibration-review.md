# Manual calibration review

From the repository root, with the SkillFreq environment active:

```powershell
python -m pip install streamlit==1.64.0
python -m streamlit run scripts/review_calibration.py
```

Streamlit is also in `requirements.txt`. Excel support reuses the existing
`openpyxl` dependency. This is a local, single-reviewer utility; no database or AI
calls are made. Keep the output workbook closed in Excel while saving reviews.

## Load a comparison

The default paths are the saved `results-db-90-days-requirements.csv` and
`results-db-90-days-requirement-semantics.csv` exports in `data/outputs/`.
Change these to review another grading pass. `skillfreq/pipeline.py` writes these
exports; `scripts/regrade_saved_cohort.py` can generate a new export. The existing
comparison scripts produce reports from those exports, not an Excel review table.
The review UI only reads the saved results and their existing `grade_json` evidence.

Choose either:

- **Two grading exports:** OLD and NEW CSV/XLSX paths. Matching uses
  `(source_site, id or source URL)`, as in the existing comparison scripts.
  `job_id` and `source_row_id` are also accepted. Unmatched records are counted
  and excluded. Duplicate or missing identities produce an error.
- **One comparison file:** a CSV/XLSX with `old_*` and `new_*` named grading
  columns, plus `id`, `job_id`, `source_row_id`, or `source` and optional
  `source_site`, `title`, `company`, `description`. Use existing names such as
  `old_role_lane`, `new_fit_score`, `old_apply_decision`,
  `new_ai_review_required`. Short aliases `lane`, `fit`/`score`, `decision`,
  and `result` are accepted after either prefix. `old_grade_json` and
  `new_grade_json` are also supported. Excel reads the first worksheet with
  headers on the first row. Keep IDs stored as text to retain leading zeros.

The default queue contains up to **100 unreviewed changed jobs plus 5 unchanged
jobs**. Selected signals are OR filters: decision change, lane change, absolute
fit-score change of at least 5, or AI-review flag/reason change. Optional
**Other evidence changed** includes requirement gaps, seniority, blockers,
reasons, and smaller score changes. Adjust the threshold, count and status,
then click **Load / rebuild queue**.

Within the changed set, unreviewed jobs come first, then decision changes,
lane changes, score changes and AI changes, then largest score difference.
The unchanged sample uses a fixed random seed and excludes small score changes.
“Unchanged” refers to the displayed grading fields, excluding version IDs;
it does not imply identical hidden audit metadata. Only one job is rendered.

## Review and resume

Read OLD/NEW results, description and grading evidence. Select **1 = Good**,
**2 = Neutral / Unclear**, or **3 = Bad**, with optional tags and note.
Judge whether NEW is justified by the posting and configured rules, not personal
job preference, whether you would apply today, or a guess about recruiter interest.
The reminder above the controls stays visible; expand **Calibration mindset**
for the full guidance. Each rating control also has a short help tooltip.

The overall rating remains the top-level judgment. Neutral / Unclear includes
mixed results, both OLD and NEW being defensible, or insufficient evidence.
Three sub-grades explain that judgment:

- **Decision quality:** `better`, `same`, `worse`, `unclear` — NEW vs OLD under
  SkillFreq's application-decision rules.
- **Score quality:** `too_high`, `reasonable`, `too_low`, `unclear` — NEW fit
  score relative to the posting's requirements and other grading evidence.
- **Requirement interpretation:** `correct`, `unclear`, `incorrect` — NEW
  handling of required/preferred, alternatives, groups, equivalents and ambiguity.

Sub-grades start blank, with no suggested answer. They can remain blank to avoid
blocking a review; choose `unclear` when that is your judgment rather than leaving
an unanswered field. `requirement_semantics_issue` is available alongside the
existing issue tags. For ratings 2 or 3, please explain with a note or issue tag.

**Save + Next** saves and advances. **Save** stays on the current job.
**Previous / Next** navigate without saving and discard unsaved edits.
Ratings 2 and 3 without explanation show a gentle reminder but still save.
At the end of a queue, rebuild it for the next batch. Saved items remain in the
current queue until rebuilding, so Previous can revisit them.

With a blank output path, the UI finds the most recent matching
`calibration_review_*.xlsx` next to the NEW/comparison input, including previous
days. Otherwise it creates `calibration_review_YYYY-MM-DD.xlsx` there on the first
save. The selected output path stays fixed throughout the run. Supply an explicit
path to resume a differently named workbook or start a separate review run.
If today's filename already belongs to another comparison, choose another path.

Each save rereads the review workbook, updates the row for the same
`(source_site, job_id)`, and replaces the workbook after a complete temporary
write. It contains only reviewed records: identifiers, title/company, selected
OLD/NEW grading fields (including existing grading versions), `review_rating`,
`decision_quality`, `score_quality`, `requirement_interpretation`, note,
semicolon-separated tags, `reviewed`, and a UTC `reviewed_at` timestamp.
Input paths identify the comparison. Full descriptions and raw grade JSON are
not copied into the review output. Original inputs are never written.

After restarting, choose the same inputs and click **Load / rebuild queue**.
The saved file is detected and reviewed IDs are excluded by default, so the
queue resumes with unreviewed work. Use **All** or **Reviewed** to amend saved
ratings. Filters and an unsaved cursor are not persisted; saved reviews are.
Revisiting a saved record restores the overall rating, all three sub-grades,
tags and note. Older review workbooks without sub-grade columns still load:
these fields appear blank and are added on the next save. Existing reviews
remain reviewed and retain their original notes/tags. No migration is needed.

Assumptions: input exports remain unchanged during a review run, one reviewer
writes a workbook at a time, and a source-row ID is stable within its comparison.
Company is shown when present; current grading CSVs omit it. Missing optional
fields stay unavailable. No grader changes or versioning subsystem are needed.

Deferred: keyboard shortcuts, company enrichment, additional import aliases,
saved filter preferences and concurrent reviewers. There are no dashboards,
charts, services, database changes, or frontend/backend split.

**AI second opinion is deferred.** SkillFreq currently has AI-review flags and
imports of external review output, but no callable AI client to reuse here.
This update adds no AI integration or automated judging. A future second opinion
should be explicitly requested only after saving the human judgment and stored
separately, without prefilling or overwriting human fields.

Focused checks:

```powershell
python -m unittest discover -s tests -p test_calibration_review.py
```
