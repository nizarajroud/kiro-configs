---
name: mermaid-diagrams
description: Visualise n'importe quel sujet avec l'API Mermaid (api.mermaid.ai) — l'agent choisit le bon type de diagramme parmi une trentaine, écrit le code Mermaid lui-même, le rend en SVG via scripts/mermaid-render.py, et l'affiche inline dans kiro-web ou l'archive dans AI-GENERATED. Activates when the user says "mermaid", "visualise ça", "visualiser", "visualise-moi", "fais-moi un diagramme / schéma / flux / flowchart", "flux d'exécution", "montre le flux", or any request to draw/illustrate a process, architecture, sequence, data model, plan, comparison or structure — unless the user explicitly names another tool (draw.io, D2, Excalidraw).
---

## Objectif

Une seule façon de visualiser, identique pour tous les agents et toutes les sessions :
l'agent comprend ce que l'utilisateur veut illustrer, choisit le type de diagramme qui
le montre le mieux, écrit le code Mermaid, et le rend via l'API. Le résultat apparaît
inline dans kiro-web, ou s'ouvre dans le navigateur en CLI.

## Règle de choix de l'outil

- Demande de visualisation sans outil nommé : Mermaid, toujours.
- L'utilisateur nomme draw.io, D2, Excalidraw : suivre sa demande, pas Mermaid.
- Texte arabe / tunisien (RTL) : ne pas utiliser Mermaid pour l'instant, rester sur
  `rtl-visual-mcp` (sujet à revoir avec l'utilisateur).
- Le MCP `mcp-mermaid` n'a aucun lien avec l'API : ne pas l'utiliser pour ce flux.

## Procédure (dans cet ordre)

1. Identifier ce que l'utilisateur veut montrer (processus, échanges, données, planning,
   comparaison, structure...) et choisir le type dans la matrice ci-dessous.
2. Écrire le code Mermaid soi-même (pas de `/generate`, il coûte 25 crédits).
3. Appeler le script :

```bash
cat <<'EOF' | python3 ~/.kiro/scripts/mermaid-render.py --name <nom-kebab> --domain <personal|work> --subject <sujet-kebab>
flowchart LR
  A --> B
EOF
```

   Options utiles : `--file code.mmd`, `--format svg|png|pdf` (défaut svg), `--theme neutral`,
   `--config '{"look":"handDrawn"}'`, `--validate` (1 crédit), `--balance` (gratuit).
4. Lire la sortie : `ARTIFACT=` est le chemin à citer dans la réponse (kiro-web l'affiche inline
   quand il contient `.kiro-web-artifacts/`). `CREDITS_REMAINING=` informe du solde.
5. Dans la réponse : citer le chemin absolu de `ARTIFACT`, en deux phrases dire ce que le diagramme
   montre et pourquoi ce type a été choisi, et inclure le code source seulement si l'utilisateur
   veut le modifier (il est déjà sauvegardé dans `SOURCE=`).

Le script s'occupe seul de : lire la clé dans `.env`, vérifier le solde, espacer les appels,
ranger le fichier (kiro-web : `./.kiro-web-artifacts/` + copie `AI-GENERATED/` ; CLI : `AI-GENERATED/`
+ ouverture dans le navigateur), journaliser dans `logs/mermaid-usage.jsonl`. Ne jamais copier la clé
dans un prompt, une commande ou un fichier.

## Quota (important : 500 crédits par mois, partagés avec le projet GNL)

| Appel | Coût |
|-------|------|
| render | 5 |
| validate | 1 |
| generate | 25 |
| repair | 25 |
| balance | 0 |

- Un rendu servi par le cache est facturé quand même : ne jamais re-rendre un code identique,
  réutiliser le fichier déjà produit.
- Soigner le code avant de rendre. Une modification demandée par l'utilisateur coûte un nouveau rendu :
  regrouper plusieurs retouches en une seule.
- Le script refuse de rendre sous 50 crédits (code de sortie 3, message `QUOTA_LOW`). Dans ce cas :
  dire à l'utilisateur combien il reste et quand le quota se réinitialise, et proposer d'insister
  (`--force`) ou d'attendre. Ne jamais passer `--force` de ta propre initiative.
- Ne pas boucler : au plus 2 rendus par demande, sauf si l'utilisateur demande des retouches.

## Matrice : besoin -> type de diagramme

