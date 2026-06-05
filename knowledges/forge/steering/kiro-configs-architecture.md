---
inclusion: always
---
# Kiro-Configs — Architecture Maître

> Document de référence unique pour la structure, les conventions et les responsabilités de tout le projet `kiro-configs/`. Maintenu par IT-Supervisor.

## 1. Vue d'ensemble

```
kiro-configs/                          ← Racine du projet
├── agents/                            ← Définitions JSON des agents (identité + outils + resources)
├── prompts/                           ← System prompts (.md) injectés dans les agents
├── cao-profiles/                      ← Profils pour le mode CAO (orchestration non-interactive)
├── knowledges/                        ← Savoirs structurés (steering + domains + config)
│   ├── shared/                        ← Règles cross-space (data-principles, output-rules)
│   ├── personal/                      ← Espace personnel (vie privée, famille, finances)
│   ├── work/                          ← Espace professionnel (Beneva, Alithya, mandats)
│   └── forge/                         ← Espace outillage (MCP, patterns, expériences)
├── settings/                          ← Configuration technique (mcp.json, cli.json, servers.yaml)
├── memories/                          ← Mémoire persistante JSONL par agent
├── wrappers/                          ← Scripts Python/Bash lanceurs de MCP servers
├── scripts/                           ← Scripts opérationnels (start/stop servers, deploy)
├── hooks/                             ← Hooks pre/post-exécution (sécurité, logging)
├── steering/                          ← Règles globales CLI (non-interactive, documentation)
├── credentials/                       ← Tokens OAuth (gitignored)
├── logs/                              ← Logs de debug (éphémère)
├── sessions/                          ← Historique conversations CLI (éphémère, auto-géré)
├── zzz/                               ← Archive d'anciens agents/prompts (obsolètes, référence)
├── powers/                            ← Registre de capacités (quasi vide, hérité)
├── skills/                            ← Réservé (vide, hérité)
└── .env                               ← Secrets (API keys, tokens) — JAMAIS commité
```

## 2. Contrat par type de fichier

### 2.1 `agents/*.json` — Définition d'agent

Chaque agent est défini par UN fichier JSON. C'est le **point d'entrée technique** qui lie tout.

| Champ | Obligatoire | Rôle |
|-------|:-----------:|------|
| `name` | ✅ | Identifiant unique (lowercase, hyphenated) |
| `description` | ✅ | 1 phrase : quoi + quand l'utiliser |
| `prompt` | ✅ | Chemin vers le system prompt (`file://../prompts/<name>-prompt.md`) |
| `mcpServers` | ⚠️ | Serveurs MCP propres à cet agent (ex: mémoire dédiée) |
| `tools` | ✅ | Liste des outils demandés |
| `allowedTools` | ✅ | Liste des outils effectivement autorisés |
| `resources` | ✅ | Fichiers chargés en contexte (steering, domains) |
| `useLegacyMcpJson` | ⚠️ | `true` = utilise `settings/mcp.json` global |
| `welcomeMessage` | ⚠️ | Message affiché au démarrage de session |

**Convention de nommage** : `<nom-agent>.json` (lowercase, hyphenated)

**Relation** : agent JSON → pointe vers → prompt .md + resources knowledges/

### 2.2 `prompts/*.md` — System Prompt

Le prompt définit le **comportement, la personnalité et les règles** de l'agent.

