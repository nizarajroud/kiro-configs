---
name: aws-api-mcp-server
description: AWS API MCP Server (READ-ONLY) — executes AWS CLI commands for querying resources across all services.
---
# AWS API MCP Server

- **Status**: installed
- **JSON key**: `awslabs.aws-api-mcp-server`
- **Location**: agents/exp2.json
- **Wrapper**: `wrappers/aws_api_mcp_wrapper.py`
- **Command**: awslabs AWS API MCP server
- **Source**: https://github.com/awslabs/mcp (awslabs official)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `aws_api_call` | Execute any AWS CLI command (read-only) |

## Auth

- AWS SSO profile: `csna-operations-sso-828`
- Region: ca-central-1
- `READ_OPERATIONS_ONLY=true` enforced

## Limitations

- READ-ONLY — no create/update/delete operations allowed
- Catch-all for AWS services not covered by specialized MCP servers
- No local file access (`AWS_API_MCP_ALLOW_UNRESTRICTED_LOCAL_FILE_ACCESS=no-access`)
