---
name: unified-search
description: Multi-level search skill with enhanced news aggregation (v4.0). Supports general web search, news aggregation from 9+ Chinese sources, academic search, deep content extraction, and broad research workflows.
version: 4.0.0
---

# Unified Search Skill v4.0

A multi-level search framework for OpenClaw. Choose the right level based on the task complexity.

## Key Improvements in v4.0
- **9 news engines** in parallel: Baidu News, Bing News, Sogou News, DuckDuckGo News, Toutiao Hot, IT之家 RSS, 澎湃新闻 API, 新浪新闻 API, 360 News
- **Smart Chinese tokenization** via jieba for accurate keyword matching
- **Time-weighted ranking** for news (newer = higher score)
- **Source credibility weighting** for news results
- **28+ results** per news search (up from 4)

---

## News Search Best Practices (IMPORTANT)

When user asks for news, current events, or "最新" anything:

### 1. ALWAYS use `--mode news` for news queries
```bash
# CORRECT - uses all 9 news engines
python3 /usr/local/bin/enhanced_search.py "AI人工智能" --mode news --output markdown

# WRONG - only uses general search engines, misses news sources
python3 /usr/local/bin/enhanced_search.py "AI人工智能最新新闻" --output markdown
```

### 2. Keep queries SHORT and FOCUSED
```bash
# GOOD - jieba splits "科技新闻" into "科技" + "新闻", matches broadly
python3 /usr/local/bin/enhanced_search.py "科技新闻" --mode news --output markdown

# GOOD - specific topic
python3 /usr/local/bin/enhanced_search.py "AI芯片" --mode news --output markdown

# BAD - too long, reduces matches
python3 /usr/local/bin/enhanced_search.py "2026年最新人工智能科技新闻动态" --mode news --output markdown
```

### 3. For comprehensive news coverage, run MULTIPLE searches
```bash
# Search 1: Main topic
python3 /usr/local/bin/enhanced_search.py "科技" --mode news --output markdown --save /tmp/news1.json

# Search 2: Specific subtopic
python3 /usr/local/bin/enhanced_search.py "AI" --mode news --output markdown --save /tmp/news2.json

# Search 3: Another angle
python3 /usr/local/bin/enhanced_search.py "芯片半导体" --mode news --output markdown --save /tmp/news3.json
```

### 4. Use `--no-cache` for breaking news
```bash
# Force fresh results, bypass 10-minute news cache
python3 /usr/local/bin/enhanced_search.py "突发事件" --mode news --no-cache --output markdown
```

---

## Reliable Chinese News Sources

For direct browsing (when search is insufficient):

**API-based (most reliable):**
1. IT之家 RSS — `https://www.ithome.com/rss/` (60+ tech articles)
2. 澎湃新闻 API — hot news via API (20 items)
3. 新浪新闻 API — rolling news by category (20 items)
4. 头条热榜 API — trending topics (50 items)

**Search-based:**
5. 百度资讯 — `https://www.baidu.com/s?wd=QUERY&tn=news&cl=2`
6. Bing 新闻 — `https://cn.bing.com/news/search?q=QUERY`
7. 360 新闻 — `https://news.so.com/ns?q=QUERY`

**Use `agent-browser` for these (anti-bot protected):**
8. `https://36kr.com` — 36氪
9. `https://news.qq.com/ch/tech` — 腾讯科技

**Avoid these (network issues from China servers):**
- `https://news.ycombinator.com` — Hacker News (blocked)
- `https://news.google.com` — Google News (blocked)
- `https://rsshub.app` — RSSHub (blocked)

---

## L1: Quick Search

For fast, immediate answers.

### 1. Standard Tool Search (Primary)
```python
# For general info
default_api.search(type='info', queries=['query'])
# For news
default_api.search(type='news', queries=['query'])
```

### 2. Enhanced Script Search (Secondary)
```bash
# General search across multiple engines (Baidu, Bing, Sogou, 360, DuckDuckGo, Zhihu, Weibo)
python3 /usr/local/bin/enhanced_search.py "search query" --output markdown

# NEWS search across 9 news engines (ALWAYS use --mode news for news!)
python3 /usr/local/bin/enhanced_search.py "topic" --mode news --output markdown

# Academic search
python3 /usr/local/bin/enhanced_search.py "research topic" --mode scholar --output markdown
```

---

## L2: Deep Search

For analyzing content beyond search snippets.

### Tier 1: Multi-Source Extraction (Free)
```bash
# Search and extract text from top 5 results
python3 /usr/local/bin/enhanced_search.py "research topic" --mode deep --extract-count 5 --output markdown

# Extract more characters per page
python3 /usr/local/bin/enhanced_search.py "detailed topic" --extract --extract-chars 8000
```

### Tier 1.5: Browser-Based Extraction (Free, bypasses anti-bot)
```bash
agent-browser open "https://target-site.com/article" && agent-browser wait --load networkidle
agent-browser get text 'article'
agent-browser screenshot /tmp/article.png
```

### Tier 2: Gemini Deep Research (Paid)
**Inform the user of the cost ($2-5) and time (2-10 min) before using.**
```bash
python3 /home/ubuntu/skills/deep-research/scripts/research.py --query "Analyze the impact of AI on software development"
```

---

## L3: Broad Research (Autonomous Workflow)

For large, complex research tasks.

### 1. Plan
- Create `research_plan.md` with 3-5 key sub-questions
- Identify diverse source types

### 2. Execute (Iterative Search)
- Round 1: Broad search (`[topic] overview`)
- Round 2: Specific search (`[topic] [technical detail]`)
- Round 3: Comparative search (`[topic] vs [alternative]`)
- Save findings to `research_notes.md` with URLs

### 3. Synthesize & Report
- Write `research_report.md` with executive summary, sections, and references

---

## Appendix: `enhanced_search.py` v4.0 Full Options

| Option | Description | Example |
|--------|-------------|---------|
| `--mode` | Search mode: `general`, `news`, `scholar`, `images`, `deep` | `--mode news` |
| `--source` | Specific engine: `all`, `baidu`, `bing`, `ddg`, `sogou`, `360`, `zhihu`, `weibo`, `scholar`, `arxiv`, `baidu-news`, `toutiao`, `ithome`, `thepaper`, `sina` | `--source ithome` |
| `--output` | Output format: `json`, `markdown`, `brief` | `--output markdown` |
| `--limit` | Results per engine (default: 10 general, 15 news) | `--limit 20` |
| `--extract` | Extract webpage content from results | `--extract` |
| `--extract-count` | Number of pages to extract (default: 5) | `--extract-count 8` |
| `--extract-chars` | Max chars per page (default: 5000) | `--extract-chars 8000` |
| `--no-cache` | Skip cache (30min general, 10min news) | `--no-cache` |
| `--save` | Save results to file | `--save /tmp/results.json` |

### News Mode Engines (9 total)
| Engine | Source | Type | Typical Results |
|--------|--------|------|-----------------|
| Baidu News | 百度资讯 | Search | 4-10 |
| Bing News | cn.bing.com | Search | 0-5 |
| Sogou News | 搜狗新闻 | Search | 2-5 |
| DuckDuckGo News | DDG | Search | 0-10 |
| Toutiao Hot | 头条热榜 | API | 0-50 (filtered) |
| IT之家 RSS | ithome.com | RSS | 5-20 (filtered) |
| 澎湃新闻 | thepaper.cn | API | 0-20 (filtered) |
| 新浪新闻 | sina.com.cn | API | 5-20 (filtered) |
| 360 News | news.so.com | Search | 0-5 |
