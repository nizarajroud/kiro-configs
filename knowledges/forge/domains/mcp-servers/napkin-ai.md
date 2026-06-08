---
name: napkin-ai
description: Generate infographics and visuals (mindmaps, flowcharts, timelines, comparisons) from text via Napkin AI API
---
# Napkin AI MCP Server

- **Status**: installed
- **JSON key**: `napkin-ai`
- **Wrapper**: `wrappers/napkin_ai_wrapper.py`
- **npm**: `napkin-ai-mcp`
- **GitHub**: https://github.com/LouisChanCLY/napkin-ai-mcp
- **API access**: Developer preview — request at api@napkin.ai

## What it does

Generates professional infographics from text content:
- Mindmaps, flowcharts, timelines, comparisons, hierarchies, cycles, matrices
- Output formats: SVG, PNG, PPT
- Storage: local filesystem, S3, Google Drive, Slack, Notion, Telegram, Discord

## Tools

| Tool | Description |
|------|-------------|
| `generate_visual` | Submit async generation request |
| `generate_and_wait` | Generate and wait for result |
| `generate_and_save` | Generate and save to storage |
| `check_status` | Check generation status |
| `download_visual` | Download as base64 |
| `list_styles` | List available styles |

## Activation steps

1. Request API key at api@napkin.ai
2. Replace `NAPKIN_API_KEY=PLACEHOLDER_REQUEST_ACCESS` in `.env`
3. Set `"disabled": false` in `settings/mcp.json`
4. Test: ask agent to generate a mindmap

## Verdict

Pending — cannot test until API key obtained. Promising for visual generation use cases.
