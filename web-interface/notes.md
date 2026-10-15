# Web Interface — notes de travail (mémoire projet)

Wrapper web autour de `kiro-cli acp` : reproduit `qq` (agents Kiro) dans une page web
avec rendu markdown/tableaux lisible. Basé sur le fork de `aws-samples/sample-kiro-acp-ui`.

## État actuel — Phase 1 (MVP) : ✅ TERMINÉE
## Évolution — Menu de sessions (comme `qq -r`) : ✅ TERMINÉE

Pipeline validé de bout en bout :
`Navigateur ↔ WebSocket ↔ FastAPI (app.py) ↔ kiro-cli acp ↔ agents Kiro`

- Backend `app.py` : FastAPI, sert `static/index.html`, WebSocket `/ws`, endpoint `GET /api/sessions`
- 1 connexion WS = 1 subprocess `kiro-cli acp` dédié (spawn, handshake, create_session, set_mode)
- Streaming des réponses (chunks) → WS → rendu markdown incrémental côté navigateur
- Frontend `static/index.html` : chat dark, marked.js + highlight.js, tableaux stylés, sélecteur d'agent + **sélecteur de session**
- Réutilise SANS modification la couche ACP : `src/kiro_acp_chat_client/{process_manager,acp_client,models}.py`

### Menu de sessions — reproduit `qq -r` À L'IDENTIQUE (zéro divergence)
- `list_recent_sessions()` dans app.py = copie exacte de la logique `qq -r` :
  fenêtre 24h (`time()-86400`), `allowed_agents={exp2,compass,forge,it-supervisor}` (light exclu),
  tri `updated_at DESC`, dédup par sid, `_human_date()` (français : "Il y a X min", "Ce matin a HH:MM"...),
  topics depuis `~/.kiro/sessions/topics.db`, format `{folder[:16]}-via-{agent}`.
- Dropdown "Session" dans le header : `➕ Nouvelle session` + liste `nom · date · N msgs · topic`.
- **Reprise** : sélectionner une session → WS envoie `session_id` → `session/load` → l'historique
  est REJOUÉ (session/update: user_message_chunk/agent_message_chunk/tool_call) et reconstruit dans le chat.
- L'agent réel de la session repris est lu depuis la DB (`_agent_for_session`) — PAS le currentModeId
  ACP (qui vaut kiro_default) — puis ré-appliqué via set_mode. Testé : reprise metaflow → agent=exp2 ✅.
- session/load valide : capability loadSession=True, replay confirmé (83 updates sur session test).

