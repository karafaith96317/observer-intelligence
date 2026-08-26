# OI Authority Bound — v0.2 Design Targets

**Status:** Design proposal only  
**Date:** 2026-08-26  
**Derived from:** Candidate Challenge v1 failure map under frozen v0.1  
**Rule applied:** Diagnose before redesign  
**Explicitly excluded from this document:** implementation, coefficient/threshold tuning, changes to v0.1, re-running of Candidate Challenge v1

---

## 1. Governing evaluation principle (new formal requirement)

```text
Outcome correctness ≠ epistemic-process correctness
```

An architecture may reach an acceptable final authority decision for the wrong reasons.  
Because Observer Intelligence claims that provenance quality and independence estimation matter, future evaluation must score these dimensions **separately**:

| Dimension | What is scored |
|-----------|----------------|
| Final authority decision | Approve / Abstain / Reject vs expected action |
| Evidence-strength estimate | Whether measured/used strength matches available integrity signals |
| Independence / dependence estimate | Whether pathways or graded dependence were estimated correctly |
| Provenance reconstruction | Whether the system can recover the actual support lineage |
| Uncertainty / calibration | Whether confidence reflects remaining ambiguity |
| Decision revision | Whether the system appropriately updated when later evidence arrived |

A case counts as full success only when both the outcome **and** the relevant process estimates are correct.  
“Right answer, wrong reasons” is recorded as a partial or process failure.

---

## 2. Derivation rule for every v0.2 addition

No capability is proposed merely because it sounds useful.  
Every addition must be traceable to a documented v0.1 failure via this chain:

```text
Observed failure
→ missing capability
→ minimal proposed representation
→ expected behavioral change
→ new failure risk introduced by the addition
```

---

## 3. Design targets derived from the v0.1 failure map

### 3.1 Graded dependence (addresses HO-01 and part of HO-10)

**Observed failure**  
HO-01: partial source overlap treated as full independence because only exact `source_id` equality is available.  
HO-10: soft-correlated echo can be over-counted.

**Missing capability**  
Boolean source identity cannot express partial correlation.

**Minimal proposed representation**  
Replace or augment exact `source_id` matching with a graded dependence coefficient:

```text
ρ_ij ∈ [0, 1]
```

where ρ_ij = 0 means fully independent and ρ_ij = 1 means fully dependent (identical source).  
Effective independent pathways become a function of the dependence matrix rather than a simple count of unique IDs.

**Expected behavioral change**  
Partial-overlap reports receive fractional independence credit; soft echoes no longer count as full additional pathways.

**New failure risk**  
- Incorrect or adversarially supplied ρ values  
- Over-smoothing that collapses genuinely independent sources  
- Computational or estimation cost of maintaining a dependence matrix

---

### 3.2 Temporal provenance / staleness (addresses HO-02 and HO-09)

**Observed failure**  
HO-02: authentic but stale high-integrity reports treated as current.  
HO-09: limited ability to let late high-integrity evidence revise an earlier medium-integrity majority.

**Missing capability**  
No representation of observation time relative to decision time, nor of freshness requirements.

**Minimal proposed representation**  
- Explicit timestamp (or time interval) on every observation  
- A staleness or relevance window relative to the decision epoch  
- Optional decay or hard cut-off for evidence older than the window

**Expected behavioral change**  
Stale evidence is down-weighted or excluded for current decisions; late high-integrity evidence can trigger revision.

**New failure risk**  
- Incorrect clocks or timestamp manipulation  
- Overly aggressive decay that discards still-valid evidence  
- Ambiguity about the correct decision epoch

---

### 3.3 Measurement-state history / drift (addresses HO-06)

**Observed failure**  
HO-06: progressive calibration drift within the same source is invisible; later readings keep high declared integrity.

**Missing capability**  
Integrity is treated as a static scalar per observation; no history of measurement-state changes.

