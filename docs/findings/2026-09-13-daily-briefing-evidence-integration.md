# 2026-09-13 — Daily briefing evidence integration

This record integrates only source-checked material from the 2026-09-13 briefing and applies the repository evidence-status boundary in `docs/EVIDENCE_STATUS.md`.

## 1. Sabazios vessel at Collet — symbolic attribution requires contextual evidence

**Evidence status:** VERIFIED EXTERNAL EVIDENCE / peer-reviewed archaeological research.

Bouzas Sabater et al. reported fragments of a large Augustan-period ceramic vessel from the Roman villa of Collet in north-eastern Spain. The preserved handle is decorated as a two-headed serpent. The study combines formal comparison, laboratory analysis, and 3D modelling and argues that the iconography is linked to the Thracian/Phrygian god Sabazios. The ceramic paste may indicate an origin outside Europe. The authors also place the find alongside related evidence from nearby Emporiae and other Iberian contexts.

**What is established:** the artifact, its archaeological context, material properties, serpent imagery, and the authors' comparative analysis.

**What remains interpretive:** that this specific vessel was used in Sabazios ritual practice. The paper argues for that association; the artifact is not itself an inscribed declaration of cult identity.

**OI effect:** supports a benchmark for preventing pattern resemblance from silently becoming categorical identification. Suggested lineage:

```text
artifact observation
-> material/context evidence
-> iconographic comparison
-> candidate attribution
-> uncertainty / competing explanations
-> historical conclusion
```

**Research consequence:** archaeological and symbolic inference should be represented as typed transitions with source-specific uncertainty rather than collapsing `symbol -> identity`.

**Source:**
- Bouzas Sabater, M. et al., “Of snakes and gods: early evidence for the cult of Sabazios in the Roman villa of Collet,” *Antiquity* (2026), DOI 10.15184/aqy.2026.10420: https://www.cambridge.org/core/journals/antiquity/article/of-snakes-and-gods-early-evidence-for-the-cult-of-sabazios-in-the-roman-villa-of-collet/A96472EA586EA1FFA9E5889BE99BF9DE

---

## 2. Human tau pathology and nontraveling slow waves — propagation quality is not equivalent to signal presence

**Evidence status:** VERIFIED EXTERNAL EVIDENCE / peer-reviewed neuroscience study.

Sharon et al. reported that frontal tau pathology in humans is associated with impaired unity and cortical propagation of non-REM slow waves, and that reduced slow-wave travel is associated with poorer overnight memory retention. The study used PET tau imaging and replicated/extended the result in an independent clinical cohort using cerebrospinal-fluid Alzheimer’s-disease markers.

**What is established:** an association among frontal tau pathology, impaired slow-wave propagation, and memory impairment in the studied cohorts.

**What is not established:** that altered slow-wave travel is the sole cause of Alzheimer’s memory loss, or that restoring traveling waves would by itself reverse disease.

**OI effect:** sharpens the distinction among signal existence, temporal/spatial propagation, pathway integrity, and system-level function.

**Suggested representation:** preserve separate fields for:

```text
signal_present
propagation_quality
synchronization_quality
temporal_integrity
pathway_dependence
measurement_uncertainty
```

**Research consequence:** distributed-observer systems should not equate “all nodes are active” with “information is propagating correctly or independently.”

**Source:**
- Sharon, O. et al., “Human tau pathology is associated with lonely, nontraveling slow waves linked to memory impairment,” *Nature Neuroscience* (published 11 September 2026), DOI 10.1038/s41593-026-02415-9: https://www.nature.com/articles/s41593-026-02415-9

---

## 3. NASA Artifact InSPECtor + NASA-IBM Lunar Foundation Model — measurement integrity and multimodal provenance

### 3A. Artifact InSPECtor

**Evidence status:** VERIFIED EXTERNAL EVIDENCE / active NASA citizen-science project.

NASA lists Artifact InSPECtor as an active citizen-science project in which volunteers help train tools used to remove artifacts from space-telescope data. The project is suitable for participation using a smartphone or laptop.

**OI effect:** strong real-world example of the distinction:

```text
authentic instrument record != verified external-world feature
```

A genuine detector output may contain an instrumental artifact. Provenance authenticates where data came from; it does not by itself establish that the apparent feature corresponds to an astronomical object.

**Suggested test direction:** model the workflow as:

```text
instrument output
-> artifact candidate
-> machine classification
-> independent human review
-> reconciled label
-> retraining / downstream use
```

and record where physical measurement integrity is assessed separately from data authenticity.

**Source:**
- NASA Citizen Science — Artifact InSPECtor listing: https://science.nasa.gov/citizen-science/

### 3B. NASA-IBM Lunar Foundation Model

**Evidence status:** VERIFIED EXTERNAL EVIDENCE / NASA-released open-source AI system.

NASA announced the NASA-IBM Lunar Foundation Model on 10 September 2026. The model is trained primarily on Lunar Reconnaissance Orbiter data and is publicly hosted for testing, with the complete codebase available on GitHub. NASA describes it as an open-source model built specifically for lunar science.

**OI effect:** creates a practical future benchmark for preserving provenance across heterogeneous planetary-data layers and distinguishing raw observations, preprocessing, model features, inference, confidence, and independent corroboration.

**What this does not establish:** that model outputs are ground truth, or that OI improves lunar-science performance. That would require a separate benchmark.

