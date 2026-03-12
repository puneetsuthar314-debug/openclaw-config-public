# 脚本代码审查与优化建议 - 2026-03-09 00:00

## 📋 审查范围

7 个 Python 脚本的深度代码审查，评估代码质量、潜在问题和优化空间。

---

## ✅ 总体评价

| 指标 | 评分 | 说明 |
|------|------|------|
| 代码规范 | ⭐⭐⭐⭐ | 整体良好，部分细节需改进 |
| 错误处理 | ⭐⭐⭐ | 基础处理有，边界情况不足 |
| 可维护性 | ⭐⭐⭐⭐ | 结构清晰，注释充分 |
| 安全性 | ⭐⭐⭐ | 文件操作需注意权限 |
| 性能 | ⭐⭐⭐⭐ | 无明显性能问题 |

**综合评分**: ⭐⭐⭐⭐ (4/5)

---

## 📄 逐个脚本分析

### 1. auto-backup.py ⭐⭐⭐⭐

**功能**: 自动备份工作区配置

**优点**:
- ✅ 结构清晰，函数职责单一
- ✅ 备份命名规范（时间戳）
- ✅ 自动清理旧备份（保留 7 天）
- ✅ 有大小显示和数量统计

**问题**:
- ⚠️ **无异常处理** - `tar.add()` 失败时无处理
- ⚠️ **无日志文件** - 只在 stdout 打印，无法追溯
- ⚠️ **备份目录硬编码** - 未检查磁盘空间
- ⚠️ **WORKSPACE 路径错误** - 应该是 `/root/.openclaw/workspace` 但备份时可能遗漏隐藏文件

**优化建议**:
```python
# 1. 添加异常处理
try:
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(WORKSPACE, arcname="workspace")
except Exception as e:
    print(f"❌ 备份失败：{e}")
    return None

# 2. 添加日志文件
import logging
logging.basicConfig(
    filename="/root/.openclaw/logs/backup.log",
    level=logging.INFO
)

# 3. 检查磁盘空间
def check_disk_space(path, required_mb=100):
    import shutil
    total, used, free = shutil.disk_usage(path)
    return free // (1024 * 1024) > required_mb

# 4. 添加 exclude 参数排除大文件
tar.add(WORKSPACE, arcname="workspace", 
        filter=lambda x: None if x.name.endswith('.large') else x)
```

**优先级**: 🔴 高（异常处理）

---

### 2. check-group-tasks.py ⭐⭐⭐⭐

**功能**: 检查定时任务中的群状态

**优点**:
- ✅ 文档清晰，说明了钉钉 API 限制
- ✅ 生成 Markdown 报告供用户参考
- ✅ 自动备份配置
- ✅ 日志记录完整

**问题**:
- ⚠️ **JOBS_FILE 路径可能不存在** - 未检查 `/root/.openclaw/cron/` 目录
- ⚠️ **日志文件无限增长** - 无清理机制
- ⚠️ **错误处理不完整** - `json.load()` 失败时无处理
- ⚠️ **群 ID 截断显示** - `group_id[:40]` 可能不够

**优化建议**:
```python
# 1. 检查目录存在
CRON_DIR = Path("/root/.openclaw/cron")
CRON_DIR.mkdir(parents=True, exist_ok=True)

# 2. 添加 JSON 解析异常处理
try:
    with open(JOBS_FILE, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    log(f"❌ JSON 解析失败：{e}")
    return
except FileNotFoundError:
    log(f"❌ 文件不存在：{JOBS_FILE}")
    return

# 3. 限制日志文件大小
def rotate_log(log_file, max_size_mb=10):
    if os.path.getsize(log_file) > max_size_mb * 1024 * 1024:
        with open(log_file, "r") as f:
            lines = f.readlines()[-1000:]  # 保留最后 1000 行
        with open(log_file, "w") as f:
            f.writelines(lines)

# 4. 完整显示群 ID
log(f"\n  群 ID: {group_id}")  # 不截断
```

**优先级**: 🟡 中（目录检查、JSON 异常处理）

---

### 3. course_reminder.py ⭐⭐⭐⭐⭐

**功能**: 根据课表返回当天课程信息

**优点**:
- ✅ 课表数据完整（从小和山校区 PDF 提取）
- ✅ 周次计算逻辑正确
- ✅ 课程进度百分比计算准确
- ✅ 支持时间段过滤（morning/afternoon/evening）
- ✅ JSON 输出便于集成

