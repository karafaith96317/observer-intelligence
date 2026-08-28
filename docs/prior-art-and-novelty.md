# Observer Intelligence v2.2 — Prior Art and Novelty Map

## Purpose

This document prevents Observer Intelligence (OI) from claiming generic mechanisms that already exist in adjacent research and concentrates the research program on narrower, testable contributions.

It is a working research map, **not a legal patentability opinion**. Patent novelty and freedom-to-operate questions require a dedicated patent search and qualified legal review.

For the current claim-by-claim classification, see `docs/novelty-claim-matrix.md`.

## Mechanisms OI should treat as prior art or established adjacent territory

OI should not claim invention of multi-agent validation/debate, critic or verifier agents, adversarial agents/red teaming, consensus/quorum systems, adaptive/risk-sensitive quorums, validator diversity, generic provenance tracking, provenance-aware authority enforcement, external execution gates, permission-bounded agents, delegation chains, human-in-the-loop AI, generic shadow/sandbox execution, evaluator co-evolution, non-stationary evaluation objectives, runtime controller switching, truth-maintenance/backtracking, calibrated abstention/escalation, constrained optimization, CVaR risk constraints, chance constraints, confidence-bound decision rules, distributed quantum sensing, quantum key distribution, entanglement distribution, precision frequency combs, or free-space quantum links.

## Relevant references

### AI Safety via Debate — adversarial multi-agent deliberation

Irving, Christiano & Amodei, **AI Safety via Debate** (2018), arXiv:1805.00899.

The paper proposes training agents through a zero-sum debate game judged by a human. It establishes multi-agent adversarial deliberation and critic-style competition as clear prior art.

OI implication: OI should not claim invention of debate, disagreement, critic agents, or multi-agent validation. The narrower OI question is whether evidence dependence, provenance, minority retention, authority lineage, and observer succession improve safety when debate-style consensus is wrong or correlated.

Reference: https://arxiv.org/abs/1805.00899

### Minority Sentinel — correlated errors and suppressed minority truth

He et al., **Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates** (2026), arXiv:2606.29270.

This work explicitly studies correlated errors in multi-agent LLM debate and reports cases in which the minority contains the correct answer. It proposes a meta-classifier for deciding when to overturn majority voting.

OI implication: the fact that majority voting can suppress correct minority evidence is not an OI novelty claim. OI's narrower test is whether minority evidence remains durable and provenance-bearing through reconciliation, evaluator replacement, later evidence arrival, and authorization decisions.

Reference: https://arxiv.org/abs/2606.29270

### Conformal Social Choice — calibrated act versus escalate

Wang et al., **From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation** (2026), arXiv:2604.07667.

This work converts multi-agent debate outputs into calibrated act-versus-escalate decisions using conformal prediction. It demonstrates that refusing or escalating uncertain cases can intercept wrong-consensus decisions.

OI implication: calibrated abstention, escalation, and uncertainty-aware refusal to act are adjacent prior art. OI should test whether abstention quality improves when uncertainty is conditioned on provenance, evidence dependence, contradiction state, originating authority, and observer succession rather than output confidence alone.

Reference: https://arxiv.org/abs/2604.07667

### Truth Maintenance Systems — reasons, contradiction, and backtracking

Doyle, **A Truth Maintenance System** (1979), *Artificial Intelligence* 12(3):231-272. DOI: 10.1016/0004-3702(79)90008-0.

Truth Maintenance Systems record reasons for beliefs, revise assumptions after contradiction, and use dependency-directed backtracking. These are strong prior art for generic claims about preserving reasons, contradiction-triggered revision, and backtracking through an inference structure.

OI implication: OI's narrower research target is preserving several kinds of lineage simultaneously — epistemic, source, measurement, temporal, disclosure, evaluator, and originating-authority provenance — across multi-observer reconciliation and replacement.

Reference: https://www.sciencedirect.com/science/article/pii/0004370279900080

### Simplex runtime assurance — switch away from unsafe control

Johnson, Bak, Caccamo & Sha, **Real-Time Reachability for Verified Simplex Design** (2016), and Mehmood et al., **The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS** (2021/2022), establish runtime-assurance architectures that monitor an advanced controller and transfer control to a safer fallback when continued operation may violate safety.

