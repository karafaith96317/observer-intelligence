# Observer Intelligence v0.2.1 — Hardened Protocol Baseline Candidate

**Date recorded:** 2026-08-27

## Working definition

Observer Intelligence (OI) is an epistemic-governance architecture that preserves the lineage of evidence, reasoning, disagreement, and authority across independently generated observations, then calibrates those observers against outcomes over time.

## Three lineage graphs

1. **Provenance lineage:** source -> evidence -> observation/grounding.
2. **Epistemic lineage:** evidence -> proposition -> support/contradiction/qualification/dependency relations.
3. **Authority lineage:** observation -> inference -> evaluation -> recommendation -> authorization -> execution.

## Core invariant

> Assertion, verification, reconciliation, authorization, and execution should remain separable functions wherever self-validation would create an epistemic or operational conflict of interest.

This means:

- observers do not certify their own truth;
- shadow observers do not certify their own attacks;
- citing authentic evidence does not certify its relevance;
- unsupported contradicting claims do not automatically demote supported claims;
- authorizers do not gain execution permission merely by issuing a recommendation;
- archive generation and archive verification are separate operations;
- declared observer isolation is checked against the evidence/proposition references submitted later.

## v0.2.1 hardening changes

- Directed contradiction semantics.
- Orthogonal `EpistemicCategory` and `EvidenceState`.
- Explicit evidence-to-proposition grounding relations.
- Grounded != Supported: `INSUFFICIENT_FOR` remains unresolved.
- Adversarial attacks are submitted unadjudicated and must establish relevant counterevidence.
- Observer context manifests lock declared evidence/prior-proposition access before claims are registered.
- Grounding and dependency references are rejected when they exceed the declared isolation envelope.
- Subjective confidence remains metadata and is not used as a truth threshold.
- Authorization uses an Ed25519 verification interface and persistent nonce consumption.
- Replay protection survives engine restart when the same nonce database is reused.
- Append-only blocks advance the previous hash and include sequence numbers.
- `verify_chain()` independently checks sequence, parent hashes, run identity, and payload integrity.
- External timestamp anchoring remains **anchor-ready**, not verified, until an external proof is actually validated.

## Falsifiable benchmark fixtures

The repository test suite compares OI v0.2.1 with a deliberately simple confidence-weighted majority baseline. The baseline is a comparison condition only; it is **not** claimed to represent all multi-agent systems.

Current fixtures:

1. **Consensus/Sybil bias:** three confident positive agents versus one evidence-grounded counter-observer.
2. **Semantic leap:** authentic latency evidence used to justify an unrelated security conclusion.
3. **Directed contradiction asymmetry:** supported challenger targets a fragile claim without becoming contested solely because it challenges.
4. **Observer isolation breach:** observer cites evidence outside its locked manifest.
5. **Irrelevant counterevidence:** authentic but irrelevant evidence must not make a shadow attack successful.
6. **Unsupported contradiction:** an unresolved attacking proposition must not automatically demote a supported target.
7. **Replay after restart:** a previously consumed authorization nonce must remain rejected after engine reconstruction.
8. **Signature mutation:** alteration of scope/payload must prevent authorization.
9. **Hash-chain tamper:** mutation of an archived payload must cause chain verification failure.
10. **Monte Carlo telemetry perturbation:** 1,000 seeded trials of packet loss and jitter compare naive optimistic authorization with OI unresolved/contested containment.

## Evidence discipline

Predicted benchmark numbers are not recorded as empirical results. Any percentage such as a projected baseline failure rate or OI safety rate remains a hypothesis until produced by an executed, reproducible test run. Test outputs should be stored with:

- code commit SHA;
- random seed;
- environment/dependency versions;
- iteration count;
- raw result artifact;
- timestamp;
- pass/fail criteria defined before execution.

## Baseline-candidate freeze criterion

Treat v0.2.1 as the hardened baseline only after the test suite executes successfully and the results are preserved. At minimum, the following must pass:

- isolation breach rejected;
- irrelevant counterevidence does not win;
- unsupported contradiction does not automatically demote a supported target;
- replay rejected after restart;
- signature/payload mutation fails authorization;
- archive tampering fails independent chain verification.

After baseline freeze, architectural expansion should pause long enough to run OI-001/OI-002 empirical comparisons against conventional synthesis/aggregation methods.

## Central research question

Does preserving independent observation, provenance, disagreement, and separated authority measurably improve reasoning reliability, calibration, error detection, adversarial robustness, or failure containment compared with simpler synthesis/aggregation approaches under the conditions where OI predicts an advantage?
