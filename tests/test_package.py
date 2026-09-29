import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import secrets
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT / 'tools/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PluginPackageTest(unittest.TestCase):
    def test_reproducible_bundles_are_complete_and_exclude_unlisted_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'package'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('dist', '__pycache__'))
            secret = secrets.token_hex(24)
            (root / build.PLUGIN / '.env').write_text('SECRET=' + secret)
            (root / build.PLUGIN / 'debug.log').write_text('Private diagnostic data')
            artifacts = build.artifacts(root)
            self.assertEqual(artifacts, build.artifacts(root))
            with zipfile.ZipFile(io.BytesIO(artifacts['sendery-plugin.zip'])) as bundle:
                self.assertEqual(set(build.PLUGIN_FILES), set(bundle.namelist()))
                self.assertIn('https://sendery.co/mcp', bundle.read('.mcp.json').decode())
            with zipfile.ZipFile(io.BytesIO(artifacts['sendery-marketplace.zip'])) as bundle:
                self.assertIn('sendery-plugin/.agents/plugins/marketplace.json', bundle.namelist())
                self.assertIn('sendery-plugin/.claude-plugin/marketplace.json', bundle.namelist())
            for data in artifacts.values():
                with zipfile.ZipFile(io.BytesIO(data)) as bundle:
                    for name in bundle.namelist():
                        self.assertNotIn('..', Path(name).parts)
                        self.assertNotIn('.env', Path(name).parts)
                        self.assertNotIn(secret.encode(), bundle.read(name))

    def test_manifests_and_marketplaces_resolve_the_same_plugin(self):
        self.assertRegex(build.validate(), r'^\d+\.\d+\.\d+$')
        for name in ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            manifest = build.read_json(ROOT / build.PLUGIN, name)
            self.assertEqual('https://github.com/sendery-co/sendery-plugin', manifest['repository'])
        with zipfile.ZipFile(io.BytesIO(build.artifacts()['sendery-skill.zip'])) as bundle:
            self.assertEqual((ROOT / build.PLUGIN / 'skills/sendery-onboarding/SKILL.md').read_bytes(), bundle.read('sendery-onboarding/SKILL.md'))

    def test_missing_assets_symlinks_and_embedded_credentials_fail_release(self):
        for issue in ('missing', 'symlink', 'credentials'):
            with self.subTest(issue=issue), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / 'package'
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('dist', '__pycache__'))
                icon = root / build.PLUGIN / 'assets/icon.svg'
                if issue == 'missing':
                    icon.unlink()
                elif issue == 'symlink':
                    icon.unlink()
                    icon.symlink_to(ROOT / build.PLUGIN / 'assets/icon.svg')
                else:
                    path = root / build.PLUGIN / '.mcp.json'
                    data = json.loads(path.read_text())
                    data['mcpServers']['sendery']['headers'] = {'Authorization': 'Bearer private'}
                    path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    build.artifacts(root)

    def test_marketplace_archive_builds_without_the_application_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            with zipfile.ZipFile(io.BytesIO(build.artifacts()['sendery-marketplace.zip'])) as bundle:
                bundle.extractall(directory)
            self.assertEqual(build.artifacts(), build.artifacts(Path(directory) / 'sendery-plugin'))


if __name__ == '__main__':
    unittest.main()
