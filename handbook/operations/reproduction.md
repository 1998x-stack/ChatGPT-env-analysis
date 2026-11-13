# 重新采集 / Reproduce

```bash
# 1. 采集当前 Linux/Python，不访问网络，不导出环境变量值
python skills/runtime-audit/scripts/audit_runtime.py --output out/runtime.json

# 2. 枚举指定文件树中的一级 Skill 入口及允许使用的 URI 清单
python skills/skill-inventory/scripts/catalog_skills.py \
  --local-root /home/oai/skills \
  --registry data/catalog/plugin-skill-registry.tsv \
  --output out/skills.json

# 3. 比较差异
python skills/environment-diff/scripts/compare_snapshots.py \
  baseline/runtime.json out/runtime.json --output out/diff.json --no-fail-on-change

# 4. 测试本项目
python -m unittest discover -s tests -v
```

目前 `scripts/build_catalog.py` 默认读取之前本地生成的 `/mnt/data/environment-audit-2026-11-13` 历史快照，属于**快照整理器**，不负责直接连通 ChatGPT 插件注册表。若换机器，须显式提供合法取得的历史数据路径：`--source /path/to/audit-archive`。新运行环境通常无法复现 2026-11-13 的固定数量。
