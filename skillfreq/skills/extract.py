from datetime import datetime
from string import punctuation
import re
from typing import Any, Dict, List


BAD_PHRASES = {
    "key responsibilities",
    "actionable insights",
    "business stakeholders",
    "non-exempt position summary",
    "chief information officer flsa status",
}

BAD_SINGLE_WORDS = {
    "engineers",
    "collaboration",
    "systems",
    "processing",
    "reporting",
    "ingesting",
    "sc",
}

from skillfreq.configuration import CONFIG_DIR, read_config
from skillfreq.skills.text import term_counts


def _nlp():
    # Free-form diagnostics only; deterministic grading needs no spaCy model.
    global nlp
    if nlp is None:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    return nlp


nlp = None


def get_hotwords(text):
    result = []
    pos_tag = ["PROPN", "ADJ", "NOUN"]
    nlp = _nlp()
    doc = nlp(text.lower())

    for token in doc:
        if token.text in nlp.Defaults.stop_words or token.text in punctuation:
            continue

        if token.pos_ in pos_tag:
            result.append(token.text)

    return result


def get_nounChunks(text):
    results = []
    nlp = _nlp()
    doc = nlp(text.lower())

    for chunk in doc.noun_chunks:
        pos_tag = ["PROPN", "ADJ", "NOUN"]

        if chunk.text in nlp.Defaults.stop_words or chunk.text in punctuation:
            continue

        if chunk.text in BAD_PHRASES:
            continue

        if chunk.text in BAD_SINGLE_WORDS:
            continue

        # check chunk in allowed list
        if all(token.pos_ in pos_tag for token in chunk):
            results.append(chunk.text)

    return results


def _extract_description_text(jd: Any) -> str:
    if isinstance(jd, dict):
        return str(jd.get("description", "") or "")

    if isinstance(jd, tuple):
        if len(jd) < 2:
            return ""

        payload = jd[1]
        if isinstance(payload, dict):
            return str(payload.get("description", "") or "")

        return str(payload or "")

    return str(jd or "")



def extract_jd_skills(jdParsedObject):
    extracted_skills = []

    for jd in jdParsedObject:
        text = _extract_description_text(jd)

        if not text:
            extracted_skills.append([])
            continue

        output = list(set(get_nounChunks(text)))
        extracted_skills.append(output)

    return extracted_skills


def extract_sections(description: str, config=None) -> Dict[str, str]:
    config = config or read_config(CONFIG_DIR/"requirements.yml")
    text = description.lower()

    matches = []

    for section_name, patterns in config["section_patterns"].items():
        for pattern in patterns:
            for m in re.finditer(pattern, text):
                # An inline modality ("Power BI preferred") is not a heading.
                if m.group() == 'preferred':
                    prefix = text[text.rfind('\n', 0, m.start()) + 1:m.start()].strip(' -*#\t')
                    if prefix and not text[m.end():].lstrip().startswith(':'):
                        continue
                matches.append((m.start(), m.end(), section_name))

    if not matches:
        return {"full_text": text}

    # Longest heading wins at overlapping offsets ("preferred qualifications"
    # also matches "preferred"). Keep every repeated section, not just one.
    matches.sort(key=lambda x: (x[0], -x[1]))
    non_overlapping = []
    for match in matches:
        if not non_overlapping or match[0] >= non_overlapping[-1][1]:
            non_overlapping.append(match)
    matches = non_overlapping

    sections: Dict[str, str] = {}

    for i, (start, end, section_name) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        section_text = text[end:next_start].strip()

        sections[section_name] = (sections.get(section_name, '') + '\n' + section_text).strip()

    sections["full_text"] = text

    return sections


