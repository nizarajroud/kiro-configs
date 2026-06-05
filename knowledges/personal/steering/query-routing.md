---
inclusion: always
---
# Query Routing — Complementary Rules

Rules that extend the prompt's routing logic with domain-specific overrides, examples, and operational tips.

## Domain-Specific Routing Overrides

### Santé (médecin, clinique, RAMQ, GAP, rendez-vous médical, pharmacie, dentiste, hôpital)

1. **Bookmarks** — dossier/catégorie santé (`search_bookmarks`)
2. **Notion** — section santé (`APIpostsearch`)
3. Sources habituelles (NotebookLM, Gmail)

## User-Directed Routing — Examples

- "Cherche dans NotebookLM, notebook Famille" → Query that specific notebook FIRST
- "Regarde dans TickTick, projet Déménagement" → Query that project FIRST, then related projects
- "C'est dans Notion, page Assurance" → Go to that page FIRST, then related pages in the same database
- "Vérifie dans Gmail, les emails de Sophie" → Search Gmail with from:Sophie FIRST

**Rule:** When the user specifies a source + specific location, go DIRECTLY there. Second priority: sibling/related locations. Third: expand to other sources.

## Override: Information publique → FireCrawl EN PREMIER

**RÈGLE ABSOLUE** — Quand la question porte sur une information **PUBLIQUE** (non personnelle):

1. **FireCrawl** (scraping du site officiel) — TOUJOURS en premier
2. Bookmarks — si FireCrawl indisponible
3. Connaissance générale — dernier recours avec avertissement

**Appliquer quand :** Tarifs, procédures officielles, formulaires, horaires, conditions générales, infos médicales générales, sites officiels (gouv.qc.ca, hydroquebec.com, bnc.ca, etc.)

**NE PAS appliquer quand :** L'info est personnelle (mes comptes, mes dates, mes documents)

## Query Formulation Tips

| Source | Tips |
|--------|------|
| NotebookLM | Use the notebook matching the domain |
| Notion | Filter results to personal pages only |
| Gmail | Use Gmail search syntax (from:, subject:, newer_than:) |
| TickTick | Filter by project/tag matching domain |
| Excel | For financial data only |
| Alithya RAG | Fallback for sensitive/offline documents |

## Deduplication Rules

- 2+ sources return same fact → report ONCE, cite ALL sources
- Sources return complementary info → merge into coherent answer
- Sources return contradictory info → see Contradiction Handling in prompt
