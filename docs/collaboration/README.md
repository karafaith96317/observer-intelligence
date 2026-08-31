# Collaboration Workspace

Operational files for the multi-model Observer Intelligence development process.

| File | Purpose |
|---|---|
| [multi-model-process.md](multi-model-process.md) | Asymmetric roles, contribution IDs, first-build target, core rules |
| [test-matrix-v0.md](test-matrix-v0.md) | Canonical eight-condition test matrix and metrics for the minimal runtime |
| [prompt-pack-gemini.md](prompt-pack-gemini.md) | Ready-to-paste prompts for Gemini (implementation + critique) |
| [prompt-pack-grok.md](prompt-pack-grok.md) | Ready-to-paste prompts for Grok (red-team / adversarial) |
| [reconciliation-template.md](reconciliation-template.md) | Conflict record and disposition template |
| [contribution-log.md](contribution-log.md) | Running ID ledger |

Related higher-level documents:

- `docs/collaboration-contribution-ledger.md` — broader provenance classes and human collaborator inventory
- `docs/cross-model-novelty-audit-protocol.md` — novelty and prior-art attack protocol

## Quick start

1. Freeze a commit.
2. Paste the Gemini or Grok packet into the corresponding model (do not cross-contaminate on the first pass).
3. File the response under a new contribution ID in `contribution-log.md`.
4. Open a reconciliation record if there is conflict or a proposed merge.
5. Run the relevant conditions from `test-matrix-v0.md` before disposition ACCEPTED.
