---
name: rtl-visual-mcp
description: Generate PNG visuals with proper RTL Arabic/English bidi rendering via Playwright headless browser. Use for Tunisian explanation visuals.
---
# RTL Visual MCP

- **Status**: installed
- **JSON key**: `rtl-visual-mcp`
- **Wrapper**: none (standalone Python script)
- **Command**: `python3 /home/nizar/HomeWspce/rtl-visual-mcp/server.py`
- **Notion**: [MCP: RTL Visual](https://app.notion.com/p/MCP-RTL-Visual-379174cb5dcc81d3803af0e8b7e17415)
- **Source**: custom (built in-house)
- **Verdict**: adopted — only solution for proper bidi Arabic+English in diagrams

## Tools

| Tool | Description |
|------|-------------|
| `create_rtl_mindmap` | Mindmap with colored branches, grid layout |
| `create_rtl_flowchart` | Vertical step-by-step flowchart |

## How it works

1. Takes structured content (title, branches/steps with Arabic+English text)
2. Generates HTML with `dir="rtl"` + CSS grid/flexbox
3. Renders via Playwright/Chromium headless → PNG screenshot
4. Browser's native Unicode Bidi Algorithm handles the mix perfectly

## Dependencies

- Python 3.10+
- playwright (`pip install playwright`)
- Chromium headless (`playwright install chromium`)

## When to use

- User asks for "visual tunisian explanation"
- Any diagram with Arabic/Tunisian text mixed with English technical terms
- NOT for pure English diagrams (use `excalidraw-mcp` instead)
