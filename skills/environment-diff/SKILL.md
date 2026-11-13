---
name: environment-diff
description: >
  Compare two environment audit JSON snapshots, identify package additions,
  removals, upgrades, and executable status changes with reproducible evidence.
  Use for image upgrades, regression triage and toolchain drift alerts.
---

# Environment Diff — Reproducibility gate

## Steps
1. Obtain two safe JSON snapshots created by the Runtime Audit skill.
2. Check schema compatibility and timestamp order; highlight unsupported fields.
3. Compare normalized package names and versions. Report added, removed, upgraded, downgraded packages (version ordering may be ambiguous for non-PEP440 versions; do not overinterpret).
4. Compare command availability without interpreting an off-PATH result as an uninstall.
5. Flag important drifts in major language runtimes, PDF/Office toolchain, headless browsers and ML dependencies.
6. Store a machine-readable delta; optionally fail CI with code `2` when changes are found.

## Run
```bash
python skills/environment-diff/scripts/compare_snapshots.py old.json new.json --output diff.json
# Add --no-fail-on-change for informational reports.
```

This tool is read-only and uses Python stdlib only.
