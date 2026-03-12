---
name: unified-search
description: "Provides a 3-level unified search capability. Use for all search and research tasks. L1 for quick queries, L2 for in-depth investigation with content extraction, and L3 for autonomous, multi-step research report generation."
---

# Unified Search Skill

This skill provides a comprehensive, three-level framework for search and research tasks, from quick lookups to autonomous, in-depth report generation.

## Trigger Conditions

Use this skill for any user request involving "search", "find", "research", "look up", "what is", "compare", or any other information-gathering query.

## Core Workflow: Choose the Right Level

Based on the user's request, select the appropriate search level:

| Level | Name | Best For | Speed & Cost |
|---|---|---|---|
| **L1** | Quick Search | Fact-checking, definitions, simple questions. | **Fastest**, Free |
| **L2** | Deep Search | Deeper questions, requires content from multiple pages, comparisons. | **Moderate**, Mostly Free |
| **L3** | Broad Research | Complex topics, market analysis, literature reviews, report generation. | **Slowest**, Can be Costly |

---

## L1: Quick Search

For fast, immediate answers. Prioritize using the built-in `search` tool first, then escalate to the script if needed.

### 1. Standard Tool Search (Primary)

Use the `search` tool for the fastest results.

```python
# For general info
default_api.search(type='info', queries=['query'])

# For news
default_api.search(type='news', queries=['query'])
```

### 2. Enhanced Script Search (Secondary)

If the built-in tool is insufficient, use the `enhanced_search.py` script for multi-source results.

```bash
# General purpose search across multiple engines
python3 /usr/local/bin/enhanced_search.py "search query" --output markdown
```

---

## L2: Deep Search

For when you need to go beyond search result snippets and analyze the content of the source pages. This level has two tiers: a free content extraction method and a powerful, paid AI-based method.

### Tier 1: Multi-Source Extraction (Free)

Use `enhanced_search.py` with the `--mode deep` or `--extract` flag to automatically fetch and read the content of top search results.

```bash
# Search and automatically extract text from the top 5 results
python3 /usr/local/bin/enhanced_search.py "research topic" --mode deep --extract-count 5 --output markdown

# Extract more characters if needed (default is limited)
python3 /usr/local/bin/enhanced_search.py "detailed topic" --extract --extract-chars 8000
```

### Tier 2: Gemini Deep Research (Paid)

For complex queries requiring deep analysis and synthesis. **Inform the user of the cost ($2-5) and time (2-10 min) before using.** Requires `GEMINI_API_KEY`.

```bash
# Start a deep research task
python3 /home/ubuntu/skills/deep-research/scripts/research.py --query "Analyze the impact of AI on software development"

# Provide a desired structure for the output
python3 /home/ubuntu/skills/deep-research/scripts/research.py --query "Compare Python web frameworks" --format "1. Executive Summary\n2. Comparison Table\n3. Recommendations"

# Check status while running
python3 /home/ubuntu/skills/deep-research/scripts/research.py --status <interaction_id>
```

---

## L3: Broad Research (Autonomous Workflow)

For large, complex research tasks that require a structured, multi-step approach similar to a human researcher. This is not a single command but a **methodology** you must follow.

### 1. Plan

- Create a research plan in a markdown file (`research_plan.md`).
- Decompose the main topic into 3-5 key sub-questions.
- Identify diverse source types to consult (docs, blogs, papers, news).

### 2. Execute (Iterative Search)

- For each sub-question, perform iterative L1/L2 searches.
- **Round 1:** Broad search (`[topic] overview`).
- **Round 2:** Specific search (`[topic] [technical detail]`).
- **Round 3:** Comparative search (`[topic] vs [alternative]`).
- Use the `browser` tool to read full articles. Save key findings, quotes, and data to a notes file (`research_notes.md`). **Always cite your sources with URLs.**

### 3. Synthesize & Report

- Review `research_notes.md` to identify patterns, contradictions, and key insights.
- Structure the findings into a coherent narrative.
- Write a final, comprehensive report (`research_report.md`) with an executive summary, detailed sections for each sub-question, and a full list of references.

---

## Appendix: `enhanced_search.py` Advanced Options

- **Specify Search Mode:**
  - `--mode news`: News articles.
  - `--mode scholar`: Academic papers via Semantic Scholar.
  - `--mode images`: Get image results.

- **Specify Search Source:**
  - `--source baidu`: Use Baidu.
  - `--source bing`: Use Bing.
  - `--source ddg`: Use DuckDuckGo.

- **Control Output:**
  - `--output json`: For programmatic use.
  - `--output brief`: For a quick list of titles and links.
  - `--save /path/to/file.json`: Save results to a file.

- **Cache Control:**
  - `--no-cache`: Force a fresh search, ignoring the 30-minute cache.
