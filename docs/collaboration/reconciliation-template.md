# Reconciliation / Conflict Record Template

**Purpose:** Preserve disagreement and evidence instead of silently averaging model outputs.  
**Process:** `docs/collaboration/multi-model-process.md`

Copy this template for every non-trivial cross-model proposal before disposition.

---

## Header

| Field | Value |
|---|---|
| Record ID | REC-YYYYMMDD-### |
| Date | |
| Triggering contribution IDs | e.g. GEM-IMPL-001, GROK-ATTACK-003, GPT-SPEC-007 |
| Commit / ref under discussion | |
| Architecture lead (ChatGPT / human) | |
| Status | OPEN / NEEDS-TEST / RESOLVED |

## Proposals under conflict

### Proposal A
- **ID:**
- **Source:** ChatGPT / Gemini / Grok / Human
- **Summary:**
- **Evidence offered:**
- **Requested change:**

### Proposal B (if any)
- **ID:**
- **Source:**
- **Summary:**
- **Evidence offered:**
- **Requested change:**

### Proposal C (if any)
...

## Points of agreement

List only what is actually shared after independent review. Do not invent consensus.

-

## Points of unresolved disagreement

| Topic | Position A | Position B | Why it matters | Evidence still missing |
|---|---|---|---|---|
| | | | | |

## Independence / dependence notes

- Did any model see another model’s output before producing this proposal?
- Shared source material or prompts?
- Common training-data or tool dependence that could explain convergence?

## Attack / critique summary (from Grok or other red-team)

-

## Required tests before disposition

Link to conditions in `test-matrix-v0.md` or new tests:

| Test ID | What it must show | Pass / fail criterion |
|---|---|---|
| | | |

## Disposition

| Decision | ACCEPTED / ACCEPTED-WITH-MODIFICATION / REJECTED / DEFERRED / SUPERSEDED / NEEDS-TEST |
|---|---|
| Final text or code change | |
| Narrowing applied (if any) | |
| Commit hash | |
| Rationale (evidence-based) | |
| Dissent preserved? | Yes / No — location of dissent record |

## Provenance labels applied

```text
OI-PREEXISTING / HUMAN-KARA / AI-CHATGPT / AI-GEMINI / AI-GROK /
AI-INDEPENDENT-CONVERGENCE / EXTERNAL-PRIOR-ART / IMPLEMENTATION-ONLY /
ATTRIBUTION-UNRESOLVED / JOINT
```

## Follow-ups

- [ ] Update contribution-log.md
- [ ] Update relevant spec or experiment docs
- [ ] Open issue for deferred items
- [ ] Schedule second-pass red-team if accepted with modification
