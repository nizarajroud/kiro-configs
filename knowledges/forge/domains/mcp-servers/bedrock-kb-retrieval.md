---
name: bedrock-kb-retrieval
description: Bedrock Knowledge Base retrieval MCP — RAG search across AWS Bedrock knowledge bases.
---
# Bedrock KB Retrieval

- **Status**: disabled (PC Alithya required)
- **JSON key**: `remote.awslabs.bedrock-kb-retrieval-mcp-server`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `uvx awslabs.bedrock-kb-retrieval-mcp-server@latest`
- **Source**: https://github.com/awslabs/mcp (awslabs official)
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| `search_knowledge_base` | RAG query across Bedrock KBs |

## Auth

- AWS SSO profile: csna-operations-sso-828
- Region: ca-central-1

## Limitations

- Currently disabled (remote on PC Alithya)
- Reranking disabled (`BEDROCK_KB_RERANKING_ENABLED=false`)
