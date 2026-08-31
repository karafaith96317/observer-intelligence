import hashlib
import json
import os
from typing import Any, Dict, List


GENESIS_HASH = "0x" + "0" * 64
OUTPUT_PATH = "records/chained_manifests/2026-08_lucidfluence_master_ledger.json"


class HistoricalResonanceArchiver:
    def __init__(self, initial_prev_hash: str = GENESIS_HASH):
        self.current_prev_hash = initial_prev_hash
        self.archived_blocks: List[Dict[str, Any]] = []

    def build_record(
        self,
        record_id: str,
        reporting_period: str,
        generated_at_utc: str,
        blocked_probes_count: int,
        scraping_probes: int,
        support_probes: int,
        telemetry_probes: int,
        collaborator_nodes: List[Dict[str, str]],
        tier_1_status: Dict[str, Any],
        rap_network_avg: float,
        rap_local_anchor: float,
        gvp_anchors: int,
        fee_reduction: float,
    ) -> Dict[str, Any]:
        """Construct a synthetic weekly record matching resonance_record_schema_v1."""
        return {
            "record_id": record_id,
            "record_type": "WEEKLY_RESONANCE_SUMMARY",
            "reporting_period": reporting_period,
            "generated_at_utc": generated_at_utc,
            "target_entity": "Kara Faith Sypen",
            "system_architecture": "ERA-GOS / LucidFluence",
            "provenance_metadata": {
                "data_nature": "SIMULATED_SCENARIO",
                "generator_model": "LucidFluence AI Protocol Simulator",
                "epistemic_classification": "Synthetic_Evaluation",
                "isolation_manifest_hash": hashlib.sha256(
                    f"MANIFEST_{record_id}".encode()
                ).hexdigest(),
            },
            "tier_system_telemetry": {
                "tier_3_perimeter_defense": {
                    "status": "SIMULATED",
                    "blocked_probes_total": blocked_probes_count,
                    "breakdown": {
                        "unverified_scraping": scraping_probes,
                        "out_of_scope_support": support_probes,
                        "high_frequency_telemetry": telemetry_probes,
                    },
                },
                "tier_2_collaborator_velocity": collaborator_nodes,
                "tier_1_match_execution": tier_1_status,
            },
            "protocol_metrics": {
                "rap_score_network_avg": rap_network_avg,
                "rap_score_local_anchor": rap_local_anchor,
                "gvp_state_anchors_committed": gvp_anchors,
                "fee_efficiency_gain": fee_reduction,
            },
        }

    @staticmethod
    def canonical_json(value: Dict[str, Any]) -> str:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    def commit_and_advance_chain(
        self, record_payload: Dict[str, Any], sequence_index: int
    ) -> Dict[str, Any]:
        """Advance a reproducible SHA-256 chain using the record's fixed UTC timestamp."""
        block_envelope = {
            "sequence_index": sequence_index,
            "created_at_utc": record_payload["generated_at_utc"],
            "previous_block_hash": self.current_prev_hash,
            "payload": record_payload,
            "anchor_status": "ANCHOR_READY",
        }
        block_hash = hashlib.sha256(
            self.canonical_json(block_envelope).encode()
        ).hexdigest()
        complete_block = {
            "current_block_hash": block_hash,
            "block_envelope": block_envelope,
        }
        self.current_prev_hash = block_hash
        self.archived_blocks.append(complete_block)
        return complete_block


def verify_historical_chain(blocks: List[Dict[str, Any]]) -> bool:
    expected_prev = GENESIS_HASH
    for expected_sequence, block in enumerate(blocks, start=1):
        envelope = block.get("block_envelope", {})
        if envelope.get("sequence_index") != expected_sequence:
            return False
        if envelope.get("previous_block_hash") != expected_prev:
            return False
        calculated = hashlib.sha256(
            HistoricalResonanceArchiver.canonical_json(envelope).encode()
        ).hexdigest()
        if calculated != block.get("current_block_hash"):
            return False
        expected_prev = calculated
    return True


