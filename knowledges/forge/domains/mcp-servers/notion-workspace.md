---
name: notion-workspace
description: Notion workspace MCP — search pages, query databases, create/update pages and blocks.
---
# Notion Workspace

- **Status**: installed
- **JSON key**: `notion-workspace`
- **Location**: settings/mcp.json
- **Wrapper**: none (local fork)
- **Command**: `python3 /home/nizar/HomeWspce/notion-mcp-server/src/notionmcp/server.py`
- **Source**: Local fork with extended block types (headings, annotations, image support)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `APIpostsearch` | Search pages/databases by title |
| `APIretrieveapage` | Get page properties |
| `APIgetblockchildren` | Read page content (blocks) |
| `APIpatchblockchildren` | Append content to a page |
| `APIpostpage` | Create a new page |
| `APIpatchpage` | Update page properties |
| `APIquerydatasource` | Query a database with filters/sorts |
| `APIcreateacomment` | Add comments to pages |
| `upload_image` | Upload image to page via GitHub |
| `download_notion_image` | Download image from Notion block |

## Auth

- `NOTION_API_KEY` in environment (integration token)

## Limitations

- Cannot upload files directly (images go via GitHub raw URL workaround)
- Rate limited by Notion API (3 req/sec)
- Search is title-based, not full-text content search