### Fix troncature du replay (important)
- BUG : une réponse assistant = plusieurs `agent_message_chunk` entrecoupés de `tool_call`.
  L'ancien code faisait flush() sur chaque tool_call → réponse coupée après le 1er fragment
  (symptôme : "seulement les 3 premières lignes" à la reprise d'une session).
- FIX : flush UNIQUEMENT sur changement de rôle (user↔assistant). Les tool_call ne terminent
  PAS un message — ils sont bufferisés (pending_tools) et émis en notes APRÈS le message complet.
### Parité complète avec qq — hooks pre/post-session : ✅ TERMINÉE
Le web reproduit maintenant TOUT le comportement de qq autour d'une session :
- **SQLite** : automatique via `kiro-cli acp` (chaque tour sauvé dans data.sqlite3) — sessions visibles dans `qq -r`.
- **Pre-flight** (startup serveur) : `~/.kiro/hooks/sync-catchup.py` (rattrape sessions manquées).
- **Post-session** (fermeture WS, dans le `finally`) : `post_session_sync(sid)` lance en background :
  - `~/.kiro/hooks/sync-session-to-memory.py <sid>` → AgentCore Memory
  - `PROC/.../kiro-kb-sync.py one <sid>` → Knowledge Base
  - `PROC/.../session-catalog.py enrich-one <sid>` → topics/tags
- `_run_bg()` = subprocess.Popen détaché (start_new_session), équivalent du `&` de qq.
- Testé : startup logue "sync-catchup launched", fermeture WS logue "post-session sync for <sid>".
- Donc cascading_search / qq -t / mémoire cross-session voient AUSSI les sessions menées via le web.

### Boutons Démarrer / Arrêter session (UI)
- **▶ Démarrer session** : SEUL déclencheur de connexion. Les dropdowns (agent/session) sont inertes ;
  on choisit agent + session, puis clic → connexion (nouvelle ou reprise avec historique).
  Au chargement de la page, AUCUNE connexion auto.
- **⏹ Arrêter session** : envoie `{type:"stop"}` au backend → lance immédiatement `post_session_sync(sid)`
  (Memory + KB + catalog), renvoie `{type:"stopped"}`, UI confirme "sync lancé ✓" + rafraîchit la liste.
  Équivaut à fermer l'onglet, mais explicite et avec feedback.
- Flag `synced` côté backend : évite le double-sync entre le stop explicite et le `finally` (fermeture WS).
- Testé : stop → log "post-session sync for <sid>" + message "stopped" reçu.

### Refonte layout Meta AI (sidebar) : ✅ TERMINÉE
- Layout 2 colonnes : SIDEBAR (280px) + MAIN.
- Sidebar : bouton "✏️ Nouveau chat" + liste des sessions **filtrée par l'agent** sélectionné en haut.
  Chaque item = topic (ou nom) + "date · N msgs". Session active surlignée.
- Header (main) : dropdown agent. Changer d'agent → re-filtre la sidebar UNIQUEMENT (pas de connexion).
- **Clic sur une session** → démarrage immédiat avec historique (plus de bouton Démarrer/Arrêter).
- **✏️ Nouveau chat** → nouvelle session avec l'agent courant.
- **Hooks au switch** : startConnection() ferme le WS courant AVANT d'ouvrir le nouveau →
  le `finally` backend lance post_session_sync(sid) de la session quittée (parité qq garantie sans bouton).
- Les boutons Démarrer/Arrêter et le vieux dropdown session sont supprimés (remplacés par la sidebar).
- Testé E2E : éléments présents, filtrage par agent OK, hooks au switch confirmés (log post-session sync).

### Raffinements sidebar : ✅ TERMINÉS
- **Badge couleur par agent** : petit rond coloré devant chaque session (exp2=bleu, compass=vert,
  forge=orange, light=violet, it-supervisor=rouge, media1=rose). Map AGENT_COLORS côté JS.
- **Regroupement par date** : en-têtes "Aujourd'hui" / "Hier" / "Plus ancien" (helper dateGroup()
  basé sur updated_ms, ajouté au listing backend).
- **Suppression de session** : bouton 🗑 au survol → confirm() → DELETE /api/sessions/{sid}
  (supprime toutes les lignes conversations_v2 pour ce conversation_id). Si session active supprimée,
  reset de la zone chat. Endpoint testé safe (session inexistante → deleted:0).
### Source de vérité partagée qq ↔ web : ✅ TERMINÉE (zéro divergence)
- PROBLÈME : la logique de listing `qq -r` était dupliquée (bash dans common-functions.bash +
  Python dans app.py). Une évolution de qq n'aurait PAS suivi dans le web.
- SOLUTION : script Python unique `PROC/xxxxuseful-scripts/session-query.py` :
  - `recent` → format d'affichage qq -r (tab-séparé, sid_short, padding) — pour le CLI
  - `recent --json` → liste JSON (session_id, cwd, agent, name, date, updated_ms, msgs, topic) — pour le web
  - `agent <sid>` → agent (current_profile) d'une session
- Extraction FIDÈLE validée par `diff` strict : sortie identique à l'ancien bloc -r (0 différence).
- **qq** (common-functions.bash) : le bloc python inline de -r (lignes 1301-1373) remplacé par
  `recent_list=$(python3 .../session-query.py recent)`. Parsing aval (sid/cwd/agent → _qq_resume) intact.
  Sauvegarde avant modif : /tmp/common-functions.bash.bak-*. Syntaxe bash validée, fonctions OK.
- **web** (app.py) : list_recent_sessions() et _agent_for_session() appellent session-query.py en subprocess.
  Helpers dupliqués supprimés (_human_date, _TOPICS_DB, _ALLOWED_AGENTS). _DB_PATH gardé (DELETE endpoint).
- RÉSULTAT : modifier la logique -r dans session-query.py → CLI ET web suivent automatiquement.
- Ce qui était DÉJÀ partagé (inchangé) : agents/.kiro/ (via kiro-cli acp), DB SQLite, scripts de hooks.

## Démarrage

```bash
cd ~/HomeWspce/kiro-configs/web-interface
./start.sh                      # http://127.0.0.1:8770
PORT=9000 ./start.sh            # port custom
KIRO_WEB_AGENT=compass ./start.sh
```

Puis ouvrir http://127.0.0.1:8770 dans le navigateur.

## Variables d'environnement

| Var | Défaut | Rôle |
|-----|--------|------|
| `PORT` | `8770` | Port du serveur |
| `HOST` | `127.0.0.1` | Interface d'écoute |
| `KIRO_WEB_AGENT` | `exp2` | Agent par défaut |
| `KIRO_WEB_CWD` | `~/HomeWspce/kiro-configs` | Dossier de la session ACP (charge la config .kiro/) |

## Décisions techniques

- **Option A** (subprocess `kiro-cli acp`) retenue vs API directe — réutilise 100% de la config `.kiro/` (agents, MCPs, steering) via symlink kiro-configs.
- **1 subprocess par connexion WS** — isolation simple ; un onglet = une session.
- **Auto-approve des permissions d'outils** en MVP (choisit l'option "allow"/première). À raffiner en Phase 2+ (prompt UI).
- **FastAPI + uvicorn + websockets** dans un venv dédié `.venv/` (jamais global).
- Capabilities ACP confirmées : `loadSession=True` → reprise de session possible (pour Phase 3).

