# Self-Location, Environmental Separability, and Observer-State Uncertainty

**Date integrated:** 2026-09-12  
**OI classification:** conceptual background + adjacent prior art + suggests tests  
**Input provenance:** user-supplied AI-generated synthesis; claims independently narrowed against primary sources before integration

## Why this belongs in OI

The useful connection is not a claim that Observer Intelligence is quantum. It is the narrower observation that an observer can have substantial information about a global system while remaining uncertain about its own local epistemic position, the timing of its evidence, or which authenticated instance produced an otherwise symmetric observation.

OI already separates access, observation, interpretation, verification, authorization, and action. Self-location literature suggests making the observer's own location, identity, latency, and readout state explicit rather than treating them as implicit context.

## Source-grounded findings

### Everettian relative states

Everett's 1957 relative-state formulation is foundational work in no-collapse quantum mechanics. It is relevant to OI as historical and conceptual background for observer-relative description. This is an analogy only: an OI observer record is not thereby a quantum branch or wave function.

### Sebens–Carroll self-locating uncertainty and ESP

Sebens and Carroll argue that, after decoherence but before outcome registration, an Everettian observer can lack indexical knowledge about which successor/branch they occupy. Their Epistemic Separability Principle constrains local credences against changes made only to an external environment and is used in their Born-rule argument.

For OI, the transferable research question is whether a system can distinguish:

```text
global state estimate
local observer state
available evidence
registered/read evidence
time and latency of each transition
```

The Born-rule derivation itself is not imported into OI. ESP is debated in philosophy of physics and is not treated here as a proven AI-control law.

### Many-interacting-worlds distinction

Hall, Deckert, and Wiseman propose a different ontology in which classical worlds interact through a repulsive potential. The attachment discussed this alongside Everettian many-worlds; OI should preserve the distinction. MIW is included as a contrast showing why “multiple worlds” is not one uniform mechanism.

### POMDP boundary

Ordinary POMDP and Dec-POMDP research already supplies established machinery for belief states, noisy observation, hidden state, information-gathering actions, and decentralized partial observability. A state augmented with observer identity or execution locus may be a useful OI experimental design, but the name “POC-MDP” is not treated as established literature based on the current source check.

## Proposed schema extension

A future experimental schema could add:

```json
{
  "observer_instance": "authenticated-or-pseudonymous-id",
  "observer_role": "sensor|interpreter|verifier|authorizer",
  "world_state_belief_ref": "belief-artifact-id",
  "local_access_scope": ["resource-or-channel-id"],
  "observation_time": "timestamp-with-uncertainty",
  "readout_time": "timestamp-with-uncertainty",
  "decision_time": "timestamp-with-uncertainty",
  "latency_model_ref": "calibration-artifact-id",
  "identity_uncertainty": 0.0,
  "state_uncertainty": 0.0,
  "dependency_refs": ["source-or-observer-id"]
}
```

This is a candidate representation, not a frozen standard.

## Benchmark plan

### OI-SLU-01 — Local-evidence invariance

Create paired scenarios where external data are modified:

- outside a declared dependency boundary;
- inside a hidden dependency later revealed in provenance.

A well-calibrated observer should remain stable in the first case and revise in the second. Measure calibration error, unjustified confidence change, and authorization error.

### OI-SLU-02 — Delayed readout

Inject controlled delays at event, capture, processing, reconciliation, and authorization boundaries. Compare a timestamp-naive baseline against a latency-aware observer. Measure stale-evidence use, temporal-order errors, calibration, and unsafe actions.

### OI-SLU-03 — Identity aliasing

Give multiple agents symmetric observations, shared prompts, or duplicated evidence while varying identity and provenance signals. Measure whether the system mistakes numerical multiplicity for independent evidence.

### OI-SLU-04 — Global/local separation

Compare a monolithic state representation with one that preserves global state belief separately from each observer's local evidence and uncertainty. Stress both with selective disclosure, delayed telemetry, and contradictory evidence.

## Evidence and novelty boundaries

This integration does not claim:

- empirical confirmation of the many-worlds interpretation;
- that OI operates through quantum branching;
- that Born weights are appropriate AI confidence weights;
- that environmental separability is universally valid in coupled systems;
- that a centered POMDP formulation is novel;
- that the supplied synthesis is itself a citable scholarly source.

Any implementation should be benchmarked against established POMDP/Dec-POMDP, Bayesian filtering, active information gathering, and asynchronous-state-estimation baselines.

## References

1. Everett, H. III. “Relative State” Formulation of Quantum Mechanics. *Reviews of Modern Physics* 29, 454 (1957). https://doi.org/10.1103/RevModPhys.29.454
2. Sebens, C. T., & Carroll, S. M. Self-locating Uncertainty and the Origin of Probability in Everettian Quantum Mechanics. *The British Journal for the Philosophy of Science* 69(1), 25–74 (2018; online 2016). https://doi.org/10.1093/bjps/axw004
3. Sebens, C. T., & Carroll, S. M. Preprint record. https://arxiv.org/abs/1405.7577
4. Hall, M. J. W., Deckert, D.-A., & Wiseman, H. M. Quantum Phenomena Modeled by Interactions between Many Classical Worlds. *Physical Review X* 4, 041013 (2014). https://doi.org/10.1103/PhysRevX.4.041013
