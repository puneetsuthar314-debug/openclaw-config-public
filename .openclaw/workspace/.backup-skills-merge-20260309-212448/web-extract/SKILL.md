---
name: web-extract
description: "Extract and save web page content in clean format. Supports articles, tables, data, and full page archival. Use when user wants to read, extract, summarize, or save content from a URL. Triggers: extract, read this page, 提取, 读取网页, 保存网页, 抓取内容, summarize URL, 总结这个链接"
allowed-tools: Bash, Computer, Write, Read
---

# Web Extract — 网页内容提取

## 核心能力
从任意 URL 提取干净的正文内容，去除广告、导航、侧边栏等噪音。

## 提取方式（按优先级）

### 方式 1: trafilatura（推荐，最快）
```bash
python3.12 << 'PYEOF'
import trafilatura, httpx, sys

url = "TARGET_URL"
r = httpx.get(url, timeout=15, follow_redirects=True, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

# 提取正文
text = trafilatura.extract(r.text, 
    include_links=True,
    include_tables=True,
    include_images=True,
    output_format='txt'
)

if text:
    # 保存到文件
    filename = url.split('/')[-1][:50] or 'article'
    path = f'/root/.openclaw/workspace/files/articles/{filename}.md'
    with open(path, 'w') as f:
        f.write(f'# Source: {url}\n\n{text}')
    print(f'Extracted {len(text)} chars -> {path}')
else:
    print('trafilatura failed, try agent-browser')
    sys.exit(1)
PYEOF
```

### 方式 2: agent-browser（动态页面/JS 渲染）
```bash
agent-browser open "TARGET_URL"
agent-browser wait --load networkidle
agent-browser snapshot
# 从 snapshot 输出中提取文本内容
```

### 方式 3: BeautifulSoup（自定义提取）
```bash
python3.12 << 'PYEOF'
import httpx
from bs4 import BeautifulSoup

url = "TARGET_URL"
r = httpx.get(url, timeout=15, follow_redirects=True)
soup = BeautifulSoup(r.text, 'lxml')

# 移除脚本和样式
for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
    tag.decompose()

# 提取正文
text = soup.get_text(separator='\n', strip=True)
print(text[:5000])
PYEOF
```

## 特殊场景

### 提取表格数据
```bash
python3.12 << 'PYEOF'
import pandas as pd
tables = pd.read_html("TARGET_URL")
for i, t in enumerate(tables):
    path = f'/root/.openclaw/workspace/files/data/table_{i}.csv'
    t.to_csv(path, index=False)
    print(f'Table {i}: {t.shape} -> {path}')
PYEOF
```

### 提取 PDF 内容
```bash
python3.12 << 'PYEOF'
import pdfplumber, httpx

# 下载 PDF
r = httpx.get("PDF_URL", timeout=30, follow_redirects=True)
with open('/tmp/doc.pdf', 'wb') as f:
    f.write(r.content)

# 提取文本
with pdfplumber.open('/tmp/doc.pdf') as pdf:
    text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
    path = '/root/.openclaw/workspace/files/articles/pdf_extract.md'
    with open(path, 'w') as f:
        f.write(text)
    print(f'Extracted {len(text)} chars from {len(pdf.pages)} pages')
PYEOF
```

## 环境说明
- Python: `python3.12`（/root/anaconda3/bin/python）
- 已安装: trafilatura, beautifulsoup4, lxml, httpx, pandas, pdfplumber
