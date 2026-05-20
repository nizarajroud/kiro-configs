---
inclusion: always
---
# Personal Knowledge Hub — Query Routing Rules

## Strategy: Intelligent Routing + Parallel Enrichment

The agent does NOT search all sources for every question. It classifies the request, selects 2-3 relevant sources, queries them in parallel, then synthesizes.

## Step 0 — User-Directed Routing (HIGHEST PRIORITY)

When the user explicitly specifies a data source or a specific location within a source, this OVERRIDES all automatic routing logic:

1. **Source specified** → Use THAT source first, no classification needed
2. **Source + specific location** (e.g., a notebook name, a Notion page, a project, a folder) → Go DIRECTLY to that exact location and search there
3. **Second priority** → Search sibling/related locations at the same hierarchical level (e.g., other pages in the same database, other tasks in the same project, other notebooks in the same domain)
4. **Third priority** → Only then expand to other sources if needed

**Examples:**
- "Cherche dans NotebookLM, notebook Famille" → Query that specific notebook FIRST
- "Regarde dans TickTick, projet Déménagement" → Query that project FIRST, then related projects
- "C'est dans Notion, page Assurance" → Go to that page FIRST, then related pages in the same database
- "Vérifie dans Gmail, les emails de Sophie" → Search Gmail with from:Sophie FIRST

**Rule:** Never ignore a user-directed source. Never substitute automatic routing when the user has explicitly told you where to look.

---

## Step 1 — Classify the Request

Every incoming question must be classified along two axes:

### Domain Classification
| Domain | Keywords / Signals |
|--------|-------------------|
| demenagement | déménagement, maison, adresse, boîtes, logement |
| famille/enfants | enfants, Léa, Adam, école, garderie, club |
| famille/ecoles | inscription, école, bulletin, professeur |
| finances | compte, budget, dépense, revenu, épargne, investissement |
| admin | papiers, assurance, impôt, immigration, permis |
| abonnements | téléphone, internet, gym, cloud, Netflix |
| identite | passeport, NAS, carte, date de naissance |

### Request Type Classification
| Type | Description | Example |
|------|-------------|---------|
| factual | A specific fact (date, amount, name) | "Quelle est la date X?" |
| action | Something to do / a reminder | "Qu'est-ce que je dois faire pour Y?" |
| document | A file or attachment needed | "Où est le contrat de Z?" |
| timeline | Chronological history | "Qu'est-ce qui s'est passé avec X?" |
| procedure | How-to / steps | "Comment faire pour Y?" |
| exploration | Everything we know about X | "Donne-moi tout sur X" |

## Step 2 — Select Sources

Based on classification, select sources using this matrix:

| Request Type | Primary Sources | Fallback Sources |
|-------------|----------------|-----------------|
| factual | NotebookLM, Notion | Gmail, Telegram |
| action | TickTick, Notion | NotebookLM |
| document | NotebookLM, Gmail, Alithya RAG | Notion, local files |
| timeline | Gmail, Notion, TickTick | NotebookLM, Telegram |
| procedure | NotebookLM, Notion | — |
| exploration | ALL sources (fan-out) | — |
| link/reference | Bookmarks, NotebookLM | Telegram, Gmail |
| conversation | Telegram, Gmail | Notion |

**Rules:**
- Maximum 3 sources for non-exploration queries
- For `exploration` type: query ALL sources in parallel
- If primary sources return nothing: try fallback sources
- NEVER skip NotebookLM for factual/procedure questions

## Step 3 — Query Sources in Parallel

Once sources are selected, query them simultaneously. Do NOT wait for one to finish before starting the next.

### Query Formulation per Source

| Source | How to Query | Tips |
|--------|-------------|------|
| NotebookLM | `notebook_query(notebook_id, query)` | Use the notebook matching the domain |
| Notion | `APIpostsearch(query)` | Filter results to personal pages only |
| Gmail | `query_gmail_emails(query)` | Use Gmail search syntax (from:, subject:, newer_than:) |
| TickTick | `query_tasks(text_query, tags, project_names)` | Filter by project/tag matching domain |
| Excel | `read_data_from_excel(filepath, sheet)` | For financial data only |
| Local files | `search_knowledge(query)` | Fallback for sensitive/offline data |

## Step 4 — Synthesize the Response

### Deduplication Rules
- If 2+ sources return the same fact → report it ONCE, cite ALL sources
- If sources return complementary info → merge into a coherent answer
- If sources return contradictory info → see Contradiction Handling below

### Citation Format (MANDATORY)
Every fact in the response MUST include its source:

```
✅ CORRECT:
"La date d'inscription est le 15 mars 2026. [NotebookLM: Notebook Famille]"

❌ INCORRECT:
"La date d'inscription est le 15 mars 2026."
```

### Response Structure
```
[Answer to the question]

Sources:
- [NotebookLM] Notebook X → description
- [Notion] Page Y → description
- [Gmail] Email from Z, date

[Coherence status: ✓ All sources agree / ⚠️ Contradiction detected]
```

## Step 5 — Handle Contradictions

When sources disagree:

1. **Signal it explicitly** — never silently pick one
2. **Show both versions** with their sources
3. **Suggest which is more likely correct** based on recency
4. **Ask the user to confirm** which is authoritative

```
⚠️ CONTRADICTION:
- [NotebookLM] says: inscription le 15 mars
- [Gmail] says: email du 20 mars reportant au 22 mars

→ The email is more recent. The date was likely postponed.
→ Recommendation: update NotebookLM notebook.
→ Which information is correct?
```

## Anti-Patterns (NEVER DO)

| ❌ Never | ✅ Instead |
|----------|-----------|
| Query all sources for a simple factual question | Select 2-3 relevant sources |
| Return an answer without citing the source | ALWAYS cite |
| Silently ignore a contradiction | ALWAYS flag it |
| Maintain a local copy of source data | Query live via MCP |
| Assume data hasn't changed since last query | Always query fresh |
| Answer "I don't know" without trying all fallbacks | Exhaust fallback sources first |
