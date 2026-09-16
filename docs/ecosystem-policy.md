# Ecosystem concentration policy

Policy belongs in configuration. Mechanism belongs in Python.

Vendor names are evidence, not verdicts. The current policy separates ordinary
platform use, proprietary specialization, platform ownership, transferable work,
candidate fit and the application decision.

## Configuration owners

`configs/roles.yml` owns these controlled term groups:

| Group | Meaning |
|---|---|
| `ecosystem.products` | Existing enterprise/integration ecosystems such as Boomi, Informatica, Workday, Salesforce and ServiceNow |
| `ecosystem.ownership` | Ownership/administration evidence, retaining previous MDM and platform guards |
| `ecosystem.specialization` | Proprietary delivery components and experience: AtomSphere/Molecules, MDM Hub components, Workday Studio/EIB, Salesforce components, ServiceNow development artifacts |
| `ecosystem.administration` | System upgrades, platform security/performance, environment ownership and configuration |
| `ecosystem.admin_titles` | Generic administrator/admin title evidence; vendor context and responsibilities must corroborate it |
| `ecosystem.transferable` | SQL/database work, Python, ETL, data pipelines, APIs, formats, mapping, quality and warehousing, referencing existing concepts/atomic aliases |
| `ecosystem.data_platforms` | Palantir plus existing Snowflake, Databricks, Redshift and BigQuery atomic references |
| `ecosystem.data_specialization` | Foundry delivery components, Snowpipe/Snowpark; recorded independently of enterprise specialization |

These are role-evidence categories, not another atomic taxonomy. No market skill,
alias table or candidate proficiency was added. AtomSphere and Molecule terminology
moved from ownership into specialization: knowing a runtime name does not prove
that the role owns it. Existing explicit ownership protections remain active.

Title, specialization and ownership signals contribute zero lane points on their
own. They supply facts to the configured eligibility rules. Data-platform usage
does not receive the enterprise usage penalty. No category service or product
registry was introduced; ordinary term groups express the distinction.

## Current thresholds

Rules run in descending priority, using the existing condition/action evaluator.

1. `transferable_data_counterweight`: eight distinct transferable phrases establish
   the strong counterweight. This count is not a percentage of responsibilities.
2. `ecosystem_specialization_evidence`: at least two specialization phrases plus an
   enterprise product in the title **or** description establish specialization.
3. `ecosystem_ownership_evidence`: vendor context plus title-and-ownership evidence,
   or two ownership phrases, preserves the previous explicit ownership gate.
4. `ecosystem_admin_evidence`: admin title, admin responsibilities and vendor context
   require either a vendor-specific title or limited transferable evidence with
   at least two administration phrases. A mixed DBA/data role is not automatically
   a vendor administrator because Salesforce appears in one responsibility.
5. `ecosystem_concentration_evidence`: ownership or admin identity establishes
   concentration. Specialization establishes concentration when corroborated by a
   vendor title, at least six specialization phrases, or a weak transfer counterweight.
6. The existing `ecosystem_identity_guard` removes TARGET when concentration is true.
   It does not invent SECONDARY/BRIDGE eligibility; existing positive lane evidence
   and scores choose the result.
7. Low-transfer admin identity becomes WRONG. Four specialization phrases with at
   most three transferable phrases also become WRONG when concentrated. Strong
   transferable specialist work can remain SECONDARY and receive manual review.

This allows a broad Data Engineer using a vendor tool to remain TARGET, while a
vendor developer with proprietary delivery responsibilities can become SECONDARY.
A generic title can still be downgraded when the responsibilities are highly
specialized. A title-only vendor mention is insufficient.

`configs/weights.yml` consumes the same declared flags:

- Existing enterprise usage penalty: 3 fit points.
- Explicit ownership gate: existing 30-point penalty and blocker.
- Specialization with strong transfer: 8 fit points and a review flag.
- Specialization with limited transfer: 18 fit points and a review flag.
- Admin identity: explicit administration blocker.

Specialization penalties are not stacked on the ownership penalty. Existing
seniority, requirement and lane-cap policies still apply independently. Lane,
fit quality and apply decision remain separate; a specialist can have substantial
technical fit while requiring review. No decision thresholds changed in this pass.

