"""Local config editor: python -m streamlit run scripts/config_editor.py."""
from dataclasses import dataclass
from datetime import datetime, timezone
import difflib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from uuid import uuid4

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode
from yaml.tokens import AliasToken, AnchorToken

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillfreq.configuration import CONFIG_DIR
from skillfreq.score.grading import GradingContext

FILES = ('profile.yml', 'roles.yml', 'requirements.yml', 'weights.yml',
         'market_skills.yml', 'skills.yml')


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently discarding a user's setting."""


def _mapping(loader, node):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def parse_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


@dataclass
class ConfigFile:
    path: Path
    bundle: dict
    data: dict

    @property
    def original(self):
        return self.bundle[self.path.name]


@dataclass
class Preview:
    loaded: ConfigFile
    content: bytes
    diff: str


def load_config(directory, filename):
    directory = Path(directory).resolve()
    if filename not in FILES:
        raise ValueError('Choose a supported config file')
    for name in FILES:
        if (directory / name).is_symlink():
            raise ValueError('Config symlinks are not supported')
    bundle = {name: (directory / name).read_bytes() for name in FILES}
    data = parse_yaml(bundle[filename].decode('utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Config must contain a top-level mapping')
    return ConfigFile(directory / filename, bundle, data)


def _preserve_structure(old, new, path=()):
    label = '.'.join(map(str, path)) or 'config'
    if path == ('active_clearance',):
        if new is not None and not isinstance(new, bool):
            raise ValueError('active_clearance must be true, false or null')
    elif isinstance(old, dict):
        if not isinstance(new, dict) or old.keys() - new.keys():
            raise ValueError(f'{label}: existing mapping keys must be preserved; use 0 to disable a skill')
        for key in old:
            _preserve_structure(old[key], new[key], path + (key,))
    elif isinstance(old, list):
        if not isinstance(new, list):
            raise ValueError(f'{label} must remain a list')
        if old and all(isinstance(v, str) for v in old) and any(not isinstance(v, str) for v in new):
            raise ValueError(f'{label} must contain text items')
        if old and all(type(v) in (int, float) for v in old) and any(type(v) not in (int, float) for v in new):
            raise ValueError(f'{label} must contain numeric items')
        # Rule IDs are config identity, not disposable list positions.
        if old and all(isinstance(v, dict) and 'id' in v for v in old):
            if any(not isinstance(v, dict) or not isinstance(v.get('id'), str) for v in new):
                raise ValueError(f'{label}: rules need text IDs')
            by_id = {v['id']: v for v in new}
            if len(by_id) != len(new) or {v['id'] for v in old} - by_id.keys():
                raise ValueError(f'{label}: existing rule IDs must be preserved; disable rules with active: false')
            for value in old:
                _preserve_structure(value, by_id[value['id']], path + (value['id'],))
        elif old and all(isinstance(v, list) for v in old):
            for index, value in enumerate(new):
                template = old[min(index, len(old) - 1)]
                if not isinstance(value, list) or len(value) != len(template):
                    raise ValueError(f'{label}: preserve the shape of numeric/list tuples')
                _preserve_structure(template, value, path + (index,))
    elif isinstance(old, bool):
        if not isinstance(new, bool):
            raise ValueError(f'{label} must remain a boolean')
    elif isinstance(old, (int, float)):
        if type(new) not in (int, float) or not math.isfinite(new):
            raise ValueError(f'{label} must remain a finite number')
    elif isinstance(old, str) and not isinstance(new, str):
        raise ValueError(f'{label} must remain text')


def validate_candidate(loaded, content):
    """Validate a proposed complete bundle using the grader's own loader."""
    candidate = parse_yaml(content.decode('utf-8'))
    _preserve_structure(loaded.data, candidate)
    if loaded.path.name not in ('market_skills.yml', 'skills.yml') and candidate.keys() != loaded.data.keys():
        raise ValueError('Top-level config keys must be preserved')
    # The grader validates references, profile ranges and policy rules together.
    with tempfile.TemporaryDirectory(prefix='skillfreq-config-') as temp:
        directory = Path(temp)
        for name, original in loaded.bundle.items():
            data = content if name == loaded.path.name else original
            parse_yaml(data.decode('utf-8'))
            (directory / name).write_bytes(data)
        context = GradingContext.load(
            skills_path=directory / 'skills.yml', profile_path=directory / 'profile.yml',
            weight_path=directory / 'weights.yml', roles_path=directory / 'roles.yml',
            taxonomy_path=directory / 'market_skills.yml', requirements_path=directory / 'requirements.yml')
        for field in ('skills', 'atomic_skills'):
            for name, strength in context.profile_config.get(field, {}).items():
                if type(strength) not in (int, float) or not math.isfinite(strength) or strength < 0:
                    raise ValueError(f'Profile strength must be a finite nonnegative number: {name}')
        # Supplement areas that the runtime loader deliberately treats loosely.
        for name, strength in context.profile.items():
            if not math.isfinite(strength) or strength < 0:
                raise ValueError(f'Profile strength must be finite and nonnegative: {name}')
        for key, value in context.requirements.items():
            patterns = (list(p for group in value.values() for p in group) if key == 'section_patterns'
                        else value if key.endswith('_patterns') else [value] if key.endswith('_pattern') else [])
            for pattern in patterns:
                re.compile(pattern)
        for pattern in context.requirements.get('clearance', {}).values():
            re.compile(pattern)
    return candidate


def _node_at(node, path):
    for key in path:
        if isinstance(node, MappingNode):
            node = next(value for name, value in node.value if name.value == str(key))
        else:
            node = node.value[key]
    return node


def _content_end(node, tokens):
    # Block collection end marks include following comments/whitespace. Leave
    # those untouched; flow containers must include their closing delimiter.
    if isinstance(node, ScalarNode) or node.flow_style:
        return node.end_mark.index
    return max((t.end_mark.index for t in tokens
                if node.start_mark.index <= t.start_mark.index < t.end_mark.index <= node.end_mark.index),
               default=node.end_mark.index)


def edit_value(loaded, path, value):
    """Patch one YAML value; leave text outside its span byte-for-byte intact."""
    if not path:
        raise ValueError('Select a setting, not the complete document')
    text = loaded.original.decode('utf-8')
    root = yaml.compose(text)
    try:
        node = _node_at(root, path)
    except StopIteration:
        # Add a profile skill or vocabulary entry by replacing its parent map.
        parent = loaded.data
        for key in path[:-1]:
            parent = parent[key]
        return edit_value(loaded, path[:-1], dict(parent, **{path[-1]: value}))
    tokens = list(yaml.scan(text))
    start, end = node.start_mark.index, _content_end(node, tokens)
    anchors = [t for t in tokens if isinstance(t, AnchorToken) and start <= t.start_mark.index < end]
    for anchor in anchors:
        if anchor.start_mark.index != start and any(isinstance(t, AliasToken) and t.value == anchor.value
                and not start <= t.start_mark.index < end for t in tokens):
            raise ValueError('This collection defines shared YAML anchors. Select an individual item to edit it safely.')
    anchor_prefix = f'&{anchors[0].value} ' if anchors and anchors[0].start_mark.index == start else ''
    # JSON scalar/flow syntax is valid YAML; it avoids implicit dates/booleans,
    # wraps complex values readably, and needs no new serialization dependency.
    rendered = anchor_prefix + json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2)
    column = node.start_mark.column
    if isinstance(node, (MappingNode, SequenceNode)) and not node.flow_style:
        # An indentless block sequence is legal YAML, but flow syntax needs an
        # indent under its mapping key. A fresh newline also handles alias owners.
        parent = _node_at(root, path[:-1])
        if isinstance(parent, MappingNode):
            key_node = next(k for k, v in parent.value if k.value == str(path[-1]))
            if node.start_mark.line > key_node.start_mark.line and column <= key_node.start_mark.column:
                rendered = '  ' + rendered
                column += 2
    rendered = rendered.replace('\n', '\n' + ' ' * column)
    return (text[:start] + rendered + text[end:]).encode('utf-8')


