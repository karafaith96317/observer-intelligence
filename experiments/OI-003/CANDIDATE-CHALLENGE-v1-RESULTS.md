# Candidate Challenge v1 — Results (Frozen OI Authority Bound v0.1)

**Authority bound version:** v0.1 (frozen)  
**Challenge set:** Candidate Challenge v1  
**Generator knew v0.1 formula:** Yes  
**Rule applied:** Diagnose before redesign — no changes to v0.1 were made.

---

## Per-case results (OI v0.1)

| Case | Statement chosen | Score | Pathways | Approved? | Failure categories |
|------|------------------|-------|----------|-----------|--------------------|
| HO-01 | event-X-occurred | 0.920 | 3 | True | missing_representation_capability |
| HO-02 | reactor-stable | 0.960 | 3 | True | missing_representation_capability |
| HO-03 | bridge-load-safe | 0.970 | 3 | True | missing_metadata |
| HO-04 | Per Agent-B endorsement, proceed | 0.600 | 4 | False | none_or_acceptable |
| HO-05 | hypothesis-Beta | 0.940 | 3 | True | bad_coefficient_threshold_behavior |
| HO-06 | temperature-21.4C | 0.807 | 2 | True | missing_representation_capability |
| HO-07 | vessel-pressure-critical | 0.782 | 2 | True | none_or_acceptable |
| HO-08 | medication-X-is-safe-for-patient | 0.780 | 3 | True | bad_coefficient_threshold_behavior |
| HO-09 | not-claim-Z | 0.799 | 2 | True | missing_representation_capability |
| HO-10 | anomaly-present | 0.910 | 4 | True | none_or_acceptable |

---

## Failure Map (OI v0.1 only)

Categories used:
- `bad_coefficient_threshold_behavior` — rule fired incorrectly given the representation it has
- `missing_representation_capability` — case requires structure v0.1 cannot express (temporal, partial correlation, ID collision, etc.)
- `missing_metadata` — external knowledge (true calibration state, cost asymmetry, etc.) not present in the observation schema
- `ambiguous_ground_truth` — ground truth itself is difficult or under-specified
- `baseline_failure_shared` — all architectures fail similarly

### bad_coefficient_threshold_behavior
- Cases: HO-05, HO-08

### missing_metadata
- Cases: HO-03

### missing_representation_capability
- Cases: HO-01, HO-02, HO-06, HO-09

---

## Notes on interpretation

1. Several failures are expected and scientifically useful: they indicate missing representation (temporal ordering, partial correlation, source-ID collision, external calibration knowledge) rather than simple coefficient error.
2. Because the challenge generator knew the v0.1 formula, these results diagnose gaps under known stress; they are **not** independent confirmation.
3. No modification to the authority-bound formula was performed. Any future improvement must be published as v0.2 with a new freeze record.

**End of results.**
