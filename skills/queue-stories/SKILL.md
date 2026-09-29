---
name: queue-stories
description: Transforme la file d'attente kiro-web en user stories + issues GitHub, et renvoie chaque story au panneau Stories de kiro-web. Lit les items pending par scope (dossier), déduit le repo via `git remote`, crée une issue GitHub par item (ou groupe), POST chaque story vers /api/stories pour qu'elle s'affiche dans le panneau « User stories », puis marque les items traités. Activates when the user asks to "génère les user stories", "génère les stories de la file", "transforme la file en user stories", "crée les issues GitHub depuis la file", "Générer stories" (bouton kiro-web), or any equivalent request.
---

## Objectif

Quand l'utilisateur demande de générer les user stories de la file d'attente
(bouton « ✨ Générer stories » de kiro-web, ou formulation équivalente), l'agent :

1. lit les items **pending** de la file (par **scope** = dossier) ;
2. transforme chaque item en **user story** (titre court + résumé) ;
3. crée une **issue GitHub** par story dans le repo du dossier courant ;
4. **POST chaque story vers `/api/stories`** de kiro-web (titre + résumé + URL de
   l'issue) → la story apparaît dans le panneau « User stories » (grisée car elle
   a une issue) ;
5. **marque les items traités** (`/processed`) pour qu'ils sortent de la file.

L'étape 4 est **OBLIGATOIRE** : sans elle, les issues sont créées mais le panneau
« User stories » de kiro-web reste vide (« Aucune story »).

## Sources de vérité (deux bases + l'API kiro-web)

| Base / API | Chemin | Rôle | Accès |
|------------|--------|------|-------|
| kiro-cli | `~/.local/share/kiro-cli/data.sqlite3` | Résoudre le scope (cwd) de la session | Lecture seule |
| kiro-web  | `$KIRO_WEB_DB` sinon `~/.local/share/kiro-web/kiro-web.sqlite3` | La file d'attente | Lecture (marquage via API) |
| kiro-web API | `$KIRO_WEB_URL` (ex : `http://127.0.0.1:8771`) | POST stories + marquer traité | HTTP POST |

Table `queue_items(session_id, position, text, summary, status, processed_at, topic_processed, created_at, scope, category)` — clé logique = **`scope`** (le dossier). Table `stories(scope, title, summary, issue_url, created_at)`.

## Procédure OBLIGATOIRE (dans cet ordre)

### 1. Résoudre le scope (dossier) et le session_id

- SID explicite dans le message → l'utiliser. Sinon fallback :

```bash
SID=$(sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT conversation_id FROM conversations_v2 ORDER BY updated_at DESC LIMIT 1")
SCOPE=$(sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT key FROM conversations_v2 WHERE conversation_id='$SID'")
```

`SCOPE` = le cwd du dossier (ex : `/home/nizar/HomeWspce/gnl-process`). Le
`session_id` utilisé pour l'API est ce **SID**.

### 2. Lire les items pending du scope

```bash
DB="${KIRO_WEB_DB:-$HOME/.local/share/kiro-web/kiro-web.sqlite3}"
sqlite3 "$DB" "SELECT position, summary, text FROM queue_items WHERE scope='$SCOPE' AND status='pending' ORDER BY position;"
```

Si aucun item → le dire simplement (file vide), ne rien créer. Ne rien inventer.

### 3. Déduire le repo GitHub du dossier

```bash
cd "$SCOPE" && git remote get-url origin
```

En extraire `owner/repo` (gérer les formats `git@github.com:owner/repo.git` et
`https://github.com/owner/repo.git`). Si pas de remote GitHub → le signaler et
s'arrêter (on ne crée pas d'issue sans repo).

### 4. Pour chaque item : story → issue GitHub → POST story → marquer traité

Pour chaque item pending :

a. **Composer la user story** : un **titre** court et une **description** (format
   « En tant que…, je veux…, afin de… » + le contexte de l'item). Utiliser le
   contexte de domaine de l'agent pour enrichir.

b. **Créer l'issue GitHub** dans `owner/repo` (via l'outil github `create_issue` :
   `title` = titre de la story, `body` = description, `labels` = `["user-story"]`
   + label de type si pertinent : `bug`, `enhancement`, `documentation`…).
   Récupérer l'**URL** de l'issue créée (`html_url`).

c. **POST la story vers kiro-web** (étape à NE PAS oublier) :

```bash
curl -s -X POST "$KIRO_WEB_URL/api/stories/$SID" \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg t "<titre>" --arg s "<résumé court>" --arg u "<issue_html_url>" \
        '{title:$t, summary:$s, issue_url:$u}')"
```

- `title` (obligatoire) = le titre de la story.
- `summary` = résumé court (affiché en tooltip dans le panneau).
- `issue_url` = l'URL de l'issue GitHub (rend la story cliquable + la grise comme
  « traitée »).
- Si `jq` n'est pas dispo, construire le JSON à la main en **échappant** les
  guillemets. `$KIRO_WEB_URL` est fourni dans l'environnement (fallback :
  `http://127.0.0.1:8771`).

d. **Marquer l'item traité** dans kiro-web (le sort de la file pending) :

```bash
curl -s -X POST "$KIRO_WEB_URL/api/queue/$SID/processed" \
  -H 'Content-Type: application/json' -d "{\"position\": <position>}"
```

### 5. Restituer

Afficher un récapitulatif (tableau : issue #, titre, statut/label) + confirmer que
les stories ont été renvoyées au panneau kiro-web. L'utilisateur peut cliquer ⟳
dans le panneau « User stories » pour les voir (elles apparaissent grisées car
elles ont une issue).

## Regroupement (optionnel)

Si plusieurs items pending parlent de la même chose, l'agent peut créer **une
seule** issue/story pour le groupe (titre englobant) et marquer **tous** les items
du groupe traités. Le POST story se fait alors une fois pour le groupe.

## Règles strictes

- ✅ Lire/écrire par **scope** (jamais par `session_id` pour la file), mais utiliser
  le **SID** dans les URLs d'API (`/api/stories/$SID`, `/api/queue/$SID/processed`).
- ✅ **Toujours** faire le POST `/api/stories/$SID` (étape 4c) — c'est ce qui
  remplit le panneau. Sans lui, la génération est incomplète.
- ✅ Respecter `$KIRO_WEB_DB` et `$KIRO_WEB_URL` s'ils sont définis.
- ✅ Une issue par story (ou par groupe), label `user-story` sur toutes.
- ✅ Ne marquer traité (`/processed`) que **après** avoir créé l'issue ET posté la
  story (jamais avant).
- ❌ Ne jamais inventer d'items absents de la DB.
- ❌ Ne pas créer d'issue s'il n'y a pas de remote GitHub sur le dossier.
- ❌ Ne pas confondre avec `queue-topics` (topics courts) : ici on crée des issues
  + stories complètes.

## Portée

Skill **global**, partagé par les agents domaine (surtout exp2/technique). Chaque
agent l'exécute avec son contexte de domaine.
