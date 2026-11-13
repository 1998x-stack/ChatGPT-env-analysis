#!/usr/bin/env python3
"""Index local SKILL.md paths and optional ChatGPT plugin skill URI registry."""
import argparse
import csv
import json
from pathlib import Path


def collect(local_root: Path, registry: Path | None) -> list[dict]:
    items = []
    if local_root.is_dir():
        for path in sorted(local_root.glob('*/SKILL.md')):
            # Only direct subfolders; avoids exposing internal asset contents.
            items.append({'name': path.parent.name, 'kind': 'local',
                          'reference': str(path), 'source': 'filesystem', 'content_mirrored': False})
    if registry and registry.is_file():
        with registry.open(newline='', encoding='utf-8') as fh:
            for row in csv.DictReader(fh, delimiter='\t'):
                uri = row.get('skill_uri', '').strip()
                if uri.startswith('skills://plugins/'):
                    items.append({'name': uri.split('/')[-1], 'kind': 'plugin',
                                  'reference': uri, 'source': 'registry-export', 'content_mirrored': False})
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-root', default='/home/oai/skills')
    parser.add_argument('--registry', default='')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    records = collect(Path(args.local_root), Path(args.registry) if args.registry else None)
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({'schema_version': '1.0', 'entries': records}, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(records)} skill entries -> {dest}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
