# Five-job market spot check

Scope: the five reviewed jobs from the refreshed 2026-10-08 population, investigated
on `refactor/pre-ai-grading-engine`. This is not a new calibration batch.

The original implementation reproduces the reported results with grading version
`5e01f710d103c4c0`. The two exports referenced by the review workbook have identical
grading results for these jobs. Their complete grade JSON differs only in
`market_context` provenance. This review provides no evidence of OLD-to-NEW
improvement. No saved export or review workbook was overwritten.

Sources: `data/outputs/comparison-requirement-semantics-refreshed-2026-10-09/new.csv`
and `data/outputs/results-db-2026-10-08_17-08-54-691977.csv`. The five original
titles/descriptions are retained in `tests/fixtures/market_spot_check_jobs.yml`
so regression tests do not depend on ignored local exports or a live database.

## Integration Engineer: specialization evidence was missing

Job `in-12212552d5d9b1fa`, Integration Engineer with Integration Tool Experience.
Classification: **representation issue in the configured specialization vocabulary**,
not a scoring arithmetic bug or a reason to lower global scores.

`calculate_fit_score` in `skillfreq/score/grading.py` computes weighted candidate
coverage across recognized capability concepts. Each concept contributes once;
repeated mentions do not repeatedly add fit points. It clips profile strengths to
one. The matched concepts have total weight 34 and weighted covered strength 30.2:

| Component | Fit contribution |
|---|---:|
| Capability coverage, `100 * 30.2 / 34` | 88.823529… |
| Missing preferred AWS | -0.5 |
| Missing preferred Google Cloud | -0.5 |
| Enterprise ecosystem usage | -3 |
| Total, rounded | **84.82** |

No required atomic/group penalty, ownership penalty, lead penalty, or experience-gap
penalty fires. Three required years fit the configured candidate range of 3–4.
`good_fit` starts at 80; an otherwise ungated TARGET score of at least 78 produces
`apply_now` under `configs/weights.yml`.

The lane calculation is separate. Seven core-data phrases contribute 36 TARGET
points after the six-hit cap. The integration title, data mapping, and SQL satisfy
`integration_data_evidence` and `supported_integration_target`, adding TARGET
eligibility and 24 points. TARGET wins with 60 versus SECONDARY 26, BRIDGE 24 and
WRONG 8. This supports keeping TARGET under the existing integration policy.

There is exactly one `platform_heavy_terms` match: **cloud infrastructure**. It
appears in the employer's broad practice description. It adds eight WRONG lane
points, not a direct fit deduction. This category can affect eligibility and some
contradiction rules at higher counts; here no contradiction rule fires. It does
not justify a new platform penalty for this job. Heuristic confidence is
`0.3 + 0.35 * (60 - 26) / 60 + 0.25 = 0.748` after rounding.

Cloud matches are not the source of positive inflation. AWS has capability
strength zero, Azure has 0.8, and Google Cloud has no positive capability entry
in this calculation. AWS and Google Cloud also incur the preferred-gap penalties
above. Atomic matches mean technologies found in the posting, not proven candidate
proficiency. Capability coverage spans the description rather than giving extra
bonuses for preferred matches.

The material omission is vendor-specific required work:

- Proficiency with **core Boomi components**, including connectors and process building.
- Custom Groovy/JavaScript **code within the Boomi environment**.

Neither matched the old `ecosystem.specialization` vocabulary. Boomi, MuleSoft,
Informatica and other product mentions supplied enterprise context, but specialization
had zero hits. The job therefore received only the three-point usage penalty.
Required Boomi/Groovy/JavaScript competence is also outside the controlled atomic
gap vocabulary; an empty atomic-gap list does not certify all qualifications.
Likewise, matching Azure does not independently verify a cloud certification or
product-specific years of experience. No candidate qualifications were inferred
or changed in this patch.

The existing [ecosystem policy](ecosystem-policy.md) already calls for an eight-point
deduction and manual-review flag when two proprietary specialization cues coexist
with strong transferable evidence. The smallest correction adds the two scoped
phrases above to that vocabulary. It adds no vendor-title exception, atomic skill,
threshold, weight, or new evaluator behavior. Generic “components,” “environment,”
and product mentions do not qualify; repeating one cue still counts as one.

The corrected result is **target_lane / 76.82 / possible_fit / manual_review**,
with `ecosystem_specialization_review`. Strong transferable evidence remains true.
Concentration remains false: there is no vendor title, six specialization cues,
or weak transfer counterweight. Thus TARGET is preserved, ownership is not inferred,
and the existing eight-point fit deduction is the only numerical change.

