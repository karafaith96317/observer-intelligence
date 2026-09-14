# How to run what exists today

Status: research prototype on `main` (OI v2.2 spec, runtime v0.1).

```bash
# from repo root
python3 -m pytest tests -q

# OI-004 mechanism demo (stdlib only)
python3 experiments/OI-004/oi004_runtime.py

# OI-003 development benchmark (no API key)
python3 experiments/OI-003/oi003_llm_extended.py --verbose
```

Tests import `src.oi_runtime_v0_1` by adding the repo root to `sys.path`.
They cover shadow refutation (execution denied when contested), nonce replay, and scope escalation.

What this is not: a production authorization service, a published confirmatory benchmark, or a claim that OI is safer than voting. See `experiments/OI-003/BENCHMARK-GUARDRAILS.md`.
