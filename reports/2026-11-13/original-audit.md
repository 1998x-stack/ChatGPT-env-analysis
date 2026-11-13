# ChatGPT 运行环境全景审计报告

> 审计快照：2026-11-13 03:12 UTC（北京时间 11:12）；对象：当前会话可访问的 Linux 容器及本会话暴露的工具/技能注册表；类型：只读枚举 + 有限烟雾测试。**不是宿主机全盘审计，也不是所有外部账号的权限审计。**

## 0. 摘要与完整性原则

本次检查不把“可以调用的工具”“已安装的 Python/系统软件”“文件形式存储的 Skill”“插件托管 Skill”混为一谈。下列是分别确认的层级：

| 指标 | 数量或结果 | 来源文件 |
|---|---:|---|
| 本地第一方核心 Skills | 4 | `raw/filesystem-skill-files.txt`、`raw/local-skills-manifest.tsv` |
| 第三方 Python 包内附带的独立 Skill | 1（Typer；有 2 个路径入口） | `raw/filesystem-skill-files.txt` |
| 插件 Skills 注册表项目 | 31 | `skills/plugin-skill-registry.tsv` |
| 当前会话可枚举的工具接口 | 242，分属 12 个工具组 | `skills/tool-interfaces.tsv` |
| 主 Python venv pip 包 | 507 | `raw/python3-main-pip.json` |
| Python 工具 venv pip 包 | 124 | `raw/python3-tool-pip.json` |
| Terminal venv pip 包 | 14 | `raw/python3-terminal-pip.json` |
| 系统 Python pip 包 | 34 | `raw/python3-system-pip.json` |
| Debian 系统软件包 | 1,398 | `raw/system-packages.tsv` |
| Node 全局顶层 npm 包 | 22 | `raw/npm-global.json` |
| PATH 上不同名称的可执行文件 | 2,101 | `raw/path-executables.tsv` |
| fontconfig 中唯一 family 字段值 | 1,772 | `raw/font-families.txt` |
| fontconfig 中唯一字体文件路径 | 2,561 | `raw/font-files.txt` |
| 本地四 Skill 目录内文件 | 184 | `raw/local-skills-manifest.tsv` |
| 本地四 Skill 目录内子目录 | 20 | `raw/local-skills-manifest.tsv` |
| `/mnt` 原有普通文件 | 5（生成本审计之前） | `raw/mnt-manifest.tsv` |

**重要限定：** 上表“所有”均指具体枚举源及其时点。例如 2,101 是当前 PATH 下不同名称的可执行文件，不包括 shell 内建、未列入 PATH 的程序、随时可能生成的进程或容器外软件；507 是一个特定 Python venv 的发行版包数，四套 Python 环境不可累加理解为完全独立的包集合。对插件只有技能/工具元数据，并非所有插件的登录认证都已验证。`/mnt` 文件清单刻意不包含本报告生成目录，以防递归自包含。

## 1. 操作系统、硬件、资源、隔离

| 属性 | 实测 |
|---|---|
| 发行版 | Debian GNU/Linux 13.3 (trixie) |
| 内核 | Linux 6.18.57，x86_64 |
| 容器内用户 | root (`uid=0`)；不等于拥有宿主机 root 权限 |
| Python 默认版本 | 3.13.5 |
| 命令行可见逻辑 CPU (`nproc`) | 5 |
| cgroup CPU quota | `400000 100000`：相当于约 4 CPU 核计算配额 |
| `free` 系统内存显示 | 约 5.8 GiB |
| cgroup 实际内存上限 | **4 GiB** (`4294967296` bytes) |
| Swap | 0 |
| `/` 文件系统 | overlay，32 GiB，约 30 GiB 可用（审计时） |
| NVIDIA / CUDA | 未发现 NVIDIA 设备或 `nvidia-smi`；PyTorch `torch.cuda.is_available()` 返回 `False` |
| 容器公网访问 | 对 `https://example.com` 的 DNS 解析测试失败，`curl` 返回 code 6；该测试不等同于所有网络都禁用 |
| 时区 | 容器时钟采样为 UTC；用户界面、目标系统的时区可以不同 |

