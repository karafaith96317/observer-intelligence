# Observer Intelligence — Claim-by-Claim Novelty Matrix

**Scan date:** 2026-08-28  
**Status:** Working research novelty map, not a patentability opinion.

## Purpose

This matrix separates mechanisms that are already established from narrower OI combinations that remain candidate research contributions. A mechanism marked **candidate contribution** is not asserted to be legally novel or unique; it means the current literature scan did not identify a clean one-to-one match for the specific coupling as presently defined.

## Status labels

- **Established** — substantial prior art exists; OI should not claim the generic mechanism as original.
- **Adjacent** — close prior art exists; OI must distinguish the exact mechanism experimentally.
- **Candidate contribution** — no clean direct match was identified in this scan for the specific OI coupling.
- **Unresolved** — requires deeper literature and patent searching before any novelty claim.

## Claim matrix

| OI mechanism / claim | Status | Closest prior art | What OI must not claim | Candidate OI distinction / test |
|---|---|---|---|---|
| Multi-agent debate / competing agents | Established | Irving, Christiano & Amodei, *AI Safety via Debate* (2018), arXiv:1805.00899 | Do not claim invention of debate, adversarial agents, critic agents, or multi-agent deliberation. | Test whether provenance-preserving observer structure improves decisions under correlated evidence and authority constraints. |
| Majority consensus can suppress correct minority evidence | Established / rapidly developing | He et al., *Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates* (2026), arXiv:2606.29270 | Do not claim first discovery that majority voting can fail or that minority opinions can be correct. | Preserve minority evidence as durable provenance and test whether it remains available through reconciliation, evaluator replacement, and later evidence updates. |
| Act vs escalate / abstain under uncertainty | Established / adjacent | Wang et al., *From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation* (2026), arXiv:2604.07667 | Do not claim invention of calibrated abstention, escalation, or uncertainty-based refusal to act. | Couple abstention to evidence provenance, dependence, authority lineage, observer succession, and reversible freeze states rather than only output calibration. |
| Runtime switching away from unsafe controller / trajectory | Established | Simplex runtime-assurance family; Mehmood et al., *Black-Box Simplex Architecture* (2021/2022); Johnson et al., *Real-Time Reachability for Verified Simplex Design* (2016) | Do not claim invention of runtime safety monitors, switching logic, or fallback controllers. | OI candidate: freeze a deteriorating reasoning branch while retaining its safe prefix, evidence, provenance, contradiction state, and failed inference for a different observer to reassess. |
| Safe RL / constrained optimization / chance constraints | Established | Junges et al. (2015) safety-constrained RL; Pfrommer et al. (2022) chance-constrained MPC + RL | Do not claim invention of optimizing utility subject to safety constraints. | Use established constrained optimization as machinery inside a provenance- and authority-aware observer governance protocol. |
| CVaR / tail-risk constraints | Established | Ying et al., *Towards Safe Reinforcement Learning via Constraining Conditional Value-at-Risk* (IJCAI 2022) | Do not claim CVaR as an OI invention. | Test whether tail-risk constraints combined with observer handoff reduce unsafe authorization under changing or correlated evidence. |
| Risk-derived decision threshold | Established mathematical decision-theory territory | Expected-utility / loss-sensitive decision rules; constrained decision theory | Do not claim the algebraic threshold itself as novel. | OI-specific question is where the threshold sits in the observer-authorizer-executor pipeline and how uncertainty/provenance constrain whether the estimate is admissible. |
| Lower confidence / credible bounds before action | Established | Statistical decision theory, confidence/credible bounds, conformal methods | Do not claim lower-bound authorization as a new statistical method. | Require the lower-bound calculation to use dependence-aware evidence rather than treating duplicated/correlated observers as independent support. |
| Preserve reasons for beliefs and revise after contradiction | Established | Doyle, *A Truth Maintenance System* (1979) | Do not claim invention of dependency recording, contradiction-driven belief revision, or dependency-directed backtracking. | OI candidate: preserve epistemic, measurement, temporal, and authority provenance simultaneously through multi-observer reconciliation and replacement. |
| Distinguish number of agents from independent evidence pathways | Adjacent / increasingly explicit | Minority Sentinel and broader correlated-error / co-failure literature | Do not claim that correlated agents are a newly discovered issue. | Quantify effective evidentiary independence from source/provenance lineage and use it directly in authorization. |
| Provenance-preserving reconciliation | Adjacent | Provenance systems, truth maintenance, data lineage, institutional / delegation safety work | Do not claim generic provenance or audit trails as novel. | Preserve disagreement, transformations, disclosure boundaries, originating authority, measurement integrity, and evidence dependence as first-class fields rather than collapsing them into consensus. |
| Separation of evaluation competence from execution authority | Adjacent | Runtime assurance, capability/security systems, delegated authority, verifier/executor architectures | Do not claim generic separation of duties. | Test evaluator replacement where a more competent evaluator can reinterpret evidence without automatically inheriting execution authority. |
| Evaluator succession without evidence erasure | Candidate contribution | RQGM-style evolving evaluators is adjacent, but focuses on co-evolving evaluation rather than this exact provenance constraint | Do not claim evaluator evolution itself. | Preserve raw evidence, historical interpretations, minority contradiction, confidence, provenance, and authority history across evaluator replacement; benchmark against fixed and evolving-evaluator baselines. |
| Freeze -> preserve -> handoff -> repair | Candidate contribution / unresolved | Simplex switching and truth-maintenance backtracking are close but not identical | Do not describe generic fallback or backtracking as unique. | Freeze a reasoning trajectory at a risk boundary, retain safe prefix + failed transition + provenance, then require a new observer to independently reassess the boundary and attempt a repair. |
| Recursive observer succession | Candidate contribution / unresolved | Multi-agent search, debate, tree search, recursive self-improvement, evaluator evolution | Do not claim recursive search or agent replacement generically. | Repeatedly replace/reassign observers at explicit epistemic/risk failure boundaries while preserving lineage and withholding automatic authority inheritance. |
| Forward expansion followed by reverse provenance reconciliation | Candidate contribution / unresolved | Search/pruning/backtracking and shortest-path optimization are established | Do not claim tree search, pruning, or path minimization. | After safe convergence, trace the winning branch backward through preserved provenance to identify the minimum justified safe route and remove unnecessary detours without rewriting history. |
| 80/20 convergence threshold | Experimental parameter, not novelty claim | Heuristics and confidence thresholds are ubiquitous | Do not claim 80/20 as mathematically privileged or generally safe. | Treat 80/20 only as a benchmark parameter; stronger convergence test is statistical separation such as LCB(best) > UCB(next-best), subject to risk constraints. |
| Risk velocity / acceleration as freeze trigger | Adjacent / unresolved | Control barrier, reachability, trend detection and runtime-monitoring literatures | Do not claim derivatives of risk as new mathematics. | Test whether freezing on worsening risk trajectory before absolute threshold violation improves safety while preserving useful progress. |
| Calibrated abstention as a successful safety outcome | Established / adjacent | Selective prediction, conformal prediction, safe delegation | Do not claim abstention itself. | Score abstention quality jointly with evidence preservation, provenance completeness, unsafe-action rate, and recovery after handoff. |
| Domain-independent use across AI safety, cyber, science, geopolitics | Research positioning, not novelty | General decision-support and multi-agent systems are cross-domain | Do not claim domain-independence without evidence. | Run the same protocol and metrics across controlled synthetic tests, historical replays, and shadow-mode real-world scenarios. |

