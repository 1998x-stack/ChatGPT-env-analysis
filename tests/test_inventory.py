"""stdlib-based tests: no external package downloads needed."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class AuditTests(unittest.TestCase):
    def test_safe_inventory_contract(self):
        mod = load(ROOT/'skills/runtime-audit/scripts/audit_runtime.py', 'runtime')
        item = mod.collect()
        self.assertFalse(item['privacy']['env_var_values_exported'])
        self.assertIn('platform', item)
        self.assertIn('python_packages', item)
        self.assertNotIn('environment', item)

    def test_skill_registry(self):
        mod = load(ROOT/'skills/skill-inventory/scripts/catalog_skills.py', 'skills')
        with tempfile.TemporaryDirectory() as td:
            base = Path(td); (base/'alpha').mkdir(); (base/'alpha/SKILL.md').write_text('---\nname: alpha\n---')
            items = mod.collect(base, None)
            self.assertEqual(len(items), 1)
            self.assertFalse(items[0]['content_mirrored'])

    def test_snapshot_diff(self):
        mod = load(ROOT/'skills/environment-diff/scripts/compare_snapshots.py', 'delta')
        old = {'python_packages': {'packages': [{'name':'pandas','version':'2.2'}]}, 'executables': {'git': True}}
        new = {'python_packages': {'packages': [{'name':'pandas','version':'3.0'}]}, 'executables': {'git': True}}
        d = mod.compare(old, new)
        self.assertTrue(d['changed'])
        self.assertEqual(d['changes']['updated_packages']['pandas']['new'], '3.0')

    def test_published_dataset_safety(self):
        data = json.loads((ROOT/'docs/data/catalog.json').read_text())
        self.assertEqual(len(data['skills']), 36)
        self.assertEqual(sum(x['count'] for x in data['tool_groups']), 242)
        self.assertTrue(all('secret' not in k.lower() for k in data.keys()))

if __name__ == '__main__':
    unittest.main()
