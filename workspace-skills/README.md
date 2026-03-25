# Skills 索引

最后更新：2026-03-08  
OpenClaw 版本：2026.3.7（已升级）

## 📁 目录结构

```
skills/
├── content/           # 内容创作 (6 个)
├── data-analysis/     # 数据分析 (7 个)
├── file-tools/        # 文件工具 (3 个)
├── learning/          # 学习研究 (4 个)
├── security/          # 安全套件 (8 个)
├── system/            # 系统工具 (7 个)
├── task-management/   # 任务管理 (4 个)
└── web-tools/         # Web 工具 (2 个)
```

---

## 🔒 Security (8 个)

| Skill | 功能 |
|-------|------|
| `clawsec-suite` | ClawSec 套件管理器（主入口） |
| `clawsec-feed` | 安全咨询 feed |
| `clawsec-clawhub-checker` | ClawHub 声誉检查 |
| `clawsec-nanoclaw` | NanoClaw 安全检查 |
| `clawtributor` | 社区事件报告 |
| `openclaw-audit-watchdog` | 自动安全审计 |
| `prompt-agent` | 安全审计执行 |
| `soul-guardian` | 文件完整性保护 |

---

## 📝 Content (6 个)

| Skill | 功能 |
|-------|------|
| `content-writer` | 多平台内容生成（小红书/知乎/公众号/抖音） |
| `content-research-writer` | 内容研究与写作助手 |
| `writing-assistant` | 写作团队管理 |
| `content-ideas-free` | 内容创意生成 |
| `article-extractor` | 文章提取 |
| `video-generator` | AI 视频生成 |

---

## 📊 Data Analysis (7 个)

| Skill | 功能 |
|-------|------|
| `excel` | Excel 电子表格处理 |
| `csv-summarizer` | CSV 数据分析 |
| `exploratory-data-analysis` | 科学数据探索分析 |
| `stock-analysis` | 股票分析 |
| `similarweb-analytics` | 网站流量分析 |
| `market-research-reports` | 市场研究报告 (50+ 页) |
| `scientific-visualization` | 科学可视化 |

---

## 📂 File Tools (3 个)

| Skill | 功能 |
|-------|------|
| `pdf` | PDF 处理（读取/合并/分割/OCR） |
| `markdown-converter` | 文件转 Markdown |
| `file-organizer` | 智能文件整理 |

---

## 🎓 Learning (4 个)

| Skill | 功能 |
|-------|------|
| `learn-this` | 内容提取 + 行动计划 |
| `ship-learn-next` | 学习转行动框架 |
| `deep-research` | 深度研究 (Gemini) |
| `youtube-transcript` | YouTube 字幕下载 |

---

## ✅ Task Management (4 个)

| Skill | 功能 |
|-------|------|
| `task-manager` | 任务管理 |
| `task-cron-manager` | 任务与定时任务 |
| `planning-with-files` | 文件规划 (Manus 风格) |
| `unblock-action` | 行动解除阻塞 |

---

## 🌐 Web Tools (2 个)

| Skill | 功能 |
|-------|------|
| `webapp-testing` | Web 应用测试 (Playwright) |
| `weather` | 天气查询 |

---

## ⚙️ System (7 个)

| Skill | 功能 |
|-------|------|
| `skill-creator` | 技能创建指南 |
| `internet-skill-finder` | 技能查找器 |
| `claw-release` | 发布自动化 |
| `reflection` | 自我反思 |
| `session-log` | 会话日志 |
| `superpowers-mode` | 工程工作流 |
| `scrum-sage` | Scrum 教练 |

---

## 📋 使用指南

### 技能调用规则

1. **按功能域选择** - 根据用户需求选择对应分类的 skill
2. **优先主入口** - 如安全类优先 `clawsec-suite`
3. **避免重复** - 相似功能选择最匹配的一个

### 快速查找

```bash
# 查找特定功能的 skill
grep -r "description:" skills/*/SKILL.md | grep "关键词"

# 列出所有 skill 名称
find skills -name SKILL.md -exec grep "^name:" {} \;
```

---

## 🔧 维护说明

- 新增 skill 时放入对应分类目录
- 如无合适分类可创建新目录
- 定期审查重复功能并考虑合并
- 更新本索引文件保持同步

| **`scrapling`** | ✅ 可用 | 高级网页爬取、反爬绕过（Cloudflare Turnstile）、Spider框架 | 当需要绕过反爬保护或编写Python爬虫时使用 |
