# Agent 工作日志

**日期**: 2026-03-16
**Agent**: Manus AI (外部)
**任务**: 修复 Playwright Chromium 浏览器未安装的问题

## 执行摘要

成功安装 Playwright Chromium 浏览器核心（v1208，Chrome for Testing 145.0.7632.6），修复了浏览器自动化功能。

## 问题描述

Playwright Python 包已安装，但其所需的 Chromium 浏览器二进制文件未下载安装，导致所有需要浏览器自动化的任务（如动态网页抓取、截图、JS 渲染页面访问）均无法执行。

## 操作详情

### 安装过程

1. **尝试 `playwright install chromium`**：由于 `cdn.playwright.dev` 在海外，服务器直连下载速度极慢（约 60-100 KB/s），多次超时断连。
2. **尝试 npmmirror 国内镜像**：镜像尚未同步 v1208 版本，返回 404。
3. **最终方案 - 中转下载**：
   - 在 Manus 沙箱环境中以 20 MB/s 高速下载两个文件（共 279MB）
   - 通过 scp + rsync 传输到目标服务器
   - 手动解压到 Playwright 浏览器目录 `/root/.cache/ms-playwright/`

### 安装的文件

| 文件 | 大小 | 安装路径 |
|---|---|---|
| chrome-linux64.zip | 175,440,843 bytes | `/root/.cache/ms-playwright/chromium-1208/chrome-linux64/` |
| chrome-headless-shell-linux64.zip | 116,288,461 bytes | `/root/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/` |

### 验证测试

| 测试项 | 结果 |
|---|---|
| 浏览器启动 (headless) | 通过 |
| 访问百度 | 通过（标题: 百度一下，你就知道） |
| 截图功能 | 通过（81558 bytes） |
| JavaScript 执行 | 通过 |
| 访问 GitHub (JS渲染) | 通过（标题正确） |

## 注意事项

- 系统依赖（apt-get）未安装成功（Alibaba Cloud Linux 不支持 apt-get），但实测浏览器可正常运行
- 如果未来升级 Playwright 版本，需要重新下载对应版本的浏览器

---

## 追加：Playwright 优化记录

**时间**: 2026-03-16 (第二轮)

### 发现的问题与修复

| 问题 | 根因 | 修复方案 |
|---|---|---|
| 截图超时 (30s) | 百度页面动画/字体加载阻塞 | 注入 CSS 禁用动画 + 仅截可视区域 |
| 百度搜索框不可见 | 百度对 Headless 浏览器隐藏了 `#form` (`display:none`) | 用 JS 强制显示所有隐藏的祖先元素 |
| GitHub 访问超时 | 国内直连海外站点慢 | 通过 Mihomo 代理 (127.0.0.1:7890) 访问 |

### 最佳实践总结（供丫丫 Agent 参考）

1. **桌面模式**：始终设置 `viewport: 1920x1080` + 桌面 UA，避免网站返回移动端页面
2. **反爬处理**：百度等网站会对 Headless 浏览器隐藏元素，使用 `force_show_hidden_ancestors()` 函数强制显示
3. **截图优化**：注入 `animation: none !important` CSS 禁用动画，避免字体加载超时
4. **海外网站**：创建带 `proxy={"server": "http://127.0.0.1:7890"}` 的 context 访问
5. **等待策略**：优先用 `domcontentloaded` 而非 `networkidle`，配合 `time.sleep()` 等待 JS 渲染

### 最终测试结果

12 项测试全部通过，通过率 100%。
