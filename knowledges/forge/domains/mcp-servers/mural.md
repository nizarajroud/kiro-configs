---
name: mural
description: MURAL collaboration tool — visual boards, sticky notes, shapes, search, and widget management.
---
# MURAL

- **Status**: installed
- **JSON key**: `mural`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `python3 /home/nizar/HomeWspce/kiro-configs/wrappers/mural_wrapper.py`
- **Source**: Community wrapper
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `list_workspaces` | List accessible workspaces |
| `list_rooms` | List rooms in a workspace |
| `list_murals` | List murals in a room |
| `create_mural` | Create new mural |
| `get_mural_widgets` | Get all widgets from a mural |
| `create_sticky_note` | Add sticky note |
| `update_sticky_note` | Edit sticky text |
| `delete_widget` | Remove widget |
| `search_mural` | Search text in a mural |

## Auth

- MURAL API token in `.env`

## Limitations

- Default mural: PERSONAL (ID: f6a392091666d7eb480abe141fe326f5e6b96c54)
- Limited to sticky notes and basic shapes (no complex widgets)
- Case-insensitive search
