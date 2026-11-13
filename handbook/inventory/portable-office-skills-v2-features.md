# 功能覆盖矩阵（Expanded v2）

这里记录的是**本包实际实现的功能**。因受限源 Skill 不能被镜像，这不是对 OpenAI 内置 Skill 的逐文件复刻或声称完全兼容。

| 领域 | 功能 | 当前状态 | 工具 |
|---|---|---|---|
| DOCX | 文本 / 标题 / 列表 | 实现 | `from-text`, `compose` |
| DOCX | 结构化表格、图片、页眉尾注（固定 footer） | 实现（有限） | `compose` |
| DOCX | 段落、标题与媒体数量检查 | 实现 | `inspect`, `audit` |
| DOCX | 内容提取 | 实现（非保真） | `extract` |
| DOCX | 常见核心元数据最小化 | 部分实现 | `scrub` |
| DOCX | PDF 转换 | 可选 LibreOffice | `render` |
| DOCX | 完整修订/批注/OOXML 修改 | **未实现** | — |
| PDF | 页数、尺寸、元信息 | 实现 | `inspect` |
| PDF | 可搜索文本提取 | 实现 | `text` |
| PDF | 合并/拆页/区间提取/旋转 | 实现 | `merge`, `split`, `pages`, `rotate` |
| PDF | PNG 页面预览 | 实现 | `render` |
| PDF | 文本标记与基本文字脱敏 | 有限实现 | `watermark`, `redact-text` |
| PDF | 常见元数据最小化 | 部分实现 | `clean-metadata` |
| PDF | OCR/加密权限/表单/全面安全脱敏 | **未实现** | — |
| PPTX | 标题、项目符号、多栏、表格 | 实现 | `create` |
| PPTX | 图表、图片、演讲者备注 | 实现 | `create` |
| PPTX | 结构检查 / 坐标边界检查 | 实现 | `inspect`, `audit` |
| PPTX | 通过 LibreOffice 渲染 PDF | 可选 | `render` |
| PPTX | 动画/母版设计/完整可访问性审计 | **未实现** | — |
| XLSX | CSV 安全导入/导出 | 实现 | `import-csv`, `export-csv` |
| XLSX | 多工作表/显式公式/图表/单元格格式 | 实现 | `build` |
| XLSX | 公式/错误/链接/隐藏表审计 | 部分实现 | `audit` |
| XLSX | 单元格差异比较 | 实现 | `compare` |
| XLSX | 公式执行/全面Excel引擎兼容 | **未实现** | — |

## 功能覆盖的定义

`实现` = 自带代码路径并有代表性的测试；`部分实现` = 有明确保护范围限制；`可选` = 依赖本机可执行软件；`未实现` = 禁止对外宣称已有此能力。即便标注实现，也不代表经历了多平台/恶意输入/高安全级别认证。
