from __future__ import annotations

import re
from typing import Dict, List
from .text import normalize_text, term_counts


def _normalize_text(text: str) -> str:
    #jd = text['description'].lower()
    jd = text.lower()
    text = re.sub(r"\s+", " ", jd).strip() #trim and collapse whitespace
    return text


def match_skills(text: str, skills: Dict[str, List[str]]) -> Dict[str, int]:
    return {skill: sum(term_counts(text, terms).values()) for skill, terms in skills.items()}
