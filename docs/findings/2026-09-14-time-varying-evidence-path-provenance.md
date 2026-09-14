# Time-Varying Evidence-Path Provenance

**OI research timestamp:** 2026-09-14  
**Status:** Architectural refinement / research specification. The motivating networking work is treated as enabling evidence and analogy, not validation of Observer Intelligence.

## Research consequence

Observer Intelligence should model trust as a property of the **evidence pathway at the time an observation was produced and transported**, not as a permanent scalar attached to an observer, device, model, institution, or channel.

A verified observer can still produce weak evidence if its sensor, clock, transport path, shared source, calibration state, or environment is degraded. Likewise, two authenticated observers may not constitute two independent evidence pathways if they share the same upstream sensor, stream, model, clock, network path, or correction subsystem.

Core distinction:

```text
observer identity
!= channel identity
!= channel quality
!= evidence independence
!= evidentiary support
!= authorization
```

## Proposed provenance object

```text
evidence_path:
  observer_id
  observer_credential
  source_modality
  source_id
  direct_or_mediated
  transport_medium
  channel_id
  capture_time
  receive_time
  clock_id
  synchronization_source
  synchronization_uncertainty
  channel_state
  measurement_uncertainty
  calibration_state
  authentication_method
  shared_dependencies
  transformation_lineage
  evidence_hash
```

The exact schema remains experimental. Implementations may represent these fields differently, but the distinctions should remain inspectable where they affect inference or authority.

## OI architecture connection

This refinement strengthens:

- **distributed observer trust** by separating observer identity from current pathway quality;
- **runtime separation of authority** by preventing authenticated transport from silently granting evidentiary or operational authority;
- **synchronization** by preserving clock source, offset/uncertainty, and event-to-reconciliation timing;
- **authentication** by distinguishing who produced or transported evidence from whether the underlying measurement is reliable;
- **provenance** by preserving source, channel, transformation, shared dependencies, and temporal state;
- **reconciliation** by allowing support to be discounted when seemingly separate observations share a dependency or degraded pathway.

## Integration with Blind Observer Sampling

Blind Observer Sampling reduces informational contamination between observers, but blinding alone does not guarantee independent evidence.

A stronger pipeline is:

```text
BLINDED OBSERVERS
        |
        v
SEALED / PRECOMMITTED RESPONSES
        |
        v
EVIDENCE-PATH PROVENANCE
  - source modality
  - transport path
  - clock/synchronization state
  - measurement quality
  - shared dependencies
        |
        v
DEPENDENCE ANALYSIS
        |
        v
PROVENANCE-PRESERVING RECONCILIATION
        |
        v
AUTHORITY GATE
```

Thus:

```text
N_observers != N_authenticated_observers != N_independent_evidence_pathways
```

## Suggested benchmark

Add a benchmark in which observer count is held constant while pathway conditions vary:

1. independent observers + independent sources/paths;
2. independent observers + shared upstream sensor;
3. independent observers + shared transport or clock dependency;
4. mixed-quality paths with time-varying loss/noise/latency;
5. one compromised or stale pathway;
6. blinded vs socially exposed observers under the same physical-path conditions.

Measure:

- calibration;
- false-corroboration rate;
- dependence-adjusted effective observer count;
- contradiction retention;
- stale-data detection;
- timing-ordering error;
- reconciliation accuracy;
- downstream authorization error.

## Framework rule

> Trust should attach to the evidence pathway at the time of the event, not permanently to the observer.

A high-trust observer should not be able to carry historical reputation across a degraded or unverifiable path without explicit provenance and uncertainty accounting.

## Claim boundary

This refinement does **not** claim that quantum networking, QKD, photonic timing, or heterogeneous communications validate OI. Those systems are useful because they make channel state, synchronization, authentication, modality, and shared infrastructure explicit enough to expose design distinctions that also matter in distributed observational systems.

Likewise, heterogeneous physical channels do not automatically create independent evidence. Independence must be assessed from actual source and dependency lineage.
