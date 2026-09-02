# 2026-09-02 — Reconciliation boundary, representation, and adjudication update

## Scope

This note integrates three newly surfaced 2026 preprints that materially intersect Observer Intelligence (OI). All three are **preprints**, not peer-reviewed validation of OI. They are recorded as adjacent evidence/prior art and as sources of falsifiable design requirements.

---

## 1. Boundary metadata collapse in multi-agent LLM handoffs

**Finding.** Wang, Goyal, Chandrasekharan, and Sundaram study multi-agent LLM handoffs in which an upstream interaction is compressed into a downstream handoff artifact. They report that operational facts can remain intact while privacy/usage-boundary metadata degrades independently. In their controlled testbed, boundary-marker survival and operational-fact survival were nearly uncorrelated; tighter handoff compression reduced boundary survival while fact survival remained high. Explicit boundary constraints substantially reduced downstream leakage compared with vague constraints.

**Status / boundary.** arXiv preprint 2608.29028, surfaced in the 1 September 2026 arXiv listings. This is not peer-reviewed and does not validate OI.

**OI connection.** Selective disclosure; provenance-preserving reconciliation; multi-agent handoff; information-governance metadata; epistemic-process correctness.

**Effect on OI.** **Supports + adjacent prior art + suggests a benchmark.** It directly supports treating boundary/disclosure metadata as an independently measurable reconciliation property rather than assuming factual fidelity implies governance fidelity.

**Research consequence.** Add a **Boundary Preservation Invariant**: consequential usage, audience, consent, scope, and disclosure metadata should survive reconciliation/handoff independently of semantic fact survival. Evaluate at least two channels separately:

\[
F = \text{fact survival}, \qquad B = \text{boundary survival}.
\]

A system with high \(F\) but low \(B\) should count as an epistemic-process failure even when its summary is factually correct.

**Source.** Yian Wang, Agam Goyal, Eshwar Chandrasekharan, Hari Sundaram, “Facts Without Rules: Boundary Metadata Collapse in Multi-Agent LLM Handoffs,” arXiv:2608.29028 (2026). https://arxiv.org/abs/2608.29028

---

## 2. Provenance-aware structured state reconciliation for human-AI handover

**Finding.** Bishop, Stull, Crockett, and Hayes present a provenance-aware pipeline that converts task telemetry and human-authored reports into a shared typed task-state representation, aligns/reconciles their facts, detects conflicts, and produces structured handover reports. Their controlled evaluation uses 13 paired task states. The authors report that combining both sources preserved greater estimated task-state utility than either source alone, and that structured reconciliation produced substantially less misinformation than a direct end-to-end LLM given the same inputs while retaining comparable estimated utility.

**Status / boundary.** arXiv preprint 2608.28907, surfaced in the 1 September 2026 listings and described as in preparation for conference submission. Not peer reviewed.

**OI connection.** Human-machine observer heterogeneity; typed state representation; provenance-aware reconciliation; conflict preservation; partial observability; handover safety.

**Effect on OI.** **Significant partial duplicate / prior art + support + comparison target.** Generic claims that heterogeneous human and machine observations can be typed, provenance-aware, conflict-detected, and reconciled should not be claimed as uniquely OI.

**Novelty consequence.** OI's narrower candidate contribution remains the coupling of observer-specific access state, measurement integrity, evidence dependence, temporal provenance, competing hypotheses, disclosure boundaries, reconciliation lineage, authority lineage, and action gating.

**Research consequence.** Add this method as an explicit baseline for future OI evaluation:

```text
direct end-to-end LLM
vs structured state reconciliation
vs OI provenance/dependence/authority-aware reconciliation
```

Stress conditions should include correlated sources, stale evidence, inaccurate-but-authenticated telemetry, hidden dependencies, boundary loss, minority counterevidence, and authority laundering.

**Source.** Kayleigh Bishop, Maria P. Stull, Breanne Crockett, Bradley Hayes, “Structured State Reconciliation for Human-AI Task Handover,” arXiv:2608.28907 (2026). https://arxiv.org/abs/2608.28907

---

## 3. Verification abundance and representational adjudication

**Finding.** Kallel and El Louadi distinguish three layers in machine-assisted mathematical verification: **derivational validity**, **representational fidelity**, and **epistemic significance**. Their central argument is that cheap machine proof checking addresses derivational validity but does not remove the expert burden of determining whether a formal statement faithfully represents the intended problem or what epistemic significance should be assigned to the result. They propose a taxonomy of representational mismatch and disclosure requirements for machine-generated mathematical claims.

**Status / boundary.** arXiv preprint 2608.28997 (2026). This is a conceptual analysis/preprint and should be treated as such rather than as empirical validation.

**OI connection.** Typed epistemic transitions; representation; verification; adjudication; authority; provenance; AI evaluators.

**Effect on OI.** **Conceptual support + suggests a representation refinement.** It reinforces the distinction between proving a derivation and establishing that the representation corresponds to the intended target.

**Research consequence.** OI should explicitly distinguish:

\[
\text{verification status} \neq \text{representation validity} \neq \text{authority status}.
\]

Candidate pipeline refinement:

```text
WORLD / ENVIRONMENT
    -> ACCESS
    -> REPRESENTATION
    -> SOURCE ATTRIBUTION
    -> OBSERVATION / EVIDENCE RECORD
    -> MEASUREMENT INTEGRITY
    -> INTERPRETATION
    -> HYPOTHESIS
    -> CLAIM
    -> VERIFICATION
    -> SELECTIVE DISCLOSURE
    -> RECONCILIATION
    -> AUTHORIZATION
    -> ACTION
```

Representation and source attribution should themselves carry uncertainty and provenance; neither should be treated as automatically correct.

**Source.** Maher Kallel and Mohamed El Louadi, “Verification abundance, adjudication scarcity: what happens to mathematical knowledge when proof checking becomes free,” arXiv:2608.28997 (2026). https://arxiv.org/abs/2608.28997

---

## Proposed reconciliation invariant

The combined findings motivate a stronger candidate OI invariant:

\[
R_{valid} = F \land P \land B \land D \land M \land T \land A
\]

where:

- \(F\) = factual/content fidelity,
- \(P\) = provenance preservation,
- \(B\) = boundary/disclosure preservation,
- \(D\) = dependence-structure preservation,
- \(M\) = measurement-integrity preservation,
- \(T\) = temporal-lineage preservation,
- \(A\) = authority-lineage preservation.

This is a **proposed research structure**, not an established mathematical law. In implementation, the dimensions should be scored separately rather than collapsed prematurely into a Boolean.

The central synthesis is:

> **Preserving the answer is not equivalent to preserving what made the answer legitimate.**

A reconciled result can be semantically correct while still failing epistemically because it lost usage boundaries, source dependence, representation fidelity, measurement state, temporal ordering, or authority lineage.
