---
name: task-planner
description: A unified skill for task planning, management, and scheduling. Use for breaking down complex projects, managing todo lists, and setting up recurring or scheduled tasks.
---

# Unified Task Planner

This skill provides a comprehensive system for planning complex tasks, managing simple todos, and scheduling automated jobs. It merges the concepts of file-based planning, task management, and cron job scheduling into a single, coherent workflow.

## Core Principles

- **Write to Disk**: Your filesystem is your persistent memory. Important plans, findings, and progress are always written to files.
- **Plan First**: Never start a complex task without a plan. For simple tasks, a quick checklist suffices.
- **Progressive Disclosure**: Start with a high-level plan. Elaborate on complex phases with dedicated sub-plans as needed.
- **Automate Repetition**: Use scheduled tasks (cron jobs) for recurring actions.

## File Structure

All planning and task files should be created within your project's working directory.

```
/home/ubuntu/your_project/
├── task_plan.md         # Main plan for the entire project.
├── findings.md          # Discoveries, research, and external content.
├── progress.md          # Detailed session logs and command outputs.
├── subplan_phase2.md    # (Optional) Detailed plan for a complex phase.
└── jobs.json            # (Optional) Configuration for scheduled tasks.
```

## Workflow: From Goal to Completion

### 1. Initial Planning

When a new task is assigned, first create a `task_plan.md`.

- **Copy Template**: Start from `/home/ubuntu/skills/task-planner/templates/task_plan.md`.
- **Define Goal**: State the final objective clearly.
- **Break Down Phases**: Decompose the goal into high-level steps or phases.
- **Identify Simple vs. Complex**: For each phase, decide if it's a simple checklist item or a complex sub-project.

### 2. Execution

- **Read Before Decide**: Before starting a phase, read `task_plan.md` to load the goal into your context.
- **Update After Act**: After completing a step, update its status in `task_plan.md` (`[ ]` -> `[x]`).
- **The 2-Action Rule**: After every two `view`/`browser`/`search` operations, **IMMEDIATELY** save key findings to `findings.md`. This prevents loss of multimodal information.
- **Log Everything**: Use `progress.md` to log detailed actions, command outputs, and test results. Log all errors to `task_plan.md` to avoid repeating mistakes.

### 3. Handling Complex Phases (Sub-plans)

If a phase is too complex for a simple checklist, create a dedicated sub-plan file (e.g., `subplan_implement_api.md`).

- Use the template from `/home/ubuntu/skills/task-planner/templates/sub_plan.md`.
- Treat this sub-plan just like the main plan: break it down, track progress, and mark it complete.
- The main `task_plan.md` should simply track the sub-plan's overall status: `- [ ] Phase 2: Implement API (see subplan_implement_api.md)`.

### 4. The 3-Strike Error Protocol

When you encounter an error, follow this protocol:

1.  **Attempt 1: Diagnose & Fix**: Understand the root cause and apply a targeted fix.
2.  **Attempt 2: Alternative Approach**: If the error persists, try a different tool, library, or method. **NEVER** repeat the exact same failing action.
3.  **Attempt 3: Broader Rethink**: Question your assumptions. Search for solutions. Consider updating the plan.

If you fail three times, escalate to the user with a summary of your attempts.

## ⏰ Scheduled & Recurring Tasks (Cron)

For tasks that need to run on a schedule, use the cron manager.

**Management:**

```bash
# List all scheduled jobs
python3 /home/ubuntu/skills/task-planner/scripts/cron-manager.py list

# Check and disable jobs that have reached their execution limit
python3 /home/ubuntu/skills/task-planner/scripts/cron-manager.py check

# Manually increment the run count for a job
python3 /home/ubuntu/skills/task-planner/scripts/cron-manager.py increment <task-id>
```

**Configuration (`jobs.json`):**

Use `/home/ubuntu/skills/task-planner/templates/jobs-template.json` as a reference. **Always set limits (`maxRuns` or `expireAt`) for temporary jobs** to prevent infinite loops or message spam.

```json
{
  "id": "daily-report-8am",
  "schedule": { "kind": "cron", "expr": "0 8 * * *" },
  "limits": { "maxRuns": 10 },
  "payload": { "kind": "agentTurn", "message": "Generate the daily sales report." }
}
```

## Scripts & Templates

- **Templates**
  - `/home/ubuntu/skills/task-planner/templates/task_plan.md`
  - `/home/ubuntu/skills/task-planner/templates/sub_plan.md`
  - `/home/ubuntu/skills/task-planner/templates/findings.md`
  - `/home/ubuntu/skills/task-planner/templates/progress.md`
  - `/home/ubuntu/skills/task-planner/templates/jobs-template.json`
- **Scripts**
  - `/home/ubuntu/skills/task-planner/scripts/cron-manager.py`
  - `/home/ubuntu/skills/task-planner/scripts/session-catchup.py`
