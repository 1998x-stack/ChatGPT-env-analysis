# Severity guide

- Critical: a required executable disappears or a secret is exposed in a publication artifact.
- High: a critical compatibility dependency changes, CPU/GPU availability changes, or a required test fails.
- Medium: compatible package upgrades, altered CLI presence, changed export capabilities.
- Low: noncritical build metadata or harmless test environment drift.

Severity is task-dependent; never infer breakage solely from a version number.