因此这里适合中小型 CPU 工作负载、代码构建、浏览器自动化、文档处理和小样本机器学习；**不适合假设拥有 GPU 来本地推理大型模型**，也不能把内核/宿主硬件/外部登录状态视为容器已掌控资源。外部网页搜索、生成图片、访问 GitHub 和 Google 服务等依靠 ChatGPT 工具层，不能据此推断 Linux 容器具备同等公网权限。

## 2. 文件系统与常用工作目录

```text
/
├── /mnt/
│   └── data/                      # 对话输出与附件处理目录
│       ├── available-commands.txt      # 旧盘点产物
│       ├── environment-inventory.md    # 旧盘点产物
│       ├── environment-inventory.zip   # 旧盘点产物
│       ├── pip-packages.txt            # 旧盘点产物
│       ├── system-packages.tsv         # 旧盘点产物
│       └── environment-audit-2026-11-13/   # 本次新增
├── /home/oai/skills/             # 4 个本地第一方 Skills
├── /opt/pyvenv/                 # 主 Python 运行环境
├── /opt/pyvenv-python-tool/     # 第二 Python 运行环境
├── /opt/terminal-server/pyvenv/ # Terminal Python 环境
├── /opt/nvm/                   # Node 版本管理文件
├── /opt/imagemagick/           # ImageMagick
├── /opt/novnc/                 # 预装 noVNC 组件
├── /opt/python-tool/           # 平台 Python 工具组件
├── /opt/terminal-server/       # 平台终端服务组件
└── /usr/bin/                   # Debian 软件命令
```

系统存在多个其他 `/opt` 平台目录；**目录存在不代表用户可控制或需要直接操作内部服务**。完整顶层名称在 `raw/top-level-opt.txt`。本次对 `/mnt`、`/home/oai/skills` 进行了递归遍历，包括隐藏文件名、文件大小、Unix 权限、mtime、SHA-256（普通文件）、符号链接指向，见两份 TSV。没有导出用户隐私文件正文、环境变量值或凭据。

## 3. Skills：三种不同的“安装”概念

### 3.1 本地明确注册的核心 Skills（4）

| 路径 | 能力 | 实际内容规模 |
|---|---|---|
| `/home/oai/skills/docx/SKILL.md` | DOCX 创作、修改、修订、批注、目录、样式、对比、保护、无障碍与渲染核验 | 69 文件，含 34 个 scripts、25 篇 tasks |
| `/home/oai/skills/pdfs/SKILL.md` | PDF 创建、提取、检查、编辑、表单、OCR、脱敏、转换、页面渲染、比较 | 47 文件，含 21 个 scripts、16 篇 tasks |
| `/home/oai/skills/slides/SKILL.md` | 演示文稿、PPTX、图表、视觉设计、母版与图形 | 64 文件，含 `artifact_tool/`、`container_tools/`、`pptxgenjs_helpers/`、`slide_templates/` |
| `/home/oai/skills/spreadsheets/SKILL.md` | XLSX / 数据表创建、读写、公式、计算、分析及可视化 | 4 文件，含模板与 API 说明 |

实际 Skill 目录不仅有入口文档：`docx/scripts/` 中有批注提取/追加/清理、接受修订、Word 域处理、文档无障碍审计、元数据脱敏、渲染检查等；`pdfs/scripts/` 涵盖渲染、提取、预检、脱敏、水印和表单处理；`slides/` 配有大量生成工具和示例。

### 3.2 第三方依赖携带的 Skill（1 项）

`/opt/pyvenv/lib/python3.13/site-packages/typer/.agents/skills/typer/SKILL.md`。相同相对路径在 `lib64` 下可见，但属于同一 Python 环境的两处目录入口；**不能把它统计成两个独立技能**。这是 Python `typer` 发行物所携带的 Skill 文件，不代表被当前 ChatGPT Skills 注册表自动启用。若要使用，仍需按显式路径和实际能力判断。

