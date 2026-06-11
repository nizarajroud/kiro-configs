---
name: markdown2pdf
description: Converts Markdown content to PDF files with syntax highlighting, tables, images, and Mermaid diagrams.
---
# Markdown2PDF

- **Status**: disabled
- **JSON key**: `markdown2pdf`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `node /home/nizar/.npm-global/lib/node_modules/markdown2pdf-mcp/build/index.js`
- **Source**: Community (markdown2pdf-mcp)
- **Verdict**: adopted (disabled by choice)

## Tools

| Tool | Description |
|------|-------------|
| `create_pdf_from_markdown` | Convert markdown string to PDF file |

## Auth

- None

## Limitations

- Output dir: `/home/nizar/workspace/assets/markdown2pdf-output`
- No LaTeX math support
- Supports: headers, lists, tables, code blocks, images, Mermaid
