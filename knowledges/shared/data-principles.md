---
inclusion: always
---
# Data Principles

## Principle 1: Data is Dynamic

All sources change at any time without notification. The agent MUST:
- Query sources in real time for every request
- Never assume data is the same as a previous session
- Never rely on cached or memorized answers from past conversations

## Principle 2: No Duplication

Data lives in ONE authoritative location. We do not copy it elsewhere.

| ❌ Wrong | ✅ Right |
|----------|---------|
| Copy Notion page content into a local .md file | Query Notion live |
| Export NotebookLM answers into a local index | Query NotebookLM live |
| Store Gmail search results locally | Query Gmail live |
| Maintain a "last known state" cache | Always query fresh |

**Exception**: The `domains/` folder contains data that has NO other home (e.g., steering files for the déménagement project that don't exist in Notion or NotebookLM).

## Principle 3: Source Citation is Mandatory

Every piece of information returned to the user MUST include:
- Which source it came from
- Enough context to verify (page name, email date, notebook name)

This is non-negotiable. An answer without a source citation is incomplete.

## Principle 4: Contradictions are Valuable

When sources disagree, this is INFORMATION, not an error. The agent must:
1. Present both versions clearly
2. Indicate which is more recent
3. Suggest which might be outdated
4. Ask the user to confirm the truth
5. Optionally suggest updating the stale source

## Principle 5: Extensibility Over Completeness

It is better to have a system that can easily add new sources than to try to cover everything from day one.

**Adding a new source requires only:**
1. A working MCP server
2. An entry in `sources-registry.md`
3. A routing rule in `query-routing.md`

No infrastructure changes, no database migrations, no reindexing.

## Principle 6: Privacy and Sensitivity

- Sensitive data (passwords, financial details, legal documents) stays in local files or NotebookLM (private notebooks)
- The agent never exposes raw sensitive data in responses — it references by key, not by value
- No source data is transmitted to third-party services beyond the MCP connections already configured

## Principle 7: Freshness Over Completeness

If a source is temporarily unavailable:
- Inform the user that source X could not be reached
- Provide partial results from available sources
- NEVER fabricate or guess information to fill the gap
- Suggest retrying later for the missing source

## Principle 8: Timezone is Always Montreal (America/Toronto)

All dates and times displayed to the user or interpreted from sources MUST use the **America/Toronto** timezone (Eastern Time, Montréal/Québec). This applies to:
- Displaying task due dates and event times
- Interpreting timestamps from TickTick, Gmail, Google Calendar, etc.
- Converting UTC or other timezone data before presenting to the user
- The current time reference is always the local machine time (ET)

Never display raw UTC times to the user. Always convert to Eastern Time (ET).

## Principle 9: The Agent Learns Routing, Not Data

The steering files teach the agent HOW to find information, not WHAT the information is. If the agent needs to "remember" a fact, it should be stored in one of the sources (NotebookLM, Notion, etc.), not in a steering file.

| Belongs in steering files | Belongs in data sources |
|--------------------------|------------------------|
| "For school questions, check NotebookLM first" | "Léa is enrolled at École X" |
| "Financial data is in the Excel file" | "Monthly rent is $1,500" |
| "Use Gmail for confirmation dates" | "The appointment is March 15" |

## Principle 10: Local Project Memory

Every project folder that involves iterative work (multiple sessions) MUST contain a `notes.md` file that serves as the **local working memory** for that project.

### Rules

1. **Updated during the session** — not at the end. If the session crashes or context compacts, the notes are already persisted.
2. **First file read** — when the agent works on a project folder, `notes.md` is the first thing it reads to restore context.
3. **Contains**:
   - Current state (what's done, what remains)
   - Decisions taken and their rationale
   - Technical patterns/conventions discovered (e.g., "style X uses tab at position Y")
   - Blockers or open questions
4. **Does NOT contain** transient data that belongs in live sources (dates, amounts, contact info → those live in NotebookLM/Notion/Gmail).
5. **Applies universally** across all knowledge spaces (`personal`, `work`, `forge`) and all project depths.

### Relationship to `memory-compass`

| `notes.md` (local to project folder) | `memory-compass` (global graph) |
|---------------------------------------|----------------------------------|
| Project-specific details and state | Cross-project user preferences |
| Decisions and progress tracking | Routing corrections and global patterns |
| Read only when working on THIS project | Consulted on any query for routing hints |

### Example structure

```
domains/carriere/opportunities/bnc-bedrock/notes.md   ← memory for BNC Bedrock
domains/demenagement/steering/11-baklog-actions.md     ← memory for déménagement
work/domains/novatech/notes.md                         ← memory for Novatech project
```


## Principle 11: Adresse de référence

À compter du **23 juin 2026**, l'adresse domicile est :

**2745 boulevard Roland-Therrien, Longueuil, QC J4M 1J5**
(Arrondissement : Vieux-Longueuil)

Toute recommandation impliquant une distance, un quartier, une appartenance municipale, ou un choix de service local DOIT être calculée par rapport à cette adresse. Cela inclut :
- Clubs et activités sportives des enfants
- Écoles, garderies, camps de jour
- Services municipaux (arrondissement Vieux-Longueuil)
- Commerces, cliniques, pharmacies
- Transport (distance en voiture et transport en commun)
- Évaluation foncière, taxes, collectes

Avant le 23 juin 2026, l'adresse précédente s'applique encore pour les décisions immédiates.


## Principle 10: Local Project Memory

Every project folder that involves iterative work (multiple sessions) MUST contain a `notes.md` file that serves as the **local working memory** for that project.

### Rules

1. **Updated during the session** — not at the end. If the session crashes or context compacts, the notes are already persisted.
2. **First file read** — when the agent works on a project folder, `notes.md` is the first thing it reads to restore context.
3. **Contains**:
   - Current state (what's done, what remains)
   - Decisions taken and their rationale
   - Technical patterns/conventions discovered (e.g., "style X uses tab at position Y")
   - Blockers or open questions
4. **Does NOT contain** transient data that belongs in live sources (dates, amounts, contact info → those live in NotebookLM/Notion/Gmail).
5. **Applies universally** across all knowledge spaces (`personal`, `work`, `forge`) and all project depths.

### Relationship to `memory-compass`

| `notes.md` (local to project folder) | `memory-compass` (global graph) |
|---------------------------------------|----------------------------------|
| Project-specific details and state | Cross-project user preferences |
| Decisions and progress tracking | Routing corrections and global patterns |
| Read only when working on THIS project | Consulted on any query for routing hints |

### Example structure

```
domains/carriere/opportunities/bnc-bedrock/notes.md   ← memory for BNC Bedrock
domains/demenagement/steering/11-baklog-actions.md     ← memory for déménagement
work/domains/novatech/notes.md                         ← memory for Novatech project
```


---

## Règle : Écriture Excel — Confirmation de fermeture obligatoire

**Déclencheur** : Toute opération d'ÉCRITURE sur un fichier Excel (write_data_to_excel, create_workbook, format_cells, create_chart, create_pivot_table, ou toute modification de contenu .xlsx).

**Action OBLIGATOIRE** : Avant d'exécuter l'écriture, l'agent DOIT :

1. Informer l'utilisateur : "Je dois modifier le fichier Excel. S'il est ouvert dans ton navigateur ou Dropbox, ferme-le d'abord pour éviter un conflit."
2. Demander confirmation : "Est-ce que le fichier est fermé ?"
3. Attendre une réponse positive (oui, yes, ok, c'est fait, fermé, etc.)
4. SEULEMENT ALORS procéder à l'écriture

**NE PAS appliquer pour** : les opérations de lecture seule (read_data_from_excel, list_sheets).

**JAMAIS** : écrire dans un fichier Excel sans avoir obtenu la confirmation de fermeture.


---

## Règle : Numéro de session actuelle

**Déclencheur** : L'utilisateur demande le numéro de session, l'ID de session, "quelle session", "session actuelle", "c'est quelle conversation".

**Action OBLIGATOIRE** : Exécuter cette commande et retourner le résultat :

```bash
sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT conversation_id FROM conversations_v2 ORDER BY updated_at DESC LIMIT 1"
```

**JAMAIS** : dire "je n'ai pas accès" ou demander à l'utilisateur de le faire lui-même.


---

## Règle : Recherche de session par sujet

**Déclencheur** : L'utilisateur demande "dans quelle session on a parlé de X", "tu te rappelles quand on a discuté de X", "retrouve la session où on a parlé de X", ou toute question visant à retrouver une conversation passée.

**Action OBLIGATOIRE (dans cet ordre)** :

1. **Cascading Search** (prioritaire) — utiliser l'outil `cascading_search` :
```
cascading_search(query="<sujet>", current_folder="<dossier courant>", current_agent="<nom agent actuel>")
```

2. **Si rien trouvé → fallback SQLite** :
```bash
sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT conversation_id, updated_at, substr(json_extract(value, '$.history[0].user.content'), 1, 120) FROM conversations_v2 WHERE value LIKE '%<sujet>%' ORDER BY updated_at DESC LIMIT 5"
```

3. **Retourner** : session ID + extrait du contenu + date pour chaque résultat trouvé.

**JAMAIS** : répondre "je ne me rappelle pas" ou "je n'ai pas cette information" sans avoir exécuté les deux étapes ci-dessus.


---

## Règle d'or : Communication inter-agents via le filesystem

**Source** : [aws-samples/sample-kiro-cli-multiagent-development](https://github.com/aws-samples/sample-kiro-cli-multiagent-development) — l'architect écrit les specs dans des fichiers, les subagents lisent et écrivent leurs résultats dans des fichiers. Le filesystem est le canal officiel.

**Principe** : Quand un agent délègue via `use_subagent`, les résultats complets transitent par un FICHIER — jamais uniquement par le résumé du subagent.

### Flux obligatoire (3 étapes)

**Étape 1 — L'agent principal construit la query avec un chemin de fichier unique** :

Format du nom de fichier : `/tmp/subagent-<agent-cible>-<YYYYMMDD-HHMMSS>.md`

```json
{
  "command": "InvokeSubagents",
  "content": {
    "subagents": [{
      "query": "<description de la tâche>. IMPORTANT: Écris le résultat COMPLET (tous les détails, liens, tableaux, données brutes) dans /tmp/subagent-<agent>-<timestamp>.md PUIS résume les points clés dans ta réponse.",
      "agent_name": "<agent-cible>"
    }]
  }
}
```

**Étape 2 — L'agent principal lit le fichier après le retour du subagent** :

```
fs_read /tmp/subagent-<agent>-<timestamp>.md
```

**Étape 3 — L'agent principal présente le contenu COMPLET à l'utilisateur puis supprime le fichier** :

```bash
rm /tmp/subagent-<agent>-<timestamp>.md
```

### Règles strictes

- **JAMAIS** présenter uniquement le résumé du subagent à l'utilisateur
- **JAMAIS** utiliser un nom de fichier fixe (risque d'écrasement) — toujours inclure un timestamp
- **TOUJOURS** lire le fichier après le retour du subagent pour récupérer les données complètes
- **TOUJOURS** supprimer le fichier après lecture (nettoyage)
- **TOUJOURS** informer l'utilisateur si le fichier est vide ou absent (le subagent a peut-être échoué)

### Exemple concret

Compass veut chercher sur Marketplace via connect2 :

```json
{
  "query": "Cherche sur Facebook Marketplace (rayon 50 km de Longueuil) les annonces des 10 derniers jours pour 'tapis marocain'. Affiche prix, titre, lieu, lien direct. IMPORTANT: Écris le résultat COMPLET dans /tmp/subagent-connect2-20260712-071900.md PUIS résume les points clés.",
  "agent_name": "connect2"
}
```

Compass lit ensuite `/tmp/subagent-connect2-20260712-071900.md` et affiche les résultats complets (avec les liens).


---

## Règle d'or : Mise à jour obligatoire du diagramme d'architecture

**Déclencheur** : Toute modification de la structure des agents — création, suppression, renommage d'un agent, ajout/retrait d'un serveur MCP sur un agent.

**Action OBLIGATOIRE** : Mettre à jour `docs/architecture-globale-agents.drawio` pour refléter le changement.

**JAMAIS** : créer/modifier un agent sans mettre à jour le diagramme draw.io.
**TOUJOURS** : le diagramme doit être le miroir exact de l'état réel des agents et de leurs MCPs.
