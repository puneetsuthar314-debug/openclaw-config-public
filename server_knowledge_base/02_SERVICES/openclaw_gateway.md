> **核心洞察**：这是一个由 `systemd` 管理的 Node.js 服务，同时受 `cron` 健康检查脚本双重保护。`systemd` 负责秒级自动重启，`cron` 负责每小时兜底检查和搜索配置修复。但需警惕 **systemd 崩溃循环**：如果服务反复启动失败，systemd 会在达到重启次数上限后彻底放弃，导致服务停止且不再自动恢复。

# 02 - 服务：OpenClaw Gateway

**最后更新**: `2026-03-19`

## 1. 服务管理架构

OpenClaw Gateway 当前采用 **systemd + cron 双重保活** 架构：

| 层级 | 机制 | 行为 | 恢复速度 |
|------|------|------|---------|
| **第一层** | systemd (`Restart=always`, RestartSec=5) | 进程退出后 5 秒自动重启 | 秒级 |
| **第二层** | cron 健康检查 (每小时) | 检查进程和端口，必要时重启；同时修复搜索配置 | 最长 1 小时 |

> **操作雷区：崩溃循环陷阱**：如果 gateway 因配置错误等原因反复启动失败，systemd 会在达到 `start-limit-burst` 上限后**彻底停止重启尝试**，服务状态变为 `inactive (dead)`。此时必须手动介入：先修复根本问题，然后执行 `systemctl reset-failed openclaw-gateway && systemctl start openclaw-gateway`。

## 2. 如何正确管理服务

| 任务 | 首选命令 | 备注 |
|---|---|---|
| **启动服务** | `systemctl start openclaw-gateway` | 通过 systemd 启动，享受自动重启保护 |
| **重启服务** | `systemctl restart openclaw-gateway` 或 `openclaw gateway restart` | 两者均可 |
| **停止服务** | `systemctl stop openclaw-gateway` | 服务会被 cron 在下一个小时拉起，如需永久停止需同时 `systemctl disable` |
| **查看状态** | `systemctl status openclaw-gateway` | 查看 systemd 管理的服务状态 |
| **查看日志** | `tail -f /var/log/openclaw-gateway.log` | gateway 主日志 |
| **查看健康检查日志** | `tail -f /var/log/openclaw-health.log` | 健康检查和 post-start 脚本的日志 |
| **重置崩溃计数器** | `systemctl reset-failed openclaw-gateway` | 当服务因崩溃循环被 systemd 放弃后，必须先执行此命令 |

## 3. 故障排查指南

- **如果服务状态为 `inactive (dead)` 且不自动恢复**:
  1. 检查 `journalctl -u openclaw-gateway -n 50` 查看是否进入了崩溃循环（restart counter 持续增长）。
  2. 检查 `/var/log/openclaw-gateway.log` 末尾的错误信息，定位根本原因。
  3. 修复问题后执行 `systemctl reset-failed openclaw-gateway && systemctl start openclaw-gateway`。
- **如果进程存在但端口 `18789` 未监听**:
  - 服务内部可能在启动时遇到了问题。检查 `openclaw.json` 配置或 `/tmp/openclaw/openclaw-*.log` 内部日志。
- **如果搜索功能被禁用**:
  - DingTalk 插件启动时会自动将 `tools.web.search.enabled` 设为 `false`，而 `post-start.sh` 脚本会将其改回 `true`。这是一个已知的"拉锯战"，通常 post-start 脚本会最终胜出。

## 4. 关联性

- **与 ProjectChimera 的关系**: **无**。经过代码和配置分析，此服务与 `ProjectChimera` 没有任何已知的直接关联。
- **核心数据**: 所有数据和配置均位于 `/root/.openclaw/` 目录，是服务的生命线。
- **systemd 服务文件**: `/etc/systemd/system/openclaw-gateway.service`（enabled，包含 OOM 保护和安全加固）

## 5. 端口清单

| 端口 | 进程 | 用途 |
|------|------|------|
| 18789 | openclaw-gateway | 主 API 端口（WebSocket + HTTP） |
| 18791 | openclaw-gateway | 浏览器控制端口（auth=token） |
| 18792 | openclaw-gateway | 用途待确认 |
| 18800 | chromium-browser | CDP 远程调试端口 |

---

## 历史 Agent 建议

