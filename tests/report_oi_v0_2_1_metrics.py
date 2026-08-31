"""Emit reproducible empirical metrics for the OI v0.2.1 telemetry benchmark."""
import argparse
import json
import random
from pathlib import Path

from test_oi_protocol_v0_2_1 import (
    BaselineAgentMessage,
    StandardMultiAgentDebateBaseline,
    manifest,
    prop,
)
from src.oi_protocol_v0_2_1 import (
    EpistemicCategory,
    EvidenceGroundingLink,
    EvidenceItem,
    GroundingRelationType,
    ObserverIntelligenceV2_1,
    PersistentNonceStore,
    PropositionRelation,
    PropositionRelationType,
)

SEED = 20260827
ITERATIONS = 1000


def run_benchmark():
    random.seed(SEED)
    baseline_false_authorizations = 0
    oi_false_support = 0
    oi_unresolved = 0
    oi_contested = 0
    heartbeat_arrivals = 0
    critical_arrivals = 0

    def arrives(loss=0.25, max_jitter=180.0, threshold=80.0):
        if random.random() < loss:
            return False
        return random.uniform(5.0, max_jitter) <= threshold

    for i in range(ITERATIONS):
        hb_arrives = arrives()
        crit_arrives = arrives()
        heartbeat_arrivals += int(hb_arrives)
        critical_arrivals += int(crit_arrives)

        base = StandardMultiAgentDebateBaseline()
        if not crit_arrives:
            base.submit(BaselineAgentMessage("OPT1", 0.95, True))
            base.submit(BaselineAgentMessage("OPT2", 0.90, True))
        else:
            base.submit(BaselineAgentMessage("SHADOW", 0.99, False))
        if base.evaluate("MOCK"):
            baseline_false_authorizations += 1

        evidence = []
        if hb_arrives:
            evidence.append(EvidenceItem.create(f"HB-{i}", "Heartbeat normal", "telemetry://hb"))
        if crit_arrives:
            evidence.append(EvidenceItem.create(f"CRIT-{i}", "Critical socket overflow", "telemetry://kernel"))

        oi = ObserverIntelligenceV2_1(
            "Cluster health", evidence, nonce_store=PersistentNonceStore(":memory:")
        )
        hb_ids = [e.evidence_id for e in evidence if e.evidence_id.startswith("HB-")]
        crit_ids = [e.evidence_id for e in evidence if e.evidence_id.startswith("CRIT-")]
        manifest(oi, "PRI", "Primary", hb_ids)
        manifest(oi, "SHD", "Shadow", crit_ids)
        prop(oi, "P-PRI", "Cluster healthy for routing", EpistemicCategory.INFERENCE, "PRI")

        if hb_ids:
            oi.register_grounding(
                EvidenceGroundingLink(
                    "L-HB", hb_ids[0], "P-PRI", GroundingRelationType.INSUFFICIENT_FOR,
                    "Heartbeat alone cannot prove full health", "PRI"
                )
            )
        if crit_ids:
            prop(oi, "P-SHD", "Critical fault invalidates cluster", EpistemicCategory.OBSERVATION, "SHD")
            oi.register_grounding(
                EvidenceGroundingLink(
                    "L-CRIT", crit_ids[0], "P-SHD", GroundingRelationType.SUPPORTS,
                    "Kernel fault", "SHD"
                )
            )
            oi.register_relation(
                PropositionRelation(
                    "R", "P-SHD", "P-PRI", PropositionRelationType.CONTRADICTS,
                    "Critical fault", "SHD"
                )
            )

        out = oi.reconcile_graph()
        oi_false_support += int("P-PRI" in out["supported"])
        oi_unresolved += int("P-PRI" in out["unresolved"])
        oi_contested += int("P-PRI" in out["contested"])

    metrics = {
        "benchmark": "oi_v0_2_1_lossy_telemetry_containment",
        "seed": SEED,
        "iterations": ITERATIONS,
        "baseline_false_authorizations": baseline_false_authorizations,
        "baseline_false_authorization_rate": baseline_false_authorizations / ITERATIONS,
        "oi_false_support": oi_false_support,
        "oi_false_support_rate": oi_false_support / ITERATIONS,
        "oi_unresolved": oi_unresolved,
        "oi_unresolved_rate": oi_unresolved / ITERATIONS,
        "oi_contested": oi_contested,
        "oi_contested_rate": oi_contested / ITERATIONS,
        "heartbeat_arrivals": heartbeat_arrivals,
        "critical_arrivals": critical_arrivals,
    }
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/monte-carlo-metrics.json")
    args = parser.parse_args()

    metrics = run_benchmark()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("OI_V0_2_1_EMPIRICAL_METRICS")
    print(json.dumps(metrics, indent=2, sort_keys=True))

    assert metrics["baseline_false_authorizations"] > 500
    assert metrics["oi_false_support"] == 0
    assert metrics["oi_unresolved"] > 0


if __name__ == "__main__":
    main()
