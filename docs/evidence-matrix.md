# Observer Intelligence Evidence Matrix — v2.1

## Purpose

The Observer Intelligence Evidence Matrix (OIEM) is a structured method for describing an observer and its evidence state without converting a complex profile into a single categorical judgment.

It can be applied to AI agents, multi-agent systems, human–AI research settings, simulated agents, distributed sensor systems, and other systems where claims about observation, agency, internal state, reliability, or experience require careful evidentiary separation.

OI v2.1 distinguishes **observer capacity** from **evidentiary trust between observers**. A capable observer can still produce unreliable evidence, and an authenticated record can still contain a physically inaccurate measurement.

## Observer capacity dimensions

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

## Evidence integrity dimensions

| Dimension | Core question |
|---|---|
| Measurement integrity | What are the sensor's calibration state, detection efficiency, false-positive/background rate, uncertainty, environmental interference, and hardware state? |
| Observer identity | Can the system establish which observer produced the observation? |
| Temporal provenance | Can event time, capture time, processing time, and reconciliation time be distinguished and reconstructed? |
| Cryptographic provenance | Can unauthorized alteration of the evidence or lineage be detected? |
| Evidence independence | How dependent is the observation on other observers, shared sources, common models, or upstream transformations? |

**Key distinction:** authenticated evidence is not necessarily accurate evidence. Cryptographic integrity can establish that a record was not altered without establishing that the originating sensor measured the world correctly.

## Distributed Observer Trust Fabric

OI v2.1 uses **Distributed Observer Trust Fabric (DOTF)** as a substrate-neutral term for mechanisms that preserve identity, timing, authentication, independence, disclosure boundaries, and provenance across multiple observers.

DOTF does not require quantum networking. Implementations may use classical cryptography, post-quantum cryptography, quantum networking/QKD where appropriate, or hybrid systems.

| Dimension | Core question |
|---|---|
| Pair / channel authentication | Were communicating observers or nodes mutually authenticated? |
| Observation independence | Was an observation generated before contamination by another observer's interpretation or conclusion? |
| Trust-domain integrity | Which observers, data flows, permissions, and transformations were allowed inside the observational context? |
| Cross-observer agreement | Which genuinely independent evidence pathways converge, and which merely repeat a shared source? |
| Selective disclosure | Can an observer contribute to an authorized collective inference without unnecessarily exposing its full local observation? |
| Minimum necessary reconciliation | Did reconciliation receive only the information required for the authorized conclusion? |
| Authority separation | Were observation, interpretation, reconciliation, authorization, and execution kept logically distinct where risk required it? |

## Observer Trust Domain

An **Observer Trust Domain (OTD)** is a logical/security boundary defining participating observers, permitted information flows, temporal scope, authentication state, disclosure permissions, and authority relationships.

The OTD is not a claim that current quantum networking creates a literal physical protective "bubble." It is an architectural abstraction for bounded observational relationships.

## Typed epistemic chain

```text
PHYSICAL / INFORMATION ENVIRONMENT
→ ACCESS
→ OBSERVATION
→ MEASUREMENT-INTEGRITY CHECK
→ INTERPRETATION
→ HYPOTHESIS
→ CLAIM
→ VERIFICATION
→ SELECTIVE DISCLOSURE
→ RECONCILIATION
→ AUTHORIZATION
→ ACTION
```

Each stage should retain links to the evidence and transformations that produced it.

## Temporal provenance

Where timing matters, a record should distinguish at minimum:

- event time
- capture time
- processing time
- reconciliation time
- synchronization source and uncertainty, when available

Precision timing is treated as an enabling infrastructure for evidentiary ordering, not as proof that an observation is true.

## Minimum observation record

Each observation should preserve at minimum:

- observer identifier
- observation identifier
- event/capture timestamp(s)
- synchronization source and timing uncertainty, where relevant
- accessible information channels
- source modality
- raw or minimally transformed observation
- sensor calibration / measurement-integrity metadata where relevant
- environmental / operational context
- interpretation, if any
- candidate hypotheses
- confidence / uncertainty
- provenance chain
- source identifiers
- corroborating evidence
- contradicting evidence
- dependency links to other observers/evidence
- disclosure boundary
- epistemic label
- authority role/scope
- unresolved questions

## Independence profile

OI distinguishes numerical observer count from effective evidentiary diversity.

