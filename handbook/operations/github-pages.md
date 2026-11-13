# GitHub Pages 部署、验证与回滚

项目使用 `docs/` 为**零构建静态站点**，资源路径全部是相对路径，适合 `https://1998x-stack.github.io/ChatGPT-env-analysis/` 的子路径。提交 `.github/workflows/pages.yml` 后，部署是否成功取决于仓库设置、GitHub Actions 和 Pages 资源权限。

## 初次配置

1. GitHub 仓库 `Settings → Pages` 中选择 `GitHub Actions` 作为 Build and deployment 来源。若当前无法由 API 配置，需要由仓库管理员在网页中手动操作。
2. 仓库 `Actions` 允许工作流执行。
3. 推送到 `main` 后，检查 `Deploy dashboard to GitHub Pages` workflow 是否成功。
4. 打开上述 Pages URL，检查 dashboard 数字、搜索、过滤器、响应式布局及移动端显示。

## 本地验证

```bash
python -m unittest discover -s tests -v
python -m json.tool docs/data/catalog.json >/dev/null
python -m http.server 8000 --directory docs
# 访问 http://localhost:8000 ，用浏览器 Console 确认无错误。
```

## 失败排查

- 404：Pages 尚未启用、尚未部署或发布路径不正确。
- 工作流 `pages` 权限失败：检查 `Settings → Pages` 来源和仓库的 Actions 运行策略。
- 页面能打开但数据为空：确保 `docs/data/catalog.json` 随版本提交，所有路径相对于仓库子路径。
- UI 不工作：检查 JSON 和 JS 控制台错误，不使用外部 CDN 依赖。

回滚：回退 main 上的前端相关 commit，再次触发 Pages workflow。数据快照要保留版本，以便审计。
