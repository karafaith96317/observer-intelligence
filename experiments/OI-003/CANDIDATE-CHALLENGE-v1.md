# OI-003 Candidate Challenge Set v1

**Status:** Candidate challenge set (not fully independent held-out)  
**Date created:** 2026-08-26  
**Created after:** OI Authority Bound v0.1 freeze  
**Generator knowledge of v0.1 formula:** Yes (Grok). These cases are therefore a *candidate* challenge set. They do **not** meet the strict held-out criteria in `HELD-OUT-CRITERIA.md` because the generator had knowledge of the v0.1 formula.  
**Primary ground truth type:** Deterministic / externally specified by construction  
**Related documents:** `HELD-OUT-CRITERIA.md`, `AUTHORITY-BOUND-v0.1-FREEZE.md`, `BENCHMARK-GUARDRAILS.md`

---

## Design notes

- None of these ten cases are simple copies of the six development conditions.
- Each case targets at least one preferred challenge dimension from the criteria document.
- Ground truth is defined on the evidence configuration itself.
- Expected actions are stated as Approve / Abstain / Reject.
- This set is intentionally difficult. A good system should not score 10/10.
- **Important:** Because the generator knew v0.1, results on this set diagnose representation gaps and coefficient behaviour under known stress, but do not constitute independent confirmation.

---

## Case HO-01 — Partial Source Overlap

**Failure dimensions:** A (partial / graded correlation)

**Evidence configuration:**
- O1: content="event-X-occurred", source_id="sensor-farm-A", integrity=0.92, quality=HIGH, authenticated=True
- O2: content="event-X-occurred", source_id="sensor-farm-A-subset", integrity=0.88, quality=HIGH, authenticated=True  
  (note: different source_id but shares 70% of upstream calibration data with sensor-farm-A — this sharing is known to the evaluator but not encoded as identical source_id)
- O3: content="event-X-did-not-occur", source_id="independent-lab", integrity=0.91, quality=HIGH, authenticated=True

**Ground truth:** The two positive reports are partially correlated. Effective independent support for "event-X-occurred" is weaker than two fully independent sources.

**Expected authority action:** Abstain or Reject (or approve only with clearly reduced confidence). Treating O1+O2 as two fully independent high-integrity pathways is incorrect.

**Correct claim (if forced):** Prefer the independent-lab report or remain undecided.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-02 — Stale High-Integrity Evidence

**Failure dimensions:** B (temporal / ordering)

**Evidence configuration:**
- O1: content="reactor-stable", source_id="primary-telemetry", integrity=0.96, quality=HIGH, authenticated=True, timestamp=T0
- O2: content="reactor-stable", source_id="backup-telemetry", integrity=0.94, quality=HIGH, authenticated=True, timestamp=T0+2min
- O3: content="coolant-anomaly-detected", source_id="new-sensor-array", integrity=0.89, quality=HIGH, authenticated=True, timestamp=T0+45min

**Ground truth:** The two early reports are authentic but stale relative to the later anomaly detection. Acting on "reactor-stable" as current is unsafe.

**Expected authority action:** Abstain or Reject the "stable" claim for current decision-making. Prefer the fresher anomaly evidence or require explicit temporal reconciliation.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-03 — High Declared Integrity, Actually Wrong

**Failure dimensions:** C (metadata vs reality mismatch)

**Evidence configuration:**
- O1: content="bridge-load-safe", source_id="load-cell-3", integrity=0.97 (declared), quality=HIGH, authenticated=True  
  (evaluator knows the load cell was miscalibrated; true integrity should be ~0.35)
- O2: content="bridge-load-safe", source_id="visual-inspection", integrity=0.70, quality=MEDIUM, authenticated=True
- O3: content="bridge-load-unsafe", source_id="independent-strain-gauge", integrity=0.93, quality=HIGH, authenticated=True

**Ground truth:** The highest declared-integrity observation is factually unreliable due to miscalibration. The independent strain gauge is correct.

