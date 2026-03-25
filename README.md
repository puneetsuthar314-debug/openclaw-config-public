# OpenClaw 配置与技能库（公开版）

本仓库是 OpenClaw AI Agent 平台的**脱敏配置模板和技能集合**，适合学习、参考和快速部署。

## 目录结构

```
openclaw-config-public/
├── config/                    # 核心配置文件（已脱敏）
│   ├── openclaw.json          # OpenClaw 主配置（使用环境变量引用）
│   ├── mcp.json               # MCP Server 配置
│   └── .env.example           # 环境变量模板
├── skills/                    # OpenClaw 原生技能
│   ├── 1sec-security/         # 安全审计技能
│   ├── agent-browser/         # 浏览器自动化
│   ├── content-fetcher/       # 内容抓取
│   ├── cron-backup/           # 定时备份
│   ├── duckdb-cli/            # DuckDB 数据分析
│   ├── ontology/              # 知识本体
│   ├── scrapling/             # 网页爬取
│   ├── unified-search/        # 统一搜索
│   └── ...
├── workspace-skills/          # 工作区扩展技能（30+）
│   ├── stock-analysis/        # 股票分析
│   ├── market-research-reports/ # 市场研究报告
│   ├── data-analysis-unified/ # 统一数据分析
│   ├── soul-guardian/         # 系统守护
│   ├── skill-creator/         # 技能创建器
│   └── ...
├── scripts/                   # 运维脚本
│   ├── chromium-watchdog.sh   # Chromium 看门狗
│   ├── filesystem-guard.sh    # 文件系统守护
│   ├── session-cleanup.sh     # 会话清理
│   └── workspace-doctor.sh    # 工作区诊断
├── server_knowledge_base/     # 服务器知识库
│   ├── 01_PROJECTS/           # 项目文档
│   ├── 02_SERVICES/           # 服务配置文档
│   ├── 03_ENV_AND_DATA/       # 环境与数据文档
│   └── 04_AUTOMATION/         # 自动化文档
├── vault/                     # 知识体系
│   ├── reference/             # 参考手册
│   └── systems/               # 系统规范
└── cron/                      # 定时任务模板
    └── jobs-template.json
```

## 快速开始

1. 安装 OpenClaw：参考官方文档
2. 复制配置：`cp config/.env.example ~/.openclaw/.env`
3. 编辑 `.env` 填入你的 API 密钥
4. 复制 `config/openclaw.json` 到 `~/.openclaw/openclaw.json`
5. 将 `skills/` 目录复制到 `~/.openclaw/skills/`

## 注意事项

- 所有敏感信息（API 密钥、Token、密码）已替换为占位符
- `openclaw.json` 中的凭据使用 `${ENV_VAR}` 格式引用环境变量，无需修改
- 如需完整备份（含运行时数据），请使用私有仓库

## 更新日期

**2026-03-25** - 从生产服务器同步最新配置