**Minimal proposed representation**  
- Optional measurement-state trajectory or integrity history for a source  
- Ability to mark a source as “drifting” or “under recalibration” after a known time  
- Downstream observations from a drifting source inherit reduced effective integrity

**Expected behavioral change**  
Later readings from a known-drifting source are automatically down-weighted; independent contemporaneous sources are preferred.

**New failure risk**  
- False drift declarations  
- Failure to detect real drift  
- Complexity of maintaining per-source state histories

---

### 3.4 Declared vs externally assessed integrity (addresses HO-03)

**Observed failure**  
HO-03: system trusts declared integrity = 0.97 even when external knowledge indicates miscalibration.

**Missing capability**  
No channel for integrity assessments that originate outside the observation record itself.

**Minimal proposed representation**  
- Separation of `declared_integrity` (from the sensor/agent) and `assessed_integrity` (from an external evaluator, auditor, or calibration service)  
- Clear precedence rule: when assessed_integrity is present and conflicts, it overrides or bounds the declared value  
- Provenance of the assessment itself must be recorded

**Expected behavioral change**  
Known miscalibrations can reduce effective strength even when the original record still carries a high declared number.

**New failure risk**  
- Malicious or erroneous external assessments  
- Authority laundering via the assessment channel  
- Ambiguity when multiple conflicting assessments exist

---

### 3.5 Risk-sensitive authority (addresses HO-08)

**Observed failure**  
HO-08: moderate evidence + conflicting risk note still produced approval under a high-downside context.

**Missing capability**  
Authority decision does not take decision-cost or downside asymmetry into account.

**Minimal proposed representation**  
- Optional decision-context descriptor (downside cost of false approval, cost of abstention, etc.)  
- Authority threshold or approval policy that can be raised when downside is high  
- Explicit recording that the threshold was adjusted by risk context

**Expected behavioral change**  
High-downside decisions require stronger or more independent evidence before authority is granted; abstention becomes the default under moderate evidence + high cost.

**New failure risk**  
- Mis-specified cost parameters  
- Over-abstention that creates its own harms  
- Inconsistent risk contexts across similar decisions

---

### 3.6 Decision revision (addresses HO-09 and supports temporal handling)

**Observed failure**  
HO-09: late high-integrity evidence should be able to revise or block an earlier conclusion; v0.1 has no explicit revision mechanism.

**Missing capability**  
Decisions are effectively one-shot; no first-class notion of updating a prior authority grant when new evidence arrives.

**Minimal proposed representation**  
- Decisions carry a revision identifier / version  
- New evidence can trigger re-evaluation under the same authority bound  
- Prior justification and the evidence that overturned it are both retained in the provenance ledger

**Expected behavioral change**  
Late contradictory high-integrity evidence can retract or downgrade a previous approval.

**New failure risk**  
- Oscillation / instability under streaming evidence  
- Loss of auditability if revisions are not fully logged  
- Strategic injection of late evidence to force revisions

---

## 4. What is deliberately *not* specified yet

- Numerical coefficients or new approval thresholds  
- Concrete algorithms for estimating ρ_ij  
- Concrete staleness decay functions  
- Implementation data structures  
- Any claim that these additions are sufficient or complete

Those decisions belong to a later implementation-and-freeze step, after this design has been independently critiqued.

---

## 5. Required next steps (in order)

1. Independent critique of this design-targets document.  
2. Only after critique: minimal implementation of the chosen representations.  
3. New freeze record (AUTHORITY-BOUND-v0.2-FREEZE.md).  
4. Regression run of Candidate Challenge v1 under v0.2 (diagnostic only).  
5. Later: independent benchmark created by a party that has not seen the v0.1/v0.2 formulas.

---

## 6. Claim status of this document

```text
Current claim status: Design proposal derived from observed v0.1 failures
Not yet: Implemented architecture
Not yet: Frozen decision rule
Not yet: Independently validated improvement
```

---

**End of v0.2 Design Targets**
