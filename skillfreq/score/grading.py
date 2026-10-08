"""Deterministic pre-AI grading composed from the existing extraction/scoring stages."""
from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path

from skillfreq.configuration import CONFIG_DIR, configuration_version, evaluation_config, load_roles, read_config
from skillfreq.skills.dictionary import load_skill_dictionary, load_weights
from skillfreq.skills.extract import extract_requirement_flags, extract_sections
from skillfreq.skills.job_market import extract_market_skills, load_market_taxonomy, taxonomy_version
from skillfreq.skills.match import match_skills
from skillfreq.skills.profile import load_profile
from skillfreq.skills.text import clean_text, term_counts
from .decision_layer import decide_apply_bucket, derive_fit_quality
from .lane_classifier import score_lanes
from .similarity import weighted_alignment_score
from .thresholds import classify
from .policy import evaluate_rules
from .policy import capture_evaluations
from .trace import build_observability


@dataclass
class GradingContext:
    skills: dict
    profile: dict
    profile_config: dict
    weights: dict
    penalties: dict
    settings: dict
    taxonomy: dict
    roles: dict
    requirements: dict
    grading_version: str
    taxonomy_version: str
    snapshot: dict

    @classmethod
    def load(cls, skills_path=CONFIG_DIR/'skills.yml', profile_path=CONFIG_DIR/'profile.yml',
             weight_path=CONFIG_DIR/'weights.yml', roles_path=CONFIG_DIR/'roles.yml',
             taxonomy_path=CONFIG_DIR/'market_skills.yml', requirements_path=CONFIG_DIR/'requirements.yml'):
        paths = dict(skills=skills_path, profile=profile_path, weights=weight_path, roles=roles_path,
                     market_skills=taxonomy_path, requirements=requirements_path)
        snapshot = {key: read_config(path) for key, path in paths.items()}
        experience = snapshot['profile'].get('experience_years')
        if experience is not None and (not isinstance(experience, list) or len(experience) != 2 or
                any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in experience) or
                not 0 <= experience[0] <= experience[1] <= 50):
            raise ValueError('experience_years must be a plausible [minimum, maximum] range')
        clearance = snapshot['profile'].get('active_clearance')
        if clearance is not None and not isinstance(clearance, bool):
            raise ValueError('active_clearance must be true, false or null')
        # Version algorithms as well as authoring inputs; no deployment service needed.
        root = Path(__file__).resolve().parents[1]
        modules = ['configuration.py','score/grading.py','score/lane_classifier.py','score/decision_layer.py',
                   'score/similarity.py','score/policy.py','score/thresholds.py','skills/extract.py','skills/match.py',
                   'skills/text.py','skills/job_market.py','skills/dictionary.py','skills/profile.py']
        modules.append('score/trace.py')
        snapshot['market_taxonomy_version'] = taxonomy_version(Path(taxonomy_path))
        snapshot['implementation'] = {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in modules}
        version = configuration_version(snapshot)
        taxonomy = load_market_taxonomy(Path(taxonomy_path))
        requirements = snapshot['requirements']
        skills = load_skill_dictionary(Path(skills_path), taxonomy, requirements)
        profile = load_profile(Path(profile_path))
        weights, penalties = load_weights(Path(weight_path))
        roles = load_roles(Path(roles_path), concepts=snapshot['skills'], taxonomy=taxonomy, requirements=requirements)
        from skillfreq.configuration import validate_grading_settings
        validate_grading_settings(snapshot['weights'], roles)
        equivalences = requirements.get('equivalences', {})
        if not isinstance(equivalences, dict):
            raise ValueError('Requirement equivalences must be a mapping')
        for name, accepted in equivalences.items():
            if name not in taxonomy or not isinstance(accepted, dict) or set(accepted) - {'atomic_skills', 'capability_concepts'}:
                raise ValueError(f'Invalid requirement equivalence: {name}')
            for key, vocabulary in (('atomic_skills', taxonomy), ('capability_concepts', skills)):
                values = accepted.get(key, [])
                if not isinstance(values, list) or any(not isinstance(v, str) or v not in vocabulary for v in values):
                    raise ValueError(f'Invalid requirement equivalence {key}: {name}')
        for name, strength in snapshot['profile'].get('atomic_skills', {}).items():
            if name not in taxonomy or not isinstance(strength, (int, float)) or not 0 <= strength <= 1:
                raise ValueError(f'Invalid atomic profile skill: {name}')
        for name, path in snapshot['profile'].get('growth_paths', {}).items():
            if name not in taxonomy or not 0 <= path['priority'] <= 1 or not path['adjacent_concepts']:
                raise ValueError(f'Invalid growth path: {name}')
            if any(concept not in skills for concept in path['adjacent_concepts']):
                raise ValueError(f'Unknown growth adjacency: {name}')
        return cls(skills, profile, snapshot['profile'], weights, penalties, snapshot['weights'],
                   taxonomy, roles, requirements, version, taxonomy_version(Path(taxonomy_path)), snapshot)


