---
name: agent-learning
description: "Enables the agent to learn from experience by capturing errors, user corrections, and session summaries. It supports self-reflection before delivering work, logs learnings for continuous improvement, and summarizes conversations for future reference. Use when the agent fails, gets corrected, or when a session needs to be logged."
---

# Agent Learning Skill

This skill provides a unified framework for agent self-improvement, reflection, and session logging. It allows the agent to capture learnings from interactions, analyze its own work for quality, detect recurring patterns of error, and maintain a structured log of its activities.

## When to Use

- **Error or Failure**: When a command, tool, or operation fails.
- **User Correction**: When the user corrects the agent's output or reasoning (e.g., "No, that's wrong...", "Actually...").
- **Pre-Delivery Check**: Before submitting significant deliverables like code, reports, or strategic plans.
- **Session Summary**: When the user requests to log or summarize the current conversation.
- **Discovering Inefficiency**: When a better approach for a recurring task is identified.

## Core Workflows

This skill integrates three primary workflows:

1.  **Structured Logging**: Capturing events (errors, learnings, feedback) into structured markdown files.
2.  **Reflection & Analysis**: Proactively reviewing work for quality and analyzing past mistakes to find root causes.
3.  **Session Summarization**: Condensing conversations into a weekly log for review.

```
         ┌──────────────────────────────────────────────┐
         │               AGENT LEARNING LOOP            │
         └──────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐
  │ EVENT OCCURS │    │ PRE-DELIVERY     │    │ USER REQUESTS │
  │(Error, Fix)  │    │ CHECK            │    │ LOG           │
  └──────┬───────┘    └────────┬─────────┘    └───────┬───────┘
         │                     │                      │
         ▼                     ▼                      ▼
  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐
  │ 1. LOG EVENT │    │ 2. REFLECT       │    │ 3. SUMMARIZE  │
  │  (Structured)│    │   (7 Dimensions) │    │    SESSION    │
  └──────┬───────┘    └──────────────────┘    └───────┬───────┘
         │                                            │
         └───────────────────┬────────────────────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │   PERIODIC REVIEW  │
                  │ (Detect Patterns & │
                  │  Promote Lessons)  │
                  └────────────────────┘
```

## 1. Structured Logging

All learnings, errors, and feature requests are logged in the `~/.learnings/` directory. This provides a persistent, machine-readable knowledge base.

### Directory Structure

```
~/.learnings/
├── LEARNINGS.md        # User corrections, knowledge gaps, best practices
├── ERRORS.md           # Command failures, tool errors, exceptions
├── PATTERNS.md         # Detected recurring issues and prevention rules
└── FEATURE_REQUESTS.md # User-requested capabilities
```

### How to Log

When an event occurs, append a new entry to the appropriate file. Use a unique ID for each entry.

**ID Format**: `TYPE-YYYYMMDD-XXX` (e.g., `LRN-20260309-001`, `ERR-20260309-A4C`)

#### Learning Entry (`LEARNINGS.md`)

Use for user corrections or new insights.

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted

### Summary
One-line description of what was learned.

### Details
Full context: what happened, what was wrong, what's correct.

### Suggested Action
Specific fix or improvement to make.

### Metadata
- Source: user_feedback | self_discovery
- Related Files: path/to/file.ext
---
```

#### Error Entry (`ERRORS.md`)

Use for command or tool failures.

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending | resolved

### Summary
Brief description of what failed.

### Error
```
Actual error message or output
```

### Context
- Command/operation attempted
- Input or parameters used

### Suggested Fix
If identifiable, what might resolve this.
---
```

## 2. Reflection & Analysis

Proactive quality assurance and reactive root cause analysis are key to improvement.

### Pre-Delivery Reflection (7-Dimension Evaluation)

Before sending important work, perform a quick (30-second) scan. If any dimension scores below 7/10, fix it first.

| # | Dimension    | Question                                |
|---|--------------|-----------------------------------------|
| 1 | Correctness  | Does it solve the stated problem?       |
| 2 | Completeness | Are edge cases covered? Assumptions stated? |
| 3 | Clarity      | Is it immediately understandable?       |
| 4 | Robustness   | What could break this?                  |
| 5 | Efficiency   | Is there unnecessary complexity?        |
| 6 | Alignment    | Is this what the user actually wants?   |
| 7 | Pride        | Would I sign my name on this?           |

### Pattern Detection & Promotion

Periodically review `LEARNINGS.md` and `ERRORS.md` to find recurring issues.

- **3+ similar entries**: This is a pattern. Create a pattern entry.
- **Broadly applicable lesson**: Promote the learning to a core agent document (e.g., `AGENTS.md`, `TOOLS.md`) for permanent reference.

#### Pattern Entry (`PATTERNS.md`)

```markdown
## [Pattern Name]
category: technical | communication | process
frequency: 4 occurrences
status: active | monitoring | resolved

**Pattern:** A description of what keeps happening.
**Root Cause:** A deep analysis of why this pattern exists (use the "5 Whys" technique).
**Prevention Rule:** A clear, actionable rule to break the pattern.
**Last seen:** YYYY-MM-DD
```

### Injecting Lessons

Before starting a new task, check `PATTERNS.md` for relevant active patterns. If one exists, surface it.

> "Before we proceed, I have a lesson from past work on [topic]: [prevention rule]. I will apply it here."

## 3. Session Summarization

When requested, summarize the current conversation and append it to a weekly log file.

### Workflow

1.  **Determine File**: Get the ISO week (`date +%Y-w%V`) to find the target file: `YYYY-wWW-agent-log.md`.
2.  **Review Conversation**: Identify distinct topics, decisions, and outputs.
3.  **Format Entry**: For each day, create a `## YYYY-MM-DD` heading. List topics as bullets.
4.  **Append to Log**: Add the new content to the weekly log file in reverse chronological order (newest day on top).

### Formatting Rules

- **One `##` heading per day**: `## YYYY-MM-DD`.
- **Topics as bullets**: Use `- Topic title`.
- **Details as nested bullets**: Indent with a tab.
- **No meta-commentary**: Do not add intros like "In this session...".

#### Example (`2026-w09-agent-log.md`)

```markdown
## 2026-03-09

- Merged three skills into the new agent-learning skill
  - Analyzed reflection, self-improving-agent, and session-log skills.
  - Created a unified workflow combining structured logging, reflection, and summarization.
  - Generated the new SKILL.md file.
```