> **[2026-03-16] Agent 建议**: OpenClaw 的 MCP filesystem 配置位于 `/root/.openclaw/mcp.json`，其中定义了 Agent（如"丫丫"）可访问的目录白名单。如果需要让 Agent 访问新目录（如 `/root/server_knowledge_base/`），必须将路径添加到该配置文件的 `filesystem.args` 数组中，然后执行 `openclaw gateway restart` 使配置生效。注意：`openclaw gateway restart` 实际上重启的是 systemd 服务，但重启后进程会正常运行并监听端口 18789。

> **[2026-03-16] Agent 建议**: 健康检查日志中频繁出现 `[ALERT] 端口18789未监听` 和 `搜索功能被禁用，自动启用` 的警报。这表明 gateway 在 cron 检查时可能存在短暂的端口未就绪状态，健康检查脚本会自动修复搜索功能配置。此外，重启后可能出现 `浏览器自动启动失败` 的日志，但不影响 gateway 核心功能。

> **[2026-03-17] Agent 建议 (浏览器搜索操作)**:
> 1. 百度首页的搜索框是一个 `textarea` 元素而非普通 `input`，使用 `openclaw browser type <ref> "关键词"` 时不要加 `--submit` 参数，因为 `--submit` 会尝试按 Enter，但 textarea 的 Enter 行为可能超时。正确做法是：先 `type` 输入文字（不加 `--submit`），然后用 `openclaw browser click <百度一下按钮ref>` 点击搜索按钮触发搜索。
> 2. 在百度首页点击搜索框 (`click`) 后，页面可能会切换到"AI搜索"模式，导致 DOM 结构变化、ref 编号重新分配。建议在 `click` 搜索框后重新执行 `snapshot --labels` 获取最新的 ref 编号。
> 3. 实测发现：即使 `type` 命令报超时错误，文字实际上可能已经成功输入并触发了搜索（百度有输入即搜的行为）。遇到超时错误时，先用 `snapshot` 检查当前页面状态，不要盲目重试。

> **[2026-03-17] Agent 建议 (大模型配置快照)**:
> OpenClaw 当前通过 DashScope 统一接入以下 8 个大模型，配置文件位于 `/root/.openclaw/openclaw.json`：
> - **Qwen3.5 Plus** (`qwen3.5-plus`) — 推理模型，100万上下文，主控 Agent "丫丫-主控" 的主模型，也是全局默认模型
> - **Qwen3 Max** (`qwen3-max-2026-01-23`) — 推理模型，262K上下文，"丫丫-研究" Agent 的回退模型（主模型已切换为 Kimi K2.5）
> - **Qwen3 Coder Next** (`qwen3-coder-next`) — 非推理模型，262K上下文
> - **Qwen3 Coder Plus** (`qwen3-coder-plus`) — 非推理模型，100万上下文，"丫丫-编码" Agent 的主模型，也是 subagents 默认模型
> - **MiniMax-M2.5** — 推理模型，200K上下文，别名 minimax
> - **GLM-5** — 推理模型，202K上下文，别名 glm5
> - **GLM-4.7** — 推理模型，169K上下文，别名 glm4，也用于 heartbeat 心跳检查
> - **Kimi K2.5** (`kimi-k2.5`) — 推理模型，262K上下文，别名 kimi，同时作为图像模型使用
> 所有模型均通过 DashScope 的 `https://coding.dashscope.aliyuncs.com/v1` 端点接入。

---

## 💡 建议：丫丫智能提升方案 (2026-03-17 Manus 审计)

### 诊断摘要

当前丫丫已具备三 Agent 分工、完善的 system prompt 体系、lossless-claw 插件、memory flush 机制。但以下短板制约了智能上限：

| 短板 | 影响 | 优先级 |
|------|------|--------|
| MCP 工具已扩展为 3 个 | filesystem + fetch + playwright | 已解决 |
| 无 model fallback | 主模型失败时无自动降级 | P0 |
| 无外部 Provider (OpenRouter) | 无法使用 Claude/GPT 等更强模型 | P1 |
| mihomo 代理未激活 | 海外 API 不可达 | P1 |
| system prompt 注入文件可能超 8KB | 上下文浪费 | P2 |

### 推荐操作

**P0 - 零成本立即可做：**
1. ~~在 openclaw.json 中添加 model fallbacks~~ **已完成**：三个 Agent 均已配置 fallback 链
2. 添加 Tavily MCP（免费 1000次/月搜索）或 SearXNG MCP（自托管）
3. 检查核心注入文件总大小，确保 < 8KB

