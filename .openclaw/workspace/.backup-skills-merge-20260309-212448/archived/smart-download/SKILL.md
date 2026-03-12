---
name: smart-download
description: "Intelligent file and media downloader. Automatically detects URL type and uses the best tool. Supports: web pages, images, videos (YouTube/Bilibili), audio, PDFs, documents, image galleries, and batch downloads. Triggers: download, 下载, save from URL, 保存, 帮我下, grab, fetch file, 抓取"
allowed-tools: Bash, Computer, Write, Read
---

# Smart Download — 智能下载器

## 核心能力
自动识别 URL 类型，选择最佳下载工具，支持所有常见格式。

## URL 类型识别与工具选择

| URL 类型 | 识别特征 | 使用工具 | 命令示例 |
|----------|----------|----------|----------|
| 普通文件 | .pdf/.docx/.zip 等 | aria2c | `aria2c -x 16 -d /path URL` |
| 图片 | .jpg/.png/.gif/.webp | wget/curl | `wget -O output.jpg URL` |
| YouTube 视频 | youtube.com/youtu.be | yt-dlp | `yt-dlp -o output URL` |
| Bilibili 视频 | bilibili.com | yt-dlp | `yt-dlp -o output URL` |
| 其他视频平台 | 各平台域名 | yt-dlp | `yt-dlp --list-formats URL` |
| 图片画廊 | imgur/pixiv/flickr 等 | gallery-dl | `gallery-dl -d /path URL` |
| 网页保存 | 任意网页 | agent-browser | 截图 + trafilatura 提取 |
| 网页转 PDF | 任意网页 | agent-browser | 打印为 PDF |

## 工作流程

### Step 1: 识别 URL 类型
```bash
# 获取 URL 的 Content-Type 和最终地址
curl -sIL "URL" 2>&1 | grep -iE "content-type|location|HTTP/" | tail -5
```

### Step 2: 根据类型下载

#### 普通文件下载（PDF/文档/压缩包等）
```bash
# 使用 aria2c 多线程下载（16 线程）
aria2c -x 16 -s 16 -d /root/.openclaw/workspace/files/downloads -o "filename" "URL"
```

#### 图片下载
```bash
# 单张图片
wget -O /root/.openclaw/workspace/files/images/photo.jpg "URL"

# 批量图片（从文件列表）
aria2c -x 16 -d /root/.openclaw/workspace/files/images -i urls.txt
```

#### 视频下载
```bash
# 查看可用格式
yt-dlp --list-formats "URL"

# 下载最佳质量（视频+音频合并，需要 ffmpeg）
yt-dlp -f "bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  -o "/root/.openclaw/workspace/files/videos/%(title)s.%(ext)s" \
  "URL"

# 仅下载音频（MP3）
yt-dlp -x --audio-format mp3 \
  -o "/root/.openclaw/workspace/files/audio/%(title)s.%(ext)s" \
  "URL"

# Bilibili 专用（带 cookie）
yt-dlp --cookies-from-browser chromium \
  -f "bestvideo+bestaudio/best" \
  -o "/root/.openclaw/workspace/files/videos/%(title)s.%(ext)s" \
  "URL"
```

#### 图片画廊批量下载
```bash
# Pixiv / Imgur / Flickr 等
gallery-dl -d /root/.openclaw/workspace/files/gallery "URL"

# 限制数量
gallery-dl --range 1-20 -d /root/.openclaw/workspace/files/gallery "URL"
```

#### 网页保存
```bash
# 方式 1: 截图保存
agent-browser open "URL"
agent-browser wait --load networkidle
agent-browser screenshot /root/.openclaw/workspace/files/screenshots/page.png --full-page

# 方式 2: 提取正文保存为 Markdown
python3.12 << 'PYEOF'
import trafilatura, httpx
r = httpx.get("URL", timeout=15, follow_redirects=True)
text = trafilatura.extract(r.text, output_format='txt', include_links=True)
with open('/root/.openclaw/workspace/files/articles/article.md', 'w') as f:
    f.write(text)
print(f"Saved: {len(text)} chars")
PYEOF
```

### Step 3: 验证下载结果
```bash
# 检查文件大小和类型
ls -lh /path/to/downloaded/file
file /path/to/downloaded/file
```

### Step 4: 通过钉钉发送给用户（如需要）
下载完成后，如果文件小于 20MB，可以直接通过钉钉发送给用户。
大文件建议提供下载链接或保存到指定位置。

## 下载目录结构
```
/root/.openclaw/workspace/files/
├── downloads/    # 普通文件
├── images/       # 图片
├── videos/       # 视频
├── audio/        # 音频
├── gallery/      # 图片画廊
├── articles/     # 网页文章
└── screenshots/  # 网页截图
```

## 环境说明
- Python: `python3.12`（conda 环境，路径 /root/anaconda3/bin/python）
- ffmpeg: 已安装（`/usr/local/bin/ffmpeg`），支持视频合并
- yt-dlp: 最新版 2026.03.03（`/usr/local/bin/yt-dlp`）
- gallery-dl: v1.31.9（`/usr/local/bin/gallery-dl`）
- aria2c: v1.35.0，支持 16 线程并行下载

## 注意事项
- 中国大陆无法访问 YouTube，但可访问 Bilibili
- 大文件下载优先使用 aria2c（多线程更快）
- 视频下载前先 `--list-formats` 确认可用格式
- 下载完成后告知用户文件位置和大小
