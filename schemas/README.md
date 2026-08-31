# Observer Intelligence Schemas

JSON Schema (draft 2020-12) definitions for the minimal five-object runtime.

| Schema | Object | Addresses |
|---|---|---|
| [observation.schema.json](observation.schema.json) | Observation Record | Base evidence unit (pre-existing; still minimal) |
| [authority-token.schema.json](authority-token.schema.json) | Authority Token | GROK-ATTACK-001 C — binding, scope, time window, evidence refs |
| [shadow-evaluation.schema.json](shadow-evaluation.schema.json) | Shadow / Adversarial Evaluation | GROK-ATTACK-001 D — input scope, isolation, correlation |
| [reconciliation.schema.json](reconciliation.schema.json) | Reconciliation Record | GROK-ATTACK-001 A, E — resolvable lineage, retained disagreement, completeness from resolvability |
| [action-authorization.schema.json](action-authorization.schema.json) | Action Authorization | GROK-ATTACK-001 C, E — mandatory token revalidation |

## Design rules baked into these schemas

1. **Presence ≠ completeness.** Reconciliation `completeness.score` must be derived from resolvability and required-field presence.
2. **Tokens are not flags.** Action Authorization must re-verify binding, scope, time window, and evidence resolvability.
3. **Critics must declare what they saw.** Shadow Evaluation requires `input_scope` and should record correlation with the primary path.
4. **Disagreement is retained.** Reconciliation requires an explicit `retained_disagreement` array (may be empty only if honestly empty).
5. **`additionalProperties: false`** on the new schemas to reduce silent field invention during development.

## Status

These are **minimal development schemas** derived from GROK-ATTACK-001 and the multi-model process. They are not yet a frozen v1.0 contract. Gemini implementation work should target these shapes; further critique may narrow or extend them via a new reconciliation record.

## Related

- `docs/collaboration/multi-model-process.md`
- `docs/collaboration/attacks/GROK-ATTACK-001.md`
- `docs/collaboration/reconciliations/REC-20260831-001.md`
