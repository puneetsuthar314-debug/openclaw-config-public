> **核心洞察**：这是一个**手动管理的网络代理工具**，用于在需要时访问特殊网络资源。它不会开机自启，需要手动管理。

# 02 - 服务：Mihomo 代理

**最后更新**: `2026-03-17`

## 1. 何时使用

当 Agent 需要执行的网络任务（如 `curl`、`git clone`）因网络问题（如连接超时、被墙）失败时，应考虑使用此代理。

## 2. 如何使用

要让某个命令通过此代理执行，你需要在命令前加上 `HTTP_PROXY` 环境变量的声明。

- **HTTP 代理**: `http://127.0.0.1:7890`
- **SOCKS5 代理**: `socks5://127.0.0.1:7891`

**示例**：

```bash
# 使用 HTTP 代理 curl 谷歌
HTTP_PROXY=http://127.0.0.1:7890 curl https://www.google.com

# 使用 HTTP 代理克隆 GitHub 仓库
export HTTP_PROXY=http://127.0.0.1:7890
git clone https://github.com/some/repo.git
unset HTTP_PROXY # 使用完毕后及时取消，避免影响其他命令
```

## 3. 服务管理

- **状态**: **默认离线**。该服务不会随服务器重启而自动启动。
- **启动命令**:
  ```bash
  nohup /usr/local/bin/mihomo -f /etc/mihomo_config.yaml > /tmp/mihomo.log 2>&1 &
  ```
- **停止命令**:
  ```bash
  pgrep -f mihomo | xargs kill
  ```
- **检查状态**:
  ```bash
  ps aux | grep mihomo
  ```

## 4. 关联性

- **当前使用者**: **无**。目前未发现服务器上有任何应用或全局配置默认使用此代理。它完全是一个按需使用的工具。
