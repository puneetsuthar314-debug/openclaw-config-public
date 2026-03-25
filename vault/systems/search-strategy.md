# 搜索策略

## 搜索工具

**唯一搜索工具：unified-search 技能（enhanced_search.py）**

```bash
# 基础用法
python3 /usr/local/bin/enhanced_search.py "关键词" --output markdown

# 常用模式
--mode news      # 新闻搜索
--mode deep      # 深度搜索（自动提取网页正文）
--mode scholar   # 学术搜索
--mode images    # 图片搜索

# 高级选项
--extract-count 5   # 提取前5个结果的正文
--source baidu      # 指定搜索引擎（baidu/bing/ddg/sogou）
--limit 10          # 每个引擎的结果数
--no-cache          # 跳过缓存
```

**已弃用**：MCP web_search（API 不可用）、super-search、wide-search

## 搜索分级

| 级别 | 场景 | 方法 |
|------|------|------|
| L1 快速查询 | 事实确认、简单问题 | `enhanced_search.py "关键词" --output markdown` |
| L2 标准搜索 | 需要对比多个来源 | `enhanced_search.py "关键词" --mode deep --extract-count 5 --output markdown` |
| L3 深度研究 | 综合报告、技术调研 | 多轮 enhanced_search.py + agent-browser 深度阅读 + 结构化报告 |

## 搜索触发规则

以下场景自动触发搜索，无需用户额外说明：
- **时间相关**：今天、最新、最近、现在、当前、2024-2026
- **数据相关**：价格、股价、天气、汇率、统计
- **新闻相关**：新闻、动态、消息、事件、进展
- **验证相关**：是真的吗、确认、验证、核实

搜索后不要只依赖摘要（snippet），应使用 `--extract` 或 `fetch` 深入阅读 2-3 篇重要文章。

## 内容提取备选链

当 enhanced_search.py 的 `--extract` 提取不够时：
1. `fetch` 工具直接抓取已知 URL
2. `agent-browser` 浏览器自动化（最可靠，绕过反爬虫）
3. `aliyun_web_parser`（MCP 工具，备选）
