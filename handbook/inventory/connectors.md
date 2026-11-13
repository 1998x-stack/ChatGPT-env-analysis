# 工具接口与外部连接器

目前会话动态接口数 **242**，其中 GitHub 89、Google Drive 45、Remote Desktop Commander 30、Gmail 21、Google Calendar 15、Finances 14、Automations 8、Files 7、Plugin Management 6、Contacts 3、User Settings 2、Skills 2。

这是一份**接口曝光表**，不是服务授权表，也不说明可以越权调用。一个 GitHub 接口的存在不表示可以修改所有仓库；一个 Desktop Commander 的接口不代表当前设备已在线。详见 `data/catalog/tools.csv` 和仪表盘。

以下工具能力可在会话中以独立通道出现：网页搜索、可视化 UI、容器命令、Python、个人上下文与记忆、安全设置等。其统计口径与 242 个动态接口不同。

## 建议验证阶梯

`接口存在 → 连接状态 → 对象可见性 → 只读测试 → 经用户授权的写入测试 → 审计记录`。绝不自动批量使用具有写入能力的连接器来证明“权限齐全”。