### 3.3 插件 Skills 注册表（31 项，非本地文件）

**OpenAI Templates（20 项）**：

1. `artifact-template-analytics-dashboard` — 数据分析仪表盘
2. `artifact-template-business-review` — 经营复盘演示
3. `artifact-template-design-report` — 设计报告
4. `artifact-template-experiment-analysis` — 实验分析
5. `artifact-template-financial-budget` — 财务预算
6. `artifact-template-investment-committee-memo` — 投资委员会备忘录
7. `artifact-template-legal-memorandum` — 法律备忘录
8. `artifact-template-market-trends-report` — 市场趋势报告
9. `artifact-template-minimal-letterhead` — 信函模板
10. `artifact-template-operating-calendar` — 运营日历
11. `artifact-template-operating-review` — 运营复盘
12. `artifact-template-project-kickoff` — 项目启动会
13. `artifact-template-project-tracker` — 项目跟踪器
14. `artifact-template-sales-pipeline` — 销售管道
15. `artifact-template-simple-dark-mode` — 深色演示模板
16. `artifact-template-simple-light-mode` — 浅色演示模板
17. `artifact-template-strategy-memorandum` — 战略备忘录
18. `artifact-template-system-design` — 系统设计文档
19. `artifact-template-team-alignment` — 团队对齐演示
20. `artifact-template-three-statement-forecast` — 三表联动预测

**其他（11 项）**：

21. `template-creator/template-creator` — 制作/维护可复用个人模板
22. `presentations-router/presentation` — 演示文稿能力路由
23. `pdf-router/pdf` — PDF 能力路由
24. `documents-router/document` — 文档能力路由
25. `google-drive/google-docs` — Google Docs 创建与编辑
26. `google-drive/google-drive` — Drive 文件检索、组织、权限和版本管理
27. `google-drive/google-drive-comments` — 云端评论与审阅
28. `google-drive/google-sheets` — Google Sheets 表格与范围操作
29. `google-drive/google-slides` — Google Slides 内容与样式操作
30. `plugin-management/plugin-management` — 插件发现、连接与权限管理
31. `spreadsheets-router/spreadsheet` — 电子表格能力路由

完整 URI 见 `skills/plugin-skill-registry.tsv`。注意模板 Skills 的启用通常取决于用户是否选中相应模板，路由 Skills 有显式选择条件；其**存在**不代表每次请求都会被自动调用，也不代表磁盘上有一个对应 `/home/oai/skills` 文件夹。

## 4. 当前会话工具接口（242 项）

完整 242 个**精确接口名**见 `skills/tool-interfaces.tsv`，以下按 API 服务分组，合计已经逐项核对。

| API / 连接器命名空间 | 接口数 | 可以做什么（视权限与连接状态） |
|---|---:|---|
| GitHub | 89 | 仓库/分支/PR/Issue/文件/GitHub Actions 的读取与变更 |
| Google Drive | 45 | 文件、Docs、Sheets、Slides、评论、导入导出与共享 |
| Remote Desktop Commander | 30 | 连接授权设备、检索文件、读写文件、执行进程 |
| Gmail | 21 | 查邮件、草稿、标签、附件、发送或归档 |
| Google Calendar | 15 | 日历、活动、空闲状态、创建/修改/RSVP |
| Finances | 14 | 连接账户、财务数据查询、信用报告、关注列表 |
| Automations | 8 | 定时任务、执行、查看和管理 |
| Files | 7 | 当前对话或 Library 文件检索、读取、分享、持久管理 |
| Plugin Management | 6 | 搜索插件、推荐、检查权限、管理连接 |
| Google Contacts | 3 | 联系人检索与详情 |
| User Settings | 2 | 可支持的偏好设置读写 |
| Skills Registry | 2 | 列举及阅读插件 Skills |
| **合计** | **242** | **API 接口暴露数，不是已授权账号数** |

