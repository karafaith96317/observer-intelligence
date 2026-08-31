# Observer Intelligence — Research Findings Log

## Purpose

This is a dated evidence-integration log for credible external research that materially intersects Observer Intelligence (OI). It is designed to help assemble and refine the framework without turning resemblance into proof.

Each entry separates:

```text
external finding
-> demonstrated vs prospective
-> OI connection
-> effect on OI (support / challenge / duplicate / test)
-> research consequence
-> source
```

A paper that resembles an OI idea does not establish that OI is correct, nor does repeated emergence establish truth. The log preserves chronology, citations, claim boundaries, and testable consequences.

---

## 2026-08-31 — Preserved arousability during dexmedetomidine sedation

**Finding.** Zhang et al. report a mouse study of dexmedetomidine sedation in which a moderate dose produced sedation from which animals could be transiently aroused by tactile stimulation, while a higher dose produced deeper unresponsiveness. Functional mapping and fiber photometry implicated glutamatergic neurons in the central medial thalamus (CMT). Manipulating this circuit altered arousability.

**Demonstrated / reported.** Peer-reviewed original research showing dissociation between overt behavioral unresponsiveness and preserved latent transition capacity under moderate sedation.

**Status / boundary.** Peer-reviewed, *Neuroscience Bulletin*, published 29 August 2026. Does not establish a general theory of consciousness or validate OI.

**OI connection.** Observer capability; consciousness-oriented evidence matrix; distinction between overt output and latent causal capacity; stimulus accessibility; state-transition capacity.

**Effect on OI.** **Supports + suggests a test.** Consistent with the methodological principle that absence of current behavioral output is not equivalent to absence of underlying transition capacity.

**Research consequence.** OI should represent, when measurable, both realized state and latent transition capacity. Candidate fields include current observable state, available transition repertoire, stimulus accessibility, perturbation required for transition, response threshold, and uncertainty about latent capacity.

**Source.** Zhang, Y., Wang, S., Li, H. et al. “The Central Medial Thalamus Serves as a Critical Hub for Preserved Arousability During Dexmedetomidine Sedation.” *Neuroscience Bulletin* (2026). DOI: 10.1007/s12264-026-01702-6. https://link.springer.com/article/10.1007/s12264-026-01702-6

---

## 2026-08-31 — 128-element optical phased array with per-channel digital reconstruction

**Finding.** Gurses et al. report a 128-element integrated optical phased array in which each antenna channel is routed to its own coherent receiver and digitized independently. Per-channel amplitude and phase are recovered and beam/image reconstruction is performed numerically after acquisition rather than by on-chip phase shifting. Supporting measurement data and analysis code were released through CaltechDATA.

**Demonstrated / reported.** Peer-reviewed hardware architecture that preserves local channel records while enabling post-acquisition global reconstruction, with open data and code.

**Status / boundary.** Peer-reviewed *Scientific Reports* article, published 28 August 2026, with associated open research dataset. The hardware is not an OI implementation.

**OI connection.** Distributed observation; local evidence preservation; provenance-preserving reconciliation; transformation lineage; dependence-aware observer counting; auditable global reconstruction.

**Effect on OI.** **Enabling infrastructure + suggests a test.** Provides a useful physical analogue for architectures in which local observations remain available after a global estimate is reconstructed.

**Research consequence.** Build an OI benchmark inspired by the architecture: preserve each channel record, deliberately introduce drift, corruption, delay, common-mode noise, and shared-source dependence, then compare ordinary aggregate reconstruction with provenance/dependence-aware reconciliation. Explicitly test whether the system distinguishes `N_channels` from `N_independent_evidence_pathways`.

**Sources.**
- Gurses, V., Sarkar, D., Khachaturian, A. et al. “A large-scale integrated optical phased array with digital beamforming.” *Scientific Reports* (2026). DOI: 10.1038/s41598-026-68798-8. https://www.nature.com/articles/s41598-026-68798-8
- Gurses, V. et al. “Measurement data and analysis code for ‘A large-scale integrated optical phased array with digital beamforming’.” CaltechDATA (2026). https://data.caltech.edu/records/40wk6-9fa71

---

