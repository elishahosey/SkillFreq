"""Boundary matching shared by controlled evidence layers."""
import math
import re
from functools import lru_cache


def clean_text(value) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ''
    return str(value).strip()


def normalize_text(value) -> str:
    return _normalized(clean_text(value))


@lru_cache(maxsize=128)
def _normalized(text):
    return ' '.join(text.casefold().split())


@lru_cache(maxsize=4096)
def _term_pattern(term):
    return re.compile(r'(?<!\w)' + re.escape(term) + r'(?!\w)')


def term_counts(text, terms):
    normalized = normalize_text(text)
    counts = {}
    for term in dict.fromkeys(normalize_text(t) for t in terms):
        if not term or term not in normalized:
            continue
        count = len(_term_pattern(term).findall(normalized))
        if count:
            counts[term] = count
    return counts
