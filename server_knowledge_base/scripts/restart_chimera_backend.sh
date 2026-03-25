#!/bin/bash
#
# restart_chimera_backend.sh
# 安全地重启 ProjectChimera 后端服务

# 1. 定义变量
PROJECT_DIR="/root/ProjectChimera"
BACKEND_DIR="${PROJECT_DIR}/backend"
LOG_FILE="/tmp/chimera_backend.log"

# 2. 检查目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo "[ERROR] 项目目录不存在: $PROJECT_DIR" >&2
    exit 1
fi

# 3. 杀死旧进程
OLD_PID=$(pgrep -f "ProjectChimera.backend.app.main:app")
if [ -n "$OLD_PID" ]; then
    echo "找到旧进程，PID: $OLD_PID，正在终止..."
    kill $OLD_PID
    sleep 2 # 等待进程退出
fi

# 4. 启动新进程
# 必须在 /root 目录下执行，以确保 Python 模块路径正确
echo "正在启动新进程..."
cd /root

# 激活 Anaconda 环境
source /root/anaconda3/bin/activate base

# 在后台启动 uvicorn
nohup python3 -m uvicorn ProjectChimera.backend.app.main:app --host 0.0.0.0 --port 5000 --reload > $LOG_FILE 2>&1 &

# 5. 验证
NEW_PID=$(pgrep -f "ProjectChimera.backend.app.main:app")
if [ -n "$NEW_PID" ]; then
    echo "[SUCCESS] ProjectChimera 后端已成功重启，新 PID: $NEW_PID"
    echo "日志文件位于: $LOG_FILE"
else
    echo "[ERROR] 重启失败，请检查日志文件: $LOG_FILE" >&2
    exit 1
fi
fi
