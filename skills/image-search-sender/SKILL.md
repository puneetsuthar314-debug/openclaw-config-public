# image-search-sender
搜索图片并通过钉钉发送给用户的一站式技能。

## 使用场景
当用户要求发送图片（如"发一张猫的图片"、"找5张壁纸"、"搜一张XX的照片"）时使用此技能。

## ⚠️ 严重警告
**绝对禁止**使用 `aliyun_code_interpreter` 下载图片！code_interpreter 在远程沙箱中执行，下载的文件只存在于远程沙箱，本地服务器上不存在，会导致 `[DING:IMAGE]` 发送失败（"图片上传失败"）。
必须使用下面的 `image_search.py` 脚本通过本地 `exec` 工具下载图片。

## 使用步骤

### 第一步：搜索图片（必须用 exec 工具在本地执行）
```bash
/root/anaconda3/bin/python3 /usr/local/bin/image_search.py "关键词 高清" --limit 5 --output /root/.openclaw/workspace/images --json
```
参数说明：
- 关键词后面加"高清"可以提高图片质量
- `--limit N` 下载 N 张候选图片（根据用户要求的数量设置）
- `--output` 指定保存目录
- `--json` 输出 JSON 格式结果

### 第二步：验证图片有效性
```bash
file /root/.openclaw/workspace/images/下载的图片文件名
```
必须确认输出包含 `JPEG image data` 或 `PNG image data`。如果显示 `HTML document`、`XML` 或 `ASCII text`，说明下载失败，该文件是错误页面，必须删除。

### 第三步：发送到钉钉（⚠️ 每张图片都要单独写一个标签！）
确认图片有效后，**必须为每张图片都写一个 `[DING:IMAGE]` 标签**。如果用户要求 5 张，就必须写 5 个标签。

**正确示例（用户要求5张图片）：**
```
给你找到了5张蔡文姬的图片：

[DING:IMAGE path="/root/.openclaw/workspace/images/img_1_xxx.jpg"]

[DING:IMAGE path="/root/.openclaw/workspace/images/img_2_xxx.jpg"]

[DING:IMAGE path="/root/.openclaw/workspace/images/img_3_xxx.jpg"]

[DING:IMAGE path="/root/.openclaw/workspace/images/img_4_xxx.png"]

[DING:IMAGE path="/root/.openclaw/workspace/images/img_5_xxx.jpg"]
```

**错误示例（只发了1张）：**
```
[DING:IMAGE path="/root/.openclaw/workspace/images/img_1_xxx.jpg"]
```
这是错误的！用户要求了5张，你只发了1张。必须把所有下载成功的图片都发送出去。

## 注意事项
1. **绝对禁止**使用 `aliyun_code_interpreter` 下载图片——远程沙箱文件不在本地，必定失败
2. **绝对禁止**直接用 curl/wget 下载搜索结果中的图片 URL，因为大量 URL 已失效，会下载到 HTML 错误页面
3. 必须使用 `image_search.py` 脚本，它内置了文件头验证，只保存真正有效的图片
4. 如果图片都验证失败，换一个关键词重试
5. 发送前必须用 `file` 命令验证，不要跳过这一步
6. **用户要求几张就发几张**，必须为每张图片写一个单独的 `[DING:IMAGE]` 标签，不能偷懒只发一张
