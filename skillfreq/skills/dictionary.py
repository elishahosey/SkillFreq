from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import yaml


SkillDict = Dict[str, List[str]]
WeightDict = Dict[str, float]

def load_skill_dictionary(path: Path, taxonomy=None, requirements=None) -> SkillDict:
    """Load broad concepts and expand explicit atomic/phrase relations.

    The returned mapping is the existing matcher's API. Atomic extraction still
    runs independently: a PostgreSQL hit can imply sql fit, never a SQL fact.
    Legacy list-form dictionaries remain supported for external callers.
    """
    from skillfreq.configuration import CONFIG_DIR, read_config
    from .job_market import load_market_taxonomy
    data = read_config(path)
    taxonomy = taxonomy if taxonomy is not None else load_market_taxonomy(CONFIG_DIR/'market_skills.yml')
    out = {}
    for concept, meta in data.items():
        if isinstance(meta, list):
            terms = meta
        elif isinstance(meta, dict):
            terms = list(meta.get('terms', []))
            for atomic in meta.get('atomic_skills', []):
                terms.extend(taxonomy[atomic])
            for owner, term in meta.get('term_refs', []):
                if term not in data[owner]['terms']:
                    raise ValueError(f'Unknown concept term {owner}:{term}')
                terms.append(term)
        else:
            raise ValueError(f'Invalid capability {concept}')
        if not all(isinstance(t, str) for t in terms):
            raise ValueError(f'Non-string term in {concept}')
        out[concept.lower()] = list(dict.fromkeys(t.lower() for t in terms))
    # Compatibility scoring channel; evidence is separately exposed as seniority.
    requirements = requirements if requirements is not None else read_config(CONFIG_DIR/'requirements.yml')
    out['seniority'] = requirements['seniority_terms']
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