## 2026-08-31 — Quantum-internet governance: technical security is not sufficient for trust

**Finding.** Vermaas, Possati, and Seskir analyze the governance of quantum internet systems and argue that technically secure network functions do not, by themselves, guarantee user trust. They emphasize governance, operation, regulation, transparency, organizational separation, and independent checking as additional trust-producing conditions.

**Demonstrated / reported.** Peer-reviewed analysis of trust requirements beyond technical security for quantum-internet systems.

**Status / boundary.** Peer-reviewed original research paper in *Ethics and Society*, published 28 August 2026; earlier preprint available as arXiv:2505.15852. Organizational separation and independent checking should not be claimed as uniquely OI.

**OI connection.** Runtime separation of authority; transport independence; institutional independence; provenance of authority; distinction among secure transport, authentic observation, independent verification, and justified action.

**Effect on OI.** **Supports an architectural principle + adjacent prior art.** OI’s narrower research contribution remains the coupling of epistemic provenance, observer access state, evidence dependence, reconciliation state, and authority lineage.

**Research consequence.** OI should model institutional independence as an empirical property rather than a label. Separate organizations may still share infrastructure, measurements, incentives, software, timing sources, data pipelines, or authority dependencies.

**Sources.**
- Vermaas, P. E., Possati, L. M., & Seskir, Z. C. “Quantum Internet, Governance, Trust, and the Promise of Secure Communication.” *Ethics and Society* (2026). DOI: 10.1007/s11569-026-00516-0. https://link.springer.com/article/10.1007/s11569-026-00516-0
- Earlier preprint: arXiv:2505.15852. https://arxiv.org/abs/2505.15852

---

## 2026-08-27 — Red Queen Gödel Machine: co-evolving agents and evaluators

**Finding.** Iacob et al. introduced the Red Queen Gödel Machine (RQGM), an evolutionary framework for recursive self-improvement under non-stationary utilities. Evaluation becomes part of the improvement loop: search proceeds in epochs with a fixed criterion within an epoch while the utility/evaluation criterion may change at epoch boundaries. The paper also studies adversarial objectives and agent-as-a-judge evaluation.

**Demonstrated / reported.** The preprint reports improved coding test pass rate over prior SOTA with a complementary code-review signal while using 1.35x–1.72x fewer tokens; higher acceptance rates for co-evolved scientific writers; improved ground-truth accuracy for co-evolved graders; and an adversarial objective that reduced a reviewer's differential over-acceptance of AI-generated papers.

**Status / boundary.** Preliminary preprint and work in progress, first submitted 24 June 2026 and revised 29 June 2026. It does not validate Observer Intelligence and does not establish that unrestricted recursive self-improvement is safe.

**OI connection.** Adversarial evaluation; observer/evaluator evolution; non-stationary evaluation criteria; iterative selection; reward-hacking resistance; observer succession.

**Effect on OI.** **Duplicates / prior art + suggests a test + sharpens the novelty boundary.** Generic co-evolving evaluators and adversarial evaluator improvement should be treated as adjacent prior art. The more specific OI research question is whether epistemic integrity can survive evaluator succession without collapsing raw evidence, provenance, minority contradiction, historical interpretation, and authority into the currently dominant evaluator.

**Research consequence.** Add an **Evaluator Evolution / Observer Succession** benchmark. Construct epochs in which evaluator O1 is replaced by O2 after O2 passes an improvement criterion. Measure whether the system preserves: (1) raw evidence, (2) O1's historical interpretation, (3) O2's new interpretation, (4) minority counterevidence, (5) evidence/evaluator dependence, (6) originating authority, and (7) separation between evaluation competence and execution authority. Include a failure condition in which O2 is better on the anchor set but worse on an unseen dimension.

**Comparison target.** Fixed evaluator vs controlled co-evolving evaluator vs OI-style provenance-preserving evaluator succession under evaluator drift, reward hacking, correlated judges, anchor blind spots, minority counterevidence, and authority laundering.

**Source.** Iacob, A. et al., *The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators*, arXiv:2606.26294 (v1 submitted 24 June 2026; v2 29 June 2026). https://arxiv.org/abs/2606.26294

