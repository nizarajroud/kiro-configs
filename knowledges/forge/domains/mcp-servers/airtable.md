---
name: airtable
description: Airtable database MCP — CRUD records, manage tables/fields, search, upload attachments.
---
# Airtable

- **Status**: installed
- **JSON key**: `airtable`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `npx -y @airtable/mcp-server`
- **Source**: https://github.com/airtable (official)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `list_bases` | List accessible bases |
| `list_tables` / `describe_table` | Table structure and fields |
| `list_records` / `get_record` | Read records |
| `create_record` / `update_records` / `delete_records` | CRUD |
| `search_records` | Full-text search |
| `create_table` / `create_field` | Schema management |
| `upload_attachment` | Upload files to attachment fields |
| `create_comment` / `list_comments` | Record comments |

## Auth

- `AIRTABLE_API_KEY` in environment

## Limitations

- Max 10 records per update_records call
- Upload limited to 5MB per file
- Rate limited (5 req/sec)
