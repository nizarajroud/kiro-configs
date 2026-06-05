---
inclusion: always
---
# Kiro-Configs — Conventions & Bonnes Pratiques

> Conventions de nommage, cycle de vie des agents, règles de mémoire, et bonnes pratiques.
> Complément au document d'architecture maître. Maintenu par IT-Supervisor.

## 1. Conventions de nommage

### 1.1 Agents

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Fichier agent | `<nom-agent>.json` (lowercase, hyphenated) | `it-supervisor.json` |
| Champ `name` | Identique au nom de fichier (sans .json) | `"name": "it-supervisor"` |
| Prompt lié | `prompts/<nom-agent>-prompt.md` | `prompts/it-supervisor-prompt.md` |
| CAO profile | `cao-profiles/<nom-agent>.md` | `cao-profiles/compass.md` |
| Mémoire | `memories/memory-<nom-agent>.jsonl` | `memories/memory-compass.jsonl` |
| MCP memory key | `memory-<nom-agent>` | `"memory-supervisor"` |

**Règle** : Un agent = 1 fichier JSON + 1 prompt .md + (optionnel) 1 CAO profile + 1 mémoire JSONL. Les noms DOIVENT correspondre.

### 1.2 MCP Servers

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Clé JSON dans mcp.json | lowercase, hyphenated | `"notion-workspace"` |
| Wrapper | `wrappers/<name>_wrapper.py` (underscore) | `wrappers/gmail_wrapper.py` |
| Variables .env | `UPPER_SNAKE_CASE` avec préfixe du serveur | `FIRECRAWL_API_KEY` |
| Skill file | `knowledges/forge/domains/mcp-servers/<name>.md` | `mcp-servers/markitdown.md` |
| Description JSON | 1 phrase → QUAND l'utiliser + QUOI il fait | Obligatoire |

### 1.3 Knowledge Spaces

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Space name | singular, lowercase | `personal`, `work`, `forge` |
| Steering file | `knowledges/<space>/steering/<nom>.md` | `personal/steering/product.md` |
| Config | `knowledges/<space>/config/domains.yaml` | `work/config/domains.yaml` |
| Domain data | `knowledges/<space>/domains/<domain-name>/` | `personal/domains/finances/` |
| Skill files | lowercase, hyphenated, descriptif | `comptes-bancaires.md` |

### 1.4 Steering Files

| Élément | Convention |
|---------|-----------|
| Frontmatter | OBLIGATOIRE : `inclusion: always` |
| Nom de fichier | `<numéro-optionnel>-<nom-descriptif>.md` |
| Contenu | HOW (comment trouver), jamais WHAT (données factuelles) |
| Taille | Idéal < 200 lignes. Si plus → découper |

## 2. Structure obligatoire par Knowledge Space

Chaque space DOIT contenir exactement :

```
knowledges/<space>/
├── steering/
│   └── product.md          ← OBLIGATOIRE : identité + mission + scope
├── config/
│   └── domains.yaml        ← OBLIGATOIRE : taxonomie de mots-clés
└── domains/
    └── (au moins 1 dossier si le space a des données locales)
```

### Comparaison actuelle (audit) :

| Space | product.md | domains.yaml | Steering extras | Conforme ? |
|-------|:----------:|:------------:|:---------------:|:----------:|
| **personal** | ✅ | ✅ | architecture, sources-registry, query-routing | ✅ |
| **work** | ✅ | ✅ | tech, conventions | ✅ |
| **forge** | ✅ | ✅ | kiro-configs-architecture, conventions (ce fichier) | ✅ |
| **shared** | N/A | N/A | data-principles, output-rules | ✅ (cross-space) |

## 3. Cycle de vie d'un agent

### 3.1 Création

```
1. Créer agents/<nom>.json (schéma complet : name, description, prompt, tools, allowedTools, resources)
2. Créer prompts/<nom>-prompt.md (structure IDENTITY → MISSION → ROUTING → RULES)
3. Créer memories/memory-<nom>.jsonl (fichier vide initialement)
4. Si CAO requis → créer cao-profiles/<nom>.md
5. Ajouter au registre dans kiro-configs-architecture.md (section 3)
6. Valider la checklist de cohérence (architecture.md section 9)
```

