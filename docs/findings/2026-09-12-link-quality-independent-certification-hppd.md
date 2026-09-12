# OI Research Integration — Link Quality, Independent Certification, and HPPD

**Integration date:** 2026-09-12

This note records three newly surfaced sources that materially intersect Observer Intelligence (OI). Inclusion is attribution-aware: external work is credited for the result it actually establishes, and analogy to OI is not treated as validation of OI.

---

## 1. Engineering quantum links with time-, modality-, and interference-aware quality metrics

**Source.** Marcello Caleffi, Laura d'Avossa, Angela Sara Cacciapuoti, “Engineering Quantum Links: Noise and Quantum-State-Degradation Metrics over Metropolitan Fiber Network,” arXiv:2609.11359, submitted 10 September 2026. https://arxiv.org/abs/2609.11359

**Status.** Preprint. The reported link characterization is based on experimental measurements on a 7.3 km deployed metropolitan fiber loop in the QuantumInternet.it testbed; peer review and independent replication remain outstanding.

**External contribution.** The authors quantify intrinsic noise, interference from classical traffic, and channel-induced degradation for polarization, time, and frequency encoding, including drift over time. Their engineering framing treats link quality as a measurable, decomposable state rather than a permanent scalar property.

**OI connection.** Adaptive observer quorums; measurement integrity; temporal provenance; modality provenance; interference/common-cause dependence; dynamic evidence quality.

**Effect on OI.** **Supports an architectural principle + suggests a benchmark.** It strengthens the case for representing evidence-path reliability as time-, modality-, environment-, and interference-dependent rather than assigning a permanent trust score to an observer or channel. It is not an OI implementation and does not imply that OI requires quantum networking.

**Research consequence.** Candidate OI evidence-path metadata should preserve, where relevant:

```text
source -> modality -> transformation -> interference/environment -> timestamp -> quality estimate -> uncertainty
```

A benchmark should introduce temporal drift, shared interference, modality-specific degradation, and common-cause failures, then compare fixed trust/quorum policies against adaptive dependence-aware reconciliation.

---

## 2. Separate adaptive discovery from independent certification

**Source.** Jean Cortés, Luciano Pereira, Aldo Delgado, “Self-guided certification of nonlocality in quantum networks,” arXiv:2609.11451, submitted 10 September 2026. https://arxiv.org/abs/2609.11451

**Status.** Preprint. The protocol is validated numerically in the reported work; peer review, experimental implementation, and independent replication remain outstanding.

**External contribution.** The protocol variationally searches for measurement settings that maximize violation of a network Bell inequality using classical-shadow-assisted evaluation and CSPSA. After convergence, the selected settings are implemented directly and the inequality is re-evaluated without the search approximation. The authors explicitly separate a device-dependent search stage from a certificate based on observed statistics and the assumed network causal structure.

**OI connection.** Runtime separation of roles; independent adjudication; provenance-preserving verification; evidence reconstruction; authority separation.

**Effect on OI.** **Strong architectural analogy + suggests a test.** It supports a general design principle already relevant to OI:

```text
discovery / optimization != certification / authorization
```

The external work should be credited as a concrete quantum-network example of a two-stage search/certification architecture. OI's broader claim concerns preserving epistemic and authority lineage across heterogeneous observers and consequential action.

**Research consequence.** Candidate OI workflow:

```text
GENERATE / SEARCH
-> freeze candidate and search provenance
-> independent evidence reconstruction
-> CERTIFY / ADJUDICATE
-> AUTHORIZE, DEFER, or REJECT
```

A benchmark should deliberately bias or manipulate the discovery process while keeping the certification evidence fixed, then test whether the independent certification layer rejects unsupported conclusions. Reciprocal tests should also corrupt the verifier while preserving valid source evidence to localize which layer failed.

---

## 3. HPPD case: persistent perceptual disturbance should remain distinct from psychosis, mood, and interpretation

**Source.** Sonali Notani, Vikas Srinivasa, Serena Chaudhry, Ashley Weiss, “Hallucinogen Persisting Perception Disorder in a Young Adult Case Report,” *Case Reports in Psychiatry* (2026), published 3 September 2026, DOI: 10.1155/crps/6605265, PMID: 42694657. https://pubmed.ncbi.nlm.nih.gov/42694657/

**Status.** Peer-reviewed case report. This is a single-patient clinical observation and cannot establish prevalence, mechanism, general treatment effectiveness, or population-level causality.

**External contribution.** The report describes a 24-year-old with bipolar I disorder, generalized anxiety disorder, recent LSD exposure, mania, and psychosis. Mood and psychosis remitted with olanzapine while perceptual disturbances including visual snow persisted and fluctuated despite subsequent HPPD-directed treatment trials. The authors emphasize diagnostic distinction between HPPD and psychosis and the limited treatment evidence base.

**OI connection.** Human-observer evidence representation; altered-state phenomenology; longitudinal state tracking; source/interpretation separation; computational psychiatry.

**Effect on OI.** **Methodological support + challenge to overly unified altered-state models.** The case supports keeping perceptual alteration, salience, belief/interpretation, mood, psychotic symptoms, functional impairment, and treatment response as separate variables rather than collapsing them into a single “altered state.”

**Research consequence.** Candidate longitudinal fields include:

- perceptual alteration / visual phenomena
- salience attribution
- belief or interpretation
- mood state
- psychotic symptoms
- functional impairment
- substance/exposure timing
- medication/intervention timing
- confidence and distress
- independent clinical/behavioral evidence where available

For prospective altered-state studies, symptom persistence and belief interpretation should be analyzed separately from whether an external claim is independently verified.

---

## Combined OI implication

These sources reinforce three separations:

```text
observer identity != current evidence-path quality
search/discovery != certification/authorization
perceptual experience != interpretation != independently established external cause
```

A stronger OI architecture therefore treats reliability as dynamic, certification as independently reconstructable where possible, and human phenomenology as multidimensional rather than collapsing observation, interpretation, and external attribution.

## Attribution rule

If these sources materially influence future OI terminology, benchmark design, architecture, or implementation, retain author/title/source attribution and identify the specific OI modification they motivated. Independent convergence should remain labeled as convergence; prior art should remain labeled as prior art; analogies should not be represented as validation.