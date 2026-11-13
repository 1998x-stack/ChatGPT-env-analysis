#!/usr/bin/env python3
"""Create a public-safe data catalog from the 2026-11-13 audit archive."""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path('/mnt/data/environment-audit-2026-11-13')
LOCAL = [('docx', 'Document authoring'), ('pdfs', 'PDF pipeline'),
         ('slides', 'Slides and visual design'), ('spreadsheets', 'Spreadsheet modeling')]
RISKS = [
 ('R-01','high','Python','moviepy 2.2.1 vs Pillow 12.3.0','pip check failed: version constraint mismatch','Observed','Pin a compatible Pillow or MoviePy build in an isolated venv; re-test before changing shared environment'),
 ('R-02','medium','Python','system supervisor missing setuptools','pip check failed for system Python','Observed','Do not modify Debian system Python in place; repair only inside a controlled image'),
 ('R-03','high','Compute','4 GiB cgroup memory / 4 CPU quota','cgroup values, not host reported memory','Validated','Size models and test runners to cgroup limits'),
 ('R-04','medium','Network','Direct container DNS check failed','curl exit code 6 for example.com','Observed','Use platform connectors for supported external workflows; do not assume generic Internet access'),
 ('R-05','medium','Browser','Playwright data: navigation blocked','data: goto failure; set_content passed','Validated','Use page.set_content or a local server; test target navigation policy'),
 ('R-06','medium','Publication','Platform Skills have unknown reuse licenses','Metadata available; code redistribution not authorized','Declared','Publish URI/summary only and original project Skills; manual private export if authorized'),
 ('R-07','medium','Availability','Connection permissions not individually exercised','Tool registry is not an auth audit','Unknown','Check each external service on demand'),
]

def read_tsv(path):
    with path.open(encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh, delimiter='\t'))

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',default=str(RAW))
    a=ap.parse_args()
    source=Path(a.source)
    local = [{'id': 'local:'+name, 'name': name, 'origin': 'Core local Skill',
              'category': cat, 'reference': f'/home/oai/skills/{name}/SKILL.md',
              'evidence':'filesystem', 'publish':'metadata-only'} for name,cat in LOCAL]
    plugin_rows=read_tsv(source/'skills/plugin-skill-registry.tsv')
    plugins=[]
    for r in plugin_rows:
        uri=r['skill_uri']
        tokens=uri.removeprefix('skills://plugins/').split('/')
        name=tokens[-1]
        plugins.append({'id':'plugin:'+uri, 'name':name,'origin':'Plugin registry',
                        'category':tokens[0], 'reference':uri, 'evidence':'registry',
                        'publish':'metadata-only'})
    bundled=[{'id':'bundled:typer','name':'typer','origin':'Bundled, not registered',
              'category':'Python package', 'reference':'typer/.agents/skills/typer/SKILL.md',
              'evidence':'filesystem', 'publish':'metadata-only'}]
    skills=local+bundled+plugins
    assert len(skills)==36
    groups=json.loads((source/'skills/tool-groups.json').read_text())
    tools=[]
    for r in read_tsv(source/'skills/tool-interfaces.tsv'):
        # Public catalog intentionally does not export connector credentials/args.
        tool=(r.get('tool_name') or r.get('name') or list(r.values())[0]).strip()
        ns=next((x['namespace'] for x in groups if tool.startswith('mcp__'+x['namespace']+'__') or tool.startswith(x['namespace']+'__')),'other')
        tools.append({'name':tool, 'namespace':ns})
    assert len(tools)==242, len(tools)
    packages=[]
    for key,desc in [('main','main'),('tool','tool'),('terminal','terminal'),('system','system')]:
        rows=json.loads((source/f'raw/python3-{key}-pip.json').read_text())
        for r in rows:
            packages.append({'name':r['name'],'version':r['version'], 'ecosystem':f'pip:{desc}'})
    with (source/'raw/system-packages.tsv').open(encoding='utf-8',newline='') as fh:
        for fields in csv.reader(fh,delimiter='\t'):
            if fields:
                packages.append({'name':fields[0], 'version': fields[1] if len(fields)>1 else '', 'ecosystem':'Debian'})
    npm=json.loads((source/'raw/npm-global.json').read_text())
    dep=npm.get('dependencies',{})
    for name,r in dep.items():
        packages.append({'name':name,'version':r.get('version',''), 'ecosystem':'npm-global'})
    pcounts=Counter(x['ecosystem'] for x in packages)
    assert pcounts=={'pip:main':507,'pip:tool':124,'pip:terminal':14,'pip:system':34,'Debian':1398,'npm-global':22},pcounts
    base=ROOT/'data/catalog'
    write_csv(base/'skills.csv',skills,list(skills[0]))
    write_csv(base/'tools.csv',tools,['name','namespace'])
    write_csv(base/'packages.csv',packages,['name','version','ecosystem'])
    write_csv(base/'risks.csv',[dict(zip(['id','severity','domain','title','evidence','level','mitigation'],r)) for r in RISKS],['id','severity','domain','title','evidence','level','mitigation'])
    write_csv(base/'plugin-skill-registry.tsv',plugin_rows,['skill_uri','category']) if False else None
    (base/'plugin-skill-registry.tsv').write_text((source/'skills/plugin-skill-registry.tsv').read_text())
    summary={'id':'2026-11-13','date':'2026-11-13','scope':'ChatGPT Linux container + tool registry',
             'os':'Debian 13.3 / Linux 6.18.57','architecture':'x86_64',
             'python':'3.13.5','node':'22.16.0','resource_cpu':'4 CPU quota',
             'resource_memory':'4 GiB cgroup', 'gpu':'CPU only observed',
             'limitations':'Container and tool registry are separate; permissions outside the container not audited.',
             'counts':{'core_skills':4,'plugin_skills':31,'bundled_skill':1,'tool_interfaces':242,
                      'pip_main':507,'pip_tool':124,'pip_terminal':14,'pip_system':34,
                      'debian':1398,'npm_global':22,'path_commands':2101,'font_filepaths':2561}}
    catalog={'schema_version':'1.0','summary':summary,'skills':skills,
             'tool_groups':groups,'tools':tools, 'package_groups':[{'name':k,'count':v} for k,v in pcounts.items()],
             'packages':packages,'risks':[dict(zip(['id','severity','domain','title','evidence','level','mitigation'],r)) for r in RISKS],
             'sources':{'audit':'reports/2026-11-13/original-audit.md','skill_registry':'data/catalog/plugin-skill-registry.tsv'},
             'notes':['Snapshot is historical; not a live endpoint.', 'Counts are per environment and may overlap.',
                     'No credentials or environment variable values are included.']}
    (ROOT/'docs/data/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (base/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    # Only allowlisted files are added to public snapshot, never credentials.
    dst=ROOT/'data/snapshots/2026-11-13'
    for rel in ['audit-validation.json','tests/smoke-results.json','skills/tool-groups.json']:
        f=source/rel
        target=dst/f.name
        target.write_bytes(f.read_bytes())
    print(json.dumps({'total_skills':len(skills),'tool_interfaces':len(tools),'packages':len(packages),
                      'site_catalog_bytes':(ROOT/'docs/data/catalog.json').stat().st_size},ensure_ascii=False))

if __name__=='__main__':
    main()
