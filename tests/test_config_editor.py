"""Config editor tests only write temporary copies, never the live configs."""
import copy
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
import yaml

from scripts.config_editor import (
    FILES, edit_value, load_config, make_preview, parse_yaml, save_preview, validate_candidate,
)
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
        self.assertIn(' experience_years:', preview.diff)
        self.assertIn('-- 3', preview.diff)
        self.assertIn('+- 5', preview.diff)
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


if __name__ == '__main__':
    unittest.main()
