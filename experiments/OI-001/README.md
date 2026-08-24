# OI-001 — Observer Disagreement & Reconciliation

## Question

Does provenance-preserving multi-observer reconciliation improve calibration and error detection compared with naive majority voting or single-observer decision making?

## Hypothesis

A reconciliation system that tracks observer independence, provenance, confidence, and known failure modes will outperform simple aggregation when evidence is incomplete, correlated, or adversarially manipulated.

## Minimal experimental design

Create a synthetic environment with a hidden ground-truth state. Multiple observers receive partially overlapping and intentionally imperfect views.

Conditions should include:

1. independent noisy observers
2. correlated observers sharing the same erroneous source
3. one high-confidence but unreliable observer
4. one adversarial observer
5. missing observations
6. conflicting but individually plausible evidence

Compare:

- single-observer selection
- majority vote
- confidence-weighted vote
- provenance-aware OI reconciliation

## Primary metrics

- ground-truth accuracy
- Brier score / calibration error
- false-confidence rate
- contradiction detection rate
- adversarial robustness
- proportion of cases correctly left unresolved

## Falsification criterion

The OI approach is not supported if provenance-aware reconciliation fails to improve calibration, error detection, or adversarial robustness under the conditions where those mechanisms are predicted to help.

## Important principle

**Correctly saying “unresolved” can be superior to confidently selecting an unsupported answer.**