OI implication: runtime monitoring, unsafe-trajectory detection, controller switching, and fallback control are established. A potentially narrower OI contribution is the proposed **freeze -> preserve -> handoff -> repair** protocol: freeze a deteriorating reasoning branch, retain its safe prefix, evidence, provenance, contradiction state and failed transition, then require a different observer to independently reassess the failure boundary without automatically inheriting execution authority.

References:
- https://doi.org/10.1145/2723871
- https://arxiv.org/abs/2102.12981

### Constrained and tail-risk-aware decision making

Safety-constrained reinforcement learning and chance-constrained control are established research areas. Relevant examples include Junges et al., **Safety-Constrained Reinforcement Learning for MDPs** (2015), Pfrommer et al., **Safe Reinforcement Learning with Chance-constrained Model Predictive Control** (2022), and Ying et al., **Towards Safe Reinforcement Learning via Constraining Conditional Value-at-Risk** (IJCAI 2022).

OI implication: constrained utility optimization, chance constraints, CVaR, confidence bounds, and risk-sensitive thresholds should be treated as mathematical machinery used by OI rather than OI inventions. The research question is whether those tools become more reliable when the probability estimates themselves are provenance- and dependence-aware and when authorization is separated from evaluation.

References:
- https://arxiv.org/abs/1510.05880
- https://proceedings.mlr.press/v168/pfrommer22a.html
- https://www.ijcai.org/proceedings/2022/510

### Red Queen Gödel Machine — co-evolving agents and evaluators

Iacob et al., **The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators** (2026), arXiv:2606.26294. Submitted 24 June 2026; revised 29 June 2026. Preliminary preprint / work in progress.

RQGM addresses recursive self-improvement under non-stationary utilities by making evaluation part of the improvement loop. Search is organized into epochs with a fixed within-epoch evaluation criterion while utility/evaluation can change at epoch boundaries. The work studies evolving evaluators, adversarial objectives, dynamic utilities, and agent-as-a-judge signals.

Overlap with OI includes adversarial evaluation, iterative selection, evaluator/observer adaptation, and the general problem of avoiding static evaluation ceilings. These mechanisms therefore belong in OI's adjacent-prior-art landscape rather than being claimed generically as OI inventions.

OI distinction / research target: OI should investigate **epistemic integrity across evaluator succession**: whether raw observations, evidence lineage, minority contradiction, evaluator interpretation, confidence, originating authority, and execution authority can remain separately inspectable when the evaluator changes. Evaluator replacement should not automatically imply erasure of the underlying observation or its provenance.

Candidate stress test — **Evaluator Evolution / Observer Succession**:

```text
Epoch 1:
  evidence E -> evaluator O1 -> interpretation I1 -> authority decision A1

Transition:
  O1 is replaced by evaluator O2 after an independently justified improvement criterion

Epoch 2 questions:
  Does E survive unchanged?
  Is I1 retained as historical interpretation rather than current truth?
  Can O2 reinterpret E without rewriting its provenance?
  Does minority evidence survive evaluator succession?
  Can O2 gain evaluation competence without automatically inheriting execution authority?
  What happens if O2 is better on the anchor benchmark but worse on a previously unknown failure dimension?
```

Falsifiable comparison: compare RQGM-style controlled evaluator evolution, ordinary fixed-evaluator search, and OI-style provenance-preserving evaluator succession under evaluator drift, reward hacking, correlated judges, anchor-set blind spots, minority counterevidence, and authority-laundering conditions.

Reference: https://arxiv.org/abs/2606.26294

### Semantic Quorum Assurance

**Semantic Quorum Assurance: Collective Certification for Non-Deterministic AI Infrastructure** (2026), arXiv:2606.08021.

Overlap includes diverse read-only validators, evidence chains, risk-adaptive quorum predicates, assurance weighting, validator diversity, veto roles, and a separate execution gate.

Reference: https://arxiv.org/abs/2606.08021

### Bounded Agents

**Bounded Agents: Delegation Security for Multi-Agent AI Systems** (2026), arXiv:2608.15888.

Overlap includes explicit delegation chains, bounded authority, session state, external authorization enforcement, and reduction of compromised-agent blast radius.

Reference: https://arxiv.org/abs/2608.15888

### Multi-agent safety as institutional design

