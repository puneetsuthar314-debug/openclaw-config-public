# OpenClaw Skills 导航手册

本目录包含所有已安装的 Agent Skills。此文档作为导航指南，帮助 AI 在面对复杂任务时，智能选择最合适的工具组合。

> **AI 必读指南**：
> - 每次对话的系统提示词中已自动注入所有可用 Skills 的基础列表。
> - 本手册提供了更高级的**分类、依赖状态和选择策略**。
> - 当遇到不确定的任务时，请优先参考本手册的分类指引，然后使用 `read` 工具读取对应技能目录下的 `SKILL.md` 获取详细指令。

---

## 🔍 搜索与研究 (Search & Research)

在进行信息收集时，请**严格按照以下优先级**选择工具：

| 技能名称 | 状态 | 适用场景与触发词 | 选择策略 |
|---------|------|-----------------|----------|
| **`unified-search`** | ✅ 可用 | 快速搜索、事实核查、L1/L2/L3 级别调研 | **[首选]** 日常 90% 的搜索任务都应使用此技能。它免费、快速，且支持多源检索。 |
| **`content-fetcher`** | ✅ 可用 | 提取网页正文、下载视频/PDF/图片 | 当用户提供特定 URL，要求"抓取"、"提取"或"下载"时使用。 |

---

## 💬 通讯与多媒体 (Communication & Media)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`image-search-sender`** | ✅ 可用 | 找图并发给用户（如："发一张猫的图片"） | **必须使用此技能**，严禁使用沙箱内的 code_interpreter 下载图片，否则会导致钉钉发送失败。 |
| **`dingtalk-send-media`** | ✅ 可用 | 将本地已存在的文件或图片发送到钉钉 | 仅在需要发送特定文件时调用，底层依赖 `[DING:IMAGE]` 标签。 |
| **`wacli`** | ✅ 可用 | 发送 WhatsApp 消息、搜索/同步聊天记录 | 需要 WhatsApp 账号配对后使用。 |

---

## 🌐 浏览器与自动化 (Browser & Automation)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`agent-browser`** | ✅ 可用 | 网页截图、交互式操作、绕过反爬虫 | 这是重型工具（Headless Chrome），仅当 `content-fetcher` 或普通搜索无法获取内容（如需登录、动态渲染）时才使用。 |
| **`scrapling`** | ✅ 可用 | 高级网页爬取、反爬绕过（Cloudflare Turnstile）、隐身浏览器、Spider 框架、自适应抓取 | 当 `content-fetcher` 无法抓取（反爬保护、动态渲染）或需要编写 Python 爬虫/Spider 时使用。支持 CLI 直接提取和 MCP 服务器。 |

---

## 📊 数据与分析 (Data & Analytics)

| 技能名称 | 状态 | 适用场景与触发词 | 选择策略 |
|---------|------|-----------------|----------|
| **`duckdb-cli`** | ✅ 可用 | CSV/JSON/Parquet 文件分析、SQL 查询 | 处理结构化数据时的首选工具，比 Python pandas 脚本更快、更省内存。 |
| **`summarize`** | ✅ 可用 | 长文本、文档的快速总结 | 当用户要求"总结"、"TL;DR"或提取要点时使用。 |
| **`nano-pdf`** | ✅ 可用 | 用自然语言指令编辑 PDF 文件 | 当用户需要修改 PDF 页面内容时使用。 |

---

## 🔒 安全与运维 (Security & Infra)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`1sec-security`** | ✅ 可用 | 服务器安全监控、入侵检测 | 已安装 1-SEC 引擎。用于响应"检查服务器安全"、"防护 VPS"等请求。 |
| **`dependency-audit`** | ✅ 可用 | 检查 npm/pip 依赖的安全漏洞 | 在开发或审查代码项目时主动使用。 |
| **`cron-backup`** | ✅ 可用 | 设置定时备份、版本追踪 | 当用户要求"定期备份"、"保存当前状态"时使用。 |
| **`healthcheck`** | ✅ 可用 | 主机安全加固、风险评估 | 用于安全审计、防火墙/SSH/更新加固、风险态势检查。 |

---

