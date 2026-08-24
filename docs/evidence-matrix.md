# Observer Intelligence Evidence Matrix

## Purpose

The Observer Intelligence Evidence Matrix (OIEM) is a structured method for describing an observer without converting a complex evidence profile into a single categorical judgment.

It can be applied to AI agents, multi-agent systems, human–AI research settings, simulated agents, and other systems where claims about observation, agency, internal state, or experience require careful evidentiary separation.

## Dimensions

| Dimension | Core question | Example evidence |
|---|---|---|
| Sensory / data access | What can the observer actually access? | sensors, APIs, files, environmental measurements |
| Memory continuity | What persists across time? | logs, persistent state, recalled information |
| Global information availability | Where can observed information propagate? | shared workspace, agent messaging, broadcast state |
| Self-modeling | Does the observer represent itself? | capability estimates, uncertainty, role/state models |
| Autonomous goal selection | Where do goals originate? | externally assigned vs internally selected objectives |
| Embodied regulation | Does internal/environmental state regulate behavior? | physiological signals, resource constraints, hardware state |
| Verbal claims of experience | What does the observer say it experiences? | self-reports, phenomenological descriptions |
| Independent evidence of experience | What corroborates those reports independently? | behavioral signatures, instrumentation, third-party observations |

## Evidence rule

No individual dimension establishes consciousness, sentience, truthfulness, alignment, or reliability.

A verbal report is evidence **that a report occurred**. Whether the report accurately describes an external event or internal mechanism is a separate evidentiary question.

## Suggested record

Each observation should preserve at minimum:

- observer identifier
- observation identifier
- timestamp
- source modality
- raw or minimally transformed observation
- interpretation, if any
- confidence
- provenance chain
- corroborating evidence
- contradicting evidence
- epistemic label
- unresolved questions

## Indicator profiles

Rather than outputting `conscious = true` or `aligned = true`, an OI implementation should expose a multidimensional profile with explicit unknowns.

Example:

```text
sensory_access: high
memory_continuity: medium
information_availability: high
self_modeling: medium
 autonomous_goal_selection: low
embodied_regulation: unknown
verbal_experience_claims: present
independent_experience_evidence: insufficient
```

The profile should be revisable as evidence changes.
