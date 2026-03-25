#!/bin/bash
# ============================================================
# workspace-doctor.sh — OpenClaw 工作区自治健康检查与自动修复
# 
# 功能：
#   1. 检测核心文件中的模型配置是否与 openclaw.json 一致
#   2. 检测并清理 .bak / .tmp 垃圾文件
#   3. 检测 MEMORY.md 是否膨胀（超过阈值）
#   4. 检测 projects 目录是否有命名冲突（空格/重复）
#   5. 检测 IDENTITY.md 是否为空模板
#   6. 生成健康报告并可选自动修复
#
# 用法：
#   workspace-doctor.sh check    # 仅检查，输出报告
#   workspace-doctor.sh fix      # 检查并自动修复可安全修复的问题
#   workspace-doctor.sh report   # 生成 Markdown 报告到 memory/
# ============================================================

set -euo pipefail

OPENCLAW_DIR="/root/.openclaw"
WORKSPACE="$OPENCLAW_DIR/workspace"
WORKSPACE_CODING="$OPENCLAW_DIR/workspace-coding"
WORKSPACE_RESEARCHER="$OPENCLAW_DIR/workspace-researcher"
CONFIG="$OPENCLAW_DIR/openclaw.json"
REPORT_FILE="$WORKSPACE/memory/doctor-report-$(date +%Y%m%d).md"
LOG_FILE="/var/log/openclaw-doctor.log"

# 计数器
ISSUES_FOUND=0
ISSUES_FIXED=0
MODE="${1:-check}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

issue() {
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    log "⚠️  问题 #$ISSUES_FOUND: $*"
}

fixed() {
    ISSUES_FIXED=$((ISSUES_FIXED + 1))
    log "✅ 已修复: $*"
}

