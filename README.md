# OpenClaw 配置模板 (公开 / 脱敏版)

一套经过实战验证的 **OpenClaw AI Agent** 完整配置模板，包含工作区设计、多 Agent 架构、技能体系、定时任务和自动化运维脚本。可作为快速部署 OpenClaw 的起点，也可作为学习 OpenClaw 最佳实践的参考。

> **注意**: 所有敏感信息（API Key、Token、密钥）已替换为占位符 `<YOUR_...>`，使用前需替换为您自己的凭证。

## 快速部署

### 前置条件

- 一台 Linux 服务器（推荐 Ubuntu 22.04+ / CentOS 8+）
- Node.js 22.x 或更高版本
- 钉钉开发者账号（如需使用钉钉通道）

### 部署步骤

```bash
# 1. 克隆仓库
git clone https://github.com/puneetsuthar314-debug/openclaw-config-public.git
cd openclaw-config-public

# 2. 填入您的凭证
#    编辑 openclaw.json，将所有 <YOUR_...> 替换为真实值
#    编辑 .env，填入 Moonshot/Kimi API Key

# 3. 运行一键部署
chmod +x deploy.sh
sudo ./deploy.sh
```

### 需要替换的凭证

| 占位符 | 说明 | 获取方式 |
|--------|------|----------|
| `<YOUR_DINGTALK_CLIENT_ID>` | 钉钉机器人 AppKey | [钉钉开发者后台](https://open-dev.dingtalk.com/) |
| `<YOUR_DINGTALK_CLIENT_SECRET>` | 钉钉机器人 AppSecret | 同上 |
| `<YOUR_ALIYUN_DASHSCOPE_API_KEY>` | 阿里云百炼 API Key | [百炼控制台](https://bailian.console.aliyun.com/) |
| `<YOUR_GATEWAY_TOKEN>` | Dashboard 访问令牌 | 自行生成: `openssl rand -hex 32` |
| `<YOUR_API_KEY>` | LLM 模型 API Key | 对应模型提供商 |
| `<YOUR_MOONSHOT_API_KEY>` | Moonshot API Key | [Moonshot 控制台](https://platform.moonshot.cn/) |
| `<YOUR_KIMI_API_KEY>` | Kimi API Key | 同上 |

## 仓库结构

```
.
├── deploy.sh                      # 一键部署脚本
├── openclaw.json                  # 主配置文件（已脱敏）
├── .env                           # 环境变量模板
├── mcp.json                       # MCP Server 配置
├── identity/                      # 设备身份（首次运行自动生成）
│   └── README.md
├── agents/                        # Agent 配置
│   └── main/agent/
│       ├── auth.json
│       └── models.json            # 模型提供商配置（已脱敏）
├── workspace/                     # 主工作区
│   ├── SOUL.md                    # Agent 人格定义
│   ├── AGENTS.md                  # 多 Agent 协作规则
│   ├── USER.md                    # 用户画像
│   ├── TOOLS.md                   # 工具使用指南
│   ├── STYLE.md                   # 输出风格规范
│   ├── MEMORY.md                  # 记忆系统入口
│   ├── HEARTBEAT.md               # 心跳检查规则
│   ├── skills/                    # 31 个自定义技能
│   ├── memory/                    # 记忆系统
│   ├── scripts/                   # 自动化脚本
│   ├── templates/                 # 项目和任务模板
│   ├── projects/                  # 项目工作目录
│   ├── tasks/                     # 任务管理
│   └── docs/                      # 文档归档
├── workspace-coding/              # Coding Agent 工作区
├── workspace-researcher/          # Researcher Agent 工作区
├── cron/                          # 定时任务配置
├── memory/                        # 全局记忆
├── scripts/                       # 运维脚本
│   ├── openclaw-cleanup.sh        # 每周清理
│   └── openclaw-health-check.sh   # 每小时健康检查
├── completions/                   # Shell 自动补全
└── proxy/                         # 代理配置
```

## 架构亮点

### 多 Agent 协作

本配置采用三 Agent 架构，各司其职：

- **main**: 主 Agent，负责对话、任务规划和工具调用
- **coding**: 编程专用 Agent，负责代码编写和调试
- **researcher**: 研究 Agent，负责信息检索和深度分析

### 技能体系

包含 31 个精心设计的自定义技能，覆盖股票分析、市场研究、科学分析、PDF 生成、Markdown 转换、视频生成、安全审计、任务规划、项目管理、统一搜索、网页测试等领域。

### 记忆系统

分层记忆架构，包括工作记忆 (MEMORY.md)、每日日志 (memory/NOW.md)、经验教训 (memory/lessons/)、成功剧本 (memory/playbooks/) 和基于 DashScope 的向量语义搜索。

### 自动化运维

- **每小时健康检查**: 进程监控、端口检查、内存/磁盘告警、自动重启
- **每周清理**: 废弃会话、浏览器缓存、过期日志
- **每日自动备份**: workspace 增量备份
- **Job Runner**: 统一的任务守护包装器，失败时写入记忆供 Agent 自查

## 安全建议

部署后请务必执行以下安全加固：

1. 设置 `conversation.allowFrom` 白名单，限制钉钉私聊访问
2. 配置 `gateway.trustedProxies` 信任反向代理
3. 设置 `session.dmScope` 为 `per-channel-peer` 隔离会话
4. 运行 `openclaw security audit` 检查安全状态

## 版本信息

- **OpenClaw 版本**: 2026.3.7
- **钉钉插件版本**: clawdbot-dingtalk 0.4.6
- **配置日期**: 2026-03-12

## 许可

本配置模板仅供学习和参考使用。OpenClaw 本身的许可请参考 [OpenClaw 官方文档](https://docs.openclaw.ai/)。
