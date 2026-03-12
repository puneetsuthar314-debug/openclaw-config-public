# 定时任务使用指南

*版本：2.0 - 支持执行次数限制*

---

## 🆕 新功能：执行次数限制

现在可以为定时任务设置：

| 限制类型 | 字段 | 说明 |
|----------|------|------|
| **最大执行次数** | `limits.maxRuns` | 任务最多执行多少次后自动禁用 |
| **过期时间** | `limits.expireAt` | ISO 格式时间，到期自动禁用 |

---

## 📝 任务配置示例

### 示例 1：讲笑话 10 次后停止

```json
{
  "id": "joke-task-001",
  "name": "陈玺翔笑话连播",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "*/5 * * * *",
    "tz": "Asia/Shanghai"
  },
  "limits": {
    "maxRuns": 10,
    "currentRuns": 0
  },
  "payload": {
    "kind": "agentTurn",
    "message": "@陈玺翔 来听个笑话！😄"
  },
  "delivery": {
    "mode": "announce",
    "channel": "clawdbot-dingtalk",
    "to": "dingtalk:group:xxx"
  }
}
```

### 示例 2：24 小时后过期的提醒

```json
{
  "id": "temp-reminder-001",
  "name": "临时提醒",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 * * * *",
    "tz": "Asia/Shanghai"
  },
  "limits": {
    "expireAt": "2026-03-09T18:00:00+08:00"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "提醒内容"
  },
  "delivery": {
    "mode": "announce",
    "channel": "clawdbot-dingtalk",
    "to": "target"
  }
}
```

### 示例 3：同时设置次数和过期时间

```json
{
  "limits": {
    "maxRuns": 10,
    "currentRuns": 0,
    "expireAt": "2026-03-09T18:00:00+08:00"
  }
}
```

---

## 🔧 管理命令

```bash
# 查看所有任务
python /root/.openclaw/workspace/scripts/cron-manager.py list

# 检查并禁用达到限制的任务
python /root/.openclaw/workspace/scripts/cron-manager.py check

# 手动增加执行计数（调试用）
python /root/.openclaw/workspace/scripts/cron-manager.py increment <task-id>
```

---

## 📋 快速创建任务

### 方式 1：直接编辑 jobs.json

```bash
# 备份
cp /root/.openclaw/cron/jobs.json /root/.openclaw/cron/jobs.json.backup

# 编辑
nano /root/.openclaw/cron/jobs.json
```

### 方式 2：使用模板

```bash
cp /root/.openclaw/cron/jobs-template.json /tmp/new-task.json
# 编辑后合并到 jobs.json
```

---

## ⚠️ 注意事项

1. **每次创建限时任务前，先确认是否需要限制**
2. **达到限制的任务会自动禁用**，不会删除（可手动重新启用）
3. **过期任务会保留记录**，方便追溯
4. **建议为临时任务设置限制**，避免遗忘

---

## 📊 Cron 表达式参考

| 表达式 | 含义 |
|--------|------|
| `30 7 * * *` | 每天 7:30 |
| `*/5 * * * *` | 每 5 分钟 |
| `0 * * * *` | 每小时整点 |
| `0 0 * * *` | 每天午夜 |
| `0 0 * * 1` | 每周一午夜 |
| `30 6,18 * * *` | 每天 6:30 和 18:30 |

---

*最后更新：2026-03-08*
