---
name: playwright
description: Browser automation and web screenshots using Playwright headless browser.
---
# Playwright

- **Status**: disabled (remote on PC Alithya)
- **JSON key**: `playwright`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `npx @playwright/mcp@latest --headless`
- **Source**: https://github.com/microsoft/playwright-mcp (official Microsoft)
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| Navigate, click, type, scroll | Page interaction |
| Take screenshots | Full page or element-specific |
| Execute JavaScript | DOM manipulation, CSS injection |

## Auth

- Remote server on PC Alithya (192.168.2.56:3210)

## Limitations

- Currently disabled (remote unavailable)
- Supports CSS injection for visual annotations
