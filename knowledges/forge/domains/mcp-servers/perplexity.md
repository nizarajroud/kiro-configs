---
name: perplexity
description: Real-time web search, reasoning, and deep research via Perplexity Sonar models.
---
# Perplexity

- **Status**: installed
- **JSON key**: `perplexity`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `python3 /home/nizar/HomeWspce/kiro-configs/wrappers/perplexity_wrapper.py`
- **Source**: Community wrapper
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `perplexity_search` | Quick web search |
| `perplexity_ask` | Ask with reasoning |
| `perplexity_research` | Deep research (multi-step) |
| `perplexity_reason` | Complex reasoning tasks |

## Auth

- `PERPLEXITY_API_KEY` in `.env`

## Limitations

- Pay-per-use (API credits)
- Deep research can be slow (30s+)
- Results quality depends on model tier
