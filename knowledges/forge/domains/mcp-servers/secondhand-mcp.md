---
name: secondhand-mcp
description: Search secondhand marketplaces (Facebook Marketplace, eBay, Depop, Poshmark) for used items. Use when user asks to find articles on used-goods platforms.
---
# Secondhand MCP Server

- **Status**: installed
- **JSON key**: `secondhand-mcp`
- **Wrapper**: none (npx direct)
- **Command**: `npx -y secondhand-mcp`
- **Source**: https://github.com/jlsookiki/secondhand-mcp
- **Notion**: [MCP: Secondhand](https://app.notion.com/p/MCP-Secondhand-Facebook-Marketplace-eBay-Depop-382174cb5dcc81dbba47df6ea48fadd0)
- **Verdict**: adopted — most active FB Marketplace MCP, communautaire, MIT

## Tools (3)

| Tool | Description |
|------|-------------|
| `search_marketplace` | Chercher des articles (query, marketplace, location, maxPrice, limit) |
| `get_listing_details` | Détails d'une annonce (photos, description, vendeur) |
| `list_marketplaces` | Lister les marketplaces actifs |

## Configuration actuelle

- `MARKETPLACES=facebook` (seul Facebook activé)
- Pour eBay : ajouter `EBAY_CLIENT_ID` et `EBAY_CLIENT_SECRET` dans `.env`
- Pour Depop/Poshmark : Chrome/Chromium requis

## Limitations

- Scraping (pas d'API officielle) — peut casser si Facebook change
- Ne pas faire trop de requêtes rapidement (rate limiting)
- Depop/Poshmark : ~5s par recherche (headless browser)