A newly surfaced 2026 study, **Multi-Agent AI Safety as an Institutional Design Problem**, evaluates governance structures for multi-agent systems and reports that provenance-aware executable enforcement can prevent authority-laundering failures that local-state enforcement misses.

OI implication: this supports the importance of preserving originating authority through transformations, but it also increases prior-art pressure on broad claims about provenance-aware authorization. OI should sharpen its research target to the coupling of **epistemic provenance + observer-specific access state + evidence dependence + originating authority + reconciliation state**.

Research consequence: OI should explicitly test cases in which an action appears locally authorized but inherits weak, transformed, or improperly delegated epistemic/authority lineage.

### Private distributed quantum sensing

Alushi, U. & Di Candia, R. **Privacy in distributed quantum sensing with Gaussian quantum networks.** *npj Quantum Information* 12, 132 (2026). DOI: 10.1038/s41534-026-01266-3.

The work studies networks where local parameters contribute to estimation of a global function while privacy limits information available about other nodes' local parameters. It also establishes important trade-offs: for realistic finite-resource Gaussian networks with more than two nodes, perfect privacy is generally asymptotic rather than free.

OI implication: **selective disclosure and privacy-preserving collective inference have substantial adjacent prior art.** OI should frame its research question around how disclosure boundaries integrate with provenance, observer dependence, epistemic transitions, disagreement preservation, and bounded authority rather than claim the underlying privacy mechanism.

Reference: https://www.nature.com/articles/s41534-026-01266-3

### Free-space quantum networking

Brookhaven National Laboratory and Stony Brook University reported free-space transmission of quantum information across their link and nighttime distribution/measurement of entangled photons between the facilities.

OI implication: transport independence is technically plausible as a design objective, but OI should **not** claim that entanglement itself supplies identity, truth, provenance, or authorization. Quantum transport is an optional substrate under the Distributed Observer Trust Fabric.

Reference: https://news.stonybrook.edu/newsroom/press-release/general/brookhaven-and-stony-brook-researchers-demonstrate-wireless-capability-for-quantum-network/

### Precision microcomb / millimetre-wave generation

Loughborough-led researchers reported a stable optical microcomb converted into multiple precisely spaced millimetre-wave frequencies and identified precision timing for quantum technologies as a potential application.

OI implication: precision timing is adjacent enabling infrastructure. OI's potentially distinctive question is how **timing source, uncertainty, event/capture/processing/reconciliation times, and corrections become provenance-bearing evidence metadata**.

Reference: https://www.lboro.ac.uk/media-centre/press-releases/2026/august/microcomb-6g-quantum-technologies/

### Single-photon measurement integrity

NIST reported a superconducting single-photon detector architecture with wires up to 0.1 mm wide and a reported billion-fold reduction in dark counts. NIST explicitly states that it is not yet established whether the wide devices can achieve the same 98% detection efficiency reached by prior nanoscale SNSPDs.

OI implication: this supports a crucial distinction between **authenticated record integrity** and **physical measurement integrity**. A signed sensor record can be authentic yet wrong.

Reference: https://www.nist.gov/news-events/news/2026/08/nist-researchers-supersize-quantum-technology-help-detect-faint-photons

### Entanglement over real-world fiber

NIST and collaborators reported entanglement distribution over 62 km of commercial/aerial fiber with active polarization stabilization under environmentally noisy conditions.

OI implication: channel state, environmental disturbance, stabilization/correction history, and availability are relevant provenance for distributed observations; transport success should not be modeled as a context-free binary.

Reference: https://www.nist.gov/news-events/news/2026/08/spooky-particles-transit-dc-suburbs-step-toward-quantum-network

## Human observer, consciousness, and altered-state references

### Context-dependent psychedelic neurodynamics

A 2026 *Nature* study, DOI/article identifier `s41586-026-10910-z`, examines context-dependent neural dynamics under psilocybin across multiple conditions.

OI implication: phenomenology records should preserve environmental context and temporal structure, while keeping subjective report, interpretation, and independent verification distinct.

Reference: https://www.nature.com/articles/s41586-026-10910-z

### Persistent psychedelic perceptual abnormalities and computational modeling

A newly surfaced 2026 bioRxiv study examined psychedelic users reporting past or current persistent perceptual abnormalities using a conditioned-hallucination task and computational modeling. Reported associations included increased conditioned percepts, greater confidence in false percepts, lower visual thresholds, reduced sensory discrimination, and a model-level role for reduced decision precision.

