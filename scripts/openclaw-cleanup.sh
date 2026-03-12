#!/bin/bash
# OpenClaw 定期清理脚本
# 每周日凌晨 3:30 自动执行
LOG=/tmp/openclaw-cleanup.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始清理" >> $LOG
# 1. 清理废弃会话文件
SESSIONS_DIR=/root/.openclaw/agents/main/sessions
DEL_COUNT=$(ls $SESSIONS_DIR/*.deleted* $SESSIONS_DIR/*.reset* 2>/dev/null | wc -l)
if [ $DEL_COUNT -gt 0 ]; then
    find $SESSIONS_DIR -name '*.deleted*' -o -name '*.reset*' -delete 2>/dev/null
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 已清理废弃会话文件: ${DEL_COUNT} 个" >> $LOG
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 无废弃会话文件" >> $LOG
fi
# 2. 清理 Chromium 浏览器缓存（保留 cookies/登录状态）
for profile_dir in /root/.openclaw/browser/clawd/user-data/Default \
                   /root/.openclaw/browser/openclaw/user-data/Default \
                   /root/.openclaw/browser/data/user-data/Default; do
    if [ -d "$profile_dir" ]; then
        for cache_dir in Cache "Code Cache" GPUCache ShaderCache CachedData; do
            [ -d "$profile_dir/$cache_dir" ] && find "$profile_dir/$cache_dir" -type f -delete 2>/dev/null
        done
    fi
done
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 浏览器缓存已清理" >> $LOG
# 3. 清理超过 7 天的日志
find /tmp/openclaw/ -name '*.log' -mtime +7 -delete 2>/dev/null
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 清理完成" >> $LOG
