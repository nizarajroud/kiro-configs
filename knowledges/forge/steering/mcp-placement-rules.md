---
inclusion: always
---
# MCP Placement Rules — Routing Matrix & Capacity Management

> Detailed rules for deciding which agent receives a newly installed MCP server.
> Referenced by the MCP PLACEMENT PROCEDURE in forge-prompt.md.

## 1. Routing Matrix

| MCP Category | Keywords | Target Agent | Rationale |
|---|---|---|---|
| Social networks | LinkedIn, profil, emploi, réseau pro | **connect1** | Social/external communication |
| Video/Audio remote | YouTube, transcript, vidéo, audio URL | **connect1** | Media content via remote APIs |
| SSH/Remote access | SSH, remote server, machine distante | **connect1** | Remote connectivity |
| Google services | Google Maps, itinéraire, météo | **connect1** | Google ecosystem |
| Messaging | Telegram, WhatsApp (si migré) | **connect2** | Direct messaging |
| Email/Calendar | Gmail, mail, calendrier, RDV | **connect2** | Communication directe |
| Web search | recherche web, actualité, Perplexity | **connect2** | Web research |
| Marketplace | Facebook Marketplace, eBay, occasion | **connect2** | Secondhand commerce |
| AWS services | EKS, S3, Lambda, CloudWatch, Bedrock | **exp2** (→ aws1 si créé) | Infrastructure cloud |
| Infrastructure | Terraform, CDK, CloudFormation | **exp2** (→ aws1 si créé) | IaC |
| Code repos | GitHub, GitLab, Bitbucket, CI/CD | **exp2** (→ dev1 si créé) | Development workflow |
| Diagrams | Excalidraw, Mermaid, draw.io, Graphviz | **exp2** (→ diagram1 si créé) | Visual architecture |
| Data/spreadsheets | Excel, Airtable, bases de données | **compass** (→ data1 si créé) | Données structurées |
| Personal tools | TickTick, NotebookLM, bookmarks | **compass** | Vie personnelle |
| Notion | Notion workspace | **it-supervisor** ou agent qui l'utilise le plus | Cross-cutting |
| Utilities | time, fetch, memory | **light** | Utilitaires légers |
| Transcription locale | Whisper, audio local, fichier MP3/MP4 | **connect1** ou agent dédié | Media processing |

## 2. Capacity Rules

### Hard limit : 5 MCPs actifs par agent

- Compter UNIQUEMENT les MCPs avec `"disabled": false`
- Les MCPs de mémoire (`memory-*`) et `agentcore-memory` ne comptent PAS dans la limite (infrastructure)
- Les MCPs utilitaires partagés (`sequential-thinking`, `time`) comptent

### Quand la limite est atteinte

1. Proposer la création d'un agent sibling :
   - `connect1` plein → créer `connect3`
   - `exp2` plein → créer `aws1` ou `dev1` selon le type de MCP
   - `compass` plein → créer `data1`
2. Le nouvel agent hérite :
   - D'un sous-ensemble des keywords du parent
   - D'un prompt structuré (IDENTITY → MISSION → ROUTING → RULES)
   - De sa propre mémoire (`memories/memory-<name>.jsonl`)
3. Mettre à jour `agent-directory.md` avec le nouvel agent

## 3. Cross-cutting MCPs (exception à la règle)

Certains MCPs sont utilisés par **3+ agents** et ne doivent PAS être placés sur un seul agent :

| MCP | Pourquoi cross-cutting | Solution |
|---|---|---|
| `notion-workspace` | Tous les agents écrivent dans Notion | Garder dans chaque agent qui l'utilise |
| `firecrawl` | Recherche web universelle | Garder dans les agents qui en ont besoin |
| `sequential-thinking` | Utilitaire de raisonnement | Garder partout où c'est utile |
| `agentcore-memory` | Mémoire cross-session | Infrastructure — partout |

Pour ces MCPs, on les définit **dans chaque agent JSON individuellement** (pas de `useLegacyMcpJson`).

## 4. Communication Protocol

### Source unique de vérité

`knowledges/shared/agent-directory.md` est le SEUL fichier qui communique les changements de scope entre agents.

### Workflow post-placement

1. Forge place le MCP sur l'agent cible (JSON + domains.yaml + prompt)
2. Forge met à jour `agent-directory.md` (description + matrice)
3. Tous les autres agents verront automatiquement le changement au prochain démarrage de session (car `agent-directory.md` est `inclusion: always` dans shared/)

### Ce que Forge ne fait PAS

- ❌ Modifier le prompt d'un agent pour ajouter des règles de délégation vers le nouveau MCP
- ❌ Modifier les resources d'autres agents
- ❌ Notifier manuellement chaque agent — `agent-directory.md` fait ce travail

## 5. Décision Flowchart

```
Nouveau MCP installé et validé (Step 6 ✅)
    │
    ▼
Lire agent-directory.md + tous domains.yaml
    │
    ▼
Le MCP matche un agent existant ?
    │
    ├── OUI → L'agent a < 5 MCPs actifs ?
    │           │
    │           ├── OUI → Placer sur cet agent (Step 9)
    │           │
    │           └── NON → Proposer sibling agent
    │
    └── NON → Le MCP est cross-cutting (3+ agents) ?
                │
                ├── OUI → Placer sur chaque agent qui en a besoin
                │
                └── NON → Proposer création d'un nouvel agent spécialisé
```

---

*Dernière mise à jour : 2026-07-10 par Forge*