A record should expose whether observers share the same original source, retrieval result, model/checkpoint, prompt/context, sensor hardware, upstream transformation, human annotator, synchronization dependency, or failure mode.

## Selective disclosure and minimum necessary reconciliation

OI v2.1 adds a privacy-preserving design objective:

> An observer should reveal only the information necessary to establish the authorized collective conclusion, where the task and threat model permit it.

This does not imply that every OI implementation can or should use quantum-private sensing. It means the reconciliation layer should explicitly model **what information was disclosed, to whom, and why**.

Research on private distributed quantum sensing provides an adjacent technical precedent: spatially separated nodes can be designed to estimate global functions while limiting information leakage about individual local parameters, with important precision/privacy/resource trade-offs in realistic Gaussian networks.

## Provenance-preserving reconciliation

A reconciled result should preserve:

- agreement
- disagreement
- uncertainty
- missing evidence
- disclosure boundaries
- transformation history
- authority history
- retained source lineage

Disagreement is evidence. Reconciliation should not silently erase consequential contradictory observations or minority hypotheses.

## Evidence rule

No individual dimension establishes consciousness, sentience, truthfulness, alignment, reliability, or external reality.

A verbal report is evidence **that a report occurred**. Whether the report accurately describes an external event, internal mechanism, or causal explanation is a separate evidentiary question.

Likewise, multiple reports are not automatically multiple independent evidence sources.

## Human phenomenology extension

For human-observer research, record observer state, environmental context, timing, sensory modality, direct phenomenological report, interpretation assigned by the observer, prospective prediction if any, independent corroboration, independent contradiction, and later reinterpretation separately.

## Indicator profiles

Rather than outputting `conscious = true`, `aligned = true`, or `correct = true`, an OI implementation should expose a multidimensional, revisable profile with explicit unknowns.

The profile should change as evidence changes, while retaining enough provenance to reconstruct why it changed.

## Research foundations for v2.1 additions

1. Alushi, U. & Di Candia, R. **Privacy in distributed quantum sensing with Gaussian quantum networks.** *npj Quantum Information* 12, 132 (2026). DOI: 10.1038/s41534-026-01266-3. https://www.nature.com/articles/s41534-026-01266-3
   - Supports the adjacent precedent for privacy-preserving distributed estimation and explicitly identifies privacy/precision/resource trade-offs. It does **not** establish OI itself.

2. Brookhaven National Laboratory / Stony Brook University. **Brookhaven and Stony Brook Researchers Demonstrate 'Wireless' Capability for Quantum Network.** 21 Aug 2026. https://news.stonybrook.edu/newsroom/press-release/general/brookhaven-and-stony-brook-researchers-demonstrate-wireless-capability-for-quantum-network/
   - Reports free-space transmission of quantum information and nighttime distribution/measurement of entangled photons across the Brookhaven–Stony Brook link. Supports transport-independence as a forward-looking design consideration.

3. Loughborough University. **'Rainbow-on-a-chip' breakthrough could help unlock 6G networks and precision timing for quantum technologies.** 21 Aug 2026. https://www.lboro.ac.uk/media-centre/press-releases/2026/august/microcomb-6g-quantum-technologies/
   - Reports a stable optical microcomb converted into multiple precisely spaced millimetre-wave signals and identifies precision timing as a potential application. Supports treating synchronization quality as an explicit evidentiary variable; it does not prove OI synchronization requirements.

4. NIST. **NIST Researchers Supersize Quantum Technology to Help Detect Faint Photons.** 24 Aug 2026. https://www.nist.gov/news-events/news/2026/08/nist-researchers-supersize-quantum-technology-help-detect-faint-photons
   - Reports superconducting single-photon detector wires up to 0.1 mm wide and a billion-fold reduction in dark counts in the reported experiments; NIST explicitly notes that equivalent 98% detection efficiency has not yet been established for the wide architecture. Supports separating measurement integrity from authentication/provenance.

5. NIST. **'Spooky' Particles Transit DC Suburbs, a Step Toward a Quantum Network.** 5 Aug 2026. https://www.nist.gov/news-events/news/2026/08/spooky-particles-transit-dc-suburbs-step-toward-quantum-network
   - Reports entanglement distribution over 62 km of commercial/aerial fiber with real-time polarization stabilization. Supports the practical importance of channel state, environmental disturbance, and correction metadata in distributed observation infrastructure.

These references are **supporting adjacent research**, not evidence that OI has been experimentally validated.