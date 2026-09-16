"""One-time migration helper; retained to document the vocabulary inventory process."""
import ast
from pathlib import Path
import yaml


def migrate():
    root = Path(__file__).resolve().parents[1]
    def read(name):
        return yaml.safe_load((root / 'configs' / name).read_text(encoding='utf-8'))
    def write(name, value):
        (root / 'configs' / name).write_text(yaml.safe_dump(value, sort_keys=False, width=100), encoding='utf-8')
    skills, roles, market = read('skills.yml'), read('roles.yml'), read('market_skills.yml')
    if 'lane_rules' in roles:
        raise SystemExit('Configuration already consolidated; migration is intentionally one-time.')
    alias_owner = {a: k for k, aliases in market.items() for a in aliases}
    concept_owner = {}
    for concept, terms in skills.items():
        for term in terms:
            concept_owner.setdefault(term, concept)
    seniority = skills.pop('seniority')
    vocab = {}
    def ref(term):
        if term in alias_owner:
            return {'atomic': alias_owner[term]}
        if term in seniority:
            return {'seniority': term}
        if term in concept_owner:
            return {'concept_term': [concept_owner[term], term]}
        vocab.setdefault(term, term)
        return {'role_term': term}
    concepts = {}
    for concept, terms in skills.items():
        concepts[concept] = {'terms': [], 'atomic_skills': [], 'term_refs': []}
        for term in dict.fromkeys(terms):
            if term in alias_owner:
                if alias_owner[term] not in concepts[concept]['atomic_skills']:
                    concepts[concept]['atomic_skills'].append(alias_owner[term])
            elif concept_owner[term] != concept:
                concepts[concept]['term_refs'].append([concept_owner[term], term])
            else:
                concepts[concept]['terms'].append(term)
    # Explicit relation missing from the old concept file, used by requirement blockers.
    concepts['spark'] = {'terms': [], 'atomic_skills': ['Spark'], 'term_refs': []}
    write('skills.yml', concepts)
    groups = {}
    paths = {'lane': 'score/lane_classifier.py', 'decision': 'score/decision_layer.py', 'alignment': 'score/similarity.py'}
    inventory = {}
    for prefix, filename in paths.items():
        path = root / 'skillfreq' / filename
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source)
        replacements = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.List):
                try:
                    terms = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    continue
                if terms and all(isinstance(t, str) for t in terms):
                    name = node.targets[0].id
                    group = f'{prefix}.{name}'
                    groups[group] = [ref(t) for t in dict.fromkeys(terms)]
                    for t in terms:
                        inventory.setdefault(t, []).append(f'{filename}:{name}')
                    replacements.append((node.value.lineno, node.value.col_offset, node.value.end_lineno, node.value.end_col_offset, f'rule_terms("{group}")'))
        # Preserve decision/alignment algorithms, replacing their vocabularies.
        if prefix != 'lane':
            lines = source.splitlines(keepends=True)
            for start, col, end, endcol, replacement in sorted(replacements, reverse=True):
                lines[start-1:end] = [lines[start-1][:col] + replacement + lines[end-1][endcol:]]
            source = ''.join(lines)
            source = source.replace('from __future__ import annotations', 'from __future__ import annotations\n\nfrom skillfreq.configuration import rule_terms')
            path.write_text(source, encoding='utf-8')
    # Route existing resume consumers through the same vocabulary references.
    for meta in roles['resume_variants'].values():
        meta['keywords'] = [ref(t) for t in meta['keywords']]
    for section in ['title_overrides', 'negative_keywords', 'seniority_penalties']:
        roles[section] = {k: [ref(t) for t in ts] for k, ts in roles[section].items()}
    roles['ai_stack_penalty']['keywords'] = [ref(t) for t in roles['ai_stack_penalty']['keywords']]
    rule_meta = {
        'hard_wrong_title_terms': ('wrong_lane', 100, 'title', True),
        'strong_target_title_terms': ('target_lane', 30, 'title', False),
        'secondary_title_terms': ('secondary_lane', 30, 'title', False),
        'bridge_title_terms': ('bridge_lane', 30, 'title', False),
        'consultant_title_terms': ('bridge_lane', 20, 'title', False),
        'bad_consultant_title_terms': ('wrong_lane', 30, 'title', False),
        'non_target_title_terms': ('secondary_lane', 0, 'title', False),
        'core_data_signals': ('target_lane', 6, 'description', False),
        'backend_data_signals': ('secondary_lane', 6, 'description', False),
        'support_signals': ('bridge_lane', 2, 'description', False),
        'bridge_positive_signals': ('bridge_lane', 3, 'description', False),
        'analytics_terms': ('bridge_lane', 2, 'description', False),
        'wrong_desc_terms': ('wrong_lane', 12, 'description', False),
        'platform_heavy_terms': ('wrong_lane', 8, 'description', False),
        'platform_admin_title_terms': ('wrong_lane', 25, 'title', False),
        'low_signal_terms': ('wrong_lane', 5, 'both', False),
    }
    roles['lane_rules'] = [dict(id=k, category=k, signal_type='title' if scope=='title' else 'description',
                                 group='lane.'+k, lane=lane, weight=weight, scope=scope,
                                 hard_exclusion=hard, active=True, max_hits=6 if scope!='title' else 1)
                           for k,(lane,weight,scope,hard) in rule_meta.items()]
    roles['lane_policy'] = dict(min_data_hits=2, min_support_hits=2, min_bridge_hits=4,
                                max_platform_hits=3, consultant_bridge_hits=5,
                                bad_consultant_bridge_hits=7, min_backend_hits=2,
                                fallback_wrong_score=8, conflict_penalty=15)
    requirements_tree = ast.parse((root/'skillfreq/skills/extract.py').read_text())
    requirements = {}
    for node in ast.walk(requirements_tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ['SECTION_PATTERNS', 'CORE_BLOCKER_SKILLS', 'MODERN_STACK_SKILLS', 'lead_terms']:
                value = ast.literal_eval(node.value)
                requirements[name.lower()] = sorted(value) if isinstance(value,set) else value
    requirements['seniority_terms'] = seniority
    requirements['modern_blocker_count'] = 2
    requirements['ambiguity_patterns'] = [r'\b(?:or equivalent|equivalent experience|one of the following|and/or)\b']
    write('requirements.yml', requirements)
    roles['vocabulary'] = vocab
    roles['term_groups'] = groups
    write('roles.yml', roles)
    resume = read('resume_signal.yml')
    for meta in resume.values():
        meta['aliases'] = [ref(t) for t in meta['aliases']]
    write('resume_signal.yml', resume)
    # ref() can discover resume-only role vocabulary; save final registry.
    write('roles.yml', roles)
    lines = ['# Vocabulary inventory (before migration)', '', '| Existing term | Current locations | Intended owner |', '|---|---|---|']
    for term, locations in sorted(inventory.items()):
        if term in concept_owner:
            locations.append('skills.yml:'+concept_owner[term])
        if term in alias_owner:
            locations.append('market_skills.yml:'+alias_owner[term])
        if len(locations)>1:
            owner = 'atomic '+alias_owner[term] if term in alias_owner else ('capability '+concept_owner[term] if term in concept_owner else 'roles.yml vocabulary')
            lines.append('| '+term+' | '+', '.join(locations)+' | '+owner+' |')
    (root/'docs').mkdir(exist_ok=True)
    (root/'docs/vocabulary-inventory.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__ == '__main__':
    migrate()
