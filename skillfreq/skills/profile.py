from __future__ import annotations
from pathlib import Path
from typing import Dict
import yaml

def load_profile(path: Path) -> Dict[str, int]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "skills" not in data or not isinstance(data["skills"], dict):
        raise ValueError("profile.yml must contain a top-level 'skills:' mapping")

    # normalize keys to lowercase, values to int (0/1)
    out: Dict[str, int] = {}
    for k, v in data["skills"].items():
        out[str(k).lower()] = int(v)
    return out