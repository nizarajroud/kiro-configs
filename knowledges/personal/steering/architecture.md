---
inclusion: always
---
# Personal Knowledge Hub — Architecture

## Layered Architecture (4 Layers)

```
LAYER 1: INTERFACE (extensible input channels)
    │
LAYER 2: AGENT (intelligence + routing + synthesis)
    │
LAYER 3: MCP (standardized connectors, live access)
    │
LAYER 4: DATA SOURCES (dynamic, self-indexed, autonomous)
```

## Layer 1 — Interface

Any channel that sends a natural language request to the agent.

| Channel | Status | Protocol |
|---------|--------|----------|
| Kiro CLI | ✅ Active | Direct MCP |
| Telegram Bot | 🔜 Planned | Webhook → Agent |
| Web UI | 🔜 Planned | HTTP → Agent |
| Voice | 🔜 Planned | STT → Agent |

**Rule**: The interface layer is a thin pass-through. It NEVER contains business logic or routing decisions.

## Layer 2 — Agent

The brain. Receives a request, classifies it, routes to sources, synthesizes the answer.

**Responsibilities:**
- Intent classification (what domain? what type of info?)
- Source selection (which 2-3 sources are relevant?)
- Parallel querying of selected sources
- Deduplication and synthesis
- Source citation for every fact
- Contradiction detection and signaling

**Implementation**: Kiro + prompt system (exp2 agent) with MCP connectors.
**Config location**: `~/HomeWspce/kiro-configs/agents/`

## Layer 3 — MCP (Connectors)

Each source is accessed via a standardized MCP server. The protocol is uniform — only the underlying data differs.

| MCP Server | Source | Query Tool |
|------------|--------|------------|
| notebooklm | Google NotebookLM (2 accounts) | `notebook_query()` |
| notion-workspace | Notion pages & databases | `APIpostsearch()` |
| ticktick | Tasks, habits, reminders | `query_tasks()` |
| gmail | Emails, attachments | `query_gmail_emails()` |
| excel | Financial spreadsheets | `read_data_from_excel()` |
| knowledge-rag | Local files (~/My-KB-Documents) | `search_knowledge()` |
| n8n | Automation workflows | Trigger/query workflows |

**Rule**: Adding a new source = adding a new MCP server. No other layer changes.

## Layer 4 — Data Sources

Sources are **dynamic and autonomous**. They change at any time without notification.

**Critical principle**: We NEVER copy data locally. Each source manages its own indexation:
- NotebookLM: RAG embeddings managed by Google
- Notion: Native search API
- Gmail: Google search engine
- TickTick: Built-in filters and full-text search

**Rule**: The agent queries sources in REAL TIME. There is no batch sync, no local cache, no stale index.

## Data Flow for a Typical Query

```
User: "Quelle est la date d'inscription de Léa à l'école?"

1. CLASSIFY → Domain: famille/enfants/écoles | Type: factual (date)
2. SELECT SOURCES → NotebookLM (notebook famille) + Notion + Gmail
3. PARALLEL QUERY:
   - NotebookLM: notebook_query("date inscription Léa école")
   - Notion: APIpostsearch("inscription Léa école")
   - Gmail: query_gmail_emails("from:ecole subject:inscription")
4. SYNTHESIZE:
   - Deduplicate identical facts
   - Cite source for each fact
   - Flag any contradictions
5. RESPOND with citations
```

## Directory Structure

```
~/HomeWspce/personal-knowledge-hub/
├── .kiro/steering/          ← Routing rules, architecture, principles
├── config/                  ← Domain taxonomy, source registry
├── domains/                 ← Symlinks to local data projects
│   ├── demenagement/ →      ~/workspace/demenagement/
│   └── personal-details/ →  ~/workspace/perosnal-dtls/
└── README.md
```

## Relationship to Other Workspaces

| Path | Role |
|------|------|
| `~/HomeWspce/kiro-configs/` | Technical config (agents, prompts, MCP settings) |
| `~/HomeWspce/personal-knowledge-hub/` | Knowledge orchestration (this project) |
| `~/workspace/demenagement/` | Domain data (relocation) |
| `~/workspace/perosnal-dtls/` | Domain data (personal details) |
