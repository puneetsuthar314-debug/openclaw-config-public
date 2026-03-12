---
name: super-search
description: "Multi-source intelligent search with caching, concurrent execution, deduplication, and content extraction. Supports: general search, news, academic papers, images, and deep research mode."
license: Apache-2.0
metadata:
  author: clawd-assistant
  version: "2.0"
---

# Super Search v2.0 — 多源智能搜索技能

## 概述
通过 `enhanced_search.py` 提供多搜索引擎并发搜索能力，支持 DuckDuckGo、百度、Bing、搜狗、Semantic Scholar，具备结果缓存、智能去重排名、批量网页正文提取功能。

## 前置条件
- Python 3.8+ (已安装)
- 依赖包: duckduckgo-search, httpx, trafilatura, beautifulsoup4, lxml (已安装)

## 搜索模式

### 1. 通用搜索（默认）
同时查询 DuckDuckGo + 百度 + Bing + 搜狗，结果去重排名。
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "搜索关键词" --output markdown
```

### 2. 新闻搜索
聚合百度新闻 + DuckDuckGo News + Bing News。
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "新闻关键词" --mode news --output markdown
```

### 3. 学术搜索
使用 Semantic Scholar API（免费，无需 API Key）。
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "学术主题" --mode scholar --output markdown
```

### 4. 深度研究模式
全引擎搜索 + 自动提取前 8 个结果的网页正文。
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "研究主题" --mode deep --output markdown
```

### 5. 图片搜索
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "图片关键词" --mode images --output json
```

## 高级选项

### 指定搜索源
```bash
# 仅百度
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --source baidu
# 仅 Bing
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --source bing
# 仅 DuckDuckGo
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --source ddg
# 仅搜狗
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --source sogou
```

### 提取网页正文
```bash
# 搜索 + 提取前 5 个结果的正文
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --extract --extract-count 5

# 控制每个网页提取的字符数
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --extract --extract-chars 8000
```

### 输出格式
```bash
# JSON 格式（默认，适合程序处理）
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --output json

# Markdown 格式（适合阅读）
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --output markdown

# 简洁格式（快速浏览）
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --output brief
```

### 保存结果
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --save /root/.openclaw/workspace/files/research/result.json
```

### 缓存控制
```bash
# 跳过缓存，强制重新搜索
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --no-cache
```

## 搜索策略建议

1. **日常查询:** 优先使用 OpenClaw 内置 `web_search`（Kimi 提供商），速度最快
2. **需要多源验证:** 使用 `enhanced_search.py` 的通用模式
3. **新闻时事:** 使用 `--mode news`
4. **学术论文:** 使用 `--mode scholar`
5. **深度调研:** 使用 `--mode deep`，自动提取正文
6. **查询优化:** 中文搜索同时附加英文关键词变体

## 注意事项
- 中国大陆服务器无法访问 Google，已优先配置百度/Bing/搜狗
- 搜索结果缓存 30 分钟，过期自动清理
- 并发搜索默认开启，最多 5 个引擎同时查询
- 结果自动去重（基于 URL + 标题相似度）
- 结果自动排名（基于摘要质量、时效性、引用数等）
