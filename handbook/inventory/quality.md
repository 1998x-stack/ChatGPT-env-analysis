# 测试、失败与未知项

## 2026-11-13 快照观察

- 已通过：核心 Python 导入、文档模块、artifact_tool、PyTorch CPU、OpenCV、Chromium `set_content`、Noto CJK 字体、FFmpeg 编解码器输出、Go、SQLite、MathJax 子路径导入。
- 观察到失败：直接 `data:` URL Playwright 导航；容器直连 `example.com` DNS；两处 Python 环境 `pip check` 不满足声明约束。
- 特别区分：最初 Node 脚本的 `require('mathjax-full')` 返回未找到，但针对子路径的检测通过；因此不能简单归纳为“MathJax 缺失”。
- 未验证：所有 242 个接口逐项授权、外部 Pages 线上部署、宿主机资源、私有连接器资源完整性。

风险清单保存在 `data/catalog/risks.csv`，原始烟测快照保存在 `data/snapshots/2026-11-13/smoke-results.json`。网页上的未测试项目不应以红色 FAIL 展示。
