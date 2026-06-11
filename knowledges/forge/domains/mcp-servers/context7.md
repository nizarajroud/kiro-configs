---
name: context7
description: Live documentation lookup for any library, SDK, or framework. Fetches real-time docs from source.
---
# Context7

- **Status**: installed
- **JSON key**: `context7`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `npx -y @upstash/context7-mcp`
- **Source**: https://github.com/upstash/context7 (official Upstash)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `resolve-library-id` | Find the Context7 ID for a library |
| `get-library-docs` | Fetch live documentation for a library |

## Auth

- None required (public API)

## Limitations

- Timeout: 200s configured
- Not all libraries indexed — popular ones only
- Use to verify API signatures before writing code
