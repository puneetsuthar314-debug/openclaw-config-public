# quick-search 快速搜索技能

## 描述
一键快速搜索，自动选择最佳搜索引擎和模式。

## 触发条件
当用户说"搜索"、"查找"、"搜一下"、"帮我查"时自动触发。

## 使用方法

### 快速搜索
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词"
```

### 中文搜索
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "中文关键词" --source baidu
```

### 新闻搜索
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --mode news
```

### 深度搜索（搜索+正文提取）
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --mode deep
```

### 学术搜索
```bash
/root/anaconda3/bin/python3 /usr/local/bin/enhanced_search.py "关键词" --mode academic
```

## 搜索流程
1. 先用 web_search (MCP) 快速获取结果
2. 如果结果不够，用 enhanced_search.py 多源搜索
3. 对感兴趣的结果用 web_fetch 获取全文
4. 综合分析后给出答案
