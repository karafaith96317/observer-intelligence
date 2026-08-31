# Observer Intelligence — Multi-Model Collaboration Process

**Status:** Working operational protocol — 2026-08-31  
**Related:** `docs/collaboration-contribution-ledger.md`, `docs/cross-model-novelty-audit-protocol.md`

## Purpose

Treat ChatGPT, Gemini, and Grok as separate research agents with asymmetric roles. Use the GitHub repository as the shared source of truth and evidence ledger. Agreement among models is treated as consensus evidence, never as proof.

The development process itself is an early prototype of Observer Intelligence:

- different epistemic positions
- preserved provenance of proposals
- adversarial evaluation before authority
- conflict records rather than silent averaging
- disposition only after evidence and test

## Asymmetric roles

| Agent | Primary role | Allowed actions | Forbidden actions |
|---|---|---|---|
| **ChatGPT** | Architecture / governance lead | Maintain canonical OI spec, test criteria, threat model, experiment design, provenance rules; reconcile disagreements against requirements | Implement code as authoritative; outvote other agents without evidence |
| **Gemini** | Implementation / independent review | Implement modules, critique assumptions, generate alternative designs, inspect or run tests | Redefine core architecture unilaterally; claim novelty without audit |
| **Grok** | Adversarial / red-team | Attack architecture: bypasses, Sybil, authority escalation, stale-state, bad incentives, edge cases, alternative explanations | Soften attacks to produce consensus; propose features without first attacking |
| **GitHub** | Evidence ledger | Issues, branches, commits, design notes, test results, conflict records | Merge solely because models agree |

## Core rule

> ChatGPT, Gemini, and Grok should not simply vote. They should have asymmetric roles and be required to show evidence for proposed changes.

## Contribution identity scheme

Every consequential cross-model contribution receives an ID:

```text
GPT-SPEC-###     ChatGPT architecture / requirements proposal
GEM-IMPL-###     Gemini implementation or alternative design
GEM-CRIT-###     Gemini independent critique
GROK-ATTACK-###  Grok adversarial finding or counterexample
GROK-ALT-###     Grok alternative explanation or simpler architecture
JOINT-###        Explicitly joint refinement after conflict record
KARA-###         Human originator decision or originating architecture
```

Record for each ID:

```text
proposal → source model → evidence → counterarguments → test → result → disposition → commit hash
```

Dispositions: `ACCEPTED`, `ACCEPTED-WITH-MODIFICATION`, `REJECTED`, `DEFERRED`, `SUPERSEDED`, `NEEDS-TEST`.

## Collaboration loop

```text
Canonical OI Spec (repo)
       │
       ├── ChatGPT: architecture + requirements
       │
       ├── Gemini: implementation + independent critique
       │
       └── Grok: adversarial attack + counterexamples
                      │
                      ▼
                Conflict Record
                      │
                      ▼
                Test / Evidence
                      │
              ┌───────┴───────┐
              ▼               ▼
            MERGE           REJECT
              │               │
              └──── provenance log
```

## First build target (minimal runtime)

Implement only these five typed objects and the transitions between them:

1. **Observation Record** — what was observed, by whom, under what access/measurement conditions, with provenance and uncertainty.
2. **Authority Token** — a bounded, time-limited, scope-limited authorization derived from evidence strength, independence, and risk.
3. **Shadow / Adversarial Evaluation** — independent critic or counterfactual observer that receives controlled information and produces contradiction or alternative hypothesis.
4. **Reconciliation Record** — provenance-preserving synthesis that retains disagreement, dependence estimates, disclosure boundaries, and lineage.
5. **Action Authorization** — final gate that decides whether execution is permitted; must reference the preceding records.

Do not expand the runtime until this minimal loop has a working test suite and failure modes are characterized.

## First test suite (required conditions)

Every architecture under test (including a simpler multi-agent baseline) must be evaluated on at least:

- corrupted telemetry
- majority hallucination / Sybil pressure
- legitimate minority counterevidence
- semantic leap from valid evidence
- expired or replayed authority
- compromised agent
- contradictory evidence
- rapidly changing world state

## Required metrics (per run)

- false authorization rate
- correct escalation rate
- provenance completeness
- adversarial success rate
- latency
- compute / token overhead

Additional recommended metrics: independence-estimation error, contradiction preservation, authority-lineage reconstruction accuracy, abstention quality.

## Ownership and provenance note

The repository distinguishes:

- originating architecture and requirements (Kara / human)
- AI-generated implementation suggestions
- AI adversarial findings
- joint refinements
- external prior art

This creates a cleaner research provenance trail. It does not substitute for a legal IP or inventorship agreement.

## Operational files in this directory

- `test-matrix-v0.md` — canonical first-build test matrix
- `prompt-pack-gemini.md` — implementation and critique prompts
- `prompt-pack-grok.md` — red-team prompts
- `reconciliation-template.md` — conflict and disposition record
- `contribution-log.md` — running ID ledger
