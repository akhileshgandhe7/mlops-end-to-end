"""Load params.yaml so every stage reads the same settings."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_params(path: Path = ROOT / "params.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)