| Ce que l'utilisateur veut montrer | Type | Mot-clé de début |
|-----------------------------------|------|------------------|
| Un processus, un algorithme, un flux d'exécution, une décision | flowchart | `flowchart LR` ou `TD` |
| Qui parle à qui, dans quel ordre (API, services, personnes) | sequence | `sequenceDiagram` |
| Cycle de vie, statuts, transitions | state | `stateDiagram-v2` |
| Modèle de données, tables, relations | er | `erDiagram` |
| Classes, objets, héritage, modules | class | `classDiagram` |
| Planning, jalons, dépendances de tâches | gantt | `gantt` |
| Chronologie d'événements, historique | timeline | `timeline` |
| Parcours utilisateur, étapes avec satisfaction | journey | `journey` |
| Idées, brainstorming, plan d'un sujet | mindmap | `mindmap` |
| Répartition, parts d'un tout | pie | `pie` |
| Comparer des options sur 2 axes (effort/impact) | quadrant | `quadrantChart` |
| Courbes, barres, tendances | xychart | `xychart-beta` |
| Flux quantifiés entre étapes | sankey | `sankey-beta` |
| Architecture cloud / systèmes (groupes, services) | architecture | `architecture-beta` |
| Contexte système, conteneurs, composants | c4 | `C4Context` / `C4Container` |
| Disposition en blocs | block | `block-beta` |
| Exigences et traçabilité | requirement | `requirementDiagram` |
| Historique de branches git | gitgraph | `gitGraph` |
| Tableau de suivi à colonnes | kanban | `kanban` |
| Structure binaire d'un paquet / protocole | packet | `packet-beta` |

Types plus récents et moins courants, présents dans l'API mais dont la syntaxe n'a pas été vérifiée
ici : ishikawa (causes d'un problème), radar, treemap, venn, wardley, cynefin, swimlanes,
eventmodeling, treeview. Pour ceux-là, toujours passer `--validate` (1 crédit) avant le rendu, et
retomber sur un type classique si le code est refusé.

Règle de choix quand plusieurs types conviennent : prendre celui qui répond à la question posée,
pas le plus impressionnant. Un flux d'exécution est un flowchart (ou une sequence si ce sont des
échanges entre acteurs). Un doute entre deux : choisir le plus simple.

## Qualité du diagramme

- Étiquettes courtes (2 à 5 mots), détails dans un texte voisin, pas dans les nœuds.
- Direction `LR` pour un flux, `TD` pour une hiérarchie. Éviter plus de ~15 nœuds : découper en
  plusieurs diagrammes, ou sous-graphes (`subgraph`).
- Thème : défaut de Mermaid. `--theme neutral` pour un rendu sobre de documentation. Ne pas
  multiplier les couleurs.
- Caractères spéciaux dans une étiquette (parenthèses, deux-points, guillemets) : mettre l'étiquette
  entre guillemets, `A["Étape (1): saisie"]`.
- Nom de fichier : kebab-case descriptif ; `--subject` = thème réutilisable (gnl, bnc, demenagement...).

## Erreurs et pièges connus

| Symptôme | Cause | Quoi faire |
|----------|-------|-----------|
| Code de sortie 3 `QUOTA_LOW` | Moins de 50 crédits | Informer l'utilisateur, ne pas forcer seul |
| Code de sortie 4 `CODE_INVALID` + ligne/colonne | Syntaxe Mermaid fausse | Corriger le code à l'endroit indiqué, relancer. Pas de `/repair` (25 crédits) |
| Code de sortie 5 | Clé refusée | Dire que la clé est à vérifier ; ne pas réessayer |
| 401 `ERR_KEY_MISSING` alors que la clé existe | Appel fait avec `urllib` : la redirection CloudFront supprime l'en-tête | Le script utilise `curl -L` ; ne jamais réécrire l'appel avec `urllib` |
| HTTP 429 | Plus de 20 requêtes en 60 s | Le script espace et réessaie seul |
| Rendu différent d'un jour à l'autre | Version Mermaid « latest » qui change (API en beta) | Épingler avec `--mermaid-version 12.1.0` si la reproductibilité compte |

Pour toute demande de support à Mermaid, citer le `x-request-id` (champ `request_id` du journal
`logs/mermaid-usage.jsonl`).

## Statut de l'API

Beta : champs, limites et version de Mermaid peuvent changer sans préavis, et la documentation
déconseille une dépendance de production. Si l'API est injoignable (code de sortie 6), l'écrire
clairement et proposer le secours local (`mmdc`) seulement s'il a été installé ; sinon donner le code
Mermaid brut, que l'utilisateur peut coller dans un éditeur Mermaid.
