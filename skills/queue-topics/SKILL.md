---
name: queue-topics
description: Résume la file d'attente kiro-web. Mode « topics » : génère un topic de 1 à 2 mots par item non traité (colonne summary). Mode « réorganiser » : en plus du topic, assigne une rubrique/catégorie (colonne category) pour regrouper les items. Activates when the user asks to "résume la file d'attente", "summarize the queue", "génère les topics de la file" (topics seuls), OR "résume et réorganise la file", "réorganise la file", "rubriques", "catégories", "Résumer & réorganiser" (topics + rubriques), or any equivalent request on the kiro-web queue.
---

## Objectif

Quand l'utilisateur demande de résumer la file d'attente de kiro-web, l'agent lit
les items non encore traités et écrit, **directement en base SQLite**, un topic
court (1 à 2 mots) pour chacun. L'agent profite de son contexte de domaine
(Compass = vie perso, Exp2 = technique, Forge = outillage, etc.) pour produire un
topic plus pertinent qu'un résumé à froid.

Aucune API externe, aucun appel Bedrock — uniquement des commandes `sqlite3` via
`execute_bash`.

## Déclencheur

L'utilisateur demande explicitement de résumer / topiquer la file d'attente (queue)
de kiro-web :
- « résume la file d'attente », « résume les items de la file »
- « summarize the queue », « génère les topics de la file »
- toute formulation équivalente

## Sources de vérité (deux bases distinctes)

| Base | Chemin | Rôle | Accès |
|------|--------|------|-------|
| kiro-cli | `~/.local/share/kiro-cli/data.sqlite3` | Résoudre le `session_id` courant | **Lecture seule** |
| kiro-web | `$KIRO_WEB_DB` sinon `~/.local/share/kiro-web/kiro-web.sqlite3` | File d'attente à résumer | Lecture + écriture `summary`/`topic_processed` |

Table kiro-web :
```
queue_items(session_id, position, text, summary, status, processed_at, topic_processed, created_at, scope, category)
```
- `summary` = topic court (1-2 mots) — mode topics.
- `category` = rubrique/toggle (mode réorganiser). Vide (`''`) = « Non classé ».
- `scope` = le cwd du dossier (la file est **par dossier**).

## Procédure OBLIGATOIRE

### Étape 1 — Déterminer le session_id (SID explicite PRIORITAIRE)

**Règle de priorité (ordre strict) :**

1. **SID explicite dans le message → PRIORITÉ ABSOLUE.** Si le message de l'utilisateur
   contient un identifiant de session (ex : « résume la file d'attente de la session
   `ADB0D8` », « la session `0c609cd4-1b97-...` »), utiliser **CE** SID directement.
   Dans ce cas, **NE PAS** exécuter la détection par `ORDER BY updated_at` — le fallback
   est ignoré.
2. **Aucun SID fourni → fallback détection auto.** Résoudre le session_id courant depuis
   la DB kiro-cli :

```bash
sqlite3 ~/.local/share/kiro-cli/data.sqlite3 \
  "SELECT conversation_id FROM conversations_v2 ORDER BY updated_at DESC LIMIT 1"
```

⚠️ La détection `ORDER BY updated_at DESC LIMIT 1` n'est qu'un **fallback**. Elle peut
tomber sur une autre session que celle voulue (celle avec la file à résumer). Dès qu'un
SID est mentionné par l'utilisateur, il l'emporte sur cette détection.

### Étape 2 — Lire les items à résumer

Résoudre d'abord le chemin de la DB kiro-web (respecter `$KIRO_WEB_DB`) :

```bash
DB="${KIRO_WEB_DB:-$HOME/.local/share/kiro-web/kiro-web.sqlite3}"
sqlite3 "$DB" \
  "SELECT position, text FROM queue_items WHERE session_id='<SID>' AND topic_processed=0 ORDER BY position;"
```

- Traiter **uniquement** les items `topic_processed=0`.
- Si aucune ligne n'est retournée → la file (non traitée) est vide. **S'arrêter** et
  le dire simplement à l'utilisateur. Ne rien écrire.

### Étape 3 — Générer un topic par item

Pour chaque item, produire un **topic de 1 à 2 mots MAXIMUM**, en français :
- Contextuel au domaine de l'agent (l'agent connaît la vie et les projets de
  l'utilisateur → topic plus pertinent qu'un résumé générique).
- Pas de phrase, pas de ponctuation finale, pas de guillemets.
- Exemples : `LinkedIn`, `Impôts 2026`, `Deploy Lambda`, `Fix pipeline`, `École Léa`.

### Étape 4 — Écrire chaque topic en DB

Une commande `UPDATE` par item. **Doubler les apostrophes** dans la valeur SQL
(`'` → `''`) pour éviter toute erreur ou injection :

```bash
sqlite3 "$DB" \
  "UPDATE queue_items SET summary='<topic>', topic_processed=1 WHERE session_id='<SID>' AND position=<pos>;"
```