**问题**:
- ⚠️ **硬编码学期开始日期** - 2026 年 3 月 2 日，下学期需手动更新
- ⚠️ **无配置文件** - 课表数据应分离到 JSON 文件
- ⚠️ **周次范围硬编码** - `min(week, 16)` 假设所有学期 16 周
- ⚠️ **无命令行帮助** - `sys.argv` 使用无提示

**优化建议**:
```python
# 1. 配置文件分离
CONFIG_FILE = Path("/root/.openclaw/config/course_config.json")
# {
#   "semester_start": "2026-03-02",
#   "total_weeks": 16,
#   "course_table": {...}
# }

# 2. 添加命令行帮助
def print_help():
    print("用法：python course_reminder.py [时间段]")
    print()
    print("时间段: morning, afternoon, evening (默认：morning)")
    print("示例：python course_reminder.py afternoon")

if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
    print_help()
    sys.exit(0)

# 3. 添加配置文件加载
def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"semester_start": "2026-03-02", "total_weeks": 16}
```

**优先级**: 🟢 低（功能完善，可延后优化）

---

### 4. cron-manager.py ⭐⭐⭐⭐⭐

**功能**: 定时任务管理器（支持执行次数限制）

**优点**:
- ✅ 功能完整（check/list/increment/create）
- ✅ 支持执行次数和过期时间限制
- ✅ 命令行界面友好
- ✅ 禁用原因记录清晰
- ✅ UUID 生成任务 ID

**问题**:
- ⚠️ **时区处理可能有问题** - `datetime.now(expire_time.tzinfo)` 可能报错
- ⚠️ **create 命令未实现** - 只打印提示
- ⚠️ **无备份机制** - 直接修改 jobs.json
- ⚠️ **并发安全问题** - 多进程同时修改可能冲突

**优化建议**:
```python
# 1. 修复时区处理
from datetime import timezone

def check_limits(data):
    # ...
    if expire_at:
        try:
            expire_time = datetime.fromisoformat(expire_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)  # 使用 UTC 时间
            if now > expire_time:
                # ...
        except Exception as e:
            log(f"⚠️ 过期时间解析失败：{e}")

# 2. 实现 create 命令
elif cmd == 'create':
    if len(sys.argv) < 7:
        print("用法：create <name> <cron_expr> <message> <target> [max_runs] [expire_hours]")
        return
    name = sys.argv[2]
    cron_expr = sys.argv[3]
    message = sys.argv[4]
    target = sys.argv[5]
    max_runs = int(sys.argv[6]) if len(sys.argv) > 6 else None
    expire_hours = int(sys.argv[7]) if len(sys.argv) > 7 else None
    
    job_id = create_task(name, cron_expr, message, target, max_runs, expire_hours)
    print(f"✅ 任务已创建：{job_id}")

# 3. 添加备份
def save_jobs(data):
    # 先备份
    backup_path = JOBS_FILE.with_suffix('.json.bak')
    if JOBS_FILE.exists():
        shutil.copy(JOBS_FILE, backup_path)
    
    # 临时文件写入，避免写入中断损坏
    temp_path = JOBS_FILE.with_suffix('.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp_path.replace(JOBS_FILE)
```

**优先级**: 🟡 中（时区处理、create 命令实现）

---

### 5. daily-skill-review.py ⭐⭐⭐⭐

**功能**: 每日技能回顾（凌晨 3 点执行）

**优点**:
- ✅ 自动扫描技能目录
- ✅ 查找可能重复的技能
- ✅ 生成详细 Markdown 报告
- ✅ 工作区结构分析
- ✅ 提供具体优化建议

**问题**:
- ⚠️ **SKILL.md 读取截断** - `content[:500]` 可能错过关键信息
- ⚠️ **重复检测逻辑简单** - 仅基于关键词，可能误判
- ⚠️ **报告文件无轮转** - 每日生成新报告，无清理
- ⚠️ **日志文件无限增长** - 同 check-group-tasks.py

