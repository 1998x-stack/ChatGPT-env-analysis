# 文档导航 · Audit Handbook

本系列将执行环境按“在哪里运行 → 能运行什么 → 证据是什么 → 哪些限制 → 如何发布”组织，不用笼统的“已安装”掩盖各层差异。

| 分类 | 文档 | 核心问题 |
|---|---|---|
| 体系结构 | [执行环境架构](architecture.md) | Container / Skills / Tool registry 的边界 |
| 系统 | [Linux 与资源](inventory/linux.md) | CPU、RAM、文件系统、系统软件 |
| Python | [解释器与依赖](inventory/python.md) | 四套 Python、包冲突、可复现性 |
| Skills | [Skill 生态](inventory/skills.md) | 4 + 31 + 1，什么能公开 |
| 工具 | [连接器与 API](inventory/connectors.md) | 242 个接口，哪些算可用 |
| 质量 | [测试与限制](inventory/quality.md) | 已测、未测、失败、风险 |
| 源数据 | [数据字典](governance/data-dictionary.md) | JSON / CSV schema 和可信度 |
| 安全 | [发布策略](governance/publication-safety.md) | 隐私、证据与版权 |
| 操作 | [重新采集](operations/reproduction.md) | 无密钥、无全局安装、零依赖 |
| 操作 | [本地迁移](operations/migration.md) | Skill 文件打包、转移和安装 |
| 操作 | [GitHub Pages](operations/github-pages.md) | 构建、部署、验证与故障排查 |
| 规划 | [演进路线](roadmap.md) | 安全差分、持续回归、公开看板 |
