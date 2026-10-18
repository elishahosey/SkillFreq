"""Small, explicit SkillFreq forms and search entries; no separate config schema."""
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re

import yaml

from scripts.config_editor import (
    FILES, ConfigFile, _select_setting, load_config, make_changes_preview,
    parse_yaml, save_preview,
)
from skillfreq.score.policy import LANES

VIEWS = ('Quick Edit', 'Profile', 'Skills / Vocabulary', 'Role Lanes',
         'Seniority / Requirements / Hard Filters', 'Advanced Policy', 'Advanced YAML')
GUIDANCE = {
    'profile.yml': 'Candidate Profile: Change this when SkillFreq’s stored description of your actual experience, skills, familiarity, growth interests, or clearance status is inaccurate or outdated. If those values are already correct but the grader behaves as if they are different, investigate grader code instead. A job belonging in a different lane is a Role/Lane Policy question.',
    'skills.yml': 'Vocabulary: Add or change terms when the config does not know a synonym, capability phrase, or capability-to-technology mapping. If the correct term already exists but extraction fails to use it, investigate the extractor/grader. Atomic technology aliases belong in market_skills.yml.',
    'market_skills.yml': 'Vocabulary: Add or change terms when the config does not know a technology synonym or alias. If the correct term already exists but extraction fails to use it, investigate the extractor/grader. Broader capability phrases and capability-to-technology mappings belong in skills.yml.',
    'roles.yml': 'Role/Lane Policy: Change this when your intended policy for what kinds of jobs belong in TARGET, SECONDARY, BRIDGE, SURVIVAL, or WRONG is represented incorrectly. “This type of job should be TARGET” is usually a role-policy question, not a candidate-profile question. For example, changing how Integration Engineer fits your search strategy is a role-policy edit. If the correct rule already exists but the job still becomes WRONG, investigate lane logic.',
    'requirements.yml': 'Requirements/Seniority Policy: Change this when the intended tolerance, ranking, vocabulary, or requirement policy itself is wrong. If years, modality, ownership, or clearance evidence are extracted incorrectly from the posting, investigate grader/parser logic instead. Changing seniority ranking/tolerance is a config decision; years_required = 200, or “strong plus” classified as required despite correct preferred patterns, is a grader/parser issue.',
    'weights.yml': 'Scoring/Decision Policy: Change this only when calibration evidence shows the scoring policy itself is wrong. Do not use weight or threshold changes to compensate for broken extraction, incorrect lane classification, or ignored profile/config values.',
    'resume_signal.yml': 'These are resume evidence domains and references, not candidate proficiency. Correct references that are ignored require resume extraction work.',
}
ISSUE_CHEAT_SHEET = """**Which kind of issue is this?**

- **Facts about me are wrong** → Profile
- **Type of job belongs in a different lane** → Role/Lane Policy
- **Seniority/requirement tolerance itself is wrong** → Requirements/Policy
- **Missing synonym/alias/technology mapping** → Vocabulary
- **Config is already correct but output is wrong** → Grader/code
"""
ERRORS = (ValueError, TypeError, KeyError, OSError, yaml.YAMLError, re.error)


@dataclass
class Setting:
    file: str
    path: tuple
    title: str
    kind: str
    value: object
    evidence: str = ''

    @property
    def label(self):
        return f'{self.title} — {self.file}' + (' · Advanced' if self.kind == 'advanced' else '')


