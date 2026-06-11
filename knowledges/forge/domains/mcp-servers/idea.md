---
name: idea
description: Product Owner prompt server — @idea/idea (auto-detect repo) and @idea/backlog (IDEAS project).
---
# Idea (Product Owner)

- **Status**: disabled (remote on PC Alithya)
- **JSON key**: `idea`
- **Location**: agents/exp2.json
- **Wrapper**: `/home/nizar/.kiro/wrappers/idea_prompt_wrapper.py`
- **Command**: `npx mcp-remote http://192.168.2.56:3208/mcp`
- **Source**: Custom local server
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| `@idea/idea` | Auto-detect repo or fallback IDEAS |
| `@idea/backlog` | Always targets IDEAS project |

## Auth

- Remote server on PC Alithya

## Limitations

- Currently disabled (remote unavailable)