### 3.2 Modification

```
1. Identifier le composant à modifier (agent, prompt, steering, memory)
2. Vérifier les impacts cross-composants (un prompt qui change peut nécessiter une mise à jour du CAO)
3. Appliquer le changement
4. Mettre à jour kiro-configs-architecture.md si la structure change
5. Re-valider la checklist de cohérence
```

### 3.3 Archivage (retrait)

```
1. Déplacer agents/<nom>.json → zzz/agents/<nom>.json
2. Déplacer prompts/<nom>-prompt.md → zzz/prompts/<nom>-prompt.md
3. Conserver la mémoire dans memories/ (ne pas supprimer — historique)
4. Mettre à jour kiro-configs-architecture.md (retirer de section 3)
5. Ajouter un commentaire dans zzz/ : date + raison du retrait
```

## 4. Bonnes pratiques — Mémoire (détaillé)

### 4.1 Format JSONL (memory-server)

Chaque ligne = un objet JSON. Deux types :

```jsonl
{"type":"entity","name":"Nom","entityType":"type","observations":["obs1","obs2"]}
{"type":"relation","from":"Entity1","to":"Entity2","relationType":"verb"}
```

### 4.2 Types d'entités recommandés

| entityType | Usage | Exemple |
|------------|-------|---------|
| `rule` | Règle métier validée par l'utilisateur | "Exhaustivité de recherche avant conclusion" |
| `routing_rule` | Correction de routing | "Santé → chercher d'abord Notion" |
| `person` | Personne avec contexte | Nizar, Abir, contacts |
| `suivi_famille` | Suivi d'un sujet famille | "Travail été Radwan 2026" |
| `suivi_sante` | Suivi médical | "Suivi Psychiatrie Radwan 2026" |
| `service_sante` | Service/institution santé | "GAP - Guichet d'accès" |
| `evenement_famille` | Événement planifié | "Fête XY 2028" |

### 4.3 Règles critiques

1. **JAMAIS écrire sans confirmation utilisateur** (validé 1er juin 2026)
2. **Max 50 entités par fichier** — au-delà, migrer vers steering files
3. **Pas de données factuelles temporaires** — uniquement des patterns stables
4. **Les `rule` sont les plus importantes** — ce sont les corrections de comportement
5. **Révision trimestrielle** — supprimer les entités obsolètes

### 4.4 Quand la mémoire vs quand un steering file

| Situation | Mémoire | Steering file |
|-----------|:-------:|:-------------:|
| Correction ponctuelle de routing | ✅ | |
| Préférence utilisateur | ✅ | |
| Règle complexe avec exemples | | ✅ |
| Architecture ou procédure | | ✅ |
| Info qui dépasse 3-4 lignes | | ✅ |
| Info utile à PLUSIEURS agents | | ✅ (dans shared/ ou forge/) |

## 5. Bonnes pratiques — System Prompts (détaillé)

### 5.1 Séparation des responsabilités

| Le prompt contient | Les steering files contiennent |
|-------------------|-------------------------------|
| Comportement (comment répondre) | Routing (où chercher) |
| Personnalité (ton, style) | Registre de sources (quels outils) |
| Règles DO/DON'T | Taxonomie des domaines |
| Format de réponse | Architecture technique |

### 5.2 Anti-patterns à éviter

| ❌ Anti-pattern | ✅ Bonne pratique |
|----------------|------------------|
| Mettre des données factuelles dans le prompt | → Données dans sources live ou domains/ |
| Prompt > 5000 mots | → Externaliser dans steering files |
| Dupliquer des règles entre agents | → Centraliser dans shared/ |
| Lister tous les MCP servers dans le prompt | → Référencer via steering file |
| Hardcoder des chemins absolus dans le prompt | → Les lire depuis resources |

### 5.3 Pattern de prompt optimal

```markdown
## IDENTITY          (5-10 lignes max — qui je suis)
## CORE MISSION      (tableau ou liste — quoi je fais)
## ROUTING LOGIC     (décision tree — comment je route)
## RESPONSE BEHAVIOR (5-10 lignes — style et format)
## MEMORY            (3-5 lignes — comment j'utilise ma mémoire)
## RULES             (10-15 rules max — DO/DON'T)
```