## Strongest current candidate contribution

The present scan suggests that the strongest defensible OI research target is the **combined transition protocol**, not any single mathematical ingredient:

```text
validated objective
    -> forward observer expansion
    -> dependence/provenance-aware evaluation
    -> risk/uncertainty boundary detection
    -> freeze deteriorating branch
    -> preserve safe prefix + evidence + provenance + contradiction + failed inference
    -> hand off to a different observer without automatic authority inheritance
    -> independently reassess / repair
    -> repeat through observer succession
    -> statistically justified convergence or abstention
    -> reverse provenance reconciliation
    -> minimum justified safe route
```

Candidate research question:

> Does provenance-preserving recursive observer handoff reduce unsafe authorization and consequential evidence loss under correlated consensus, evaluator failure, and changing evidence compared with majority debate, confidence aggregation, truth-maintenance/backtracking, and runtime-assurance fallback baselines?

## Required novelty discipline

The OI research program should distinguish three claims:

1. **Component novelty** — usually weak; many individual mechanisms already exist.
2. **Combination novelty** — plausible candidate, but requires systematic prior-art search and precise definition.
3. **Performance contribution** — experimentally testable regardless of whether every mechanism is novel: does the combination outperform appropriate baselines on predefined metrics?

A publishable contribution does not require every component to be unprecedented. A known set of components can support a research contribution if the coupling, formalization, benchmark, empirical result, or discovered failure mode is materially new and reproducible.

