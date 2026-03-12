#!/root/anaconda3/bin/python3
"""
weekly-cleanup.py — 每周自动清理脚本
每周日 03:30 由 cron 自动执行
"""
import os
import time
import glob
import json

WORKSPACE = "/root/.openclaw/workspace"
OPENCLAW = "/root/.openclaw"
NOW = time.time()
DAY = 86400

results = []

# 1. 清理超过7天的每日日志
memory_dir = os.path.join(WORKSPACE, "memory")
if os.path.isdir(memory_dir):
    count = 0
    for f in glob.glob(os.path.join(memory_dir, "202?-??-??.md")):
        if NOW - os.path.getmtime(f) > 7 * DAY:
            os.remove(f)
            count += 1
    if count:
        results.append(f"清理了 {count} 个过期日志文件")

# 2. 清理超过7天的临时下载文件
downloads = os.path.join(WORKSPACE, "downloads")
if os.path.isdir(downloads):
    count = 0
    for f in glob.glob(os.path.join(downloads, "*")):
        if os.path.isfile(f) and NOW - os.path.getmtime(f) > 7 * DAY:
            os.remove(f)
            count += 1
    if count:
        results.append(f"清理了 {count} 个过期下载文件")

# 3. 清理 delivery-queue/failed 中超过7天的死信
failed_dir = os.path.join(OPENCLAW, "delivery-queue", "failed")
if os.path.isdir(failed_dir):
    count = 0
    for f in glob.glob(os.path.join(failed_dir, "*.json")):
        if NOW - os.path.getmtime(f) > 7 * DAY:
            os.remove(f)
            count += 1
    if count:
        results.append(f"清理了 {count} 个过期死信消息")

# 4. 清理浏览器缓存
browser_caches = [
    os.path.join(OPENCLAW, "browser", "data", "component_crx_cache"),
    os.path.join(OPENCLAW, "browser", "data", "WidevineCdm"),
    os.path.join(OPENCLAW, "browser", "data", "ShaderCache"),
    os.path.join(OPENCLAW, "browser", "proxy-data"),
]
import shutil
for cache_dir in browser_caches:
    if os.path.isdir(cache_dir):
        def safe_size(path):
            try:
                return os.path.getsize(path) if os.path.isfile(path) else 0
            except (OSError, FileNotFoundError):
                return 0
        size = sum(safe_size(os.path.join(dp, f)) for dp, dn, fn in os.walk(cache_dir) for f in fn)
        if size > 10 * 1024 * 1024:  # 只清理超过10MB的
            shutil.rmtree(cache_dir, ignore_errors=True)
            results.append(f"清理浏览器缓存: {cache_dir} ({size // 1024 // 1024}MB)")

# 5. 清理 .search_cache 中超过3天的搜索缓存
search_cache = os.path.join(OPENCLAW, ".search_cache")
if os.path.isdir(search_cache):
    count = 0
    for f in glob.glob(os.path.join(search_cache, "*")):
        if os.path.isfile(f) and NOW - os.path.getmtime(f) > 3 * DAY:
            os.remove(f)
            count += 1
    if count:
        results.append(f"清理了 {count} 个过期搜索缓存")

# 6. 清理workspace根目录中的无效图片文件（非真正图片的.jpg/.png）
import subprocess
for ext in ["*.jpg", "*.png", "*.jpeg"]:
    for f in glob.glob(os.path.join(WORKSPACE, ext)):
        try:
            result = subprocess.run(["file", f], capture_output=True, text=True)
            if "image data" not in result.stdout.lower():
                os.remove(f)
                results.append(f"删除无效图片: {os.path.basename(f)}")
        except:
            pass

# 输出结果
if results:
    print("本周清理完成：")
    for r in results:
        print(f"  - {r}")
else:
    print("本周无需清理，一切干净。")
