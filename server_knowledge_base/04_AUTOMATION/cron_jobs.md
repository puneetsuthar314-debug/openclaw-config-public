> **核心洞察**：服务器配置了严密的定时任务，主要围绕 OpenClaw 系统的健康、安全、备份和清理。了解这些任务可以避免很多“神秘现象”。

# 04 - 自动化：Cron 定时任务
**最后更新**: `2026-03-25`

## 1. 当前 Crontab 配置
以下是 `root` 用户的当前定时任务列表：

```bash
# OpenClaw 定时任务（由 job-runner 任务守护者包装）
# 每周日 03:30 执行清理
30 3 * * 0 /usr/local/bin/job-runner /usr/local/bin/openclaw-cleanup.sh 300

# 每小时执行健康检查
0 * * * * /usr/local/bin/job-runner /usr/local/bin/openclaw-health-check.sh 120

# Chromium 内存看门狗 — 每 5 分钟检查
*/5 * * * * /root/.openclaw/scripts/chromium-watchdog.sh

# OpenClaw 会话清理（每周日 04:00 执行）
0 4 * * 0 /bin/bash /root/.openclaw/scripts/session-cleanup.sh >> /var/log/openclaw-cleanup.log 2>&1

# 文件系统安全加固（每天 03:30 执行）
30 3 * * * /bin/bash /root/.openclaw/scripts/filesystem-guard.sh >> /var/log/openclaw-security.log 2>&1

# 备份清理（每天 02:00 执行）
0 2 * * * /root/bin/cleanup_backups.sh >> /var/log/openclaw-cleanup.log 2>&1

# 每日自动备份（每天 03:00 执行）
0 3 * * * /root/.openclaw/skills/cron-backup/scripts/backup.sh /root/.openclaw /root/.openclaw/backups .openclaw >> /root/.openclaw/backups/.backup.log 2>&1 # cron-backup-daily

# 备份文件清理（每周日 04:00 执行，保留7天）
0 4 * * 0 /root/.openclaw/skills/cron-backup/scripts/cleanup.sh /root/.openclaw/backups 7 # cron-backup-cleanup

# OpenClaw 工作区自治健康检查（每天 04:30 自动修复）
30 4 * * * /bin/bash /root/.openclaw/scripts/workspace-doctor.sh fix >> /var/log/openclaw-doctor.log 2>&1
```

## 2. 任务详解与影响

### 2.1 清理与维护
- **openclaw-cleanup.sh**: 定期清理 OpenClaw 平台的废弃会话、浏览器缓存和旧日志。**重要文件请勿存放在 `/tmp/openclaw/` 或缓存目录**。
- **session-cleanup.sh**: 专门清理过期的会话数据。
- **cleanup_backups.sh**: 清理 `/root/.openclaw/backups/` 目录下超过 14 天的旧备份文件。

### 2.2 健康与监控
- **openclaw-health-check.sh**: 检查 `openclaw-gateway` 服务的健康状况，并在其崩溃时自动重启。这是服务高可用的保障。
- **chromium-watchdog.sh**: 监控 Chromium 内存占用，防止内存泄漏导致 OOM。
- **workspace-doctor.sh**: 工作区自治健康检查与自动修复。

### 2.3 安全与备份
- **filesystem-guard.sh**: 文件系统安全加固。
- **cron-backup**: 每天自动备份 `.openclaw` 目录，并定期清理旧备份。
