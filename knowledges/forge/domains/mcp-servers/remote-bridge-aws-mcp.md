---
name: remote-bridge-aws-mcp
description: AWS MCP bridge (remote) — proxy to AWS official MCP endpoint for documentation and skills.
---
# Remote Bridge AWS MCP

- **Status**: installed
- **JSON key**: `remote.bridge.aws-mcp`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `uvx mcp-proxy-for-aws@latest https://aws-mcp.us-east-1.api.aws/mcp`
- **Source**: Official AWS remote MCP (via proxy)
- **Priority**: critical
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `aws___search_documentation` | Search AWS docs |
| `aws___read_documentation` | Read doc pages |
| `aws___get_regional_availability` | Check service availability by region |
| `aws___list_regions` | List AWS regions |
| `aws___recommend` | Get doc recommendations |
| `aws___retrieve_skill` | Load domain expertise skills |

## Auth

- None (public remote endpoint)
- Region metadata: us-east-1

## Limitations

- Duplicate of `remote.aws-knowledge` in mcp.json (same backend, different proxy)
- Aliased tools (aws_mcp_read_docs, etc.)
