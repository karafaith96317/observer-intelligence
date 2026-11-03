# Observer Intelligence ↔ Trusted Tier review interface (proposal)

Status: ARCHITECTURAL HYPOTHESIS. Documentation only; no production authorization or empirical validation implied.
Attribution: Kara Faith Sypen — Trusted Tier conceptual design; review and implementation contributions to be recorded separately.

## Separation of duties
Trusted Tier / ERA owns access requests, voting, expiry, revocation and enforcement. OI independently examines provenance, uncertainty, disagreement, conflict-of-interest, and adversarial signals. **OI is not a voting system and must never turn agreement into truth or independently issue privileges.**

## Reflected-pyramid review semantics
- Internal pyramid: participant's self-reported values, commitments and explanations, tagged SELF_REPORT / UNVERIFIED.
- External pyramid: independently attributable behavioral evidence, outcomes, contrary evidence and missing data.
- Trusted Tier band: a time-limited authorization policy decision made outside OI, not a measured frequency or human-worth score.
- Variations in pyramid size and band position are design metaphors until an operational metric is explicitly defined, ethically evaluated and validated.

## Proposed OI input
- request_id, pseudonymous subject_id, requested_scope, requested_duration, policy_version;
- signed reviewer attestation references and independence/conflict declarations;
- evidence references with provenance, timestamps, freshness and disclosure permissions;
- optional previous decision and revocation references.

## Proposed OI output
- review_id, request_id, evidence_status, uncertainty, provenance findings;
- independence/correlation findings, adversarial flags, missing evidence, conflicting hypotheses;
- recommendation: NO_OBJECTION / HOLD_FOR_REVIEW / INSUFFICIENT_EVIDENCE;
- reason codes and links to redacted audit evidence.

A NO_OBJECTION recommendation is **not** proof of trustworthiness and never grants access. Any consequential access decision requires separate authorization and runtime enforcement.

## Red-team fixtures (synthetic)
1. Reviewer collusion / copied evidence: flag non-independence.
2. Replayed signed vote: flag nonce reuse.
3. Fabricated behavioral testimony: label unverified and require provenance.
4. Biometric or meditative 'coherence lock' presented as moral truth: reject inference.
5. Pressure for immediate access: record process violation without diagnosing the applicant.
6. Scope escalation: compare requested and authorized capabilities; flag mismatch.
7. Expired evidence and revocation: flag staleness and request revalidation.
8. Disagreement: preserve minority report and competing hypotheses; do not force convergence.
9. Reviewer retaliation or bias: route to independent appeal, retain privacy safeguards.

## Acceptance criteria before implementation
- Synthetic fixtures for all cases, reproducible tests, no leakage of private identifiers.
- OI advisory output cannot mint an access token or override authorization.
- Existing OI authority-token, nonce and shadow-evaluation tests continue to pass.
- Policy owners explicitly document response to HOLD, including fail-closed enforcement.

No runtime files changed in this proposal.