def settings_catalog(bundle):
    """Index the owned surfaces, not every arbitrary YAML leaf."""
    data = {name: parse_yaml(content) for name, content in bundle.items()}
    entries = []

    def add(file, path, kind, title=None, evidence=''):
        value = data[file]
        for key in path:
            value = value[key]
        entries.append(Setting(file, path, title or str(path[-1]), kind, value, evidence))

    profile = data['profile.yml']
    for key in ('experience_years', 'active_clearance'):
        add('profile.yml', (key,), key, key.replace('_', ' ').title())
    # Group each technology's familiarity, growth path and notes in one form.
    for name in dict.fromkeys([*data['market_skills.yml'], *profile['growth_paths']]):
        value = {field: profile[field][name] for field in ('atomic_skills', 'growth_paths', 'atomic_skill_notes')
                 if name in profile[field]}
        entries.append(Setting('profile.yml', ('atomic_skills', name), name, 'technology', value,
                               ' '.join(data['market_skills.yml'].get(name, []))))
    for name in data['skills.yml']:
        entries.append(Setting('profile.yml', ('skills', name), name + ' capability strength', 'strength',
                               profile['skills'].get(name, 0.0)))
        add('skills.yml', (name,), 'concept')
    for name in data['market_skills.yml']:
        add('market_skills.yml', (name,), 'terms', name + ' aliases')
    roles = data['roles.yml']
    for section in ('vocabulary', 'term_groups', 'title_overrides', 'negative_keywords', 'resume_variants'):
        for name, value in roles[section].items():
            kind = 'text' if section == 'vocabulary' else 'terms' if (
                isinstance(value, list) and all(isinstance(v, str) for v in value)) else 'advanced'
            add('roles.yml', (section, name), kind, f'{section}: {name}')
    for section in ('lane_rules', 'eligibility_rules'):
        for index, rule in enumerate(roles[section]):
            group = roles['term_groups'].get(rule.get('group'), '')
            seen = set()
            while isinstance(group, str) and group in roles['term_groups'] and group not in seen:
                seen.add(group)
                group = roles['term_groups'][group]
            add('roles.yml', (section, index), 'lane' if section == 'lane_rules' else 'advanced',
                rule['id'], str(group))
    requirements = data['requirements.yml']
    for name in requirements['seniority_levels']:
        add('requirements.yml', ('seniority_levels', name), 'seniority', name + ' seniority')
    for key in requirements:
        if key == 'seniority_levels':
            continue
        kind = ('terms' if key in ('seniority_terms', 'lead_terms', 'lead_title_terms', 'core_blocker_skills', 'modern_stack_skills')
                else 'equivalences' if key == 'equivalences'
                else 'integer' if key in ('maximum_experience_years', 'modern_blocker_count') else 'advanced')
        add('requirements.yml', (key,), kind)
    # Policy stays explicitly Advanced, even when discovered by global search.
    for key, value in data['weights.yml'].items():
        if key in ('quality_rules', 'decision_rules'):
            for index, rule in enumerate(value):
                add('weights.yml', (key, index), 'advanced', rule['id'])
        elif isinstance(value, dict):
            for child in value:
                add('weights.yml', (key, child), 'advanced', f'{key}: {child}')
        else:
            add('weights.yml', (key,), 'advanced')
    for name in data['resume_signal.yml']:
        add('resume_signal.yml', (name,), 'advanced', name + ' resume evidence')
    return entries


def search_settings(entries, query):
    words = query.casefold().split()
    return [entry for entry in entries if all(word in (
        entry.label + ' ' + '.'.join(map(str, entry.path)) + ' ' + str(entry.value) + ' ' + entry.evidence
    ).casefold() for word in words)]


def _lines(st, label, values):
    return [line.strip() for line in st.text_area(label + ' (one per line)', '\n'.join(values)).splitlines() if line.strip()]


def _number(st, label, value, **kwargs):
    return st.number_input(label, value=float(value), **kwargs)


