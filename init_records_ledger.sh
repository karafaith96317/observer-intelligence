#!/usr/bin/env bash
set -euo pipefail

echo "================================================================================"
echo "INITIALIZING LUCIDFLUENCE / ERA-GOS PROVENANCE & LEDGER ARCHIVE"
echo "================================================================================"

mkdir -p records/synthetic_benchmarks
mkdir -p records/empirical_telemetry
mkdir -p records/chained_manifests
mkdir -p scripts
mkdir -p schemas

SCHEMA_PATH="schemas/resonance_record_schema_v1.json"
ARCHIVER_PATH="scripts/archive_historical_reports.py"
LEDGER_PATH="records/chained_manifests/2026-08_lucidfluence_master_ledger.json"

for required in "$SCHEMA_PATH" "$ARCHIVER_PATH"; do
  if [[ ! -f "$required" ]]; then
    echo "ERROR: required canonical file missing: $required" >&2
    exit 1
  fi
done

echo "[+] Generating deterministic five-block synthetic ledger..."
python3 "$ARCHIVER_PATH"

echo "[+] Verifying ledger regeneration is stable..."
first_sha="$(sha256sum "$LEDGER_PATH" | awk '{print $1}')"
python3 "$ARCHIVER_PATH" >/dev/null
second_sha="$(sha256sum "$LEDGER_PATH" | awk '{print $1}')"

if [[ "$first_sha" != "$second_sha" ]]; then
  echo "ERROR: ledger regeneration is nondeterministic" >&2
  exit 1
fi

echo "[+] Ledger file SHA-256: $second_sha"
echo "[+] Canonical schema: $SCHEMA_PATH"
echo "[+] Historical generator: $ARCHIVER_PATH"
echo "[+] Ledger: $LEDGER_PATH"
echo "================================================================================"
echo "SUCCESS: deterministic synthetic provenance ledger initialized and verified"
echo "================================================================================"
