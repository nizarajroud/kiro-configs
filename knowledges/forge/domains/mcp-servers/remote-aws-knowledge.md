---
name: remote-aws-knowledge
description: Remote AWS official documentation — search docs, read pages, check regional availability, get recommendations.
---
# Remote AWS Knowledge

- **Status**: installed
- **JSON key**: `remote.aws-knowledge`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `npx -y mcp-remote https://aws-mcp.us-east-1.api.aws/mcp`
- **Source**: Official AWS remote MCP
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `aws___search_documentation` | Search AWS docs by topic (reference, troubleshooting, CDK, etc.) |
| `aws___read_documentation` | Read full documentation pages |
| `aws___get_regional_availability` | Check service/API availability by region |
| `aws___list_regions` | List all AWS regions |
| `aws___recommend` | Get content recommendations for a doc page |
| `aws___retrieve_skill` | Load agent skills (domain expertise) |

## Auth

- None required (public remote MCP)

## Limitations

- Read-only (documentation only, no AWS API calls)
- URL allow-list restricted to docs.aws.amazon.com and related domains
- Max 10 regions per availability check
