# Expanded v2 发布说明

本版本是在先前独立编写的轻量 portable-office-skills 基础上全面扩展，而不是从任何受限的内置平台 Skill 导出代码。

## 新增与改进

- DOCX：增加结构化 JSON 文档排版、标题/列表/表格/图片/分页、提取、元数据最小化、基础结构审计、LibreOffice 可选转换。
- PDF：增加拆分、旋转、页渲染、文字搜索脱敏、文字水印、清理元信息、来源检查，并为脱敏添加提取后复查。
- Slides：增加多栏、表格、柱状/折线图、图片、备注、基础几何检查和 PDF 转换。
- Spreadsheets：增加多表、明确的公式映射、图表和格式、CSV 文本注入防护、公式/链接/错误值审计、工作簿比较。
- 分发：补齐 YAML front matter 的独立 SKILL.md、参考文档、示例输入、迁移说明、版权边界、SHA-256 和集成测试。

## 当前测试情况

2026-11-13 当前容器内 `python -m unittest discover -s tests -v`：11 tests passed。测试覆盖代表性正向路径和部分边界情况；不构成全面安全审计或所有 Office 软件兼容性保证。

## 未包含

- OpenAI 专有 `/home/oai/skills` 原始文件、源代码、模板或体积约 123MB 的专有 slides 资产。
- 完整 DOCX 追踪修订和审阅、PDF OCR 与全面安全脱敏、PPT 动画母版、Excel 计算引擎。

如需特别高的功能覆盖，应按照 `FEATURE-MATRIX.zh-CN.md` 提供的缺口列表进行逐项独立开发和测试。
