#!/root/anaconda3/bin/python3
"""
定时任务管理器 - 支持执行次数限制
- 检查并更新任务执行计数
- 自动禁用达到限制的任务
- 清理过期任务
"""

import json
from datetime import datetime
from pathlib import Path

CRON_DIR = Path("/root/.openclaw/cron")
JOBS_FILE = CRON_DIR / "jobs.json"

def load_jobs():
    """加载任务列表"""
    if not JOBS_FILE.exists():
        return {"version": 2, "jobs": []}
    
    with open(JOBS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_jobs(data):
    """保存任务列表"""
    with open(JOBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_limits(data):
    """检查并处理达到限制的任务"""
    disabled = []
    expired = []
    
    for job in data.get('jobs', []):
        limits = job.get('limits', {})
        
        if not limits:
            continue
        
        # 检查执行次数
        max_runs = limits.get('maxRuns')
        current_runs = limits.get('currentRuns', 0)
        
        if max_runs and current_runs >= max_runs:
            job['enabled'] = False
            job['_disabledReason'] = f'达到最大执行次数 ({current_runs}/{max_runs})'
            disabled.append({
                'name': job['name'],
                'runs': f'{current_runs}/{max_runs}'
            })
        
        # 检查过期时间
        expire_at = limits.get('expireAt')
        if expire_at:
            try:
                expire_time = datetime.fromisoformat(expire_at.replace('Z', '+00:00'))
                if datetime.now(expire_time.tzinfo) > expire_time:
                    job['enabled'] = False
                    job['_disabledReason'] = f'已过期 ({expire_at})'
                    expired.append({
                        'name': job['name'],
                        'expiredAt': expire_at
                    })
            except Exception as e:
                pass
    
    return disabled, expired

def increment_run(job_id):
    """增加任务执行计数"""
    data = load_jobs()
    
    for job in data.get('jobs', []):
        if job.get('id') == job_id:
            limits = job.setdefault('limits', {})
            limits['currentRuns'] = limits.get('currentRuns', 0) + 1
            limits['lastRunAt'] = datetime.now().isoformat()
            save_jobs(data)
            return True
    
    return False

def create_task(name, cron_expr, message, target, max_runs=None, expire_hours=None):
    """创建带限制的新任务"""
    import uuid
    
    data = load_jobs()
    
    limits = {}
    if max_runs:
        limits['maxRuns'] = max_runs
        limits['currentRuns'] = 0
    if expire_hours:
        from datetime import timedelta
        expire_time = datetime.now() + timedelta(hours=expire_hours)
        limits['expireAt'] = expire_time.isoformat()
    
    job = {
        'id': str(uuid.uuid4()),
        'name': name,
        'enabled': True,
        'schedule': {
            'kind': 'cron',
            'expr': cron_expr,
            'tz': 'Asia/Shanghai'
        },
        'limits': limits if limits else None,
        'payload': {
            'kind': 'agentTurn',
            'message': message
        },
        'delivery': {
            'mode': 'announce',
            'channel': 'clawdbot-dingtalk',
            'to': target
        }
    }
    
    data['jobs'].append(job)
    save_jobs(data)
    return job['id']

def list_tasks():
    """列出所有任务及状态"""
    data = load_jobs()
    
    print(f"{'任务名称':<25} {'状态':<8} {'执行次数':<15} {'过期时间':<20}")
    print("-" * 75)
    
    for job in data.get('jobs', []):
        name = job.get('name', '未知')[:24]
        enabled = '✅' if job.get('enabled') else '❌'
        
        limits = job.get('limits', {})
        if limits:
            max_runs = limits.get('maxRuns', '∞')
            current = limits.get('currentRuns', 0)
            runs = f'{current}/{max_runs}' if max_runs != '∞' else f'{current}/∞'
            expire = limits.get('expireAt', '永不过期')[:19] if limits.get('expireAt') else '永不过期'
        else:
            runs = '无限制'
            expire = '永不过期'
        
        print(f"{name:<25} {enabled:<8} {runs:<15} {expire:<20}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python cron-manager.py [check|list|increment|create]")
        print()
        print("命令:")
        print("  check              - 检查并禁用达到限制/过期的任务")
        print("  list               - 列出所有任务")
        print("  increment <id>     - 增加任务执行计数")
        print("  create <params>    - 创建新任务（需要参数）")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'check':
        data = load_jobs()
        disabled, expired = check_limits(data)
        save_jobs(data)
        
        print("=== 定时任务检查 ===")
        print(f"时间：{datetime.now().isoformat()}")
        print()
        
        if disabled:
            print(f"🚫 已禁用 {len(disabled)} 个任务（达到执行次数限制）:")
            for t in disabled:
                print(f"  - {t['name']} ({t['runs']})")
        else:
            print("✅ 无任务达到执行限制")
        print()
        
        if expired:
            print(f"🕐 已禁用 {len(expired)} 个任务（已过期）:")
            for t in expired:
                print(f"  - {t['name']} ({t['expiredAt']})")
        else:
            print("✅ 无任务过期")
    
    elif cmd == 'list':
        list_tasks()
    
    elif cmd == 'increment':
        if len(sys.argv) < 3:
            print("错误：需要任务 ID")
            return
        job_id = sys.argv[2]
        if increment_run(job_id):
            print(f"✅ 任务 {job_id} 执行计数 +1")
        else:
            print(f"❌ 未找到任务 {job_id}")
    
    elif cmd == 'create':
        print("请使用 API 方式创建任务，或手动编辑 jobs.json")

if __name__ == "__main__":
    main()