## Faits validés (smoke tests)

- `kiro-cli 2.21.1`, mode `acp` OK
- Modes = agents : exp2, compass, forge, it-supervisor, light, media1, sandbox, kirocrew*, kiro_default/planner/guide
- `set_mode`, `send_prompt` (streaming), `session/load` : tous OK

## Reste à faire (phases suivantes — NON commencées)

- **Phase 2** : sélecteur d'agent piloté par les `modes` réels renvoyés par l'ACP (au lieu de la liste hardcodée dans index.html) + choix du cwd/dossier depuis l'UI + sélecteur de modèle.
- **Phase 3** : intégrer la logique `qq` — agent auto selon le dossier (lire `~/.local/share/kiro-cli/data.sqlite3`), reprise de session via `session/load`, liste des sessions récentes.
- Permissions d'outils : remplacer l'auto-approve par un vrai prompt dans l'UI.
- Gestion multi-onglets / nettoyage des subprocess orphelins.

### Affichage inline des diagrammes/images AI-GENERATED : ✅ TERMINÉE
- Comme Claude online : quand un agent génère un fichier dans AI-GENERATED, l'image s'affiche
  directement dans le flux de discussion.
- **Backend** : route GET /ai-generated/{path:path} sert les fichiers de
  /mnt/c/Users/nizar/Documents/AI-GENERATED (lecture seule, anti path-traversal via resolve+startswith).
- **Frontend** : enrichAIGenerated(bubble) scanne le texte de la bulle, détecte tout chemin
  AI-GENERATED (Windows C:\..\ ou WSL /mnt/c/..), le convertit en /ai-generated/<rel encodé>.
  - Images (png/svg/jpg/jpeg/gif/webp) → <img> inline (maxWidth 100%, clic=zoom) + lien plein écran.
  - Sources (drawio/d2/excalidraw/pdf/html) → lien 📎 cliquable.
  - Appelée dans addMsg (historique repris) + handler 'done' (streaming live, après réponse complète).
- Testé E2E : détection Windows+WSL, image servie 200 (image/svg+xml), path traversal bloqué.

### Streaming : input toujours actif
- Pendant qu'une réponse streame, le champ de saisie reste ACTIF + focus (on peut taper la question
  suivante). Seul le bouton Envoyer (et Entrée) est bloqué pendant le streaming (flag `streaming`,
  fonction updateSendState) — évite 2 prompts simultanés au subprocess ACP.

### Auto-focus permanent
- Le curseur reste dans la saisie : refocus au clic dans le vide, au retour sur l'onglet, et dès
  qu'on tape un caractère (si session prête).

### Sidebar = toutes les sessions (option B)
- La sidebar montre TOUTES les sessions 24h (tous agents), badge couleur par agent + nom X-via-agent.
  Le dropdown agent en haut ne filtre plus — il choisit juste l'agent du prochain "Nouveau chat".

### Liens en nouvel onglet + reconnexion auto + lecture pendant génération
- **Liens _blank** : tous les <a> des bulles (markdown) → target=_blank rel=noopener (addMsg + chunk live).
  Résout le cas "clic sur lien = perte de session".
- **Reconnexion auto** : flags intentionalClose + reconnectTimer. ws.onclose inattendu (F5, veille,
  réseau, restart serveur) → reconnexion après 1.5s sur la session active (activeSessionId).
  startConnection() marque intentionalClose=true pour ne PAS reconnecter lors d'un switch volontaire.
  visibilitychange → reconnecte au retour sur l'onglet si WS fermé. onopen renvoie session_id pour reprendre.