**P1 - 低成本高回报：**
1. 注册 OpenRouter 免费账户，接入免费模型（Gemini Flash、DeepSeek 等）
2. 启动 mihomo 代理，打通海外 API 通道
3. 配置 model fallbacks 跨 provider：dashscope → openrouter

**P2 - 长期投资：**
1. 购买 OpenRouter 付费额度，关键任务用 Claude Sonnet
2. 安装 Playwright MCP 替代自定义 Playwright 脚本
3. 考虑 Cognetivy（开源记忆增强框架）


---

## 💡 建议：MCP 工具扩展方案 (2026-03-17 Manus 审计)

### 验证结论
- Tavily API (api.tavily.com) 国内可直连，HTTP 200
- GitHub API (api.github.com) 国内可直连，HTTP 200
- DuckDuckGo 国内被墙，需代理
- @playwright/mcp v0.0.68 npm 可用，服务器已有 Playwright + Chromium
- tavily-mcp npm 可用

### 推荐 MCP 扩展（按优先级）

| 优先级 | MCP | 包名 | 需要 API Key | 内存 |
|--------|-----|------|-------------|------|
| P0 | Tavily 搜索 | tavily-mcp | 是(免费1000次/月) | ~50MB |
| P0 | Playwright 浏览器 | @playwright/mcp | 否 | ~50MB+浏览器 |
| P1 | GitHub | @anthropic-ai/mcp-github | 是(PAT) | ~30MB |
| P1 | Sequential Thinking | @anthropic-ai/mcp-sequential-thinking | 否 | ~30MB |

### 注意事项
- 服务器已升级至 7.3GB RAM，内存资源充裕，可同时安装多个 MCP 工具
- Playwright MCP 必须加 --headless 参数
- 安装后需同步更新 TOOLS.md 中的工具优先级


> **[2026-03-17] Agent 建议 (配置审计 by Manus)**:
> 1. **MCP 工具已扩展为 3 个**：当前 `mcp.json` 中已配置 `filesystem`、`fetch` 和 `playwright`（headless 模式）。之前文档中"MCP 工具仅 filesystem + fetch"的描述已过时。
> 2. **DingTalk 集成已上线**：`clawdbot-dingtalk` 插件已启用，集成了阿里云 MCP（webSearch、codeInterpreter、webParser、wan26Media），使用独立的 API Key `sk-xxxx-REDACTED-xxxx`。
> 3. **搜索配置的"拉锯战"**：`openclaw.json` 中 `tools.web.search.enabled` 默认为 `false`，但 `openclaw-post-start.sh` 脚本会在每次 gateway 启动后自动将其改为 `true` 并通过 SIGHUP 热加载。同时 DingTalk 插件启动时也会干预此配置（auto-disable core web_search）。这导致搜索配置在启动过程中被多次修改，可能产生竞态条件。
> 4. **systemd 服务已配置完善**：`openclaw-gateway.service` 已设置为 `enabled` + `Restart=always`（RestartSec=5），包含 OOM 保护（`OOMScoreAdjust=-500`）和安全加固（`NoNewPrivileges`、`ProtectSystem=full` 等）。不再仅依赖 cron 健康检查来保活。
> 5. **端口清单**：gateway 运行时监听 3 个端口：18789（主 API）、18791（浏览器控制）、18792（用途待确认）。Chromium 监听 18800（CDP 远程调试）。

> **[2026-03-17] Agent 建议 (双 systemd 服务冲突)**:
> 发现服务器上同时存在两个 openclaw-gateway 的 systemd 服务：
> 1. **System-level**: `/etc/systemd/system/openclaw-gateway.service`（手动创建，使用 `openclaw gateway` 命令启动）
> 2. **User-level**: `/root/.config/systemd/user/openclaw-gateway.service`（由 `openclaw` 自动生成，使用 `node ... gateway --port 18789` 启动）
>
> 这两个服务会互相竞争端口 18789，导致新启动的实例因 "Port 18789 is already in use" 而反复崩溃。systemd 的 `Restart=always` 策略使得两者形成死亡循环——每次重启都会因端口被对方占用而失败。
>
> **[2026-03-19 更新] 解决方案**: 双服务冲突已解决。当前 **system-level 服务为主服务**（`/etc/systemd/system/openclaw-gateway.service`，enabled + active），user-level 服务已停用（inactive/dead）。管理命令统一使用 `systemctl status/stop/start openclaw-gateway`。system-level 服务已添加 MemoryLimit=6G 和崩溃循环保护（StartLimitBurst=10/600s）。
> **[2026-03-17] Agent 建议**: 经审计（已过时），OpenClaw 曾短暂使用 GLM-5 作为主控，**当前已切换回 Qwen3.5-Plus 作为主控大脑**，并根据任务类型自动路由至 Qwen3 Coder Plus、Kimi K2.5、Qwen3 Max 等专家模型。系统运行稳定，资源占用正常。