Ne modifier **que** les colonnes `summary` et `topic_processed`.

### Étape 5 — Confirmer à l'utilisateur

Afficher :
- Le nombre d'items résumés.
- La liste `position → topic` (tableau ASCII aligné selon les output rules).

## Règles strictes

- ✅ Topic 1-2 mots, en français, contextuel au domaine de l'agent.
- ✅ SID explicite du message = priorité absolue ; la détection `ORDER BY updated_at` n'est qu'un fallback quand aucun SID n'est fourni.
- ✅ Traiter uniquement `topic_processed=0` (ne jamais retoucher un item déjà résumé).
- ✅ Écrire directement en DB via `sqlite3`. Aucune API externe, aucun Bedrock.
- ✅ Doubler les apostrophes dans les valeurs SQL (`'` → `''`).
- ✅ Respecter `$KIRO_WEB_DB` s'il est défini (défaut : `~/.local/share/kiro-web/kiro-web.sqlite3`).
- ❌ Ne jamais modifier `text`, `status`, `position`, `processed_at`, ni la DB kiro-cli.
- ❌ Ne pas résumer si la file (non traitée) est vide → le dire simplement.

## Mode « Résumer & réorganiser » (topics + rubriques)

**Déclencheur de la réorganisation** : le message contient « réorganise », « rubriques »,
« catégories », ou le prompt exact « résume et réorganise la file d'attente de la session
`<SID>` » (envoyé par le bouton kiro-web « Résumer & réorganiser »).

- Si le message dit seulement « résume » (sans réorganiser) → **comportement topics
  seul** (section ci-dessus, pas de `category`).
- Si réorganisation demandée → en plus du topic (`summary`), assigner une **rubrique**
  (`category`) à chaque item pour **regrouper** les items similaires.

### Procédure OBLIGATOIRE (réorganisation)

**1. Résoudre le scope (cwd)** — SID explicite prioritaire, sinon fallback
`ORDER BY updated_at DESC`. Puis résoudre le dossier :

```bash
SCOPE=$(sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT key FROM conversations_v2 WHERE conversation_id='<SID>'")
```

**2. Lire les items pending du scope + les catégories déjà existantes** (à réutiliser en priorité) :

```bash
DB="${KIRO_WEB_DB:-$HOME/.local/share/kiro-web/kiro-web.sqlite3}"
# items à traiter
sqlite3 "$DB" "SELECT position, text FROM queue_items WHERE scope='$SCOPE' AND status='pending' ORDER BY position;"
# catégories existantes (à RÉUTILISER en priorité)
sqlite3 "$DB" "SELECT DISTINCT category FROM queue_items WHERE scope='$SCOPE' AND category!='';"
```

**3. Pour chaque item, déterminer :**
- Un **topic court** (1-2 mots) → colonne `summary` (comme le mode topics).
- Une **rubrique** → colonne `category` :
  - **Réutiliser une rubrique existante** si l'item y correspond (liste de l'étape 2).
  - Sinon **créer une nouvelle rubrique** avec un nom court et clair (1-3 mots, ex :
    `Bugs WebSocket`, `Features file`, `Docs`, `Refactor`).
  - **Regrouper** les items similaires sous la même rubrique (c'est tout l'intérêt).

**4. Écrire en DB** (une commande `UPDATE` par item, apostrophes doublées `'`→`''`) —
écrire `summary` ET `category` dans le même UPDATE :

```bash
sqlite3 "$DB" "UPDATE queue_items SET summary='<topic>', category='<rubrique>', topic_processed=1 WHERE scope='$SCOPE' AND position=<pos>;"
```

Ne modifier **que** `summary`, `category`, `topic_processed`. Jamais `text`, `status`,
`position`, `scope`.

**5. Confirmer à l'utilisateur** : nombre d'items réorganisés + la liste **rubrique →
items** (tableau ASCII aligné selon les output rules), pour qu'il voie le regroupement.

### Règles strictes (réorganisation)

- ✅ Toujours lire/écrire par **scope** (jamais `session_id`).
- ✅ **Réutiliser** les rubriques existantes avant d'en créer de nouvelles.
- ✅ Noms de rubriques courts et cohérents (**regrouper**, pas une rubrique par item).
- ✅ Respecter `$KIRO_WEB_DB`.
- ✅ Écrire `summary` + `category` ensemble.
- ❌ Ne jamais inventer d'items absents de la DB.
- ❌ Ne pas créer une rubrique unique par item (l'objectif est de grouper).
- ❌ Ne pas toucher `text`/`status`/`position`/`scope`.

## Portée

Skill **global**, partagé par tous les agents domaine (exp2, compass, forge, light…).
Chaque agent l'exécute avec son propre contexte de domaine — le même item peut donc
être résumé différemment selon l'agent. **C'est voulu.**
