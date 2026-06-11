---
name: firecrawl
description: Web scraping, crawling, search, extraction, and autonomous research agent via Firecrawl API.
---
# Firecrawl

- **Status**: installed
- **JSON key**: `firecrawl`
- **Location**: settings/mcp.json
- **Wrapper**: `wrappers/firecrawl_wrapper.py`
- **Command**: `npx -y firecrawl-mcp`
- **Source**: https://github.com/firecrawl/firecrawl (official)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `firecrawl_scrape` | Scrape single URL (markdown, JSON, branding) |
| `firecrawl_search` | Web search with optional scraping |
| `firecrawl_crawl` | Crawl entire sites |
| `firecrawl_map` | Discover all URLs on a site |
| `firecrawl_extract` | Structured data extraction with LLM |
| `firecrawl_agent` | Autonomous web research agent |
| `firecrawl_interact` | Browser session interaction (click, fill) |
| `firecrawl_parse` | Parse local files |
| `firecrawl_monitor_*` | Change monitoring |

## Auth

- `FIRECRAWL_API_KEY` in `.env`

## Limitations

- Pay-per-use (credits)
- Agent research can take 1-5 minutes
- Some sites block scraping (use stealth proxy)
