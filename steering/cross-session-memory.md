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

## Format de réponse obligatoire

Quand l'agent retourne un résultat de recherche cross-session, il DOIT :

1. Faire un lookup dans `~/.kiro/sessions/topics.db` (table `session_catalog`) avec le `session_id` pour obtenir le nom de session, le thème et les sujets
2. Répondre avec une phrase d'introduction puis un tableau ASCII aligné

**Phrase d'introduction** : "On a parlé de **[sujet recherché]** dans les sessions suivantes :"

**Tableau** (aligné, pleine largeur, sujets en bullets intra-cellule) :

```
| Thème          | Session           | Last access          | Autres sujets                    | Accès                                          |
|----------------|-------------------|----------------------|----------------------------------|-------------------------------------------------|
| déménagement   | nizar-via-compass | Hier à 19:30         | • RDV ServiceRG                  | qq d79e35e8-d97a-42cb-8f3d-c17e5be24ec2        |
|                |                   |                      | • silicone salle de bain         |                                                 |
|                |                   |                      | • robinet d'arrêt                |                                                 |
|----------------|-------------------|----------------------|----------------------------------|-------------------------------------------------|
| entretien      | nizar-via-compass | Vendredi à 14:30     | • recherches RONA                | qq 1d2219cb-98c0-44c3-b334-f29871bb2473        |
|                |                   |                      | • WD-40 rangée/section           |                                                 |
```

**Format de la colonne "Last access"** :
- Aujourd'hui → "Aujourd'hui à HH:MM"
- Hier → "Hier à HH:MM"
- Avant-hier → "Avant-hier à HH:MM"
- Cette semaine → "Jour à HH:MM" (ex: "Vendredi à 14:30")
- Plus ancien → "YYYY-MM-DD"

**Règles du tableau** :
- Chaque sujet est sur sa propre ligne physique avec bullet `•`, DANS la même cellule (pas de nouvelle ligne logique)
- La colonne "Accès" contient `qq <session_id_complet>` — prêt à copier-coller
- Le séparateur `|---|` entre chaque session (ligne logique)
- Respecter les règles de tableaux ASCII des output rules (padding, alignement, largeur complète)

### Lookup SQLite

```sql
SELECT theme, session_name, subjects FROM session_catalog WHERE session_id = '<id>';
```
Fichier : `~/.kiro/sessions/topics.db`
