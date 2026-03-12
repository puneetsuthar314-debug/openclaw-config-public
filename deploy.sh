#!/bin/bash
# ============================================================
# OpenClaw 一键灾难恢复部署脚本
# 用途：在全新服务器上快速恢复 OpenClaw 系统
# 使用方法：
#   1. 在新服务器上 clone 此私密仓库
#   2. chmod +x deploy.sh && ./deploy.sh
# ============================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── 前置检查 ──────────────────────────────────────────
if [ "$(id -u)" -ne 0 ]; then
    log_error "请使用 root 用户运行此脚本"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCLAW_DIR="$HOME/.openclaw"

log_info "=========================================="
log_info "  OpenClaw 灾难恢复部署脚本"
log_info "=========================================="
echo ""

# ── 第 1 步：安装 Node.js (如果未安装) ──────────────────
if ! command -v node &>/dev/null; then
    log_info "正在安装 Node.js 22.x ..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
    apt-get install -y nodejs
else
    log_info "Node.js 已安装: $(node --version)"
fi

# ── 第 2 步：安装 OpenClaw ──────────────────────────────
if ! command -v openclaw &>/dev/null; then
    log_info "正在安装 OpenClaw ..."
    npm install -g openclaw
else
    log_info "OpenClaw 已安装: $(openclaw --version 2>/dev/null || echo 'unknown')"
fi

# ── 第 3 步：恢复配置文件 ──────────────────────────────
log_info "正在恢复配置文件到 $OPENCLAW_DIR ..."

# 备份已有配置（如果存在）
if [ -d "$OPENCLAW_DIR" ]; then
    BACKUP_NAME="${OPENCLAW_DIR}.backup-$(date +%Y%m%d_%H%M%S)"
    log_warn "发现已有配置，备份到 $BACKUP_NAME"
    mv "$OPENCLAW_DIR" "$BACKUP_NAME"
fi

mkdir -p "$OPENCLAW_DIR"

# 复制核心配置
cp "$SCRIPT_DIR/openclaw.json" "$OPENCLAW_DIR/"
cp "$SCRIPT_DIR/.env" "$OPENCLAW_DIR/"
cp "$SCRIPT_DIR/mcp.json" "$OPENCLAW_DIR/"
cp "$SCRIPT_DIR/exec-approvals.json" "$OPENCLAW_DIR/" 2>/dev/null || true

# 复制 identity（设备身份）
if [ -d "$SCRIPT_DIR/identity" ]; then
    cp -r "$SCRIPT_DIR/identity" "$OPENCLAW_DIR/"
fi

# 复制 workspace（工作区，包含 SOUL.md 等核心人格文件）
if [ -d "$SCRIPT_DIR/workspace" ]; then
    cp -r "$SCRIPT_DIR/workspace" "$OPENCLAW_DIR/"
fi

# 复制 workspace-coding 和 workspace-researcher
for ws in workspace-coding workspace-researcher; do
    if [ -d "$SCRIPT_DIR/$ws" ]; then
        cp -r "$SCRIPT_DIR/$ws" "$OPENCLAW_DIR/"
    fi
done

# 复制 cron 任务配置
if [ -d "$SCRIPT_DIR/cron" ]; then
    cp -r "$SCRIPT_DIR/cron" "$OPENCLAW_DIR/"
fi

# 复制 agents 配置
if [ -d "$SCRIPT_DIR/agents" ]; then
    cp -r "$SCRIPT_DIR/agents" "$OPENCLAW_DIR/"
fi

# 复制 memory
if [ -d "$SCRIPT_DIR/memory" ]; then
    cp -r "$SCRIPT_DIR/memory" "$OPENCLAW_DIR/"
fi

