#!/usr/bin/env python3
"""Compare two safe runtime JSON snapshots; exit 2 when differences found."""
import argparse
import json
from pathlib import Path


def compare(old: dict, new: dict) -> dict:
    left = {p['name'].lower(): p['version'] for p in old.get('python_packages', {}).get('packages', [])}
    right = {p['name'].lower(): p['version'] for p in new.get('python_packages', {}).get('packages', [])}
    added = {k: right[k] for k in sorted(right.keys() - left.keys())}
    removed = {k: left[k] for k in sorted(left.keys() - right.keys())}
    updated = {k: {'old': left[k], 'new': right[k]} for k in sorted(left.keys() & right.keys()) if left[k] != right[k]}
    before = old.get('executables', {})
    after = new.get('executables', {})
    tools = {k: {'old': before.get(k), 'new': after.get(k)}
             for k in sorted(before.keys() | after.keys()) if before.get(k) != after.get(k)}
    changes = {'added_packages': added, 'removed_packages': removed,
               'updated_packages': updated, 'changed_executables': tools}
    return {'changed': any(changes.values()), 'changes': changes}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('old')
    p.add_argument('new')
    p.add_argument('--output')
    p.add_argument('--no-fail-on-change', action='store_true')
    a = p.parse_args()
    result = compare(json.loads(Path(a.old).read_text()), json.loads(Path(a.new).read_text()))
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.output:
        Path(a.output).write_text(text)
    else:
        print(text)
    return 0 if a.no_fail_on_change or not result['changed'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