此外，当前会话还有 **18 个独立命名的直接工具调用入口**，见 `skills/direct-tools.tsv`；它们没有计入以上 242 个动态接口。独立于上述 242 个动态接口的能力：`web` 网页与结构化搜索、`genui` 交互组件、`image_gen` 图像生成/编辑、`container` 本地命令执行、Python 执行、用户可见 Python、个人上下文检索、Memory、对话摘要、安全设置等。这些不应错误记入 `pip` 或本地 Skill 数量。外部 API 的认证、资源权限、配额和限制应针对具体服务单独测试；仅凭工具接口名无法断定账号已连接且具备写权限。

## 5. Python：四套不同环境

| 环境 | 解释器 | Python 版本 | pip 包数 | 典型用途 |
|---|---|---|---:|---|
| 主环境 | `/opt/pyvenv/bin/python` | 3.13.5 | 507 | 文档、可视化、数据科学、浏览器脚本、CPU ML |
| Python Tool | `/opt/pyvenv-python-tool/bin/python` | 3.13.5 | 124 | 平台 Python 工具隔离依赖 |
| Terminal Server | `/opt/terminal-server/pyvenv/bin/python` | 3.13.5 | 14 | 平台服务自身依赖 |
| Debian 系统环境 | `/usr/bin/python3` | 3.13.5 | 34 | Debian 系统 Python 生态 |

**不能合并这四套的版本作为一个 `requirements.txt`**。例如主环境 `numpy 2.3.5 / pandas 2.2.3`，Python Tool 环境 `numpy 2.4.4 / pandas 3.0.2`。不同解释器调用同名包可能得到不同接口和行为。开发时应始终使用绝对解释器路径或明确的 `venv`。

### 5.1 主 Python 环境重要包（均从已安装包元数据核验）

| 领域 | 软件与版本 |
|---|---|
| 数值和表格 | numpy 2.3.5、pandas 2.2.3、scipy 1.17.0 |
| 传统机器学习 | scikit-learn 1.8.0、XGBoost 3.1.3、LightGBM 4.6.0、CatBoost 1.2.8 |
| 深度学习 | PyTorch 2.10.0+cpu、Torchvision 0.25.0+cpu、Torchaudio 2.10.0+cpu |
| NLP | spaCy 3.8.11、NLTK 3.9.2、Gensim 4.4.0、TextBlob 0.19.0 |
| 绘图与分析 | Matplotlib 3.10.8、Plotly 6.5.2、Bokeh 3.8.2、Seaborn 0.13.2 |
| 图像 | Pillow 12.3.0、OpenCV 4.13.0.92、scikit-image 0.26.0 |
| API 与异步 | FastAPI 0.128.2、Uvicorn 0.48.0、Pydantic 2.13.5、aiohttp 3.13.3 |
| 网络/页面解析 | requests 2.32.5、httpx 0.28.1、BeautifulSoup4 4.14.3、lxml 6.1.1 |
| 浏览器自动化 | Playwright 1.57.0 |
| PDF | PyMuPDF 1.26.7、pypdf 5.9.0、pdfplumber 0.11.9、ReportLab 4.4.9、WeasyPrint 68.0 |
| Office | python-docx 1.2.0、python-pptx 1.0.2、openpyxl 3.1.5、XlsxWriter 3.2.9、odfpy 1.4.1 |
| 多媒体 | MoviePy 2.2.1、imageio 2.37.3、librosa 0.11.0、soundfile 0.13.1 |
| 工作流/测试 | JupyterLab 4.5.3、IPykernel 7.2.0、pytest 9.0.2、pytest-asyncio 1.3.0 |

