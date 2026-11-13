# 数据字典与口径

## `docs/data/catalog.json`

- `schema_version`: 数据结构版本；当前 1.0。
- `summary`: 快照 ID、观察日期、系统类型、容器资源限制、计数字段。
- `skills[]`: `id/name/origin/category/reference/evidence/publish`；每条仅对应一种来源。
- `tool_groups[]`: `namespace/count`；全部计数之和 242。
- `tools[]`: `name/namespace`；接口名不是 OAuth 权限。
- `package_groups[]`: `name/count`；各 Python 环境按实例计算，同名包可重复。
- `packages[]`: `name/version/ecosystem`；2099 条包行（4 套 pip + Debian + npm）。
- `risks[]`: `id/severity/domain/title/evidence/level/mitigation`；不代表漏洞扫描报告。
- `sources/notes`: 来源及解释性限制。

## 导出表

`data/catalog/skills.csv` — 36 条来自三类外部/本地来源；`data/catalog/tools.csv` — 242 行；`data/catalog/packages.csv` — 2099 行；`data/catalog/risks.csv` — 7 行；`summary.json` — 主要 KPI。

## 采样与安全

均来自 2026-11-13 的单一可用会话；没有复制用户私有邮件、云盘文件、凭据或第三方 Skill 代码。其它环境重复采集会得到不同数据。
