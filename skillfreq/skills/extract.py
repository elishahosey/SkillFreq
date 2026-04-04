from datetime import datetime
from string import punctuation
import re
from typing import Dict, List

import spacy

BAD_PHRASES = {
    "key responsibilities",
    "actionable insights",
    "business stakeholders",
    "non-exempt position summary",
    "chief information officer flsa status"
}

BAD_SINGLE_WORDS = {
    "engineers",
    "collaboration",
    "systems",
    "processing",
    "reporting",
    "ingesting",
    "sc"
}

SECTION_PATTERNS = {
    "required": [
        r"required qualifications",
        r"minimum qualifications",
        r"must have",
        r"mandatory skills?",
        r"requirements",
    ],
    "preferred": [
        r"preferred qualifications",
        r"nice to have",
        r"preferred",
        r"pluses",
    ],
    "responsibilities": [
        r"responsibilities",
        r"key responsibilities",
        r"what you'll do",
        r"job description",
    ],
}



CORE_BLOCKER_SKILLS = {"sql", "etl", "python"}

nlp = spacy.load('en_core_web_sm')

def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result

def get_nounChunks(text):
    
    results = []
    doc = nlp(text.lower()) 
    for chunk in doc.noun_chunks:
        pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
        
        if(chunk.text in nlp.Defaults.stop_words or chunk.text in punctuation):
         continue
        
        if chunk.text in BAD_PHRASES:
         continue

        if chunk.text in BAD_SINGLE_WORDS:
         continue
        
        #check chunk in allowed list
        if all(token.pos_ in pos_tag for token in chunk):
            results.append(chunk.text)
    
    return results
        
    
def extract_jd_skills(jdParsedObject):
    extracted_skills = []
    for jd in jdParsedObject:
        text = jd[1]['description'] if 'description' in jd[1] else jd[1]
        output = list(set(get_nounChunks(text)))

        extracted_skills.append(output)
        
    
    return extracted_skills

def extract_sections(description: str) -> Dict[str, str]:
    text = description.lower()

    matches = []
    for section_name, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            for m in re.finditer(pattern, text):
                matches.append((m.start(), m.end(), section_name))

    if not matches:
        return {"full_text": text}

    matches.sort(key=lambda x: x[0])

    sections: Dict[str, str] = {}
    for i, (start, end, section_name) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        section_text = text[end:next_start].strip()

        # keep the longest occurrence if duplicate headings appear
        if section_name not in sections or len(section_text) > len(sections[section_name]):
            sections[section_name] = section_text

    sections["full_text"] = text
    return sections

def extract_requirement_flags(
    description: str,
    skills: Dict[str, List[str]],
    profile: Dict[str, float],
) -> Dict[str, object]:
    sections = extract_sections(description)
    required_text = sections.get("required", "")
    preferred_text = sections.get("preferred", "")
    full_text = sections.get("full_text", description.lower())

    flags = {
        "mandatory_missing_skills": [],
        "preferred_missing_skills": [],
        "years_required": None,
        "is_lead_like": False,
        "has_hard_requirement_blockers": False,
    }

    years_match = re.search(r"(\d+)\s*-\s*(\d+)\s+years", full_text)
    if years_match:
        flags["years_required"] = (int(years_match.group(1)), int(years_match.group(2)))

    lead_terms = [
        "technical lead",
        "subject matter expert",
        "staff",
        "principal",
        "architect",
        "lead engineer",
    ]
    flags["is_lead_like"] = any(term in full_text for term in lead_terms)

    # hard blockers only from required section
    if required_text:
        for skill, terms in skills.items():
            if profile.get(skill, 0.0) > 0:
                continue
            if skill not in CORE_BLOCKER_SKILLS:
                continue

            for term in terms:
                pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
                if re.search(pattern, required_text):
                    flags["mandatory_missing_skills"].append(skill)
                    break

    # softer signals from preferred section
    if preferred_text:
        for skill, terms in skills.items():
            if profile.get(skill, 0.0) > 0:
                continue

            for term in terms:
                pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
                if re.search(pattern, preferred_text):
                    flags["preferred_missing_skills"].append(skill)
                    break

    flags["mandatory_missing_skills"] = sorted(set(flags["mandatory_missing_skills"]))
    flags["preferred_missing_skills"] = sorted(set(flags["preferred_missing_skills"]))
    flags["has_hard_requirement_blockers"] = (
     len(flags["mandatory_missing_skills"]) > 0
    )

    return flags