# 设置正确的文件权限
chmod 700 "$OPENCLAW_DIR"
chmod 600 "$OPENCLAW_DIR/openclaw.json"
chmod 600 "$OPENCLAW_DIR/.env"
chmod 600 "$OPENCLAW_DIR/exec-approvals.json" 2>/dev/null || true
chmod -R 700 "$OPENCLAW_DIR/identity" 2>/dev/null || true

log_info "配置文件恢复完成"

# ── 第 4 步：安装钉钉插件 ──────────────────────────────
log_info "正在安装钉钉插件 ..."
npm install -g clawdbot-dingtalk || log_warn "钉钉插件安装失败，请手动安装"

# ── 第 5 步：安装自动化脚本 ──────────────────────────────
log_info "正在安装自动化脚本 ..."

# 安装 cleanup 脚本
if [ -f "$SCRIPT_DIR/scripts/openclaw-cleanup.sh" ]; then
    cp "$SCRIPT_DIR/scripts/openclaw-cleanup.sh" /usr/local/bin/
    chmod +x /usr/local/bin/openclaw-cleanup.sh
fi

# 安装 health check 脚本
if [ -f "$SCRIPT_DIR/scripts/openclaw-health-check.sh" ]; then
    cp "$SCRIPT_DIR/scripts/openclaw-health-check.sh" /usr/local/bin/
    chmod +x /usr/local/bin/openclaw-health-check.sh
fi

# 安装 job-runner
if [ -f "$SCRIPT_DIR/scripts/job-runner" ]; then
    cp "$SCRIPT_DIR/scripts/job-runner" /usr/local/bin/
    chmod +x /usr/local/bin/job-runner
fi

# ── 第 6 步：安装 systemd 服务 ──────────────────────────
log_info "正在安装 systemd 服务 ..."

cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway Service
Documentation=https://docs.openclaw.ai/gateway
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
User=root
WorkingDirectory=/root
Environment=HOME=/root
Environment=PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Environment=OPENCLAW_NO_RESPAWN=1
EnvironmentFile=-/root/.openclaw/.env
ExecStart=/usr/bin/openclaw gateway
ExecReload=/usr/bin/openclaw gateway restart
Restart=always
RestartSec=5
StandardOutput=append:/var/log/openclaw-gateway.log
StandardError=append:/var/log/openclaw-gateway.log
OOMScoreAdjust=-500
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
RestrictSUIDSGID=true
LimitNOFILE=65536
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

# ── 第 7 步：安装 crontab ──────────────────────────────
log_info "正在配置 crontab ..."

(crontab -l 2>/dev/null; echo "# OpenClaw 定时任务
# 每周日 03:30 执行清理
30 3 * * 0 /usr/local/bin/job-runner /usr/local/bin/openclaw-cleanup.sh 300
# 每小时执行健康检查
0 * * * * /usr/local/bin/job-runner /usr/local/bin/openclaw-health-check.sh 120") | sort -u | crontab -

# ── 第 8 步：启动服务 ──────────────────────────────────
log_info "正在启动 OpenClaw Gateway ..."
systemctl enable openclaw-gateway
systemctl start openclaw-gateway

sleep 3

if systemctl is-active --quiet openclaw-gateway; then
    log_info "OpenClaw Gateway 启动成功!"
else
    log_error "OpenClaw Gateway 启动失败，请检查日志: journalctl -u openclaw-gateway"
fi

# ── 完成 ──────────────────────────────────────────────
echo ""
log_info "=========================================="
log_info "  部署完成!"
log_info "=========================================="
echo ""
log_info "服务状态: systemctl status openclaw-gateway"
log_info "查看日志: tail -f /var/log/openclaw-gateway.log"
log_info "安全审计: openclaw security audit"
log_info "Dashboard: http://localhost:18789"
echo ""
log_warn "重要提醒："
log_warn "1. 如果更换了服务器IP，钉钉机器人的回调地址可能需要更新"
log_warn "2. 请运行 'openclaw security audit' 检查安全状态"
log_warn "3. identity/ 中的设备身份可能需要重新注册"
