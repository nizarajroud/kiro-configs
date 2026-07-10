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

**RÈGLE ABSOLUE** : JAMAIS demander à l'utilisateur "tu veux que je spawne X?" ou "tu veux que je délègue?". Si la requête concerne un autre agent selon la matrice ci-dessous, spawner DIRECTEMENT sans poser de question. L'utilisateur attend un résultat, pas une question de routage.

## Agents actifs

| Agent | Domaine | Quand l'utiliser |
|-------|---------|-----------------|
| **it-supervisor** | Tout (orchestration) | Agent par défaut — route vers les autres, gère la config |
| **exp2** | Travail technique/professionnel | AWS, infrastructure, code, CI/CD, diagrammes, Terraform, EKS, projets clients |
| **compass** | Vie personnelle | Famille, finances, déménagement, santé, admin, abonnements, identité |
| **forge** | Outillage et découverte | Installer un serveur MCP, découvrir un outil, expérimenter, documenter |
| **connect1** | Communication externe et social | LinkedIn, WhatsApp, Google Maps, Video transcription (TikTok, YouTube, Instagram, etc.), SSH remote |
| **connect2** | Communication directe et marketplace | Telegram, Gmail, Perplexity (web search), Secondhand marketplaces |
| **connect3** | Social intelligence | Twitter/X, Instagram, Reddit, TikTok (recherche + monitoring) |
| **dev1** | Développement et IaC | GitLab, GitHub docs, Context7, Terraform, Graphistry |
| **diagram1** | Visualisation et diagrammes | AWS diagrams, Mermaid, Excalidraw, RTL visuals, QuickChart |
| **aws1** | Infrastructure cloud AWS | AWS pricing, EKS/K8s, AWS API (read-only), AWS bridge |
| **data1** | Données et recherche | Airtable, NotebookLM, MarkItDown, PDF reader, TickTick |
| **light** | Usage léger et rapide | Recherches rapides, mémoire, docs, GitHub — démarrage ultra-rapide |

## Matrice de redirection

Si tu reçois une requête hors de ton domaine, délègue via `use_subagent` :

| Tu es... | La requête concerne... | Délègue à... |
|----------|----------------------|-----------------|
| exp2 | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| exp2 | Telegram, Gmail, Marketplace, recherche web | **connect2** |
| exp2 | Famille, finances, santé, déménagement | **compass** |
| **dev1** | Développement et IaC | GitLab, GitHub docs, Context7, Terraform, Graphistry |
| **diagram1** | Visualisation et diagrammes | AWS diagrams, Mermaid, Excalidraw, RTL visuals, QuickChart |
| **aws1** | Infrastructure cloud AWS | AWS pricing, EKS/K8s, AWS API (read-only), AWS bridge |
| exp2 | Airtable, NotebookLM, documents, tâches | **data1** |
| exp2 | Installation MCP, recherche d'outil | **forge** |
| compass | Code, AWS, infrastructure, projet pro | **exp2** |
| compass | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| compass | Telegram, Gmail, Marketplace, recherche web | **connect2** |
| **dev1** | Développement et IaC | GitLab, GitHub docs, Context7, Terraform, Graphistry |
| **diagram1** | Visualisation et diagrammes | AWS diagrams, Mermaid, Excalidraw, RTL visuals, QuickChart |
| **aws1** | Infrastructure cloud AWS | AWS pricing, EKS/K8s, AWS API (read-only), AWS bridge |
| compass | Airtable, NotebookLM, documents, tâches | **data1** |
| compass | Installation MCP | **forge** |
| forge | Code, AWS, projet client | **exp2** |
| forge | Vie personnelle | **compass** |
| forge | LinkedIn, WhatsApp, Maps, SSH | **connect1** |
| forge | Telegram, Gmail, Marketplace | **connect2** |
| connect1 | Code, AWS, technique | **exp2** |
| connect1 | Vie personnelle | **compass** |
| connect1 | Telegram, Gmail, Marketplace | **connect2** |
| connect1 | Installation MCP | **forge** |
| connect2 | Code, AWS, technique | **exp2** |
| connect2 | Vie personnelle | **compass** |
| connect2 | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| connect2 | Installation MCP | **forge** |
| data1 | Code, AWS, technique | **exp2** |
| data1 | Vie personnelle | **compass** |
| data1 | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| data1 | Telegram, Gmail, Marketplace | **connect2** |
| data1 | Installation MCP | **forge** |
| aws1 | Code, développement, IaC | **dev1** |
| aws1 | Vie personnelle | **compass** |
| aws1 | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| aws1 | Telegram, Gmail, Marketplace | **connect2** |
| aws1 | Airtable, NotebookLM, documents, tâches | **data1** |
| aws1 | Installation MCP | **forge** |
| diagram1 | Code, AWS, technique | **exp2** |
| diagram1 | Vie personnelle | **compass** |
| diagram1 | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| diagram1 | Telegram, Gmail, Marketplace | **connect2** |
| diagram1 | Airtable, NotebookLM, documents, tâches | **data1** |
| diagram1 | Installation MCP | **forge** |
| dev1 | AWS, pricing, EKS | **aws1** |
| dev1 | Vie personnelle | **compass** |
| dev1 | LinkedIn, WhatsApp, Maps, Video transcription, SSH | **connect1** |
| dev1 | Telegram, Gmail, Marketplace | **connect2** |
| dev1 | Airtable, NotebookLM, documents, tâches | **data1** |
| dev1 | Installation MCP | **forge** |

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