## Change your preferences without Python

- **Accept Boomi specialization:** edit its entries in `ecosystem.specialization`
  (AtomSphere/Molecules, Boomi runtime/deployment and direct-experience wording).
  Retain or remove the corresponding ownership terms according to whether you
  also want platform administration. Removing the vendor name alone is insufficient
  when the job independently evidences another ecosystem.
- **Tolerate more specialization broadly:** raise the two-hit threshold in
  `ecosystem_specialization_evidence`, or adjust the title/transfer conditions in
  `ecosystem_concentration_evidence`.
- **Preserve TARGET despite concentration:** change or disable the existing
  `ecosystem_identity_guard`. Fit penalties and review flags remain independent;
  adjust them separately if appropriate.
- **Change the transfer counterweight:** edit `ecosystem.transferable` and the
  eight-hit threshold in `transferable_data_counterweight`.
- **Change penalties:** edit the 8/18-point actions in `weights.yml`, or replace a
  blocker action with a review flag when that better reflects your policy.
- **Evaluate a modern platform more strictly:** author a rule using
  `hits.data_platform_title`, `hits.data_platform_specialization` and ownership or
  transfer evidence. Do not automatically copy enterprise-platform policy onto it.

Terms were drawn from the actual postings. A generic word such as “Studio” or
“connectors” is not sufficient on its own. Numeric years tied to individual
products are not newly parsed here: direct-experience phrases are auditable
specialization evidence, not proof of a calibrated minimum-years gate. Preferred
and required wording can still need manual review.

## Generic mechanism change

The existing lane evaluator already derives Boolean flags. `LaneResult.policy_flags`
now carries the configured flags to grading, where validated `flags.<name>` fields
are read-only inputs to fit/decision evaluation. `DeterministicGrade.policy_flags`
records them alongside the actual triggering conditions/actions.

This small change avoids repeating concentration thresholds in both role and fit
policy. It adds no operators, actions, executable YAML, vendor branches or framework.
Unknown cross-stage flags fail configuration validation. Flags and their provenance
are saved in existing JSON audit output and the versioned configuration snapshot.

## Files and verification

Changed grading files: `skillfreq/score/lane_classifier.py`,
`skillfreq/score/grading.py`, `skillfreq/configuration.py`. Policy changes:
`configs/roles.yml`, `configs/weights.yml`. The profile, SQL concepts, market taxonomy,
DB schema, prevalence calculation, search-context handling and domain guards are
preserved.

Added `tests/test_ecosystem_calibration.py` and 12 fixtures in
`tests/fixtures/ecosystem_jobs.yml`, covering all seven requested cases, modern
platforms, absent/repeated vendor titles, strong-transfer specialists and mixed
database administration. The suite also verifies shared flag audit, configuration-only
eligibility changes and invalid cross-stage flag rejection. Existing domain tests
continue to protect SQL Server/PostgreSQL, Oracle PL/SQL, QA/security and flight controls.

All 62 tests pass when the two PostgreSQL tests are enabled; the normal run has 60
passing tests and two opt-in skips. PostgreSQL tests use rollback transactions.

Reporting additions: `scripts/regrade_saved_cohort.py` reuses the existing pipeline
functions with frozen DB-export inputs and one prevalence read;
`scripts/compare_ecosystem_calibration.py` verifies identical identities/text and
reports aggregate changes, 20+ examples and all five retained TARGET integration jobs.
The shared report loader in `scripts/compare_domain_calibration.py` exposes actual
fit-rule IDs and flags. Reports never manufacture rule explanations.

```powershell
python scripts/regrade_saved_cohort.py
python scripts/compare_ecosystem_calibration.py
```

The separate result is `data/outputs/results-db-90-days-ecosystem.csv` with its
`.grading.yml` snapshot. This exact-cohort replay intentionally uses the previous
DB export because another rolling 90-day DB query can change membership after
midnight. Fresh operational grading still uses `grade-db` normally.

See [the measured comparison](ecosystem-calibration-comparison.md). The previous
domain report remains a historical comparison rather than being overwritten.
