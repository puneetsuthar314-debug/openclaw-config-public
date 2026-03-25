# 审计日志：GLM-5 主控模型升级

- **日期**: 2026-03-17
- **操作者**: Manus AI (受用户指令)
- **变更类型**: 模型配置升级

## 变更内容

| 项目 | 变更前 | 变更后 |
|------|--------|--------|
| 丫丫-主控 primary | dashscope/qwen3.5-plus | **dashscope/glm-5** |
| 丫丫-主控 fallbacks | 无 | qwen3.5-plus → kimi-k2.5 |
| 丫丫-研究 primary | dashscope/qwen3-max-2026-01-23 | **dashscope/glm-5** |
| 丫丫-研究 fallbacks | 无 | qwen3-max-2026-01-23 |
| 默认模型 | dashscope/qwen3.5-plus | **dashscope/glm-5** |
| 模型路由规则 | qwen3.5-plus 为默认 | **glm-5 为默认主控** |

## 修改的文件

1. `/root/.openclaw/openclaw.json` — 主控和研究员模型改为 glm-5，添加 fallback 链
2. `/root/.openclaw/workspace/vault/systems/model-routing.md` — 路由规则重写，glm-5 为默认

## 备份

- `openclaw.json.bak.202603171352` — 变更前的完整备份

## 风险提示

- GLM-5 工具调用存在不稳定风险（社区反馈错误率 2-6%），已配置 fallback 降级到 qwen3.5-plus
- GLM-5 maxTokens 限制为 16384，长输出任务应切换到 coder 或 minimax
- 建议观察 3-5 天，关注 Coding Plan Pro 用量变化