---

## Agent 建议 (2026-03-17 性能分析)

> **来源**: Manus 基于 4 个数据源、10 万+ 行日志的深度分析

### 崩溃循环根因已确认

config-audit 日志证实：搜索配置拉锯战是崩溃循环的直接原因。每次启动 → DingTalk 禁用搜索 → post-start 修复 → 配置写入 → 触发 reload/重启 → 循环。3月17日仅配置变更就达 205 次。

### 关键性能数据

| 指标 | 值 |
|------|-----|
| OpenClaw 正常内存 | 260-350 MB |
| OpenClaw 峰值内存 | 481 MB |
| Chromium 峰值内存 | 681 MB（触发告警） |
| 系统内存使用率 | 25%-70%，平均 59% |
| 磁盘使用率 | 68%-89%，24 次超 85% 告警 |
| 历史总启动次数 | 4,184 次 |
| 历史总失败次数 | 4,104 次（98.1%） |
| 最高重启计数器 | 4,051 |

### P0 建议

1. **解决搜索配置拉锯战**：在 DingTalk 插件中禁用其自动管理 web.search 的行为，或锁定 openclaw.json 中的搜索配置
2. **配置 systemd 重启限制**：添加  和 ，避免无限重启

### P1 建议

3. **Chromium 自动重启**：健康检查脚本检测到内存 >500MB 时自动重启浏览器
4. **磁盘清理频率提升**：从每周改为每三天

> **[2026-03-17] Agent 建议**: 已将 openclaw.json 中 agents.defaults.model.primary 从 dashscope/qwen3.5-plus 修改为 dashscope/glm-5，使 GLM-5 临时成为系统级默认主控模型。**注：后续已切换回 qwen3.5-plus**。修改前已备份为 openclaw.json.bak.pre-glm5。重启后日志确认 agent model: dashscope/glm-5 生效，端口 18789/18791/18792 正常监听。

> **[2026-03-17] Agent 建议**: 已对 8 个模型进行全流程 API 调用验证，全部通过。响应时间分布：Coder 系列和 Kimi 最快（1-1.5s），GLM 系列中等（10-16s），Qwen3.5 Plus 和 MiniMax 较慢（18-20s）。GLM-5 曾短暂作为主控大脑。**注：当前主控已切换回 qwen3.5-plus，Researcher 已切换为 kimi-k2.5，三个 Agent 均已配置 fallbacks。**

---

## Agent 建议 (2026-03-17 优化方案)

> **来源**: Manus 第三次全面审计

### 紧急发现

1. **服务处于 disabled 状态**：`systemctl is-enabled` 返回 disabled，服务器重启后不会自启
2. **ExecStartPost 未配置**：systemd 服务文件中没有 ExecStartPost，post-start.sh 从未被 systemd 调用
3. **当前主模型为 qwen3.5-plus**（曾短暂切换为 glm-5，已切回）
4. **搜索配置当前为 false**（openclaw.json 中），但 config get 返回 true（内存中）

### 必须执行的修复

- `systemctl enable openclaw-gateway` — 启用开机自启
- 在 service 文件中添加 `ExecStartPost=/usr/local/bin/openclaw-post-start.sh`
- 添加 `StartLimitIntervalSec=600` 和 `StartLimitBurst=5`

> **[2026-03-17] Agent 建议**: 成功实现双搜索共存方案。关键步骤：(1) 设置 channels.clawdbot-dingtalk.aliyunMcp.tools.webSearch.enabled=false 禁用插件的 web_search；(2) 修补了 /usr/lib/node_modules/clawdbot-dingtalk/dist/index.js，在工具注册循环中加入 enabled 检查（原插件无条件注册所有工具，不检查 enabled 状态）；(3) 启用内置搜索 tools.web.search.enabled=true, provider=kimi；(4) 通过 MCPorter 接入阿里云 WebSearch MCP 作为独立工具。注意：插件更新后需要重新打补丁。备份位于 index.js.bak。

