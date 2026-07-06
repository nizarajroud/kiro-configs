---
name: git-mcp
description: Remote MCP server that converts any GitHub repo into an MCP endpoint via gitmcp.io. Use to fetch README, docs, and repo structure from any public GitHub repository as MCP context.
---
# GitMCP

- **Status**: installed
- **JSON key**: `git-mcp`
- **Agent**: exp2 only (`~/.kiro/agents/exp2.json`)
- **Type**: Remote (URL-based SSE, no local process)
- **Wrapper**: None needed
- **Dependencies**: None (free remote service)
- **API Key**: None required

## Configuration

```json
"git-mcp": {
  "url": "https://gitmcp.io/sse"
}
```

## What it does

GitMCP (https://github.com/idosal/git-mcp) is a free remote MCP server that:
- Converts any GitHub repository URL into an MCP-accessible endpoint
- Provides repository README, documentation, and structure as context
- Works via Server-Sent Events (SSE) protocol
- No local installation, no API keys, no dependencies

## Usage

The server exposes tools to fetch documentation and context from GitHub repos. Pass a GitHub repo URL and it returns the repo's docs as MCP-formatted context.

## References

- **Repo**: https://github.com/idosal/git-mcp (8,229+ stars)
- **Service**: https://gitmcp.io
- **Installed**: 2026-07-03
- **Verdict**: Adopted — zero-friction remote MCP, useful for pulling repo docs as context
