#!/bin/bash
# OpenClaw 健康检查脚本
# 每小时由 crontab 执行一次
LOG_FILE="/var/log/openclaw-health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] 开始健康检查..." >> "$LOG_FILE"
# 1. 检查进程
if pgrep -f "openclaw-gatewa" > /dev/null 2>&1; then
    echo "[$TIMESTAMP] [OK] openclaw-gateway 进程正常" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] [ALERT] openclaw-gateway 进程不存在，尝试重启..." >> "$LOG_FILE"
    OPENCLAW_BIN=$(which openclaw 2>/dev/null || echo "/usr/bin/openclaw")
    if [ -x "$OPENCLAW_BIN" ]; then
        "$OPENCLAW_BIN" gateway restart >> "$LOG_FILE" 2>&1
    else
        export HOME=/root
        nohup openclaw gateway >> /var/log/openclaw-gateway.log 2>&1 &
    fi
    sleep 10
    if pgrep -f "openclaw-gatewa" > /dev/null 2>&1; then
        echo "[$TIMESTAMP] [OK] 重启成功" >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] [CRITICAL] 重启失败！" >> "$LOG_FILE"
    fi
fi
# 2. 检查端口
if ss -tlnp | grep -q ":18789"; then
    echo "[$TIMESTAMP] [OK] 端口18789正常监听" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] [ALERT] 端口18789未监听" >> "$LOG_FILE"
fi
# 3. 检查内存使用率
MEM_TOTAL=$(free | awk '/^Mem:/{print $2}')
MEM_USED=$(free | awk '/^Mem:/{print $3}')
MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
echo "[$TIMESTAMP] [INFO] 内存使用率: ${MEM_PERCENT}%" >> "$LOG_FILE"
if [ "$MEM_PERCENT" -gt 90 ]; then
    echo "[$TIMESTAMP] [ALERT] 内存使用率超过90%！" >> "$LOG_FILE"
fi
# 4. 检查磁盘使用率
DISK_PERCENT=$(df / | awk 'NR==2{print $5}' | tr -d '%')
echo "[$TIMESTAMP] [INFO] 磁盘使用率: ${DISK_PERCENT}%" >> "$LOG_FILE"
if [ "$DISK_PERCENT" -gt 85 ]; then
    echo "[$TIMESTAMP] [ALERT] 磁盘使用率超过85%！" >> "$LOG_FILE"
fi
# 5. 检查 openclaw 进程内存
OC_PID=$(pgrep -f "openclaw-gatewa" | head -1)
if [ -n "$OC_PID" ]; then
    OC_RSS=$(ps -p "$OC_PID" -o rss= 2>/dev/null | tr -d ' ')
    OC_RSS_MB=$((OC_RSS / 1024))
    echo "[$TIMESTAMP] [INFO] OpenClaw内存: ${OC_RSS_MB}MB" >> "$LOG_FILE"
fi
echo "[$TIMESTAMP] 健康检查完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
# 保留最近1000行日志
tail -1000 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
