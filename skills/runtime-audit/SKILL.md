---
name: runtime-audit
description: >
  Safely inventory a Linux execution environment, including OS, cgroup limits,
  interpreters, packages, executables and test evidence; produce reproducible
  JSON without leaking credentials. Use for environment capability audits,
  preflight inspections and reproducibility checks.
---

# Runtime Audit — Evidence-first Linux environment inventory

## Objective
Produce a scope-bounded, provenance-aware snapshot rather than claim an impossible audit of every host layer. Separate **installed**, **on PATH**, **importable**, **smoke-tested**, and **externally connected**.

## Workflow
1. **Scope** — identify the current container, execution timestamp, file system boundaries, user context, and intended publication visibility.
2. **Privacy gate** — prohibit reading or exporting credentials, token values, cookies, browser profiles, private keys, arbitrary `$HOME` trees and private connector resources. No automated publication without a review gate.
3. **Enumerate** — detect OS/architecture, cgroup CPU/memory, mounted storage size, interpreters, `pip`/system packages and executable presence. Record authoritative source and collection errors.
4. **Validate** — cross-check record counts, versions, hashes and formats. `pip check` errors are first-class observations, not hidden.
5. **Test** — run minimal non-destructive smoke tests for software relevant to the request; differentiate successful import from real execution.
6. **Analyze** — classify risks, compatibility gaps, capability constraints and confidence level. Avoid extrapolating host hardware from container CPU views.
7. **Deliver** — export machine-readable JSON, an interpretation report, environment deltas and a redacted public catalog. Maintain local-only artifacts separately.
8. **Review** — ensure every reported total comes from a reproducible list and every assertion names its measurement boundary.

## Command
```bash
python skills/runtime-audit/scripts/audit_runtime.py --output snapshot.json
python -m json.tool snapshot.json > /dev/null
```

The script uses only Python stdlib. It does not inspect credential files or export environment variable values, and does not send anything over the network.

## Evidence levels
- **Observed**: command return value or file content exists in this container.
- **Validated**: independently cross-checked counts/versions or test passed.
- **Declared**: external registry/tool advertises capability; authorization not tested.
- **Unknown**: out of scope, not reachable, or untested.

## Exit criteria
Schema-valid JSON, a clear capture timestamp, explicit scope, recorded partial failures, proof that secrets were not deliberately collected, and a separate local/manual publication decision.

See `references/evidence-policy.md` and `references/publication-safety.md`.
