# workspace-doctor — 工作区自治健康检查

## 概述

自动检测和修复 OpenClaw 工作区中的常见问题，包括：
- 核心文件中的模型配置与 openclaw.json 不一致
- .bak / .tmp 垃圾文件堆积
- MEMORY.md 膨胀（混入技能文档）
- 项目目录命名冲突（空格/重复/空目录）
- IDENTITY.md 未初始化
- 权限配置矛盾

## 使用方式

### 手动检查（仅报告，不修改）
```bash
/root/.openclaw/scripts/workspace-doctor.sh check
```

### 自动修复（检查并修复安全问题）
```bash
/root/.openclaw/scripts/workspace-doctor.sh fix
```

### 生成报告
```bash
/root/.openclaw/scripts/workspace-doctor.sh report
```

报告输出到 `memory/doctor-report-YYYYMMDD.md`

## 自动化

已配置 cron 任务，每天 04:30 自动运行 fix 模式：
```
30 4 * * * /bin/bash /root/.openclaw/scripts/workspace-doctor.sh fix
```

## 触发时机

以下情况应主动运行 check：
1. 修改了 openclaw.json 中的模型配置后
2. 安装了新技能后
3. 用户反馈 Agent 行为异常或"失忆"时
4. 每周例行维护时

## 设计原则

- **check 模式绝不修改任何文件**，只输出诊断报告
- **fix 模式只修复确定安全的问题**（如删除 .bak、清理空目录）
- 涉及内容变更的问题（如模型描述不匹配）会在报告中标注，需人工确认
- 所有操作记录到 /var/log/openclaw-doctor.log
