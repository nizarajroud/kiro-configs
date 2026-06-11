---
name: notebooklm
description: Google NotebookLM MCP — manage notebooks, add sources, AI queries, generate studio artifacts (audio, video, slides, mind maps).
---
# NotebookLM

- **Status**: installed
- **JSON key**: `notebooklm`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `notebooklm-mcp`
- **Source**: Community (notebooklm-mcp package)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `notebook_list` / `notebook_create` / `notebook_delete` | Notebook management |
| `notebook_query` | Ask AI about sources in a notebook |
| `source_add` | Add sources (URL, text, Drive, file) |
| `source_delete` / `source_rename` | Source management |
| `studio_create` | Generate artifacts (audio, video, slides, infographic, quiz, etc.) |
| `studio_status` / `download_artifact` | Check and download generated content |
| `research_start` / `research_status` / `research_import` | Deep/fast web research |
| `cross_notebook_query` | Query across multiple notebooks |
| `label` | Organize sources with labels |
| `note` | Manage notes in notebooks |

## Auth

- Cookie-based auth (`nlm login` CLI or manual cookie injection)
- Requires periodic re-auth (~7 days)

## Limitations

- Auth expires frequently — needs `nlm login` refresh
- Queries can timeout on large notebooks (50+ sources) — use async mode
- Cannot write back to sources (read-only RAG)
- Studio artifacts take time to generate (poll for completion)