@dataclass
class DeterministicGrade:
    job_id: str
    role_lane: str
    lane_scores: dict
    raw_lane_scores: dict
    fit_score: float
    learning_score: float | None
    learning_status: str
    blocking_reasons: list
    review_flags: list
    input_context: dict
    policy_flags: dict
    pre_ai_score: float
    confidence: float
    confidence_evidence: dict
    matched_atomic_skills: list
    matched_capability_concepts: dict
    missing_required_skills: dict
    missing_preferred_skills: dict
    growth_skills: list
    market_relevant_gaps: list
    matched_role_signals: list
    seniority_signals: dict
    exclusion_signals: list
    triggered_rules: list
    reason_codes: list
    apply_decision: str
    fit_quality: str
    ai_review_required: bool
    ai_review_reasons: list
    grading_version: str
    taxonomy_version: str
    market_context: dict
    alignment_score: float
    label: str
    matched: int
    required_total: int
    missing: list
    counts: dict
    lane_resolution: dict = field(default_factory=dict)
    category_hits: dict = field(default_factory=dict)
    observability: dict = field(default_factory=dict)
    requirement_flags: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


def atomic_profile(context):
    return context.profile_config.get('atomic_skills', {}).copy()


def extract_gaps(description, flags, context):
    missing = {}
    groups = flags.get('requirement_groups', [])
    for section in ('required', 'preferred'):
        text = flags['semantic_requirement_text'][section]
        section_groups = [g for g in groups if g['section'] == section]
        atomic = list(dict.fromkeys(skill for g in section_groups if g['type'] == 'all_of'
                                   for skill in g['skills'] if skill not in g['candidate_satisfied_skills']))
        if not groups:  # Compatibility for callers without a structured taxonomy.
            atomic = [m.canonical_skill for m in extract_market_skills(text, context.taxonomy)
                      if atomic_profile(context).get(m.canonical_skill, 0) < context.settings['fit']['known_atomic_threshold']]
        missing[section] = {
            'atomic_skills': atomic,
            'requirement_groups': section_groups,
            'unsatisfied_groups': [g for g in section_groups if g['type'] in ('any_of', 'equivalent') and g['satisfied'] is False],
            'ambiguous_groups': [g for g in section_groups if g['type'] == 'ambiguous'],
            'capability_concepts': [k for k, count in match_skills(text, context.skills).items()
                                    if k != 'seniority' and count and context.profile.get(k, 0) <= 0],
        }
    # A skill mentioned in both sections is required; do not penalize twice.
    for kind in ('atomic_skills', 'capability_concepts'):
        missing['preferred'][kind] = sorted(set(missing['preferred'][kind]) - set(missing['required'][kind]))
    return missing


