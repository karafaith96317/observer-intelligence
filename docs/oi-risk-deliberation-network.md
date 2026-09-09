# OI Risk Deliberation Network (OI-RDN)

**Status:** Research architecture / proposed extension

## Purpose

The OI Risk Deliberation Network extends Observer Intelligence from claim- and action-level adjudication into structured, cross-domain risk forecasting and mitigation analysis.

It is **not** a world-governance system and does not grant AI political or coercive authority. Its purpose is to help humans inspect competing risk models, evidence, uncertainties, interventions, and trade-offs while preserving disagreement and provenance.

## Core question

Can a network of epistemically differentiated observers identify, challenge, combine, and mitigate high-impact risks more reliably than a single model, ordinary multi-agent voting, or debate systems in which agents share the same evidence and incentives?

## Architecture

```text
SYSTEM QUESTION
    |
    +-- domain observers
    |     climate / ecology
    |     food / water
    |     public health / pandemic
    |     conflict / geopolitical
    |     nuclear / cyber / infrastructure
    |     energy / supply chain
    |     economic / social stability
    |     biological / health-data governance
    |
    v
INDEPENDENT RISK GENERATION
    |
    v
EVIDENCE + PROVENANCE BINDING
    |
    v
ADVERSARIAL PAIRING
    |
    +-- challenge assumptions
    +-- identify missing evidence
    +-- propose falsification tests
    +-- estimate dependence/shared-source risk
    |
    v
ROLE REVERSAL / STEELMANNING
    |
    v
CROSS-DOMAIN SYNTHESIS
    |
    v
MITIGATION GENERATION
    |
    v
ADVERSARIAL MITIGATION TESTING
    |
    v
HUMAN DELIBERATION / AUTHORIZATION
```

## Observer design

The system should not instantiate several copies of the same model with identical prompts and data and call that diversity. OI-RDN distinguishes:

- **numerical diversity** — number of agents;
- **model diversity** — different models or model families;
- **role diversity** — different epistemic responsibilities;
- **evidence diversity** — different source sets or information partitions;
- **disciplinary diversity** — different domain models and assumptions;
- **stakeholder diversity** — different affected populations or institutional perspectives;
- **failure-mode diversity** — agents optimized to detect different classes of error.

`N_agents != N_independent_evidence_pathways` remains a governing rule.

## Risk representation

Each candidate risk should retain at least:

```json
{
  "risk_id": "...",
  "domain": "...",
  "scenario": "...",
  "causal_chain": [],
  "supporting_evidence": [],
  "counterevidence": [],
  "probability_or_frequency_model": null,
  "severity": null,
  "exposure": null,
  "reversibility": null,
  "uncertainty": null,
  "time_horizon": null,
  "affected_groups": [],
  "shared_dependency_risk": [],
  "falsification_conditions": [],
  "proposed_mitigations": []
}
```

Numerical scores are optional and must not imply precision beyond the evidence.

## Deliberation protocol

### 1. Independent generation
Observers form initial hypotheses before reading other observers' conclusions where practical.

### 2. Evidence separation
Where useful, agents receive partially distinct evidence sets to reduce correlated reasoning and information herding.

### 3. Adversarial challenge
Observers identify unsupported premises, missing variables, alternative causal explanations, distribution shift, strategic behavior, and hidden dependencies.

### 4. Role reversal
Observers must periodically defend the strongest version of an opposing hypothesis. This is intended to distinguish evidence-sensitive belief revision from rhetorical persistence.

### 5. Minority preservation
A minority finding is not erased solely because a majority disagrees. Its evidence and provenance remain durable for later re-evaluation.

### 6. Cross-domain synthesis
Risks may interact. The system should build a dependency graph rather than force every branch into a single ranked list.

### 7. Mitigation inversion
After identifying a harmful pathway, the system reverses the analysis:

