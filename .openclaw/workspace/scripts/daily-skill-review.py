#!/root/anaconda3/bin/python3
"""
每天凌晨 3 点执行：
1. 过一遍所有技能，熟悉并掌握
2. 检查现有技能，思考有重复内容的是否需要合并
3. 整理文件、建议文件夹结构

输出报告到：/root/.openclaw/cron/daily-review-report.md
"""

import json
import os
from datetime import datetime

SKILLS_DIR = "/root/.openclaw/workspace/skills"
REPORT_FILE = "/root/.openclaw/cron/daily-review-report.md"
LOG_FILE = "/root/.openclaw/cron/daily-review.log"

def log(message):
    """记录日志"""
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

def get_skills_list():
    """获取所有技能列表"""
    skills = []
    if not os.path.exists(SKILLS_DIR):
        return skills
    
    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            skill_info = {
                "name": item,
                "path": item_path,
                "has_skill_md": os.path.exists(os.path.join(item_path, "SKILL.md"))
            }
            
            # 读取 SKILL.md 获取描述
            skill_md_path = os.path.join(item_path, "SKILL.md")
            if os.path.exists(skill_md_path):
                with open(skill_md_path, "r", encoding="utf-8") as f:
                    content = f.read()[:500]
                    # 提取 description
                    if "description:" in content:
                        desc_start = content.find("description:") + 12
                        desc_end = content.find("\n", desc_start)
                        if desc_end == -1:
                            desc_end = content.find("---", desc_start)
                        skill_info["description"] = content[desc_start:desc_end].strip().strip('"').strip("'")
            
            skills.append(skill_info)
    
    return skills

def find_duplicate_skills(skills):
    """查找可能重复的技能"""
    duplicates = []
    
    # 关键词分组（可能重复的技能）
    keyword_groups = {
        "excel": ["excel", "xlsx", "spreadsheet"],
        "pdf": ["pdf"],
        "content": ["content", "writing"],
        "research": ["research", "analysis"],
        "video": ["video", "youtube"],
        "file": ["file", "organize"],
        "web": ["web", "browser", "http"],
        "data": ["data", "csv", "scientific"],
    }
    
    for keyword, related in keyword_groups.items():
        matching = [s for s in skills if any(k in s["name"].lower() for k in related)]
        if len(matching) > 1:
            duplicates.append({
                "category": keyword,
                "skills": matching
            })
    
    return duplicates

def check_workspace_structure():
    """检查工作区结构"""
    workspace = "/root/.openclaw/workspace"
    structure = {}
    
    if os.path.exists(workspace):
        for item in os.listdir(workspace):
            item_path = os.path.join(workspace, item)
            if os.path.isdir(item_path):
                item_count = len(os.listdir(item_path))
                structure[item] = {"type": "directory", "items": item_count}
            else:
                structure[item] = {"type": "file"}
    
    return structure

def generate_report(skills, duplicates, structure):
    """生成每日检查报告"""
    report = f"""# 📅 每日技能与工作区检查报告

**生成时间：** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 技能库概览

**技能总数：** {len(skills)}

**有效技能（有 SKILL.md）：** {sum(1 for s in skills if s.get('has_skill_md'))}

### 技能列表

| 序号 | 技能名 | 描述 |
|------|--------|------|
"""
    
    for i, skill in enumerate(skills, 1):
        desc = skill.get("description", "无描述")[:50] + "..." if len(skill.get("description", "")) > 50 else skill.get("description", "无描述")
        report += f"| {i} | `{skill['name']}` | {desc} |\n"
    
    report += f"""
---

## ⚠️ 可能重复的技能

"""
    
    if duplicates:
        for dup in duplicates:
            report += f"""### {dup['category'].upper()} 相关
"""
            for skill in dup["skills"]:
                desc = skill.get("description", "无描述")[:80]
                report += f"- `{skill['name']}` - {desc}\n"
            report += "\n"
    else:
        report += "未发现明显重复的技能。\n"
    
    report += f"""
---

## 📂 工作区结构

```
/root/.openclaw/workspace/
"""
    
    for item, info in sorted(structure.items()):
        if info["type"] == "directory":
            report += f"├── {item}/  ({info['items']} 项)\n"
        else:
            report += f"├── {item}\n"
    
    report += """```

---

## 💡 建议

### 技能优化建议

"""
    
    # 生成具体建议
    suggestions = []
    
    # 检查 excel 相关
    excel_skills = [s for s in skills if "excel" in s["name"].lower() or "xlsx" in s["name"].lower()]
    if len(excel_skills) > 1:
        suggestions.append(f"**Excel 相关技能 ({len(excel_skills)} 个)**：考虑合并成一个统一的 `excel` 技能")
    
    # 检查 content 相关
    content_skills = [s for s in skills if "content" in s["name"].lower()]
    if len(content_skills) > 2:
        suggestions.append(f"**内容创作技能 ({len(content_skills)} 个)**：功能可能有重叠，检查是否需要合并")
    
    # 检查 research 相关
    research_skills = [s for s in skills if "research" in s["name"].lower()]
    if len(research_skills) > 2:
        suggestions.append(f"**研究相关技能 ({len(research_skills)} 个)**：检查功能边界是否清晰")
    
    if suggestions:
        for s in suggestions:
            report += f"- {s}\n"
    else:
        report += "- 当前技能结构合理，无需合并\n"
    
    report += """
### 文件整理建议

- 定期检查 `skills/` 目录，删除无 SKILL.md 的文件夹
- 保持 `docs/`、`scripts/`、`files/` 目录结构清晰
- 及时清理临时下载文件

---

## 📝 本次检查总结

"""
    
    if duplicates:
        report += f"- 发现 {len(duplicates)} 组可能重复的技能\n"
    report += f"- 技能总数：{len(skills)}\n"
    report += f"- 工作区目录数：{sum(1 for v in structure.values() if v['type'] == 'directory')}\n"
    
    report += f"""
---

*报告路径：`{REPORT_FILE}`*
*日志路径：`{LOG_FILE}`*

---

*此报告由每日定时任务自动生成*
"""
    
    return report

def main():
    log("=" * 60)
    log("开始每日技能与工作区检查...")
    
    # 获取技能列表
    log("正在扫描技能目录...")
    skills = get_skills_list()
    log(f"发现 {len(skills)} 个技能")
    
    # 查找重复技能
    log("正在分析可能重复的技能...")
    duplicates = find_duplicate_skills(skills)
    log(f"发现 {len(duplicates)} 组可能重复的技能")
    
    # 检查工作区结构
    log("正在检查工作区结构...")
    structure = check_workspace_structure()
    log(f"工作区包含 {len(structure)} 个顶级项目")
    
    # 生成报告
    log("正在生成报告...")
    report = generate_report(skills, duplicates, structure)
    
    # 保存报告
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"报告已保存：{REPORT_FILE}")
    log("=" * 60)
    log("每日检查完成！")

if __name__ == "__main__":
    main()
