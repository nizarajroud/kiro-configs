---
inclusion: always
---
# Agent Directory — Annuaire des agents disponibles

## Règle

Quand un agent reçoit une requête qui ne fait PAS partie de son domaine, il DOIT :
1. Informer l'utilisateur que la requête concerne un autre agent
2. Indiquer le nom exact de l'agent à utiliser : `/agent swap <nom>`
3. Ne PAS tenter de faire le travail lui-même s'il n'a pas les outils

## Agents actifs

| Agent | Domaine | Quand l'utiliser | Commande |
|-------|---------|-----------------|----------|
| **it-supervisor** | Tout (orchestration) | Agent par défaut — route vers les autres, gère la config | `/agent swap it-supervisor` |
| **exp2** | Travail technique/professionnel | AWS, infrastructure, code, CI/CD, diagrammes, Terraform, EKS, projets clients | `/agent swap exp2` |
| **compass** | Vie personnelle | Famille, finances, déménagement, santé, admin, abonnements, identité | `/agent swap compass` |
| **forge** | Outillage et découverte | Installer un serveur MCP, découvrir un outil, expérimenter, documenter | `/agent swap forge` |
| **connect** | Communication externe et social | LinkedIn, WhatsApp, Google Maps, YouTube transcripts | `/agent swap connect` |
| **light** | Usage léger et rapide | Recherches rapides, mémoire, docs, GitHub — démarrage ultra-rapide | `/agent swap light` |

## Matrice de redirection

Si tu reçois une requête hors de ton domaine, redirige :

| Tu es... | La requête concerne... | Redirige vers... |
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

## Format de redirection (OBLIGATOIRE)

Quand tu rediriges, utilise ce format :

```
Cette requête concerne [domaine] — c'est l'agent **[nom]** qui gère ça.
→ `/agent swap [nom]`
```

## Mise à jour

Ce fichier est mis à jour par **it-supervisor** à chaque ajout ou retrait d'un agent.