def _focused_form(st, entry, loaded, bundle):
    """Return path/value edits for one explicit supported config structure."""
    value, path, kind = entry.value, entry.path, entry.kind
    if kind == 'experience_years':
        return [(path, [st.number_input('Minimum experience (years)', value=value[0]),
                        st.number_input('Maximum experience (years)', value=value[1])])]
    if kind == 'active_clearance':
        return [(path, st.selectbox('Active clearance', [False, True, None], index=[False, True, None].index(value),
                                   format_func=lambda v: 'Unknown' if v is None else 'Yes' if v else 'No'))]
    if kind == 'technology':
        name = path[-1]
        profile = loaded.data
        updates = []
        current = profile['atomic_skills'].get(name, 0)
        familiarity = _number(st, 'Atomic familiarity', current, min_value=0.0, max_value=1.0, step=0.05)
        if name in profile['atomic_skills'] or familiarity != current:
            updates.append((path, familiarity))
        growth = profile['growth_paths'].get(name)
        if growth is not None:
            updates += [
                (('growth_paths', name, 'priority'), _number(st, 'Growth priority', growth['priority'], min_value=0.0, max_value=1.0, step=0.05)),
                (('growth_paths', name, 'adjacent_concepts'), st.multiselect('Adjacent concepts',
                    list(parse_yaml(bundle['skills.yml'])), default=growth['adjacent_concepts'])),
            ]
        else:
            st.caption('No configured growth path. Existing growth paths are editable here.')
        note = st.text_area('Notes', profile['atomic_skill_notes'].get(name, ''))
        if note or name in profile['atomic_skill_notes']:
            updates.append((('atomic_skill_notes', name), note))
        return updates
    if kind == 'strength':
        return [(path, _number(st, 'Capability strength', value, min_value=0.0, step=0.05))]
    if kind == 'concept':
        st.caption('Atomic links: ' + ', '.join(value.get('atomic_skills', [])))
        st.caption('Term refs: ' + str(value.get('term_refs', [])))
        return [(path + ('terms',), _lines(st, 'Vocabulary terms', value['terms']))]
    if kind == 'terms':
        return [(path, _lines(st, 'Terms', value))]
    if kind == 'text':
        return [(path, st.text_input('Role term', value))]
    if kind == 'integer':
        return [(path, st.number_input(entry.title, value=value, min_value=1 if path[-1] == 'maximum_experience_years' else 0))]
    if kind == 'seniority':
        return [(path + ('rank',), st.number_input('Seniority rank', value=value['rank'], min_value=0)),
                (path + ('terms',), _lines(st, 'Seniority terms', value['terms']))]
    if kind == 'lane':
        st.caption(f"Rule ID: {value['id']} · Scope: {value['scope']} · Hard exclusion: {value['hard_exclusion']}")
        st.write('Pattern/group:', value.get('pattern', value.get('title_pattern', value.get('group'))))
        if entry.evidence:
            with st.expander('Group terms / references'):
                st.text(entry.evidence)
        lanes = list(LANES)
        return [(path + ('lane',), st.selectbox('Lane', lanes, index=lanes.index(value['lane']))),
                (path + ('active',), st.checkbox('Active', value=value['active'])),
                (path + ('weight',), _number(st, 'Evidence weight', value['weight']))]
    raise ValueError('This setting requires Advanced editing')


def _advanced_value(st, value, raw=False):
    if not raw and isinstance(value, bool):
        return st.checkbox('Value', value=value)
    if not raw and type(value) in (int, float):
        return st.number_input('Value', value=value)
    if not raw and isinstance(value, str):
        return st.text_input('Value', value=value)
    return st.text_area('Value (YAML)', yaml.safe_dump(value, sort_keys=False, allow_unicode=True), height=260)