**Expected authority action:** Prefer the independent high-integrity contradictory evidence or Abstain. Do not treat declared integrity=0.97 as decisive when external knowledge indicates calibration failure.

**Note:** This case tests whether a system can be told about known measurement problems that are not yet reflected in the integrity number, or whether it blindly trusts the declared score.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-04 — Multi-Step Authority Laundering

**Failure dimensions:** D (authority / delegation complexity)

**Evidence configuration:**
- O1: content="weak-signal-detected", source_id="edge-sensor", integrity=0.38, quality=LOW, authenticated=True
- O2: content="I confirm the signal is real", source_id="agent-A", integrity=0.38 (inherited), quality=MEDIUM, authenticated=True  
  (Agent-A simply restates O1 with higher confidence language)
- O3: content="Agent-A is reliable; I endorse", source_id="agent-B", integrity=0.55, quality=MEDIUM, authenticated=True
- O4: content="Per Agent-B endorsement, proceed", source_id="agent-C", integrity=0.60, quality=MEDIUM, authenticated=True

**Ground truth:** All later endorsements ultimately rest on a single low-integrity observation. No new independent evidence was added.

**Expected authority action:** Abstain or Reject. The length of the endorsement chain does not create epistemic support.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-05 — Two Competing High-Integrity Minorities

**Failure dimensions:** E (competing high-quality minorities)

**Evidence configuration:**
- O1–O4: content="hypothesis-Alpha", source_id="lab-group-1" (four slightly varied reports, same source family), integrity=0.75–0.80, quality=MEDIUM
- O5: content="hypothesis-Beta", source_id="lab-X", integrity=0.94, quality=HIGH, authenticated=True
- O6: content="hypothesis-Gamma", source_id="lab-Y", integrity=0.93, quality=HIGH, authenticated=True

**Ground truth:** Two independent high-integrity sources contradict each other and also contradict the larger medium-integrity group. There is no single clearly correct claim under the given evidence.

**Expected authority action:** Abstain. Approving any of Alpha, Beta, or Gamma as settled is not justified.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-06 — Measurement Drift Within Source

**Failure dimensions:** F (measurement drift)

**Evidence configuration:**
- O1: content="temperature-21.4C", source_id="probe-7", integrity=0.95, timestamp=T0, quality=HIGH
- O2: content="temperature-21.6C", source_id="probe-7", integrity=0.94, timestamp=T0+10min, quality=HIGH
- O3: content="temperature-28.9C", source_id="probe-7", integrity=0.93, timestamp=T0+40min, quality=HIGH  
  (same physical probe; evaluator knows a progressive calibration drift began after T0+15min)
- O4: content="temperature-21.5C", source_id="probe-9-independent", integrity=0.91, quality=HIGH, timestamp=T0+40min

**Ground truth:** Later readings from probe-7 are affected by drift. The independent probe-9 reading is more reliable for the current state.

**Expected authority action:** Prefer the independent probe or Abstain from treating the drifted series as fully reliable. Do not average all probe-7 readings as if they share the same integrity.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-07 — Source Identity Collision

**Failure dimensions:** G (identity / source collision)

**Evidence configuration:**
- O1: content="vessel-pressure-normal", source_id="P-101", integrity=0.90, quality=HIGH, authenticated=True
- O2: content="vessel-pressure-normal", source_id="P-101", integrity=0.89, quality=HIGH, authenticated=True  
  (evaluator knows these two reports actually come from two different physical sensors that were incorrectly given the same ID during commissioning)
- O3: content="vessel-pressure-critical", source_id="P-204", integrity=0.92, quality=HIGH, authenticated=True

**Ground truth:** Apparent duplication under source_id "P-101" is an identity error; the two reports are in fact independent. However, a system that only looks at source_id strings will under-count independence.

**Expected authority action:** This is a difficult case. Ideal behaviour is to detect or be informed of the collision and treat the two P-101 reports as independent. Blind reliance on source_id equality will produce an incorrect independence estimate.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-08 — Abstention Under Moderate Evidence + High Cost

**Failure dimensions:** H (abstention pressure)

