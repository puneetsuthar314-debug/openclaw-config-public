#!/root/anaconda3/bin/python3
"""
每天检查定时任务中的钉钉群是否存在
如果群被解散，自动删除对应的定时任务

由于钉钉机器人无法直接查询群状态，本脚本采用以下策略：
1. 读取所有定时任务，提取群 ID
2. 生成检查报告，列出所有群和对应任务
3. 由于无法自动检测，报告供用户参考
4. 用户可以通过回复"删除群任务 <群 ID>"来手动删除
"""

import json
import os
from datetime import datetime

JOBS_FILE = "/root/.openclaw/cron/jobs.json"
BACKUP_DIR = "/root/.openclaw/cron/backups"
LOG_FILE = "/root/.openclaw/cron/group-check.log"
REPORT_FILE = "/root/.openclaw/cron/group-check-report.md"

def log(message):
    """记录日志"""
    timestamp = datetime.now().isoformat()
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

def extract_group_info(jobs):
    """从定时任务中提取群信息和任务映射"""
    groups = {}
    private_jobs = []
    
    for job in jobs:
        delivery = job.get("delivery", {})
        to = delivery.get("to", "")
        
        if to.startswith("dingtalk:group:"):
            group_id = to.replace("dingtalk:group:", "")
            if group_id not in groups:
                groups[group_id] = {"jobs": [], "task_names": []}
            groups[group_id]["jobs"].append(job["id"])
            groups[group_id]["task_names"].append(job["name"])
        elif to and not to.startswith("dingtalk:group:"):
            # 私聊任务
            private_jobs.append({
                "id": job["id"],
                "name": job["name"],
                "to": to
            })
    
    return groups, private_jobs

def backup_jobs():
    """备份当前任务配置"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"jobs_{timestamp}.json")
    
    with open(JOBS_FILE, "r") as f:
        content = f.read()
    
    with open(backup_path, "w") as f:
        f.write(content)
    
    return backup_path

def generate_report(groups, private_jobs, jobs):
    """生成 Markdown 格式的检查报告"""
    report = f"""# 定时任务群状态检查报告

**检查时间：** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 概览

- 任务总数：{len(jobs)}
- 群任务涉及的群数量：{len(groups)}
- 私聊任务数量：{len(private_jobs)}

---

## 群任务列表

"""
    
    for i, (group_id, info) in enumerate(groups.items(), 1):
        report += f"""### {i}. 群 ID: `{group_id}`

**任务数量：** {len(info['jobs'])}

**任务列表：**
"""
        for name in info["task_names"]:
            report += f"- {name}\n"
        report += "\n"
    
    if private_jobs:
        report += """---

## 私聊任务列表

"""
        for job in private_jobs:
            report += f"- **{job['name']}** → {job['to']}\n"
    
    report += f"""
---

## 说明

1. **钉钉机器人无法直接查询群状态** - 这是钉钉 API 的限制
2. **如何确认群是否解散** - 尝试在群里发消息，如果提示"群不存在"则说明已解散
3. **如何删除任务** - 回复"删除群任务 <群 ID>"或手动编辑 `/root/.openclaw/cron/jobs.json`

---

*报告生成路径：`/root/.openclaw/cron/group-check-report.md`*
*备份路径：`/root/.openclaw/cron/backups/`*
"""
    
    return report

def main():
    log("=" * 60)
    log("开始检查定时任务中的群状态...")
    
    # 读取任务配置
    if not os.path.exists(JOBS_FILE):
        log(f"错误：任务配置文件不存在 {JOBS_FILE}")
        return
    
    with open(JOBS_FILE, "r") as f:
        data = json.load(f)
    
    jobs = data.get("jobs", [])
    log(f"当前任务总数：{len(jobs)}")
    
    # 提取群信息
    groups, private_jobs = extract_group_info(jobs)
    log(f"涉及的群数量：{len(groups)}")
    log(f"私聊任务数量：{len(private_jobs)}")
    
    # 显示群和任务映射
    log("\n群任务列表:")
    for group_id, info in groups.items():
        log(f"\n  群 ID: {group_id[:40]}...")
        log(f"  任务数量：{len(info['jobs'])}")
        for name in info["task_names"]:
            log(f"    - {name}")
    
    # 生成报告
    report = generate_report(groups, private_jobs, jobs)
    
    # 保存报告
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"\n✓ 检查报告已保存：{REPORT_FILE}")
    
    # 备份配置
    backup_path = backup_jobs()
    log(f"✓ 配置已备份：{backup_path}")
    
    log("\n" + "=" * 60)
    log("检查完成！")
    log("提示：钉钉机器人无法自动检测群状态，请查看报告文件确认")
    log("=" * 60)

if __name__ == "__main__":
    main()