def make_preview(loaded, path, value):
    content = edit_value(loaded, path, value)
    candidate = validate_candidate(loaded, content)
    if candidate == loaded.data:
        raise ValueError('No values changed')
    # Semantic YAML diff avoids noise from comments, quote styles and anchors.
    before = yaml.safe_dump(loaded.data, sort_keys=False, allow_unicode=True)
    after = yaml.safe_dump(candidate, sort_keys=False, allow_unicode=True)
    diff = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                      fromfile=loaded.path.name + ' (current)',
                                      tofile=loaded.path.name + ' (proposed)'))
    return Preview(loaded, content, diff)


def save_preview(preview):
    loaded = preview.loaded
    validate_candidate(loaded, preview.content)

    def check_current():
        if any((loaded.path.parent / name).is_symlink() or
               (loaded.path.parent / name).read_bytes() != content for name, content in loaded.bundle.items()):
            raise ValueError('Config changed on disk since loading. Reload and preview again.')

    check_current()
    backups = loaded.path.parent.parent / 'data/outputs/config-backups'
    backups.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    backup = backups / f'{loaded.path.stem}.{stamp}.{uuid4().hex[:8]}.yml'
    with backup.open('xb') as stream:
        stream.write(loaded.original)
        stream.flush()
        os.fsync(stream.fileno())
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=loaded.path.parent, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(preview.content)
            stream.flush()
            os.fsync(stream.fileno())
        shutil.copymode(loaded.path, temporary)
        check_current()
        os.replace(temporary, loaded.path)
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
    return backup


