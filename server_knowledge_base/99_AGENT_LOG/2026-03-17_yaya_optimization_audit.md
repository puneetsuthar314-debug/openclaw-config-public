# 审计日志：丫丫智能提升方案分析

- **日期**: 2026-03-17
- **操作者**: Manus (外部 AI 审计)
- **任务**: 分析丫丫当前配置，提出智能提升方案

## 检查范围
- openclaw.json 完整配置
- mcp.json、workspace 全部核心文件、vault 系统文件
- memory 目录、skills 目录、cron jobs、lossless-claw 插件
- 服务器资源状态

## 关键发现
1. 三 Agent 分工架构合理，system prompt 体系完善
2. MCP 工具严重不足（仅 filesystem + fetch）
3. 无 model fallback 配置
4. 无外部 Provider（OpenRouter）
5. mihomo 代理 inactive
6. OpenClaw 2026.3.7（最新版）
7. 服务器 1.8GB RAM, 磁盘 74% 已用

## 文档更新
- 已更新: 02_SERVICES/openclaw_gateway.md（追加智能提升方案建议）

---

## 追加：MCP 工具扩展方案审计 (2026-03-17 14:00)

### 检查范围
- mcp.json 当前配置
- openclaw.json tools/plugins 配置
- TOOLS.md 和 vault/reference/tools-manual.md
- 服务器网络可达性测试（Tavily/GitHub/DuckDuckGo/百度）
- npm 包可用性验证（@playwright/mcp, tavily-mcp）
- 已安装软件清单（Playwright, duckduckgo_search, agent-browser, markitdown）

### 关键发现
1. Tavily API 和 GitHub API 国内可直连，无需 mihomo 代理
2. DuckDuckGo 被墙
3. @playwright/mcp v0.0.68 可用，服务器已有 Playwright + Chromium
4. 百炼内置工具（web_search/web_parser/code_interpreter/wan26_media）已可用
5. 当前 MCP 仅 2 个（filesystem + fetch），严重不足

### 文档更新
- 已更新: 02_SERVICES/openclaw_gateway.md（追加 MCP 扩展方案）

---

## Playwright MCP 安装记录 (2026-03-17 14:10)

### 操作
1. 备份 mcp.json → mcp.json.bak.20260317
2. 添加 playwright MCP 配置（@playwright/mcp@latest, --headless）
3. 预热 npx 缓存（npx -y @playwright/mcp@latest --help 成功）
4. 重启 openclaw-gateway（systemctl restart）

### 结果
- Gateway: active (running)，PID 356002
- MCP 服务器数量: 3（filesystem, fetch, playwright）
- 内存: 896MB used / 1.8GB total（可用 974MB）
- Playwright MCP 为懒加载，首次使用时才 spawn

### 注意
- Playwright MCP 启动浏览器实例会额外占用 200-300MB
- 建议在 TOOLS.md 中注明简单网页获取优先用 fetch，仅在需要 JS 渲染时用 Playwright
