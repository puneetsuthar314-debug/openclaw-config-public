# 工具使用指南

## 搜索工具

### 1. 阿里云 MCP web_search（首选）
通过阿里云 MCP 提供的 web_search 工具进行搜索。速度快，结果质量高。
- 直接调用 web_search 工具即可

### 2. enhanced_search.py（多源搜索）
支持多个搜索引擎的聚合搜索工具，位于 /usr/local/bin/enhanced_search.py。

**搜索模式：**

| 模式 | 说明 | 命令 |
|------|------|------|
| general | 通用搜索（默认） | `python3 /usr/local/bin/enhanced_search.py "关键词"` |
| news | 新闻搜索 | `python3 /usr/local/bin/enhanced_search.py "关键词" --mode news` |
| deep | 深度搜索+正文提取 | `python3 /usr/local/bin/enhanced_search.py "关键词" --mode deep` |
| academic | 学术论文搜索 | `python3 /usr/local/bin/enhanced_search.py "关键词" --mode academic` |

**搜索源：**

| 源 | 适用场景 |
|----|----------|
| bing | 英文/技术搜索（默认） |
| baidu | 中文搜索 |
| sogou | 中文搜索备选 |
| ddgs | DuckDuckGo 搜索 |
| all | 所有搜索源 |

**常用参数：**
- `--source bing/baidu/sogou/ddgs/all` 指定搜索源
- `--limit 10` 最大结果数
- `--output brief/full/json` 输出格式
- `--no-cache` 禁用缓存

### 3. image_search.py（图片搜索下载，极其重要）

**当用户要求搜索/发送图片时，必须使用此工具！**

位于 /usr/local/bin/image_search.py，支持从 Bing、百度、搜狗搜索并下载高质量图片。

**基本用法：**
```bash
python3 /usr/local/bin/image_search.py "搜索关键词 高清" --limit 3 --output /root/.openclaw/workspace/images --json
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 第一个参数 | 搜索关键词 | 必填 |
| `--limit N` | 下载图片数量 | 3 |
| `--output DIR` | 保存目录 | /tmp/image_search |
| `--min-size N` | 最小文件大小(字节) | 10240 |
| `--json` | JSON 格式输出 | 否 |

**核心特性：**
- 自动从 3 个搜索引擎搜索图片
- 自动验证每张图片（检查文件头魔数、格式、大小）
- 自动排除 404 错误页面、XML 错误文档等无效文件
- 只保存真正有效的图片

**绝对禁止：**
- ❌ 直接用 `curl` 或 `wget` 下载图片 URL（大量 URL 已失效，会下载到 HTML 错误页面）
- ❌ 发送未经 `file` 命令验证的图片文件
- ❌ 使用 enhanced_search.py --mode image（已废弃，用 image_search.py 替代）

### 4. web_fetch（网页内容获取）
获取指定 URL 的完整网页内容，用于深入阅读搜索结果。

### 5. aliyun_web_parser（网页解析）
阿里云 MCP 提供的网页解析工具。

### 6. aliyun_code_interpreter（代码执行）
阿里云 MCP 提供的代码解释器。

## 搜索决策流程

```
用户提问 → 判断是否需要搜索
  ├── 需要搜索 → 选择搜索工具
  │   ├── 快速搜索 → web_search (MCP)
  │   ├── 多源搜索 → enhanced_search.py
  │   ├── 新闻搜索 → enhanced_search.py --mode news
  │   ├── 学术搜索 → enhanced_search.py --mode academic
  │   ├── 图片搜索 → image_search.py（必须用这个！）
  │   └── 深入阅读 → web_fetch 获取全文
  └── 不需要搜索 → 直接回答
```

## 图片发送到钉钉的完整流程

```
1. python3 /usr/local/bin/image_search.py "关键词 高清" --limit 3 --output /root/.openclaw/workspace/images --json
2. file /root/.openclaw/workspace/images/img_1_xxxx.jpg  # 验证是真正的图片
3. [DING:IMAGE path="/root/.openclaw/workspace/images/img_1_xxxx.jpg"]  # 发送
```
