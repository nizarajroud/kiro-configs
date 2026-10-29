---
inclusion: always
---
# 🟥 GOLDEN RULE — Inventaire des sujets en temps réel (topic_log)

> **RÈGLE ABSOLUE, NON-NÉGOCIABLE, APPLICABLE À TOUS LES AGENTS SANS EXCEPTION**
> (compass, exp2, forge, light, it-supervisor, sandbox, et tout agent présent ou futur).
> Cette règle n'est PAS optionnelle. Son non-respect est une FAUTE GRAVE au même titre
> qu'une réponse sans citation de source. L'agent qui détecte le déclencheur et n'écrit
> PAS dans `topic_log` a échoué à sa tâche, même si le reste de la réponse est parfait.

## Pourquoi cette règle existe

L'utilisateur jongle entre des dizaines de sessions/agents/dossiers. Il doit pouvoir
retrouver **instantanément** « dans quelle session a-t-on parlé de X ». Le hook
post-session (`session_catalog`) est un filet de rattrapage tardif et imprécis. Cette
règle capture le sujet **au moment exact** où il démarre, écrit par l'agent lui-même
avec un titre pertinent en contexte. `topic_log` devient la **source primaire**.

## Source de vérité (une seule base, déjà existante)

| Base | Chemin | Table | Rôle |
|------|--------|-------|------|
| topics | `~/.kiro/sessions/topics.db` | **`topic_log`** | Inventaire des sujets (cette règle — écriture live) |
| topics | `~/.kiro/sessions/topics.db` | `session_catalog` | Vue par session (hook post-session — NE PAS toucher) |
| kiro-cli | `~/.local/share/kiro-cli/data.sqlite3` | `conversations_v2` | Résoudre le scope/agent de la session |

Schéma `topic_log` :
```
topic_log(id, topic_title, topic_context, session_id, agent, scope, created_at, last_message)
```

---

## PARTIE A — ÉCRITURE (détecter un sujet → l'enregistrer IMMÉDIATEMENT)

### A.1 Déclencheurs (quand écrire)

**Déclencheur explicite** — l'utilisateur annonce un changement/nouveau sujet. Marqueurs
(liste **enrichissable** — insensible à la casse, non exhaustive) :

- « laissons ce sujet au parking », « on met ça de côté », « on parque ce sujet »
- « nouveau sujet », « changeons de sujet », « on switch de sujet », « on change de sujet »
- « on passe à autre chose », « passons à », « sujet suivant », « autre sujet »
- « je vais te parler de… », « parlons de… », « maintenant je veux parler de… »
- « oublie ça pour l'instant, je veux… », « revenons à… » (reprise d'un sujet)

> **ENRICHISSEMENT DU DICTIONNAIRE (obligatoire)** : si l'utilisateur emploie une
> NOUVELLE tournure sémantiquement équivalente à « changement de sujet » qui n'est pas
> dans la liste ci-dessus, l'agent DOIT (a) la traiter comme un déclencheur valide, et
> (b) **ajouter cette tournure à la liste ci-dessus** via `fs_write` (str_replace) dans
> ce fichier, pour que le dictionnaire grandisse avec le vocabulaire réel de l'utilisateur.

