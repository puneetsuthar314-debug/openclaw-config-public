---
name: task-manager
description: Manage tasks and todos with priorities, deadlines, and progress tracking. Use when user needs to track tasks, manage todos, or organize checklists.
---

# Task Manager

Simple task management with file-based persistence.

## When to Use

- User wants to track tasks or todos
- User needs to manage deadlines
- User wants to organize a checklist
- User needs to prioritize work

## File Location

Tasks are stored in: `/root/.openclaw/workspace/tasks.md`

## Task Format

```markdown
# Task List

## Todo
- [ ] Task name (Priority: High/Medium/Low, Due: YYYY-MM-DD)

## In Progress
- [ ] Task name (Priority: High/Medium/Low, Due: YYYY-MM-DD)

## Done
- [x] Task name (Completed: YYYY-MM-DD)
```

## Commands

| Command | Action |
|---------|--------|
| Add task | Add to Todo section |
| Start task | Move from Todo to In Progress |
| Complete task | Move from In Progress to Done |
| List tasks | Show all tasks by status |
| Delete task | Remove from file |

## Usage Examples

```
用户：帮我记个任务，明天交数据库作业
→ 添加到 Todo: 数据库作业 (Priority: High, Due: 2026-03-09)

用户：我开始做数据库作业了
→ 移动到 In Progress

用户：数据库作业做完了
→ 移动到 Done，记录完成时间
```

## Priority Levels

- **High** - Urgent and important, do first
- **Medium** - Important but not urgent
- **Low** - Nice to have, do when time permits

## Best Practices

1. Review tasks daily
2. Move tasks between statuses promptly
3. Add due dates for time-sensitive tasks
4. Use priorities to focus on what matters
5. Archive done tasks monthly
