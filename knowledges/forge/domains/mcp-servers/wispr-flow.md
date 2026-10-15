---
name: wispr-flow
description: Wispr Flow Notetaker MCP (remote, OAuth) — access meeting notes and transcripts captured by Wispr Flow Notetaker. Query/summarize/search recorded meetings. Does NOT access dictations.
---
# Wispr Flow (wispr-flow)

- **Status**: installed (requires one-time OAuth browser approval)
- **JSON key**: `wispr-flow` (in `settings/mcp.json`, global — all agents)
- **Type**: remote HTTP MCP via `mcp-remote` bridge
- **URL**: `https://api.wisprflow.ai/connect/mcp`
- **Wrapper**: none (OAuth, no API key)
- **Auth**: OAuth in browser (first run opens an approval page; token cached by `mcp-remote` in `~/.mcp-auth/`)
- **Placement**: cross-cutting (global `settings/mcp.json`) + explicit blocks on it-supervisor/forge/light; compass/exp2 inherit via `useLegacyMcpJson`
- **Scope**: meeting notes + transcripts from Wispr Flow Notetaker. **Does NOT access dictations.**
- **Verdict**: ADOPTED — official Wispr Flow connector for querying recorded meetings.

## Config

```json
"wispr-flow": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://api.wisprflow.ai/connect/mcp"],
  "disabled": false
}
```

## Setup (one-time)

1. Config added (done).
2. On first use, `mcp-remote` opens a browser page to approve access to your Notetaker data.
3. After approval, the token is cached — subsequent sessions connect automatically.

## Notes

- Official source: Wispr Flow app → Settings → MCP (connection URL + custom connector instructions).
- Complementary to `youtube-search` / `video-transcriber-mcp`: those handle YouTube/video; this handles YOUR recorded meetings.
- If auth expires, delete the cached token under `~/.mcp-auth/` and re-approve.