## AI & Automation Intern: soft exclusion evidence becomes a hard decision

Job `in-85165dc0ecbc4c68`, AI & Automation Development Intern.
Classification: **policy/tuning issue**, with an overly categorical representation
of a mixed result. No evaluator bug was found; no behavior change is made here.

`wrong_desc_terms` matches **prompt engineering**, **AI agents**, and **machine
learning**, at 12 points per distinct phrase: **36 WRONG points**. Repeated AI-agent
mentions do not add more points. Prompt engineering and machine learning occur
in a preferred-familiarity sentence. AI agents also occurs in duties and learning
topics. The description-scoped role signal does not distinguish these contexts
or required versus preferred wording.

Positive evidence is recognized:

| Lane | Raw points | Eligible? |
|---|---:|---|
| TARGET | 24 | No |
| SECONDARY | 12 | No |
| BRIDGE | 22 | Yes |
| WRONG | 36 | Yes |

`data_ok`, `bridge_ok`, and `data_identity` are true. TARGET still requires an
appropriate title/domain anchor; the intern title supplies none. SECONDARY
requires independent technical identity, database development, or substantive
integration/backend evidence. The current phrases/patterns do not recognize its
workflow-development duties as that evidence. SQL/Python/API overlap alone is
deliberately insufficient, protecting unrelated occupations.

Crucially, **`description_exclusion_guard` does not fire**, because `data_ok` is true.
BRIDGE is already eligible. WRONG simply wins 36 to 22. There is no hard title
exclusion or hard-exclusion confidence override for this posting.

`positive_and_exclusion_signals` lowers confidence by 0.22. With lane margin
`(36 - 22) / 36`, the result is
`0.3 + 0.35 * 14 / 36 + 0.25 - 0.22 = 0.466` after rounding.
Both that contradiction and low confidence request AI review.

Then the existing `wrong_role_gate` converts any WRONG winner into
`wrong_role_identity`, and the WRONG lane cap reduces pre-cap fit 89.66 to 15.
`configured_hard_blocker` takes precedence over `ambiguous_role_review`, producing
`skip`. The AI-review flag requests review but does not execute AI or override
the deterministic blocker.

The mechanism distinguishes this case from Robotics/QA/DevOps in its evidence,
eligibility and confidence, but collapses them to the same final lane/blocker.
BRIDGE plus manual review is a reasonable policy alternative for this actual
workflow-development posting. SECONDARY would additionally require broader
recognition of independent software-work evidence; adding that alone would not
overcome the 36 WRONG points.

Changing the outcome would require an explicit policy for mixed AI/software
automation work: which responsibilities establish adjacency, and when soft
description exclusions should yield to review. Lowering the wrong-term weight,
removing AI terms, or promoting every low-confidence WRONG result would also
affect other occupations. Existing policy explicitly includes these AI phrases
as exclusions. One neutral review does not justify that broader change. The
intern remains **wrong_lane / 15 / skip**, with AI review required; the focused
test records this deferred policy choice, not an assertion that it is ideal.

## Regression protections and validation

| Job | Preserved result | Relevant protections |
|---|---|---|
| `in-7fb8f90cfca11195`, Robotics Engineer | WRONG / 15 / skip | Hard hardware title identity |
| `li-4459650362`, Quality Assurance Supervisor | WRONG / 15 / skip | Hard wrong-title evidence and lead review flag |
| `li-4446676420`, Lead DevOps Engineer (GovCloud) | WRONG / 15 / skip | Hard operational identity, lead/seniority, four-year experience gap, clearance review |

The DevOps replay records clearance eligibility for review, not an active-clearance
blocker. Its hard role exclusion independently keeps it skipped. These distinctions
are retained rather than claiming every signal is a separate hard blocker.

Focused tests compare complete grades with and without the two vocabulary entries:
all three protected jobs and the intern are unchanged. They also verify the exact
Integration Engineer score transition, preservation of TARGET and requirement gaps,
and no specialization from incidental usage or repetition of one cue.

The change can affect other postings containing both scoped Boomi responsibilities,
which is its intended generalization. It does not rescue any role or weaken any
exclusion. No full-population tuning or rerun was performed.

Validation completed with `python -m unittest discover -s tests -q`: 138 tests
discovered, 136 passed, and two opt-in PostgreSQL integration tests skipped.
The four new focused tests also pass independently. The suite required a run
outside the sandbox because Windows denied replacement of temporary workbooks
inside it. `git diff --check` passes. The updated grading version is
`434d61fbf4dfe7b9`; the reviewed historical version remains `5e01f710d103c4c0`.