`artifact_tool` 可从主环境成功导入，属于可用的文档/表格/展示工具链。现有包清单中未发现 `openai`、`anthropic`、`transformers`、`langchain` 这几个发行版；**这不表示 ChatGPT 没有 OpenAI 模型接口，而是容器该 Python 环境没有相应官方 SDK 包**。所有 507 项的精确拼写和版本都在 `raw/python3-main-pip.json`，其余三个环境分别提供无损 JSON。

### 5.2 pip 依赖检查发现的问题

| 环境 | `pip check` | 结果 |
|---|---|---|
| 主环境 | 有冲突 | `moviepy 2.2.1` 要求 `Pillow >=9.2.0,<12.0`，当前 `Pillow 12.3.0` |
| Python Tool | 通过 | No broken requirements found |
| Terminal Server | 通过 | No broken requirements found |
| 系统 Python | 有缺项 | `supervisor 4.2.5` 声明需要 `setuptools`，当前系统 Python 包元数据中无此项 |

这反映的是声明依赖健康状况，不等于已验证每个安装包所有运行分支。出于不破坏平台环境的原则，本次没有擅自升级/降级共享依赖。

## 6. 命令行、语言生态与构建能力

| 分组 | 已检测到的组件 |
|---|---|
| Python | Python 3.13.5、pip 25.1.1、uv 0.10.0 |
| JavaScript | Node.js 22.16.0、npm 10.9.2、npx、TypeScript 5.8.3、ts-node 10.9.2 |
| 编译 | GCC/G++ 14.2.0、Clang 17.0.0、CMake 3.31.6、Ninja 1.12.1、GNU Make 4.4.1 |
| 其他语言 | Go 1.23.2、Java/Javac 21.0.12.1、Swift 6.2.1、Ruby 3.3.8、PHP 8.4.24、Perl |
| 版本控制 | Git 2.47.3、rsync 3.4.1 |
| 浏览器 | Chromium 144.0.7559.96、Playwright 1.57.0 |
| Office/文件转换 | LibreOffice 25.2.3.2、Pandoc 3.1.11.1 |
| 文档渲染 | TeX Live 2025、pdfLaTeX、XeLaTeX、LuaLaTeX、Poppler 工具、Ghostscript 10.05.1 |
| 图像/矢量 | ImageMagick 7.1.2-1、Inkscape 1.4 |
| 音视频 | FFmpeg 7.1.5、ffprobe |
| OCR | Tesseract 5.5.0 |
| 数据/系统工具 | jq 1.7、ripgrep 14.1.1、curl 8.10.1、wget 1.25.0、zip/unzip、tar、zstd、OpenSSL 3.5.5 |

本次 PATH 上没有找到：`gh`、`docker`、`podman`、`conda`、`mamba`、`rustc`、`cargo`、`R`、`firefox`、`google-chrome`、`sqlite3` CLI、`psql`、`mysql`、`redis-cli`、`git-lfs`。这里的“没有找到”只代表 PATH 未暴露对应命令；不排除系统中存在相应库、远程连接器或不同名称的接口。例如 Python 标准库的 `sqlite3` 可运行，SQLite 为 3.46.1，即使 `sqlite3` 命令行未安装。GitHub 连接器有 89 个工具接口，**但并不意味着本地装有 GitHub CLI `gh`**。

### 6.1 npm 22 个顶层全局包

- 排版/PPT：`pptxgenjs 4.0.0`、`mathjax-full 3.2.1`、`fontkit 2.0.4`、`linebreak 1.1.0`、`image-size 2.0.2`
- 图像：`sharp 0.34.1`、`skia-canvas 3.0.8`
- 样式：`tailwindcss 4.1.10`、`postcss 8.5.6`、`autoprefixer 10.4.21`
- 工程：`typescript 5.8.3`、`ts-node 10.9.2`、`corepack 0.32.0`、`npm 10.9.2`、`http-server 14.1.1`
- 图标与代码高亮：五个 Font Awesome 相关包、`prismjs 1.30.0`、`@types/prismjs 1.26.5`

