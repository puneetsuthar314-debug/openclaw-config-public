---
name: summarize
description: "Fast document and text summarization. Use when: user uploads a document and asks for a summary, user pastes long text and wants key points, user says 'summarize this', 'give me the gist', 'TL;DR', 'extract key points', or wants to quickly understand a long piece of content. Supports PDF, DOCX, TXT, Markdown, web pages, and pasted text."
---

# Document Summarizer

Generate concise, structured summaries from documents or text in seconds.

## Core Workflow

1. **Identify input type**: file upload, pasted text, or URL
2. **Extract content**: read the full document into context
3. **Analyze structure**: identify sections, headings, key arguments
4. **Generate summary**: produce output matching the requested depth

## Summary Levels

| Level | Trigger | Output |
|-------|---------|--------|
| **One-liner** | "one sentence summary" | Single sentence capturing the core message |
| **TL;DR** | "TL;DR", "gist", "quick summary" | 3-5 bullet points, ~100 words |
| **Executive Summary** | "summarize this", default | Structured paragraphs with key findings, 200-400 words |
| **Detailed Summary** | "detailed summary", "comprehensive" | Section-by-section breakdown, 500-1000 words |

## Input Handling

### Files
- **PDF**: Extract text with `pdftotext` or read via file tool
- **DOCX**: Read via file tool (text extraction)
- **Markdown/TXT**: Read directly
- **Spreadsheets**: Summarize structure, key columns, and data patterns

### Pasted Text
- Accept any length of pasted content
- For very long text (>10k words), summarize in chunks then synthesize

### URLs
- Navigate to URL, extract main content
- Ignore navigation, ads, and boilerplate

## Output Format

```markdown
## Summary

**Source**: [document name or "pasted text"]
**Length**: [original word count] -> [summary word count]
**Key Topics**: [topic1], [topic2], [topic3]

### Key Points

1. [Most important finding/argument]
2. [Second most important]
3. [Third most important]

### Details

[Structured paragraphs organized by theme or document section]

### Action Items (if applicable)

- [ ] [Action item 1]
- [ ] [Action item 2]
```

## Guidelines

- Preserve the author's intent and tone
- Highlight numbers, dates, and specific claims
- Flag any contradictions or notable omissions
- Use the document's own terminology
- For technical documents, keep domain-specific terms intact
- For multilingual documents, summarize in the document's primary language unless user specifies otherwise
- Always state the compression ratio (original vs summary length)