def calculate_fit_score(counts, flags, gaps, lane, context, facts=None):
    settings = context.settings['fit']
    evidence = []
    relevant = {k: context.weights.get(k, 1) for k, n in counts.items()
                if n and k not in context.penalties and context.weights.get(k, 1) > 0}
    denominator = sum(relevant.values())
    coverage = settings['coverage_scale'] * sum(w * min(1, max(0, context.profile.get(k, 0))) for k, w in relevant.items()) / denominator if denominator else 0
    evidence.append(dict(rule_id='fit_profile_coverage', kind='fit', contribution=round(coverage, 3),
                         concepts={k: {'weight': w, 'profile_strength': context.profile.get(k, 0)} for k,w in relevant.items()}))
    score = coverage + settings['base_score']
    evidence.append(dict(rule_id='fit_base', kind='fit', contribution=settings['base_score']))
    for section in ('required', 'preferred'):
        for skill in gaps[section]['atomic_skills']:
            delta = -settings[section+'_atomic_penalty']
            score += delta
            evidence.append(dict(rule_id=f'fit_missing_{section}_atomic', kind='fit', skill=skill, contribution=delta))
    for group in gaps['required']['unsatisfied_groups']:
        delta = -settings['required_group_penalty']
        score += delta
        evidence.append(dict(rule_id='fit_unsatisfied_required_group', kind='fit',
                             group_id=group['group_id'], type=group['type'], skills=group['skills'],
                             source=group['source'], contribution=delta))
    for name, penalty in settings['flag_penalties'].items():
        if flags.get(name):
            score -= penalty
            evidence.append(dict(rule_id='fit_'+name, kind='fit', contribution=-penalty))
    facts = facts if facts is not None else {}
    facts['fit_score'] = score
    evidence.extend(evaluate_rules(facts, settings['rules'], 'fit'))
    score = facts['fit_score']
    capped = min(settings['lane_caps'][lane], max(0, score))
    evidence.append(dict(rule_id='fit_lane_cap_and_bounds', kind='fit', lane=lane, contribution=round(capped-score, 3)))
    return round(capped, 2), evidence


def calculate_learning_score(atomics, lane, context, prevalence):
    settings = context.settings['learning']
    if lane not in settings['eligible_lanes']:
        return 0.0, []
    known = atomic_profile(context)
    growth = []
    for match in atomics:
        skill = match.canonical_skill
        path = context.profile_config.get('growth_paths', {}).get(skill)
        if not path or known.get(skill, 0) >= context.settings['fit']['known_atomic_threshold']:
            continue
        adjacent = {k: context.profile.get(k, 0) for k in path['adjacent_concepts'] if context.profile.get(k, 0) > 0}
        pct = prevalence.get(skill)
        if not adjacent or pct is None or pct <= 0:
            continue
        relevance = min(1, float(pct) / settings['prevalence_saturation_pct'])
        novelty = 1 - max(0, min(1, known.get(skill, 0)))
        points = settings['points_per_growth_skill'] * relevance * path['priority'] * min(1, max(adjacent.values())) * novelty
        growth.append(dict(skill=skill, prevalence_pct=float(pct), adjacent_concepts=adjacent,
                           priority=path['priority'], novelty=novelty, contribution=round(points, 3)))
    return round(min(settings['max_score'], sum(g['contribution'] for g in growth)), 2), growth


def calculate_confidence(lanes, description, ambiguity, settings):
    """Explainable heuristic confidence, explicitly NOT a calibrated probability."""
    ordered = sorted(lanes.lane_scores.values(), reverse=True)
    margin = (ordered[0] - ordered[1]) / max(1, ordered[0])
    signal_count = sum(1 for rule in lanes.triggered_rules if rule['kind'] == 'signal')
    evidence = dict(margin=round(margin, 3), signal_count=signal_count,
                    contradictions=lanes.contradictions, requirement_ambiguity=ambiguity,
                    weak_description=len(description.split()) < settings['weak_description_words'],
                    heuristic_not_probability=True)
    value = settings['base'] + settings['margin_weight']*margin + settings['signal_weight']*min(1,signal_count/settings['signal_saturation'])
    value -= settings['contradiction_penalty']*len(lanes.contradictions)
    value -= settings['ambiguity_penalty']*bool(ambiguity)
    value -= settings['weak_description_penalty']*evidence['weak_description']
    if lanes.hard_exclusions:
        value = settings['hard_exclusion_confidence']
        evidence['hard_exclusion_override'] = lanes.hard_exclusions
    return round(min(1, max(0, value)), 3), evidence


def should_request_ai_review(grade, settings=None):
    """Return a review request only; no provider or automatic AI call is introduced."""
    if settings is None:
        settings = read_config(CONFIG_DIR/'weights.yml')['confidence']
    if settings['suppress_review_on_hard_exclusion'] and grade.confidence_evidence.get('hard_exclusion_override'):
        return False
    return bool(grade.confidence < settings['review_below'] or
                grade.confidence_evidence['margin'] <= settings['close_margin'] or
                (settings['review_on_contradictions'] and grade.confidence_evidence['contradictions']) or
                (settings['review_on_requirement_ambiguity'] and grade.confidence_evidence['requirement_ambiguity']))