def _select_setting(st, loaded, section):
    path, value = (section,), loaded.data[section]
    if loaded.path.name == 'profile.yml' and section == 'experience_years':
        return path, value
    while ((isinstance(value, dict) and value) or
           (isinstance(value, list) and value and not all(isinstance(v, str) for v in value))):
        key = 'select:' + loaded.path.name + repr(path)
        if isinstance(value, dict):
            options = list(value)
            if loaded.path.name == 'profile.yml' and path in (('skills',), ('atomic_skills',)):
                vocab = 'skills.yml' if path == ('skills',) else 'market_skills.yml'
                options += sorted(set(parse_yaml(loaded.bundle[vocab].decode('utf-8'))) - set(options))
            selected = st.sidebar.selectbox('Setting: ' + '.'.join(map(str, path)), options, key=key)
            value = value.get(selected, 0.0)
        else:
            # Structured lists retain the repo's rule/reference format.
            options = ['Whole list (YAML)'] + list(range(len(value)))
            selected = st.sidebar.selectbox('Item: ' + '.'.join(map(str, path)), options,
                index=1, key=key, format_func=lambda i, items=value: i if isinstance(i, str) else
                    str(items[i].get('id', items[i])) if isinstance(items[i], dict) else str(items[i]))
            if isinstance(selected, str):
                break
            value = value[selected]
        path += (selected,)
    return path, value


def main(config_dir=CONFIG_DIR):
    import streamlit as st

    st.set_page_config(page_title='SkillFreq config editor', layout='wide')
    st.title('SkillFreq config editor')
    filename = st.sidebar.selectbox('Config file', FILES)
    identity = (str(Path(config_dir).resolve()), filename)
    if st.session_state.get('config_identity') != identity:
        st.session_state.config_identity = identity
        st.session_state.pop('loaded_config', None)
        st.session_state.pop('config_preview', None)
    if st.sidebar.button('Reload / reset'):
        st.session_state.pop('loaded_config', None)
        st.session_state.pop('config_preview', None)
        st.session_state['edit_generation'] = st.session_state.get('edit_generation', 0) + 1
    try:
        if 'loaded_config' not in st.session_state:
            st.session_state.loaded_config = load_config(config_dir, filename)
        loaded = st.session_state.loaded_config
        st.caption(str(loaded.path))
        st.caption('Last modified: ' + datetime.fromtimestamp(loaded.path.stat().st_mtime).astimezone().isoformat(timespec='seconds'))
        if 'config_saved' in st.session_state:
            st.success(st.session_state.pop('config_saved'))
        section = st.sidebar.selectbox('Section', list(loaded.data))
        path, value = _select_setting(st, loaded, section)
        label = '.'.join(map(str, path))
        st.subheader(label)
        if filename == 'profile.yml':
            st.caption('Skill strengths express your evidence. Atomic technologies use 0–1; domain concepts are under skills. Existing entries can be set to 0, and vocabulary entries can be added.')
        with st.form('edit:' + repr((identity, path, st.session_state.get('edit_generation', 0)))):
            if filename == 'profile.yml' and path == ('experience_years',):
                draft = [st.number_input('Minimum experience (years)', value=value[0]),
                         st.number_input('Maximum experience (years)', value=value[1])]
            elif path == ('active_clearance',):
                draft = st.selectbox(label, [False, True, None], index=[False, True, None].index(value),
                                     format_func=lambda v: 'Unknown' if v is None else 'Yes' if v else 'No')
            elif isinstance(value, bool):
                draft = st.checkbox(label, value=value)
            elif isinstance(value, (int, float)):
                draft = st.number_input(label, value=value)
            elif isinstance(value, str):
                draft = st.text_input(label, value=value)
            elif isinstance(value, list) and all(isinstance(v, str) for v in value):
                draft = st.text_area('One item per line', '\n'.join(value), height=220)
            else:
                draft = st.text_area('Value (YAML)', yaml.safe_dump(value, sort_keys=False, allow_unicode=True), height=240)
            submitted = st.form_submit_button('Validate and preview')
        if submitted:
            st.session_state.pop('config_preview', None)
            try:
                if isinstance(value, list) and all(isinstance(v, str) for v in value):
                    draft = [line.strip() for line in draft.splitlines() if line.strip()]
                elif (isinstance(value, (dict, list)) or value is None) and isinstance(draft, str):
                    if path != ('active_clearance',):
                        draft = parse_yaml(draft)
                st.session_state.config_preview = make_preview(loaded, path, draft)
            except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError, re.error) as error:
                st.error(str(error))
        preview = st.session_state.get('config_preview')
        if preview:
            st.subheader('Validated changes')
            st.code(preview.diff, language='diff')
            st.caption('Save writes exactly this preview. Submit Validate and preview again to include further edits. No fields save automatically.')
            if st.button('Save validated changes', type='primary'):
                try:
                    backup = save_preview(preview)
                    st.session_state.config_saved = f'Saved {loaded.path}. Backup: {backup}'
                    st.session_state.pop('loaded_config', None)
                    st.session_state.pop('config_preview', None)
                    st.session_state['edit_generation'] = st.session_state.get('edit_generation', 0) + 1
                    st.rerun()
                except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError, re.error) as error:
                    st.error(str(error))
        with st.expander('Current YAML (read only)'):
            st.code(loaded.original.decode('utf-8'), language='yaml')
    except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError) as error:
        st.error(f'Cannot load config: {error}')


if __name__ == '__main__':
    main()
