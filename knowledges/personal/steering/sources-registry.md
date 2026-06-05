---
inclusion: always
---
# Sources Registry — Detailed Reference

Detailed capabilities and operational notes for each source. Complements the routing table in the prompt.

## NotebookLM (Priority 1)

- **Accounts**: 2 Google accounts (both owned by me, separated by notebook type)
- **Content**: Structured knowledge bases organized by domain
- **Indexation**: Automatic (Google RAG embeddings) — no manual sync needed
- **Strengths**: Deep semantic search, synthesis, cross-document reasoning
- **Limitations**: Cannot write back; read-only queries
- **When to use**: Any factual question, procedures, reference material

## Notion Workspace (Priority 2)

- **Content**: Detailed pages, databases, mixed personal + professional
- **Indexation**: Native Notion search API — instant on any page edit
- **Strengths**: Structured data, databases, rich formatting
- **Limitations**: Mixed content (personal + pro) — must filter
- **Filtering rule**: Exclude pages under professional/work spaces
- **When to use**: Structured info, lists, databases, detailed procedures

## Alithya Knowledge RAG (Priority 3)

- **Content**: Personal documents from Dropbox/AAA_PRIVATE_LIFE — PDFs, avis de cotisation, factures, contrats, relevés fiscaux, documents d'identité
- **Server**: Remote MCP on PC Alithya (192.168.2.56:8080)
- **Indexation**: Hybrid search (semantic embeddings + BM25) with cross-encoder reranking
- **Tools**: `search_knowledge(query)`, `list_documents()`, `get_document(filepath)`
- **When to use**: Personal documents, impôts, finances, identité, contrats, factures
- **Note**: Must be running on PC Alithya. If unreachable, inform user.

## Airtable (Priority 3b — Déménagement)

- **Content**: Tâches actionnables du déménagement (80 tâches, 5 phases)
- **Base**: Personal Life (`appt4WObx12eJVPvK`)
- **Table**: Déménagement (`tblVZqY2ARz3R1CCY`)
- **URL**: https://airtable.com/appt4WObx12eJVPvK/tblVZqY2ARz3R1CCY/viw5DIXBPaFwdQot0
- **Colonnes**: Tâche, Statut, Responsable, Date limite, Priorité, Catégorie, Phase, Notes
- **Rôle**: Source de vérité UNIQUE pour le suivi des tâches du déménagement
- **When to use**: Statut d'une tâche, filtrer par priorité/phase/catégorie, mise à jour de statut

## TickTick (Priority 4)

- **Content**: Tasks, recurring reminders, habits, projects
- **Indexation**: Built-in filters, full-text search, tag system
- **When to use**: "What do I need to do?", deadlines, reminders

## Gmail (Priority 5)

- **Content**: Emails, attachments, confirmations, invoices
- **Indexation**: Google search engine — instant
- **When to use**: Confirmations, official dates, correspondence history

## Telegram (Priority 6)

- **Content**: Messages personnels, conversations avec Abir, notes à soi-même, groupes familiaux
- **When to use**: Échanges avec conjointe, notes/liens envoyés à soi-même, conversations informelles
- **Note**: Timezone America/Toronto

## Browser Bookmarks (Priority 7)

- **Content**: 7 260 Chrome + 2 454 Edge bookmarks
- **When to use**: "J'avais sauvegardé un lien sur X", retrouver une URL déjà consultée

## Excel (Priority 8)

- **Content**: suivi-des-affaires.xlsx
- **Path**: `/mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Procedures-en-cours/Suivi-tresorie-perso/suivi-des-affaires.xlsx`
- **When to use**: Financial amounts, budget tracking, account balances
