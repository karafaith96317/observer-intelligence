# Observer Intelligence: Reconciliation Decision Record (RDR)

**Record ID:** `RDR-YYYY-###`  
**Target feature / component:**  
**Evaluation date:**  
**Human authorizing lead:**  
**Repository commit tested:**  

---

## 1. Divergence / Conflict Summary

- **Architecture requirement (`GPT-SPEC-###` or `KFS-ROOT-###`):**
- **Implementation / critique (`GEM-IMPL-###`):**
- **Adversarial challenge (`GROK-ATK-###`):**
- **Exact disagreement:**

## 2. Evidence Boundary

- **Artifacts inspected:**
- **Tests / fixtures executed:**
- **Environment:** Python version, dependency versions, OS/runner, commit SHA
- **Random seed(s), if applicable:**
- **Evidence excluded or unavailable:**

## 3. Empirical Findings

- **Baseline outcome:** Passed / Failed / Not Applicable
- **OI engine outcome:** Passed / Failed / Not Executed
- **Observed latency / resource cost:** measured value or `NOT MEASURED`
- **Authorization result:** Allowed / Blocked / Escalated / Not Applicable
- **Provenance completeness:** Complete / Partial / Failed
- **Unexpected behavior:**

Do not substitute predicted values for measured results.

## 4. Reconciliation Verdict

Choose one:

- [ ] **ACCEPTED — DIRECT MERGE:** evidence supports the change for the tested scope; no known unresolved finding within that scope blocks merge.
- [ ] **ACCEPTED WITH PATCHES:** useful contribution, but specified changes/tests are required before or with merge.
- [ ] **CONTESTED / REMANDED:** evidence is insufficient or contradictory; further tests or redesign required.
- [ ] **REJECTED:** falsified, unsafe, redundant, or outside scope; preserve rationale and evidence.

**Rationale:**

**Residual risks / open attacks:**

**Required follow-up:**

## 5. Lineage & Repository References

- **Related contribution IDs:**
- **PR / issue:**
- **Tested commit SHA:**
- **Resulting commit SHA (after merge/patch, if any):**
- **Authority token / nonce reference (only if the implemented protocol generated one):**
- **Archived raw output / CI artifact:**

---

## Reconciliation Principle

A reconciliation record documents what was supported by a defined test at a defined repository state. It does not claim that all possible attack vectors have been exhausted, nor that a passing test proves general safety.