def render_editor(config_dir):
    import streamlit as st

    st.set_page_config(page_title='SkillFreq calibration config', layout='wide')
    st.title('SkillFreq calibration config')
    st.info('Config issue: If I can fix the behavior by changing configuration without changing the intended algorithm, it is probably a config issue.\n\n'
            'Grader issue: If I need to change how the algorithm parses, resolves, scores, or applies that configuration, it is probably a grader issue.')
    st.markdown(ISSUE_CHEAT_SHEET)
    view = st.sidebar.radio('View', VIEWS)
    reset = st.sidebar.button('Reload / reset')
    if reset or st.session_state.get('config_directory') != str(config_dir):
        st.session_state.pop('config_bundle', None)
        st.session_state.pop('config_preview', None)
        st.session_state.edit_generation = st.session_state.get('edit_generation', 0) + 1
    st.session_state.config_directory = str(config_dir)
    try:
        if 'config_bundle' not in st.session_state:
            st.session_state.config_bundle = load_config(config_dir, 'profile.yml').bundle
        bundle = st.session_state.config_bundle
        generation = st.session_state.get('edit_generation', 0)
        if 'config_saved' in st.session_state:
            st.success(st.session_state.pop('config_saved'))
        entries = settings_catalog(bundle)
        raw = view == 'Advanced YAML'
        if raw:
            st.warning('Advanced YAML escape hatch. Edit one selected setting; all bundle validation still applies.')
            filename = st.sidebar.selectbox('Config file', FILES)
            loaded = ConfigFile(Path(config_dir).resolve() / filename, bundle, parse_yaml(bundle[filename]))
            section = st.sidebar.selectbox('Section', list(loaded.data))
            path, value = _select_setting(st, loaded, section)
            entry = Setting(filename, path, '.'.join(map(str, path)), 'advanced', value)
        else:
            query = st.text_input('Search configuration', placeholder='Terraform, networking, Integration Engineer, principal, clearance…')
            files = {'Profile': ('profile.yml',), 'Skills / Vocabulary': ('skills.yml', 'market_skills.yml'),
                     'Role Lanes': ('roles.yml',), 'Seniority / Requirements / Hard Filters': ('requirements.yml',)}
            if view in files:
                entries = [e for e in entries if e.file in files[view]]
            if view == 'Advanced Policy':
                entries = [e for e in entries if e.kind == 'advanced']
            elif view == 'Quick Edit' and not query.strip():
                entries = [e for e in entries if e.file == 'profile.yml']
                st.caption('Start with your profile, or search all seven config files. Nothing is saved automatically.')
            matches = search_settings(entries, query)
            if not matches:
                st.info('No matching setting. A missing term may belong in vocabulary. New behavior that the current configuration cannot express requires grader/code change.')
                return
            st.caption(f'{len(matches)} matching settings')
            entry = st.selectbox('Setting to edit', matches, format_func=lambda e: e.label, key=f'result:{view}:{query}:{generation}')
            loaded = ConfigFile(Path(config_dir).resolve() / entry.file, bundle, parse_yaml(bundle[entry.file]))
        identity = (entry.file, entry.path, view)
        if st.session_state.get('edit_identity') != identity:
            st.session_state.pop('config_preview', None)
            st.session_state.edit_identity = identity
        st.subheader(entry.title)
        st.caption(f'Source: {loaded.path} · Modified: ' + datetime.fromtimestamp(loaded.path.stat().st_mtime).astimezone().isoformat(timespec='seconds'))
        st.caption(GUIDANCE[entry.file])
        advanced = raw or view == 'Advanced Policy'
        if not advanced and entry.kind in ('advanced', 'concept', 'lane'):
            if entry.kind == 'advanced':
                st.write(entry.value)
            advanced = st.checkbox('Open in Advanced', key=f'advanced:{identity}:{generation}')
        if entry.kind == 'advanced' and not advanced:
            st.caption('Complex policy or references: inspect above, then open in Advanced to edit this setting.')
            return
        if advanced:
            st.warning('Advanced / Policy — change only the intended policy. Review all affected paths before saving.')
        equivalence_owner = None
        if entry.kind == 'equivalences' and not advanced:
            st.caption('Explicit approved equivalents; broad capability does not automatically satisfy a technology.')
            equivalence_owner = st.selectbox('Required atomic technology', list(parse_yaml(bundle['market_skills.yml'])))
        with st.form(f'edit:{identity}:{generation}:{advanced}:{equivalence_owner}'):
            if equivalence_owner:
                current = entry.value.get(equivalence_owner, {})
                accepted = dict(current)
                for field, file in (('atomic_skills', 'market_skills.yml'), ('capability_concepts', 'skills.yml')):
                    chosen = st.multiselect(field.replace('_', ' ').title(), list(parse_yaml(bundle[file])), default=current.get(field, []))
                    if field in current or chosen:
                        accepted[field] = chosen
                updates = [(entry.path + (equivalence_owner,), accepted)] if accepted else []
            elif advanced:
                draft = _advanced_value(st, entry.value, raw)
                updates = []  # Parse only on submit so incomplete YAML remains editable.
            else:
                updates = _focused_form(st, entry, loaded, bundle)
            submitted = st.form_submit_button('Validate and preview')
        if submitted:
            st.session_state.pop('config_preview', None)
            try:
                if advanced:
                    value = parse_yaml(draft) if raw or isinstance(entry.value, (dict, list)) or entry.value is None else draft
                    updates = [(entry.path, value)]
                st.session_state.config_preview = make_changes_preview(loaded, updates)
            except ERRORS as error:
                st.error(str(error))
        preview = st.session_state.get('config_preview')
        if preview:
            st.subheader('Validated changes')
            st.code('\n'.join(preview.changes), language='text')
            with st.expander('Advanced: full YAML diff'):
                st.code(preview.diff, language='diff')
            st.caption('Save writes exactly this preview. Further edits need Validate and preview again. No autosave.')
            if st.button('Save validated changes', type='primary'):
                try:
                    backup = save_preview(preview)
                    st.session_state.config_saved = f'Saved {loaded.path}. Backup: {backup}'
                    st.session_state.pop('config_bundle', None)
                    st.session_state.pop('config_preview', None)
                    st.session_state.edit_generation = generation + 1
                    st.rerun()
                except ERRORS as error:
                    st.error(str(error))
        with st.expander('Advanced: current setting YAML (read only)'):
            st.code(yaml.safe_dump(entry.value, sort_keys=False, allow_unicode=True), language='yaml')
    except ERRORS as error:
        st.error(f'Cannot load config: {error}')
