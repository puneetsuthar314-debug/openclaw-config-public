# 脚本工具集

本目录包含自定义脚本工具，用于扩展 OpenClaw 功能。

## ✅ 功能测试状态 (2026-03-08 23:58)

所有 7 个脚本语法检查通过：
- ✅ auto-backup.py
- ✅ check-group-tasks.py
- ✅ course_reminder.py
- ✅ cron-manager.py
- ✅ daily-skill-review.py
- ✅ task-manager.py
- ✅ weekly-cleanup.py

**依赖**: 仅使用 Python 标准库，无需额外安装

## 📜 脚本列表

| 脚本 | 用途 | 状态 |
|------|------|------|
| `auto-backup.py` | 自动备份工作区重要文件 | ✅ 可用 |
| `check-group-tasks.py` | 检查群聊任务状态 | ✅ 可用 |
| `course_reminder.py` | 课表提醒脚本 | ✅ 可用 |
| `cron-manager.py` | 定时任务管理器 | ✅ 可用 |
| `daily-skill-review.py` | 每日技能回顾 | ✅ 可用 |
| `task-manager.py` | 任务管理工具 | ✅ 可用 |
| `weekly-cleanup.py` | 每周清理脚本 | ✅ 可用 |

## 🔧 使用方法

```bash
# 运行脚本
/root/anaconda3/bin/python3 /root/.openclaw/workspace/scripts/脚本名.py

# 查看脚本权限
ls -la /root/.openclaw/workspace/scripts/
```

## 📝 添加新脚本

1. 在 `scripts/` 目录创建 `.py` 文件
2. 添加执行权限：`chmod +x 脚本名.py`
3. 在此文件添加说明

## 🗓️ 维护建议

- 每周运行 `weekly-cleanup.py` 清理临时文件
- 每月检查脚本是否需要更新
- 废弃脚本移到 `scripts/archive/`

---

_最后更新：2026-03-08_
