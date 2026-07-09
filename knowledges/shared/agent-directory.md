---
inclusion: always
---
# Agent Directory — Annuaire des agents disponibles

## Règle

Quand un agent reçoit une requête qui ne fait PAS partie de son domaine, il DOIT :
1. **Déléguer via `use_subagent`** à l'agent spécialisé (spawn temporaire → résultat retourné)
2. Si `use_subagent` n'est pas disponible, informer l'utilisateur et indiquer : `/agent swap <nom>`
3. Ne PAS tenter de faire le travail lui-même s'il n'a pas les outils

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

## Agents actifs

| Agent | Domaine | Quand l'utiliser |
|-------|---------|-----------------|
| **it-supervisor** | Tout (orchestration) | Agent par défaut — route vers les autres, gère la config |
| **exp2** | Travail technique/professionnel | AWS, infrastructure, code, CI/CD, diagrammes, Terraform, EKS, projets clients |
| **compass** | Vie personnelle | Famille, finances, déménagement, santé, admin, abonnements, identité |
| **forge** | Outillage et découverte | Installer un serveur MCP, découvrir un outil, expérimenter, documenter |
| **connect** | Communication externe et social | LinkedIn, WhatsApp, Google Maps, YouTube transcripts |
| **light** | Usage léger et rapide | Recherches rapides, mémoire, docs, GitHub — démarrage ultra-rapide |

## Matrice de redirection

Si tu reçois une requête hors de ton domaine, délègue via `use_subagent` :

| Tu es... | La requête concerne... | Délègue à... |
|----------|----------------------|-----------------|
| exp2 | LinkedIn, WhatsApp, Maps, YouTube | **connect** |
| exp2 | Famille, finances, santé, déménagement | **compass** |
| exp2 | Installation MCP, recherche d'outil | **forge** |
| compass | Code, AWS, infrastructure, projet pro | **exp2** |
| compass | LinkedIn, WhatsApp, Maps, YouTube | **connect** |
| compass | Installation MCP | **forge** |
| forge | Code, AWS, projet client | **exp2** |
| forge | Vie personnelle | **compass** |
| forge | LinkedIn, WhatsApp, Maps | **connect** |
| connect | Code, AWS, technique | **exp2** |
| connect | Vie personnelle | **compass** |
| connect | Installation MCP | **forge** |

## Exemple de délégation

Agent exp2 reçoit "montre-moi mes posts LinkedIn récents" :

```json
{
  "command": "InvokeSubagents",
  "content": {
    "subagents": [{
      "query": "Liste les 3 derniers posts LinkedIn de l'utilisateur",
      "agent_name": "connect"
    }]
  }
}
```

→ connect démarre avec ses MCPs (linkedin-mcp), exécute la requête, retourne le résultat à exp2, puis est détruit.

## Mise à jour

Ce fichier est mis à jour par **it-supervisor** à chaque ajout ou retrait d'un agent.
