> **核心洞察**：OpenClaw 是一个高度复杂的自主 Agent 框架，深度集成在系统中，具备自我监控、自我修复和丰富的技能生态。

# 01 - 项目：OpenClaw 平台
**最后更新**: `2026-03-25`

## 1. 核心架构与目录
- **主目录**: `/root/.openclaw/` (占用约 1.8G 空间)
- **工作区**: `/root/.openclaw/workspace/`，包含 Agent 运行时的脚本、输出结果、记忆 (`MEMORY.md`) 和身份设定 (`IDENTITY.md`) 等。
- **配置文件**: `/root/.openclaw/openclaw.json`，定义了模型、Agent、网关和插件配置。

## 2. 技能生态 (Skills)
OpenClaw 拥有丰富的技能插件，位于 `/root/.openclaw/skills/` 目录下：
- `1sec-security`
- `agent-browser`
- `content-fetcher`
- `cron-backup`
- `dependency-audit`
- `dingtalk-send-media`
- `duckdb-cli`
- `image-search-sender`
- `ontology`
- `scrapling` (现代 Web 高效网页抓取工具，已内置，无需外部独立副本)
- `summarize`
- `unified-search`

## 3. Agent 角色
当前配置了以下 Agent 角色 (`/root/.openclaw/agents/`)：
- `main`: 默认主控 Agent，允许调用子 Agent。
- `coder`: 专注于代码编写的 Agent。
- `researcher`: 专注于信息检索和研究的 Agent。

## 4. 模型配置
OpenClaw 接入了多种大语言模型，主要通过 DashScope 提供：
- `Qwen3.5 Plus` (主模型)
- `Qwen3 Max Thinking` (备用模型)
- `Qwen3 Coder Next` / `Qwen3 Coder Plus`
- `MiniMax-M2.5`
- `GLM-5` / `GLM-4.7`
- `Kimi K2.5`

## 5. 运行服务
- **openclaw-gateway.service**: 网关服务，监听 18789 等端口。
- **soul-guardian.service**: 核心文件完整性监控服务。
