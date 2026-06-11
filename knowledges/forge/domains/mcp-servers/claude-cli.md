---
name: claude-cli
description: Claude CLI remote MCP — access Claude Code agent on PC Alithya.
---
# Claude CLI

- **Status**: disabled (PC Alithya éteint / remote indisponible)
- **JSON key**: `claude-cli`
- **Location**: agents/exp2.json
- **Wrapper**: `/home/nizar/.kiro/wrappers/claude_cli_wrapper.py`
- **Command**: `npx mcp-remote http://192.168.2.56:3108/mcp`
- **Source**: Custom remote setup
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| (Claude Code tools) | Code generation, analysis, debugging via Claude |

## Auth

- Remote server on PC Alithya (192.168.2.56:3108)

## Limitations

- Requires PC Alithya to be ON and server running
- Currently disabled
