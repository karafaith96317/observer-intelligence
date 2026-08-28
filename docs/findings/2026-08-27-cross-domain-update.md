# Observer Intelligence — Cross-Domain Research Update

**Date added:** 2026-08-27  
**Status:** External evidence integration; does not by itself validate OI

This note records newly surfaced or newly relevant research that materially intersects Observer Intelligence (OI). Each entry separates the external finding from the OI interpretation and classifies the relationship as **supports**, **challenges**, **duplicates/prior art**, or **suggests a test**.

---

## 1. Adversarial comparison of IIT, predictive processing / active inference, and neurorepresentationalism

**Source:** Corcoran, A. W., Haun, A. M., Dorman, R., Tononi, G., Friston, K. J., Pennartz, C. M. A., & TWCF: INTREPID Consortium (2026). “Integrated information and predictive processing theories of consciousness: An adversarial collaborative review.” *Neuroscience & Biobehavioral Reviews*, 187, 106742. DOI: 10.1016/j.neubiorev.2026.106742.  
https://doi.org/10.1016/j.neubiorev.2026.106742

**What it says.** The review compares Integrated Information Theory, Neurorepresentationalism, and Active Inference / predictive-processing approaches and explicitly frames progress in terms of structured adversarial collaboration: competing theories should make discriminating predictions against shared evidence rather than merely explaining results after the fact.

**OI connection.** Counterfactual hypothesis preservation; multi-observer disagreement; reconciliation without premature collapse; shared evidence standards.

**Classification:** **Supports + suggests a test.**

**Research consequence.** OI should distinguish ordinary disagreement from **predeclared competing hypotheses evaluated against the same observation set**. A candidate OI benchmark can require each observer/theory to register discriminating predictions before the result is revealed.

```text
H1, H2, H3
-> same observations
-> predeclared discriminating predictions
-> evidence update
-> reconciliation that preserves losing-hypothesis lineage
```

This strengthens the idea that reconciliation quality is not just “who won?” but also whether the system preserves why one hypothesis gained or lost support.

---

## 2. Privacy in continuous-variable distributed quantum sensing

**Source:** de Oliveira Junior, A., Andersen, A. L., Larsen, B. L., Moore, S. W., Markham, D., Takeoka, M., Brask, J. B., & Andersen, U. L. (2026). “Privacy in Continuous-Variable Distributed Quantum Sensing.” *PRX Quantum* 7, 033036. Published 21 August 2026. DOI: 10.1103/1zsz-clqx.  
https://doi.org/10.1103/1zsz-clqx

**What it says.** A distributed quantum-sensing network can estimate a global quantity such as an average phase while withholding individual local phase values. The work also proves a limitation: for three or more parties, finite-energy Gaussian probes cannot provide complete privacy of all unwanted phase combinations. Optical loss and displacement introduce explicit precision/privacy trade-offs.

**OI connection.** Selective disclosure; collective inference from locally private observers; disclosure boundaries; distributed observation.

**Classification:** **Supports + constrains + duplicates adjacent territory.**

**Research consequence.** OI should not represent selective disclosure as a free binary property. Introduce a prospective **disclosure/leakage budget** or privacy-loss metadata field:

```text
collective inference != free perfect privacy
```

Candidate fields include:

- information intentionally disclosed;
- information inferable from the aggregate;
- residual leakage estimate;
- resource/cost required for greater privacy;
- accuracy loss associated with privacy restrictions;
- network-size dependence.

This paper is also prior art for privacy-preserving distributed inference; OI's research question remains how such disclosure limits interact with epistemic state, provenance, dependence, reconciliation, and authority.

---

## 3. Predictive dysfunction as a mechanism-based psychiatry framework

**Source:** van Fenema, E. M. & Jacobs, G. E. (2026). “Predictive dysfunction: toward a unifying mechanism-based framework for psychiatry.” *Translational Psychiatry*. Published 4 August 2026. DOI: 10.1038/s41398-026-04356-0.  
https://doi.org/10.1038/s41398-026-04356-0

**What it says.** The authors propose “predictive dysfunction” as a transdiagnostic framework in which psychiatric phenomena can arise from different configurations of hierarchical predictive inference, including miscalibrated priors, prediction errors, precision weighting, and failures of belief updating. The proposal is mechanistic rather than a claim that one single computational defect explains all disorders.

