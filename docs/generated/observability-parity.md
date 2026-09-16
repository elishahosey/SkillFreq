# Frozen-cohort behavioral parity

Before: `data\outputs\results-db-90-days-ecosystem.csv`
After: `data\outputs\results-db-90-days-observability.csv`

The replay used the same 8,692 input rows and the same policy configuration. New grading/implementation hashes are expected; behavior fields below are compared.

| Metric | Before | After |
|---|---:|---:|
| jobs | 8692 | 8692 |
| average_fit | 31.211 | 31.211 |
| average_learning | 2.451 | 2.451 |
| nonzero_learning | 886 | 886 |
| ai_review_rate | 0.3737 | 0.3737 |

## lane_counts

| Value | Before | After |
|---|---:|---:|
| bridge_lane | 700 | 700 |
| secondary_lane | 1472 | 1472 |
| target_lane | 264 | 264 |
| wrong_lane | 6256 | 6256 |

## apply_counts

| Value | Before | After |
|---|---:|---:|
| apply_now | 99 | 99 |
| manual_review | 2257 | 2257 |
| skip | 6336 | 6336 |

## fit_quality_counts

| Value | Before | After |
|---|---:|---:|
| good_fit | 861 | 861 |
| possible_fit | 1506 | 1506 |
| weak_fit | 6325 | 6325 |

## Field-level drift

Changed field observations: 0
Changed jobs: 0

No behavior fields changed.
