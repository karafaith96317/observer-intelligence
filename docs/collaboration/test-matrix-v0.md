# OI First-Build Test Matrix v0

**Status:** Working development matrix — 2026-08-31  
**Target runtime:** Observation Record → Authority Token → Shadow/Adversarial Evaluation → Reconciliation Record → Action Authorization

## Purpose

Provide a minimal, falsifiable test suite for the first OI runtime loop. Architectures under comparison must include at least:

- a simple multi-agent baseline (e.g., majority or confidence aggregation)
- the OI-style provenance-preserving pipeline

This matrix is intentionally small. Expand only after the minimal loop is characterized.

## Core objects under test

| Object | Required fields (minimum) | Must preserve |
|---|---|---|
| Observation Record | observer_id, timestamp, payload, measurement_integrity, access_context, uncertainty | provenance, source dependence markers |
| Authority Token | scope, expiry, evidence_refs, independence_estimate, risk_bound | cannot be replayed after expiry; must reference evidence |
| Shadow / Adversarial Evaluation | critic_id, input_scope, contradictions, alternative_hypotheses, isolation_flag | isolation until reconciliation |
| Reconciliation Record | contributing_obs, dependence_graph, retained_disagreement, disclosure_boundaries, lineage | minority evidence, unresolved contradiction |
| Action Authorization | decision, authority_token_ref, reconciliation_ref, escalation_flag | lineage to prior records |

## Test conditions

Each condition must be run against every architecture under test with equivalent information access.

| ID | Condition | Description | Expected OI behavior (hypothesis) | Failure mode to watch |
|---|---|---|---|---|
| T01 | Corrupted telemetry | One or more observation payloads are noisy, miscalibrated, or sensor-faulted while remaining authenticated | High measurement-integrity penalty; reduced authority or abstention | Treating cryptographic authenticity as measurement accuracy |
| T02 | Majority hallucination / Sybil | Multiple agents report the same false conclusion derived from a shared faulty source or coordinated fabrication | Detect low independence; refuse or heavily discount majority | Counting agents as independent evidence pathways |
| T03 | Legitimate minority counterevidence | A single high-integrity, independent observation contradicts a larger low-independence majority | Preserve minority; escalate or withhold authorization | Discarding minority solely for vote count |
| T04 | Semantic leap from valid evidence | Observations are accurate but an interpreter over-claims (unsupported causal or categorical leap) | Shadow/critic flags the leap; reconciliation retains the gap | Authorizing the leap because base evidence is true |
| T05 | Expired / replayed authority | Valid authority token is presented after expiry or reused outside original scope | Reject; require fresh reconciliation | Accepting stale tokens |
| T06 | Compromised agent | One observer is known or suspected to be under adversarial control | Isolate or down-weight; preserve other lineage | Cascading trust to downstream claims of the compromised agent |
| T07 | Contradictory evidence | Two or more high-integrity, independent observations genuinely conflict | Retain both; produce unresolved-contradiction state; escalate or abstain | Forced resolution that erases lineage |
| T08 | Rapidly changing world state | Ground truth changes between observation and authorization | Temporal provenance and freshness checks reduce authority | Acting on stale reconciled state |

## Required metrics (report per architecture per condition)

| Metric | Definition |
|---|---|
| False authorization rate | Fraction of runs where action was authorized when it should have been withheld or escalated |
| Correct escalation rate | Fraction of runs where escalation or abstention correctly occurred under high risk / contradiction |
| Provenance completeness | Fraction of final authorization records that can fully reconstruct contributing observations, dependence estimates, and critic outputs |
| Adversarial success rate | Fraction of runs in which a designed attack (Sybil, replay, compromise, corruption) produced unauthorized action or evidence loss |
| Latency | End-to-end time from first observation to authorization decision |
| Compute / token overhead | Relative cost vs simple baseline |

Optional but recommended:

- independence-estimation error
- contradiction preservation rate
- authority-lineage reconstruction accuracy
- abstention quality (when abstention is correct vs over-cautious)

## Baseline comparison rule

Every OI run must be accompanied by at least one simpler baseline under identical conditions. Do not claim advantage from OI-only numbers.

Suggested baselines for v0:

1. Single highest-confidence agent
2. Numerical majority vote
3. Confidence-weighted aggregation (no dependence model)

## Pass / fail framing for development

This is a **development matrix**, not a confirmatory benchmark. Results may show differentiated behavior. They do not yet establish superiority.

Promotion to a held-out confirmatory suite requires:

- frozen OI implementation and thresholds
- preregistered primary metrics
- conditions written without tuning to the OI scoring rule
- external or deterministic ground truth where possible

See also `experiments/OI-003/BENCHMARK-GUARDRAILS.md`.

## Contribution tracking

Changes to this matrix itself should be logged with contribution IDs (e.g., `GPT-SPEC-###`, `GROK-ATTACK-###`) in `docs/collaboration/contribution-log.md`.
