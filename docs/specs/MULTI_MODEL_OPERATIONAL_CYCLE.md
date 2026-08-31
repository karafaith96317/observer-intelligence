# Observer Intelligence: Autonomous Tri-Model Interaction Workflow

**Status:** Canonical development-workflow specification for the OI multi-model research lifecycle.

This workflow turns the development process into a living implementation of the Observer Intelligence lifecycle. The human architect remains the root authority. AI nodes operate asymmetrically and may propose, implement, review, or attack, but no model may self-authorize a merge into `main`.

> Operational note: "autonomous" applies only where a participating model has been independently granted repository/testbed access. In the current ChatGPT environment, ChatGPT can interact with the connected GitHub repository; Gemini and Grok outputs may still need to be relayed into the repository unless they are separately connected through their own tooling or CI agents.

## Roles and authority boundaries

### ChatGPT — Governance & Specification Lead

- Maintains canonical specifications under `docs/specs/`.
- Drafts `GPT-SPEC-###` feature requirements, invariants, acceptance criteria, and falsification tests.
- Reviews implementation and attack evidence against the specification.
- Drafts Reconciliation Decision Records (`RDR-YYYY-###`).
- May propose repository changes, but does not hold root merge authority.

### Gemini — Implementation & Review Engine

- Ingests `GPT-SPEC-###` requirements and authors functional patches under `src/` and `tests/`.
- Produces deterministic fixtures and quantitative simulation/Monte Carlo evidence where appropriate, with `N >= 1,000` when Monte Carlo evaluation is part of the accepted test plan.
- Labels contributions `GEM-IMPL-###`.
- Must preserve raw outputs, environment metadata, seeds where applicable, and exact commit references for empirical claims.
- Does not treat model consensus as ground truth and does not self-authorize merges.

### Grok — Adversarial Red-Team

- Probes implementations for bypasses, race conditions, Sybil/collusion failure, authority escalation, stale-state or replay errors, evidence-boundary violations, and reconciliation exploits.
- Submits concrete failing fixtures or reproducible attack payloads under `GROK-ATK-###`.
- A challenge is not accepted merely because it is plausible; it must be mapped to a falsifiable test or evidence-bearing counterexample.
- Does not hold merge authority.

### Kara — Root Authority / Human-on-the-Loop

- Defines root directives under `KFS-ROOT-###`.
- Holds or controls root signing material outside the repository where applicable.
- Reviews the reconciled evidence record before final authorization.
- Authorizes final squash-merge into `main` after the accepted review conditions are satisfied.
- Human authorization does not convert an untested claim into an empirical result; evidence status remains independently recorded.

## Standard operational cycle

```text
1. Feature Specification
   ChatGPT: GPT-SPEC-###
          |
          v
2. Implementation + Test Suite
   Gemini: GEM-IMPL-###
          |
          v
3. Adversarial Red-Team Challenge
   Grok: GROK-ATK-###
          |
          v
4. Test Execution
   Deterministic + quantitative evidence
          |
          v
5. Reconciliation
   RDR-YYYY-### + CONTRIBUTION_PROVENANCE.md
          |
          v
6. Human Authorization
   KFS-ROOT-### sign-off
          |
          v
7. Squash-Merge to main
   Preserved commit/PR/test lineage
```

## Acceptance rules

A feature is not eligible for human root authorization until the following are recorded:

1. A canonical `GPT-SPEC-###` requirement or equivalent root directive.
2. The exact implementation commit/PR and affected files.
3. Deterministic acceptance tests for specified invariants.
4. Red-team evidence or a documented reason a particular adversarial class is out of scope for the cycle.
5. Quantitative results where the specification makes a quantitative claim.
6. An RDR recording disagreements, failures, patches, and disposition.
7. No unresolved critical authority-bypass or evidence-boundary failure known to the adjudicating record.

Passing the current suite means only that the tested cases passed at that commit. It does not establish the absence of unknown vulnerabilities.

## Evidence boundary

The repository distinguishes:

- design requirements;
- implementation artifacts;
- synthetic fixtures;
- executed empirical outputs;
- red-team claims;
- reconciled findings;
- human authorization.

A hash, signature, branch, commit, or PR proves repository lineage/integrity under its relevant mechanism; it does not independently prove the truth of an external-world claim.

## Interaction rule

When ChatGPT, Gemini, or Grok produces an updated specification, implementation, or challenge, the payload/diff is brought into the shared evidence workflow. The next node must inspect the actual affected code and evidence boundary before proposing a patch or disposition.

No model may silently overwrite another node's contribution history. Superseded, rejected, or patched work should remain traceable through Git history and the contribution ledger.

## Canonical support documents

- `docs/CONTRIBUTION_PROVENANCE.md`
- `docs/PROMPT_PACKS.md`
- `docs/RECONCILIATION_TEMPLATE.md`
- `docs/specs/MULTI_MODEL_OPERATIONAL_CYCLE.md`
