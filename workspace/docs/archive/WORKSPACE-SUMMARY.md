# 工作区整理报告

*最后更新：2026-03-08 18:25 | 版本：最终版*

---

## 📁 根目录（7 个核心文件）

```
/root/.openclaw/workspace/
├── AGENTS.md         ← 📘 工作流程指南（含 todo_XXX.md 使用原则）
├── SOUL.md           ← 🧬 人格定义
├── USER.md           ← 👤 用户信息（以勒）
├── MEMORY.md         ← 🧠 长期记忆
├── IDENTITY.md       ← 🎭 身份定义（爪爪 🦞）
├── TOOLS.md          ← 🔧 工具配置笔记
└── HEARTBEAT.md      ← 💓 心跳任务配置
```

**原则：** 根目录只保留核心配置文件，临时文件用完即清理

---

## 📚 docs/ - 文档中心（13 个文件）

```
docs/
├── AGENT-PROFILE.md          ← 完整档案
├── SKILLS-GUIDE.md           ← 技能快速选择指南
├── WORKSPACE-SUMMARY.md      ← 本文件
├── CRON-GUIDE.md             ← 定时任务使用指南
├── AGENTS.md                 ← 核心文档副本
├── SOUL.md                   ← 核心文档副本
├── USER.md                   ← 核心文档副本
├── TOOLS.md                  ← 核心文档副本
├── IDENTITY.md               ← 核心文档副本
├── MEMORY.md                 ← 核心文档副本
├── HEARTBEAT.md              ← 核心文档副本
├── BOOTSTRAP.md              ← 启动文档副本
└── skill-recommendations.md  ← 技能推荐
```

---

## 📋 tasks/ - 任务档案

```
tasks/
├── template.md               ← 大型任务规划模板
├── backlog.md                ← 想法收集池
├── archive/                  ← 已完成任务归档
│   ├── global-todo-2026-03-08.md  ← 废弃的全局入口（保留参考）
│   └── 2026-03.md            ← 月度归档
├── active/                   ← 活跃任务（独立文件）
│   └── README.md
├── completed/                ← 已完成任务
└── backlog/                  ← 待评估想法
```

### todo_XXX.md 使用原则

| 场景 | 操作 |
|------|------|
| 大型复杂任务 | 创建 `todo_任务名.md` |
| 简单任务 | 直接执行，不创建文件 |
| 任务完成 | 归档到 `tasks/archive/` 或删除 |

**详见：** `AGENTS.md` "Every Session" 章节

---

## 🛠️ skills/ - 技能包（32 个）

### 📊 数据分析（7 个）
- `stock-analysis` - 股票分析
- `exploratory-data-analysis` - 探索性数据分析
- `market-research-reports` - 市场研究报告
- `csv-summarizer` - CSV 数据汇总
- `similarweb-analytics` - 网站流量分析
- `data-analyzer` - 数据分析
- `time-tracker` - 时间追踪

### 📝 内容创作（6 个）
- `content-writer` - 多平台内容生成
- `content-ideas-free` - 内容创意
- `writing-assistant` - 写作助手
- `content-research-writer` - 内容研究写作
- `youtube-transcript` - YouTube 字幕提取
- `article-extractor` - 文章提取

### 📁 文件管理（5 个）
- `file-manager` - 文件管理
- `file-organizer` - 文件整理
- `pdf` - PDF 处理
- `pdf-reader` - PDF 阅读
- `markdown-converter` - Markdown 转换

### 🔧 工程工作流（7 个）
- `superpowers-mode` - 工程工作流
- `planning-with-files` - 文件规划
- `task-cron-manager` - **任务与定时任务管理** ⭐新增
- `task-manager` - 任务管理
- `session-log` - 会话日志
- `unblock-action` - 行动解锁
- `reflection` - 自我反思

### 🌐 Web 自动化（2 个）
- `browser-automation` - 浏览器自动化
- `webapp-testing` - Web 应用测试

### 💡 学习成长（5 个）
- `ship-learn-next` - 学习行动规划
- `learn-this` - 内容提取规划
- `note-taker` - 笔记管理
- `research-assistant` - 研究助手
- `tavily-search` - 实时搜索

---

## ⚙️ scripts/ - 自动化脚本（7 个）

| 脚本 | 功能 | 频率 |
|------|------|------|
| `auto-backup.py` | 自动备份工作区 | 每天 |
| `weekly-cleanup.py` | 每周清理临时文件 | 每周 |
| `daily-skill-review.py` | 每日技能审查 | 每天 |
| `check-group-tasks.py` | 群任务检查 | 定期 |
| `course_reminder.py` | 课程提醒 | 定期 |
| `cron-manager.py` | **定时任务管理** ⭐新增 | 按需 |
| `task-manager.py` | **任务状态检查** ⭐新增 | 按需 |

---

## 🧠 memory/ - 记忆文件

```
memory/
├── 2026-03-08.md      ← 今日记忆
└── improvements.md    ← 改进记录
```

---

## 📄 files/ - 文件存储

```
files/
└── pdf/
    └── 2cd1a99b4689b7725aa841171b8006fa.pdf
```

---

## 📥 downloads/ - 下载目录

```
downloads/
└── 2025-2026-2.pdf    ← 课表文件
```

---

## 📊 统计总览

| 类别 | 数量 |
|------|------|
| 核心配置文件 | 7 |
| 文档副本 | 13 |
| 技能包 | 32 |
| 自动化脚本 | 7 |
| 记忆文件 | 2 |
| **总计** | **61** |

---

## 🔧 常用命令

```bash
# 任务管理
python scripts/task-manager.py           # 检查任务状态
python scripts/cron-manager.py list      # 列出定时任务
python scripts/cron-manager.py check     # 检查并禁用达到限制的任务

# 文件整理
python scripts/weekly-cleanup.py         # 每周清理
python scripts/auto-backup.py            # 手动备份
```

---

## 📋 快速参考

### 何时创建 todo_XXX.md

✅ **创建：** 多步骤、跨会话、易跑偏的大型任务  
❌ **不创建：** 简单任务直接做

### 定时任务限制

```json
"limits": {
  "maxRuns": 10,        // 最多执行 10 次
  "currentRuns": 0,
  "expireAt": "..."     // 过期时间（可选）
}
```

### 技能查找

- **内容创作：** `content-writer`, `writing-assistant`
- **数据分析：** `stock-analysis`, `exploratory-data-analysis`
- **文件处理：** `pdf`, `markdown-converter`
- **任务管理：** `task-cron-manager`
- **学习研究：** `research-assistant`, `learn-this`
- **自动化：** `browser-automation`

---

*需要添加新技能？访问 https://clawhub.com*

*最后整理：2026-03-08 18:25*
