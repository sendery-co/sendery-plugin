#!/usr/bin/env python3
"""Build reproducible public plugin archives from an explicit file allowlist."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('plugins/sendery')
PLUGIN_FILES = (
    '.claude-plugin/plugin.json', '.codex-plugin/plugin.json', '.mcp.json',
    'skills/sendery-onboarding/SKILL.md', 'assets/icon.svg', 'assets/logo.png',
    'LICENSE', 'README.md',
)
REPOSITORY_FILES = (
    '.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json',
    '.github/workflows/check.yml', '.github/workflows/release.yml', '.gitignore',
    'README.md', 'PUBLISHING.md', 'CHANGELOG.md', 'LICENSE',
    'tools/build.py', 'tests/test_package.py',
)


def read_json(root, name):
    return json.loads((root / name).read_text())


def validate(root=ROOT):
    for name in (*REPOSITORY_FILES, *(str(PLUGIN / name) for name in PLUGIN_FILES)):
        path = root / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Missing or unsafe release file: {name}')
    codex = read_json(root / PLUGIN, '.codex-plugin/plugin.json')
    claude = read_json(root / PLUGIN, '.claude-plugin/plugin.json')
    for field in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'skills', 'mcpServers'):
        if not codex.get(field) or codex[field] != claude.get(field):
            raise ValueError(f'Plugin manifests disagree on {field}')
    if codex['name'] != 'sendery' or not re.fullmatch(r'\d+\.\d+\.\d+', codex['version']):
        raise ValueError('Use the sendery name and a stable semantic version')
    if codex['skills'] != './skills/' or codex['mcpServers'] != './.mcp.json':
        raise ValueError('Plugin component paths must stay inside the bundle')
    if codex['license'] != 'MIT':
        raise ValueError('Plugin license must match the included MIT license')
    interface = codex['interface']
    for field in ('displayName', 'shortDescription', 'longDescription', 'developerName', 'category'):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            raise ValueError(f'Missing presentation field: {field}')
    for field in ('websiteURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        if not interface[field].startswith('https://sendery.co'):
            raise ValueError(f'Unexpected listing URL: {field}')
    for field in ('composerIcon', 'logo'):
        if interface[field] not in ('./assets/icon.svg', './assets/logo.png'):
            raise ValueError(f'Unbundled image: {field}')
    prompts = interface['defaultPrompt']
    if not 1 <= len(prompts) <= 3 or any(not isinstance(p, str) or len(p) > 128 for p in prompts):
        raise ValueError('Use one to three short starter prompts')
    mcp = read_json(root / PLUGIN, '.mcp.json')
    if mcp != {'mcpServers': {'sendery': {'type': 'http', 'url': 'https://sendery.co/mcp'}}}:
        raise ValueError('Only the production OAuth MCP endpoint belongs in the public package; no credentials or local commands')
    for name, source in (
        ('.agents/plugins/marketplace.json', {'source': 'local', 'path': './plugins/sendery'}),
        ('.claude-plugin/marketplace.json', './plugins/sendery'),
    ):
        market = read_json(root, name)
        if market['name'] != 'sendery' or len(market['plugins']) != 1 or market['plugins'][0]['name'] != 'sendery' or market['plugins'][0]['source'] != source:
            raise ValueError(f'Invalid marketplace reference: {name}')
    entry = read_json(root, '.agents/plugins/marketplace.json')['plugins'][0]
    if entry['policy'] != {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'} or not entry['category']:
        raise ValueError('Marketplace must request authentication on install')
    skill = (root / PLUGIN / 'skills/sendery-onboarding/SKILL.md').read_text()
    if not skill.startswith('---\nname: sendery-onboarding\n') or 'description:' not in skill.split('---', 2)[1]:
        raise ValueError('Missing skill frontmatter')
    if '[TODO:' in json.dumps(codex) or '[TODO:' in skill:
        raise ValueError('Unfinished release metadata')
    return codex['version']


def archive(root, files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for target, source in sorted(files.items()):
            path = root / source
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f'Unsafe archive source: {source}')
            info = zipfile.ZipInfo(target, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
    return output.getvalue()


def artifacts(root=ROOT):
    validate(root)
    plugin = {name: str(PLUGIN / name) for name in PLUGIN_FILES}
    repo = {f'sendery-plugin/{name}': name for name in REPOSITORY_FILES}
    repo.update({f'sendery-plugin/{PLUGIN}/{name}': str(PLUGIN / name) for name in PLUGIN_FILES})
    skill = {'sendery-onboarding/SKILL.md': str(PLUGIN / 'skills/sendery-onboarding/SKILL.md'), 'sendery-onboarding/LICENSE': str(PLUGIN / 'LICENSE')}
    return {'sendery-plugin.zip': archive(root, plugin), 'sendery-marketplace.zip': archive(root, repo), 'sendery-skill.zip': archive(root, skill)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--check', action='store_true', help='Check committed downloads instead of writing them.')
    args = parser.parse_args()
    built = artifacts()
    checksums = ''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n' for name, data in sorted(built.items())).encode()
    built['SHA256SUMS'] = checksums
    if args.check:
        for name, data in built.items():
            path = args.output / name
            if not path.is_file() or path.read_bytes() != data:
                parser.error(f'Rebuild stale or missing artifact: {path}')
        print('Release archives match the source files.')
    else:
        args.output.mkdir(parents=True, exist_ok=True)
        for name, data in built.items():
            (args.output / name).write_bytes(data)
        print(f'Built Sendery {validate()} in {args.output}')


if __name__ == '__main__':
    main()
