# Skills 生态分层

| 来源 | 计数 | 判断条件 | 公共仓库处理 |
|---|---:|---|---|
| 本地核心 | 4 | `/home/oai/skills/{docx,pdfs,slides,spreadsheets}/SKILL.md` | 仅元数据/用法概述 |
| 插件目录 | 31 | `skills://plugins/...` URI | 仅注册表元数据 |
| 第三方依赖携带 | 1 | Typer wheel 内 `typer/.agents/skills/typer/SKILL.md` | 仅元数据 |
| 本项目原创 Skill | 3 | 本仓库 `skills/*/SKILL.md` | 源码开放发布 |

**31 插件目录细分：** 20 个 OpenAI artifact 模板、5 个 Google Drive/Docs/Sheets/Slides 能力、4 个文档路由、1 个 Template Creator、1 个 Plugin Management。静态目录不证明插件当前已授权。

### 分类逻辑

用 `installed-filesystem`、`registry-advertised`、`bundled-not-registered`、`project-authored` 四维描述；不要把四种数量混加称为“可自动调用的安装包”。详细行在 `data/catalog/skills.csv`。若需要原版 Skill 源码，请先检查其许可并在本地按相应条款转移，不能因为能读取就将其公开镜像。