# ============================================================
# 检查 1：模型配置一致性
# ============================================================
check_model_consistency() {
    log "--- 检查 1: 模型配置一致性 ---"
    
    # 从 openclaw.json 提取实际配置
    local main_model=$(python3 -c "
import json
d = json.load(open('$CONFIG'))
print(d['agents']['defaults']['model']['primary'].split('/')[-1])
" 2>/dev/null || echo "unknown")
    
    local researcher_model=$(python3 -c "
import json
d = json.load(open('$CONFIG'))
for a in d['agents']['list']:
    if a['id'] == 'researcher':
        print(a.get('model',{}).get('primary','default').split('/')[-1])
        break
" 2>/dev/null || echo "unknown")
    
    local coder_model=$(python3 -c "
import json
d = json.load(open('$CONFIG'))
for a in d['agents']['list']:
    if a['id'] == 'coder':
        print(a.get('model',{}).get('primary','default').split('/')[-1])
        break
" 2>/dev/null || echo "unknown")
    
    log "  实际配置 → 主控: $main_model, Coder: $coder_model, Researcher: $researcher_model"
    
    # 检查 coding AGENTS.md 中的主控描述
    if grep -q "GLM-5\|glm-5" "$WORKSPACE_CODING/AGENTS.md" 2>/dev/null; then
        issue "coding/AGENTS.md 中仍引用 GLM-5，实际主控为 $main_model"
        if [ "$MODE" = "fix" ]; then
            sed -i "s/GLM-5/$main_model/g" "$WORKSPACE_CODING/AGENTS.md"
            fixed "coding/AGENTS.md 中 GLM-5 已替换为 $main_model"
        fi
    fi
    
    # 检查 researcher AGENTS.md 中的主控描述
    if grep -q "GLM-5\|glm-5" "$WORKSPACE_RESEARCHER/AGENTS.md" 2>/dev/null; then
        issue "researcher/AGENTS.md 中仍引用 GLM-5，实际主控为 $main_model"
        if [ "$MODE" = "fix" ]; then
            sed -i "s/GLM-5/$main_model/g" "$WORKSPACE_RESEARCHER/AGENTS.md"
            fixed "researcher/AGENTS.md 中 GLM-5 已替换为 $main_model"
        fi
    fi
    
    # 检查 researcher AGENTS.md 中的默认模型描述是否匹配
    if ! grep -q "$researcher_model" "$WORKSPACE_RESEARCHER/AGENTS.md" 2>/dev/null; then
        issue "researcher/AGENTS.md 中的默认模型描述与实际配置 ($researcher_model) 不匹配"
    fi
    
    # 检查 MEMORY.md 中的架构描述
    if ! grep -q "$main_model\|Qwen3.5-Plus\|qwen3.5-plus" "$WORKSPACE/MEMORY.md" 2>/dev/null; then
        issue "MEMORY.md 中的主控模型描述可能已过时"
    fi
}

# ============================================================
# 检查 2：垃圾文件堆积
# ============================================================
check_garbage_files() {
    log "--- 检查 2: 垃圾文件堆积 ---"
    
    local bak_count=$(find "$WORKSPACE" "$WORKSPACE_CODING" "$WORKSPACE_RESEARCHER" -name "*.bak*" -type f 2>/dev/null | wc -l)
    local tmp_count=$(find "$OPENCLAW_DIR" -name "*.tmp" -type f 2>/dev/null | wc -l)
    local config_bak_count=$(find "$OPENCLAW_DIR" -maxdepth 1 -name "openclaw.json.*" -type f 2>/dev/null | wc -l)
    
    log "  .bak 文件: $bak_count, .tmp 文件: $tmp_count, 配置备份: $config_bak_count"
    
    if [ "$bak_count" -gt 5 ]; then
        issue "workspace 中有 $bak_count 个 .bak 文件堆积"
        if [ "$MODE" = "fix" ]; then
            find "$WORKSPACE" "$WORKSPACE_CODING" "$WORKSPACE_RESEARCHER" -name "*.bak*" -type f -delete
            fixed "已清理所有 workspace .bak 文件"
        fi
    fi
    
    if [ "$tmp_count" -gt 0 ]; then
        issue "发现 $tmp_count 个 .tmp 残留文件"
        if [ "$MODE" = "fix" ]; then
            find "$OPENCLAW_DIR" -name "*.tmp" -type f -mmin +60 -delete
            fixed "已清理超过 1 小时的 .tmp 文件"
        fi
    fi
    
    if [ "$config_bak_count" -gt 3 ]; then
        issue "openclaw.json 有 $config_bak_count 个备份，建议保留不超过 3 个"
        if [ "$MODE" = "fix" ]; then
            # 保留最新的 3 个，删除其余
            find "$OPENCLAW_DIR" -maxdepth 1 -name "openclaw.json.bak*" -type f | sort | head -n -1 | xargs rm -f
            fixed "已清理多余的 openclaw.json 备份"
        fi
    fi
}

# ============================================================
# 检查 3：MEMORY.md 膨胀检测
# ============================================================
check_memory_bloat() {
    log "--- 检查 3: MEMORY.md 膨胀检测 ---"
    
    local mem_lines=$(wc -l < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0)
    local mem_size=$(stat -c%s "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0)
    local mem_kb=$((mem_size / 1024))
    
    log "  MEMORY.md: $mem_lines 行, ${mem_kb}KB"
    
    if [ "$mem_lines" -gt 150 ]; then
        issue "MEMORY.md 已膨胀到 $mem_lines 行（建议 < 100 行），可能包含了不应存放的技能文档"
    fi
    
    if [ "$mem_kb" -gt 32 ]; then
        issue "MEMORY.md 大小为 ${mem_kb}KB，超过 32KB 上限"
    fi
    
    # 检查是否包含代码块（技能文档的标志）
    local code_blocks=0
    code_blocks=$(grep -c "\`\`\`" "$WORKSPACE/MEMORY.md" 2>/dev/null) || code_blocks=0
    if [ "$code_blocks" -gt 4 ]; then
        issue "MEMORY.md 中有 $code_blocks 个代码块，疑似混入了技能文档（应放在 skills/ 目录）"
    fi
}

# ============================================================
# 检查 4：项目目录命名冲突
# ============================================================
check_project_dirs() {
    log "--- 检查 4: 项目目录命名冲突 ---"
    
    local projects_dir="$WORKSPACE/projects"
    if [ ! -d "$projects_dir" ]; then
        log "  projects 目录不存在，跳过"
        return
    fi
    
    # 检查带空格的目录名（容易导致分裂）
    local space_dirs=$(find "$projects_dir" -maxdepth 1 -type d -name "* *" 2>/dev/null | wc -l)
    if [ "$space_dirs" -gt 0 ]; then
        issue "projects 下有 $space_dirs 个带空格的目录名（容易导致目录分裂）"
        find "$projects_dir" -maxdepth 1 -type d -name "* *" -exec echo "    → {}" \;
    fi
    
    # 检查空目录
    local empty_dirs=$(find "$projects_dir" -maxdepth 1 -type d -empty 2>/dev/null | wc -l)
    if [ "$empty_dirs" -gt 0 ]; then
        issue "projects 下有 $empty_dirs 个空目录"
        if [ "$MODE" = "fix" ]; then
            find "$projects_dir" -maxdepth 1 -type d -empty -delete
            fixed "已删除空的项目目录"
        fi
    fi
    
    # 检查根目录散落的文件
    local loose_files=$(find "$projects_dir" -maxdepth 1 -type f 2>/dev/null | wc -l)
    if [ "$loose_files" -gt 0 ]; then
        issue "projects 根目录有 $loose_files 个散落文件（应归入具体项目目录）"
    fi
}

# ============================================================
# 检查 5：IDENTITY.md 初始化状态
# ============================================================
check_identity() {
    log "--- 检查 5: IDENTITY.md 初始化状态 ---"
    
    for ws in "$WORKSPACE_CODING" "$WORKSPACE_RESEARCHER"; do
        local ws_name=$(basename "$ws")
        if grep -q "pick something" "$ws/IDENTITY.md" 2>/dev/null; then
            issue "$ws_name/IDENTITY.md 仍为未填写的模板"
        fi
    done
}

# ============================================================
# 检查 6：权限配置矛盾
# ============================================================
check_permission_conflicts() {
    log "--- 检查 6: 权限配置矛盾 ---"
    
    # 检查 researcher 是否同时被要求写入和禁止写入
    if grep -q "禁止写入" "$WORKSPACE_RESEARCHER/SECURITY_RULES.md" 2>/dev/null; then
        if grep "写入 memory" "$WORKSPACE_RESEARCHER/SOUL.md" | grep -qv "由主控" 2>/dev/null; then
            issue "researcher SOUL.md 要求写入 memory，但 SECURITY_RULES.md 禁止写入（权限矛盾）"
        fi
    fi
}

# ============================================================
# 生成报告
# ============================================================
generate_report() {
    cat > "$REPORT_FILE" << REPORT_EOF
# OpenClaw 工作区健康报告

**检查时间**：$(date '+%Y-%m-%d %H:%M:%S')
**检查模式**：$MODE
**发现问题**：$ISSUES_FOUND 个
**已修复**：$ISSUES_FIXED 个

## 检查结果摘要

$(cat "$LOG_FILE" | tail -50 | grep -E "⚠️|✅|---" | sed 's/^.*\] //')

## 建议

如果仍有未修复的问题，请运行：
\`\`\`bash
/root/.openclaw/scripts/workspace-doctor.sh fix
\`\`\`

---
_此报告由 workspace-doctor.sh 自动生成_
REPORT_EOF
    
    log "📋 报告已生成: $REPORT_FILE"
}

# ============================================================
# 主流程
# ============================================================
main() {
    log "=========================================="
    log "OpenClaw Workspace Doctor 启动 (模式: $MODE)"
    log "=========================================="
    
    check_model_consistency
    check_garbage_files
    check_memory_bloat
    check_project_dirs
    check_identity
    check_permission_conflicts
    
    log ""
    log "=========================================="
    log "检查完成: 发现 $ISSUES_FOUND 个问题, 修复 $ISSUES_FIXED 个"
    log "=========================================="
    
    if [ "$MODE" = "report" ] || [ "$ISSUES_FOUND" -gt 0 ]; then
        generate_report
    fi
    
    # 退出码：有未修复问题返回 1
    if [ "$ISSUES_FOUND" -gt "$ISSUES_FIXED" ]; then
        exit 1
    fi
    exit 0
}

main
