---
inclusion: always
---
# Notion Search Priority — Pages de référence

## Règle de recherche Notion

Quand l'agent cherche de l'information dans Notion, il DOIT d'abord consulter la page prioritaire correspondant au contexte de la question AVANT de faire une recherche globale sur le workspace.

## Routing de recherche

| Contexte de la question | Page prioritaire | ID | Quand consulter |
|-------------------------|-----------------|-----|-----------------|
| Compte-rendu, résumé d'échange, meeting passé, "qu'est-ce qu'on a dit/décidé" | **Meetings-Reports** | `84c17364-a96f-44a0-8a5b-235035d7deba` | Question sur un échange passé (physique ou en ligne) |
| Speech, préparation d'appel, script, argumentaire | **Mes Speechs** | `398174cb-5dcc-81e7-a48b-cab097d0e176` | Question sur un discours ou préparation de communication |
| Démarche en cours, procédure administrative, suivi perso | **Procédures en cours** | `da0e66ac-2c07-442b-95ca-870a423498e0` | Question sur une procédure ou démarche active |
| Serveur MCP, outil technique, configuration, setup | **Tooling** | `398c2347-678d-445a-a7f9-1fcb257d1ea8` | Question sur un outil technique ou une installation |
| Outil du quotidien, application, service utilisé | **Tools I use** | `09777d01-ebcd-4424-acfc-d9ca4607f43c` | Question sur les outils/apps en usage |
| Compte, identifiant, email, AWS account, MAC, asset digital | **AGGREGATIONS** | `2a4174cb-5dcc-8018-b743-e9a969f47bde` | Question sur un identifiant, un compte, un asset |
| Projet professionnel, mandat, client | **Projects** | `98247ec1-5ff1-45e1-b2ac-9e85a30a1094` | Question sur un projet de travail |

## Procédure de recherche (OBLIGATOIRE)

1. **Identifier le contexte** de la question (meeting? outil? compte? projet?)
2. **Consulter la page prioritaire** correspondante via `APIretrieveapage(page_id)` ou `APIgetblockchildren(block_id)` pour chercher directement dans la bonne page
3. **Si trouvé** → répondre avec citation de la page
4. **Si pas trouvé** → élargir avec `APIpostsearch(query)` sur tout le workspace
5. **JAMAIS** faire une recherche globale directement quand le contexte matche une page prioritaire

## Exemples

- "C'était quoi le résumé du meeting avec X?" → chercher dans `Meetings-Reports` d'abord
- "J'avais préparé un speech pour l'appel avec Y" → chercher dans `Mes Speechs` d'abord
- "Où en est ma procédure Z?" → chercher dans `Procédures en cours` d'abord
- "C'est quoi mon account ID AWS training?" → chercher dans `AGGREGATIONS` d'abord
- "C'est quoi le statut du projet NovaTech?" → chercher dans `Projects` d'abord
