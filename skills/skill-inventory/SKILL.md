---
name: skill-inventory
description: >
  Discover, classify and document local SKILL.md entry points and separately
  supplied ChatGPT plugin skill URIs. Use to build an auditable skill catalog
  without confusing filesystem installs with registries or redistributing
  third-party copyrighted skill implementations.
---

# Skill Inventory — Multi-source skill catalog

## Discovery order
1. Local known roots (`/home/oai/skills`, project `.codex/skills`, `.claude/skills` etc.) with explicit scope and read-only traversal.
2. Plugin registry URIs from a separately supplied TSV; do not invent or assume the script can call the platform's registry by itself.
3. Optionally inspect package-embedded Skill files, labeled `bundled-not-registered`.

## Run
```bash
python skills/skill-inventory/scripts/catalog_skills.py \
  --local-root /home/oai/skills \
  --registry data/catalog/plugin-skill-registry.tsv \
  --output /tmp/skill-catalog.json
```

## Categorization
Keep `local`, `plugin`, `bundled-not-registered`, and `original-project-skill` distinct. Collect display names, URI/path, provider, availability evidence and license/readme reference. A Skill URI does not prove an enabled plugin or local install. Never publish third-party Skill source merely because it is readable.

## Output and QA
JSON inventory with unique `kind + reference` identifiers; count by scope; list unknown license and enrollment conditions. Source content is **not** copied. Include a transparent source-to-output provenance chain.