> **[2026-03-17] Agent 建议**: 模型路由方案已验证落地。关键发现：vault/systems/model-routing.md 不会被自动注入 system prompt，必须将路由规则核心内容直接嵌入 AGENTS.md 才能生效。session_status 工具是模型切换的唯一途径，CLI 临时 session 不支持切换（Unknown sessionId），仅钉钉等持久化 session 可用。长文写作任务（>2000字）可能超时，建议增加 timeoutSeconds 到 120。

> **[2026-03-17] Agent 建议**: 8 模型全角色路由测试通过。GLM-5 能准确调度 Qwen3 Coder、Qwen3 Max、MiniMax、Kimi 等所有专家模型。建议将 openclaw.json 中的 agents.defaults.timeoutSeconds 调整为 120 秒，以防止长文写作和复杂视觉任务超时。

> **[2026-03-17] Agent 建议**: 深度分析 OpenClaw 架构后发现：(1) 搜索配置拉锯战问题仍存在，建议在 clawdbot-dingtalk 插件配置中固定 search.enabled=true，避免与 post-start.sh 冲突；(2) 历史崩溃率 98.1% (4184次启动/4104次失败) 需要关注，建议检查 journalctl 中的具体失败原因并分类统计；(3) Chromium 内存峰值 681MB，建议在 health-check 脚本中增加浏览器内存阈值告警（如超过 500MB 自动重启浏览器）；(4) 核心注入文件总大小需控制在 8KB 以内，当前 AGENTS.md 内容较多，可考虑将模型路由规则迁移到 vault/systems/ 中按需加载。

> **[2026-03-17] Agent 建议**: A 股深度调研 cron 任务已重建。旧任务 ID 为 a-stock-research-20min（已被删除），新任务 ID 为 d2a98c28-de68-4ec6-98e5-695b76708737。改进点：(1) 升级了调研脚本 a-stock-full-research.py v2，新增优先级逻辑（先处理已有目录但 outputs 为空的股票，再处理新股票）；(2) 股票列表从 75 只扩展到 79 只（补充了 TCL 科技、中兴通讯、云南白药、平安银行）；(3) 使用 dashscope/qwen3-max-2026-01-23 模型以提高报告质量；(4) 报告 prompt 更详细，要求包含 8 大章节和具体数据表格。截至重建时已完成 13/79 只，剩余 66 只将每 20 分钟自动执行一只。

> **[2026-03-18] Agent 建议**: 全面健康诊断发现 6 个问题：(1) **Chromium 内存泄漏极其严重**，每小时增长约 2GB，3-4 小时后触发 OOM Killer (峰值 5.9GB)，健康检查脚本只记录警告但不执行重启，建议在 health-check 中当 Chromium 超过 1GB 时自动执行 browser stop/start；(2) **System-level 服务处于无限崩溃循环**，虽然 disabled 但仍在运行，今天已崩溃 2232 次(累计 3893 次)，原因是端口 18789 被 user-level 服务占用，必须执行 systemctl mask openclaw-gateway 彻底阻止；(3) 健康检查脚本的 ss -tlnp 端口检测在 cron 环境下无法检测到 user-level 服务的端口，导致每小时误报，建议改用 curl 或 nc 检测；(4) memory-core 插件缺失，每次启动都有警告；(5) 阿里云百炼 MCP webParser 触发 429 限流。

> **[2026-03-18] Agent 建议 (验证与优化)**: 对 6 个诊断问题进行了实时验证测试，确认 4 个完全存在、1 个部分确认、1 个未复现。关键发现：(1) Chromium 内存泄漏已确认，30 秒内增长 17MB，推荐在健康检查脚本中增加自动重启逻辑（阈值 1.5GB）并增加每 15 分钟的独立监控 cron 任务；(2) system-level 服务崩溃循环已确认（今天 2277 次），必须用 systemctl mask 而非 disable 来彻底屏蔽；(3) 端口检测误报根因是 cron 环境缺少 XDG_RUNTIME_DIR 和 DBUS_SESSION_BUS_ADDRESS，建议改用 bash /dev/tcp 伪设备检测；(4) MCP 429 限流未复现，属间歇性问题。

