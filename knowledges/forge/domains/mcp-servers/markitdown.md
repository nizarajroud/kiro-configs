---
name: markitdown
description: Convert any document (Word, Excel, PDF, PPTX, HTML, images) to Markdown via Microsoft's MarkItDown library
---
# MarkItDown MCP

- **Status**: installed
- **JSON key**: `markitdown`
- **Agent(s)**: compass
- **Wrapper**: none (direct venv binary)
- **Binary**: `/home/nizar/.markitdown-mcp/bin/markitdown-mcp`
- **Venv**: `/home/nizar/.markitdown-mcp/`
- **Package**: `markitdown-mcp==0.0.1a4` (PyPI) — depends on `markitdown[all]>=0.1.1`
- **Source**: https://github.com/microsoft/markitdown (⭐145k)
- **Notion**: [MCP: MarkItDown](https://app.notion.com/p/MCP-MarkItDown-376174cb5dcc81eb9505e0674a9ab6d3)
- **Verdict**: adopted — official Microsoft tool, single `convert_to_markdown(uri)` tool, supports all common office formats

## Tool Exposed

| Tool | Description |
|------|-------------|
| `convert_to_markdown(uri)` | Accepts `file://`, `http://`, `https://`, `data:` URIs. Returns document content as Markdown. |

## Supported Formats

Word (.docx), Excel (.xlsx/.xls), PDF, PowerPoint (.pptx), HTML, images (with OCR), audio (transcription), YouTube transcripts

## Notes

- Installed in dedicated venv to avoid mcp version conflict (requires mcp~=1.8.0 vs global mcp>=1.27)
- No secrets needed — purely local file conversion
- For local files, use `file:///absolute/path/to/document.docx`