**OI connection.** Human-observer modeling; altered-state predictive processing; separation of sensory evidence, prior weighting, confidence, and belief updating.

**Classification:** **Supports + suggests measurement design.**

**Research consequence.** OI should avoid generic statements such as “strong priors caused the experience” or “weak priors caused the experience.” Human-observer records should preserve at least:

```text
sensory precision
!= prior precision
!= decision precision
!= confidence
!= belief-update dynamics
```

Where feasible, these should be treated as time-varying rather than fixed subject traits.

### Related active/prospective study design

**PREDiCTOR** — “Computational phenotyping and predictive modeling of outcomes using multimodal objective measures in psychiatry” (2026) describes prospective multimodal modeling using audiovisual clinical data, EHR data, cognitive assessments, passive smartphone sensing, therapeutic-alliance measures, and audio/text diaries, with model estimates updated as new information arrives. Large language models are described as feature extractors rather than clinical decision-makers. PubMed PMID: 42556642.  
https://pubmed.ncbi.nlm.nih.gov/42556642/

**OI relevance.** This suggests a concrete methodological precedent for **dynamic observer-state updating from heterogeneous evidence**, while preserving the distinction between measurement/feature extraction and decision authority.

---

## 4. Psychedelics and astrocytes / neuro-glial integration

**Source:** Ke, X., Du, X. & Wang, X. (2026). “Psychedelics and astrocytes: a hypothesis-driven perspective on neuro-glial integration, network plasticity, and neuroimmune reprogramming.” *Molecular Psychiatry*. Published 11 August 2026. DOI: 10.1038/s41380-026-03816-9.  
https://doi.org/10.1038/s41380-026-03816-9

**What it says.** The review argues that neuron-centric psychedelic models focused mainly on 5-HT2A receptor signaling may be incomplete and proposes that astrocytes could contribute to psychedelic-induced network plasticity, neuro-glial integration, and neuroimmune regulation. The authors explicitly present this as a hypothesis-driven perspective, not an established replacement mechanism.

**OI connection.** Multilevel observer-state representation; altered-state dynamics; resistance to single-variable explanations.

**Classification:** **Challenges oversimplification + suggests a test.**

**Research consequence.** OI's human-observer branch should not assume a simple one-receptor → one-network-state → one-experience chain. A more defensible multilevel representation is:

```text
receptor signaling
+ neuronal network dynamics
+ glial regulation
+ immune / metabolic context
+ environmental context
+ temporal trajectory
-> experienced state
```

This does not mean all listed variables are necessary in every study. It means candidate causal layers should remain distinguishable until evidence supports compression.

---

# Cross-domain synthesis for OI

These four developments arise in very different fields, so resemblance should not be treated as proof of one universal theory. However, together they motivate a sharper OI research proposition:

> **A global conclusion should retain enough causal, temporal, dependence, disclosure, and measurement structure to reconstruct why that conclusion was justified.**

This extends the existing OI distinction:

```text
Outcome correctness != epistemic-process correctness
```

A system may reach the correct action while using an incorrect independence estimate, stale evidence, hidden leakage, missing causal structure, or an invalid confidence transformation.

Future OI evaluations should therefore score separately:

1. final authority/action correctness;
2. claim correctness;
3. evidence-strength estimation;
4. observer/evidence dependence estimation;
5. temporal/staleness handling;
6. provenance reconstruction;
7. disclosure/leakage accounting;
8. uncertainty/calibration;
9. decision revision after new evidence;
10. ability to reconstruct the causal/epistemic path to the final conclusion.

## Working synthesis hypothesis

```text
state
+ context
+ temporal structure
+ measurement integrity
+ causal / transformation lineage
+ source dependence
+ disclosure structure
+ uncertainty
+ provenance
```

may contain decision-relevant information that is destroyed by premature reduction to a single confidence score, majority vote, aggregate neural measure, diagnostic label, or binary privacy flag.

**Claim boundary:** This is a research synthesis and data-modeling hypothesis. The cited studies do not establish Observer Intelligence as a validated universal framework.