---

## 2026-08-27 — GPS-free maritime quantum gravimetric navigation

**Finding.** Q-CTRL reported a maritime field demonstration in the Coral Sea using a software-ruggedized quantum gravimeter for autonomous gravity mapping and GPS-free navigation. The company reports approximately one nautical mile positioning accuracy over the mission duration.

**Demonstrated / reported.** A real vessel-based field trial using gravity sensing and map matching without GPS was reported by the company. The report also describes software stabilization, sensor fusion, and autonomous operation under maritime motion.

**Not yet established by this source.** The announcement is a company report rather than an independently peer-reviewed journal result. Broad claims of superiority, generality, or robustness across operating environments should therefore remain provisional until independently reproduced or supported by the linked technical manuscript and further field data.

**OI connection.** Independent physical modalities; adversarial/counterfactual observers; sensor fusion; source diversity; contested-reference environments.

**Effect on OI.** **Suggests a test and strengthens the independence model.** Different observers may obtain position or state estimates from genuinely different physical references rather than merely from different software agents consuming the same upstream data.

**Research consequence.** OI should distinguish **modality independence** from agent independence. A GPS-derived observer, inertial observer, magnetic-map observer, and gravity-map observer may provide more meaningful epistemic diversity than several agents sharing one reference channel. Reconciliation should preserve modality, map/reference provenance, sensor-fusion transformations, and environmental assumptions.

**Source.** Q-CTRL, “Q-CTRL Achieves World’s First GPS-Free Quantum Gravimetric Navigation Demonstration in Maritime Field Trial,” 27 August 2026. https://q-ctrl.com/blog/q-ctrl-achieves-worlds-first-gps-free-quantum-gravimetric-navigation-demonstration-in-maritime-field-trial

---

## 2026-08-26 — Passive picosecond synchronization using a co-propagating classical clock

**Finding.** Researchers demonstrated nonlocal Franson interferometry over 50 km of single-mode fiber while co-propagating a classical radio-over-fiber clock signal with energy-time entangled photons in the same fiber. O-band allocation for the classical signal and L-band allocation for the quantum signal suppressed Raman contamination while correlated environmental delay fluctuations enabled common-mode cancellation. The authors report passive synchronization at picosecond precision without dedicated external timing infrastructure.

**Demonstrated.** Shared-fiber classical timing and entangled-photon transport with picosecond-scale passive synchronization over 50 km.

**Not demonstrated.** A universal timing architecture for arbitrary quantum or distributed-intelligence systems.

**OI connection.** Temporal provenance; shared infrastructure dependence; synchronization lineage; effective observer independence.

**Effect on OI.** **Material refinement.** Temporal independence cannot be inferred merely from separate timestamps or separate observers when multiple records depend on a common timing pathway.

**Research consequence.** Add **Synchronization-Lineage Provenance**. Records should preserve clock source, timing path, whether timing and evidence share infrastructure, compensation/common-mode correction methods, measured synchronization uncertainty, drift, and relevant environmental delay history. Shared timing dependencies should reduce effective temporal independence where appropriate.

**Source.** Xiang et al., *Physical Review Applied* 26, 024073 (published 26 August 2026), “Passive synchronization of nonlocal Franson interferometry for fiber-based quantum networks using copropagating classical clock signals.” DOI: 10.1103/2dl9-6t4n. https://journals.aps.org/prapplied/abstract/10.1103/2dl9-6t4n

---

## 2026-08-26 — Metropolitan atom–photon entanglement over deployed fiber

**Finding.** Researchers distributed entanglement between a single atom and a resonant 780-nm photon over 14 km line-of-sight distance using 24 km of deployed commercial fiber. The photon was converted to the telecom S-band for transmission and converted back afterward. Reported photon transfer efficiency was 1.7%, while the conversion/transmission process affected atom-photon entanglement fidelity by less than 1%.

**Demonstrated.** A heterogeneous chain linking an atomic quantum node, wavelength conversion, deployed telecom fiber, reverse conversion, and a remote quantum optical state while largely preserving entanglement fidelity.

**Not demonstrated.** General-purpose large-scale heterogeneous quantum networks.