## 🧠 知识与记忆 (Knowledge & Memory)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`ontology`** | ✅ 可用 | 创建/查询结构化实体（人、项目、任务） | 当前为备用状态。除非用户明确要求建立知识图谱或复杂实体关联，否则优先使用默认的 Markdown 记忆系统。 |

---

## 🛠️ 开发与工具 (Dev & Tools)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`github`** | ✅ 可用 | GitHub 操作（Issue、PR、CI、代码审查） | 通过 `gh` CLI 操作。 |
| **`gh-issues`** | ✅ 可用 | GitHub Issue 管理 | 专注于 Issue 的创建、查询和管理。 |
| **`oracle`** | ✅ 可用 | AI 提示词+文件打包，一次性请求另一模型 | 将 prompt 和文件捆绑发送给其他 AI 模型获取回答。 |
| **`xurl`** | ✅ 可用 | X (Twitter) API 操作 | 发推、回复、搜索、管理关注者等（需 X 开发者账号）。 |
| **`clawhub`** | ✅ 可用 | 搜索、安装、更新、发布 Agent Skills | 从 clawhub.com 获取新技能。 |
| **`skill-creator`** | ✅ 可用 | 创建、编辑、改进 AgentSkills | 用于开发新的 skill 或优化现有 skill。 |
| **`mcporter`** | ✅ 可用 | 管理 MCP 服务器和工具 | 列出、配置、认证和调用 MCP 服务器。 |
| **`tmux`** | ✅ 可用 | 远程控制 tmux 会话 | 发送按键、抓取输出，管理后台进程。 |

---

## 📰 信息与监控 (Info & Monitoring)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`blogwatcher`** | ✅ 可用 | 监控博客和 RSS/Atom 订阅源更新 | 追踪博客和 Feed 的新内容。 |
| **`gifgrep`** | ✅ 可用 | 搜索 GIF 动图 | 按关键词搜索 GIF。 |
| **`weather`** | ✅ 可用 | 获取天气和预报 | 无需 API Key，直接使用。 |
| **`session-logs`** | ✅ 可用 | 搜索和分析历史会话日志 | 查找之前的对话记录。 |
| **`ordercli`** | ✅ 可用 | 查询 Foodora 外卖订单状态 | 需要 Foodora 账号。 |

---

## 🎬 媒体处理 (Media)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`video-frames`** | ✅ 可用 | 从视频中提取帧或缩略图 | 使用 ffmpeg 处理。 |
| **`canvas`** | ✅ 可用 | 在连接的节点上展示 HTML 内容 | 游戏、可视化、仪表板展示。 |
| **`gemini`** | ✅ 可用 | Gemini AI 模型集成 | 通用 AI 能力调用。 |

---

## 🔧 系统与连接 (System)

| 技能名称 | 状态 | 适用场景与触发词 | 注意事项 |
|---------|------|-----------------|----------|
| **`node-connect`** | ✅ 可用 | 诊断 OpenClaw 节点连接和配对问题 | 排查 Android/iOS/macOS 伴侣应用连接故障。 |

---

## ❌ 已卸载/不可用的技能

为避免幻觉，请注意以下技能**已从系统中移除或不可用**，切勿尝试调用：

- 🚫 `agent-deep-research` (无 GEMINI_API_KEY，已卸载)
- 🚫 `apple-notes` / `apple-reminders` / `bear-notes` / `imsg` / `things-mac` / `peekaboo` / `model-usage` / `sherpa-onnx-tts` (仅限 macOS，已卸载)
- 🚫 `goplaces` / `nano-banana-pro` / `notion` / `openai-image-gen` / `openai-whisper-api` / `sag` / `trello` (缺少 API Key，已卸载)
- 🚫 `coding-agent` / `openai-whisper` / `spotify-player` / `gog` / `himalaya` / `1password` / `obsidian` / `songsee` (缺少 CLI 工具且无法安装，已卸载)
- 🚫 `blucli` / `sonoscli` / `camsnap` / `openhue` / `eightctl` (需要特定硬件，已卸载)
- 🚫 `bluebubbles` / `discord` / `slack` / `voice-call` (缺少通道/插件配置，已卸载)
- 🚫 `llmfit` (服务器无 GPU/Ollama，已卸载)
- 🚫 `domain-trust-check` (无 API Key，已卸载)
- 🚫 `ggshield-scanner` (无 API Key，已卸载)
