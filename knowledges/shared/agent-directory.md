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

| Agent | Domaine | Quand l'utiliser |
|-------|---------|-----------------|
| **it-supervisor** | Tout (orchestration) | Agent par défaut — route vers les autres, gère la config |
| **exp2** | Travail technique/professionnel | AWS, infrastructure, code, CI/CD, diagrammes, Terraform, EKS, projets clients |
| **compass** | Vie personnelle | Famille, finances, déménagement, santé, admin, abonnements, identité |
| **forge** | Outillage et découverte | Installer un serveur MCP, découvrir un outil, expérimenter, documenter |
| **light** | Usage léger et rapide | Recherches rapides, mémoire, docs, GitHub — démarrage ultra-rapide |
| **sandbox** | Test isolé de serveurs MCP | Banc d'essai — 1 MCP temporaire à la fois, toujours vide par défaut |
| **media1** | Génération/traitement media | TTS recording (audio to file), future: video processing, image generation |

## MCPs cross-cutting (disponibles sur tous les agents domaine)

| MCP                    | Description                                         | Agents                                          |
|------------------------|-----------------------------------------------------|-------------------------------------------------|
| notion-workspace       | Pages & databases Notion                            | it-supervisor, compass, exp2, forge, light      |
| github                 | Repos, PRs, issues                                  | it-supervisor, compass, exp2, forge, light      |
| firecrawl              | Web scraping & search                               | it-supervisor, compass, exp2, forge, light      |
| bookmarks              | Chrome & Edge bookmarks                             | it-supervisor, compass, exp2, forge, light      |
| agentcore-memory       | Mémoire cross-session                               | it-supervisor, forge, light                     |
| remote.aws-knowledge   | Documentation AWS                                   | it-supervisor, exp2, forge, light               |
| mcp-image-recognition  | Analyse d'images (Bedrock)                          | it-supervisor, exp2, forge, light               |
| sequential-thinking    | Raisonnement structuré                              | it-supervisor, forge, light                     |

## Matrice de redirection

Si tu reçois une requête hors de ton domaine, délègue via `use_subagent` :

| Tu es... | La requête concerne... | Délègue à... |
|----------|----------------------|-----------------|
| exp2 | Famille, finances, santé, déménagement | **compass** |
| exp2 | Installation MCP, recherche d'outil | **forge** |
| compass | Code, AWS, infrastructure, projet pro | **exp2** |
| compass | Installation MCP | **forge** |
| forge | Code, AWS, projet client | **exp2** |
| forge | Vie personnelle | **compass** |

## Exemple de délégation

Agent exp2 reçoit "montre-moi mes posts LinkedIn récents" :

```json
{
  "command": "InvokeSubagents",
  "content": {
    "subagents": [{
      "query": "Liste les 3 derniers posts LinkedIn de l'utilisateur",
      "agent_name": "connect1"
    }]
  }
}
```

→ connect1 démarre avec ses MCPs (linkedin-mcp), exécute la requête, retourne le résultat à exp2, puis est détruit.

## Mise à jour

Ce fichier est mis à jour par **it-supervisor** à chaque ajout ou retrait d'un agent.
