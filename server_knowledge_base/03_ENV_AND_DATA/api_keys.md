> **核心洞察**：API 密钥的管理较为混乱，不同服务从不同位置加载密钥。操作时必须严格遵循各自的配置。

# 03 - 数据：API 密钥管理

**最后更新**: `2026-03-16`

## 密钥使用指南

| 服务/项目 | 配置文件 | 密钥变量 | 备注 |
|---|---|---|---|
| **ProjectChimera** | `/root/ProjectChimera/config/.env` | `OPENAI_API_KEY` | **唯一指定**。该项目只从此文件加载密钥。 |
| **OpenClaw 平台** | `/root/.openclaw/.env` | `MOONSHOT_API_KEY`, `KIMI_API_KEY` | **优先使用**。环境变量通常会覆盖 JSON 文件中的配置。 |
| OpenClaw 平台 (备用) | `/root/.openclaw/openclaw.json` | `apiKey` | 仅在 `.env` 文件不存在或未配置时才会生效。 |

## 风险与维护

- **密钥泄露风险**: 由于所有操作均在 `root` 用户下进行，任何一个服务的漏洞都可能导致所有密钥泄露。
- **续期与更换**: 本文档**未包含**密钥的续期信息。如果发现某个 API 因密钥过期而失败，你需要向服务器所有者报告，以获取新的密钥并更新到对应的配置文件中。

> **[2026-03-17] Agent 建议 (配置审计 by Manus)**:
> 1. **DingTalk 阿里云 MCP 独立密钥**：OpenClaw 的 DingTalk 插件 (`clawdbot-dingtalk`) 使用独立的阿里云 MCP API Key `sk-xxxx-REDACTED-xxxx`，配置在 `openclaw.json` 的 `channels.clawdbot-dingtalk.aliyunMcp.apiKey` 字段中。此密钥与 DashScope 模型密钥不同。
> 2. **DashScope 模型密钥统一**：所有 8 个大模型（Qwen3.5 Plus、Qwen3 Max、Qwen3 Coder Next/Plus、MiniMax-M2.5、GLM-5、GLM-4.7、Kimi K2.5）均通过同一个 DashScope API Key 接入，配置在 `openclaw.json` 的 `models.providers.dashscope.apiKey` 字段。
> 3. **OpenClaw .env 密钥用途**：`/root/.openclaw/.env` 中的 `MOONSHOT_API_KEY` 和 `KIMI_API_KEY` 实际上与 DashScope 密钥相同（`sk-xxxx-REDACTED-xxxx`），用于 OpenClaw 的搜索功能（provider: kimi）。