准确包名与版本请以 `raw/npm-global.json` 为准。`mathjax-full` 在这套安装中无法直接 `require('mathjax-full')`，但 `require('mathjax-full/js/mathjax.js')` 可用；这是模块入口层的兼容性区别，不可简化成整个 MathJax 不工作。

### 6.2 字体、TeX 和多媒体

字体文件路径 2,561 个、fontconfig family 值 1,772 种；包括 `Noto Sans CJK SC`、DejaVu、Liberation、STIX、Amiri 等，中文排版基础良好。FFmpeg 编解码器、过滤器和格式支持的完整输出分别保存在 `raw/ffmpeg-encoders.txt`、`raw/ffmpeg-decoders.txt`、`raw/ffmpeg-filters.txt`、`raw/ffmpeg-formats.txt`。

## 7. 真实运行烟雾测试

本次不只检查命令路径，而是实际运行了关键能力：

| 项目 | 结果 | 说明 |
|---|---|---|
| Python 科学计算/HTTP/API 核心模块联合导入 | 通过 | NumPy、Pandas、SciPy、scikit-learn、Matplotlib、Plotly、FastAPI 等可导入 |
| 文档模块联合导入 | 通过 | PyMuPDF、python-docx、python-pptx、ReportLab、openpyxl、Playwright |
| `artifact_tool` 导入 | 通过 | 模块存在、可载入 |
| PyTorch 导入 | 通过 | `2.10.0+cpu`，CUDA 不可用 |
| OpenCV 导入 | 通过 | `4.13.0` |
| Playwright 启动 Chromium + `page.set_content` | 通过 | 成功启动浏览器、读取标题 |
| Playwright `data:` URL 导航 | 失败（策略限制） | `net::ERR_BLOCKED_BY_ADMINISTRATOR`；不是浏览器整体无法启动 |
| Node 全局包联合导入 | 部分通过 | pptxgenjs/sharp/skia-canvas/typescript/fontkit 通过；mathjax-full 根入口失败 |
| MathJax 子模块入口 | 通过 | `mathjax-full/js/mathjax.js` 可用 |
| Python SQLite | 通过 | 内置 sqlite3 使用 SQLite 3.46.1 |
| 中文字体匹配 | 通过 | Noto Sans CJK SC 成功匹配 |
| FFmpeg 编码器枚举 | 通过 | 能输出编码器清单 |
| Go 平台查询 | 通过 | `linux/amd64` |
| 容器向 `example.com` HTTPS 访问 | 失败 | DNS 解析失败，不等于 ChatGPT Web 工具不可用 |

逐项执行命令、退出状态、输出摘要见 `tests/smoke-results.json`。烟雾测试不代表对 507 个包、1,398 个系统包进行过功能级全覆盖；不能将未测试项目写成已验证正常。

## 8. 分层能力评估与缺口

**非常适合的工作：**

- Python 数据处理、传统机器学习训练、小型 CPU 推理、可视化与统计分析。
- Word、PDF、PowerPoint、Excel、Markdown、LaTeX、图片、SVG 和视频的处理与生成。
- Git 仓库内容检查、代码修复、编译、单元测试与本地项目脚手架。
- Playwright + Chromium 的受支持页面操作与离线 HTML 渲染（受浏览器策略和网络限制）。
- 使用 ChatGPT 网页搜索工具调研，用连接器操作经授权的 GitHub/Google 等系统。

**限制与风险：**

