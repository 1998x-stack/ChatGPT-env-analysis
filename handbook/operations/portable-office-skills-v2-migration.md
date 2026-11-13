# 四套独立 Office Skills 本地迁移指南（Expanded v2）

## 1. 说明与合规边界

本包为独立编写的四个 Skill，**不是 OpenAI 内置 `/home/oai/skills/{docx,pdfs,slides,spreadsheets}` 的镜像**。那些原始目录里的许可文件禁止外部提取/留存及分发。本包不包含原始源代码和模板，功能覆盖情况请看 `FEATURE-MATRIX.zh-CN.md`。

## 2. 解压与完整性检验

```bash
unzip portable-office-skills-expanded-v2.zip
cd portable-office-skills-expanded-v2
python3 verify.py
# 也可独立检查发行包：sha256sum -c portable-office-skills-expanded-v2.zip.sha256
```

## 3. 创建独立 Python 虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Python >=3.10 推荐。没有使用网络的离线部署须提前准备对应系统/架构的 wheel。字体与 LibreOffice 不在此 ZIP 中，目标机器需要另行安装；不要求一定有 LibreOffice 才能执行基本命令。

## 4. 安装到你的 Agent 项目

```bash
# 预演，不覆盖
python install.py --framework all --project /path/to/your-project --dry-run

# 实际安装到 4 种代理结构
python install.py --framework all --project /path/to/your-project

# 指定一个位置
python install.py --dest /path/to/your-skills --framework codex

# 强制更新：会先把已存在的 Skill 目录移动到 .backup-001 等备份
python install.py --framework codex --project /path/to/your-project --force
```

目标目录如下：

```text
/path/to/your-project/
├── .codex/skills/docx-open, pdf-open, slides-open, spreadsheets-open
├── .claude/skills/... 
├── .opencode/skills/...
└── .pi/skills/...
```

> 安装前，请确认你的 Agent 工具是否自动加载这些路径。各框架的配置行为可能随版本变化。本包默认使用新命名（`*-open`），不会覆盖原有 `docx` 等目录。

## 5. 快速验收

```bash
mkdir -p output
python skills/docx-open/scripts/docx_cli.py compose examples/docx-report.json output/report.docx
python skills/docx-open/scripts/docx_cli.py audit output/report.docx
python skills/slides-open/scripts/slides_cli.py create examples/slides-deck.json output/deck.pptx
python skills/slides-open/scripts/slides_cli.py audit output/deck.pptx
python skills/spreadsheets-open/scripts/sheets_cli.py build examples/workbook.json output/model.xlsx
python skills/spreadsheets-open/scripts/sheets_cli.py audit output/model.xlsx
python skills/spreadsheets-open/scripts/sheets_cli.py import-csv examples/data.csv output/data.xlsx
python skills/pdf-open/scripts/pdf_cli.py from-text examples/notes.md output/notes.pdf
python skills/pdf-open/scripts/pdf_cli.py inspect output/notes.pdf
```

注意：PDF `from-text` 只支持 ASCII 字符，示例 `notes.md` 为 ASCII，中文应转 DOCX 后用 LibreOffice 渲染 PDF。

## 6. 发布到 GitHub 的推荐方式

- 推荐提交整个 ZIP、单独的 SHA256 文件和本迁移手册；亦可将本包独立代码提交到你的仓库。
- 在公开 README 中明确说明“independently authored/open alternative”，不要标注为 OpenAI 原版内部 Skills 或复制版。
- 若使用 GitHub Release，上传 ZIP 和校验文件作为 Release assets，并说明版本与已知限制。
- 不要把依赖虚拟环境 `.venv` 或用户文件、密钥、缓存包含在 ZIP 中。

## 7. 升级、回滚与验证

1. 在全新目录解压新版、执行 `verify.py`、单元测试。
2. 使用 `install.py --dry-run` 查看操作；存在旧版本时使用 `--force` 自动备份。
3. 运行代表性 DOCX/PDF/PPTX/XLSX 文件并逐页/逐表检查结果。
4. 若升级后出现兼容问题，移除新版目录并恢复此前的 `*.backup-NNN`。
5. 验证报告要区分：可执行命令成功、文件内容正确、渲染视觉正确、版权/安全检查完成。它们不能互相替代。

## 8. 已知缺口

本包不支持完整 Word OOXML 评审链路、OCR 流水线、PowerPoint 动画/母版体系和 Excel 公式计算引擎。详见功能矩阵。若你的项目需要这些功能，可在原有独立代码基础上逐步扩展并补测试；不要将“不能完全覆盖”伪装成原版完整复制。