**优化建议**:
```python
# 1. 改进描述提取
def extract_description(content):
    """更健壮地提取 SKILL.md 描述"""
    # 尝试多种格式
    patterns = [
        r'description:\s*["\']?(.+?)["\']?\n',
        r'## 描述\s*\n+(.+?)\n',
        r'^描述[:：]\s*(.+?)$'
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return "无描述"

# 2. 改进重复检测
from difflib import SequenceMatcher

def find_duplicate_skills(skills):
    duplicates = []
    for i, s1 in enumerate(skills):
        for s2 in skills[i+1:]:
            # 名称相似度
            name_sim = SequenceMatcher(None, s1["name"], s2["name"]).ratio()
            # 描述相似度
            desc_sim = SequenceMatcher(
                None, 
                s1.get("description", ""), 
                s2.get("description", "")
            ).ratio()
            
            if name_sim > 0.6 or desc_sim > 0.7:
                duplicates.append({
                    "skills": [s1, s2],
                    "similarity": max(name_sim, desc_sim)
                })
    return duplicates

# 3. 报告轮转（只保留最近 7 份）
def rotate_reports():
    reports = sorted(REPORT_DIR.glob("daily-review-*.md"))
    for old_report in reports[:-7]:
        old_report.unlink()
```

**优先级**: 🟢 低（功能可用，优化可延后）

---

### 6. task-manager.py ⭐⭐⭐

**功能**: 任务管理（检查过期、归档完成）

**优点**:
- ✅ 检查即将过期任务
- ✅ 自动归档已完成任务
- ✅ 生成统计报告
- ✅ 使用 Path 对象（现代 Python 风格）

**问题**:
- 🔴 **解析逻辑脆弱** - 依赖 `**创建日期：**` 等特定格式
- 🔴 **无错误处理** - 文件读取失败无处理
- 🔴 **归档逻辑不完整** - 只移动文件，未更新索引
- ⚠️ **日期格式假设** - 假设所有任务使用 `YYYY-MM-DD`
- ⚠️ **无配置文件** - 目录路径硬编码

**优化建议**:
```python
# 1. 改进解析逻辑（支持多种格式）
def parse_task_file(filepath):
    """更健壮的任务文件解析"""
    content = filepath.read_text()
    metadata = {}
    
    # 支持多种格式
    patterns = {
        'created': [r'创建日期[:：]\s*(\d{4}-\d{2}-\d{2})', 
                    r'Created[:：]\s*(\d{4}-\d{2}-\d{2})'],
        'deadline': [r'截止日期[:：]\s*(\d{4}-\d{2}-\d{2})',
                     r'Deadline[:：]\s*(\d{4}-\d{2}-\d{2})'],
        'priority': [r'优先级[:：]\s*(高 | 中 | 低|\d)',
                     r'Priority[:：]\s*(High|Medium|Low|\d)'],
        'status': [r'状态[:：]\s*(\w+)',
                   r'Status[:：]\s*(\w+)']
    }
    
    for field, field_patterns in patterns.items():
        for pattern in field_patterns:
            match = re.search(pattern, content)
            if match:
                metadata[field] = match.group(1)
                break
    
    return metadata

# 2. 添加错误处理
def parse_task_file(filepath):
    try:
        content = filepath.read_text(encoding='utf-8')
        # ... 解析逻辑
    except UnicodeDecodeError:
        print(f"⚠️ 编码错误：{filepath}")
        return {}
    except Exception as e:
        print(f"⚠️ 读取失败 {filepath}: {e}")
        return {}

# 3. 完善归档逻辑
def archive_completed():
    archived = []
    for task_file in ACTIVE_DIR.glob("TASK-*.md"):
        content = task_file.read_text()
        if '✅ 完成' in content or '完成' in content:
            dest = COMPLETED_DIR / task_file.name
            # 添加归档时间
            content += f"\n\n_归档时间：{datetime.now().isoformat()}_"
            dest.write_text(content, encoding='utf-8')
            task_file.unlink()
            archived.append(task_file.name)
    
    # 更新归档索引
    update_archive_index()
    return archived
```

**优先级**: 🔴 高（解析逻辑、错误处理）

---

### 7. weekly-cleanup.py ⭐⭐⭐

**功能**: 每周清理临时文件

**优点**:
- ✅ 清理日志和缓存
- ✅ 配置简单明了
- ✅ 有清理统计

**问题**:
- 🔴 **清理逻辑过于激进** - `shutil.rmtree()` 直接删除整个缓存目录
- 🔴 **无确认机制** - 可能误删重要文件
- 🔴 **无异常处理** - 删除失败无处理
- ⚠️ **缓存目录硬编码** - 可能不适用于所有环境
- ⚠️ **无日志记录** - 只在 stdout 打印

