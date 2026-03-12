# infra.md — 基础设施速查

## 服务器

- **主机**：阿里云 ECS（8.141.107.122）
- **系统**：Alibaba Cloud Linux 3
- **内存**：1.8GB
- **Node.js**：v22.14.0
- **Python**：3.12（conda base）

## OpenClaw

- **版本**：0.5.x
- **Gateway 端口**：18789
- **配置目录**：/root/.openclaw/
- **工作区**：/root/.openclaw/workspace/
- **进程管理**：nohup（无 systemd）

## 钉钉

- **插件**：clawdbot-dingtalk v0.4.6
- **连接方式**：Stream API
- **马斯克 staffId**：manager20

## API Keys（存储位置）

- 阿里云百炼 API Key → openclaw.json `models[].apiKey`
- Kimi API Key → openclaw.json `models[].apiKey`
- 钉钉 AppKey/Secret → openclaw.json `channels.dingtalk`