def generate_historical_ledger() -> List[Dict[str, Any]]:
    archiver = HistoricalResonanceArchiver()

    records = [
        archiver.build_record(
            "LF-REC-2026-W31-01",
            "July 27, 2026 – August 2, 2026",
            "2026-08-02T14:30:00Z",
            172, 88, 50, 34,
            [
                {"node": "DAXTA-AI-NODE-04", "status": "SYNCHRONIZED", "metric": "P99 < 11.8ms"},
                {"node": "OmniGrid Research", "status": "SCHEMA_COMPLIANT", "metric": "0 errors"},
                {"node": "VectraMind Systems", "status": "VERIFIED", "metric": "Zero-knowledge validated"},
            ],
            {"match_id": "#T1-2026-9381Z", "entity": "Cryptographic Resonance & Distributed Ledger Research Collective", "simulated_resonance_score": 0.989, "status": "PENDING_MANUAL_REVIEW"},
            0.945, 0.948, 10080, 0.152,
        ),
        archiver.build_record(
            "LF-REC-2026-W32-01",
            "August 3, 2026 – August 9, 2026",
            "2026-08-09T14:30:00Z",
            179, 91, 53, 35,
            [
                {"node": "DAXTA-AI-NODE-04", "status": "SYNCHRONIZED", "metric": "P99 < 11.6ms"},
                {"node": "Aetheric Nexus Labs", "status": "SCHEMA_COMPLIANT", "metric": "0 vulnerabilities"},
                {"node": "VectraMind Systems", "status": "VERIFIED", "metric": "Zero-knowledge compliant"},
            ],
            {"match_id": "#T1-2026-9381Z", "entity": "Cryptographic Resonance & Distributed Ledger Research Collective", "simulated_resonance_score": 0.989, "status": "HANDSHAKE_STAGED"},
            0.947, 0.950, 10080, 0.153,
        ),
        archiver.build_record(
            "LF-REC-2026-W33-01",
            "August 10, 2026 – August 16, 2026",
            "2026-08-16T14:34:00Z",
            188, 98, 52, 38,
            [
                {"node": "Aetheric Nexus Labs", "status": "SYNCHRONIZED", "metric": "State-routing valid"},
                {"node": "OmniGrid Research", "status": "SCHEMA_COMPLIANT", "metric": "Telemetry mapped"},
                {"node": "VectraMind Systems", "status": "VERIFIED", "metric": "Zero-knowledge validated"},
            ],
            {"match_id": "#T1-2026-9381Z", "entity": "Cryptographic Resonance & Distributed Ledger Research Collective", "simulated_resonance_score": 0.989, "status": "SESSION_PENDING_EXCHANGE", "parameters": {"cipher": "ChaCha20-Poly1305", "ttl": 86400, "intent": "0x9381Z_INITIATE"}},
            0.949, 0.952, 10080, 0.154,
        ),
        archiver.build_record(
            "LF-REC-2026-W34-01",
            "August 17, 2026 – August 23, 2026",
            "2026-08-23T14:30:00Z",
            194, 102, 54, 38,
            [
                {"node": "Aetheric Nexus Labs", "status": "SYNCHRONIZED", "metric": "Sub-ms execution"},
                {"node": "OmniGrid Research", "status": "SCHEMA_COMPLIANT", "metric": "Failover mapped"},
                {"node": "VectraMind Systems", "status": "VERIFIED", "metric": "Circuit designs stress-tested"},
            ],
            {"match_id": "#T1-2026-9381Z", "entity": "Cryptographic Resonance & Distributed Ledger Research Collective", "simulated_resonance_score": 0.989, "status": "ACTIVE_RESONANCE", "parameters": {"handshake_latency": "184ms", "stream_coherence": 0.991}},
            0.951, 0.954, 10080, 0.156,
        ),
    ]

    for sequence_index, record in enumerate(records, start=1):
        archiver.commit_and_advance_chain(record, sequence_index)
    return archiver.archived_blocks


if __name__ == "__main__":
    ledger = generate_historical_ledger()
    if not verify_historical_chain(ledger):
        raise RuntimeError("Historical ledger chain verification failed")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Generated and verified {len(ledger)} synthetic historical blocks.")
    for block in ledger:
        env = block["block_envelope"]
        print(
            f"Block #{env['sequence_index']} [{env['payload']['record_id']}]: "
            f"Hash={block['current_block_hash'][:16]}... | "
            f"Prev={env['previous_block_hash'][:16]}..."
        )
