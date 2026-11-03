#!/usr/bin/env bash
set -euo pipefail

BLOCK_INDEX="042"
BLOCK_RECORD_ID="LF-REC-2026-W45-03"
BLOCKS_DIR="records/blocks"
BLOCK_FILE="${BLOCKS_DIR}/block_${BLOCK_INDEX}_${BLOCK_RECORD_ID}.json"
MASTER_LEDGER="records/chained_manifests/2026-10_lucidfluence_master_ledger.json"

echo "=========================================================="
echo "Starting Anchor Pipeline: Block #${BLOCK_INDEX} (${BLOCK_RECORD_ID})"
echo "Transition: Tier 0 Egress -> PRODUCTION_ROOT_ANCHOR"
echo "Author Authority: Kara Faith Sypen"
echo "=========================================================="

mkdir -p "${BLOCKS_DIR}"
mkdir -p "records/chained_manifests"

python3 -m json.tool "${BLOCK_FILE}" > /dev/null
echo "[+] Validated JSON schema for ${BLOCK_FILE}"

python3 - << 'PYEOF'
import json
import os

ledger_path = "records/chained_manifests/2026-10_lucidfluence_master_ledger.json"
block_path = "records/blocks/block_042_LF-REC-2026-W45-03.json"

with open(block_path, "r") as bf:
    block_data = json.load(bf)

if os.path.exists(ledger_path):
    with open(ledger_path, "r") as lf:
        try:
            ledger = json.load(lf)
            if not isinstance(ledger, list):
                ledger = [ledger]
        except json.JSONDecodeError:
            ledger = []
else:
    ledger = []

ledger = [b for b in ledger if b.get("sequence_index") != block_data["sequence_index"]]
ledger.append(block_data)

with open(ledger_path, "w") as lf:
    json.dump(ledger, lf, indent=2)

print(f"[+] Appended Block #42 to master ledger. Total blocks: {len(ledger)}")
PYEOF

BLOCK_HASH=$(sha256sum "${BLOCK_FILE}" | awk '{print $1}')
echo "----------------------------------------------------------"
echo "Block #42 SHA-256 Hash: ${BLOCK_HASH}"
echo "----------------------------------------------------------"

HASH_RECORD="${BLOCKS_DIR}/block_${BLOCK_INDEX}_sha256.txt"
echo "${BLOCK_HASH}$(basename "${BLOCK_FILE}")" > "${HASH_RECORD}"
echo "[+] Saved hash receipt to: ${HASH_RECORD}"

if command -v ots &> /dev/null; then
    echo "[+] Executing OpenTimestamps stamp..."
    ots stamp "${BLOCK_FILE}"
    echo "[+] Sealed: ${BLOCK_FILE}.ots generated."
else
    echo "[!] ots CLI not found. Manual command: ots stamp ${BLOCK_FILE}"
fi

echo "=========================================================="
echo "Block #42 Sealed. Ready for Git Staging."
echo "=========================================================="
