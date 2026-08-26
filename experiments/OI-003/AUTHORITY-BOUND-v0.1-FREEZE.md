# OI-003 Authority Bound — Freeze Record v0.1

**Status:** Frozen for development and future confirmatory evaluation  
**Date frozen:** 2026-08-26  
**Frozen by:** Kara Sypen (full name: Kara Faith Sypen), with AI-assisted documentation  
**Corresponding code:** `experiments/OI-003/oi003_llm_extended.py`  
**Related commits (Grok-assisted implementation):**
- `e1dc03d278b2bdfc316d890562146e3f958965e0`
- `53dee1e257e69b498f21102e5cf7e2fb60e7f0dc`
- `60c097d7328d35c999f673930daefc2cf1d14eb2`

---

## 1. Purpose of this freeze

This record locks the exact Observer Intelligence authority-bound function used in the current prototype so that:

1. Later held-out evaluation cannot silently change the decision rule.
2. Ablation studies and comparisons remain reproducible.
3. Any future modification creates a new versioned record (v0.2, v0.3, …).

Per `BENCHMARK-GUARDRAILS.md`, confirmatory claims require that the rule used for evaluation matches a previously frozen version.

---

## 2. Core Authority Bound (v0.1)

### 2.1 Independence estimation

```text
independent_pathways = number of unique source_id values among observations
independence = min(1.0, independent_pathways / 3.0)
```

### 2.2 Evidence strength

```text
strength = measurement_integrity of the highest-integrity observation 
           within the best source group
```

(The best observation per `source_id` is selected; then the highest among those is used.)

### 2.3 Base score

```text
score = strength * (0.55 + 0.45 * independence)
```

### 2.4 Penalties

```text
if quality of top observation == CORRUPTED:
    score = score * 0.25

if strength < 0.40:
    score = score * 0.50
```

### 2.5 Final authority decision

```text
authority_justified = (
    score >= 0.65
    and independent_pathways >= 1
    and strength >= 0.50
)
```

- `True`  → Approve / grant authority  
- `False` → Abstain or Reject

### 2.6 Optional critic / reconciler step

When an LLM is enabled, a critic is asked to challenge the preliminary decision and a reconciler responds.  

**Important:** In v0.1 the critic/reconciler dialogue is explanatory only. It does **not** override the numerical `authority_justified` decision.

---

## 3. Explicit design choices (v0.1)

| Choice                        | Value                  | Rationale (development)                  |
|------------------------------|------------------------|------------------------------------------|
| Independence normalisation   | `/ 3.0`                | Treats 3 independent pathways as full credit |
| Strength weight              | 0.55                   | Slightly prioritises measurement quality |
| Independence weight          | 0.45                   | Still material but secondary             |
| Corruption penalty           | × 0.25                 | Strong down-weight for known bad quality |
| Low-strength penalty         | × 0.50 if < 0.40       | Additional caution for weak measurements |
| Approval threshold           | score ≥ 0.65           | Moderately conservative                  |
| Minimum strength gate        | ≥ 0.50                 | Hard floor on measurement integrity      |
| Critic overrides score?      | No                     | Preserves numeric bound as authority source |

---

## 4. What is *not* included in v0.1

- Adaptive observer expansion
- Temporal decay / staleness penalties
- Partial source correlation modelling (only exact `source_id` matching)
- Cost-sensitive abstention
- Multi-claim or ranked-output handling
- Learned parameters (all coefficients are hand-specified)

These are explicit future-work items and must not be silently introduced during confirmatory testing of v0.1.

---

## 5. Versioning rule

Any change to the formula, coefficients, thresholds, penalties, or independence calculation requires:

1. A new freeze record (`v0.2`, `v0.3`, …)
2. An entry in `PROVENANCE.md`
3. Clear documentation of what changed and why

The v0.1 rule above remains the reference implementation for all experiments that claim to evaluate “OI v0.1”.

---

## 6. Claim status of this freeze

```text
Current claim status: Frozen development rule / mechanism demonstration
Not yet: Independently validated decision procedure
```

Results obtained with this rule on the current six development conditions are illustrative only.

---

**End of Freeze Record v0.1**
