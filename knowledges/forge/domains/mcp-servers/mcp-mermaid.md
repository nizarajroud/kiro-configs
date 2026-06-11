---
name: mcp-mermaid
description: Mermaid diagram generator — converts Mermaid syntax to PNG/SVG/base64 images.
---
# MCP Mermaid

- **Status**: installed
- **JSON key**: `mcp-mermaid`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `npx -y @peng-yin/mcp-mermaid`
- **Source**: Community package
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `generate_mermaid_diagram` | Generate diagram from Mermaid syntax (base64, svg, file, svg_url, png_url) |

## Auth

- None required

## Limitations

- Single tool only
- Output types: base64, svg, mermaid text, file, svg_url, png_url
- Themes: default, base, forest, dark, neutral
- Does NOT support RTL/Arabic text (use rtl-visual-mcp instead)
