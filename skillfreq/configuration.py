"""Small configuration loaders, not a rules engine.

References express evidence reuse; they never equate an atomic technology with a
capability or a role. YAML is authored locally and snapshots are persisted by IO.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math
import yaml
from contextvars import ContextVar
from contextlib import contextmanager

CONFIG_DIR = Path(__file__).resolve().parents[1] / 'configs'
_evaluation_config = ContextVar('evaluation_config', default=None)


@contextmanager
def evaluation_config(roles, weights):
    token = _evaluation_config.set((roles, weights))
    try:
        yield
    finally:
        _evaluation_config.reset(token)


def scoring_config():
    current = _evaluation_config.get()
    return current[1] if current else read_config(CONFIG_DIR/'weights.yml')


def read_config(path: Path) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{path} must contain a mapping')
    return data


def configuration_version(snapshot):
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, allow_nan=False).encode()).hexdigest()[:16]


def resolve_terms(refs, *, roles=None, concepts=None, taxonomy=None, requirements=None):
    roles = roles if roles is not None else read_config(CONFIG_DIR/'roles.yml')
    concepts = concepts if concepts is not None else read_config(CONFIG_DIR/'skills.yml')
    if taxonomy is None:
        from skillfreq.skills.job_market import load_market_taxonomy
        taxonomy = load_market_taxonomy(CONFIG_DIR/'market_skills.yml')
    requirements = requirements if requirements is not None else read_config(CONFIG_DIR/'requirements.yml')
    terms = []
    for ref in refs:
        if isinstance(ref, str):
            terms.append(ref)
        elif not isinstance(ref, dict) or len(ref) != 1:
            raise ValueError(f'Invalid term reference: {ref!r}')
        elif 'atomic' in ref:
            terms.extend(taxonomy[ref['atomic']])
        elif 'concept_term' in ref:
            concept, term = ref['concept_term']
            if term not in concepts[concept]['terms']:
                raise ValueError(f'Unknown capability term: {ref!r}')
            terms.append(term)
        elif 'seniority' in ref:
            if ref['seniority'] not in requirements['seniority_terms']:
                raise ValueError(f'Unknown seniority term: {ref!r}')
            terms.append(ref['seniority'])
        elif 'role_term' in ref:
            terms.append(roles['vocabulary'][ref['role_term']])
        else:
            raise ValueError(f'Unknown term reference: {ref!r}')
    return list(dict.fromkeys(terms))


def load_roles(path=CONFIG_DIR/'roles.yml', *, concepts=None, taxonomy=None, requirements=None):
    concepts = concepts if concepts is not None else read_config(CONFIG_DIR/'skills.yml')
    if taxonomy is None:
        from skillfreq.skills.job_market import load_market_taxonomy
        taxonomy = load_market_taxonomy(CONFIG_DIR/'market_skills.yml')
    requirements = requirements if requirements is not None else read_config(CONFIG_DIR/'requirements.yml')
    roles = read_config(path)
    resolve = lambda refs: resolve_terms(refs, roles=roles, concepts=concepts,
                                          taxonomy=taxonomy, requirements=requirements)
    def resolve_group(name, stack=()):
        if name in stack:
            raise ValueError(f'Cyclic term-group reference: {name}')
        if name not in roles['term_groups']:
            raise ValueError(f'Unknown term group: {name}')
        refs = roles['term_groups'][name]
        return resolve_group(refs, stack + (name,)) if isinstance(refs, str) else resolve(refs)
    roles['resolved_groups'] = {name: resolve_group(name) for name in roles['term_groups']}
    for meta in roles['resume_variants'].values():
        meta['keywords'] = resolve(meta['keywords'])
    for section in ('title_overrides', 'negative_keywords', 'seniority_penalties'):
        roles[section] = {name: resolve(refs) for name, refs in roles[section].items()}
    roles['ai_stack_penalty']['keywords'] = resolve(roles['ai_stack_penalty']['keywords'])
    roles['tie_breakers'] = {name: resolve(refs) for name, refs in roles.get('tie_breakers', {}).items()}
    seen = set()
    for rule in roles['lane_rules']:
        if rule['id'] in seen:
            raise ValueError(f"Duplicate rule id: {rule['id']}")
        seen.add(rule['id'])
        if rule['scope'] not in ('title', 'description', 'both'):
            raise ValueError(f"Invalid scope in {rule['id']}")
        if rule['lane'] not in ('target_lane','secondary_lane','bridge_lane','survival_lane','wrong_lane'):
            raise ValueError(f"Invalid lane in {rule['id']}")
        if not isinstance(rule['active'], bool) or not isinstance(rule['hard_exclusion'], bool):
            raise ValueError('Rule active/hard_exclusion must be booleans')
        if not isinstance(rule['weight'], (int, float)) or not math.isfinite(rule['weight']):
            raise ValueError('Rule weight must be a finite number')
        if not isinstance(rule['max_hits'], int) or rule['max_hits'] < 1:
            raise ValueError('Rule max_hits must be a positive integer')
        if sum(key in rule for key in ('pattern','title_pattern','group')) != 1:
            raise ValueError(f"Conflicting or missing title pattern in {rule['id']}")
        if 'title_pattern' in rule:
            pattern = rule['title_pattern']
            if (rule['scope'] != 'title' or not isinstance(pattern,dict) or set(pattern) != {'any','with'}
                    or any(not isinstance(v,list) or not v or any(not isinstance(t,str) or not t.strip() for t in v) for v in pattern.values())):
                raise ValueError(f"Malformed title pattern in {rule['id']}")
        elif rule.get('pattern'):
            import re
            re.compile(rule['pattern'])
        elif rule.get('group') not in roles['resolved_groups']:
            raise ValueError(f"Unknown group in {rule['id']}")
    from skillfreq.score.policy import LANES, validate_rules
    flags = set(roles['derived_flags'])
    if any(not isinstance(name,str) or not name.isidentifier() for name in flags):
        raise ValueError('Invalid derived flag name')
    fields = {'always','eligible','contradictions','hard_exclusions','search_lane'} | flags
    fields |= {'hits.'+r['category'] for r in roles['lane_rules']}
    fields |= {'points.'+lane for lane in LANES}
    writable = dict(eligible='list', contradictions='list', **{f:'bool' for f in flags})
    writable.update({'points.'+lane:'score' for lane in LANES})
    validate_rules(roles['eligibility_rules'], fields, writable)
    if roles['lane_policy']['fallback_lane'] not in LANES or not 0 <= roles['lane_policy']['fallback_score'] <= 100:
        raise ValueError('Invalid lane fallback')
    return roles


def validate_grading_settings(settings, roles):
    from skillfreq.score.policy import LANES, validate_rules
    fields = {'always','role_lane','fit_score','years_required','has_hard_requirement_blockers',
              'is_lead_like','missing_required_atomic','blockers','review_flags','search_lane','ai_review_required'}
    fields |= {'experience_gap', 'seniority_rank', 'ownership_evidence', 'years_anomaly',
               'active_clearance_missing', 'clearance_review'}
    fields |= {'hits.'+r['category'] for r in roles['lane_rules']}
    fields |= {'flags.'+name for name in roles.get('derived_flags', [])}
    validate_rules(settings['fit']['rules'], fields, dict(fit_score='score',blockers='list',review_flags='list'))
    validate_rules(settings['quality_rules'], fields, dict(fit_quality=('good_fit','possible_fit','weak_fit')))
    validate_rules(settings['decision_rules'], fields, dict(apply_decision=('apply_now','manual_review','skip')))
    for stage in ('quality_rules','decision_rules'):
        final = min(settings[stage],key=lambda r:r['priority'])
        if final['when'] != dict(field='always',op='equals',value=True) or not final.get('stop') or not final.get('active',True):
            raise ValueError(f'{stage} needs an active unconditional final outcome')
    ids = [r['id'] for rules in (settings['fit']['rules'],settings['quality_rules'],settings['decision_rules'],roles['eligibility_rules'],roles['lane_rules']) for r in rules]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate rule ID across policy stages')
    def number(value, low, high, name):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f'Invalid threshold or score range: {name}')
    fit = settings['fit']
    if set(fit['lane_caps']) != set(LANES):
        raise ValueError('Invalid lane caps')
    for key,value in fit['lane_caps'].items(): number(value,0,100,key)
    for key in ('required_atomic_penalty','preferred_atomic_penalty','required_group_penalty','base_score','coverage_scale'):
        number(fit[key],0,100,key)
    number(fit['known_atomic_threshold'],0,1,'known_atomic_threshold')
    for key,value in fit['flag_penalties'].items():
        if key not in {'has_hard_requirement_blockers','has_modern_stack_blockers','is_lead_like'}:
            raise ValueError(f'Unknown requirement flag: {key}')
        number(value,0,100,key)
    learning = settings['learning']
    if not isinstance(learning['eligible_lanes'],list) or set(learning['eligible_lanes']) - set(LANES):
        raise ValueError('Invalid learning lane')
    number(learning['prevalence_saturation_pct'],0.001,100,'prevalence_saturation_pct')
    for key in ('points_per_growth_skill','max_score'): number(learning[key],0,100,key)
    for key,value in settings['confidence'].items():
        if key in {'review_on_contradictions','review_on_requirement_ambiguity','suppress_review_on_hard_exclusion'}:
            if not isinstance(value,bool): raise ValueError(f'Invalid confidence flag: {key}')
        else:
            number(value,0.001 if key == 'signal_saturation' else 0,
                   10000 if key in {'signal_saturation','weak_description_words'} else 1,key)
    thresholds = settings['thresholds']
    if not 0 <= thresholds['low'] <= thresholds['moderate'] <= thresholds['high'] <= 100:
        raise ValueError('Invalid alignment thresholds')
    for group, section in settings.get('alignment', {}).get('section_scopes', {}).items():
        if f'alignment.{group}' not in roles.get('resolved_groups', {}) and f'alignment.{group}' not in roles.get('term_groups', {}):
            raise ValueError(f'Unknown alignment section-scoped group: {group}')
        if section not in {'required', 'preferred', 'responsibilities', 'full_text'}:
            raise ValueError(f'Invalid alignment section scope: {section}')


@lru_cache(maxsize=4)
def _default_roles(_fingerprint):
    return load_roles()


def default_roles():
    # A config edit takes effect without requiring a Python process restart.
    paths = ['roles.yml','skills.yml','market_skills.yml','requirements.yml']
    return _default_roles(tuple((CONFIG_DIR/name).stat().st_mtime_ns for name in paths))


def rule_terms(name: str):
    current = _evaluation_config.get()
    return (current[0] if current else default_roles())['resolved_groups'][name]
