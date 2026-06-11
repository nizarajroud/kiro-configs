---
name: ticktick
description: TickTick task management — tasks, projects, habits, tags, focus stats, kanban, batch operations.
---
# TickTick

- **Status**: installed
- **JSON key**: `ticktick`
- **Location**: settings/mcp.json
- **Wrapper**: `wrappers/ticktick_wrapper.py`
- **Command**: `uvx ticktick-mcp`
- **Source**: Community (ticktick-mcp package)
- **Verdict**: adopted

## Tools (50+)

Key tools:
| Tool | Description |
|------|-------------|
| `create_task` / `update_task` / `complete_task` | Task CRUD |
| `query_tasks` / `tasks_of_today` / `overdue_tasks` | Query & filter |
| `list_projects` / `create_project` | Project management |
| `list_habits` / `habit_checkin` | Habit tracking |
| `list_tags` / `create_tag` | Tag management |
| `batch_create_tasks` / `batch_update_tasks` | Batch operations |
| `get_productivity_stats` | Score, streaks, completions |
| `week_overview` / `upcoming_tasks` | Planning views |

## Auth

- V1: OAuth token (via wrapper)
- V2: Session token for advanced features (batch, habits, sync)
- Both stored in `.env`

## Limitations

- V1 creation endpoint silently ignores `parentId` — must use `set_subtask_parent` after
- V2 batch cannot reliably set reminders — use V1 `update_task` instead
- `groupId` assignment requires V2 workaround
- See `ticktick_guide()` for full operating contract
