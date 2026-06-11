---
name: telegram
description: Telegram messaging MCP (userbot via MTProto) — read/send messages, manage contacts, reactions, media, stories, groups.
---
# Telegram

- **Status**: installed
- **JSON key**: `telegram`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `npx -y telegram-mcp`
- **Source**: Community (telegram-mcp package)
- **Verdict**: adopted

## Tools (100+)

Key tools:
| Tool | Description |
|------|-------------|
| `telegramreadmessages` | Read chat history |
| `telegramsendmessage` | Send message |
| `telegramsearchmessages` | Search in a chat |
| `telegramsearchglobal` | Search across all chats |
| `telegramlistchats` | List chats with unread counts |
| `telegramgetunread` | Unread messages |
| `telegramgetcontacts` | Contacts list |
| `telegramgetprofile` | User profile info |
| `telegramdownloadmedia` | Download media from message |
| `telegramforwardmessage` | Forward messages |
| `telegramsendfile` | Send file |
| `telegramcreategroup` | Create group |
| `telegramsendstory` / `telegramgetstoryviews` | Stories |

## Auth

- QR code login (first time via `telegramlogin`)
- Session persisted locally

## Limitations

- Userbot (not bot API) — account can be restricted if abused
- Full MTProto access — powerful but be careful with write operations
- Session tied to one Telegram account
