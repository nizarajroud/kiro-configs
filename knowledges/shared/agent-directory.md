---
inclusion: always
---
# Agent Directory — Annuaire des agents disponibles

## Règle

Quand un agent reçoit une requête qui ne fait PAS partie de son domaine, il DOIT :
1. **Vérifier d'abord ses propres outils** — si le MCP nécessaire est configuré sur lui-même, l'utiliser DIRECTEMENT (tool call = millisecondes). Ne JAMAIS déléguer un outil que tu possèdes déjà.
2. **Déléguer via `use_subagent`** à l'agent spécialisé UNIQUEMENT si tu n'as PAS l'outil nécessaire (spawn temporaire → résultat retourné)
3. Si `use_subagent` n'est pas disponible, informer l'utilisateur et indiquer : `/agent swap <nom>`
4. Ne PAS tenter de faire le travail lui-même s'il n'a pas les outils

## Mécanisme de délégation (OBLIGATOIRE)

Utiliser `use_subagent` avec `agent_name` :

```json
{
  "command": "InvokeSubagents",
  "content": {
    "subagents": [{
      "query": "<description claire de la tâche>",
      "agent_name": "<nom de l'agent cible>"
    }]
  }
}
```

Le subagent exécute la tâche avec ses propres MCPs, retourne le résultat, puis est détruit. L'agent principal reste actif et transmet le résultat à l'utilisateur.

**RÈGLE ABSOLUE** : JAMAIS demander à l'utilisateur "tu veux que je spawne X?" ou "tu veux que je délègue?". Si la requête concerne un autre agent selon la matrice ci-dessous, spawner DIRECTEMENT sans poser de question. L'utilisateur attend un résultat, pas une question de routage.

**RÈGLE DE COMMUNICATION** : Toute délégation via `use_subagent` DOIT suivre le pattern filesystem (voir `data-principles.md` — "Règle d'or : Communication inter-agents") :
1. Inclure dans la query : "Écris le résultat COMPLET dans `/tmp/subagent-<agent>-<YYYYMMDD-HHMMSS>.md`"
2. Après retour du subagent : lire le fichier (`fs_read`)
3. Présenter le contenu COMPLET à l'utilisateur
4. Supprimer le fichier

## Agents actifs

| Agent | Domaine | MCPs | Quand l'utiliser |
|-------|---------|------|-----------------|
| **it-supervisor** | Orchestration globale | 13 actifs | Agent par défaut — route, gère la config, vue d'ensemble |
| **exp2** | Travail technique | 24 actifs + 18 désactivés | AWS, code, CI/CD, Terraform, diagrammes, LinkedIn, WhatsApp, SSH |
| **compass** | Vie personnelle | 14 actifs + 6 désactivés | Famille, finances, santé, admin, Gmail, Telegram, Marketplace |
| **forge** | Outillage | 13 actifs | Installer un MCP, découvrir un outil, expérimenter, documenter |
| **light** | Usage rapide | 13 actifs | Recherches rapides, mémoire, docs — démarrage léger |
| **media1** | Génération media | 1 actif | TTS, audio, future: video/image |
| **sandbox** | Test isolé | 8+9 | Banc d'essai MCP — préparé par Forge avant test |

## MCPs cross-cutting (disponibles sur tous les agents domaine via global)

| MCP | Description |
|-----|-------------|
| notion-workspace | Pages & databases Notion |
| github | Repos, PRs, issues |
| firecrawl | Web scraping & search |
| bookmarks | Chrome & Edge bookmarks |
| agentcore-memory | Mémoire cross-session |
| remote.aws-knowledge | Documentation AWS |
| mcp-image-recognition | Analyse d'images |
| sequential-thinking | Raisonnement structuré |
| time | Heure & timezone |
| fetch | Téléchargement URLs |

## Matrice de redirection

| Tu es... | La requête concerne... | Délègue à... |
|----------|----------------------|-----------------|
| exp2 | Famille, finances, santé, déménagement | **compass** |
| exp2 | Installation MCP, recherche d'outil | **forge** |
| compass | Code, AWS, infrastructure, projet pro | **exp2** |
| compass | Installation MCP | **forge** |
| forge | Code, AWS, projet client | **exp2** |
| forge | Vie personnelle | **compass** |

## MCPs désactivés (toggle via `qq --mcp`)

Les agents domaine contiennent aussi des MCPs désactivés — activables à la demande sans modifier les fichiers manuellement :
- **Compass** : perplexity, xpoz-mcp, apify-mcp, mcp-canada, architecture-mcp, markdown2pdf
- **Exp2** : ssh-csben-*, bedrock-*, chrome-tools, codebase-memory, playwright, n8n, idea, lza, airtable, image-annotator, youtube-transcript

## Mise à jour

Ce fichier est mis à jour par **it-supervisor** à chaque ajout ou retrait d'un agent.
