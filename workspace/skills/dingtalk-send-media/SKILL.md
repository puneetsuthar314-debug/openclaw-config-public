# dingtalk-send-media

向当前钉钉会话发送图片或文件。

## 核心规则（必须遵守！）

**`[DING:IMAGE]` 和 `[DING:FILE]` 标签必须直接出现在你的回复文本中。**

系统会自动检测回复中的这些标签，将本地文件上传到钉钉并发送给用户。

**绝对不要**通过 `message` 工具发送这些标签！通过 message 工具发送的内容不会被解析，标签会变成纯文本显示给用户。

## 发送图片

### 图片搜索和发送的完整流程

#### 步骤 1：使用 image_search.py 搜索并下载图片

```bash
/root/anaconda3/bin/python3 /usr/local/bin/image_search.py "搜索关键词" --limit 3 --output /root/.openclaw/workspace/images --json
```

#### 步骤 2：验证下载的图片

```bash
file /path/to/downloaded/image.jpg
ls -lh /path/to/downloaded/image.jpg
```

确认 `file` 命令显示的是真正的图片格式（JPEG/PNG），文件大小 > 5KB。

#### 步骤 3：在回复中直接输出标签

```
这是我找到的图片：
[DING:IMAGE path="/root/.openclaw/workspace/images/img_1_xxxx.jpg"]
```

## 发送文件

```
这是你要的文件：
[DING:FILE path="/root/.openclaw/workspace/files/xxx.pdf"]
```

## 严格禁止

- **禁止** 通过 message 工具发送 `[DING:IMAGE]` 或 `[DING:FILE]` 标签
- **禁止** 直接用 curl/wget 下载图片 URL（用 image_search.py 代替）
- **禁止** 发送未经 file 命令验证的文件
- **禁止** 在标签的 path 中使用远程 URL（只允许本地绝对路径）

## 为什么不能用 message 工具？

1. `[DING:IMAGE]` 标签的解析发生在 monitor.js 的 deliver 函数中
2. 只有 assistant 角色的直接回复内容才会经过 deliver 函数
3. 通过 message 工具发送的内容走的是不同的代码路径，不经过标签解析
4. 通过 message 工具指定 target 会导致群聊消息被错误发送到私聊
