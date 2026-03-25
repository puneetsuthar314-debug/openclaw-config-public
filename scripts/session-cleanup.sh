#!/bin/bash
# ============================================================
# session-cleanup.sh — OpenClaw 会话文件自动清理
# 定期清理过期的会话文件，防止磁盘爆满
# ============================================================

set -euo pipefail

LOG_FILE="/var/log/openclaw-cleanup.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

log "=== 开始会话清理 ==="

# --- 配置 ---
SESSION_BASE="/root/.openclaw/agents"
RETENTION_DAYS=7
FAILED_DELIVERY_RETENTION_DAYS=30
LCM_VACUUM_THRESHOLD_MB=500
GATEWAY_LOG="/var/log/openclaw-gateway.log"
GATEWAY_LOG_MAX_MB=50

# --- 1. 清理过期会话文件 ---
log "[1/5] 清理超过 ${RETENTION_DAYS} 天的会话文件..."
CLEANED_COUNT=0
CLEANED_SIZE=0

for agent_dir in "$SESSION_BASE"/*/sessions/; do
    if [ -d "$agent_dir" ]; then
        agent_name=$(basename "$(dirname "$agent_dir")")
        # 统计清理前大小
        before_size=$(du -sm "$agent_dir" 2>/dev/null | cut -f1)
        
        # 删除超过 RETENTION_DAYS 天的 .jsonl 文件
        find "$agent_dir" -name "*.jsonl" -mtime +${RETENTION_DAYS} -delete 2>/dev/null
        # 删除空的会话目录
        find "$agent_dir" -mindepth 1 -maxdepth 1 -type d -empty -delete 2>/dev/null
        
        after_size=$(du -sm "$agent_dir" 2>/dev/null | cut -f1)
        freed=$((before_size - after_size))
        
        if [ "$freed" -gt 0 ]; then
            log "  $agent_name: 释放 ${freed}MB (${before_size}MB → ${after_size}MB)"
            CLEANED_SIZE=$((CLEANED_SIZE + freed))
        fi
    fi
done
log "  会话清理完成，共释放 ${CLEANED_SIZE}MB"

# --- 2. 清理过期的失败投递记录 ---
log "[2/5] 清理超过 ${FAILED_DELIVERY_RETENTION_DAYS} 天的失败投递记录..."
FAILED_DIR="/root/.openclaw/delivery-queue/failed"
if [ -d "$FAILED_DIR" ]; then
    before_count=$(ls "$FAILED_DIR"/*.json 2>/dev/null | wc -l)
    find "$FAILED_DIR" -name "*.json" -mtime +${FAILED_DELIVERY_RETENTION_DAYS} -delete 2>/dev/null
    after_count=$(ls "$FAILED_DIR"/*.json 2>/dev/null | wc -l)
    deleted=$((before_count - after_count))
    log "  清理了 $deleted 条过期失败投递记录"
fi

# --- 3. LCM 数据库维护 ---
log "[3/5] LCM 数据库维护..."
LCM_DB="/root/.openclaw/lcm.db"
if [ -f "$LCM_DB" ]; then
    db_size_mb=$(du -sm "$LCM_DB" | cut -f1)
    log "  当前 lcm.db 大小: ${db_size_mb}MB"
    
    if [ "$db_size_mb" -gt "$LCM_VACUUM_THRESHOLD_MB" ]; then
        log "  数据库超过 ${LCM_VACUUM_THRESHOLD_MB}MB 阈值，执行 VACUUM..."
        # 使用 sqlite3 执行 VACUUM（如果可用）
        if command -v sqlite3 &>/dev/null; then
            sqlite3 "$LCM_DB" "VACUUM;" 2>/dev/null && \
                log "  VACUUM 完成，新大小: $(du -sm "$LCM_DB" | cut -f1)MB" || \
                log "  VACUUM 失败（数据库可能被锁定）"
        else
            log "  sqlite3 未安装，跳过 VACUUM"
        fi
    else
        log "  数据库大小正常，跳过 VACUUM"
    fi
fi

# --- 4. Gateway 日志轮转 ---
log "[4/5] Gateway 日志轮转..."
if [ -f "$GATEWAY_LOG" ]; then
    log_size_mb=$(du -sm "$GATEWAY_LOG" | cut -f1)
    log "  当前日志大小: ${log_size_mb}MB"
    
    if [ "$log_size_mb" -gt "$GATEWAY_LOG_MAX_MB" ]; then
        log "  日志超过 ${GATEWAY_LOG_MAX_MB}MB，执行轮转..."
        # 保留最近的日志，归档旧日志
        ARCHIVE="/var/log/openclaw-gateway.$(date +%Y%m%d).log.gz"
        cp "$GATEWAY_LOG" "${GATEWAY_LOG}.tmp"
        gzip -c "${GATEWAY_LOG}.tmp" > "$ARCHIVE"
        # 只保留最后 1000 行
        tail -1000 "${GATEWAY_LOG}.tmp" > "$GATEWAY_LOG"
        rm -f "${GATEWAY_LOG}.tmp"
        log "  日志已轮转，归档到 $ARCHIVE"
        
        # 清理超过 30 天的归档日志
        find /var/log/ -name "openclaw-gateway.*.log.gz" -mtime +30 -delete 2>/dev/null
    fi
fi

# --- 5. 临时文件清理 ---
log "[5/5] 清理临时文件..."
# 清理 /tmp 下的 openclaw 临时文件（超过 3 天）
find /tmp/openclaw* -mtime +3 -delete 2>/dev/null || true
# 清理浏览器崩溃转储
find /tmp/ -name "chromium-*" -mtime +1 -delete 2>/dev/null || true

# --- 汇总 ---
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}')
log "=== 清理完成 | 磁盘使用率: $DISK_USAGE ==="