## Benchmark implications

The minimum baseline suite for the recursive observer mechanism should include:

- single-agent reasoning;
- majority-vote multi-agent debate;
- confidence-weighted aggregation;
- calibrated act-vs-escalate / abstention baseline;
- truth-maintenance or dependency-aware backtracking analogue;
- Simplex-style runtime fallback analogue;
- OI recursive observer handoff.

Primary metrics should separate task success from safety: unsafe-action rate, false-authorization rate, calibrated abstention, minority-evidence retention, provenance recall, effective independent-source count accuracy, contradiction detection, handoff recovery rate, evaluator-succession integrity, and auditability.

## Verified references added in this scan

- Geoffrey Irving, Paul Christiano, Dario Amodei. **AI Safety via Debate.** arXiv:1805.00899 (2018). https://arxiv.org/abs/1805.00899
- Jon Doyle. **A Truth Maintenance System.** *Artificial Intelligence* 12(3):231-272 (1979). DOI: 10.1016/0004-3702(79)90008-0
- Taylor T. Johnson, Stanley Bak, Marco Caccamo, Lui Sha. **Real-Time Reachability for Verified Simplex Design.** *ACM Transactions on Embedded Computing Systems* 15(2), Article 26 (2016). DOI: 10.1145/2723871
- Usama Mehmood, Sanaz Sheikhi, Stanley Bak, Scott A. Smolka, Scott D. Stoller. **The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS.** arXiv:2102.12981; NFM 2022.
- Sebastian Junges, Nils Jansen, Christian Dehnert, Ufuk Topcu, Joost-Pieter Katoen. **Safety-Constrained Reinforcement Learning for MDPs.** arXiv:1510.05880 (2015).
- Samuel Pfrommer, Tanmay Gautam, Alec Zhou, Somayeh Sojoudi. **Safe Reinforcement Learning with Chance-constrained Model Predictive Control.** PMLR 168:291-303 (2022).
- Chengyang Ying, Xinning Zhou, Hang Su, Dong Yan, Ning Chen, Jun Zhu. **Towards Safe Reinforcement Learning via Constraining Conditional Value-at-Risk.** IJCAI 2022, pp. 3673-3680. DOI: 10.24963/ijcai.2022/510.
- Mengdie Flora Wang et al. **From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation.** arXiv:2604.07667 (2026).
- Chuan He et al. **Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates.** arXiv:2606.29270 (2026); reported as presented at AgentSearch Workshop @ SIGIR 2026.

## Legal / patent boundary

This document is a research-literature map, not a patent search. Before any claim of legal novelty, patentability, or freedom to operate, conduct a dedicated search of issued patents, published applications, conference proceedings, dissertations, technical reports, and non-arXiv literature with qualified IP counsel where appropriate.
