from __future__ import annotations

import re
from typing import Dict, List


def _normalize_text(text: str) -> str:
    #jd = text['description'].lower()
    jd = text.lower()
    text = re.sub(r"\s+", " ", jd).strip() #trim and collapse whitespace
    return text


def match_skills(text: str, skills: Dict[str, List[str]]) -> Dict[str, int]:
    t = _normalize_text(text)
    counts: Dict[str, int] = {}

    for skill, terms in skills.items():
        c = 0
        for term in terms:
            # word-boundary-ish matching to avoid crazy false positives
            # e.g. "sql" should match " sql " or "sql," etc.
            pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
            c += len(re.findall(pattern, t))
        counts[skill] = c

    return counts