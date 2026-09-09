# Observer Intelligence — Architecture Extensions (2026-09-09)

This index records two new OI research extensions added on September 9, 2026.

## 1. OI Risk Deliberation Network (OI-RDN)

See: `docs/oi-risk-deliberation-network.md`

OI-RDN extends Observer Intelligence into hierarchical, cross-domain risk forecasting and mitigation analysis using:

- independent risk generation;
- differentiated evidence pathways;
- asymmetric observer roles;
- adversarial challenge;
- role reversal / steelmanning;
- minority-evidence preservation;
- cross-domain dependency graphs;
- mitigation inversion;
- adversarial mitigation testing;
- explicit abstention/escalation;
- human authorization for consequential decisions.

The architecture explicitly rejects the assumption that agent agreement equals truth and treats numerical agent diversity as distinct from epistemic diversity.

## 2. Biological and Sensitive Data Governance

See: `docs/biological-data-governance.md`

Any OI work involving health, physiological, biometric, genomic, behavioral, or other sensitive human data must treat those data as consent- and purpose-bound evidence.

Core boundary:

```text
biological measurement
!= identity
!= intent
!= moral worth
!= truth
!= authorization
```

Required controls include purpose limitation, consent/lawful basis, minimization, provenance, measurement-quality metadata, access separation, selective disclosure, contestability, retention/deletion policy, and human review for high-impact uses.

## New candidate research targets

### OI-005 — Risk deliberation under differentiated evidence
Compare single-agent analysis, majority voting, ordinary debate, evidence-diverse deliberation, and OI-RDN under correlated-error, minority-correctness, cross-domain dependency, role-reversal, mitigation-failure, and abstention/escalation conditions.

### OI-006 — Sensitive-data provenance and purpose-bound inference
Test whether binding biological or sensitive-data inferences to consent/purpose scope, measurement quality, transformation lineage, disclosure boundaries, uncertainty, and downstream authority reduces privacy leakage, invalid inference transfer, and unjustified high-impact decisions.

## Related systems credited in the new documentation

The new documents explicitly credit adjacent work and do not claim invention of these established areas:

- AI Safety via Debate — Irving, Christiano & Amodei (2018), arXiv:1805.00899.
- Delphi-style iterative expert forecasting.
- InfoDelphi / designed information asymmetry — Li et al. (2026), arXiv:2607.01661.
- Conformal Social Choice for safe multi-agent deliberation — Wang et al. (2026), arXiv:2604.07667.
- Truth Maintenance Systems — Doyle (1979).
- NIST AI Risk Management Framework.
- WHO ethics and governance guidance for AI and health data.
- NIST privacy/data-governance work.

OI's research target is the coupling of these adjacent mechanisms with observer-specific evidence access, typed epistemic transitions, dependence-aware observer counting, provenance-preserving reconciliation, minority retention, bounded authority, cross-domain mitigation testing, and purpose-bound sensitive-data inference.

## Human-authority boundary

OI may forecast, challenge, simulate, compare, recommend, document, and escalate. It should not coerce consensus, autonomously impose high-impact public policy, erase minority findings, or use biological signals as hidden proxies for trustworthiness, worth, or permission.