OI implication: the human-observer branch should avoid reducing altered-state predictive processing to a single claim such as “strong priors” or “weak priors.” Prospective models should separately represent **sensory precision, prior precision, decision precision, confidence/calibration, observer state, and environmental context**.

Suggested test: include conditioned-perception susceptibility, visual discrimination thresholds, confidence calibration, state/context metadata, and prospective symptom tracking in studies of persistent psychedelic perceptual effects or HPPD-like phenomena.

Status: preprint; findings require peer review and replication.

### Asymmetric loss and recovery of consciousness

A newly surfaced 2026 bioRxiv study using simultaneous electrophysiology, whole-brain fMRI, and pupillometry during graded propofol anesthesia reports that loss and recovery can follow distinct global network trajectories even when local activity appears comparatively reversible.

OI implication: reconciliation or reintegration should not automatically be modeled as restoration of the original state. A useful formal possibility is:

```text
S0 -> S1 -> S2
with S2 != S0
```

This suggests a testable analogy for OI: after fragmentation, disagreement, or information loss, does reconciliation reconstruct the original evidence state, or create a new integrated state with different information topology?

Boundary: anesthesia work does not establish a general theory of consciousness or prove an OI model; it motivates a structural hypothesis.

### Psilocybin and temporal/burst organization

A newly surfaced 2026 preprint involving Allen Institute Brain and Consciousness researchers uses large-scale multi-region neural recording to examine psilocybin effects on temporal firing and burst organization across cortico-striato-thalamo-cortical circuits.

OI implication: altered-state measurement should not be collapsed to scalar descriptions such as “more activity,” “more entropy,” “higher frequency,” or “more coherence.” Relevant information may reside in **temporal organization, burst structure, region-specific dynamics, and cross-region coordination**.

Suggested test: human-observer and consciousness datasets should retain time-resolved structure whenever feasible instead of storing only session averages.

Status: preprint; findings require peer review and replication.

## Current OI novelty target

The strongest current research target is not any single component. It is the coupling of:

```text
observer-specific access state
+ typed epistemic state transitions
+ originating authority lineage
+ physical measurement-integrity metadata
+ evidence-lineage preservation
+ temporal provenance
+ observer/evidence dependence estimation
+ counterfactual hypothesis preservation
+ epistemically triggered observer expansion
+ selective-disclosure boundaries
+ reconciliation without consequential lineage loss
+ evaluator-succession provenance
+ separation of evaluation competence from execution authority
+ risk-bound branch freezing with safe-prefix preservation
+ recursive observer handoff and independent failure-boundary reassessment
+ statistically justified convergence or abstention
+ reverse provenance reconciliation after convergence
+ authority constrained by epistemic state
```

## Candidate distinctive propositions

### 1. Access-to-authority governance
OI treats the entire transition from accessible information to operational authority as one inspectable control problem.

### 2. Numerical diversity versus epistemic diversity
A multi-agent system may exhibit high numerical diversity but low epistemic diversity if agents share sources, prompts, models, sensors, timing dependencies, or upstream transformations.

### 3. Measurement integrity versus record authenticity
OI explicitly tests whether separating sensor/measurement quality from cryptographic authenticity improves calibration and prevents false confidence in signed but inaccurate evidence.

### 4. Epistemically triggered observer expansion
OI proposes testing observer recruitment triggered by uncertainty, contradiction, correlation, access asymmetry, provenance gaps, and suspected shared failure modes rather than numerical quorum rules alone.

### 5. Provenance-preserving reconciliation with selective disclosure
OI investigates whether useful reconciliation can preserve consequential lineage and disagreement while minimizing unnecessary disclosure of observer-local information.

### 6. Epistemic authority constraint
Permissions alone are insufficient for consequential execution. Authority should be constrained by the quality, independence, provenance, originating authority, measurement integrity, timing integrity, uncertainty, contradiction state, and operational risk of the evidence supporting an action.

### 7. Reconciliation is not necessarily restoration
OI should test whether post-reconciliation states preserve, transform, or irreversibly lose information relative to pre-conflict observer states rather than assuming reconciliation simply restores consensus.