def _grade_job(row, context=None, *, prevalence=None, market_context=None):
    context = context or GradingContext.load()
    import math
    if prevalence is not None and any(not math.isfinite(float(pct)) or not 0 <= float(pct) <= 100 for pct in prevalence.values()):
        raise ValueError('Prevalence must be percentages between 0 and 100')
    title, description = clean_text(row.get('title')), clean_text(row.get('description'))
    row = dict(row, title=title, description=description)
    atomics = extract_market_skills(description, context.taxonomy)
    counts = match_skills(description, context.skills)
    requirements_config = dict(context.requirements, _taxonomy=context.taxonomy)
    flags = extract_requirement_flags(description, context.skills, context.profile, requirements_config,
                                      atomic_terms=[alias for aliases in context.taxonomy.values() for alias in aliases],
                                      atomic_profile=atomic_profile(context),
                                      known_atomic_threshold=context.settings['fit']['known_atomic_threshold'])
    title_seniority = list(term_counts(title, context.roles['seniority_penalties']['hard_titles']))
    if term_counts(title, context.requirements['lead_title_terms']):
        flags['is_lead_like'] = True
        if 'lead_like' not in flags['reason_codes']:
            flags['reason_codes'].append('lead_like')
    flags['seniority_signals'] = list(dict.fromkeys(flags['seniority_signals'] + title_seniority))
    title_levels = {name: level['rank'] for name, level in context.requirements.get('seniority_levels', {}).items()
                    if term_counts(title, level['terms'])}
    flags['title_levels'] = title_levels
    lanes = score_lanes(row, context.roles)
    gaps = extract_gaps(description, flags, context)
    years = flags['years_required']
    facts = dict(always=True, role_lane=lanes.role_lane, years_required=min(years) if isinstance(years,tuple) else years,
                 has_hard_requirement_blockers=flags['has_hard_requirement_blockers'], is_lead_like=flags['is_lead_like'],
                 missing_required_atomic=gaps['required']['atomic_skills'], blockers=[], review_flags=[],
                 search_lane=clean_text(row.get('search_lane')).lower())
    experience = context.profile_config.get('experience_years')
    facts.update(experience_gap=max(0, facts['years_required'] - max(experience))
                 if experience and facts['years_required'] is not None else None,
                 seniority_rank=max(title_levels.values(), default=0),
                 ownership_evidence=bool(flags.get('ownership_evidence')),
                 years_anomaly=bool(flags.get('years_anomalies')),
                 active_clearance_missing=any(e['kind'] == 'active' for e in flags['clearance_evidence'])
                 and context.profile_config.get('active_clearance') is False,
                 clearance_review=bool(flags['clearance_evidence'])
                 and context.profile_config.get('active_clearance') is not True)
    facts.update({'hits.'+k:v for k,v in lanes.category_hits.items()})
    # Reuse authored evidence flags across stages without duplicating policy predicates.
    facts.update({'flags.'+k:v for k,v in lanes.policy_flags.items()})
    fit, fit_evidence = calculate_fit_score(counts, flags, gaps, lanes.role_lane, context, facts)
    facts['fit_score'] = fit
    learning, growth = calculate_learning_score(atomics, lanes.role_lane, context, prevalence or {})
    confidence, confidence_evidence = calculate_confidence(lanes, description, flags['requirement_ambiguity'], context.settings['confidence'])
    with evaluation_config(context.roles, context.settings):
        alignment_evidence = []
        alignment, matched, total, missing = weighted_alignment_score(counts, context.profile, context.weights,
                                                                     context.penalties, description, flags, alignment_evidence)
        label = classify(alignment, flags)
    concepts = {k: list(term_counts(description, context.skills[k])) for k,n in counts.items() if n and k != 'seniority'}
    reasons = list(dict.fromkeys(flags['reason_codes'] + lanes.contradictions + lanes.hard_exclusions))
    if prevalence is None:
        reasons.append('market_prevalence_unavailable')
        learning = None
    grade = DeterministicGrade(
        job_id=clean_text(row.get('id') or row.get('source_job_id')), role_lane=lanes.role_lane,
        lane_scores=lanes.lane_scores, raw_lane_scores=lanes.raw_lane_scores,
        fit_score=fit, learning_score=learning, pre_ai_score=fit, confidence=confidence,
        learning_status='unavailable' if prevalence is None else ('eligible' if lanes.role_lane in context.settings['learning']['eligible_lanes'] else 'ineligible'),
        blocking_reasons=facts['blockers'], review_flags=facts['review_flags'],
        policy_flags=lanes.policy_flags,
        input_context={k: {'value':clean_text(row.get(k)), 'available':bool(clean_text(row.get(k)))} for k in ('search_lane','review_priority')},
        confidence_evidence=confidence_evidence, matched_atomic_skills=[asdict(m) for m in atomics],
        matched_capability_concepts=concepts, missing_required_skills=gaps['required'],
        missing_preferred_skills=gaps['preferred'], growth_skills=growth, market_relevant_gaps=growth,
        matched_role_signals=[e for e in lanes.triggered_rules if e['kind']=='signal'],
        seniority_signals=dict(terms=flags['seniority_signals'], years_required=flags['years_required'],
                              title_levels=title_levels, candidate_experience_years=experience,
                              experience_gap=facts['experience_gap'], years_evidence=flags['years_evidence'],
                              years_anomalies=flags['years_anomalies']),
        exclusion_signals=[e for e in lanes.triggered_rules if e.get('lane')=='wrong_lane'],
        triggered_rules=lanes.triggered_rules + fit_evidence + alignment_evidence,
        reason_codes=reasons, apply_decision='', fit_quality='',
        ai_review_required=False, ai_review_reasons=[], grading_version=context.grading_version,
        taxonomy_version=context.taxonomy_version,
        market_context=dict(market_context or {'source': 'unavailable' if prevalence is None else 'supplied'},
                            prevalence_pct={m.canonical_skill: (prevalence or {}).get(m.canonical_skill) for m in atomics}),
        alignment_score=alignment, label=label, matched=matched, required_total=total, missing=missing, counts=counts,
        lane_resolution=lanes.resolution, category_hits=lanes.category_hits,
        requirement_flags={k:v for k,v in flags.items() if k not in ('sections', 'semantic_requirement_text', 'requirement_groups')})
    grade.ai_review_required = should_request_ai_review(grade, context.settings['confidence'])
    grade.triggered_rules.append(dict(rule_id='ai_review_gate', kind='decision', result=grade.ai_review_required,
                                     confidence=confidence, margin=confidence_evidence['margin']))
    if grade.ai_review_required:
        grade.ai_review_reasons = list(lanes.contradictions)
        if confidence < context.settings['confidence']['review_below']:
            grade.ai_review_reasons.append('low_heuristic_confidence')
        if confidence_evidence['margin'] <= context.settings['confidence']['close_margin']:
            grade.ai_review_reasons.append('close_lane_scores')
        if flags['requirement_ambiguity']:
            grade.ai_review_reasons.append('ambiguous_requirements')
    facts['ai_review_required'] = grade.ai_review_required
    with evaluation_config(context.roles, context.settings):
        grade.fit_quality = derive_fit_quality(facts, grade.triggered_rules)
        grade.apply_decision = decide_apply_bucket(facts, grade.triggered_rules)
    grade.reason_codes.extend(facts['blockers'] + facts['review_flags'])
    grade.reason_codes = list(dict.fromkeys(grade.reason_codes + [
        e['rule_id'] for e in grade.triggered_rules if e['kind'] in ('override', 'decision')]))
    return grade


def grade_job(row, context=None, *, prevalence=None, market_context=None, trace=False):
    """Grade through the production path; optional trace captures evaluator history."""
    if trace:
        with capture_evaluations() as history:
            grade = _grade_job(row, context, prevalence=prevalence, market_context=market_context)
    else:
        history = None
        grade = _grade_job(row, context, prevalence=prevalence, market_context=market_context)
    context = context or GradingContext.load()
    grade.observability = build_observability(grade, grade.lane_resolution,
                                               grade.category_hits, context.settings)
    if history is not None:
        grade.observability['evaluations'] = history
    return grade