- **Lecture pendant génération** : maybeScroll() / isNearBottom() — auto-scroll SEULEMENT si l'utilisateur
  est déjà en bas (<120px). Permet de remonter lire pendant que ça streame sans être ramené en bas.
  Le message user envoyé force toujours le scroll (addMsg). Le replay history_tool force aussi.

### Système d'onglets hybride (4 chauds LRU + reste tiède) : ✅ TERMINÉE
- Refonte complète de static/index.html autour d'un modèle multi-onglets (Tab objects).
- **Barre d'onglets horizontale** (#tabbar) au-dessus de la zone de chat (#panes). Un .pane DOM par onglet
  (affiché/caché via .active) → chaque onglet garde son historique en mémoire (DOM).
- **Clic session sidebar** → openSessionInTab : ouvre un NOUVEL onglet (ou active si déjà ouvert).
  ✏️ Nouveau chat → nouvel onglet avec l'agent du dropdown.
- **Pool chaud/tiède (LRU), MAX_HOT=4** :
  - 🟢 chaud = WS + subprocess kiro-cli acp vivant → frappe instantanée.
  - 🟡 tiède = historique en mémoire (DOM), pas de subprocess. Réactivation ou envoi → redevient chaud.
  - makeHot évince le LRU des hot tabs (makeWarm ferme son WS → hooks backend) si pool plein.
  - Chaque onglet a son WS indépendant (connectTab) + auto-reconnect si hot.
- **Hooks** : à l'éviction hot→warm ET à la fermeture d'onglet, le WS se ferme → post_session_sync backend.
- **send() sur onglet tiède** : makeHot + bufferise le prompt (_pending) + waitReadyThenSend après reconnexion.
- Backend INCHANGÉ (gère déjà N WS = N subprocess). Config MAX_HOT ajustable côté JS.
- Testé: 2 WS/subprocess parallèles (réponses distinctes) + logique LRU (5 onglets → 4 chauds/1 tiède,
  réactivation évince correctement le nouveau LRU).

### Blindages inspirés de aws-samples/sample-acp-bridge : ✅ TERMINÉS
Parsing du code réel de sample-acp-bridge (src/acp_client.py) → 3 techniques de robustesse reprises :
- **#1 Kill du groupe de process** (process_manager.py) : spawn avec start_new_session=True (groupe),
  shutdown() = os.killpg(getpgid(pid), SIGTERM) puis SIGKILL sur le groupe (fallback send_signal).
  → tue kiro-cli acp ET ses MCP servers enfants. Fix fuite d'orphelins. Testé: 0 orphelin après fermeture.
- **#2 Health check ping()** (acp_client.py) : JSON-RPC 'ping' → True si répond (même erreur=vivant),
  False si process mort/timeout. stream_prompt() vérifie pm.is_running avant d'envoyer → ProcessTerminatedError
  si mort (frontend reconnecte). Testé: ping vivant=True, après shutdown=False.
- **#3 TTL cleanup idle** (app.py) : ACPSession.last_active + touch() (dans stream_prompt). Registre global
  _active_sessions. Tâche _idle_janitor (startup) scanne toutes les 5min, ferme sessions idle > IDLE_TTL_SECONDS
  (défaut 2h, env KIRO_WEB_IDLE_TTL) avec post_session_sync (hooks qq) + shutdown (killpg). Testé.
- Idées NON retenues (bonus futurs) : pidfile ghost-cleanup au restart, limites dures max_processes.
- Décision: rester en WebSocket (pas SSE) — cas local WSL, reconnexion déjà codée, bidirectionnel+multi-onglets.
- Test E2E final: startup logue janitor+catchup, session complète sans régression, endpoints 200, 0 orphelin.

### Bouton Envoyer ↔ Stop (interruption) : ✅ TERMINÉE
- Pendant le streaming, le bouton "Envoyer" devient "⏹ Stop" (rouge, classe #send.stop), toujours cliquable.
- Clic sur Stop → envoie {type:'cancel'} au backend.
- Backend: stream_prompt tourne comme asyncio.Task annulable (prompt_task). Message 'cancel' → prompt_task.cancel()
  → dans _run_prompt, CancelledError → acp.cancel(session_id) (session/cancel ACP) + envoie {type:'cancelled'}.
- Frontend: message 'cancelled' → hideThinking, finalise la bulle courante, ajoute note "⏹ Interrompu", streaming=false.
- 'stop' (fermeture session) annule aussi le prompt_task en cours avant les hooks.
- Testé en réel: prompt long → cancel → 'cancelled' reçu ✅.
