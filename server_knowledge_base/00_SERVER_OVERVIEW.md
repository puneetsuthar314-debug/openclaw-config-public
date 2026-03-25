> **高层洞察**：这是一台**中高配置的单体开发服务器**（4 vCPU / 8GB RAM / 60GB 磁盘）。所有服务和项目都运行在同一个 `root` 用户下，没有容器化或虚拟化隔离。在进行任何操作前，请务必考虑资源占用和潜在的全局影响。

# 00 - 服务器约束与雷区
**最后更新**: `2026-03-25`

## 1. 硬件配置
| 资源 | 规格 | 备注 |
|---|---|---|
| **CPU** | 4 vCPU (Intel Xeon Platinum, 2核4线程) | 足够运行现有所有服务，编译大型项目时性能尚可 |
| **内存 (RAM)** | 7.3 GB (+ 2GB Swap) | 资源充裕。当前使用率约 15%，已用 1.1Gi，可用 6.2Gi。 |
| **磁盘** | 60 GB 总容量 | 根目录 `/` 总容量 59G，已用 32G，可用 25G (使用率 57%)。Anaconda 占 14GB 是最大消耗。 |

## 2. 架构与设计决策
- **单体架构**: 所有应用（游戏后端、OpenClaw、代理）都直接运行在操作系统上。这意味着一个应用的崩溃可能会影响到其他应用。
- **Root 用户主导**: 所有操作均通过 `root` 用户进行。这是一个严重的安全风险，但也简化了权限管理。**操作时请务必谨慎，`rm -rf` 等命令会造成灾难性后果。**
- **开发环境导向**: `ProjectChimera` 后端以 `--reload` 模式运行，表明这是一个开发设置，而非生产环境。服务可能会因文件变动而自动重启。

## 3. 服务管理架构
- **openclaw-gateway**: 由 **system-level systemd 服务** (`/etc/systemd/system/openclaw-gateway.service`) 管理，`enabled` + `Restart=always`。管理命令使用 `systemctl status/stop/start openclaw-gateway`。
- **soul-guardian**: OpenClaw 核心文件完整性监控服务，当前处于 active (running) 状态。
- **nginx**: 监听端口 80（默认）和 8000（文件浏览器前端），worker_processes 设为 auto（自动匹配 4 vCPU）。
- **earlyoom**: OOM 防护守护进程，优先杀 Chromium 保护 OpenClaw。
- **cron 定时任务**: 包含健康检查、清理、备份、安全加固等严密的自动化任务。

## 4. 全局雷区与风险
- **服务器重启**: 服务器重启后，**`ProjectChimera` 后端和 `mihomo` 代理不会自动恢复**，需要手动启动。`openclaw-gateway` 已配置为 systemd enabled 服务（`Restart=always`），**通常**会在重启后自动恢复；此外 cron 每小时健康检查也会兜底拉起。
- **Python 环境**: 系统严重依赖位于 `/root/anaconda3` 的 `base` Conda 环境。**绝对不要轻易删除或修改此目录**，否则 `ProjectChimera` 将立即崩溃。
- **Go 语言环境**: 服务器上安装了 Go (`/root/go/`)，包含 `blogwatcher`, `gifgrep`, `ordercli`, `wacli` 等编译好的二进制工具。

## 5. 实时观察命令速查
不要依赖本文档中的静态数据。请使用以下命令获取服务器的实时状态：
| 任务 | 命令 |
|---|---|
| 查看磁盘使用情况 | `df -h` |
| 查看内存使用情况 | `free -h` |
| 查看网络连接和监听端口 | `ss -tlpn` |
| 查看所有正在运行的进程 | `ps aux` |
| 查看 `root` 用户的定时任务 | `crontab -l` |
| 查看 OpenClaw 服务状态 | `systemctl status openclaw-gateway` |
| 查看 earlyoom 状态 | `systemctl status earlyoom` |

## 6. 历史 Agent 建议存档
> **[2026-03-25]**: 磁盘空间已优化，删除了多余的 `/root/Scrapling` 源码和压缩包，释放了约 21.5MB 空间。OpenClaw 已内置 `scrapling` 技能，无需在 root 目录下保留独立副本。