**Suggested experiment:** intentionally remove, corrupt, or down-weight one lunar data layer and test whether a provenance-aware OI wrapper can correctly surface the degraded evidence pathway and reduce overconfident downstream inference.

**Source:**
- NASA, “NASA, IBM Launch AI Foundation Model for Lunar Science,” 10 September 2026: https://science.nasa.gov/science-research/artificial-intelligence-lunar-foundation-model/

---

## 4. Hormuz / Saudi pipeline disruptions — observation, attribution, intent, and response must remain separate

**Evidence status:** VERIFIED EXTERNAL REPORTING / current-event case study, not a scientific study.

Reuters reported on 13 September 2026 that new strikes and shipping incidents in and around the Strait of Hormuz, together with the outage of Saudi Arabia’s East-West pipeline, were worsening energy disruption. Reuters also reported Houthi advances around Perim/Bab el-Mandeb and that responsibility for individual attacks and their strategic meaning remained contested or dependent on attribution claims from governments and armed groups.

**OI effect:** high-stakes case study for preserving the chain:

```text
physical observation
-> source / launch inference
-> actor attribution
-> intent inference
-> predicted consequence
-> authorization / response
```

**Research consequence:** authority thresholds should rise as claims become more consequential. A confirmed physical event should not automatically authorize a claim about perpetrator identity or intent without additional evidence.

**Additional systems insight:** the importance of an observation is state-dependent. When one energy route is degraded, evidence concerning another route can become more decision-critical. OI therefore needs dependency-graph context, not only claim-local confidence.

**Sources:**
- Reuters, “Oil prices jump more than 2% after new strikes on Saudi, Strait of Hormuz,” 13 September 2026: https://www.reuters.com/business/energy/oil-prices-jump-more-than-3-after-new-strikes-saudi-strait-hormuz-2026-09-13/
- Reuters, “Saudi pipeline outage threatens loss of 4% of global oil supply,” 13 September 2026: https://www.reuters.com/business/energy/saudi-pipeline-outage-threatens-loss-4-global-oil-supply-2026-09-13/
- Reuters, “New attacks in Hormuz and Saudi test nerves as war's spread worsens oil disruption,” 13 September 2026: https://www.reuters.com/business/energy/new-report-attack-strait-hormuz-shipping-fans-fears-threats-oil-supplies-2026-09-13/

---

## 5. NIST, IEEE, and NSF — external requirements and actionable research opportunities

### NIST AI Standards Zero Draft / TEVV-Athlon

**Evidence status:** VERIFIED EXTERNAL PROGRAM / standards opportunity.

NIST states that input received by **16 September 2026** on its AI Standards Zero Draft will be considered for the subsequent revision. NIST also states that public comment on the TEVV-Athlon Framework remains open through **6 October 2026**.

**OI effect:** directly relevant to process-level traceability, testing, evaluation, and documentation of agentic AI. This is an opportunity for a narrow contribution on reconstructable evidence-to-action lineage without claiming that NIST has adopted or validated OI.

**Sources:**
- https://www.nist.gov/artificial-intelligence/ai-standards
- https://www.nist.gov/artificial-intelligence/nists-ai-standards-zero-drafts-pilot-project-accelerate-standardization

### IEEE JSAC — Agentic AI for Intelligent Networks

**Evidence status:** VERIFIED EXTERNAL CALL FOR PAPERS / research-landscape signal.

The IEEE Communications Society lists **15 September 2026** as the manuscript deadline for the JSAC special issue “Agentic AI for Intelligent Networks.” The scope explicitly includes distributed, closed-loop, long-horizon autonomous agents in dynamic 6G-era networks.

**OI effect:** strong external confirmation that distributed autonomous networking is an active research domain where provenance, bounded authority, and adversarial reconciliation can be formulated as testable engineering problems. It does not validate OI itself.

**Source:**
- https://www.comsoc.org/publications/journals/ieee-jsac/cfp/agentic-ai-intelligent-networks

### NSF AI Datasets

**Evidence status:** VERIFIED EXTERNAL FUNDING OPPORTUNITY.

NSF 26-512, “Unlocking Dataset Value for AI-Enabled Scientific Discovery,” has a full-proposal deadline of **4 November 2026**. NSF states that the program supports AI-ready integration and automated analysis of scientific datasets, including feature extraction, metadata generation, robust data pipelines, dataset harmonization, integrity, security, and governance. Anticipated award scales include Planning Grants up to $200,000, Impact awards up to $2 million, and Flagship awards up to $5 million.

**OI effect:** potentially relevant to provenance-aware integration of heterogeneous scientific evidence, provided institutional eligibility and an eligible scientific dataset/application are established. It should not be framed as funding OI in the abstract.

**Source:**
- https://www.nsf.gov/funding/opportunities/ai-datasets-unlocking-dataset-value-ai-enabled-scientific-discovery

---

## Combined implication for OI

Across archaeology, neuroscience, astronomy, geopolitics, standards, and scientific-data infrastructure, the common methodological pattern is:

```text
observation
!= interpretation
!= attribution
!= confidence
!= authorization
!= truth
```

and:

```text
provenance authenticity
!= physical measurement validity

multiple signals
!= independent evidence pathways

signal presence
!= correct propagation

symbolic resemblance
!= established identity

current-event observation
!= actor attribution
```

These findings strengthen OI primarily by sharpening claim boundaries and suggesting falsifiable tests. They do **not** independently validate the OI architecture, prove production readiness, or establish superiority over existing baselines.
