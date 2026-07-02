# Cross-Session Memory — Recherche dans l'historique des conversations

## Règle : Ordre de recherche d'information

Quand l'utilisateur pose une question et que l'agent ne connaît PAS la réponse dans la session courante, l'agent DOIT chercher dans cet ordre :

1. **Session courante** — ce que l'agent voit nativement (toujours vérifié en premier, aucun tool nécessaire)
2. **Knowledge graph local** (`search_nodes`) — faits structurés, préférences, décisions mémorisées
3. **Mémoire conversationnelle** (`cascading_search`) — historique complet de toutes les sessions passées

## Déclencheur pour cascading_search

L'agent DOIT utiliser le tool `cascading_search` quand :
- L'utilisateur dit : "tu te rappelles", "on a parlé de", "dans quelle session", "est-ce qu'on a déjà", "la dernière fois", "tu sais si on avait"
- L'agent ne trouve pas l'information ni dans la session courante ni dans `search_nodes`
- L'utilisateur demande un détail spécifique d'une discussion passée

## Paramètres obligatoires pour cascading_search

- `query` : la question de l'utilisateur (en langage naturel)
- `current_folder` : le dossier courant (extraire de env_context.current_working_directory)
- `current_agent` : le nom de l'agent actuel

## Comportement STRICT

- ❌ JAMAIS répondre "je n'ai pas cette information" ou "je ne me rappelle pas" sans avoir d'abord appelé `cascading_search`
- ❌ JAMAIS dire "cette information n'est pas dans ma session" comme réponse finale
- ✅ TOUJOURS appeler `cascading_search` avant de conclure qu'une information est introuvable
- ✅ Si `cascading_search` retourne des résultats, les utiliser pour répondre à l'utilisateur
- ✅ Si `cascading_search` ne retourne rien, alors seulement dire "je n'ai pas trouvé cette information dans l'historique"
