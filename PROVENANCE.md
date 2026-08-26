# Observer Intelligence — Provenance and Contribution Ledger

## Purpose

Observer Intelligence treats its own development history as a provenance problem. This file records major conceptual, implementation, AI-assisted, literature-derived, and experimental contributions without collapsing them into a single undifferentiated authorship claim.

Git commit authorship alone is not sufficient attribution when code or text is generated, transformed, or substantially assisted by AI systems under a human account.

**Primary author name used throughout this project:** Kara Sypen  
**Full name:** Kara Faith Sypen

## Contribution classes

Each major contribution should identify, where known:

- **Concept origin** — who first introduced the underlying idea in the project record.
- **Human specification** — who defined goals, constraints, hypotheses, or acceptance criteria.
- **AI collaborator** — which AI system materially helped formalize, critique, draft, or implement the contribution.
- **Implementation contributor** — who or what produced the concrete code, schema, experiment, or document.
- **External prior art / evidence** — research or systems that overlap, support, challenge, or motivate the contribution.
- **Modification history** — later changes that materially alter the contribution.
- **Current claim status** — conceptual, prototype, experimentally tested, independently replicated, or superseded.

## Core project lineage

### Observer Intelligence framework

**Concept origin:** Kara Sypen  
**Human role:** originator, research architect, hypothesis generator, portfolio integrator  
**AI collaboration:** multiple AI systems have assisted with formalization, literature comparison, documentation, critique, and prototyping  
**Current status:** early research/specification framework with working synthetic prototypes

Major conceptual lineage includes:

```text
observer-specific access
→ typed epistemic states
→ provenance preservation
→ dependence-aware observer counting
→ counterfactual / adversarial observers
→ provenance-preserving reconciliation
→ bounded execution authority
→ access-to-authority governance
```

The presence of a mechanism in OI does not imply that the mechanism itself is novel. Novelty boundaries are tracked separately in `docs/prior-art-and-novelty.md`.

## OI-003 provenance record

### Conceptual specification

**Project:** OI-003 — Provenance-Aware Epistemic Diversity  
**Conceptual lineage:** developed within the Observer Intelligence framework before the current LLM prototype commits  
**Human specification:** Kara Sypen, with AI-assisted formalization and refinement  
**Research objective:** compare numerical agent diversity against provenance-aware epistemic diversity under correlated, duplicated, corrupted, authority-laundered, and measurement-integrity-stressed evidence.

### Grok-assisted implementation

Kara Sypen reported that Grok materially assisted in developing the OI-003 prototype and extending the repository. Because the resulting commits were made through her GitHub account, Git metadata alone does not preserve that AI contribution.

The following commits are therefore recorded as **Grok-assisted implementation work under Kara Sypen’s repository/account**, subject to future refinement if a more detailed generation log becomes available:

- `60c097d7328d35c999f673930daefc2cf1d14eb2` — Add OI-003 experiment README
- `53dee1e257e69b498f21102e5cf7e2fb60e7f0dc` — Add base OI-003 LLM-integrated experiment
- `e1dc03d278b2bdfc316d890562146e3f958965e0` — Add OI-003 extended experiment with LLM-as-judge, critic debate, and provenance ledger
- `85a337ad0834f1bd83a6c27d4e2a1c127e8800e1` — Add OI Authority Bound v0.1 freeze record

**Attribution note:** this record does not claim that Grok originated the Observer Intelligence framework or the OI-003 research question. It records material AI assistance in prototype implementation and extension.

### Current scientific status

The OI-003 prototype currently demonstrates that the proposed mechanisms can be encoded and compared in a controlled synthetic harness.

It does **not yet establish** that OI outperforms alternatives in an independent benchmark, because parts of the authority bound, thresholds, and synthetic conditions were designed within the same development process.

The next validation stage is governed by `experiments/OI-003/BENCHMARK-GUARDRAILS.md`.

The authority-bound function itself is now frozen as **v0.1** — see `experiments/OI-003/AUTHORITY-BOUND-v0.1-FREEZE.md`.

## ChatGPT-assisted development

ChatGPT has materially assisted with:

- formalizing OI v2.x terminology and architecture;
- separating prior art from narrower candidate contributions;
- designing falsifiable comparison targets;
- integrating newly surfaced research into the novelty map and roadmap;
- defining the PIIE subproject;
- identifying methodological risks in OI-003, including self-confirming benchmarks and correlated LLM judges;
- maintaining documentation and repository structure at Kara Sypen’s direction;
- adding the provenance system and benchmark guardrails.

**Attribution boundary:** ChatGPT assistance should be recorded as AI-assisted formalization, critique, documentation, and implementation support. It should not erase Kara Sypen’s conceptual provenance or external prior art.

## External research provenance

External research should be recorded as one of:

- **supports** — provides evidence consistent with an OI hypothesis;
- **challenges** — raises contradictory evidence or a stronger competing explanation;
- **duplicates / prior art** — substantially overlaps a mechanism OI should not claim as original;
- **suggests a test** — motivates a new falsifiable experiment without validating OI itself.

See `docs/prior-art-and-novelty.md`.

## Future contribution template

For each major addition, append a record in this form:

```text
Title:
Date:
Concept origin:
Human specification:
AI collaborator(s):
Implementation contributor(s):
Relevant commits/files:
External prior art/evidence:
What changed:
Current claim status:
Notes on uncertainty/attribution:
```

## Timestamping

Where useful, raw source artifacts, hypothesis records, and major conceptual snapshots may be cryptographically timestamped before later modification. OpenTimestamps-style commitments can help establish chronology, but a timestamp alone does not prove authorship, originality, independence, or truth.

## Attribution principle

Observer Intelligence should apply its own rule to its development history:

> Preserve the lineage of consequential claims and contributions rather than allowing later reconciliation to erase where they came from.
