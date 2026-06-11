---
name: google-maps
description: Google Maps Grounding Lite — search places, compute routes, lookup weather via official Google remote MCP server.
---
# Google Maps Grounding Lite

- **Status**: installed
- **JSON key**: `google-maps`
- **Wrapper**: `wrappers/google_maps_wrapper.py`
- **Command**: `npx mcp-remote https://mapstools.googleapis.com/mcp`
- **Source**: https://github.com/google/mcp (⭐4.2k) — official Google
- **Documentation**: https://developers.google.com/maps/ai/grounding-lite
- **Verdict**: adopted — official Google remote MCP, GA status

## Tools (3)

| Tool | Description |
|------|-------------|
| `search_places` | Search places (restaurants, schools, clinics…) — returns AI summary + Place IDs + coords + Google Maps links |
| `compute_routes` | Calculate driving/walking route between two points (distance + duration) |
| `lookup_weather` | Weather conditions (current + hourly + daily forecast) |

## Auth

- API Key via `GOOGLE_MAPS_API_KEY` in `.env`
- Key restricted to Maps Grounding Lite API only
- Requires Google Cloud billing account (200$/month free credit)

## Quotas

- 300 queries/min per tool (search_places, compute_routes, lookup_weather)
- Budget alert set at $1

## Limitations

- 3 tools only (no Street View, no geocoding, no elevation)
- Attribution required when displaying results to end users
- LLM must not cache/train on returned data (compliant with our usage)
