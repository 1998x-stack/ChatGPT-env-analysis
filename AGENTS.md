# Agent working agreement

This repository documents a container environment; it is **not** an administrator interface to the underlying ChatGPT product or host.

## Priorities
1. Provenance and truthful scope before completeness claims.
2. Never publish personal/private data or platform-owned Skill source without redistribution permission.
3. New features should be stdlib-first where possible and independently tested.
4. Preserve original raw snapshots unchanged. Public derived datasets must be redacted, deterministic and schema-versioned.
5. CI must not require secrets. Pages should be a zero-build static site and work on a GitHub project subpath.
6. Changes to inventory counts require regenerating `docs/data/catalog.json` and the published workbook.
7. Keep interactive UI keyboard-accessible, mobile responsive, and resilient to JS and JSON loading errors.

## Development commands
```bash
python -m unittest discover -s tests -v
python skills/runtime-audit/scripts/audit_runtime.py --output /tmp/audit.json
python -m http.server 8000 -d docs
```

## Security review before any upload
Search for credentials, tokens, absolute user-profile paths and private data; verify license for third-party content. Public GitHub Pages is readable by everyone. Never conflate "tool installed" with "plugin connected".
