import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from hrs_v021 import run_validation_suite


def canonical_bytes(result):
    return (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()


if __name__ == "__main__":
    result = run_validation_suite(runs=1000, seed=42)
    payload = canonical_bytes(result)
    print(payload.decode(), end="")
    print("sha256=" + hashlib.sha256(payload).hexdigest(), file=sys.stderr)
