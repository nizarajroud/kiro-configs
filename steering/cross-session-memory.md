# Cross-Session Memory — Recherche dans l'historique des conversations

## Règle : Ordre de recherche d'information

Quand l'utilisateur pose une question et que l'agent ne connaît PAS la réponse dans la session courante, l'agent DOIT chercher dans cet ordre :

1. **Session courante** — ce que l'agent voit nativement (toujours vérifié en premier, aucun tool nécessaire)
2. **Knowledge graph local** (`search_nodes`) — faits structurés, préférences, décisions mémorisées
3. **Mémoire conversationnelle** (`cascading_search`) — historique complet de toutes les sessions passées

## Règle : cascading_search comme source de données systématique

**Déclencheur** : Toute question substantielle (factuelle, stratégique, décisionnelle) posée par l'utilisateur — indépendamment de la formulation.

**Principe** : `cascading_search` est une SOURCE DE DONNÉES au même titre que NotebookLM, Notion, Gmail ou TickTick. Elle ne se limite PAS aux questions de type "tu te rappelles ?". Elle est consultée systématiquement pour enrichir la réponse avec le contexte des discussions passées.

**Quand appeler cascading_search EN PLUS des sources habituelles** :

L'agent DOIT appeler `cascading_search` quand la question porte sur :
- Une stratégie (financière, carrière, familiale, technique)
- Une décision à prendre ou déjà prise
- Un sujet récurrent (école des enfants, déménagement, travaux, projets)
- Un historique d'actions ou de réflexions sur un thème
- Toute question dont la réponse a pu être discutée/enrichie dans une session antérieure

**Quand NE PAS appeler cascading_search** :
- Questions purement opérationnelles sans historique ("crée un fichier", "envoie ce message")
- Commandes d'exécution directe ("restructure ce speech", "génère un diagramme")
- Questions dont la réponse est intégralement dans une source live (ex: solde bancaire → Excel)

**Intégration dans le routing** :

Pour une question substantielle, l'ordre de consultation devient :
1. Session courante
2. Knowledge graph (`search_nodes`)
3. **cascading_search** (sessions passées) — EN PARALLÈLE avec les sources live
4. Sources live (NotebookLM, Notion, Gmail, Excel, etc. selon routing habituel)

**Utilisation des résultats** :
- Si `cascading_search` retourne du contexte pertinent → l'intégrer dans la réponse avec les autres sources
- Citer la source : "D'après nos discussions précédentes..." ou intégrer naturellement
- Ne PAS afficher le tableau de sessions (réservé aux questions explicites "dans quelle session")
- Si les résultats contredisent une source live → signaler la contradiction (Principe 4)

## Hiérarchie de confiance — Sources live vs cascading_search

**Règle absolue** : Les sources live ont TOUJOURS priorité sur l'historique des sessions pour les **faits actuels**.

| Type d'information | Source de vérité | cascading_search apporte |
|---|---|---|
| Chiffres actuels (soldes, montants, cotisations) | Sources live (Excel, Notion, Airtable) | Le contexte : pourquoi ce montant a été choisi |
| Dates et échéances | Sources live (TickTick, Gmail, Calendar) | Le contexte : comment la date a été décidée |
| Statuts de tâches | Sources live (Airtable, TickTick) | L'historique : ce qui a été fait avant |
| Stratégies et décisions | **cascading_search** (sessions passées) | Source primaire — c'est LÀ que les décisions sont discutées |
| Contexte décisionnel (pourquoi X) | **cascading_search** (sessions passées) | Source primaire — les sources live ne contiennent pas le "pourquoi" |

**En cas de conflit** entre cascading_search et une source live :
- La source live gagne pour les **faits** (chiffres, dates, statuts)
- Signaler le delta à l'utilisateur avec le session_id pour traçabilité
- Exemple : "Ton Excel montre 2 000$/mois actuellement. Note : dans une session précédente on avait discuté de 3 600$/mois (`qq 484d0d4f-228a-406d-8448-284fef4d1c3b`) — est-ce que la stratégie a changé ?"

## Citation des sessions dans les réponses

**Règle** : Quand `cascading_search` apporte une information utilisée dans la réponse (intégrée dans la prose, pas en format tableau), TOUJOURS inclure le `session_id` entre parenthèses avec le préfixe `qq` pour que l'utilisateur puisse y accéder directement.

**Format** : `(qq <session_id_complet>)`

**Exemples** :
- "D'après notre discussion précédente, tu avais opté pour une cotisation REER de 3 600$/mois (`qq 484d0d4f-228a-406d-8448-284fef4d1c3b`)."
- "On avait conclu que Charlemagne était le meilleur choix pour Radouane vu ses notes (`qq 88b4aee6-da05-4631-9752-624d9530a022`)."
- "La stratégie transport scolaire devait être gérée autour du 10 juillet (`qq a669d905-c12e-45a9-b31b-c49b6fdd3947`)."

**Règle** : Le `session_id` est prêt à copier-coller — l'utilisateur tape `qq <id>` pour ouvrir la session et vérifier/challenger l'information.

## Déclencheur explicite pour cascading_search (recherche de session)

L'agent DOIT utiliser `cascading_search` avec le **format tableau** quand :
- L'utilisateur dit : "tu te rappelles", "on a parlé de", "dans quelle session", "est-ce qu'on a déjà", "la dernière fois", "tu sais si on avait"
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
