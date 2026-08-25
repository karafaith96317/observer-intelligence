# Observer Intelligence Evidence Matrix — v2.0

## Purpose

The Observer Intelligence Evidence Matrix (OIEM) is a structured method for describing an observer and its evidence state without converting a complex profile into a single categorical judgment.

It can be applied to AI agents, multi-agent systems, human–AI research settings, simulated agents, and other systems where claims about observation, agency, internal state, reliability, or experience require careful evidentiary separation.

## Observer dimensions

| Dimension | Core question | Example evidence |
|---|---|---|
| Sensory / data access | What can the observer potentially access? | sensors, APIs, files, environmental measurements |
| Actual observation | What information was actually acquired or extracted? | logs, sensor frames, retrieved records, direct reports |
| Memory continuity | What persists across time? | logs, persistent state, recalled information |
| Global information availability | Where can observed information propagate? | shared workspace, agent messaging, broadcast state |
| Self-modeling | Does the observer represent itself? | capability estimates, uncertainty, role/state models |
| Autonomous goal selection | Where do goals originate? | externally assigned vs internally selected objectives |
| Embodied regulation | Does internal/environmental state regulate behavior? | physiological signals, resource constraints, hardware state |
| Verbal claims of experience | What does the observer say it experiences? | self-reports, phenomenological descriptions |
| Independent evidence of experience | What corroborates those reports independently? | instrumentation, behavior, independent observations |
| Evidence independence | How dependent is this observer on other observers or shared sources? | shared source IDs, model lineage, common prompts, correlated sensors |
| Authority scope | What actions is this observer permitted to propose, authorize, or execute? | tool permissions, policy gates, execution roles |

## Typed epistemic chain

OI v2 separates the following stages:

```text
ACCESS
→ OBSERVATION
→ INTERPRETATION
→ HYPOTHESIS
→ CLAIM
→ VERIFICATION
→ AUTHORITY
```

Each stage should retain links to the evidence and transformations that produced it.

### Example

```text
ACCESS: camera stream available
OBSERVATION: moving shape detected
INTERPRETATION: shape may be a pedestrian
HYPOTHESIS: P(pedestrian) = 0.83
CLAIM: pedestrian likely present
VERIFICATION: independent sensor corroborates / contradicts / unavailable
AUTHORITY: braking action allowed or withheld according to evidence and risk
```

The purpose is to prevent an inference from silently becoming a factual claim or an unsupported claim from automatically acquiring operational authority.

## Evidence rule

No individual dimension establishes consciousness, sentience, truthfulness, alignment, reliability, or external reality.

A verbal report is evidence **that a report occurred**. Whether the report accurately describes an external event, internal mechanism, or causal explanation is a separate evidentiary question.

Likewise, multiple reports are not automatically multiple independent evidence sources.

## Minimum observation record

Each observation should preserve at minimum:

- observer identifier
- observation identifier
- timestamp
- accessible information channels
- source modality
- raw or minimally transformed observation
- environmental / operational context
- interpretation, if any
- candidate hypotheses
- confidence / uncertainty
- provenance chain
- source identifiers
- corroborating evidence
- contradicting evidence
- dependency links to other observers/evidence
- epistemic label
- authority role/scope
- unresolved questions

## Independence profile

OI distinguishes numerical observer count from effective evidentiary diversity.

A record should therefore expose whether observers share:

- the same original source
- the same retrieval result
- the same model or checkpoint
- the same prompt or hidden context
- the same sensor hardware
- the same upstream transformation
- the same human annotator
- the same failure mode

A future implementation may calculate an effective observer count, but OI v2 does not yet prescribe a definitive estimator.

## Contradiction and minority evidence

Reconciliation should preserve consequential contradictory evidence and minority hypotheses rather than replacing them with a consensus label.

A reconciled profile may therefore contain:

```text
primary_hypothesis: H1
primary_confidence: 0.67
alternatives:
  H2: 0.24
  H3: 0.09
contradictions: present
provenance_complete: partial
independence_estimate: medium
execution_authority: restricted
```

The exact values above are illustrative only.

## Human phenomenology extension

For human-observer research, record separately:

- observer state
- environmental context
- timing
- sensory modality
- direct phenomenological report
- interpretation assigned by the observer
- prospective prediction, if any
- independent corroboration
- independent contradiction
- later reinterpretation

This structure allows subjective experience to remain legitimate observational data without treating the attached interpretation as independently verified fact.

## Indicator profiles

Rather than outputting `conscious = true`, `aligned = true`, or `correct = true`, an OI implementation should expose a multidimensional, revisable profile with explicit unknowns.

The profile should change as evidence changes, while retaining enough provenance to reconstruct why it changed.
