# Submitted ERA-GOS / LucidFluence / OI v0.2.1 bundle

**Status: DRAFT_UNVERIFIED — archival proposal, not a production release.**

Submitted by Kara Faith Sypen in conversation on 2026-11-03, with permission to add to `karafaith96317/observer-intelligence`. This directory preserves the four supplied file bodies; conversation headings and Markdown fences have been removed. Their original assertions and defects remain visible for review. This README supplies the evidence boundary and is not a claim that the implementation has been hardened. Related review: #20.

The existing repository runtime is `src/oi_runtime_v0_1.py`. The submitted runtime and tests are deliberately kept under this proposal directory to avoid replacing or shadowing the existing implementation. Relative paths inside the submitted shell script assume execution from the bundle directory. **Do not execute that script against a real ledger.** It has only been syntax-checked.

## Submitted architecture

- `oi_runtime_v0_1.py`: proposed TPM quote checks, modeled round-trip timing, Ed25519 authority tokens, and an in-memory promotion decision.
- `tests/test_hardware_attestation.py`: two simulated success tests.
- `records/blocks/block_042_LF-REC-2026-W45-03.json`: unverified example promotion manifest, preserved as submitted; not an accepted chain entry.
- `scripts/anchor_block_042.sh`: submitted ledger-writing and timestamp-request script, preserved for review only.

The manifest's `ANCHOR_READY`, `ACTIVE_TIER_1_FEED`, and verified-gate strings are submitted claims, not verified events. The regional node names do not establish deployed hardware, institutional participation, or authorization. A legal name is metadata, not a cryptographic identity credential. No private signing key was supplied or committed.

## Review findings and required follow-up

1. Establish trusted per-node attestation-key enrollment and parse the signed TPM structure, including exact challenge and PCR selection/digest binding. Current code does not establish bare-metal execution.
2. Treat the RTT model as a timing consistency heuristic. Its fiber factor, path geometry, and processing allowance do not establish location, a detected proxy, or a superluminal event. Bind challenges and measurements to authenticated sessions.
3. Replace caller-provided success flags with verified, fresh evidence bound to the particular transition. Define verifier-owned quorum and architecture policy, strict numeric validation, persistent replay protection, and transactional state changes.
4. The promotion controller changes memory and returns a dictionary. No networking or firewall activation occurs. Require separate integration and enforcement evidence before any release claim.
5. Expand tests to cover quote verification and rejection behavior, malformed inputs, stale evidence, policy failures, restart/concurrency behavior, and ledger preservation. Passing the supplied two tests is not a security certification.
6. Reconcile manifest dates: `1793962800` is 2026-11-06T11:00:00Z; 2026-11-03T13:40:00Z is `1793713200`. Verify the actual predecessor hash and attach sources for metrics, test results, token verification, and any real transition. None are established by this example.
7. Rewrite the ledger operation to fail on malformed history, verify continuity, reject conflicting duplicate indexes, and use locking and atomic persistence. The submitted code can replace unreadable history and overwrite an existing block of the same index.
8. `python -m json.tool` validates syntax, not a schema. The checksum receipt needs the standard separator between digest and filename. The script reports sealing even when the timestamp client is absent; distinguish a stamp request/receipt from independently verified anchoring. Neither hashes nor timestamp receipts establish that manifest assertions are true.
9. Original conversation Git commands were suggestions, not execution evidence. A commit acts on the current branch; specify and verify the destination before pushing. This submission uses a new draft branch and does not merge or activate anything.

## Local validation performed

Linux, Python 3.12.14, pytest 9.2.0, cryptography 50.0.0.

```text
python -m pytest tests/test_hardware_attestation.py -q
2 passed, 1 warning in 0.06s

python -m compileall -q oi_runtime_v0_1.py tests/test_hardware_attestation.py
exit 0

bash -n scripts/anchor_block_042.sh
exit 0

JSON parsing: valid
```

The warning came from the environment's AnyIO pytest plugin using a deprecated pytest alias. Pytest was initially missing and was installed before the successful run. Validation used a standalone copy of this directory. Repository-wide integration tests were not run. No real TPM, real network timing, production transition, ledger append, OpenTimestamps request, or timestamp verification was performed.

To reproduce only the two submitted simulations in a disposable environment, from the repository root:

```bash
cd proposals/tier0-v0.2.1-2026-11-03
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pytest==9.2.0 cryptography==50.0.0
python -m pytest --rootdir=. -o pythonpath=. tests/test_hardware_attestation.py -q
```

These dependency versions describe the validation environment, not an audited production dependency policy. The source is retained for provenance; hardening and integration should be separately reviewed changes.
