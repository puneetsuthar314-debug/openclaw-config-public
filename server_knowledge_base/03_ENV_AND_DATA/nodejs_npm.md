> **核心洞察**：这是一个为 `OpenClaw` 平台服务的 Node.js 环境，当前与 `ProjectChimera` 无关。

# 03 - 环境：Node.js 与 NPM

**最后更新**: `2026-03-17`

## 1. 用途与关联

- **主要服务对象**: `openclaw-gateway` 服务是一个 Node.js 应用，因此该 Node.js 环境是其运行的必要条件。
- **与 ProjectChimera 的关系**: **无**。`ProjectChimera` 是一个纯 Python 后端项目，不使用 Node.js。
- **缓存占用**: NPM 缓存 (`/root/.npm/`) 占用了超过 500MB 的空间，是磁盘清理时可以考虑的目标之一。

## 2. 操作建议

- **不要轻易删除**: 除非你准备弃用 `OpenClaw` 平台，否则不要卸载 Node.js 或清理其核心模块。
- **清理缓存**: 如果磁盘空间紧张，可以执行 `npm cache clean --force` 来释放空间。

## 3. 关键信息

- **Node.js 版本**: `v22.22.1`
- **NPM 缓存目录**: `/root/.npm/`
