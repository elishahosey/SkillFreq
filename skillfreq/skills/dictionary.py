from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import yaml


SkillDict = Dict[str, List[str]]


def load_skill_dictionary(path: Path) -> SkillDict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("skills.yml must be a mapping of skill -> [terms]")
    # normalize terms to lowercase
    out: SkillDict = {}
    for skill, terms in data.items():
        if not isinstance(terms, list):
            raise ValueError(f"Skill '{skill}' must map to a list of terms")
        out[str(skill).lower()] = [str(t).lower() for t in terms]
    return out