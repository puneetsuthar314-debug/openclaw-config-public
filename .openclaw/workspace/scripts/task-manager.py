#!/root/anaconda3/bin/python3
"""
任务管理自动化脚本
- 检查即将过期的任务
- 自动归档已完成任务
- 生成任务统计报告
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
TASKS_DIR = WORKSPACE / "tasks"
ACTIVE_DIR = TASKS_DIR / "active"
COMPLETED_DIR = TASKS_DIR / "completed"
MEMORY_DIR = WORKSPACE / "memory"

def parse_task_file(filepath):
    """解析任务文件，提取元数据"""
    content = filepath.read_text()
    metadata = {}
    
    # 提取元数据字段
    for line in content.split('\n')[:20]:
        if '**创建日期：**' in line:
            metadata['created'] = line.split('：')[1].strip()
        elif '**截止日期：**' in line:
            metadata['deadline'] = line.split('：')[1].strip()
        elif '**优先级：**' in line:
            metadata['priority'] = line.split('：')[1].strip()
        elif '**状态：**' in line:
            metadata['status'] = line.split('：')[1].strip()
    
    return metadata

def check_deadlines():
    """检查即将过期的任务"""
    urgent_tasks = []
    
    for task_file in ACTIVE_DIR.glob("TASK-*.md"):
        metadata = parse_task_file(task_file)
        deadline = metadata.get('deadline', '')
        
        if deadline and deadline != 'YYYY-MM-DD':
            try:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                days_left = (deadline_date - datetime.now()).days
                
                if days_left < 0:
                    urgent_tasks.append({
                        'file': task_file.name,
                        'deadline': deadline,
                        'status': '已过期',
                        'days': days_left
                    })
                elif days_left <= 3:
                    urgent_tasks.append({
                        'file': task_file.name,
                        'deadline': deadline,
                        'status': '紧急',
                        'days': days_left
                    })
            except ValueError:
                pass
    
    return urgent_tasks

def archive_completed():
    """归档已完成的任务"""
    archived = []
    
    for task_file in ACTIVE_DIR.glob("TASK-*.md"):
        content = task_file.read_text()
        if '✅ 完成' in content:
            # 移动到 completed 目录
            dest = COMPLETED_DIR / task_file.name
            dest.write_text(content)
            task_file.unlink()
            archived.append(task_file.name)
    
    return archived

def generate_report():
    """生成任务统计报告"""
    active_count = len(list(ACTIVE_DIR.glob("TASK-*.md")))
    completed_count = len(list(COMPLETED_DIR.glob("TASK-*.md")))
    
    report = {
        'date': datetime.now().isoformat(),
        'active': active_count,
        'completed': completed_count,
        'urgent': check_deadlines()
    }
    
    return report

def main():
    print("=== 任务管理检查 ===")
    print(f"时间：{datetime.now().isoformat()}")
    print()
    
    # 检查截止日期
    urgent = check_deadlines()
    if urgent:
        print("⚠️  紧急任务：")
        for task in urgent:
            print(f"  - {task['file']}: {task['status']} ({task['days']}天)")
    else:
        print("✅ 无紧急任务")
    print()
    
    # 归档已完成
    archived = archive_completed()
    if archived:
        print(f"📦 已归档 {len(archived)} 个任务：")
        for task in archived:
            print(f"  - {task}")
    print()
    
    # 统计
    report = generate_report()
    print(f"📊 当前活跃任务：{report['active']}")
    print(f"📊 已完成任务：{report['completed']}")

if __name__ == "__main__":
    main()