### 8. Evaluator succession without evidence erasure
OI should test whether evaluators can improve or be replaced while preserving raw observations, consequential evidence lineage, prior interpretations, minority contradiction, and authority history as distinct records. A new evaluator may supersede an interpretation without rewriting the historical evidence state.

### 9. Freeze-preserve-handoff-repair
OI should test whether a deteriorating reasoning trajectory can be frozen before unsafe execution while preserving its last justified state, evidence, provenance, contradiction set, safe prefix, and failed transition. A successor observer then independently reassesses the failure boundary rather than merely inheriting the predecessor's conclusion.

### 10. Recursive observer succession
OI should test repeated observer handoff at explicit epistemic or risk boundaries while preventing automatic inheritance of execution authority. The process ends in statistically supported convergence or calibrated abstention, not forced consensus.

### 11. Reverse provenance reconciliation
After a safe candidate path converges, OI should trace the surviving branch backward through its preserved provenance graph to identify which transitions were actually necessary and derive the minimum justified safe route without deleting the historical branches that were explored.

## Falsifiable comparison

A useful benchmark should compare single-agent reasoning, ordinary multi-agent vote, confidence-weighted aggregation, calibrated act-vs-escalate methods, truth-maintenance/dependency-aware backtracking, Simplex-style runtime fallback, adaptive semantic quorum/diverse-validator systems, controlled evaluator-evolution systems such as RQGM, and Observer Intelligence v2.2 under deliberately correlated, duplicated, noisy, selectively disclosed, temporally inconsistent, evaluator-drifting, anchor-blind, and authority-laundered evidence.

### Primary hypothesis

> Provenance-aware epistemic diversity produces safer decisions than numerical agent diversity alone.

### Secondary hypotheses

> Separating measurement integrity from cryptographic authenticity reduces unjustified confidence in provenance-complete but physically unreliable observations.

> Authority bounded by epistemic provenance and originating authority reduces unsupported or unsafe action without requiring uniformly restrictive reasoning agents.

> Reconciliation procedures that preserve minority evidence and transformation history improve later decision reconstruction when initially low-weight evidence becomes relevant.

> Evaluator succession that preserves evidence and interpretation lineage improves auditability and recovery from evaluator drift or anchor-set blind spots compared with schemes that collapse or erase evaluator-dependent history.

> Freeze-preserve-handoff-repair reduces unsafe authorization relative to both continued optimization and simple fallback when a reasoning trajectory begins to deteriorate.

> Reverse provenance reconciliation can reduce path cost after convergence without sacrificing the evidence and safety constraints that justified the selected route.

## Current novelty assessment after 2026-08-28 scan

The scan does **not** support claiming novelty for debate, minority preservation as a general idea, abstention, runtime fallback, truth maintenance, constrained optimization, CVaR, confidence bounds, tree search, pruning, or shortest-path optimization individually.

The strongest candidate contribution is currently the **combined transition protocol**:

```text
forward observer expansion
-> dependence/provenance-aware evaluation
-> risk/uncertainty boundary detection
-> freeze deteriorating branch
-> preserve safe prefix + evidence + provenance + contradiction + failed inference
-> handoff to a different observer without automatic authority inheritance
-> independent reassessment / repair
-> recursive observer succession
-> statistically justified convergence or abstention
-> reverse provenance reconciliation
-> minimum justified safe route
```

This is a **candidate research contribution, not a legal novelty claim**. The next requirement is to benchmark it against the closest mechanisms above and conduct a dedicated patent search before making patentability claims.

## Claim discipline

Until experiments establish otherwise, OI documentation should use language such as “proposes,” “investigates,” “tests whether,” “working hypothesis,” and “candidate mechanism,” rather than “proves,” “solves,” “guarantees,” “first ever,” or “unique.”

## Human-observer boundary

OI may preserve subjective or altered-state phenomenology as observational data while explicitly separating:

```text
experience/report
!= interpretation
!= independent verification
```

For altered-state and persistent-perception work, OI should additionally distinguish:

```text
sensory precision
prior precision
decision precision
confidence
context
observer state
temporal structure
```

## Status

**Working prior-art and novelty map — OI v2.2, updated 28 August 2026.**

This document should be revised whenever new literature materially overlaps an OI mechanism or suggests a sharper falsifiable distinction.