def extract_requirement_flags(
    description: str,
    skills: Dict[str, List[str]],
    profile: Dict[str, float],
    config=None,
    atomic_terms=(),
    atomic_profile=None,
    known_atomic_threshold=0.5,
) -> Dict[str, object]:
    config = config or read_config(CONFIG_DIR/"requirements.yml")
    sections = extract_sections(description, config)
    required_text = sections.get("required", "")
    preferred_text = sections.get("preferred", "")
    full_text = sections.get("full_text", description.lower())

    flags = {
        "mandatory_missing_skills": [],
        "preferred_missing_skills": [],
        "modern_required_missing_skills": [],
        "modern_preferred_missing_skills": [],
        "years_required": None,
        "is_lead_like": False,
        "has_hard_requirement_blockers": False,
        "has_modern_stack_blockers": False,
        "reason_codes": [],
        "requirement_groups": [],
        "requirement_evidence": [],
        "requirement_interpretation": [],
    }

    # years parsing
    # Normalize escaped plus signs from scraped/CSV text, e.g. "4\\+ years" -> "4+ years"
    years_text = required_text
    if not years_text:
        # Use configured experience sentences, excluding any explicitly preferred section.
        candidates = full_text.replace(preferred_text, '') if preferred_text else full_text
        years_text = ' '.join(re.findall(config['years_fallback_pattern'], candidates.replace('\\+', '+')))
    normalized_full_text = years_text.replace("\\+", "+")

    years_range_match = re.search(
        r"(\d+)\s*(?:-|to)\s*(\d+)\s*\+?\s+years",
        normalized_full_text,
    )

    if years_range_match:
        flags["years_required"] = (
            int(years_range_match.group(1)),
            int(years_range_match.group(2)),
        )
    else:
        single_years = re.findall(
            r"(\d+)\s*\+?\s+years",
            normalized_full_text,
        )

        if single_years:
            flags["years_required"] = max(int(y) for y in single_years)

    explicit_years = [int(m.group(1)) for pattern in config['explicit_years_patterns']
                      for m in re.finditer(pattern, full_text)]
    if explicit_years:
        existing = flags['years_required']
        previous = min(existing) if isinstance(existing, tuple) else (existing or 0)
        flags['years_required'] = max([previous] + explicit_years)
    flags["seniority_signals"] = list(term_counts(full_text, config["lead_terms"]))
    flags["is_lead_like"] = bool(flags["seniority_signals"])
    flags["requirement_ambiguity"] = any(re.search(p, full_text) for p in config["ambiguity_patterns"])
    flags['requirement_ambiguity'] |= any(
        re.search(r'(?<!\w)' + re.escape(term) + config['skill_alternative_suffix'], full_text)
        for term in atomic_terms)
    flags["sections"] = sections

    # Resolve sentence semantics once. Both atomic gaps and legacy capability
    # flags consume this interpretation; alternatives never leak into fallback.
    taxonomy = config.get('_taxonomy')
    if taxonomy:
        known = atomic_profile or {}
        semantic_text = {'required': [], 'preferred': []}
        for section_name, source_section, source in _requirement_sources(sections, config):
            mentions = _atomic_mentions(source, taxonomy)
            skills_found = list(dict.fromkeys(skill for _, _, skill in mentions))
            if not skills_found:
                semantic_text[section_name].append(source)
                flags['requirement_interpretation'].append(dict(
                    section=section_name, source=source, mode='legacy_mention_fallback'))
                continue
            group_type, grammar = _requirement_grammar(source, mentions)
            satisfied_skills = [s for s in skills_found if known.get(s, 0) >= known_atomic_threshold]
            equivalent_evidence = []
            if group_type == 'equivalent':
                for skill in skills_found:
                    accepted = config.get('equivalences', {}).get(skill, {})
                    for name in accepted.get('atomic_skills', []):
                        if known.get(name, 0) >= known_atomic_threshold:
                            equivalent_evidence.append(dict(kind='atomic_skill', name=name, for_skill=skill))
                    for name in accepted.get('capability_concepts', []):
                        if profile.get(name, 0) >= known_atomic_threshold:
                            equivalent_evidence.append(dict(kind='capability_concept', name=name, for_skill=skill))
            satisfied = (len(satisfied_skills) == len(skills_found) if group_type == 'all_of'
                         else bool(satisfied_skills or equivalent_evidence))
            if group_type == 'ambiguous':
                satisfied = None
                flags['requirement_ambiguity'] = True
            group_id = f'{section_name}_group_{len(flags["requirement_groups"]) + 1}'
            group = dict(group_id=group_id, section=section_name, source_section=source_section,
                         type=group_type, grammar=grammar, skills=skills_found, source=source,
                         source_span=source, candidate_satisfied_skills=satisfied_skills,
                         equivalent_evidence=equivalent_evidence, satisfied=satisfied)
            flags['requirement_groups'].append(group)
            flags['requirement_interpretation'].append(dict(
                section=section_name, source=source, mode='structured', group_id=group_id))
            for skill in skills_found:
                flags['requirement_evidence'].append(dict(
                    skill=skill, section=section_name, source_section=source_section, source=source,
                    requirement_type=group_type, group_id=group_id,
                    candidate_satisfies=skill in satisfied_skills, group_satisfied=satisfied))
            if group_type == 'all_of':
                # Known atomic evidence also satisfies its legacy alias mention.
                # Do not suppress independent non-atomic concepts in this sentence.
                chars = list(source)
                for start, end, skill in mentions:
                    if skill in satisfied_skills:
                        chars[start:end] = ' ' * (end-start)
                semantic_text[section_name].append(''.join(chars))
        required_text = '\n'.join(semantic_text['required'])
        preferred_text = '\n'.join(semantic_text['preferred'])
    flags['semantic_requirement_text'] = dict(required=required_text, preferred=preferred_text)

    # hard blockers only from required section
    if required_text:
        for skill, terms in skills.items():
            if profile.get(skill, 0.0) > 0:
                continue

            for term in terms:
                pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"

                if re.search(pattern, required_text):
                    if skill in config["core_blocker_skills"]:
                        flags["mandatory_missing_skills"].append(skill)
                    elif skill in config["modern_stack_skills"]:
                        flags["modern_required_missing_skills"].append(skill)

                    break

    # softer signals from preferred section
    if preferred_text:
        for skill, terms in skills.items():
            if profile.get(skill, 0.0) > 0:
                continue

            for term in terms:
                pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"

                if re.search(pattern, preferred_text):
                    if skill in config["modern_stack_skills"]:
                        flags["modern_preferred_missing_skills"].append(skill)
                    else:
                        flags["preferred_missing_skills"].append(skill)

                    break

    flags["mandatory_missing_skills"] = sorted(set(flags["mandatory_missing_skills"]))
    flags["preferred_missing_skills"] = sorted(set(flags["preferred_missing_skills"]))
    flags["modern_required_missing_skills"] = sorted(set(flags["modern_required_missing_skills"]))
    flags["modern_preferred_missing_skills"] = sorted(set(flags["modern_preferred_missing_skills"]))

    flags["has_hard_requirement_blockers"] = len(flags["mandatory_missing_skills"]) > 0

    # Modern stack is a blocker only if multiple required missing modern skills show up
    flags["has_modern_stack_blockers"] = len(flags["modern_required_missing_skills"]) >= config["modern_blocker_count"]

    # Reason codes
    if flags["mandatory_missing_skills"]:
        flags["reason_codes"].append("core_required_missing")

    if flags["modern_required_missing_skills"]:
        flags["reason_codes"].append("modern_required_missing")

    if flags["modern_preferred_missing_skills"]:
        flags["reason_codes"].append("modern_preferred_missing")

    if any(g['section'] == 'required' and g['type'] in ('any_of', 'equivalent')
           and g['satisfied'] is False for g in flags['requirement_groups']):
        flags['reason_codes'].append('unsatisfied_required_group')
    if any(g['type'] == 'ambiguous' for g in flags['requirement_groups']):
        flags['reason_codes'].append('ambiguous_requirement_grammar')

    if flags["is_lead_like"]:
        flags["reason_codes"].append("lead_like")

    if flags["years_required"]:
        flags["reason_codes"].append("years_present")

    return flags


