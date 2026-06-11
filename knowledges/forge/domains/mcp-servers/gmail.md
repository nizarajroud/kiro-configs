---
name: gmail
description: Gmail and Google Calendar MCP — search/read emails, create drafts, reply, manage calendar events.
---
# Gmail (mcp-gsuite)

- **Status**: installed
- **JSON key**: `gmail`
- **Location**: settings/mcp.json
- **Wrapper**: `wrappers/gmail_wrapper.py`
- **Command**: `mcp-gsuite` (local venv at ~/.gmail-mcp/)
- **Source**: mcp-gsuite package (community)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `query_gmail_emails` | Search emails (Gmail query syntax) |
| `get_gmail_email` | Read full message by ID |
| `bulk_get_gmail_emails` | Read multiple messages |
| `create_gmail_draft` | Create a new draft |
| `reply_gmail_email` | Reply (send or draft) |
| `get_gmail_attachment` | Download attachment |
| `get_calendar_events` | List calendar events |
| `create_calendar_event` | Create event |
| `delete_calendar_event` | Delete event |
| `list_calendars` | List available calendars |

## Auth

- OAuth 2.0 (Client ID + Secret in `~/.gmail-mcp/.gauth.json`)
- Credentials stored in `~/.gmail-mcp/credentials/`
- Account: nizar.ajroud@gmail.com

## Limitations

- Wrapper patches schema bugs in mcp-gsuite
- Read-only for attachments (no upload to Gmail)
- Calendar limited to primary + listed calendars