Ratio idéal : ~60% routing/mission, ~20% rules, ~20% identity+behavior.

## 6. Bonnes pratiques — Resources & Inclusion

### 6.1 Budget de contexte

Chaque fichier `inclusion: always` consomme du contexte à chaque session. Gérer avec parcimonie :

| Catégorie | Budget recommandé |
|-----------|:-----------------:|
| Shared (cross-space) | 2-3 fichiers max |
| Steering par space | 3-5 fichiers max |
| Config par space | 1 fichier (domains.yaml) |
| **Total always** | **~10-15 fichiers** |

### 6.2 Quand promouvoir un skill en steering

Un fichier dans `domains/` (skill, chargé à la demande) devrait migrer vers `steering/` (always) quand :
- Il est consulté à **presque chaque session**
- Il contient des **règles de routing** essentielles
- Sa taille est raisonnable (< 200 lignes)

### 6.3 Quand rétrograder un steering en skill

Un fichier dans `steering/` devrait migrer vers `domains/` quand :
- Il n'est pertinent que pour un **sous-domaine spécifique**
- Il contient des **données factuelles** plutôt que des règles
- Il est rarement consulté

## 7. Homogénéité inter-agents — Contrat commun

Tous les agents interactifs (it-supervisor, compass, exp2, forge) DOIVENT :

| Obligation | Comment |
|------------|---------|
| Charger `shared/*.md` | `"file:///...knowledges/shared/*.md"` dans resources |
| Avoir un prompt structuré | IDENTITY → MISSION → ROUTING → RULES |
| Citer leurs sources | Principe 3 (data-principles.md) |
| Respecter la timezone | America/Toronto (Principe 8) |
| Ne pas dupliquer de données | Principe 2 |
| Avoir une mémoire dédiée | `memories/memory-<nom>.jsonl` |

### Matrice de couverture (qui a accès à quoi)

| Agent | personal/ | work/ | forge/ | shared/ |
|-------|:---------:|:-----:|:------:|:-------:|
| **it-supervisor** | ✅ steering + skill | ✅ steering + skill | ✅ steering + skill | ✅ |
| **compass** | ✅ steering + skill | ❌ | ❌ | ✅ |
| **exp2** | ❌ | ✅ steering + skill | ❌ | ✅ |
| **forge** | ❌ | ❌ | ✅ steering + skill | ✅ |

→ **IT-Supervisor est le seul agent avec visibilité globale.** C'est lui le garant.

## 8. Procédure — Ajout d'un nouveau MCP Server

```
1. Évaluer si un wrapper est nécessaire (secret dans .env → OUI)
2. Créer wrappers/<name>_wrapper.py si besoin
3. Ajouter les secrets dans .env
4. Ajouter le bloc dans settings/mcp.json (avec description obligatoire)
5. Si le serveur est spécifique à un agent → l'ajouter dans agents/<nom>.json mcpServers
6. Créer knowledges/forge/domains/mcp-servers/<name>.md (skill file)
7. Valider : timeout 5 <command> 2>&1 | head
8. Mettre à jour kiro-configs-architecture.md section 7 (registre)
```

## 9. Procédure — Maintenance de la mémoire

### Nettoyage

```
1. Lire le fichier JSONL complet
2. Identifier les entités obsolètes (info devenue fausse, événement passé)
3. DEMANDER confirmation à l'utilisateur avant suppression
4. Supprimer via delete_entities ou delete_observations
5. Vérifier que le fichier reste < 50 entités
```

### Migration mémoire → steering file

Quand une entité de mémoire est trop complexe ou utile à plusieurs agents :

```
1. Créer un steering file dans le space approprié
2. Y transférer le contenu de l'entité (reformulé en règle claire)
3. Supprimer l'entité de la mémoire (avec confirmation)
4. Vérifier que le nouveau steering file est dans les resources de l'agent
```

---

*Dernière mise à jour : 2026-06-05 par IT-Supervisor*
