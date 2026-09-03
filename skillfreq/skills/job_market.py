from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import yaml


Taxonomy = dict[str, list[str]]


@dataclass(frozen=True)
class SkillMatch:
    canonical_skill: str
    matched_terms: tuple[str, ...]
    mention_count: int


def load_market_taxonomy(path: Path) -> Taxonomy:
    """Load canonical skill labels and aliases, rejecting ambiguous aliases."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Market skill taxonomy must be a mapping of skill to aliases")

    taxonomy: Taxonomy = {}
    alias_owner: dict[str, str] = {}
    for raw_skill, raw_aliases in data.items():
        if not isinstance(raw_skill, str) or not raw_skill.strip():
            raise ValueError("Every canonical skill must be a non-empty string")
        if not isinstance(raw_aliases, list) or not raw_aliases:
            raise ValueError(f"Skill '{raw_skill}' must have a non-empty alias list")

        skill = raw_skill.strip()
        aliases: list[str] = []
        for raw_alias in raw_aliases:
            if not isinstance(raw_alias, str) or not raw_alias.strip():
                raise ValueError(f"Skill '{skill}' has an invalid alias: {raw_alias!r}")
            alias = " ".join(raw_alias.casefold().split())
            owner = alias_owner.get(alias)
            if owner and owner != skill:
                raise ValueError(
                    f"Alias '{alias}' is assigned to both '{owner}' and '{skill}'"
                )
            alias_owner[alias] = skill
            if alias not in aliases:
                aliases.append(alias)
        taxonomy[skill] = aliases
    return taxonomy


def taxonomy_version(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def extract_market_skills(
    text: str | None, taxonomy: Mapping[str, Sequence[str]]
) -> list[SkillMatch]:
    """Return one normalized result per skill, with aliases retained as evidence."""
    normalized_text = " ".join((text or "").casefold().split())
    if not normalized_text:
        return []

    matches: list[SkillMatch] = []
    for skill, aliases in taxonomy.items():
        term_counts: dict[str, int] = {}
        # Longest aliases first is useful when inspecting evidence; counts remain
        # mention counts rather than mutually exclusive phrase classifications.
        for alias in sorted(aliases, key=len, reverse=True):
            pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
            count = len(re.findall(pattern, normalized_text))
            if count:
                term_counts[alias] = count
        if term_counts:
            matches.append(
                SkillMatch(
                    canonical_skill=skill,
                    matched_terms=tuple(term_counts),
                    mention_count=sum(term_counts.values()),
                )
            )
    return matches


def make_job_key(source_site: str | None, source_job_id: str | None, job_url: str | None) -> str:
    identity = source_job_id or job_url
    if not identity:
        raise ValueError("A clean job must have source_job_id or job_url")
    raw_key = f"{source_site or ''}\x1f{identity}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def extract_job_rows(
    jobs: Iterable[Mapping[str, object]], taxonomy: Mapping[str, Sequence[str]]
) -> list[tuple[str, str | None, str | None, str | None, str, list[str], int]]:
    rows = []
    for job in jobs:
        source_site = _optional_string(job.get("source_site"))
        source_job_id = _optional_string(job.get("source_job_id"))
        job_url = _optional_string(job.get("job_url"))
        job_key = make_job_key(source_site, source_job_id, job_url)
        for match in extract_market_skills(_optional_string(job.get("description")), taxonomy):
            rows.append(
                (
                    job_key,
                    source_site,
                    source_job_id,
                    job_url,
                    match.canonical_skill,
                    list(match.matched_terms),
                    match.mention_count,
                )
            )
    return rows


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None

