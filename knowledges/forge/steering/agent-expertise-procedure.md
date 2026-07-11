---
inclusion: always
---
# Procédure de création d'un agent expertise (worker)

## Principes fondamentaux

- Les agents **domaine** (IT-Supervisor, Compass, Exp2, Forge, Light) sont permanents — ils ont un contexte, une mémoire, un périmètre
- Les agents **expertise** (connect1, connect2, data1, aws1, diagram1, dev1, etc.) sont des workers éphémères au service des agents domaine
- Un agent expertise est **spawné via `use_subagent`**, exécute la tâche, retourne le résultat, puis est **détruit**

## Règles des agents expertise

1. **Pas de mémoire** — stateless, pas de `memory-*.jsonl` (AWS best practice : workers are stateless)
2. **Max 5 MCPs** par agent (recommandation AWS AGENTPERF05-BP02)
3. **`useLegacyMcpJson: false`** — n'hérite PAS des serveurs globaux
4. **Pas de resources knowledges** sauf `knowledges/shared/*.md` (pour connaître l'annuaire des agents)
5. **Prompt focalisé** — uniquement le routing de ses propres outils, pas de logique de domaine

## Procédure de création (6 étapes)

### Étape 1 — Créer `agents/<nom>.json`

```json
{
  "name": "<nom>",
  "description": "<description courte>",
  "prompt": "file://../prompts/<nom>-prompt.md",
  "mcpServers": { ... },
  "tools": ["*"],
  "allowedTools": ["fs_read", "grep", "glob", "@mcp1", "@mcp2", ...],
  "useLegacyMcpJson": false,
  "resources": ["file:///home/nizar/HomeWspce/kiro-configs/knowledges/shared/*.md"],
  "hooks": {},
  "toolsSettings": {}
}
```

### Étape 2 — Créer `prompts/<nom>-prompt.md`

Structure AWS best practices :
- IDENTITY (rôle, expertise, personnalité, langue)
- CORE MISSION (ce qu'il fait)
- TOOL ROUTING (1 section par MCP)
- RESTRICTIONS (NEVER / ALWAYS)
- SUCCESS/FAILURE CRITERIA
- ESCALATION

### Étape 3 — Créer `knowledges/<nom>/config/domains.yaml`

Keywords pour le routage superviseur. Le superviseur (IT-Supervisor) utilise ces keywords pour décider quel agent spawner.

### Étape 4 — Retirer les MCPs des emplacements précédents

- Retirer de `settings/mcp.json` (global) si présent
- Retirer de l'agent domaine qui les avait (exp2, compass, etc.)
- Vérifier : zéro duplication (un MCP = un seul agent)

### Étape 5 — Mettre à jour `agents/it-supervisor.json`

Ajouter `file:///.../knowledges/<nom>/config/domains.yaml` dans les resources du superviseur.

### Étape 6 — Mettre à jour `knowledges/shared/agent-directory.md`

- Ajouter le nouvel agent dans la table des agents actifs
- Mettre à jour la matrice de délégation (qui délègue quoi à ce nouvel agent)

## Catégories existantes

| Catégorie | Agents | Thème |
|-----------|--------|-------|
| **connect** | connect1, connect2 | Communication externe (social, messaging, SSH, marketplace) |
| **aws** | (à créer) | Infrastructure cloud AWS |
| **diagram** | (à créer) | Visualisation et diagrammes |
| **dev** | (à créer) | Développement, IaC, code |
| **data** | (à créer) | Données, documents, recherche |

Si un agent d'une catégorie atteint 5+ MCPs → créer un nouvel agent dans la même catégorie (ex: connect3, aws2).

## Vérification finale (checklist)

- [ ] Agent JSON créé avec `useLegacyMcpJson: false`
- [ ] Prompt créé (structure AWS best practices)
- [ ] `domains.yaml` créé avec keywords
- [ ] MCPs retirés des emplacements précédents (zéro duplication)
- [ ] IT-Supervisor mis à jour (resources)
- [ ] Agent-directory mis à jour (table + matrice)
- [ ] PAS de mémoire ajoutée (worker stateless)
- [ ] Sandbox alimenté (copier la config du nouveau MCP dans `agents/sandbox.json` pour test isolé immédiat)

## Alimentation du sandbox (après chaque installation)

Après l'étape 6, copier la config du nouveau MCP dans `agents/sandbox.json` (qui doit être vide). L'utilisateur peut ensuite `/agent swap sandbox` pour valider le fonctionnement en isolation.

Après validation, remettre `"mcpServers": {}` dans sandbox.json (nettoyage).
