#!/usr/bin/env python3
"""Build an editable, polished Excel workbook using artifact_tool only."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/catalog'
DEST=ROOT/'spreadsheets/ChatGPT-environment-audit-2026-11-13.xlsx'

def rows(name):
    with (DATA/name).open(newline='',encoding='utf-8') as fh:
        reader=csv.reader(fh)
        return [row for row in reader]

def add_table(wb,name,source,widths):
    sheet=wb.worksheets.add(name)
    table=rows(source)
    ncols=len(table[0]); nrows=len(table)
    sheet.merge_cells(f'A1:{chr(64+ncols)}1')
    sheet.get_range('A1').values=[[name.upper()+'  |  AUDIT INVENTORY']]
    sheet.get_range('A1').format={'fill':'#0F2030','font':{'size':16,'bold':True,'color':'#FFFFFF'},'row_height':38,'vertical_alignment':'center'}
    sheet.get_range_by_indexes(2,0,nrows,ncols).values=table
    sheet.get_range_by_indexes(2,0,1,ncols).format={'fill':'#214151','font':{'bold':True,'color':'#FFFFFF'},'row_height':26}
    sheet.freeze_panes.freeze_rows(3)
    for i,w in enumerate(widths):
        sheet.get_range_by_indexes(0,i,nrows+3,1).format.column_width=w
    if nrows > 1:
        sheet.get_range_by_indexes(3,0,nrows-1,ncols).format.row_height=20
    return sheet,nrows-1

def main():
    wb=Workbook.create()
    summary=wb.worksheets.add('Dashboard')
    summary.merge_cells('A1:G2')
    summary.get_range('A1').values=[['CHATGPT ENVIRONMENT  /  AUDIT DASHBOARD']]
    summary.get_range('A1:G2').format={'fill':'#0F2030','font':{'size':18,'bold':True,'color':'#FFFFFF'},'row_height':26,'vertical_alignment':'center'}
    summary.get_range('A4:B4').values=[['Snapshot','2026-11-13']]
    summary.get_range('A5:B5').values=[['Scope','ChatGPT container + advertised tools']]
    summary.get_range('A7:B7').values=[['Metric','Count']]
    summary.get_range('A7:B7').format={'fill':'#214151','font':{'bold':True,'color':'#FFFFFF'},'row_height':27}
    metrics=[('Core local Skills',4),('Plugin Skills',31),('Bundled Skill (not registered)',1),('Connector actions',242),('Main pip',507),('Tool pip',124),('Terminal pip',14),('System pip',34),('Debian packages',1398),('Global npm',22),('PATH commands',2101),('Font filepaths',2561)]
    summary.get_range('A8:B19').values=[[a,b] for a,b in metrics]
    summary.get_range('A21').values=[['Crosscheck with inventory sheets ↓']]
    summary.get_range('A22:A24').values=[['Skill inventory rows'],['Tool inventory rows'],['Package inventory rows']]
    summary.get_range('B22').formulas=[['=COUNTA(Skills!A4:A39)']]
    summary.get_range('B23').formulas=[['=COUNTA(Tools!A4:A245)']]
    summary.get_range('B24').formulas=[['=COUNTA(Packages!A4:A2102)']]
    summary.get_range('A27').values=[['Important: counts are environment-scoped, not deduplicated across Python interpreters.']]
    summary.merge_cells('A27:G27')
    summary.get_range('A27:G27').format={'fill':'#FFF5E5','font':{'color':'#855F26'},'row_height':28}
    summary.get_range('A:A').format.column_width=36
    summary.get_range('B:B').format.column_width=35
    for col in 'CDEFG': summary.get_range(f'{col}:{col}').format.column_width=13
    summary.get_range('A8:B19').format.row_height=22
    summary.get_range('B8:B24').set_number_format('#,##0')
    summary.get_range('A21').format.font.bold=True
    summary.freeze_panes.freeze_rows(2)
    add_table(wb,'Skills','skills.csv',[53,20,27,73,22,22,22])
    add_table(wb,'Tools','tools.csv',[77,30])
    add_table(wb,'Packages','packages.csv',[55,24,22])
    add_table(wb,'Risks','risks.csv',[11,12,18,48,64,17,95])
    sources=wb.worksheets.add('Sources')
    sources.get_range('A1:C1').values=[['Evidence class','Scope','Source / guidance']]
    sources.get_range('A1:C1').format={'fill':'#214151','font':{'bold':True,'color':'#FFFFFF'},'row_height':28}
    evidence=[['Observed','Container-local','reports/2026-11-13/original-audit.md'],['Validated','Tests / crosschecks','data/snapshots/2026-11-13/smoke-results.json'],['Declared','Plugin registry','data/catalog/plugin-skill-registry.tsv'],['Unknown','Not verified','handbook/inventory/quality.md'],['Security','No credentials copied','handbook/governance/publication-safety.md'],['Reproduction','Python stdlib collectors','skills/runtime-audit/SKILL.md'],['Docs','GitHub Pages / site','handbook/operations/github-pages.md']]
    sources.get_range('A2:C8').values=evidence
    for i,w in enumerate([17,34,68]):sources.get_range_by_indexes(0,i,8,1).format.column_width=w
    sources.freeze_panes.freeze_rows(1)
    try:
        summary.get_range('D5:E11').values=[['Tool Namespace','Interfaces'],['GitHub',89],['Google Drive',45],['Remote Desktop',30],['Gmail',21],['Calendar',15],['Finances',14]]
        chart=summary.charts.add('bar','D5:E11')
        chart.title_text='Tool interface concentration'
        chart.set_position('D13','L25')
    except Exception as ex:
        print('Non-blocking chart issue:',type(ex).__name__,str(ex)[:200])
    DEST.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(DEST))
    print('Saved',DEST, DEST.stat().st_size)
    print('Dashboard:',wb.inspect({'kind':'table','range':'Dashboard!A7:B12','include':'values,formulas','table_max_rows':8,'table_max_cols':2}).ndjson[:1200])
    print('Sheets:',wb.inspect({'kind':'sheet','include':'id,name'}).ndjson[:900])

if __name__=='__main__':main()
