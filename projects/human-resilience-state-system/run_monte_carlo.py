import json
import pathlib
import sys

SRC = pathlib.Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC))

from hrs_v021 import run_monte_carlo


if __name__ == "__main__":
    metrics = run_monte_carlo(runs=1000, seed=42, noise_sd=0.006)
    print(json.dumps(metrics, indent=2, sort_keys=True))
