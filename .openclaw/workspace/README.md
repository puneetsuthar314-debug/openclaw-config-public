# 工作区概览

这是 Claw (赛博助理) 的工作空间，位于 `/root/.openclaw/workspace`。

## 📁 目录结构

```
workspace/
├── 核心文件
│   ├── SOUL.md          # 身份和原则定义
│   ├── IDENTITY.md      # 个人身份信息 (名字、风格等)
│   ├── USER.md          # 用户信息 (马斯克)
│   ├── MEMORY.md        # 长期记忆和重要事项
│   ├── TOOLS.md         # 本地工具和环境配置
│   ├── AGENTS.md        # 工作区使用规范
│   └── HEARTBEAT.md     # 定期检查任务
│
├── memory/              # 每日日志和详细记录
│   ├── 2026-03-08.md    # 当日详细日志
│   └── improvements.md  # 改进记录和经验教训
│
├── tasks/               # 任务管理
│   ├── active/          # 进行中的任务
│   ├── backlog/         # 待办任务池
│   ├── archive/         # 已完成任务归档
│   └── template.md      # 任务模板
│
├── skills/              # 已安装的技能 (49 个)
├── docs/                # 文档和参考资料
├── scripts/             # 自定义脚本工具
├── files/               # 工作文件
├── downloads/           # 下载文件临时目录
├── templates/           # 模板文件（项目模板、文档模板）
├── references/          # 参考资料
├── requirements.txt     # Python 依赖文档
└── .gitignore          # Git 忽略规则
```

## 📝 项目文件组织规则

- **每个项目独立文件夹** - 避免文件混乱
- **命名规范** - `project_项目名称` 或直接使用项目名
- **完成归档** - 项目完成后移动到 `tasks/archive/`

## 🔧 环境信息

- **主机**: 阿里云 ECS (iZ2ze2iybytt1ex18qsfmpZ)
- **系统**: Linux 5.10.134-19.2.al8.x86_64
- **Node**: v22.22.1
- **模型**: dashscope/qwen3.5-plus
- **渠道**: 钉钉 (clawdbot-dingtalk)

## 📌 快速参考

| 需求 | 操作 |
|------|------|
| 启动新项目 | 复制 `templates/极简任务卡.md` → `todo_项目名.md` |
| 查看任务 | `tasks/backlog.md` + `tasks/active/` |
| 查看日志 | `memory/YYYY-MM-DD.md` |
| 查看记忆 | `MEMORY.md` |
| 查看技能 | `skills/` 目录 |
| 临时文件 | `downloads/` 或 `files/` |
| 常用命令 | `QUICKSTART.md` |
| 项目指南 | `QUICKSTART-PROJECT.md` |

## ⚙️ 系统目录

| 目录 | 说明 |
|------|------|
| `.openclaw/` | OpenClaw 系统状态（勿手动修改） |
| `.clawhub/` | ClawHub 技能管理（勿手动修改） |

---

_最后更新：2026-03-08_