**OI connection.** Distributed observation; transport independence; transformation-chain provenance; physical-channel provenance; measurement integrity.

**Effect on OI.** **Supports infrastructure plausibility and suggests a test**, but does not support treating entanglement as truth, identity, provenance, or authority.

**Research consequence.** Add **Transformation-Chain Integrity**. Distributed OI records should preserve conversion stages, representation/domain changes, channel loss, fidelity or quality estimates, timing, correction/stabilization history, and transformations applied before reconciliation. Endpoint authenticity alone is insufficient when consequential transformations occur between source and destination.

**Source.** Büki et al., *Physical Review Letters* 137, 090803 (published 26 August 2026), “Metropolitan Entanglement Distribution between an Atom and a Near-Visible Photon.” DOI: 10.1103/94hz-xtht. https://journals.aps.org/prl/abstract/10.1103/94hz-xtht

---

## 2026-08-26 — 18-km intermodal free-space quantum key distribution

**Finding.** Researchers demonstrated a real-time quantum key distribution field trial over an 18-km free-space optical link between a remote terminal and an urban optical ground station. Adaptive optics performed direct wavefront sensing and high-order aberration correction, enabling efficient single-mode fiber coupling. The experiment generated secure key material at approximately 200 bit/s using room-temperature detectors.

**Demonstrated.** Long-range intermodal free-space QKD at telecom wavelengths using adaptive optics and room-temperature detection hardware, with experimental validation of a turbulence-based coupling model.

**Not demonstrated.** Universal secure wireless networking, immunity to all attack classes, or an OI trust architecture.

**OI connection.** Channel-state provenance; correction provenance; authentication/secure transport distinction; environmental context; transformation integrity.

**Effect on OI.** **Material refinement.** A recovered signal can depend on active environmental estimation and correction. Therefore the correction process itself can become epistemically relevant.

**Research consequence.** Add **Correction Provenance**: preserve raw/estimated channel state where feasible, disturbance model, correction method, correction confidence, residual uncertainty, and post-correction quality. This principle generalizes beyond quantum networking to sensor calibration, denoising, image enhancement, preprocessing, error correction, and AI-generated transformations.

**Source.** Rossi et al., *npj Quantum Information* (published 26 August 2026), “Intermodal quantum key distribution over an 18-km free-space channel with adaptive optics and room-temperature detectors.” DOI: 10.1038/s41534-026-01358-0. https://www.nature.com/articles/s41534-026-01358-0

---

## 2026-08-08 — IIT and testability of silent-neuron predictions

**Finding.** A *Neuroscience of Consciousness* paper analyzes two unusual predictions associated with Integrated Information Theory (IIT): a “silent brain” prediction involving neurons that are inactive but remain capable of spiking, and a “disabled neuron” prediction involving silent neurons whose ability to spike is removed. The paper's main relevance here is methodological: it treats apparently difficult consciousness claims as candidates for causal/testability analysis rather than relying on report alone.

**OI connection.** Observer Intelligence Evidence Matrix; distinction between substrate/capacity, access/report channels, verbal claims, and independent evidence.

**Effect on OI.** **Suggests a test and sharpens representation.** It does not establish IIT or OI as a correct theory of consciousness.

**Research consequence.** Consciousness-oriented OI records should avoid collapsing current activity, causal capacity, information access, report capability, verbal report, and independent causal evidence.

**Source.** *Neuroscience of Consciousness* (2026), “Integrated information theory (IIT) and the testability of the silent neuron predictions,” article niag037, published 8 August 2026. DOI: 10.1093/nc/niag037. https://academic.oup.com/nc/article/2026/1/niag037/8756945

---

## 2026-07-15 — DMT micro-phenomenology of immersion and perceived presences

**Finding.** Twenty-three participants received 20 mg intravenous DMT during simultaneous fMRI–EEG acquisition, followed by detailed micro-phenomenological interviews. Researchers extracted 125 phenomenological categories spanning sensory/amodal faculties, spatial organization, self-world configuration, and social relatedness. Dynamic analysis found structured temporal patterns: bodily effects typically preceded visual/auditory effects, while perceived presences emerged after multisensory integration and three-dimensional spatial characteristics had developed. The study treats perceived presences as higher-order features within an unfolding immersive process rather than establishing an external ontology for them.

