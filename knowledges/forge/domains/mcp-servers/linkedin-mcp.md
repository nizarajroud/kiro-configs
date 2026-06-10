---
name: linkedin-mcp
description: Access LinkedIn data: profiles, job search, company info, messages, feed, people search via browser session scraping.
---
# LinkedIn MCP Server

- **Status**: installed
- **JSON key**: `linkedin-mcp`
- **Wrapper**: none (auth via browser session)
- **Command**: `uvx linkedin-scraper-mcp@latest`
- **Source**: https://github.com/stickerdaniel/linkedin-mcp-server (⭐2214)
- **Notion**: [MCP: LinkedIn](pending)
- **Verdict**: adopted — most starred & actively maintained LinkedIn MCP, communautaire

## Tools (16)

| Tool | Description |
|------|-------------|
| `get_person_profile` | Profil complet (experience, education, skills, posts) |
| `get_my_profile` | Son propre profil |
| `search_people` | Chercher des personnes |
| `search_jobs` | Chercher des offres |
| `search_companies` | Chercher des entreprises |
| `get_company_profile` | Profil entreprise |
| `get_company_employees` | Employés d'une entreprise |
| `get_job_details` | Détails d'une offre |
| `get_inbox` | Messages LinkedIn |
| `send_message` | Envoyer un message |
| `connect_with_person` | Envoyer invitation |
| `get_feed` | Fil d'actualité |
| `get_sidebar_profiles` | Profils recommandés |
| `search_conversations` | Chercher dans les messages |
| `get_conversation` | Lire une conversation |
| `close_session` | Fermer la session |

## Auth

Premier lancement : ouvre un navigateur Chromium, tu te connectes à LinkedIn manuellement. Les cookies sont sauvegardés dans `~/.linkedin-mcp/`. Les sessions suivantes sont automatiques.

## Limitations

- Non-officiel (scraping) — risque de blocage si abus
- Pas de support des "Saved Items" (éléments enregistrés)
- Nécessite un navigateur (Patchright/Chromium)