**Déclencheur automatique** — même sans marqueur explicite, si la conversation **vire
nettement** vers un thème différent du précédent (nouveau domaine/projet/problème),
l'agent enregistre le nouveau sujet. En cas de doute léger → enregistrer quand même
(un sujet en trop est sans gravité ; un sujet manqué casse la promesse de l'inventaire).

### A.2 Action d'écriture (procédure EXACTE — aucune improvisation)

Dès qu'un déclencheur est détecté, AVANT de répondre sur le fond du nouveau sujet,
exécuter cette séquence `sqlite3` (via `execute_bash`), silencieusement :

```bash
# 1. Résoudre la session du DOSSIER courant (jamais la dernière session globale)
CWD="$(pwd)"
SID=$(sqlite3 ~/.local/share/kiro-cli/data.sqlite3 \
  "SELECT conversation_id FROM conversations_v2 WHERE key='$CWD' ORDER BY updated_at DESC LIMIT 1")
# Fallback si aucune session pour ce cwd : prendre KIRO_SESSION_ID de l'environnement
[ -z "$SID" ] && SID="${KIRO_SESSION_ID:-unknown}"

# 2. Écrire le sujet (doubler les apostrophes '→'' dans CHAQUE valeur)
DB="$HOME/.kiro/sessions/topics.db"
sqlite3 "$DB" "INSERT INTO topic_log
  (topic_title, topic_context, session_id, agent, scope, created_at, last_message)
  VALUES ('<TITRE>', '<CONTEXTE>', '$SID', '<AGENT>', '$CWD', strftime('%s','now'), '<EXTRAIT>');"
```

Où :
- `<TITRE>` = titre court du sujet, **1 à 5 mots**, en français, sans ponctuation finale
  (ex : `Migration Kiro V3`, `Achat robot aspirateur`, `Skill queue-topics`).
- `<CONTEXTE>` = **une** phrase décrivant le sujet (de quoi il s'agit précisément).
- `<AGENT>` = le nom de l'agent courant (compass, exp2, forge, light, it-supervisor, …).
- `<EXTRAIT>` = court extrait (≤120 car.) du message qui a lancé le sujet.
- **Apostrophes doublées** dans toutes les valeurs texte (`'` → `''`).

### A.3 Règles strictes d'écriture

- ✅ Écrire **au moment** de la détection, pas en fin de session.
- ✅ Écrire **par scope (cwd)** — jamais supposer le dossier.
- ✅ `topic_log` seulement. NE JAMAIS modifier `session_catalog` ni la DB kiro-cli.
- ✅ Opération silencieuse : ne pas noyer la réponse. Un simple `✓ sujet enregistré`
  discret en fin de réponse suffit (ou rien).
- ❌ NE JAMAIS inventer un `session_id`. Si introuvable → `KIRO_SESSION_ID` puis `unknown`.
- ❌ NE JAMAIS sauter l'écriture parce que « le sujet semble mineur » — on enregistre.

---

## PARTIE B — LECTURE (« dans quelle session on a parlé de X ? »)

### B.1 Déclencheur

L'utilisateur demande où/quand/avec quel agent un sujet a été abordé : « où on a parlé
de X », « dans quelle session le sujet Y », « tu te rappelles quand on a discuté de Z »,
« retrouve le sujet… », etc.

### B.2 Ordre de consultation (STRICT)

1. **`topic_log` EN PREMIER** (source primaire) :

```bash
DB="$HOME/.kiro/sessions/topics.db"
sqlite3 -separator ' | ' "$DB" "SELECT datetime(created_at,'unixepoch','localtime'),
  topic_title, session_id, agent, scope, last_message
  FROM topic_log
  WHERE topic_title LIKE '%<MOT>%' OR topic_context LIKE '%<MOT>%' OR last_message LIKE '%<MOT>%'
  ORDER BY created_at DESC LIMIT 10;"
```

2. **Si `topic_log` ne retourne rien → fallback `cascading_search`** (règle
   `cross-session-memory.md`) puis `session_catalog` si utile.

### B.3 Restitution

Présenter : **titre du sujet · session_id (complet, préfixe `qq` pour copier-coller) ·
agent · dossier · date · extrait**. Respecter le format tableau des output-rules.
Citer la session : `qq <session_id_complet>` (UUID 36 caractères, JAMAIS tronqué).

---

## Rapport avec les autres mécanismes

- **Hook `session-catalog.py`** (post-session) : conservé **tel quel, inchangé**. Il
  continue d'alimenter `session_catalog`. `topic_log` ne le remplace pas — il le complète
  en capture live et devient la source primaire de recherche de sujet.
- **`cascading_search`** : reste le fallback sémantique quand `topic_log` est muet.

## Ajout à la checklist de sortie (NON-NÉGOCIABLE)

- [ ] **Changement/nouveau sujet détecté (marqueur explicite OU virage automatique) ?**
  → `INSERT` immédiat dans `topic_log` (titre + contexte + session du cwd + agent + scope
  + extrait, apostrophes doublées). Nouvelle tournure détectée → l'ajouter au dictionnaire
  de la Partie A.1.
- [ ] **Question « où a-t-on parlé de X » ?** → interroger `topic_log` EN PREMIER, puis
  fallback `cascading_search`. Citer `qq <session_id complet>`.
