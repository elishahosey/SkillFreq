# Local calibration/config editor

From the repository root, activate the existing SkillFreq Python environment:

```powershell
python -m streamlit run scripts/config_editor.py --server.address 127.0.0.1
```

Streamlit and PyYAML are already dependencies. No database, API, AI calls, or
background jobs are needed.

## Search, edit, preview, save

**Quick Edit** opens by default. Search for a technology, capability, title,
lane rule, seniority term, clearance setting, or policy concept. Results show
the owning file; you do not need to choose a YAML file first.

For example, search **Terraform** and select its `profile.yml` result. Familiarity,
growth priority, adjacent concepts, and notes appear together. Change priority
and select an adjacent concept, then click **Validate and preview**:

```text
profile.growth_paths.Terraform.priority: 0.35 -> 0.5
profile.growth_paths.Terraform.adjacent_concepts: + "aws"
```

Only changed values appear. **Advanced: full YAML diff** shows the exact text
changes, including formatting and any shared-anchor effects. Click **Save validated
changes** to write exactly the preview. Further edits need another preview.
Nothing saves automatically. Navigation to another setting clears the pending
preview; **Reload / reset** discards drafts and reloads the files.

Saving shows the original path and backup path. Normal grading commands pick up
the saved configuration on their next run. The editor does not run calibration,
interpret job grades, recommend changes, or decide what the profile should be.

## Config issue or grader issue?

The decision rule appears at the top of every view:

- If changing configuration fixes the behavior without changing the intended
  algorithm, it is probably a config issue.
- If the algorithm must parse, resolve, score, or apply that configuration
  differently, it is probably a grader issue.

Each setting also has guidance specific to its owner. A missing networking
synonym may be a vocabulary edit. A synonym already present but undetected needs
extractor investigation. Incorrect candidate experience belongs in the profile;
`years_required = 200` or correct preferred patterns being ignored belongs in
parser/code work. Correct role rules ignored by eligibility need lane logic work.
Do not compensate for these defects with weights or thresholds.

**Requires grader/code change:** interpretation/application of correct config,
new algorithmic behavior, or a setting that does not exist in the current schema.
The editor does not move implementation constants into YAML.

## Views and ownership

| View / file | Focused edits | Advanced-only |
|---|---|---|
| Profile / `profile.yml` | Experience range, active clearance (yes/no/unknown), capability strengths, atomic familiarity, existing growth priority/adjacent concepts, notes | Other structural edits |
| Skills / Vocabulary / `skills.yml` | Existing capability terms; atomic links and term refs are visible | Atomic links, term refs, structural changes |
| Skills / Vocabulary / `market_skills.yml` | Existing technology alias lists | New taxonomy structures |
| Role Lanes / `roles.yml` | Role vocabulary text, plain term lists, lane-rule lane/active/weight | Regexes, reference lists, eligibility conditions, title overrides and resume mappings with references, scope and exclusion mechanics |
| Seniority / Requirements / Hard Filters / `requirements.yml` | Seniority ranks/terms, lead lists, blocker lists/count, maximum experience years, explicit equivalences | Required/preferred, ownership, years and clearance regexes |
| Advanced Policy / `weights.yml` | No normal quick-edit weights | Capability weights, caps, penalties, experience-gap/fit/quality/decision rules and other scoring policy |
| Advanced Policy / `resume_signal.yml` | Search and inspection of resume evidence domains/references | Edits to resume evidence mappings |

Role rules show their ID, lane, scope, active state, weight and pattern/group.
Complex search results require **Open in Advanced** before editing. Advanced
Policy keeps weights and complex rules visibly separate from personal edits.
**Advanced YAML** is a secondary file/section/setting navigator and raw-value
escape hatch, not a whole-file editor. Roles are never presented as one giant
editable document.

Atomic familiarity and growth priority use 0–1. Broad capability strength may
exceed 1 where the current profile supports it. Cloud/domain evidence uses the
existing capability vocabulary, not new profile fields. Known vocabulary entries
can be added to profile strengths. Existing growth paths have a focused form;
creating new growth paths is intentionally left to manual YAML authoring. Equivalences use approved atomic
and capability selections and are never inferred automatically.

## Validation and safe saves

Validation stages a temporary copy of all seven configs, then calls the existing
`GradingContext.load`, which reuses `read_config`, `load_roles`,
`validate_grading_settings`, skill dictionary, profile, weights and market taxonomy
loaders. Resume aliases use the existing `resolve_terms` with the proposed bundle,
so edits cannot silently leave broken resume references to a removed term.

Small editor safeguards additionally reject duplicate YAML keys, deletion of
existing mapping/rule identities, changed field types, nonfinite/negative profile
strengths, invalid seniority rank/term shapes, invalid maximum experience years,
and malformed regexes. Existing loader checks cover numeric policy bounds,
experience ranges, valid lanes/rules, duplicate rule IDs and cross-file references.
A validation failure prevents backup and write. These checks establish structural
validity, not whether a policy choice will improve grading.

Existing mapping keys/rule IDs cannot be deleted. Set a strength to 0 or an
existing rule's active flag to false. List terms can be added/removed, but removing
a referenced term will fail validation until the references are addressed. There
is no multi-file transaction workflow; coordinated migrations remain code work.

Every save revalidates and checks that **all seven files** still match the loaded
snapshot. It then makes an exact backup of the selected file under:

```text
data/outputs/config-backups/profile.20261018T200000.123456Z.a1b2c3d4.yml
```

The UTC timestamp plus unique suffix prevents backup reuse. The backup and staged
write are flushed before atomic replacement. Backup failure prevents overwrite;
replacement failure preserves the original and cleans up the staged file. A stale
preview requires reload and a fresh preview. This is a local optimistic check,
not a locking service. Config symlinks are unsupported.

Only edited value spans are rewritten. Surrounding comments and unrelated text
are preserved; edited collections use YAML flow syntax. Shared anchors may affect
multiple paths, all of which appear in the semantic diff. Collections defining
nested anchors used elsewhere must be edited through individual items.

To restore, stop editing, copy the chosen backup over its original config, and
reload. No restore UI or automatic backup pruning is included.

Focused tests use temporary copies only:

```powershell
python -m unittest tests.test_config_editor -v
```
