from __future__ import annotations

from skillfreq.configuration import rule_terms, scoring_config


def keyword_count(text, keywords):
    # Compatibility: alignment retains its historical substring boosts.
    return sum(1 for word in keywords if word in text.lower())


def weighted_alignment_score(skill_counts, profile, weights, penalties=None,
                             description='', flags=None, evidence=None):
    """Preserved weighted alignment with configurable adjustments and a point ledger."""
    settings = scoring_config()
    rules = settings['alignment']
    points = rules['points']
    flags, penalties = flags or {}, penalties or {}
    ledger = evidence if evidence is not None else []
    score, matched, total, missing = 0.0, 0, 0, []

    def add(name, amount, **detail):
        nonlocal score
        score += amount
        ledger.append(dict(rule_id='alignment:'+name, kind='alignment', contribution=amount, **detail))

    for skill, count in skill_counts.items():
        if count <= 0:
            continue
        total += 1
        if skill in penalties:
            add('concept_penalty', count*penalties[skill], concept=skill, count=count)
            continue
        strength = profile.get(skill, 0)
        contribution = strength*weights.get(skill, 1)
        contribution = min(contribution, settings['alignment_caps'].get(skill, contribution))
        add('profile_overlap', contribution, concept=skill, profile_strength=strength)
        if skill in rules['unmatched_concepts']:
            continue
        if strength > 0:
            matched += 1
        else:
            missing.append(skill)

    desc = description.lower()
    scoped = rules.get('section_scopes', {})
    sections = flags.get('sections', {})
    def hits(group):
        source = sections.get(scoped.get(group), desc) if scoped.get(group) else desc
        return keyword_count(source, rule_terms('alignment.'+group))
    pipeline = hits('pipeline_keywords')
    if pipeline >= rules['pipeline_strong_hits']:
        name = 'pipeline_sql' if skill_counts.get('sql', 0) else 'pipeline_strong'
        add(name, points[name], hits=pipeline)
    elif pipeline >= rules['pipeline_light_hits']:
        add('pipeline_light', points['pipeline_light'], hits=pipeline)
    if hits('integration_keywords') >= rules['integration_hits']:
        add('integration', points['integration'])
    for name in ('early_career','no_experience','analytics','ai_terms'):
        if hits(name):
            add(name, points[name])
    if skill_counts.get('etl', 0) >= rules['etl_deep_hits'] and skill_counts.get('sql', 0):
        add('etl_deep', points['etl_deep'])
    aws = skill_counts.get('aws', 0)
    if aws >= rules['aws_heavy_hits']:
        add('aws_heavy', points['aws_heavy'])
    elif aws >= rules['aws_medium_hits']:
        add('aws_medium', points['aws_medium'])
    modern = hits('modern_heavy')
    if modern >= rules['modern_heavy_hits']:
        add('modern_heavy', points['modern_heavy'])
    elif modern:
        add('modern_light', points['modern_light'])
    if hits('ml_keywords') >= rules['ml_hits']:
        add('ml', points['ml'])
    ai = skill_counts.get('ai_ml', 0)
    if ai >= rules['ai_heavy_hits']:
        # Both historical dampeners are retained, now separately visible.
        add('ai_primary', points['ai_primary'])
        add('ai_heavy', points['ai_heavy'])
    elif ai:
        add('ai_light', points['ai_light'])
    if skill_counts.get('etl', 0) >= rules['etl_overlap_hits'] and skill_counts.get('sql', 0):
        add('etl_overlap', points['etl_overlap'])
    for name, flag in [('mandatory_missing','mandatory_missing_skills'),
                       ('modern_required','modern_required_missing_skills'),
                       ('modern_preferred','modern_preferred_missing_skills')]:
        if flags.get(flag):
            add(name, points[name]*len(flags[flag]), skills=flags[flag])
    if flags.get('is_lead_like'):
        add('lead', points['lead'])
    years = flags.get('years_required')
    max_years = years[1] if isinstance(years, (list, tuple)) else years
    if max_years is not None:
        for minimum, amount in rules['years_penalties']:
            if max_years >= minimum:
                add('years', amount, years=max_years)
                break
    if total:
        scaled = score / total * rules['scale']
        ledger.append(dict(rule_id='alignment:normalization', kind='alignment',
                           contribution=scaled-score, denominator=total, scale=rules['scale']))
        score = scaled
    return score, matched, total, missing