**优化建议**:
```python
# 1. 改进清理逻辑（按文件年龄而非删除整个目录）
def cleanup_cache():
    cleaned_size = 0
    cleaned_count = 0
    
    for cache_dir in CACHE_DIRS:
        if os.path.exists(cache_dir):
            cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                        if mtime < cutoff:
                            os.remove(filepath)
                            cleaned_count += 1
                            cleaned_size += os.path.getsize(filepath)
                    except Exception as e:
                        print(f"⚠️ 无法删除 {filepath}: {e}")
    
    return cleaned_count, cleaned_size

# 2. 添加安全名单
SAFE_DIRS = [
    "/root/.cache/pip",  # pip 缓存，保留
    "/root/.openclaw/cache",  # OpenClaw 缓存，保留
]

def is_safe_to_clean(path):
    """检查是否在安全名单中"""
    for safe in SAFE_DIRS:
        if path.startswith(safe):
            return False
    return True

# 3. 添加异常处理
def main():
    try:
        print("=" * 50)
        print("开始清理临时文件...")
        
        logs_cleaned = cleanup_logs()
        print(f"✓ 清理日志文件：{logs_cleaned} 个")
        
        cache_count, cache_size = cleanup_cache()
        print(f"✓ 清理缓存文件：{cache_count} 个 ({cache_size / 1024 / 1024:.2f} MB)")
        
        print("\n" + "=" * 50)
        print("清理完成！")
    except Exception as e:
        print(f"❌ 清理失败：{e}")
        import traceback
        traceback.print_exc()
```

**优先级**: 🔴 高（安全性问题）

---

## 📊 问题汇总

### 高优先级 🔴

| 脚本 | 问题 | 风险 |
|------|------|------|
| task-manager.py | 解析逻辑脆弱，无错误处理 | 任务管理失败 |
| weekly-cleanup.py | 清理过于激进，无异常处理 | 误删重要文件 |
| auto-backup.py | 无异常处理 | 备份失败无通知 |

### 中优先级 🟡

| 脚本 | 问题 | 影响 |
|------|------|------|
| check-group-tasks.py | 目录检查、JSON 异常处理 | 脚本崩溃 |
| cron-manager.py | 时区处理、create 命令未实现 | 功能不完整 |

### 低优先级 🟢

| 脚本 | 问题 | 建议 |
|------|------|------|
| course_reminder.py | 硬编码配置 | 配置文件分离 |
| daily-skill-review.py | 重复检测简单 | 改进算法 |

---

## 🎯 优化实施建议

### 第一阶段（立即执行）
1. **task-manager.py** - 添加错误处理和健壮解析
2. **weekly-cleanup.py** - 改进清理逻辑，添加安全名单
3. **auto-backup.py** - 添加异常处理和日志

### 第二阶段（本周内）
4. **check-group-tasks.py** - 目录检查和 JSON 异常处理
5. **cron-manager.py** - 修复时区处理，实现 create 命令

### 第三阶段（可选优化）
6. **course_reminder.py** - 配置文件分离
7. **daily-skill-review.py** - 改进重复检测算法

---

## 📝 通用改进建议

### 1. 日志系统统一
```python
# 创建统一的日志模块 /root/.openclaw/scripts/logging_utils.py
import logging
from pathlib import Path

def setup_logger(name, log_file):
    """设置日志记录器"""
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

### 2. 配置文件统一管理
```json
// /root/.openclaw/config/settings.json
{
  "workspace": "/root/.openclaw/workspace",
  "backup_dir": "/root/.openclaw/backups",
  "log_dir": "/root/.openclaw/logs",
  "retention_days": 7,
  "semester_start": "2026-03-02",
  "total_weeks": 16
}
```

### 3. 异常处理模板
```python
def safe_operation(func):
    """异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"{func.__name__} 失败：{e}")
            return None
    return wrapper
```

---

## ✅ 总结

**整体质量**: 良好，功能完整，代码结构清晰

**主要问题**: 异常处理不足，部分脚本解析逻辑脆弱

**改进方向**: 
1. 统一日志系统
2. 配置文件分离
3. 增强错误处理
4. 改进安全性（尤其是清理脚本）

---

**审查时间**: 2026-03-09 00:00  
**审查者**: Claw（自主审查）  
**状态**: 报告完成，待实施优化
