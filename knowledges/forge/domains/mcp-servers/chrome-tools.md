---
name: chrome-tools
description: Chrome DevTools Protocol — capture network traffic, execute JS, query DOM, take screenshots.
---
# Chrome Tools

- **Status**: disabled (requires SSH tunnel to PC Alithya)
- **JSON key**: `chrome-tools`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `npx mcp-remote http://192.168.2.56:3212/mcp`
- **Source**: Community (@nicholmikey/chrome-tools)
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| Capture network traffic | Headers, requests, responses |
| Execute JavaScript | In browser tabs |
| Query DOM elements | CSS selectors |
| Take screenshots | Full page or elements |
| Monitor network events | Real-time |

## Auth

- Chrome running with `--remote-debugging-port=9222`
- SSH tunnel: `ssh -N -L 9222:localhost:9222 nizar@localhost`

## Limitations

- Currently disabled (SSH tunnel to PC Alithya required)
- Requires Chrome/Edge running with debug port
