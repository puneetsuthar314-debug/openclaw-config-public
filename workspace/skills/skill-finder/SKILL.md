---
name: skill-finder
description: Discovers and recommends Agent Skills from the open skills ecosystem and verified GitHub repositories. Use when users ask to find, discover, search for, or recommend skills/plugins for specific tasks, domains, or workflows.
---

# Skill Finder

This skill helps you discover and install skills from the open agent skills ecosystem and a curated list of verified GitHub repositories.

## Workflow

Follow this two-step process to find the best skill for the user's needs.

### Step 1: Quick Search (Ecosystem-wide)

First, perform a quick search across the entire open agent skills ecosystem using the `skills` CLI. This is the fastest way to find a registered skill.

```bash
npx skills find "[query]"
```

**Examples:**
- User asks "how do I make my React app faster?" → `npx skills find "react performance"`
- User asks "can you help me with PR reviews?" → `npx skills find "pr review"`

If you find a relevant skill, present it to the user and offer to install it with `npx skills add <package> -g -y`.

### Step 2: Extended Search (Verified Repositories)

If the quick search yields no results or the user wants more options, perform an extended search across a list of verified, high-quality GitHub repositories. This search is more targeted and can uncover skills that are not yet in the main registry.

*This functionality is currently under development and will be available in a future update.*

### Step 3: Presenting Results

When presenting skills found by the extended search, format them clearly:

```markdown
### [Skill Name]
**Source**: [Repository] | ⭐ [Stars]
**Description**: [From SKILL.md]
👉 **[Import](import_url)**
```

### What to Do If No Skills Are Found

If neither search method finds a relevant skill:

1.  Acknowledge that no existing skill was found for their specific request.
2.  Offer to help with the task directly using your general capabilities.
3.  Suggest that the user could create their own skill for this task using the `skill-creator` skill.

## Verified Sources for Extended Search

The extended search script pulls from the following curated repositories:

- anthropics/skills
- obra/superpowers
- vercel-labs/agent-skills
- K-Dense-AI/claude-scientific-skills
- ComposioHQ/awesome-claude-skills
- travisvn/awesome-claude-skills
- BehiSecc/awesome-claude-skills
