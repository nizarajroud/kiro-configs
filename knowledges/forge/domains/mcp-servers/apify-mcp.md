---
name: apify-mcp
description: Apify platform MCP — extract data from social media, search engines, maps, e-commerce sites using 1000+ ready-made Actors (scrapers/crawlers/automations).
---
# apify-mcp — Web Data Extraction Platform

- **Status**: installed (pending token activation)
- **JSON key**: `apify-mcp`
- **Agent**: **connect2**
- **Type**: Remote (Streamable HTTP via mcp-remote bridge)
- **URL**: `https://mcp.apify.com/mcp`
- **Auth**: API token (Bearer header) — apify.com/account#/integrations
- **Source**: https://github.com/apify/apify-mcp-server (officiel Apify)
- **Version**: 0.10.8 (server-side, dernière release 21 mai 2026)
- **Verdict**: adopted — plateforme officielle, 1000+ Actors pré-faits, actif aujourd'hui

## Tools (dynamiques — dépendent des Actors configurés)

Les tools sont générés dynamiquement selon les Actors Apify activés. Exemples courants :

| Actor                        | Description                              |
|------------------------------|------------------------------------------|
| Web Scraper                  | Scraping générique de pages web          |
| Google Maps Scraper          | Extraire business data de Google Maps    |
| Instagram Scraper            | Posts, profils, hashtags Instagram       |
| TikTok Scraper               | Vidéos, profils, hashtags TikTok         |
| Amazon Product Scraper       | Prix, reviews, détails produits          |
| Google Search Scraper        | Résultats de recherche Google            |
| Facebook Pages/Groups        | Posts et commentaires de pages/groupes   |
| RAG Web Browser              | Navigation web intelligente pour RAG     |

## Configuration MCP

```json
"apify-mcp": {
  "description": "Apify platform — extract data from social media, search engines, maps, e-commerce sites using 1000+ ready-made Actors.",
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://mcp.apify.com/mcp"],
  "env": {
    "APIFY_TOKEN": "${APIFY_TOKEN}"
  },
  "disabled": false
}
```

## Auth

- Obtenir token : apify.com/account#/integrations
- Free tier : 5$/mois de crédits gratuits
- Token dans `.env` : `export APIFY_TOKEN=apify_api_xxxxx`

## Pricing

- **Free** : 5$/mois de crédits (suffisant pour tests)
- **Pay-as-you-go** : au-delà du free tier
- Chaque Actor a son propre coût (compute + réseau)

## Notes

- Remote server — zéro RAM locale, zéro processus (via mcp-remote bridge)
- 1000+ Actors disponibles sur Apify Store
- Peut remplacer/compléter Firecrawl pour du scraping structuré
- Différence avec Firecrawl : Apify = Actors spécialisés (Google Maps, Amazon, etc.), Firecrawl = scraping générique
