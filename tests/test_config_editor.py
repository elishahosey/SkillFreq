"""Config editor tests only write temporary copies, never the live configs."""
import copy
import os
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
import yaml

from scripts.config_editor import (
    FILES, Preview, edit_value, load_config, make_preview, make_changes_preview,
    parse_yaml, save_preview, semantic_diff, validate_candidate,
)
from scripts.config_editor_views import search_settings, settings_catalog, VIEWS, GUIDANCE, ISSUE_CHEAT_SHEET
from skillfreq import configuration
from skillfreq.configuration import CONFIG_DIR


class ConfigEditorTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / 'configs'
        self.directory.mkdir()
        for name in FILES:
            shutil.copyfile(CONFIG_DIR / name, self.directory / name)
        self.originals = {name: (self.directory / name).read_bytes() for name in FILES}

    def load(self, name='profile.yml'):
        return load_config(self.directory, name)

    def test_loads_existing_bundle_and_restricts_paths(self):
        loaded = self.load()
        self.assertEqual(loaded.data['experience_years'], [3, 4])
        self.assertEqual(set(loaded.bundle), set(FILES))
        self.assertEqual(loaded.original, self.originals['profile.yml'])
        with self.assertRaises(ValueError):
            load_config(self.directory, '../profile.yml')

    def test_supported_edits_validate_without_writing(self):
        for name, path, value in (
                ('profile.yml', ('experience_years',), [4, 5]),
                ('profile.yml', ('atomic_skills', 'AWS'), 0.7),
                ('profile.yml', ('active_clearance',), None),
                ('roles.yml', ('lane_rules', 0, 'weight'), 41),
                ('requirements.yml', ('lead_title_terms',), ['lead', 'principal']),
                ('requirements.yml', ('equivalences',), {'Airflow': {'capability_concepts': ['etl']}}),
                ('weights.yml', ('fit', 'rules', 0, 'actions', 0, 'value'), 4),
                ('market_skills.yml', ('Kotlin',), ['kotlin', 'kotlin jvm']),
                ('skills.yml', ('ci_cd', 'terms'), ['ci/cd', 'continuous integration'])):
            with self.subTest(name=name, path=path):
                preview = make_preview(self.load(name), path, value)
                self.assertTrue(preview.diff)
                self.assertNotEqual(preview.content, self.originals[name])
                self.assertEqual((self.directory / name).read_bytes(), self.originals[name])

    def test_can_add_known_atomic_and_domain_strengths(self):
        for path in (('atomic_skills', 'Java'), ('skills', 'healthcare_supply_chain')):
            preview = make_preview(self.load(), path, 0.6)
            self.assertEqual(parse_yaml(preview.content)[path[0]][path[1]], 0.6)

    def test_invalid_yaml_structure_types_and_ranges_are_rejected(self):
        loaded = self.load()
        for content in (b'[]', b'skills: [', b'skills: {}', b'skills: {}\nskills: {}'):
            with self.subTest(content=content), self.assertRaises((ValueError, yaml.YAMLError)):
                validate_candidate(loaded, content)
        for path, value in ((('experience_years',), [8, 3]), (('experience_years',), 'three'),
                            (('skills', 'sql'), 'strong'), (('skills', 'sql'), True),
                            (('atomic_skills', 'AWS'), 2), (('active_clearance',), 'yes')):
            with self.subTest(path=path, value=value), self.assertRaises(ValueError):
                make_preview(loaded, path, value)
        with self.assertRaises(ValueError):
            make_preview(loaded, ('atomic_skills', 'Unknown tool'), 0.5)
        with self.assertRaises((ValueError, re.error)):
            make_preview(self.load('requirements.yml'), ('ownership_patterns',), ['[invalid'])
        with self.assertRaises(ValueError):
            make_preview(self.load('weights.yml'), ('alignment', 'years_penalties'), [['7', -3]])

    def test_known_lane_and_rule_keys_cannot_disappear(self):
        loaded = self.load('roles.yml')
        rules = copy.deepcopy(loaded.data['lane_rules'])
        with self.assertRaises(ValueError):
            make_preview(loaded, ('lane_rules',), rules[1:])
        del rules[0]['lane']
        with self.assertRaises(ValueError):
            make_preview(loaded, ('lane_rules',), rules)
        loaded = self.load('weights.yml')
        with self.assertRaises(ValueError):
            make_preview(loaded, ('fit', 'lane_caps'), {'target_lane': 100})

    def test_diff_and_local_text_preservation(self):
        loaded = self.load()
        preview = make_preview(loaded, ('experience_years',), [4, 5])
        self.assertIn('profile.yml (current)', preview.diff)
        self.assertIn('-experience_years: [3, 4]', preview.diff)
        self.assertEqual(preview.changes, ['profile.experience_years: [3, 4] -> [4, 5]'])
        self.assertTrue(preview.content.startswith(b'# Candidate-confirmed'))
        self.assertEqual(preview.content.split(b'active_clearance:', 1)[1],
                         loaded.original.split(b'active_clearance:', 1)[1])
        # Block-list trailing comments belong to the next setting, not the edit.
        loaded = self.load('requirements.yml')
        content = edit_value(loaded, ('explicit_years_patterns',), ['experience required: (\\d+)'])
        self.assertIn(b'# Explicit, candidate-approved equivalents only.', content)
        with self.assertRaisesRegex(ValueError, 'No values changed'):
            make_preview(self.load(), ('active_clearance',), False)

    def test_alias_owner_edits_remain_valid_and_visible(self):
        loaded = self.load('roles.yml')
        # The real term-group list has aliases; replacing its last alias must
        # consume the alias token, not the end mark of its earlier definition.
        path = ('term_groups', 'alignment.no_experience')
        preview = make_preview(loaded, path, ['no prior experience', 'entry level'])
        self.assertEqual(parse_yaml(preview.content)['term_groups']['alignment.no_experience'],
                         ['no prior experience', 'entry level'])

    def test_backup_is_exact_and_save_only_changes_selected_file(self):
        loaded = self.load()
        preview = make_preview(loaded, ('experience_years',), [4, 5])
        backup = save_preview(preview)
        self.assertEqual(backup.read_bytes(), self.originals['profile.yml'])
        self.assertRegex(backup.name, r'profile\.\d{8}T\d{6}\.\d{6}Z\.[a-f0-9]{8}\.yml')
        self.assertEqual(loaded.path.read_bytes(), preview.content)
        for name in FILES[1:]:
            self.assertEqual((self.directory / name).read_bytes(), self.originals[name])
        next_preview = make_preview(self.load(), ('experience_years',), [5, 6])
        self.assertNotEqual(save_preview(next_preview), backup)
        self.assertEqual(backup.read_bytes(), self.originals['profile.yml'])

    def test_external_change_in_any_config_refuses_stale_preview(self):
        preview = make_preview(self.load(), ('experience_years',), [4, 5])
        other = self.directory / 'requirements.yml'
        other.write_bytes(other.read_bytes() + b'\n# edited elsewhere\n')
        with self.assertRaisesRegex(ValueError, 'changed on disk'):
            save_preview(preview)
        self.assertEqual((self.directory / 'profile.yml').read_bytes(), self.originals['profile.yml'])
        self.assertFalse((self.directory.parent / 'data/outputs/config-backups').exists())

    def test_failed_backup_or_replace_keeps_original_and_cleans_temp(self):
        preview = make_preview(self.load(), ('experience_years',), [4, 5])
        with patch('scripts.config_editor.os.fsync', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                save_preview(preview)
        self.assertEqual(preview.loaded.path.read_bytes(), preview.loaded.original)
        with patch('scripts.config_editor.os.replace', side_effect=PermissionError('locked')):
            with self.assertRaises(PermissionError):
                save_preview(preview)
        self.assertEqual(preview.loaded.path.read_bytes(), preview.loaded.original)
        self.assertFalse(list(self.directory.glob('*.tmp')))
        backups = list((self.directory.parent / 'data/outputs/config-backups').glob('*.yml'))
        self.assertTrue(any(p.read_bytes() == preview.loaded.original for p in backups))

    def test_ui_preview_explicit_save_and_reset_on_temp_configs(self):
        app = AppTest.from_string('from pathlib import Path\nfrom scripts.config_editor import main\n'
                                 f'main(Path({str(self.directory)!r}))', default_timeout=20).run()
        self.assertFalse(app.exception)
        # Initial selection exposes the candidate minimum and maximum together.
        app.number_input[0].set_value(4).run()
        self.assertEqual((self.directory / 'profile.yml').read_bytes(), self.originals['profile.yml'])
        next(b for b in app.button if b.label == 'Validate and preview').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertTrue(any(c.language == 'diff' for c in app.code))
        self.assertEqual((self.directory / 'profile.yml').read_bytes(), self.originals['profile.yml'])
        next(b for b in app.button if b.label == 'Save validated changes').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertTrue(app.success)
        self.assertEqual(self.load().data['experience_years'], [4, 4])
        app.number_input[0].set_value(9).run()
        next(b for b in app.button if b.label == 'Validate and preview').click().run()
        self.assertTrue(app.error)
        self.assertFalse(any(b.label == 'Save validated changes' for b in app.button))
        next(b for b in app.button if b.label == 'Reload / reset').click().run()
        self.assertEqual(app.number_input[0].value, 4)

    def test_search_ownership_and_related_profile_fields(self):
        entries = settings_catalog(self.load().bundle)
        terraform = search_settings(entries, 'Terraform')[0]
        self.assertEqual(terraform.file, 'profile.yml')
        self.assertEqual(terraform.value['atomic_skills'], 0)
        self.assertEqual(terraform.value['growth_paths']['priority'], 0.35)
        self.assertIn('azure', terraform.value['growth_paths']['adjacent_concepts'])
        for query, filename, kind in (
            ('network architecture', 'skills.yml', 'concept'),
            ('integration engineer', 'roles.yml', 'text'),
            ('target_lane', 'roles.yml', 'lane'),
            ('principal', 'requirements.yml', 'seniority'),
            ('clearance', 'requirements.yml', 'advanced'),
            ('experience_gap', 'weights.yml', 'advanced'),
            ('resume evidence', 'resume_signal.yml', 'advanced'),
        ):
            with self.subTest(query=query):
                self.assertTrue(any(e.file == filename and e.kind == kind for e in search_settings(entries, query)))

    def test_multi_field_growth_edit_and_concise_diff(self):
        loaded = self.load()
        preview = make_changes_preview(loaded, [
            (('growth_paths', 'Terraform', 'priority'), 0.5),
            (('growth_paths', 'Terraform', 'adjacent_concepts'), ['azure', 'systems', 'aws']),
            (('atomic_skills', 'Terraform'), 0),
        ])
        self.assertEqual(preview.changes, [
            'profile.growth_paths.Terraform.priority: 0.35 -> 0.5',
            'profile.growth_paths.Terraform.adjacent_concepts: + "aws"',
        ])
        self.assertEqual(parse_yaml(preview.content)['growth_paths']['Terraform']['priority'], 0.5)
        self.assertEqual(loaded.path.read_bytes(), loaded.original)
        preview = make_preview(self.load('skills.yml'), ('network_architecture', 'terms'),
                               ['networking architecture', 'network architecture', 'network topology'])
        self.assertEqual(preview.changes, ['skills.network_architecture.terms: + "network topology"'])
        self.assertEqual(semantic_diff({'a': 1}, {'a': 1}, 'profile'), [])
        self.assertTrue(semantic_diff(['a', 'b'], ['b', 'a'], 'terms'))

    def test_reuses_repo_validators_and_rejects_broken_references(self):
        with patch('skillfreq.score.grading.load_roles', wraps=configuration.load_roles) as roles, \
             patch('skillfreq.configuration.validate_grading_settings', wraps=configuration.validate_grading_settings) as grading, \
             patch('scripts.config_editor.resolve_terms', wraps=configuration.resolve_terms) as refs:
            make_preview(self.load(), ('experience_years',), [3, 5])
            roles.assert_called_once()
            grading.assert_called_once()
            self.assertTrue(refs.called)
        for name, path, value in (
            ('roles.yml', ('lane_rules', 0, 'lane'), 'imaginary_lane'),
            ('roles.yml', ('lane_rules', 0, 'scope'), 'imaginary_scope'),
            ('roles.yml', ('lane_rules', 0, 'max_hits'), 0),
            ('roles.yml', ('term_groups', 'alignment.no_experience'), [{'seniority': 'imaginary'}]),
            ('skills.yml', ('sql', 'term_refs'), [['python', 'imaginary']]),
            ('resume_signal.yml', ('python', 'aliases'), [{'concept_term': ['python', 'imaginary']}]),
            ('requirements.yml', ('seniority_levels', 'senior', 'rank'), -1),
            ('requirements.yml', ('maximum_experience_years',), 0),
        ):
            with self.subTest(path=path), self.assertRaises((ValueError, KeyError)):
                make_preview(self.load(name), path, value)
        rules = copy.deepcopy(self.load('roles.yml').data['lane_rules'])
        rules.append(copy.deepcopy(rules[0]))
        with self.assertRaises(ValueError):
            make_preview(self.load('roles.yml'), ('lane_rules',), rules)

    def test_backup_exists_before_replace_and_invalid_preview_cannot_write(self):
        loaded = self.load()
        invalid = Preview(loaded, edit_value(loaded, ('experience_years',), [9, 2]), '')
        with self.assertRaises(ValueError):
            save_preview(invalid)
        backup_dir = self.directory.parent / 'data/outputs/config-backups'
        self.assertFalse(backup_dir.exists())
        self.assertEqual(loaded.path.read_bytes(), loaded.original)
        replace = os.replace

        def checked_replace(source, target):
            backups = list(backup_dir.glob('*.yml'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), loaded.original)
            self.assertEqual(loaded.path.read_bytes(), loaded.original)
            replace(source, target)

        with patch('scripts.config_editor.os.replace', side_effect=checked_replace):
            save_preview(make_preview(loaded, ('experience_years',), [3, 5]))

    def test_ui_terraform_search_edit_preview_and_save(self):
        app = AppTest.from_string('from pathlib import Path\nfrom scripts.config_editor import main\n'
                                 f'main(Path({str(self.directory)!r}))', default_timeout=25).run()
        app.text_input[0].set_value('Terraform').run()
        self.assertFalse(app.exception)
        self.assertEqual(app.number_input[1].label, 'Growth priority')
        self.assertEqual(app.number_input[1].value, 0.35)
        app.number_input[1].set_value(0.5)
        app.multiselect[0].select('aws')
        next(b for b in app.button if b.label == 'Validate and preview').click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        summary = next(c.value for c in app.code if c.language == 'text')
        self.assertIn('profile.growth_paths.Terraform.priority: 0.35 -> 0.5', summary)
        self.assertIn('adjacent_concepts: + "aws"', summary)
        self.assertNotIn('atomic_skills', summary)
        self.assertEqual(self.load().original, self.originals['profile.yml'])
        next(b for b in app.button if b.label == 'Save validated changes').click().run()
        self.assertFalse(app.error)
        growth = self.load().data['growth_paths']['Terraform']
        self.assertEqual(growth, {'priority': 0.5, 'adjacent_concepts': ['azure', 'systems', 'aws']})

    def test_ui_views_render_and_advanced_policy_is_opt_in(self):
        app = AppTest.from_string('from pathlib import Path\nfrom scripts.config_editor import main\n'
                                 f'main(Path({str(self.directory)!r}))', default_timeout=25).run()
        self.assertTrue(any(m.value == ISSUE_CHEAT_SHEET.strip() for m in app.markdown))
        self.assertTrue(any(c.value == GUIDANCE['profile.yml'] for c in app.caption))
        guidance_views = {'Profile': 'profile.yml', 'Skills / Vocabulary': 'skills.yml',
                          'Role Lanes': 'roles.yml',
                          'Seniority / Requirements / Hard Filters': 'requirements.yml'}
        for view in VIEWS[1:]:
            app.radio[0].set_value(view).run()
            self.assertFalse(app.exception, view)
            self.assertFalse(app.error, view)
            self.assertTrue(any(m.value == ISSUE_CHEAT_SHEET.strip() for m in app.markdown), view)
            if view in guidance_views:
                self.assertTrue(any(c.value == GUIDANCE[guidance_views[view]] for c in app.caption), view)
        app.radio[0].set_value('Quick Edit').run()
        app.text_input[0].set_value('preferred_patterns').run()
        self.assertFalse(any(b.label == 'Validate and preview' for b in app.button))
        next(c for c in app.checkbox if c.label == 'Open in Advanced').check().run()
        self.assertTrue(any(b.label == 'Validate and preview' for b in app.button))


if __name__ == '__main__':
    unittest.main()
