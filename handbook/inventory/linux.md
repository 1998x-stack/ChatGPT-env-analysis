# Linux 与计算资源

| 分类 | 观察值 | 解读 |
|---|---|---|
| OS | Debian GNU/Linux 13.3 | 包管理以 dpkg 为主 |
| Linux | 6.18.57 x86_64 | 不能推断宿主完整硬件权限 |
| CPU | cgroup 限额约 4 vCPU | 多线程和并行测试需限流 |
| 内存 | `memory.max=4294967296` | 真正的容器内存预算是 4 GiB |
| Swap | 无 | 大模型加载更易触发内存限制 |
| 磁盘 | 32 GiB overlay，约 30 GiB 空间（采样时） | 容量随会话变化，不是长期承诺 |
| CUDA GPU | 不可访问 | `torch.cuda.is_available()` 为 False |
| PATH | 2,101 个独立命令名 | 仅 PATH 枚举，非全盘可执行文件审计 |
| fonts | 2,561 条字体文件路径 | 有 Noto CJK，可用于中文排版 |

系统还包含 FFmpeg、ImageMagick、Tesseract、LibreOffice、Pandoc、LaTeX、Chromium、Git、Go、GCC/Clang 和 Java。完整 1,398 条 Debian 软件包在 `data/catalog/packages.csv` 按 ecosystem `Debian` 过滤。Linux root 身份不等于拥有云宿主机权限。
