# Python 多环境与依赖

| 环境 | 解释器 | 包数量 | 主要风险 |
|---|---|---:|---|
| main | `/opt/pyvenv/bin/python` | 507 | `moviepy` 和 `Pillow` 约束冲突 |
| python-tool | `/opt/pyvenv-python-tool/bin/python` | 124 | 与主环境的 NumPy/Pandas 版本不同 |
| terminal | `/opt/terminal-server/pyvenv/bin/python` | 14 | 平台服务依赖，不宜随意变更 |
| system | `/usr/bin/python3` | 34 | `supervisor` 缺少 setuptools |

主环境包含 NumPy、Pandas、SciPy、Matplotlib、Plotly、PyTorch CPU、OpenCV、Playwright、FastAPI、python-docx、PyMuPDF、ReportLab、artifact_tool 和 JupyterLab 等。更多见 `data/catalog/packages.csv` 和仪表盘的 Ecosystem 过滤器。

## 版本复现方法

把 `pip:main`、`pip:tool`、`pip:terminal`、`pip:system` 分成独立 venv，不要合并导出 `requirements.txt` 直接全局安装。建议针对实际需求建立最小 `pyproject.toml` / 锁文件。在已经共享的系统环境中不要直接升级依赖来消除审计里的冲突。
