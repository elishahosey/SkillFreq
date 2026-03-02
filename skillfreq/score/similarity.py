from __future__ import annotations

from typing import Dict, Tuple




def profile_alignment_score(skill_counts: Dict[str, int], profile: Dict[str, int]) -> Tuple[float, int, int, List[str]]:
    required = [s for s, c in skill_counts.items() if c > 0]
    if not required:
        return 0.0, 0, 0, []

    matched = sum(1 for s in required if profile.get(s, 0) > 0)
    total = len(required)
    missing = [s for s in required if profile.get(s, 0) <= 0]
    
    #knock down the score if seniority is in the list
    if skill_counts.get('seniority', 0) > 0:
        matched -= 1
    

    return matched / total, matched, total, missing

def overlap_score(skill_counts: Dict[str, int]) -> Tuple[float, int, int]:
    """
    Treat every skill in the dictionary as "required_total".
    matched = how many skills had count > 0
    score = matched / required_total
    """
    required_total = len(skill_counts)
    matched = sum(1 for _, c in skill_counts.items() if c > 0)
    score = (matched / required_total) if required_total else 0.0
    return score, matched, required_total