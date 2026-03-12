# 知识库 (KNOWLEDGE.md)

> 此文件记录积累的领域知识、常用命令和重要发现。

## 服务器环境

- OS: Alibaba Cloud Linux 3
- OpenClaw 版本: v2026.3.7
- 主要 AI 提供商: DashScope (阿里云)
- 渠道: 钉钉 (clawdbot-dingtalk)
- 服务管理: systemd user service

## 常用命令

```bash
# 查看 OpenClaw 状态
systemctl --user status openclaw-gateway.service

# 重启服务
systemctl --user restart openclaw-gateway.service

# 查看实时日志
journalctl --user -u openclaw-gateway.service -f

# 查看今日日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

## 已知问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| auto-backup 失败 | staffId.notExisted | 检查钉钉用户ID配置 |
| memory-core 插件缺失 | 插件未安装 | 安装 memory-core 插件 |
| 服务频繁重启 | 内存压力/未知异常 | 已优化 systemd 配置 |

