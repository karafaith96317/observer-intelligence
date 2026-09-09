# Biological and Sensitive Data Governance for Observer Intelligence

**Status:** Required safety boundary for any OI extension using human, health, biometric, genomic, behavioral, or physiological data.

## Principle

Biological data can be useful evidence, but it is not inherently truthful, objective, consented, or appropriate for every decision.

OI must therefore distinguish:

```text
biological measurement
!= identity
!= intent
!= moral worth
!= truth
!= authorization
```

No biological signal should automatically confer or remove epistemic, social, financial, legal, or execution authority.

## Covered data

This boundary applies to data such as:

- heart rate, HRV, respiration, EDA, EEG, EMG, temperature, sleep and activity;
- medical records, diagnoses, medications, laboratory values and imaging;
- genomics, epigenomics, proteomics, metabolomics and microbiome data;
- voice, face, gait or other biometric identifiers;
- fertility, reproductive or sexual-health data;
- inferred stress, affect, cognitive state or behavioral state;
- environmental exposures linked to an identifiable person;
- combinations of otherwise ordinary data that can reveal sensitive biological or health information.

## Required governance controls

### 1. Explicit purpose binding
Every collection or use must identify its purpose before use. Data collected for one purpose must not silently migrate into another decision context.

### 2. Consent and lawful basis
Where consent is the governing basis, consent must be specific enough to distinguish collection, analysis, sharing, model training, secondary research, retention, and publication. Withdrawal and downstream consequences must be defined where technically and legally applicable.

### 3. Data minimization
Collect the least sensitive and least granular data necessary for the stated research question. Raw biological streams should not be retained when a less identifying derived feature is sufficient.

### 4. Separation of measurement from inference
OI must preserve the distinction between:

```text
RAW MEASUREMENT
  -> QUALITY / CALIBRATION
  -> DERIVED FEATURE
  -> MODEL INFERENCE
  -> INTERPRETATION
  -> CLAIM
```

A high-confidence model output does not upgrade a noisy biological measurement into fact.

### 5. Provenance
Each sensitive datum should retain, where applicable:

- source / device / system;
- subject or cohort scope;
- collection purpose;
- timestamp and timing uncertainty;
- calibration and quality metadata;
- transformation history;
- model/version used for derived inferences;
- consent or authorization scope;
- disclosure history;
- retention/deletion policy;
- known missingness and bias.

### 6. Access separation
Access to biological data should be role- and purpose-bound. A reasoning observer does not automatically receive raw identifiers simply because another component can access them.

### 7. Selective disclosure
Where possible, provide observers only the minimum derived evidence necessary for the task. Sensitive raw records should remain outside ordinary deliberation paths unless specifically justified.

### 8. No covert biometric authority
OI must not use physiological coherence, affect estimation, voice stress, EEG, HRV, facial analysis, genetics, or similar signals as a hidden basis for deciding who is trustworthy, truthful, aligned, deserving, dangerous, or authorized.

Such signals may be studied as uncertain measurements only under an explicit research protocol with appropriate controls and validation.

### 9. Group and population protections
Models built from biological data must document representativeness, subgroup error, missing populations, distribution shift, and risks of stigmatization or discriminatory downstream use.

### 10. Human override and contestability
High-impact conclusions derived from sensitive biological data must be contestable by affected people and reviewable by authorized humans. The provenance chain should make it possible to identify which data and inference produced the conclusion.

### 11. Retention and deletion
Retention must be purpose-justified. Systems should support deletion or cryptographic revocation where feasible and where retention is not legally or scientifically required. Immutable ledgers should store hashes, commitments, permissions, or provenance records rather than unnecessary raw biological data.

### 12. Security
Sensitive human data require strong confidentiality, integrity, authentication, key management, audit, and breach-response controls. Privacy risk and cybersecurity risk must be treated as coupled but distinct concerns.

## Biological data inside OI-RDN

In the OI Risk Deliberation Network, biological or population-health evidence should normally enter through a protected domain observer rather than being globally exposed to every agent.

Example:

```text
protected health/biological source
      |
      v
authorized health-data observer
      |
      +-- quality assessment
      +-- privacy filtering
      +-- population-level aggregation
      +-- uncertainty estimate
      |
      v
minimum necessary claim/evidence package
      |
      v
cross-domain deliberation
```

The cross-domain system should receive the minimum information necessary to reason about the risk. It should not receive identifiable raw health data merely because those data exist.

## Relationship to ERA / contribution recognition

If future ERA mechanisms recognize contributions derived from human or biological datasets, compensation or attribution must not override consent, privacy, licensing, participant rights, community governance, or research-ethics obligations.

A contribution ledger may record that a dataset, study, participant cohort, institution, or researcher materially contributed to a conclusion without publicly exposing sensitive source data.

## Related governance and prior art

### WHO ethics and governance of AI for health
The World Health Organization has established extensive guidance on AI for health emphasizing ethics, human rights, accountability, appropriate governance, privacy, equity, safety, and responsible use of health data.

WHO, *Ethics and governance of artificial intelligence for health: guidance on large multi-modal models*.
https://www.who.int/publications/i/item/9789240084759

WHO, *Health data governance in the age of artificial intelligence: policy imperatives for the WHO European Region* (2025).
https://www.who.int/europe/publications/i/item/WHO-EURO-2025-11462-51234-78079

### NIST AI Risk Management Framework
The NIST AI RMF treats privacy, safety, security, accountability, transparency, fairness, and ongoing risk management as trustworthiness concerns across the AI lifecycle.

https://www.nist.gov/itl/ai-risk-management-framework

### NIST data-governance work
NIST's Privacy Engineering Program is developing a Data Governance and Management Profile linking privacy, cybersecurity, and AI risk-management practices.

https://www.nist.gov/news-events/events/2026/05/data-governance-and-management-profile-working-session-2

## OI research boundary

OI does not claim invention of consent management, health-data governance, privacy engineering, access control, differential privacy, federated learning, de-identification, secure computation, biometric security, medical ethics, research ethics, or data minimization.

The OI-specific research question is narrower:

> Can provenance-preserving epistemic reasoning make sensitive-data use safer by binding each inference to its measurement quality, transformation history, consent/purpose scope, disclosure boundary, uncertainty, and downstream authority?

That proposition must be tested rather than assumed.