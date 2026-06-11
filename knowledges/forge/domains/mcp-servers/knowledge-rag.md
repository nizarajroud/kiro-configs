---
name: knowledge-rag
description: Local RAG knowledge base — search personal documents stored in ~/My-KB-Documents.
---
# Knowledge RAG (local)

- **Status**: disabled (remote on PC Alithya)
- **JSON key**: `knowledge-rag`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `npx mcp-remote http://192.168.2.56:3222/mcp`
- **Source**: Custom local server
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| `search_knowledge` | RAG search across local documents |

## Auth

- Remote server on PC Alithya

## Limitations

- Requires PC Alithya running
- Supports: PDF, Markdown, Word, Excel, PowerPoint, code files
- Currently replaced by `alithya-knowledge-rag` in mcp.json (same backend)