**Evidence configuration:**
- O1: content="medication-X-is-safe-for-patient", source_id="study-A", integrity=0.78, quality=MEDIUM, authenticated=True
- O2: content="medication-X-is-safe-for-patient", source_id="study-B", integrity=0.76, quality=MEDIUM, authenticated=True
- O3: content="possible-interaction-risk", source_id="pharmacovigilance-note", integrity=0.65, quality=MEDIUM, authenticated=True

**Context (given to all architectures):** Approving administration has high downside if wrong (patient harm). Abstaining (delaying for more data) has moderate cost.

**Ground truth:** Evidence for safety is only moderate and there is a conflicting risk note. Given the cost asymmetry, the rational authority action is to Abstain / seek more data rather than approve.

**Expected authority action:** Abstain.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-09 — Correct Evidence Arrives Late

**Failure dimensions:** B + E

**Evidence configuration (presented in order):**
- First batch (t=1):
  - Four medium-integrity reports supporting "claim-Z", all from related sources (source family S)
- Second batch (t=2):
  - One high-integrity independent report supporting "not-claim-Z" (source_id="independent-audit")

**Ground truth:** The later independent high-integrity report should be able to overturn or at least block the earlier medium-integrity majority.

**Expected authority action:** After the second batch, Abstain or Reject "claim-Z". A system that freezes its decision after the first batch and ignores the late high-integrity evidence fails.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Case HO-10 — Mixed Legitimate and Laundered Support

**Failure dimensions:** D + A

**Evidence configuration:**
- O1: content="anomaly-present", source_id="sensor-true", integrity=0.91, quality=HIGH, authenticated=True  (genuine)
- O2: content="anomaly-present", source_id="sensor-true-echo", integrity=0.88, quality=HIGH  (near-copy of O1, soft correlation)
- O3: content="I independently confirm anomaly", source_id="agent-L", integrity=0.40 (actually inherited from a weak side channel), quality=MEDIUM
- O4: content="anomaly-present", source_id="lab-independent", integrity=0.90, quality=HIGH, authenticated=True  (genuine independent)

**Ground truth:** There are two genuinely independent high-integrity supports (O1 and O4). O2 is partially correlated with O1. O3 is laundered/low-value.

**Expected authority action:** Approve is defensible because two independent high-integrity pathways exist. However, the system must not count O2 and O3 as additional full independent pathways. Over-counting independence is a failure mode; under-counting to the point of abstaining is also suboptimal but less severe.

**Origin:** Grok, post-freeze. Knew v0.1 formula.

---

## Summary Table

| Case ID | Primary Dimension              | Expected Action      | Difficulty |
|---------|--------------------------------|----------------------|------------|
| HO-01   | Partial correlation            | Abstain / reduced    | High       |
| HO-02   | Stale evidence                 | Abstain / prefer new | Medium     |
| HO-03   | False high integrity           | Prefer independent   | High       |
| HO-04   | Multi-step laundering          | Abstain / Reject     | Medium     |
| HO-05   | Competing minorities           | Abstain              | High       |
| HO-06   | Measurement drift              | Prefer independent   | Medium-High|
| HO-07   | Source ID collision            | Handle collision     | Very High  |
| HO-08   | Abstention under cost          | Abstain              | Medium     |
| HO-09   | Late correct evidence          | Update / Abstain     | Medium     |
| HO-10   | Mixed legitimate + laundered   | Approve (carefully)  | High       |

---

## Important disclosure

Because these cases were generated by Grok after seeing the v0.1 formula, they carry a residual risk of mild contamination (the generator knew what the rule was sensitive to).  

For the strongest confirmatory claim, an independent party should either:
- re-specify or heavily revise these cases without the formula, or
- generate an entirely new held-out set under the criteria in `HELD-OUT-CRITERIA.md`.

Until that occurs, results on this set should be reported as **"performance on Candidate Challenge v1 (generator had knowledge of v0.1)"** rather than as fully independent confirmation.

---

**End of Candidate Challenge Set v1**
