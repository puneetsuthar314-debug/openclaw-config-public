#!/root/anaconda3/bin/python3
"""
job-runner.py — 任务守护者包装器 (Job Guardian Wrapper)

功能：
  1. 包装执行其他定时脚本，捕获其 stdout/stderr 和退出码
  2. 执行成功时记录简要日志
  3. 执行失败时将错误信息写入 memory/job_errors.md，
     丫丫在心跳检查时会读取并向用户报告
  4. 支持超时保护（默认 300 秒）

用法：
  job-runner.py <脚本路径> [超时秒数]

示例：
  job-runner.py /root/.openclaw/workspace/scripts/weekly-cleanup.py 300
  job-runner.py /usr/local/bin/openclaw-cleanup.sh 180
"""

import sys
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
WORKSPACE = "/root/.openclaw/workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
ERROR_FILE = os.path.join(MEMORY_DIR, "job_errors.md")
LOG_FILE = "/var/log/job-runner.log"
DEFAULT_TIMEOUT = 300  # 默认超时 5 分钟
# ─────────────────────────────────────────────────────


def log(msg):
    """写入运行日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def write_error_to_memory(job_name, error_msg, exit_code, duration):
    """
    将失败信息追加到 memory/job_errors.md。
    丫丫在心跳检查时会读取此文件并向用户报告。
    """
    os.makedirs(MEMORY_DIR, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n---\n"
        f"### 任务失败告警\n"
        f"- **时间**: {ts}\n"
        f"- **任务**: `{job_name}`\n"
        f"- **退出码**: {exit_code}\n"
        f"- **耗时**: {duration:.1f} 秒\n"
        f"- **错误信息**:\n"
        f"```\n{error_msg[-2000:]}\n```\n"
        f"- **状态**: 待处理\n"
    )

    # 如果文件不存在，先写入头部
    if not os.path.exists(ERROR_FILE):
        header = (
            "# 定时任务错误日志\n\n"
            "> 此文件由 job-runner.py（任务守护者）自动维护。\n"
            "> 丫丫在心跳检查时应读取此文件，向用户报告未处理的错误，\n"
            "> 并在确认处理后将对应条目的状态改为「已处理」。\n"
        )
        with open(ERROR_FILE, "w", encoding="utf-8") as f:
            f.write(header)

    with open(ERROR_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def mark_processed_errors():
    """
    清理超过 7 天的已处理错误条目，保持文件简洁。
    在每次运行时顺便执行。
    """
    if not os.path.exists(ERROR_FILE):
        return

    try:
        with open(ERROR_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # 简单策略：如果文件超过 50KB，只保留最近的内容
        if len(content) > 50000:
            # 保留头部和最后 30KB
            lines = content.split("\n")
            header_end = 0
            for i, line in enumerate(lines):
                if line.startswith("---"):
                    header_end = i
                    break
            if header_end == 0:
                header_end = 5

            header = "\n".join(lines[:header_end])
            # 从后往前找，保留最近的条目
            recent = content[-30000:]
            first_separator = recent.find("\n---\n")
            if first_separator > 0:
                recent = recent[first_separator:]

            with open(ERROR_FILE, "w", encoding="utf-8") as f:
                f.write(header)
                f.write("\n\n> ⚠️ 旧条目已被自动清理，仅保留最近记录。\n")
                f.write(recent)
    except Exception as e:
        log(f"清理旧错误条目时出错: {e}")


def run_job(script_path, timeout):
    """执行目标脚本并监控其结果"""
    job_name = os.path.basename(script_path)
    log(f"开始执行: {job_name} (超时: {timeout}s)")

    start_time = time.time()

    try:
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "HOME": "/root"},
        )
        duration = time.time() - start_time

        if result.returncode == 0:
            log(f"执行成功: {job_name} (耗时: {duration:.1f}s)")
            return True
        else:
            error_output = result.stderr or result.stdout or "(无输出)"
            log(f"执行失败: {job_name} (退出码: {result.returncode}, 耗时: {duration:.1f}s)")
            write_error_to_memory(job_name, error_output, result.returncode, duration)
            return False

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        error_msg = f"任务执行超时（超过 {timeout} 秒），已被强制终止。"
        log(f"执行超时: {job_name} (超过 {timeout}s)")
        write_error_to_memory(job_name, error_msg, -1, duration)
        return False

    except FileNotFoundError:
        duration = time.time() - start_time
        error_msg = f"脚本文件不存在: {script_path}"
        log(f"文件不存在: {script_path}")
        write_error_to_memory(job_name, error_msg, -2, duration)
        return False

    except PermissionError:
        duration = time.time() - start_time
        error_msg = f"没有执行权限: {script_path}"
        log(f"权限不足: {script_path}")
        write_error_to_memory(job_name, error_msg, -3, duration)
        return False

    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"未知错误: {str(e)}"
        log(f"未知错误: {job_name} - {e}")
        write_error_to_memory(job_name, error_msg, -99, duration)
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: job-runner.py <脚本路径> [超时秒数]")
        print("示例: job-runner.py /path/to/script.py 300")
        sys.exit(1)

    script_path = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_TIMEOUT

    # 顺便清理旧的错误条目
    mark_processed_errors()

    # 执行目标任务
    success = run_job(script_path, timeout)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