1. **资源限制：** CPU quota 约 4 核、cgroup 内存 4 GiB、无 GPU；大型深度学习模型的本地推理/训练不现实。
2. **联网限制：** 容器 DNS 外网测试失败；不能把可搜索网页的工具能力等同于容器中 `requests`、`curl` 可直连公网。
3. **部署限制：** PATH 下无 Docker、Podman、`gh`；构建 Dockerfile/Compose 文件与在本地真正运行容器是两回事。
4. **依赖冲突：** 主环境 MoviePy/Pillow 版本不匹配；系统 Python Supervisor 缺少 setuptools 元数据依赖。
5. **环境隔离：** 四套 Python 环境包版本不同；切换 `python` 路径可能导致功能差异。
6. **浏览器策略：** `data:` URL 导航被管理员策略拦截；`page.set_content` 测试通过。
7. **模型 SDK：** 主环境未检测到 `openai`、`anthropic`、`transformers`、`langchain` 等 pip 发行版；如项目确实需要，应在独立项目环境中安装。
8. **工具权限边界：** 242 个接口只是本会话中可发现的入口，连接器认证、写权限、速率限制、远程设备授权与外部服务实际状态并未逐个测试。
9. **持久性与复现：** `/mnt/data` 适合输出交付，但不能假设该容器或临时运行态跨会话永久保留。应保存清单、锁定项目依赖、将重要代码提交版本库。

## 9. 推荐的分离部署/开发结构

可将工作拆成两个层次：**本地运行库**负责文件与计算，**ChatGPT 连接器**负责授权的外部读写。尤其是涉及 GitHub Actions、云端文档、外部搜索时，不能让本地 `curl` 无 DNS 的问题掩盖已有的官方工具通道。建议在项目工作目录配置独立 `uv`/venv，pin 项目 dependencies，并先执行 `pip check`、核心 import smoke test、Playwright 页面加载测试，再运行完整测试。不要直接修改 `/opt/pyvenv` 下的平台共享依赖来修 MoviePy 冲突。

## 10. 审计目录/证据地图

```text
environment-audit-2026-11-13/
├── README.md                         # 本中文总报告
├── inventory-summary.json           # JSON 总索引和各项采集状态
├── collect.py                       # 可复用的只读环境采集脚本
├── build_platform_catalog.py        # 本会话 242 工具 / 31 Skills 元数据清单
├── run_smoke.py                      # 实测脚本
├── skills/
│   ├── plugin-skill-registry.tsv     # 全部 31 个插件 Skill URI
│   ├── tool-interfaces.tsv          # 全部 242 个接口精确名称
│   └── tool-groups.json              # 12 类接口数
├── tests/
│   └── smoke-results.json           # 实际验证及失败细节
└── raw/
    ├── mnt-manifest.tsv             # /mnt 生成报告前的完整条目和哈希
    ├── local-skills-manifest.tsv    # 本地 4 Skills 全部 204 个条目及文件哈希
    ├── filesystem-skill-files.txt   # 扫到的 SKILL.md 路径
    ├── python3-main-pip.json        # 主环境 507 包
    ├── python3-tool-pip.json        # Python Tool 环境 124 包
    ├── python3-terminal-pip.json    # Terminal 环境 14 包
    ├── python3-system-pip.json      # 系统环境 34 包
    ├── pip-check-*.txt              # 4 套 pip 依赖健康结果
    ├── system-packages.tsv          # 1398 个 Debian 包
    ├── path-executables.tsv         # PATH 上 2101 个可执行文件名/路径
    ├── npm-global.json             # 22 个全局顶层 npm 包
    ├── font-families.txt            # fontconfig family 明细
    ├── font-files.txt               # 字体文件明细
    ├── shared-libraries.txt         # 共享库信息
    ├── ffmpeg-*.txt                 # FFmpeg 编解码格式及滤镜
    └── ...                          # CPU、内存、磁盘、命令版本等原始证据
```

### 本报告的“无遗漏”标准

对**已经声明的枚举范围**，保留了每个 API 接口、Plugin Skill URI、Python venv 包、Debian 包、全局 npm 包、PATH 可执行命令以及目标目录文件清单，没有只提供前十/前百条的截断抽样。对宿主机、容器内部平台私有服务、未枚举的网络设备、尚未连接的外部系统、进程内存与凭据则**明确不声称完全覆盖**。没有输出密钥、令牌或其他敏感环境变量值。所有清单是当前时点快照，软件或连接器变动后应重新执行对应盘点。