> **[2026-03-18] Agent 建议 (增强版优化)**: 经 8 方向广泛深搜后发现更优方案：(1) Chromium 应移除 --single-process 并改用 --headless=new + --js-flags=--max-old-space-size=2048，预计降低内存增长 50-70%；(2) 建议安装 nohang OOM 守护进程作为系统级内存防护；(3) 建议为 user-level 服务添加 systemd MemoryHigh=3G + MemoryMax=5G 分级限制；(4) 长期建议 Docker 容器化 Chromium 实现物理级内存隔离；(5) 建议用 PM2 替代 systemd 管理 Node.js 进程以获得更精细的内存管理；(6) 推荐 Beszel 作为轻量监控方案替代 Prometheus/Grafana。

> **[2026-03-18] Agent 建议**: 可行性评估发现增强版方案中6个方案不可行或不必要：(1) 服务器使用 cgroups v1 而非 v2，MemoryHigh/MemoryMax 完全不可用，必须用 MemoryLimit；(2) --single-process 非内存泄漏根因，移除后多进程模式在低内存环境反而更耗内存，应采用定期重启策略；(3) --max-old-space-size 仅限制 V8 堆，无法控制 DOM/GPU/网络缓存等内存；(4) PM2 与 systemd 双重管理冲突，对子进程内存监控无效；(5) Docker 容器化与 cgroups 直接限制重复；(6) Hindsight 需 16GB+ 内存完全不可行。推荐方案：earlyoom 替代 nohang、MemoryLimit 替代 MemoryMax、移动服务文件替代 mask、定期重启 Chromium 替代调参。

> **[2026-03-18] Agent 建议**: 已完成全面优化：(1) 彻底停止 system-level 崩溃循环（移动服务文件而非 mask）；(2) 安装 earlyoom v1.6.2 作为 OOM 防护，优先杀 Chromium 保护 OpenClaw；(3) 为 user-level 服务添加 MemoryLimit=5G（cgroups v1 兼容）；(4) 修复健康检查脚本：端口检测从 ss→curl，Chromium 内存阈值从 500MB→3GB 并添加自动重启逻辑；(5) 新增 chromium-watchdog.sh 看门狗脚本（每 2 小时 cron）；(6) 清理磁盘释放约 1GB。Chromium 内存从 5.8GB 降至 253MB。关键发现：openclaw browser restart 命令不存在，正确方式是 kill+browser start；cron 环境下 ss 命令确实无法检测 user-level 端口。

> **[2026-03-18] Agent 建议**: OpenClaw 存在严重的"假行动"（幻觉）问题 — AI 助手在回答服务状态类问题时，不执行工具验证就凭"记忆"编造答案（如声称 file-browser 在 172.16.50.229:5000 运行，实际未运行）。根因是 SOUL.md 中的"先查后答"原则缺乏强制执行机制。修复方案：(1) 在 SOUL.md 中添加「验证优先原则」完整协议，包含触发条件、执行流程、具体命令和正反示例；(2) 在 AGENTS.md 中增加「预执行检查协议」表格；(3) 创建 memory/services.md 服务状态追踪文件；(4) 调整 GLM-5 的 temperature 为 0.3 并启用 enable_thinking；(5) 配置 memoryFlush 防止压缩后遗忘。详见 /home/ubuntu/OpenClaw_假行动修复方案.md。

> **[2026-03-18] Agent 建议**: 假行动（幻觉）修复方案可行性评估完成。6个方案中：L1需精简至450字节+vault外化（原方案超8KB限制）；L2应合并到L1（空间不足）；L3可行但需防副作用；L4推翻（dist/index.js中无temperature代码）；L5推翻（当前版本不支持memoryFlush）；L6完全可行。核心修复策略：SOUL.md精简核心指令+vault/systems/verification-protocol.md详细协议。注入文件8KB限制是最大约束，当前已用6594字节仅剩1598字节，任何修改都需精确计算字节数。

> **[2026-03-18] Agent 建议**: 假行动修复已全部执行并验证通过。具体变更：(1)SOUL.md追加"验证优先"强制规则(+467字节,总7061/8192=86%,剩余1131字节)；(2)vault/systems/verification-protocol.md创建完整协议(4264字节,含触发条件表、5步流程、3个正反示例、预执行检查表)；(3)memory/services.md创建服务状态索引(1311字节,每个服务含验证命令)；(4)MEMORY.md追加"记忆保鲜"规则(+126字节)；(5)/root/scripts/detect_fake_actions.sh假行动检测脚本(2638字节,cron每6小时运行)。注意：注入文件空间仅剩1131字节，后续修改需谨慎计算。
