#!/usr/bin/env python3
"""Make editable bilingual executive audit brief (DOCX); rendered separately for QA."""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'documents/ChatGPT-environment-brief-2026-11-13.docx'
DARK=RGBColor(14,32,45); GREEN=RGBColor(45,120,79); GREY=RGBColor(90,105,113)

def p(doc,text='',style=None):
    para=doc.add_paragraph(style=style)
    if text:para.add_run(text)
    return para

def heading(doc,text,level=1):
    h=doc.add_heading(text, level);return h

def table(doc,headers,rows):
    t=doc.add_table(rows=1,cols=len(headers));t.style='Light Shading Accent 1'
    t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for cell,val in zip(t.rows[0].cells,headers):cell.text=str(val)
    for row in rows:
        cells=t.add_row().cells
        for c,val in zip(cells,row):c.text=str(val);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    doc.add_paragraph('')
    return t

def main():
    doc=Document(); section=doc.sections[0];section.top_margin=Inches(.75);section.bottom_margin=Inches(.68)
    section.left_margin=Inches(.83);section.right_margin=Inches(.83)
    styles=doc.styles
    for name in ['Normal','Title','Heading 1','Heading 2']:
        s=styles[name];s.font.name='Noto Sans CJK SC';s.font.size=Pt(9 if name=='Normal' else (26 if name=='Title' else 15 if name=='Heading 1' else 11));s.font.color.rgb=DARK
        s._element.rPr.rFonts.set(qn('w:eastAsia'),'Noto Sans CJK SC')
    styles['Normal'].paragraph_format.space_after=Pt(6)
    styles['Normal'].paragraph_format.line_spacing=1.21
    styles['Heading 1'].font.color.rgb=GREEN
    hdr=section.header.paragraphs[0];hdr.text='ENV / ATLAS     •     RUNTIME INTELLIGENCE REPORT';hdr.style='Caption'
    foot=section.footer.paragraphs[0];foot.text='1998x-stack / ChatGPT-env-analysis     •     Snapshot: 13 Nov 2026     •     Public-safe edition';foot.alignment=WD_ALIGN_PARAGRAPH.CENTER
    t=doc.add_paragraph();t.style='Title';t.add_run('ChatGPT 运行环境\n全景审计摘要')
    p(doc,'ENVIRONMENT OBSERVATORY  /  TECHNICAL EXECUTIVE BRIEF')
    p(doc,'2026 年 11 月 13 日  ·  单次执行容器与工具注册表快照',style='Subtitle')
    p(doc,'本报告以可核查证据为核心，将 Linux 容器、软件包、Skills、工具接口和运行测试拆分为不同证据层级，不将“可见”直接等同于“已授权”或“能够稳定执行”。')
    heading(doc,'核心指标 / Audit at a glance')
    table(doc,['检查对象','数量或状态','边界说明'],[
        ['本地核心 Skills','4','磁盘 SKILL.md 入口'],['插件 Skills','31','注册表 URI，不等于本地目录'],
        ['第三方随包 Skill','1','Typer 包内，非自动注册'],['动态工具接口','242','声明接口，非逐项认证'],
        ['Python pip 包','507 / 124 / 14 / 34','4 套独立 Python 环境'],
        ['Debian / npm 全局包','1,398 / 22','不同软件生态'],
        ['CPU / Memory','约 4 CPU / 4 GiB','cgroup 实际资源配额'],
        ['GPU','未检测到可访问 CUDA','不对宿主 GPU 情况做推断']])
    heading(doc,'系统构成 / Capability layers')
    p(doc,'① Runtime：Debian GNU/Linux 13、Python 3.13.5、Node.js 22、FFmpeg、LibreOffice、LaTeX、Chromium 等；当前容器适合数据分析、文档自动化与 CPU 规模工作负载。')
    p(doc,'② Skills：本地四大核心文件能力（Word、PDF、Slides、Spreadsheets）；独立插件目录另含 31 个 Skill URI，必须按照触发条件与来源分别管理。')
    p(doc,'③ Connector tools：GitHub、Google Drive、Gmail、Calendar、Remote Desktop Commander、Automations 等共 242 个方法名称。每个方法的真实权限都由对应连接器与账号状态决定。')
    doc.add_page_break()
    heading(doc,'已发现的限制 / Evidence-based constraints')
    table(doc,['级别','问题','工程建议'],[
        ['HIGH','主环境 MoviePy/Pillow 依赖版本冲突','不要全局升级；在隔离 venv 复测'],
        ['HIGH','内存配额 4 GiB，无 CUDA','控制并行与模型体积'],
        ['MEDIUM','系统 Python supervisor 缺少 setuptools','避免修改系统解释器'],
        ['MEDIUM','容器 DNS 测试失败','区分原生网络与外部工具通道'],
        ['MEDIUM','Playwright data: 跳转受限','使用 set_content/local HTTP'],
        ['UNKNOWN','连接器逐项授权状态未验证','只有在需要时做最小授权测试']])
    heading(doc,'项目交付 / What is published')
    p(doc,'原创 runtime-audit、skill-inventory、environment-diff 三项 Skill；可检索的静态网页仪表盘；分层数据目录；CSV/JSON/XLSX 台账；运维、版权、复现与质量说明；GitHub Actions 测试与 Pages 部署流程。')
    heading(doc,'安全与复现约束 / Publication rule')
    p(doc,'公开仓库只保存可公开的元数据与原创实现；不发布令牌、私钥、个人信息、环境变量值、私有仓库内容或来源不明的第三方 Skill 源码。完整本地资料可另以压缩包保留；公开 UI 显示历史快照，不能代表实时能力。')
    p(doc,'仓库：github.com/1998x-stack/ChatGPT-env-analysis')
    p(doc,'计划中的 GitHub Pages 地址：1998x-stack.github.io/ChatGPT-env-analysis/')
    OUT.parent.mkdir(exist_ok=True,parents=True);doc.save(OUT);print(OUT,OUT.stat().st_size)

if __name__=='__main__':main()