| Section | Obligatoire | Contenu |
|---------|:-----------:|---------|
| `## IDENTITY` | ✅ | Nom, rôle, scope, personnalité |
| `## KNOWLEDGE SPACES` ou `## CORE MISSION` | ✅ | Quels domaines couvre l'agent |
| `## ROUTING LOGIC` ou `## SOURCE ROUTING` | ✅ | Comment il choisit ses sources |
| `## RESPONSE BEHAVIOR` | ✅ | Style de réponse, langue, timezone |
| `## RULES` | ✅ | Contraintes (DO / DON'T) |
| `## MEMORY` | ⚠️ | Comment il utilise sa mémoire |

**Convention** : `<nom-agent>-prompt.md` (correspondance 1:1 avec l'agent JSON)

### 2.3 `cao-profiles/*.md` — Profil CAO (non-interactif)

Utilisé uniquement en mode **Supervisor → Worker** (orchestration multi-agent via CAO).

| Différence avec prompt | Explication |
|------------------------|-------------|
| Plus court | Le CAO a un contexte limité |
| Pas de welcomeMessage | Pas d'interaction directe |
| Contient des instructions de handoff | Comment répondre au supervisor |

**Agents actuels avec CAO** : supervisor, exp2, compass, forge

### 2.4 `knowledges/` — Structure obligatoire par espace

Chaque knowledge space DOIT suivre cette structure :

```
knowledges/<space>/
├── steering/          ← Règles et contexte (inclusion: always)
│   └── product.md    ← OBLIGATOIRE : identité et mission de l'espace
├── config/
│   └── domains.yaml  ← OBLIGATOIRE : taxonomie des domaines
└── domains/           ← Données locales qui n'ont pas d'autre home
    └── <domain>/      ← Un dossier par domaine actif
```

#### Rôle de chaque sous-dossier :

| Dossier | Inclusion | Rôle | Contenu permis |
|---------|-----------|------|----------------|
| `steering/` | `always` (chargé à chaque session) | Règles, routing, architecture, principes | Uniquement du HOW (comment trouver), jamais du WHAT (données factuelles) |
| `config/` | `always` | Taxonomie et métadonnées | `domains.yaml` = mots-clés de routing |
| `domains/` | `skill` (chargé à la demande) | Données locales sans autre home | Données qui n'existent NI dans Notion, NI dans NotebookLM, NI ailleurs |

#### `shared/` — L'espace transversal

| Fichier | Rôle |
|---------|------|
| `data-principles.md` | Les 10 principes fondamentaux (s'appliquent à TOUS les agents) |
| `output-rules.md` | Règles de formatage de sortie (tunisien/RTL, liens Notion) |

**Règle** : Si une règle s'applique à PLUS d'un space → elle va dans `shared/`.

### 2.5 `settings/mcp.json` — Registre MCP global

Contient TOUS les MCP servers configurés. Les agents avec `useLegacyMcpJson: true` héritent de ce registre.

| Champ par serveur | Obligatoire | Rôle |
|-------------------|:-----------:|------|
| `description` | ✅ | Quand et pourquoi utiliser ce serveur |
| `command` | ✅ | Commande de lancement |
| `args` | ✅ | Arguments |
| `env` | ⚠️ | Variables d'environnement (⚠️ `${VAR}` ne lit PAS .env — utiliser un wrapper) |
| `disabled` | ✅ | `true` = serveur OFF |
| `locked` | ⚠️ | `true` = ne pas modifier automatiquement |

### 2.6 `memories/*.jsonl` — Mémoire persistante

Un fichier JSONL par agent. Contient des entités + relations (format `@modelcontextprotocol/server-memory`).

| Mémoire | Agent | Contenu |
|---------|-------|---------|
| `memory-compass.jsonl` | compass (→ hérité par it-supervisor) | Routing corrections, préférences user, infos apprises |
| `memory-exp2.jsonl` | exp2 | Contexte technique, décisions de projet |
| `memory-forge.jsonl` | forge | Découvertes, verdicts, installations |
| `memory-supervisor.jsonl` | it-supervisor | Patterns cross-space, délégations |

**Bonnes pratiques mémoire** : voir section 4.

### 2.7 `wrappers/` — Lanceurs MCP

Scripts qui chargent les secrets depuis `.env` puis `execvp` le serveur MCP.

**Quand créer un wrapper** : dès qu'un serveur a besoin d'un secret ou d'une config dynamique.

**Convention** : `<server-name>_wrapper.py` ou `.sh`

### 2.8 `steering/` (racine) — Règles globales CLI

| Fichier | Rôle |
|---------|------|
| `non-interactive.md` | Toute commande doit être non-interactive (flags -y, etc.) |
| `documentation.md` | Exigences de documentation pour tout changement |

**⚠️ Différent de** `knowledges/*/steering/` : la racine `steering/` contient des règles **d'exécution CLI**, pas des règles de **routing de requêtes**.

### 2.9 `hooks/` — Scripts pre/post-exécution

| Hook | Rôle |
|------|------|
| `guard-destructive-commands.sh` | Bloque les commandes dangereuses |
| `check-secrets.sh` | Empêche la fuite de secrets dans les commits |
| `flywheel-log.sh` | Logging des actions |

### 2.10 `zzz/` — Archive

Anciens agents et prompts obsolètes, conservés pour référence historique.

**Règle** : Quand un agent est retiré → déplacer ses fichiers dans `zzz/` avec un commentaire date/raison.

## 3. Agents actifs — Cartographie

| Agent | Mode | Prompt | Mémoire | Scope |
|-------|------|--------|---------|-------|
| **it-supervisor** | Interactif | `it-supervisor-prompt.md` | `memory-supervisor.jsonl` | Tout (personal + work + forge) |
| **compass** | Interactif + CAO | `compass-prompt.md` | `memory-compass.jsonl` | Personal life |
| **exp2** | Interactif + CAO | `exp2-prompt.md` | `memory-exp2.jsonl` | Work (technique, cloud, code) |
| **forge** | Interactif + CAO | `forge-prompt.md` | `memory-forge.jsonl` | Tooling, MCP, discovery |
| **supervisor** | CAO uniquement | (inline dans cao-profiles) | — | Orchestrateur multi-agent |
| **code_supervisor** | Interactif | (embedded) | — | Code review/dev |
| **developer** | Interactif | (embedded) | — | Développement pur |
| **light** | Interactif | (embedded) | — | Agent léger (moins de tools) |

## 4. Bonnes pratiques — Mémoire

### Quand écrire en mémoire

| ✅ Écrire | ❌ Ne PAS écrire |
|-----------|------------------|
| Correction de routing validée par l'utilisateur | Données factuelles (dates, montants) → live sources |
| Préférence utilisateur confirmée | Info temporaire (sera obsolète demain) |
| Règle métier découverte et confirmée | Hypothèses non validées |
| Pattern de recherche qui a marché | Contenu volumineux (utiliser steering files) |

### Règle d'or
> **JAMAIS écrire en mémoire sans confirmation EXPLICITE de l'utilisateur.**

### Taille et maintenance
- Max ~50 entités par mémoire (au-delà → migrer vers steering files)
- Réviser trimestriellement : supprimer les entités devenues obsolètes
- Les entités de type `rule` sont prioritaires (chargées en premier)

## 5. Bonnes pratiques — System Prompts

### Structure recommandée

```markdown
## IDENTITY
[Qui je suis, 3-4 lignes max]

## CORE MISSION / KNOWLEDGE SPACES
[Quoi je fais, tableau si plusieurs espaces]

## ROUTING LOGIC / SOURCE ROUTING
[Comment je choisis les sources]

## RESPONSE BEHAVIOR
[Style, langue, timezone, citations]

## MEMORY
[Comment j'utilise ma mémoire]

## RULES
[DO / DON'T — liste courte et percutante]
```

### Limites de taille
- Prompt idéal : 1500-3000 mots
- Max absolu : 5000 mots (au-delà, le modèle perd le focus)
- Si le prompt dépasse → externaliser dans des steering files (inclusion: always)

### Principes
- Le prompt contient les RÈGLES DE COMPORTEMENT
- Les steering files contiennent les DONNÉES DE ROUTING et le CONTEXTE
- Jamais de données factuelles dans un prompt (pas de dates, pas de noms, pas de montants)

## 6. Bonnes pratiques — Resources (inclusion)

### Deux modes d'inclusion

| Mode | Syntaxe dans agent JSON | Comportement |
|------|------------------------|--------------|
| **always** | `"file:///path/*.md"` | Chargé à CHAQUE session dans le contexte |
| **skill** | `"skill:///path/**/*.md"` | Chargé à la DEMANDE (l'agent le lit quand pertinent) |

### Règles d'inclusion

- `steering/` et `config/` → toujours `file://` (always)
- `domains/` → toujours `skill://` (à la demande)
- `shared/` → toujours `file://` (always, cross-space)

### Frontmatter des steering files

```yaml
---
inclusion: always
---
```

Ce frontmatter est un indicateur pour l'humain et les outils. Le vrai mécanisme d'inclusion est dans le `resources` du agent JSON.

## 7. Registre des MCP Servers

### Serveurs actifs (settings/mcp.json)

| Serveur | Rôle | Wrapper | Cible |
|---------|------|---------|-------|
| `notion-workspace` | Pages & databases Notion | Non | local |
| `notebooklm` | RAG notebooks Google | Non | local |
| `ticktick` | Tasks & habits | ticktick_wrapper.py | local |
| `gmail` | Emails & Calendar | gmail_wrapper.py | local |
| `telegram` | Messages Telegram | Non | local |
| `airtable` | Bases relationnelles | Non | local |
| `excel` | Fichiers .xlsx | Non | local |
| `firecrawl` | Web scraping & search | firecrawl_wrapper.py | local |
| `bookmarks` | Chrome & Edge bookmarks | bookmarks_wrapper.py | local |
| `markitdown` | Conversion documents → MD | Non | local |
| `remote.aws-knowledge` | Docs AWS officiels | Non | local (remote API) |
| `mcp-mermaid` | Génération diagrammes | Non | local |
| `context7` | Docs live de librairies | Non | local |
| `github` | Repos, PRs, Actions | github_wrapper.py | local |
| `memory-*` | Mémoire persistante par agent | Non | local |
| `cao-mcp-server` | Orchestration multi-agent | Non | local |

### Serveurs désactivés

| Serveur | Raison |
|---------|--------|
| `alithya-knowledge-rag` | PC Alithya éteint / indisponible |
| `pdf-reader` | Remplacé par markitdown |
| `whatsapp` | En cours de configuration |
| `claude-cli` | Remote désactivé |

## 8. Flux d'exécution — Comment une requête traverse le système

```
Utilisateur → Kiro CLI
    ↓
Agent JSON chargé (it-supervisor.json)
    ↓
Resources chargées en contexte:
  - shared/*.md (data-principles, output-rules)
  - knowledges/<space>/steering/*.md (routing, product, etc.)
  - knowledges/<space>/config/domains.yaml
    ↓
System prompt injecté (it-supervisor-prompt.md)
    ↓
Mémoire lue (memory-supervisor.jsonl)
    ↓
Agent classifie la requête → routing vers sources
    ↓
Outils MCP appelés (live queries)
    ↓
Réponse synthétisée avec citations
```

## 9. Responsabilité de maintenance — IT-Supervisor

En tant que garant de ce système, je DOIS :

1. **Vérifier la cohérence** quand un agent/prompt/server est ajouté ou modifié
2. **Mettre à jour CE fichier** quand la structure change
3. **Signaler les incohérences** (ex: un agent pointe vers un prompt inexistant)
4. **Proposer le refactoring** quand un pattern se répète inutilement
5. **Valider l'homogénéité** entre espaces (même structure steering/ dans chaque space)

### Checklist de cohérence (à vérifier à chaque modification)

- [ ] L'agent JSON a un prompt correspondant dans `prompts/`
- [ ] Le prompt suit la structure standard (IDENTITY, MISSION, ROUTING, RULES)
- [ ] Les resources pointent vers des fichiers qui existent
- [ ] Les MCP servers référencés sont dans `settings/mcp.json`
- [ ] Les wrappers référencés existent dans `wrappers/`
- [ ] Le knowledge space de l'agent a `steering/product.md` + `config/domains.yaml`
- [ ] Les secrets nécessaires sont dans `.env`
- [ ] Si l'agent a une mémoire dédiée, le fichier JSONL existe dans `memories/`

---

*Dernière mise à jour : 2026-06-05 par IT-Supervisor*
