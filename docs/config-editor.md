# Local config editor

From the repository root, activate the existing SkillFreq Python environment and run:

```powershell
python -m streamlit run scripts/config_editor.py --server.address 127.0.0.1
```

Streamlit and PyYAML are already in `requirements.txt`. No extra dependencies,
database connection, or AI calls are needed.

## Edit and save

1. Choose a **Config file**, **Section**, and setting in the sidebar. The page
   shows the absolute file path and its last-modified time.
2. Change the value. Numbers use numeric inputs, flags use checkboxes or a
   selector, and text lists use one item per line. Nested rule lists support
   selecting one record/item; **Whole list (YAML)** is available for advanced edits.
3. Click **Validate and preview**. Validation uses temporary copies of all six
   configs and the grader's existing `GradingContext.load` validation. Errors
   prevent saving. The diff shows parsed values before and after, without noise
   from quote styles and comments.
4. Review the diff and click **Save validated changes**. This saves exactly the
   previewed changes. Further form edits need another **Validate and preview**.
5. A success message shows the saved path and backup path. **Reload / reset**
   discards unsaved edits and loads current files again.

Nothing saves automatically. Make one setting/list change at a time, preview it,
and save it before editing another setting. The raw YAML expander is read only.
Normal grading commands pick up saved configuration on their next run.

## Editable configuration

| File | Settings available |
|---|---|
| `profile.yml` | Experience range, active clearance (yes/no/unknown), capability strengths including clouds and domain experience, explicit atomic strengths and notes, existing growth paths |
| `roles.yml` | Existing TARGET/SECONDARY/BRIDGE/SURVIVAL/WRONG title and evidence term groups, exclusions, lane signal weights and flags, existing eligibility conditions, specialization vocabulary |
| `requirements.yml` | Required/preferred headings and patterns, lead/seniority/ownership terms and ranks, equivalences, existing clearance and experience interpretation policy |
| `weights.yml` | Existing weights, penalties, fit/decision rules and their thresholds, lane caps, learning and confidence settings |
| `market_skills.yml` | Existing technology alias lists |
| `skills.yml` | Existing capability terms, atomic links and term references |

In profile **skills** and **atomic_skills**, the setting selector also includes
existing vocabulary entries not yet in the profile. Choose one to add a strength.
Domain experience uses the existing capability vocabulary (for example,
`healthcare_supply_chain`); the editor does not invent new profile fields. Broad
capability and explicit atomic proficiency are separate settings.

Existing mapping keys and rule IDs cannot be deleted. Set a strength to `0` or
a rule's existing `active` flag to `false` instead. Term-list items can be added
and removed. New arbitrary top-level sections and a new taxonomy-entry workflow
are intentionally omitted; this utility edits the current config schema.

## Validation and file safety

Validation rejects malformed YAML, duplicate keys, deleted mapping/rule keys,
numeric-to-text/boolean changes, list-to-scalar changes, invalid experience
ranges, unknown atomic references, invalid policy rules and invalid regular
expressions. Existing loader checks are reused for cross-file references and
policy bounds. This validates configuration, not the quality of a calibration
choice; a syntactically valid threshold can still produce undesirable grades.

Each save creates an exact copy of the previous bytes under:

```text
data/outputs/config-backups/profile.20261018T200000.123456Z.a1b2c3d4.yml
```

The name contains the config stem, UTC timestamp and unique suffix. Backups are
never reused, and `data/outputs/` is already Git-ignored. Backup and staged write
are flushed before an atomic replacement of the original. A failed backup
prevents the overwrite. A failed replacement leaves the original and backup
available and cleans up the temporary write.

Saving refuses a preview if any of the six source files has changed since load.
Reload and preview again in that case. This is an optimistic check for a local
single-user utility, not a filesystem locking service. Config symlinks are not
supported.

Only the selected value's text is rewritten; surrounding comments, line endings,
and unrelated settings are preserved. Edited collections use valid YAML flow
syntax and may change local formatting. Editing an anchor owner also updates
its shared aliases, which appear in the diff. A collection that defines nested
anchors used elsewhere must be edited through its individual items instead.

To restore, stop editing and copy the desired backup over its corresponding
file in `configs/`, then reload. There is no automatic backup pruning or restore UI.

Focused tests (temporary copies only):

```powershell
python -m unittest tests.test_config_editor -v
```
