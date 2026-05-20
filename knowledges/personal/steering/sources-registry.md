---
inclusion: always
---
# Personal Knowledge Hub — Sources Registry

## Source Priority and Roles

| Priority | Source | Role | MCP Tool | Domains Covered |
|----------|--------|------|----------|-----------------|
| 1 | Google NotebookLM | Primary KB (RAG) | `notebook_query()` | ALL |
| 2 | Notion Workspace | Primary structured data | `APIpostsearch()` | ALL |
| 3 | Alithya Knowledge RAG | Personal docs (PDF, finances, impôts, identité) | `search_knowledge()` | documents personnels, finances, impôts, identité |
| 4 | TickTick | Tasks, reminders, habits | `query_tasks()` | actions, rappels |
| 5 | Gmail | Communications, confirmations | `query_gmail_emails()` | communications, factures |
| 6 | Telegram | Messages, conversations, notes personnelles | MCP telegram tools | échanges personnels, notes, conversations conjointe |
| 7 | Browser Bookmarks | Liens sauvegardés (Chrome + Edge) | MCP bookmarks tools | liens, références, URLs sauvegardées |
| 8 | Excel | Financial tracking | `read_data_from_excel()` | finances |
| 9 | n8n | Automation triggers | workflow execution | automatisation |

## Source Details

### NotebookLM (Priority 1)

- **Accounts**: 2 Google accounts (both owned by me, separated by notebook type)
- **Content**: Structured knowledge bases organized by domain
- **Indexation**: Automatic (Google RAG embeddings) — no manual sync needed
- **Strengths**: Deep semantic search, synthesis, cross-document reasoning
- **Limitations**: Cannot write back; read-only queries
- **When to use**: Any factual question, procedures, reference material

### Notion Workspace (Priority 2)

- **Content**: Detailed pages, databases, mixed personal + professional
- **Indexation**: Native Notion search API — instant on any page edit
- **Strengths**: Structured data, databases, rich formatting, collaborative
- **Limitations**: Mixed content (personal + pro) — must filter
- **Filtering rule**: Exclude pages under professional/work spaces
- **When to use**: Structured info, lists, databases, detailed procedures

### Alithya Knowledge RAG (Priority 3)

- **Content**: Personal documents indexed from Dropbox/AAA_PRIVATE_LIFE — PDFs, avis de cotisation, factures, contrats, relevés fiscaux, documents d'identité, procédures
- **Server**: Remote MCP on PC Alithya (192.168.2.56:8080)
- **Indexation**: Hybrid search (semantic embeddings + BM25 keyword) with cross-encoder reranking
- **Tools**: `search_knowledge(query)`, `list_documents()`, `get_document(filepath)`
- **Strengths**: Deep search across all personal PDF/Word/Excel/code files, exact text matching, category filtering
- **Categories**: security, ctf, logscale, development, general, redteam, blueteam
- **When to use**: Any question about personal documents, impôts, finances, identité, contrats, factures, relevés officiels
- **Note**: Must be running on PC Alithya. If unreachable, inform user.

### Airtable (Priority 3b — Déménagement tasks)

- **Content**: Tâches actionnables du déménagement (80 tâches, 5 phases)
- **Base**: Personal Life (`appt4WObx12eJVPvK`)
- **Table**: Déménagement (`tblVZqY2ARz3R1CCY`)
- **URL**: https://airtable.com/appt4WObx12eJVPvK/tblVZqY2ARz3R1CCY/viw5DIXBPaFwdQot0
- **Tools**: `list_records()`, `create_record()`, `update_records()`
- **Colonnes**: Tâche, Statut, Responsable, Date limite, Priorité, Catégorie, Phase, Notes
- **Rôle**: Source de vérité UNIQUE pour le suivi des tâches du déménagement (depuis 2026-05-20)
- **When to use**: "Qu'est-ce que je dois faire ?", statut d'une tâche, mise à jour d'un statut, filtrer par priorité/phase/catégorie
- **Note**: Les steering files restent comme référence contextuelle (chronologie, budget, rôles, contraintes) mais ne sont PLUS la source pour le suivi des tâches.

### TickTick (Priority 4)

- **Content**: Tasks, recurring reminders, habits, projects
- **Indexation**: Built-in filters, full-text search, tag system
- **Strengths**: Time-based queries, recurring items, priority system
- **When to use**: "What do I need to do?", deadlines, reminders

### Gmail (Priority 5)

- **Content**: Emails, attachments, confirmations, invoices
- **Indexation**: Google search engine — instant
- **Strengths**: Chronological proof, official communications, attachments
- **When to use**: Confirmations, official dates, correspondence history

### Telegram (Priority 6)

- **Content**: Messages personnels, conversations avec conjointe (Abir), notes à soi-même, groupes familiaux
- **Protocol**: MTProto (userbot via @overpod/mcp-telegram)
- **Strengths**: Recherche dans l'historique des conversations, messages envoyés à soi-même comme notes rapides, échanges informels non capturés par email
- **When to use**: Chercher un échange avec la conjointe, retrouver une note/lien envoyé à soi-même, vérifier une conversation informelle, retrouver un message partagé
- **Note**: Timezone configuré America/Toronto

### Browser Bookmarks (Priority 7)

- **Content**: 7 260 bookmarks Chrome + 2 454 bookmarks Edge — liens sauvegardés au fil des années
- **Indexation**: Recherche par titre, URL, ou nom de dossier
- **Strengths**: Retrouver un lien sauvegardé sur un sujet précis, même ancien. Couvre Chrome ET Edge.
- **When to use**: "J'avais sauvegardé un lien sur X", "retrouve-moi le bookmark de Y", chercher une référence web déjà consultée/sauvegardée
- **Note**: Recherche locale, pas besoin de connexion internet

### Excel (Priority 8)

- **Content**: Financial spreadsheets (suivi-des-affaires.xlsx)
- **Path**: `/mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Procedures-en-cours/Suivi-tresorie-perso/suivi-des-affaires.xlsx`
- **When to use**: Financial amounts, budget tracking, account balances

### Local Knowledge RAG (Priority 7 — DEPRECATED, remplacé par Alithya Knowledge RAG)

- **Status**: Remplacé par Alithya Knowledge RAG (Priority 3) qui couvre le même contenu avec un meilleur indexage
- **Content**: Legacy — ne plus utiliser directement

## Extensibility

To add a new source:
1. Install/configure the MCP server
2. Add an entry to this registry with priority and domains
3. Update `query-routing.md` source selection matrix
4. No other changes needed — the agent adapts automatically

### Planned Future Sources

| Source | MCP | Status |
|--------|-----|--------|
| Telegram | telegram-mcp | 🔜 Planned |
| Google Drive | drive-mcp | 🔜 Planned |
| WhatsApp | whatsapp-mcp | 💭 Idea |
| Dropbox | dropbox-mcp | 💭 Idea |

## Source Health Rules

- If a source is unreachable → skip it, use fallbacks, inform user
- If a source returns empty → try fallback sources before saying "not found"
- NEVER cache results across sessions — always query fresh
- NEVER assume source content is the same as last time