def _requirement_sentences(text: str) -> list[str]:
    """Split bullets/short prose while retaining deterministic source text."""
    return [part.strip(' -*\t') for part in re.split(r'(?<=[.!?])\s+|\n+', text) if part.strip(' -*\t')]


def _requirement_sources(sections, config):
    """Retain section context, with explicit sentence modality taking precedence."""
    covered = []
    for section in ('required', 'preferred'):
        for source in _requirement_sentences(sections.get(section, '')):
            modality = 'preferred' if re.search(r'\bpreferred\b', source) else section
            covered.append(source)
            yield modality, section, source
    # Headless explicit requirements are common in pasted snippets. Other prose
    # remains unclassified instead of turning every technology mention mandatory.
    if any(sections.get(section) for section in ('required', 'preferred', 'responsibilities')):
        return
    for source in _requirement_sentences(sections['full_text']):
        if any(source in part or part in source for part in covered):
            continue
        if re.search(r'\bpreferred\b', source):
            yield 'preferred', 'unknown', source
        elif any(re.search(pattern, source) for pattern in config.get('unscoped_requirement_patterns', [])):
            yield 'required', 'unknown', source


def _atomic_mentions(source, taxonomy):
    """Longest controlled alias owns its span (SQL Server is not an SQL option).

    Market extraction remains unchanged: this disambiguation is for requirement
    operands only. Preserve offsets into the original sentence.
    """
    mentions = []
    for skill, aliases in taxonomy.items():
        for alias in aliases:
            if alias not in source:
                continue
            for match in re.finditer(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', source):
                mentions.append((match.start(), match.end(), skill))
    return sorted(set(m for m in mentions if not any(
        n[0] <= m[0] and n[1] >= m[1] and n[1]-n[0] > m[1]-m[0] for n in mentions)))


def _requirement_grammar(source, mentions):
    equivalent = bool(re.search(r'\bor equivalent(?: experience)?\b', source))
    alternative = bool(re.search(r'\b(?:one of|one or more|and/or)\b|\bor\b', source))
    examples = bool(re.search(r'\b(?:such as|including|for example)\b|\be\.g\.', source))
    between = source[mentions[0][0]:mentions[-1][1]]
    # Only conjunctions between atomic operands count; "design and develop"
    # before the list is not mixed Boolean grammar. and/or is one connective.
    mixed = (alternative or equivalent) and bool(re.search(r'\band\b', between.replace('and/or', 'or')))
    if mixed:
        return 'ambiguous', 'mixed_conjunction_alternative'
    if equivalent:
        return 'equivalent', 'or_equivalent'
    if examples:
        return 'any_of', 'examples'
    if alternative:
        return 'any_of', 'alternatives'
    return 'all_of', 'conjunction_or_enumeration'