```text
CAUSE
  -> EARLY INDICATOR
  -> POSSIBLE INTERVENTION
  -> COUNTERARGUMENT
  -> UNINTENDED CONSEQUENCE
  -> ALTERNATIVE
  -> TEST
  -> EVIDENCE
```

### 8. Human authority
OI-RDN may forecast, challenge, simulate, compare, recommend, document, and escalate. It must not coerce consensus, declare a political answer to be uniquely true, hide unresolved minority findings, or autonomously impose high-impact policy.

## Output classes

The system should not be forced to produce a single winner. It may return parallel conclusions such as:

- highest-probability scenario;
- highest-consequence scenario;
- fastest-growing risk;
- highest-uncertainty scenario;
- most preventable scenario;
- strongest minority hypothesis;
- mitigation with best evidence;
- mitigation with highest uncertainty or unintended-consequence risk.

## Proposed evaluation

Compare:

1. single-agent reasoning;
2. same-model multi-agent majority voting;
3. conventional multi-agent debate;
4. evidence-diverse deliberation;
5. OI-RDN with asymmetric roles, provenance, minority retention, role reversal, and authority separation.

Candidate metrics:

- forecast calibration / Brier score where ground truth becomes available;
- unsupported-claim rate;
- correlated-error rate;
- contradiction discovery;
- minority-correctness retention;
- evidence attribution accuracy;
- mitigation failure discovery;
- human-review agreement;
- correct abstention/escalation;
- provenance completeness;
- time and compute cost.

## Related systems and intellectual lineage

OI-RDN builds on established ideas and does **not** claim invention of the following mechanisms.

### AI Safety via Debate
Irving, Christiano & Amodei (2018), *AI Safety via Debate*, arXiv:1805.00899. Establishes adversarial multi-agent debate judged by humans.

https://arxiv.org/abs/1805.00899

### Delphi method
The classical Delphi method uses repeated expert elicitation and feedback to improve structured forecasting and surface disagreement. OI-RDN treats Delphi-style iterative elicitation as intellectual lineage rather than an OI invention.

### InfoDelphi / designed information asymmetry
Li et al. (2026), *Diverse Evidence, Better Forecasts: Multi-Agent Deliberation Under Information Asymmetry*, arXiv:2607.01661. The work reports that deliberately partitioning evidence across agents reduces correlated error and improves forecasting compared with shared-evidence deliberation.

https://arxiv.org/abs/2607.01661

### Conformal Social Choice
Wang et al. (2026), *From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation*, arXiv:2604.07667. Demonstrates calibrated act-versus-escalate decisions after multi-agent debate and explicitly shows that agreement is not evidence of correctness.

https://arxiv.org/abs/2604.07667

### Truth Maintenance Systems
Doyle (1979), *A Truth Maintenance System*, Artificial Intelligence 12(3):231–272. Establishes dependency-aware belief maintenance, contradiction handling, and backtracking.

https://doi.org/10.1016/0004-3702(79)90008-0

### NIST AI Risk Management Framework
NIST AI RMF provides established risk-governance concepts for identifying, mapping, measuring, and managing AI risk and emphasizes multidisciplinary perspectives, privacy, safety, transparency, accountability, and ongoing risk tracking.

https://www.nist.gov/itl/ai-risk-management-framework

## OI-specific research target

The candidate contribution is not debate, Delphi, risk scoring, red teaming, voting, or human oversight by themselves. The research target is their coupling with:

```text
observer-specific evidence access
+ deliberately differentiated evidence pathways
+ typed epistemic transitions
+ dependence-aware observer counting
+ durable minority contradiction
+ role reversal
+ cross-domain causal/dependency graphs
+ provenance-preserving reconciliation
+ mitigation inversion and adversarial mitigation testing
+ explicit uncertainty / abstention
+ separation of recommendation from execution authority
+ auditable human decision lineage
```

These remain hypotheses until comparative experiments demonstrate an advantage.