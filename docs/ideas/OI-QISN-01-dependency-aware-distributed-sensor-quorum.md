# OI-QISN-01 — Dependency-Aware Distributed Sensor Quorum

**Status:** Candidate research idea / benchmark proposal  
**Added:** 2026-10-03  
**OI areas:** adaptive observer quorums; distributed observation; provenance; shared failure domains; quantum sensing

## Motivation

An NSF-funded project led by Hyeongrak “Chuck” Choi (Stony Brook University) and Bo-Han Wu (University of Hawaiʻi at Mānoa) is investigating **Quantum Intelligent Sensor Networks (QISNs)**: spatially distributed quantum sensors coordinated as a network, including distribution of entanglement and other quantum resources across sensing nodes to improve extraction of weak and spatially varying signals.

The project is a three-year, $600,000 NSF award that began June 1, 2026. It is an active research program, not yet evidence that the proposed network architecture improves every sensing or inference task.

This work provides a useful physical comparison case for an OI question:

> Does adding observers increase corroborative evidence when those observers share physical, informational, calibration, timing, model, or network dependencies?

## OI hypothesis

Observer count alone should not determine quorum confidence.

A naive quorum might behave approximately as:

```text
Q_naive = N_observers
```

OI should instead test a dependency-aware quantity such as:

```text
Q_OI = f(
  N_observers,
  modality_diversity,
  physical_failure_domain_diversity,
  source_diversity,
  network_path_diversity,
  clock_and_calibration_dependencies,
  observer_reliability,
  uncertainty,
  dependency_strength
)
```

This is a **candidate formulation**, not an established metric.

## Proposed experiment

Hold the number of observers/sensors constant while manipulating dependence.

Candidate conditions:

1. independent sensors with independent failure domains;
2. multiple sensors sharing a clock;
3. multiple sensors sharing calibration bias;
4. multiple sensors sharing a network/transport path;
5. multiple sensors exposed to correlated environmental noise;
6. heterogeneous modalities with partly independent failure domains;
7. many correlated sensors plus one genuinely independent sensor;
8. a sensor network whose dependencies change over time.

Inject controlled failures and measure whether reconciliation distinguishes numerical agreement from independent corroboration.

### Primary outcomes

- false-corroboration rate;
- dependency-detection accuracy;
- calibration;
- provenance completeness;
- minority-evidence retention;
- unsafe authorization rate;
- robustness to correlated noise;
- performance as dependency structure changes.

## Provenance requirement

Each observation should preserve enough dependency metadata to reconstruct relevant common causes where available:

```text
observation -> sensor/observer
            -> modality
            -> physical substrate
            -> calibration lineage
            -> clock/synchronization source
            -> transport path
            -> transformations
            -> shared upstream dependencies
            -> event/capture/readout time
```

A useful invariant to test is:

```text
N observers != N independent evidence pathways
```

## Relationship to recent OI research

This idea extends the shared-fibre sensing/communications finding recorded in:

`docs/findings/2026-10-01-fibre-sensing-communication-shared-substrate.md`

That work provides a concrete example of sensing and communication sharing physical infrastructure. QISN research provides a complementary case in which multiple spatially distributed sensors are intentionally coordinated.

Together they motivate explicitly testing **failure-domain independence** rather than treating physical or logical multiplicity as sufficient evidence of independence.

## Claim boundary

The QISN project does **not** validate Observer Intelligence, adaptive epistemic quorums, or OI provenance mechanisms. Quantum entanglement is not being proposed here as a mechanism for AI consensus or epistemic authority. The project is external research that supplies a useful distributed-sensing architecture and prospective comparison case.

OI's contribution would be the falsifiable question of how dependency structure should alter evidentiary weight and authorization in distributed observation.

## External source

Stony Brook University, “Choi Co-Leads Research on Next Generation Quantum Sensors,” 17 September 2026.

https://news.stonybrook.edu/?p=264312

Reported project facts: $600,000 NSF award; three-year project beginning June 1, 2026; collaboration between Stony Brook University and the University of Hawaiʻi at Mānoa; research on coordinated spatially distributed quantum sensors and distributed quantum resources.
