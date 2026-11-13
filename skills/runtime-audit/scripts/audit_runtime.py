#!/usr/bin/env python3
"""Safe, dependency-free Linux runtime inventory. Never exports environment variable values."""
from __future__ import annotations
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = ['python', 'python3', 'pip', 'uv', 'node', 'npm', 'git', 'go', 'java', 'gcc', 'g++',
         'clang', 'ffmpeg', 'magick', 'convert', 'libreoffice', 'pandoc', 'tesseract',
         'chromium', 'google-chrome', 'xelatex', 'lualatex', 'pdflatex', 'docker', 'podman', 'gh']
SCHEMA = 'https://github.com/1998x-stack/ChatGPT-env-analysis/blob/main/docs/data-dictionary.md'

def run(args: list[str], timeout: int = 20) -> dict:
    try:
        p = subprocess.run(args, text=True, capture_output=True, timeout=timeout, check=False)
        return {'status': 'pass' if p.returncode == 0 else 'fail', 'exit_code': p.returncode,
                'stdout': p.stdout[:4000].strip(), 'stderr_present': bool(p.stderr)}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'status': 'unavailable', 'error_type': type(e).__name__}

def cgroup(path: str) -> str | None:
    try:
        return Path(path).read_text().strip()
    except (OSError, UnicodeError):
        return None

def collect() -> dict:
    pkg = run([sys.executable, '-m', 'pip', 'list', '--format=json'])
    if pkg['status'] == 'pass':
        try:
            pkg['packages'] = json.loads(pkg.pop('stdout'))
        except ValueError:
            pkg['status'] = 'parse_error'
    result = {
        'schema_version': '1.0', 'collected_at_utc': datetime.now(timezone.utc).isoformat(),
        'source': 'local-python-stdlib', 'scope': 'current-process-container',
        'platform': {'system': platform.system(), 'machine': platform.machine(),
                     'release': platform.release(), 'python': platform.python_version(),
                     'executable': Path(sys.executable).name},
        'resources': {'cpu_count_reported': os.cpu_count(),
                      'cpu_cgroup_quota_period': cgroup('/sys/fs/cgroup/cpu.max'),
                      'memory_cgroup_max_bytes': cgroup('/sys/fs/cgroup/memory.max'),
                      'pids_cgroup_max': cgroup('/sys/fs/cgroup/pids.max')},
        'executables': {name: bool(shutil.which(name)) for name in TOOLS},
        'python_packages': pkg,
        'package_health': run([sys.executable, '-m', 'pip', 'check']),
        'privacy': {'env_var_values_exported': False, 'secret_files_read': False,
                    'home_tree_scanned': False, 'external_network_tested': False},
        'limitations': ['This snapshot covers only the current execution environment.',
                        'Connector availability and authorization cannot be inferred from filesystem or pip.',
                        'Missing executable on PATH does not prove absence everywhere on disk.'],
        'schema': SCHEMA,
    }
    return result

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, help='JSON path to create')
    args = p.parse_args()
    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(collect(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote safe inventory: {dst}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
