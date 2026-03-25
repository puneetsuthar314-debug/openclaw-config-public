#!/bin/bash
# ============================================================
# soul-guardian-watcher.sh — OpenClaw 核心文件主动防御
# 使用 inotifywait 实时监控核心配置文件的篡改
# ============================================================

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
AUDIT_LOG="/var/log/soul-guardian.log"
GUARDIAN_DIR="$WORKSPACE/memory/soul-guardian"
APPROVED_DIR="$GUARDIAN_DIR/approved"
QUARANTINE_DIR="$GUARDIAN_DIR/quarantine"
AUDIT_JSONL="$GUARDIAN_DIR/audit.jsonl"

# 需要监控的核心文件
WATCHED_FILES=(
    "SOUL.md"
    "SECURITY.md"
    "AGENTS.md"
    "MEMORY.md"
    "USER.md"
    "IDENTITY.md"
)

# 确保目录存在
mkdir -p "$APPROVED_DIR" "$QUARANTINE_DIR" "$(dirname "$AUDIT_LOG")"

log() {
    local ts=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
    echo "[$ts] $1" | tee -a "$AUDIT_LOG"
}

log_jsonl() {
    local ts=$(date -u +"%Y-%m-%dT%H:%M:%S+00:00")
    local event="$1"
    local path="$2"
    local note="$3"
    echo "{\"ts\": \"$ts\", \"event\": \"$event\", \"actor\": \"inotify-watcher\", \"path\": \"$path\", \"note\": \"$note\"}" >> "$AUDIT_JSONL"
}

# 初始化：为每个核心文件创建 baseline hash
init_baselines() {
    log "初始化核心文件 baseline..."
    for file in "${WATCHED_FILES[@]}"; do
        local filepath="$WORKSPACE/$file"
        if [ -f "$filepath" ]; then
            local hash=$(sha256sum "$filepath" | cut -d' ' -f1)
            echo "$hash" > "$APPROVED_DIR/$file.sha256"
            log "  $file: baseline=$hash"
            log_jsonl "baseline_init" "$file" "hash=$hash"
        else
            log "  $file: 文件不存在，跳过"
        fi
    done
    log "Baseline 初始化完成"
}

# 检查文件是否被篡改
check_integrity() {
    local file="$1"
    local filepath="$WORKSPACE/$file"
    local baseline_file="$APPROVED_DIR/$file.sha256"
    
    if [ ! -f "$baseline_file" ]; then
        log "WARNING: $file 没有 baseline，重新初始化"
        if [ -f "$filepath" ]; then
            sha256sum "$filepath" | cut -d' ' -f1 > "$baseline_file"
        fi
        return 0
    fi
    
    if [ ! -f "$filepath" ]; then
        log "ALERT: $file 被删除！"
        log_jsonl "file_deleted" "$file" "核心文件被删除"
        return 1
    fi
    
    local current_hash=$(sha256sum "$filepath" | cut -d' ' -f1)
    local baseline_hash=$(cat "$baseline_file")
    
    if [ "$current_hash" != "$baseline_hash" ]; then
        log "ALERT: $file 被修改！baseline=$baseline_hash current=$current_hash"
        log_jsonl "file_modified" "$file" "hash_mismatch baseline=$baseline_hash current=$current_hash"
        
        # 备份被修改的文件到隔离区
        local quarantine_name="${file}.$(date +%Y%m%d%H%M%S)"
        cp "$filepath" "$QUARANTINE_DIR/$quarantine_name"
        log "  已将修改版本备份到隔离区: $quarantine_name"
        
        return 1
    fi
    
    return 0
}

# 批准当前版本（更新 baseline）
approve_current() {
    local file="$1"
    local filepath="$WORKSPACE/$file"
    
    if [ -f "$filepath" ]; then
        local hash=$(sha256sum "$filepath" | cut -d' ' -f1)
        echo "$hash" > "$APPROVED_DIR/$file.sha256"
        log "APPROVED: $file 新 baseline=$hash"
        log_jsonl "approved" "$file" "new_baseline=$hash"
    fi
}

# 主监控循环
main() {
    log "=== Soul Guardian Watcher 启动 ==="
    
    # 检查 inotifywait 是否可用
    if ! command -v inotifywait &>/dev/null; then
        log "ERROR: inotifywait 未安装。请执行: dnf install -y inotify-tools"
        log "降级为轮询模式（每 30 秒检查一次）"
        
        # 初始化 baseline
        init_baselines
        
        # 轮询模式
        while true; do
            for file in "${WATCHED_FILES[@]}"; do
                check_integrity "$file" || true
            done
            sleep 30
        done
    else
        # 初始化 baseline
        init_baselines
        
        # 构建监控路径列表
        local watch_paths=()
        for file in "${WATCHED_FILES[@]}"; do
            watch_paths+=("$WORKSPACE/$file")
        done
        
        log "启动 inotify 实时监控..."
        
        # 使用 inotifywait 监控文件修改
        inotifywait -m -e modify,delete,move --format '%w%f %e %T' --timefmt '%Y-%m-%d %H:%M:%S' \
            "${watch_paths[@]}" 2>/dev/null | while read -r filepath event timestamp; do
            
            local filename=$(basename "$filepath")
            log "DETECTED: $filename event=$event at $timestamp"
            log_jsonl "inotify_event" "$filename" "event=$event"
            
            # 检查完整性
            check_integrity "$filename" || true
        done
    fi
}

# 命令行接口
case "${1:-watch}" in
    init)
        init_baselines
        ;;
    check)
        for file in "${WATCHED_FILES[@]}"; do
            check_integrity "$file" && echo "OK: $file" || echo "ALERT: $file"
        done
        ;;
    approve)
        if [ -n "${2:-}" ]; then
            approve_current "$2"
        else
            for file in "${WATCHED_FILES[@]}"; do
                approve_current "$file"
            done
        fi
        ;;
    watch)
        main
        ;;
    *)
        echo "用法: $0 {init|check|approve [file]|watch}"
        exit 1
        ;;
esac
