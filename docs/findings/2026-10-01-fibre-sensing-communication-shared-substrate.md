# Fibre sensing + communication as a shared observation substrate

**Integrated:** 2026-10-01  
**Source publication date:** 2026-09-25  
**Status:** Peer-reviewed article, *Nature Communications*  
**Classification for OI:** adjacent technological prior art; suggests a test; distributed-observation enabling analogue. **Not evidence validating OI's epistemic framework.**

## External finding

Hu, Zihe; Zhang, Youmin; Zhang, Mingming; Wen, Hao; Wang, Jun; Li, Yuqi; Chen, Yizhao; Chen, Junda; Cheng, Chen; Zhao, Luming; Zhao, Can; Shi, Lei; and Tang, Ming. “Holistic co-design of fibre-optic distributed acoustic sensing and coherent communication.” *Nature Communications* (2026). DOI: 10.1038/s41467-026-78056-0.

The authors report a co-designed sensing-and-communication (CSAC) fibre architecture that shares signal, hardware, and network resources rather than merely colocating sensing and communications. The demonstrated design uses a dual-function pilot, a single transmitter for multi-tone pilot and subcarrier communications, and a point-to-multipoint network. The paper reports multi-point frequency synchronization accuracy of 1.56 MHz, acoustic sensing response to 12 kHz, and extension to 28 kHz with on-chip modulators.

## OI connection

The relevant OI point is architectural, not evidentiary validation:

```text
network transport
+ environmental sensing
can share physical substrate
```

A communications path may therefore also participate in observation. OI provenance should represent the physical and logical dependencies behind an observation, because two nominally different evidence channels can share infrastructure and therefore share failure modes.

This sharpens an existing OI distinction:

```text
different sensors != independent evidence
different observers != independent evidence
shared physical substrate -> possible shared failure domain
```

## Research consequence

Add **failure-domain independence** to distributed-observer/quorum experiments.

Hold observer count constant while varying:

1. independent sensors on independent infrastructure;
2. different sensors sharing a communications substrate;
3. sensing embedded in the communications substrate;
4. one corrupted/degraded shared physical path;
5. cross-modal evidence with and without common clocks, power, network, correction, or synchronization dependencies.

Measure false corroboration, provenance completeness, detection of shared dependencies, calibration, and authorization error.

A candidate provenance representation should preserve enough information to identify common failure domains:

```text
evidence_path = {
  observer,
  modality,
  physical_substrate,
  transport_path,
  clock_or_sync_dependency,
  transformation_lineage,
  shared_upstream_dependencies,
  event_time,
  capture_time,
  integrity_state
}
```

## Claim boundary

This paper demonstrates a fibre-optic sensing/communications architecture. It does **not** demonstrate Observer Intelligence, epistemic independence, provenance-aware reconciliation, adaptive observer quorums, or that shared-substrate sensing necessarily improves decision quality. Its relevance to OI is as physical prior art and as motivation for explicit shared-failure-domain tests.

## Citation

Hu, Z., Zhang, Y., Zhang, M. et al. Holistic co-design of fibre-optic distributed acoustic sensing and coherent communication. *Nature Communications* (2026). https://doi.org/10.1038/s41467-026-78056-0

Primary source: https://www.nature.com/articles/s41467-026-78056-0
