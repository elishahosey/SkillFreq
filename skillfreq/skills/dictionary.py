from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import yaml


SkillDict = Dict[str, List[str]]
WeightDict = Dict[str, float]

# def load_skill_dictionary(path: Path) -> SkillDict:
#     data = yaml.safe_load(path.read_text(encoding="utf-8"))
#     if not isinstance(data, dict):
#         raise ValueError("skills.yml must be a mapping of skill -> [terms]")
#     # normalize terms to lowercase
#     out: SkillDict = {}
#     for skill, terms in data.items():
#         if not isinstance(terms, list):
#             raise ValueError(f"Skill '{skill}' must map to a list of terms")
#         out[str(skill).lower()] = [str(t).lower() for t in terms]
#     return out



def load_skill_dictionary(path: Path) -> SkillDict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("skills.yml must be a mapping of skill -> [terms]")

    out: SkillDict = {}

    for skill, terms in data.items():
        if not isinstance(skill, str):
            raise ValueError(f"Skill key must be a string, got {type(skill).__name__}")

        if not isinstance(terms, list):
            raise ValueError(f"Skill '{skill}' must map to a list of terms")

        normalized_terms = []
        for t in terms:
            if not isinstance(t, str):
                raise ValueError(f"Skill '{skill}' contains non-string term: {t!r}")
            normalized_terms.append(t.lower())

        out[skill.lower()] = normalized_terms

    return out

def load_weights(path: Path) -> Tuple[WeightDict, WeightDict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("weights.yml must be a mapping")

    weights = data.get("weights", {})
    penalties = data.get("penalties", {})

    if not isinstance(weights, dict):
        raise ValueError("'weights' must be a mapping of skill -> number")

    if not isinstance(penalties, dict):
        raise ValueError("'penalties' must be a mapping of skill -> number")

    norm_weights: WeightDict = {}
    norm_penalties: WeightDict = {}

    # normalize weights
    for k, v in weights.items():
        if not isinstance(v, (int, float)):
            raise ValueError(f"Weight for '{k}' must be numeric")
        norm_weights[str(k).lower()] = float(v)

    # normalize penalties
    for k, v in penalties.items():
        if not isinstance(v, (int, float)):
            raise ValueError(f"Penalty for '{k}' must be numeric")
        norm_penalties[str(k).lower()] = float(v)

    return norm_weights, norm_penalties