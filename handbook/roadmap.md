# Roadmap

## v1 · 已实现

- 2026-11-13 审计快照、36 条 Skill 来源记录、242 接口、2099 包行。
- 原创 `runtime-audit`、`skill-inventory`、`environment-diff` 三项 Skill。
- CSV / JSON / XLSX 台账、中文手册、静态 GitHub Pages 展示、基础回归测试。

## v1.1 · 建议下一阶段

- 将 `pip check` 与 Playwright、PDF、Office、LaTeX 等能力编排成可选、最小权限的 smoke suite。
- 为工具连接器加入经用户授权的逐项只读验证，区分连接中、连接失败、未经验证。
- 定时生成**本地私有**快照，经人工隐私门控后再选择性公开。
- 建立 JSON Schema、SBOM（SPDX/CycloneDX）转换和版本差异时间轴。
- 增加 GitHub Actions 对比前后快照的可视化报告、OpenSSF 风险提示与静态站点性能测试。
