---
name: bookmarks
description: Chrome & Edge bookmarks — search and browse bookmarks across browsers.
---
# Bookmarks

- **Status**: installed
- **JSON key**: `bookmarks` (in agents, not mcp.json — loaded via wrapper)
- **Location**: settings/mcp.json
- **Wrapper**: `wrappers/bookmarks_wrapper.py`
- **Command**: `python3 wrappers/bookmarks_wrapper.py`
- **Source**: Custom local server
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `search_bookmarks` | Search by keyword in title, URL, or folder |
| `get_bookmarks_in_folder` | List bookmarks in a folder (partial match) |
| `list_bookmark_folders` | List all folders |
| `bookmark_stats` | Count per browser, top folders |

## Auth

- None (reads local browser bookmark files)

## Limitations

- 7,260 Chrome + 2,454 Edge bookmarks indexed
- Read-only (cannot add/delete bookmarks)
- Searches both browsers by default