**OI connection.** Human-observer branch; temporal provenance; structured phenomenology; separation of experience, interpretation, and verification.

**Effect on OI.** **Supports the value of time-resolved phenomenological representation and suggests a concrete coding scheme.** It neither verifies nor falsifies external-entity interpretations.

**Research consequence.** Candidate OI phenomenology sequence:

```text
bodily state
-> sensory modalities
-> multisensory integration
-> spatial depth / world-model
-> self-world configuration
-> perceived agency / presence
-> semantic identity / interaction
```

Records should preserve when possible both the original narrative and later coded categories so that analysis does not overwrite the source report.

**Source.** Sanders et al., *Neuroscience of Consciousness* (2026), “Micro-phenomenology of immersion and perceived presences under DMT,” article niag015. DOI: 10.1093/nc/niag015. https://academic.oup.com/nc/article/2026/1/niag015/8733941

---

## 2026-08 — Context-dependent psilocybin neurodynamics

**Finding.** A 2026 *Nature* study examined psilocybin neurodynamics across multiple contexts using multimodal neuroimaging. The study reports structured context-sensitive neural trajectories rather than reducing the psychedelic state to undifferentiated disorder.

**OI connection.** Observer state; context; temporal dynamics; information integration; altered-state measurement.

**Effect on OI.** **Supports a measurement strategy and challenges scalar-only descriptions.** It does not establish external interpretations of altered-state content.

**Research consequence.** OI human-observer datasets should preserve environmental context and time-resolved state trajectories and compare their explanatory value against session-average scalar measures.

**Source.** *Nature* (2026), article s41586-026-10910-z. https://www.nature.com/articles/s41586-026-10910-z

---

## Integration rules for future findings

New literature should be added when it materially changes an OI hypothesis, representation, prior-art boundary, proposed test, implementation assumption, or threat model. Relevant evidence may come from AI/ML, distributed systems, cybersecurity, cryptography, quantum information, communications, metrology, sensing, neuroscience, cognitive science, psychology, phenomenology, statistics, information theory, control theory, robotics, HCI, safety engineering, biology, physics, or other disciplines.

Each addition should record publication/preprint status and should be classified as one or more of:

- **supports** — evidence is consistent with an OI design assumption without proving the framework;
- **challenges** — evidence conflicts with or narrows an OI assumption;
- **duplicates / prior art** — an allegedly novel mechanism already exists elsewhere;
- **suggests a test** — the finding creates a concrete falsifiable experiment or representation requirement;
- **enabling infrastructure** — an external advance makes an OI mechanism more technically feasible without validating it;
- **threat-model change** — a finding exposes a new dependency, attack surface, failure mode, or invalid assumption.

For preprints, explicitly record that peer review and replication remain outstanding. For vendor/company demonstrations, distinguish reported performance from independently verified performance.

## Current synthesis signal

The current cross-domain pattern worth testing is:

```text
state
+ context
+ temporal structure
+ measurement integrity
+ transformation lineage
+ channel/correction state
+ synchronization lineage
+ source/modality independence
+ evaluator lineage
+ provenance
+ realized vs latent capability
+ reconstruction / reconciliation lineage
```

may carry information that is lost when observations are reduced to a single confidence score, average activity measure, agent count, verbal report, timestamp, transport-success flag, or current evaluator score.

A further refinement is now warranted:

> **Observer independence is not static. It is a time-varying property of observers, evaluators, physical modalities, source lineages, transformations, channels, clocks, correction systems, models, and network topology.**

A second testable refinement is:

> **Improving or replacing an evaluator should not silently rewrite the evidence history on which earlier decisions were made.**

Additional principles arising from the 2026-08-31 update:

1. **Observed output is not identical to latent capability.**
2. **Aggregate output is not a complete description of the observations that generated it.**
3. **Institutional or agent multiplicity is not sufficient evidence of independence.**

These are research hypotheses and data-modeling principles, not established universal laws. See `docs/research-refinement-protocol.md` for how findings should be converted into candidate OI revisions and experiments.
