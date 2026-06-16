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

### Finances (revenus, dépenses, épargne, cashflow, cotisations, allocations, impôts)

**RÈGLE ABSOLUE** — Pour toute question financière, consulter l'Excel EN PREMIER :

- **Fichier** : `/mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Procedures-en-cours/Suivi-tresorie-perso/suivi-des-affaires.xlsx`
- **Onglet principal** : `Main-finance-[année en cours]` (ex: `Main-finance-2026`)
- **Onglets complémentaires** : `Cotisation`, `tresorie`, `credits d'impot`, `Allocations-Enfants` selon le sujet

**Ordre de consultation :**
1. **Excel** (onglet Main-finance de l'année en cours) — TOUJOURS en premier
2. Memory-compass — faits déjà extraits
3. NotebookLM (NLM_AAA_PRIVATE_LIFE) — documents fiscaux/relevés
4. Gmail — confirmations de montants

**Ne JAMAIS** répondre à une question financière à partir des steering files statiques (`revenus.md`, `depenses-fixes.md`) sans d'abord vérifier l'Excel qui est la source vivante et à jour.

---

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

## NotebookLM — Routing par notebook (OBLIGATOIRE)

**RÈGLE ABSOLUE** — Toujours consulter les **2 notebooks** avant de conclure qu'une info est absente :

| Notebook | ID | Contenu |
|----------|-----|---------|
| **2745 rolland therrian** | `ecb14fdb-e9e8-40fe-9e1e-2130ab7c370c` | Documents immobiliers (promesse d'achat, déclaration vendeur, inspection, taxes foncières, notaire) |
| **NLM_AAA_PRIVATE_LIFE** | `1495e7d2-3d75-419d-a9a5-d0e43fe6d1e8` | Documents personnels Dropbox (investissements, impôts, relevés fiscaux, identité, contrats, assurances, ET immobilier complémentaire) |

**Ordre de consultation :**
1. **Sujet immobilier** → « 2745 » EN PREMIER, puis « NLM_AAA_PRIVATE_LIFE » si info absente/incomplète
2. **Tout autre sujet personnel** → « NLM_AAA_PRIVATE_LIFE » directement
3. **Ne JAMAIS conclure « non trouvé dans NotebookLM »** sans avoir vérifié les DEUX notebooks

---

## Query Formulation Tips

| Source | Tips |
|--------|------|
| NotebookLM | Toujours vérifier les 2 notebooks (voir règle ci-dessus) |
| Notion | Filter results to personal pages only |
| Gmail | Use Gmail search syntax (from:, subject:, newer_than:) |
| TickTick | Filter by project/tag matching domain |
| Excel | For financial data only |
| Alithya RAG | Fallback for sensitive/offline documents |

## Deduplication Rules

- 2+ sources return same fact → report ONCE, cite ALL sources
- Sources return complementary info → merge into coherent answer
- Sources return contradictory info → see Contradiction Handling in prompt
