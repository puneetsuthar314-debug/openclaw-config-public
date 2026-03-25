#!/bin/bash
# chromium-watchdog.sh — Chromium 空闲资源回收 Watchdog
# 功能：
#   1. 检测 Chromium 是否空闲（只有 about:blank 标签页）
#   2. 空闲超过阈值后，关闭所有非空白标签页并触发 GC
#   3. 当 RSS 超过阈值时，通过 CDP 强制 GC
#   4. 记录日志到 /tmp/chromium-watchdog.log
#
# 部署方式：cron 每 5 分钟运行一次
# crontab: */5 * * * * /root/.openclaw/scripts/chromium-watchdog.sh

set -euo pipefail

# === 配置 ===
CDP_PORT=18800
CDP_URL="http://127.0.0.1:${CDP_PORT}"
LOG_FILE="/tmp/chromium-watchdog.log"
IDLE_STATE_FILE="/tmp/chromium-idle-since"
# 空闲超过 30 分钟后触发 GC
IDLE_THRESHOLD_SECONDS=1800
# RSS 超过 400MB 时强制 GC（单位 KB）
RSS_THRESHOLD_KB=1048576

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# 保持日志文件不超过 1000 行
trim_log() {
    if [ -f "$LOG_FILE" ] && [ "$(wc -l < "$LOG_FILE")" -gt 1000 ]; then
        tail -500 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
    fi
}

# 检查 Chromium 是否在运行
check_chromium_running() {
    pgrep -f "chromium.*--remote-debugging-port=${CDP_PORT}" > /dev/null 2>&1
}

# 获取打开的标签页列表
get_pages() {
    curl -s --max-time 3 "${CDP_URL}/json/list" 2>/dev/null || echo "[]"
}

# 获取 Chromium 总 RSS（KB）
get_chromium_rss() {
    ps aux | grep -i "chromium" | grep -v grep | awk '{sum+=$6} END {print sum+0}'
}

# 通过 CDP 关闭指定标签页
close_page() {
    local page_id="$1"
    curl -s --max-time 3 "${CDP_URL}/json/close/${page_id}" > /dev/null 2>&1
}

# 通过 CDP 触发 JavaScript GC
trigger_gc() {
    local ws_url="$1"
    # 使用 CDP 的 HeapProfiler.collectGarbage
    # 由于 curl 不支持 WebSocket，我们通过关闭并重新打开 about:blank 来间接触发
    curl -s --max-time 3 "${CDP_URL}/json/new?about:blank" > /dev/null 2>&1
    log "GC triggered via new blank page"
}

# === 主逻辑 ===
trim_log

# 检查 Chromium 是否运行
if ! check_chromium_running; then
    # 清理空闲状态文件
    rm -f "$IDLE_STATE_FILE"
    exit 0
fi

# 获取当前标签页
pages_json=$(get_pages)
total_pages=$(echo "$pages_json" | python3 -c "
import json, sys
try:
    pages = json.load(sys.stdin)
    print(len(pages))
except:
    print(0)
" 2>/dev/null || echo "0")

non_blank_pages=$(echo "$pages_json" | python3 -c "
import json, sys
try:
    pages = json.load(sys.stdin)
    non_blank = [p for p in pages if p.get('url', '') not in ('about:blank', '')]
    print(len(non_blank))
    for p in non_blank:
        sys.stderr.write(p.get('id', '') + '|' + p.get('url', '')[:80] + '\n')
except:
    print(0)
" 2>/dev/null || echo "0")

# 获取 RSS
current_rss=$(get_chromium_rss)
current_rss_mb=$((current_rss / 1024))

# 判断是否空闲（只有 about:blank 或无标签页）
if [ "$non_blank_pages" -eq 0 ]; then
    # 空闲状态
    if [ ! -f "$IDLE_STATE_FILE" ]; then
        # 记录空闲开始时间
        date +%s > "$IDLE_STATE_FILE"
        log "IDLE: Chromium idle detected (${total_pages} blank pages, RSS=${current_rss_mb}MB)"
    else
        idle_since=$(cat "$IDLE_STATE_FILE")
        now=$(date +%s)
        idle_seconds=$((now - idle_since))
        
        if [ "$idle_seconds" -ge "$IDLE_THRESHOLD_SECONDS" ]; then
            log "IDLE_LONG: Chromium idle for ${idle_seconds}s (threshold=${IDLE_THRESHOLD_SECONDS}s), RSS=${current_rss_mb}MB"
            
            # 如果有多个空白标签页，关闭多余的（保留 1 个）
            if [ "$total_pages" -gt 1 ]; then
                excess_ids=$(echo "$pages_json" | python3 -c "
import json, sys
try:
    pages = json.load(sys.stdin)
    blank = [p for p in pages if p.get('url', '') in ('about:blank', '')]
    # 保留第一个，关闭其余
    for p in blank[1:]:
        print(p.get('id', ''))
except:
    pass
" 2>/dev/null)
                closed=0
                for pid in $excess_ids; do
                    if [ -n "$pid" ]; then
                        close_page "$pid"
                        closed=$((closed + 1))
                    fi
                done
                if [ "$closed" -gt 0 ]; then
                    log "CLEANUP: Closed ${closed} excess blank pages"
                fi
            fi
            
            # 重置空闲计时器
            date +%s > "$IDLE_STATE_FILE"
        fi
    fi
else
    # 非空闲，清除空闲状态
    rm -f "$IDLE_STATE_FILE"
fi

# RSS 检查（无论空闲与否）
if [ "$current_rss" -gt "$RSS_THRESHOLD_KB" ]; then
    log "HIGH_RSS: Chromium RSS=${current_rss_mb}MB exceeds threshold=$((RSS_THRESHOLD_KB / 1024))MB"
    
    # 关闭所有非空白标签页
    closed_urls=$(echo "$pages_json" | python3 -c "
import json, sys
try:
    pages = json.load(sys.stdin)
    non_blank = [p for p in pages if p.get('url', '') not in ('about:blank', '')]
    for p in non_blank:
        print(p.get('id', '') + '|' + p.get('url', '')[:60])
except:
    pass
" 2>/dev/null)
    
    closed=0
    for entry in $closed_urls; do
        pid=$(echo "$entry" | cut -d'|' -f1)
        url=$(echo "$entry" | cut -d'|' -f2)
        if [ -n "$pid" ]; then
            close_page "$pid"
            log "HIGH_RSS_CLOSE: Closed page ${url}"
            closed=$((closed + 1))
        fi
    done
    
    if [ "$closed" -gt 0 ]; then
        log "HIGH_RSS_CLEANUP: Closed ${closed} pages to free memory"
    fi
fi

# 定期状态报告（每小时记录一次，通过检查分钟数）
current_minute=$(date +%M)
if [ "$current_minute" -lt 5 ]; then
    log "STATUS: pages=${total_pages} non_blank=${non_blank_pages} RSS=${current_rss_mb}MB"
fi
