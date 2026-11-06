---
inclusion: always
---
# Règle d'or : Visualiser = API Mermaid (tous les agents)

Cette règle s'applique à tous les agents, dans toutes les sessions, sans exception.

## Déclencheur

L'utilisateur dit « mermaid », « visualise ça », « visualiser », « visualise-moi », « fais-moi un
schéma / diagramme / flux », « flux d'exécution », « montre le flux », ou demande d'illustrer un
processus, une architecture, des échanges, un modèle de données, un planning, une comparaison ou une
structure (insensible à la casse, liste non exhaustive).

## Action obligatoire

1. Charger le skill `mermaid-diagrams` (skills/mermaid-diagrams/SKILL.md) et suivre sa procédure :
   choisir le type de diagramme adapté au besoin, écrire le code Mermaid, le rendre en SVG avec
   `~/.kiro/scripts/mermaid-render.py`.
2. Le script décide seul de l'emplacement :
   - kiro-web (`KIRO_WEB=1`) : `./.kiro-web-artifacts/<nom>.svg`, affiché inline dans le fil.
   - CLI : `AI-GENERATED/` puis ouverture dans le navigateur Windows.
   - Dans les deux cas, copie d'archivage dans `AI-GENERATED/` + code source `.mmd`.
3. Citer dans la réponse le chemin absolu `ARTIFACT=` renvoyé par le script.

## Priorité entre outils

- Pas d'outil nommé : Mermaid. Ne pas produire de draw.io, D2 ni Excalidraw de sa propre initiative.
- L'utilisateur nomme explicitement draw.io, D2 ou Excalidraw : suivre sa demande.
- Texte arabe / tunisien : ne pas utiliser Mermaid, rester sur `rtl-visual-mcp` (à revoir).

## Garde-fous

- Le quota est de 500 crédits par mois, partagés avec le projet GNL (render = 5, validate = 1).
  Le script refuse de rendre sous 50 crédits : en informer l'utilisateur, ne jamais forcer seul.
- Ne jamais re-rendre un code identique (le cache est facturé aussi). Regrouper les retouches.
- Ne jamais exposer la clé `MERMAID_API_KEY` (lue par le script dans `.env`).
- Ne pas faire de `find` pour retrouver le fichier : le chemin est donné par le script.

## Ajout à la checklist de sortie

- [ ] Visualisation demandée ? Passer par le skill `mermaid-diagrams` et citer le chemin `ARTIFACT=`.
