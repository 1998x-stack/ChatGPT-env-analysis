# Skill 迁移与本地操作手册

## 推荐做法：只迁移本仓库原创 Skill

```bash
git clone https://github.com/1998x-stack/ChatGPT-env-analysis.git
cd ChatGPT-env-analysis
mkdir -p ~/.codex/skills ~/.claude/skills
cp -R skills/runtime-audit ~/.codex/skills/
cp -R skills/skill-inventory ~/.codex/skills/
cp -R skills/environment-diff ~/.codex/skills/
```

不同 Agent 的技能注册方式各不相同；以上仅为目录复制示例，并不保证插件或当前 ChatGPT 产品自动注册。

## 如果你拥有合法使用和迁移平台原始 Skill 文件的授权

在**自己的受信任机器或私有工作空间**操作，并遵守对应许可；不要上传到公开 GitHub 仓库。可先检查范围和体积：

```bash
find /home/oai/skills -maxdepth 2 -name SKILL.md -print
du -sh /home/oai/skills/{docx,pdfs,slides,spreadsheets}
# 确认许可允许后，仅在本地创建私有档案：
tar -C /home/oai -czf "$HOME/skills-local-private.tar.gz" skills
```

`skills://plugins/...` 代表插件注册 URI，不是可以 `cp` 的文件路径；不能用上述文件命令导出，也不应通过抓取服务内部代码绕过许可约束。

## 回滚

删除个人安装目录中由本项目放入的三个原创 Skill 子目录即可；不要改动系统自带 `/home/oai/skills` 或平台服务组件。
