---
inclusion: always
---
# Output Rules — Règles de formatage et d'action spéciales

## Règle : "Explication en tunisien"

**Déclencheur** : L'utilisateur demande une explication ou traduction "en tunisien" (ou formulation similaire : "explique en derja", "dis-le en tunisien", "traduis en tunisien", etc.)

### ⚡ EXCEPTION — "inline / dans le chat" (PRIORITAIRE)

**Déclencheur de l'exception** : L'utilisateur demande une explication tunisienne AVEC un marqueur d'emplacement indiquant qu'il la veut directement dans la conversation. Marqueurs (liste non exhaustive, **insensible à la casse**) :
- « explique-moi ici en tunisien », « en tunisien ici », « ici en tunisien »
- « tunisien inline », « dans le chat en tunisien », « sans Notion en tunisien »

**Comportement dans ce cas** :
- ❌ NE PAS créer de page Notion. Ne PAS utiliser l'outil Notion du tout.
- ✅ Répondre DIRECTEMENT dans le chat, en appliquant EXACTEMENT le même format tunisien que la règle standard :
  - Arabe dialectal tunisien, termes techniques en anglais tels quels (ne PAS les traduire).
  - **RTL — chaque bloc de texte (paragraphe, puce, heading) commence par le caractère Unicode RTL mark U+202B (`‫`) et finit par U+202C (`‬`).**
  - Prose conversationnelle naturelle ; les termes anglais s'insèrent dans la phrase arabe.
  - Markdown (titres, gras, listes) et emojis autorisés pour structurer.
  - Interdits habituels : pas de glossaire terme-par-terme, pas de pattern « terme EN — tiret — traduction AR ».

**Règle de priorité (STRICTE)** : Le marqueur « ici / inline / dans le chat / sans Notion » l'emporte TOUJOURS → réponse inline dans le chat, AUCUNE page Notion.

**Comportement par défaut (INCHANGÉ)** : Sans ce marqueur → créer la page Notion (voir ci-dessous) + afficher le lien direct.

### Action — Création de page Notion

1. **Si on est déjà dans le contexte d'une page Notion** → créer une **sous-page** de cette page, titrée "Explication en tunisien — [sujet]"
2. **Si on n'est PAS dans un contexte de page Notion** → créer une page sous la page **"Mes notes"**, titrée "Explication en tunisien — [sujet]"

**ATTENTION — "contexte d'une page Notion"** signifie UNIQUEMENT : l'utilisateur a explicitement dit "crée ça sous telle page" ou on est en train de travailler SUR une page Notion spécifique (lecture/édition en cours). Le fait d'avoir discuté d'un sujet ou d'avoir créé un speech juste avant NE constitue PAS un contexte de page Notion. En cas de doute → "Mes notes".

### Format du contenu (OBLIGATOIRE — STRICT)

- **Langue** : arabe dialectal tunisien, termes techniques en anglais tels quels
- **Sens d'écriture** : RTL — chaque bloc de texte DOIT commencer par le caractère Unicode RTL mark (U+202B : `‫`)
- **Style** : prose conversationnelle naturelle (comme si tu expliques à l'oral à un tunisien). Les termes anglais sont insérés naturellement dans la phrase arabe.

### Technique RTL (CRITIQUE)

Chaque rich_text envoyé à Notion DOIT commencer par `‫` (U+202B) pour forcer le rendu RTL correct. Sans ce caractère, le bidi casse le rendu.

### ❌ INTERDIT

- Structure forcée type `[terme] : [explication] → [détails]`
- Puces avec séparation artificielle anglais/arabe
- Pattern "terme EN — tiret — traduction AR" (même à l'intérieur d'une puce RTL)
- Traduire item par item comme un glossaire au lieu de raconter la décision
- Texte sans le caractère RTL mark au début

### Cas des listes techniques (checklist, changelog, décisions)
Quand la source est une liste de choix/décisions (ex: "on a pas ajouté X",
"on a fait Y au lieu de Z"), chaque puce doit être UNE PHRASE COMPLÈTE
en tunisien où les termes anglais s'intègrent grammaticalement —
pas juste collés après un tiret.

❌ Mauvais :
ولا FailedInvocations ولا bus_monitoring ما يحطش — Monitoring alerting

✅ Bon :
في جزء ال Monitoring، ما ضفناش ولا alerting على FailedInvocations
ولا على ApproximateAgeOfOldestMessage متاع ال bus_monitoring.

### ✅ OBLIGATOIRE — Prose naturelle avec RTL mark

**Exemple CORRECT (tel qu'envoyé à Notion) :**
```
‫انتي Machine Learning Engineer في شركة AnyCompany Financial Services، والمهمة متاعك هي بناء مساعد مالي شخصي ذكي باش يعاون العملاء يديرو الميزانيات متاعهم وياخذو قرارات مالية مدروسة.‬
```

**Puces — Exemple CORRECT :**
```
‫تفهم وتجاوب مع الأسئلة باللغة الطبيعية على المالية الشخصية‬
‫تستعمل custom tools باش تحسب وتولد visualizations‬
‫تنسق بين عدة agents متخصصين باش تحل مشاكل معقدة‬
```

**Headings — Exemple CORRECT :**
```
‫Task 1: بناء مساعد ميزانية شخصي‬
```

### Règles de rédaction

- Écrire en **prose conversationnelle** — comme si tu expliques à quelqu'un à l'oral
- Chaque puce = une phrase avec sujet + verbe en tunisien, où le terme
  anglais s'insère au milieu (pas au début suivi d'un tiret)
- Les termes techniques anglais s'insèrent **dans la phrase arabe** sans séparation
- Ne PAS traduire les termes techniques — les garder en anglais tel quel
- Chaque paragraphe, puce, heading = une unité qui commence par `‫` et finit par `‬`
- Toujours créer la page Notion AVANT d'afficher le contenu dans le chat

---

## Règle : Lien Notion après création de page

**Déclencheur** : Toute création de page Notion (quel que soit le contexte ou le sujet).

**Action OBLIGATOIRE** : À la fin de la création, toujours afficher le **lien URL direct** de la page créée pour que l'utilisateur puisse y accéder en un clic.

**Format** :
```
📄 Page créée : [Titre de la page](URL Notion)
```

**Source du lien** : Utiliser le champ `url` retourné par l'API Notion lors de la création de la page.


---

## Règle : Images dans Notion

**Déclencheur** : Toute demande d'ajout d'image à une page Notion (diagrammes, captures, visuels générés, etc.)

**Workflow OBLIGATOIRE** :
1. Sauvegarder l'image localement (format PNG/SVG)
2. Upload vers le repo GitHub `nizarajroud/notion-images` (branche main)
3. Récupérer l'URL raw de l'image : `https://raw.githubusercontent.com/nizarajroud/notion-images/main/<filename>`
4. Ajouter un bloc image dans la page Notion avec l'URL externe

**Jamais** demander à l'utilisateur de faire l'upload manuellement si le workflow automatisé est disponible.


---

## Règle : Voix TTS pour contenu tunisien / arabe

**Déclencheur** : Toute demande de lecture audio ou d'enregistrement vocal contenant du texte en arabe tunisien, en arabe standard, ou en mix arabe+anglais technique.

**RÈGLE ABSOLUE** : Utiliser la voix **Orus** via **Google TTS** (`google_tts` avec `voice: "Orus"`).

Cette voix est la plus proche du dialecte tunisien parmi toutes les voix disponibles. Aucune autre voix ne doit être utilisée pour du contenu arabe/tunisien.

**Applique indépendamment du serveur MCP** — que l'outil s'appelle `google_tts`, `tts`, `live_tts`, `record_tts`, ou tout autre nom : la voix Orus + le provider Google est obligatoire dès que le texte contient de l'arabe.

**❌ JAMAIS** : ElevenLabs, OpenAI TTS, Piper, ou toute autre voix Google pour du contenu arabe/tunisien
**✅ TOUJOURS** : `google_tts(text="...", voice="Orus")`

**Pour le contenu en français** : libre choix de voix/provider (pas de contrainte).


---

## Règle : Visual Tunisian Explanation

**Déclencheur** : L'utilisateur demande un "visual tunisian explanation", "visuel en tunisien", ou toute demande de diagramme contenant du texte arabe/tunisien mixte avec de l'anglais technique.

**Action OBLIGATOIRE** :
1. Utiliser le MCP `rtl-visual-mcp` (outil `create_rtl_mindmap` ou `create_rtl_flowchart`)
2. Passer le contenu tunisien tel quel (mix arabe + termes anglais naturels)
3. Sauvegarder le PNG localement
4. Suivre la règle "Images dans Notion" (upload GitHub → URL raw → page Notion)

**Jamais** utiliser Napkin AI, Excalidraw MCP, ou Mermaid pour du contenu RTL arabe — ces outils ne gèrent pas le bidi correctement.


---

## Règle : Emplacement des images et diagrammes générés

**Déclencheur** : Toute génération d'image, de diagramme, ou de fichier (Excalidraw, RTL Visual, Mermaid, screenshots, exports SVG/PNG, HTML, PDF, etc.).

**Emplacement OBLIGATOIRE** :

```
/mnt/c/Users/nizar/Documents/AI-GENERATED/<mois-année>/<domaine>/<sujet-sémantique>/<extension>/<nom-descriptif>.<ext>
```

- `<mois-année>` : mois en français minuscule + tiret + année (ex: `juin-2026`, `juillet-2026`)
- `<domaine>` : `personal` ou `work` selon le contexte de l'artefact
- `<sujet-sémantique>` : sous-dossier nommé par le thème/projet auquel l'artefact appartient (kebab-case, ex: `bnc`, `demenagement`, `bitbucket-arm64`, `finances`)
- `<extension>` : sous-dossier nommé par l'extension du fichier (ex: `png`, `html`, `excalidraw`, `svg`, `pdf`)
- `<nom-descriptif>` : kebab-case, descriptif du contenu (ex: `bnc-onboarding-bedrock-architecture.excalidraw`)
- Créer les dossiers manquants (mois, domaine, sujet, extension) s'ils n'existent pas encore.

**Classification domaine** :

| Domaine | Sujets |
|---------|--------|
| `personal` | demenagement, finances, famille, divers, tunisian-voice-ai |
| `work` | bnc, bitbucket-arm64, novatech, salsa, sftp, livoq |

**Exemples** :
```
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/personal/demenagement/html/cartons-demenagement-comparatif.html
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/personal/demenagement/png/plan-maison-certificat-localisation.png
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/personal/finances/html/arbitrage-celi-nizar-toutes-options.html
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/personal/famille/html/clubs-radhouane-comparatif.html
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/work/bnc/excalidraw/bnc-onboarding-bedrock-architecture.excalidraw
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/work/bnc/png/bnc-onboarding-ai-landing-zone.png
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/work/bitbucket-arm64/drawio/bitbucket-arm64-codebuild-architecture.drawio
/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/work/novatech/pdf/NovaTech-Estimation-Couts-AWS.pdf
/mnt/c/Users/nizar/Documents/AI-GENERATED/juillet-2026/work/salsa/drawio/salsa-636-appsync-public-architecture.drawio
```

**Logique de création** :
1. Déterminer le domaine (`personal` ou `work`)
2. Déterminer le sujet sémantique (projet/thème auquel l'artefact appartient)
3. Déterminer l'extension du fichier à générer
4. Vérifier si le chemin `<domaine>/<sujet>/<extension>/` existe sous `<mois-année>/`
5. S'il existe → y placer le fichier
6. S'il n'existe pas → créer les dossiers manquants puis y placer le fichier

**Détermination du sujet sémantique** :
- Se baser sur le contexte de la conversation (quel sujet est en cours de discussion)
- Le sujet doit être un mot-clé court et réutilisable (ex: `bnc`, `demenagement`, `finances`, `livoq`, `novatech`, `salsa`)
- Si un artefact est vraiment générique et n'appartient à aucun sujet → le mettre directement sous `<domaine>/` sans sous-dossier sujet (exception rare)

**Règles strictes** :
- ❌ JAMAIS `/tmp/` ni aucun autre répertoire temporaire
- ❌ JAMAIS de UUID ou noms non-descriptifs dans le nom de fichier
- ❌ JAMAIS de fichier directement sous `<mois-année>/` sans sous-dossier domaine
- ✅ La copie locale dans `AI-GENERATED/` est TOUJOURS conservée, même si l'image est ensuite uploadée sur GitHub ou intégrée dans Notion

### Ouverture automatique après génération (OBLIGATOIRE)

**Déclencheur** : Tout fichier **ouvrable** généré et sauvegardé sous `AI-GENERATED/`.

**Action OBLIGATOIRE** : Juste après la sauvegarde, ouvrir le fichier dans un nouvel
onglet du navigateur Windows déjà ouvert. Un onglet par fichier ouvrable généré.

**Extensions à ouvrir automatiquement** :
`html`, `png`, `svg`, `jpg`, `jpeg`, `gif`, `webp`, `pdf`

**Extensions EXCLUES de l'ouverture auto** (formats d'édition, pas de rendu navigateur) :
`drawio`, `excalidraw`, `d2` (fichiers source) — ne PAS tenter de les ouvrir.

**Commande OBLIGATOIRE (WSL → navigateur Windows par défaut)** :

```bash
cmd.exe /c start "" "$(wslpath -w '/mnt/c/Users/nizar/Documents/AI-GENERATED/<...>/<fichier>.<ext>')"
```

- `wslpath -w` convertit le chemin WSL en chemin Windows.
- `cmd.exe /c start "" "..."` ouvre le fichier avec le programme Windows par défaut
  (le navigateur pour html/images/pdf) → nouvel onglet dans le navigateur existant.
- Non-interactif, aucune confirmation requise.

**Règles strictes** :
- ✅ Ouvrir CHAQUE fichier ouvrable généré (un onglet par fichier).
- ✅ Ouvrir APRÈS la sauvegarde dans `AI-GENERATED/` (jamais depuis `/tmp/`).
- ❌ NE PAS ouvrir les formats d'édition (`drawio`, `excalidraw`, `.d2` source).
- ❌ NE PAS bloquer ni attendre — la commande rend la main immédiatement.

### ⚡ EXCEPTION — Contexte kiro-web (affichage inline dans le fil web)

**Principe** : Quand l'agent tourne dans l'environnement **kiro-web** (interface web), il
ne faut PAS lancer `cmd.exe` pour ouvrir le fichier dans le navigateur Windows. À la
place, kiro-web sait afficher/épingler l'artefact directement dans le fil de discussion.
La génération dans `AI-GENERATED/` reste **inchangée et obligatoire**.

**Détection du contexte kiro-web (dans cet ordre)** :

1. **Variable d'env (méthode idéale, si disponible)** : si `$KIRO_WEB` est défini
   (=`1`) → contexte kiro-web. *(À faire ajouter côté kiro-web par l'agent du code ;
   tant que non fait, utiliser la détection par process ci-dessous.)*
2. **Ancêtre de process (méthode courante, sans toucher au code)** :

```bash
pid=$$; KWEB=0
for i in $(seq 1 10); do
  ppid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' '); [ -z "$ppid" ] && break
  ps -o args= -p "$ppid" 2>/dev/null | grep -q "kiro_web" && { KWEB=1; break; }
  pid=$ppid; [ "$pid" -le 1 ] && break
done
echo "$KWEB"   # 1 = kiro-web, 0 = CLI natif
```

**Comportement selon le contexte** :

| Contexte | Génération `AI-GENERATED/` | Ouverture |
|----------|---------------------------|-----------|
| **kiro-web** (`KWEB=1`) | ✅ Toujours | ❌ PAS de `cmd.exe`. À la place, **écrire le chemin absolu du fichier généré dans la réponse** (`/mnt/c/Users/nizar/Documents/AI-GENERATED/...`) → kiro-web le détecte et l'affiche/épingle inline dans le fil web. |
| **CLI natif** (`KWEB=0`) | ✅ Toujours | ✅ `cmd.exe /c start` → navigateur Windows (comportement standard ci-dessus) |

**Règles strictes (exception kiro-web)** :
- ✅ TOUJOURS générer dans `AI-GENERATED/` quel que soit le contexte.
- ✅ En kiro-web → référencer le **chemin absolu** de CHAQUE artefact ouvrable dans la réponse (pour l'affichage inline dans le fil).
- ❌ En kiro-web → NE JAMAIS lancer `cmd.exe /c start` (ouvrirait un onglet parasite hors du fil web).
- ✅ Formats concernés par l'affichage inline : `html`, `png`, `svg`, `jpg`, `jpeg`, `gif`, `webp`, `pdf` (mêmes extensions que l'ouverture auto ; `drawio`/`excalidraw`/`d2` source exclus).


---

## Règle : Artefacts générés en contexte kiro-web

**Déclencheur** : Toute génération d'image/diagramme (D2, Excalidraw, draw.io, Mermaid,
screenshot, export SVG/PNG, etc.) quand **`KIRO_WEB=1`** (contexte kiro-web).

**Contexte technique (déjà en place — ne PAS recoder)** :
- kiro-web pose `KIRO_WEB=1` dans chaque subprocess ACP qu'il lance.
- kiro-web sert inline dans le fil tout fichier image situé dans
  `<cwd de la session>/.kiro-web-artifacts/`, via `GET /api/artifact/{session_id}/{path}`.
  Le frontend détecte automatiquement tout chemin contenant `.kiro-web-artifacts/` dans
  la réponse de l'agent et l'affiche inline (images : png, svg, jpg, jpeg, gif, webp).
- L'agent ACP tourne déjà dans le cwd de la session → écrire dans `./.kiro-web-artifacts/`
  atterrit automatiquement au bon endroit.

### Comportement OBLIGATOIRE en contexte kiro-web (`KIRO_WEB=1`)

1. **Générer une IMAGE (SVG ou PNG)** — jamais laisser uniquement le fichier source
   (`.d2`, `.drawio`, `.excalidraw`), car seul un PNG/SVG s'affiche inline.
2. **Écrire l'image dans `./.kiro-web-artifacts/<nom-descriptif>.<svg|png>`** relatif au
   répertoire de travail courant de la session. Créer le dossier `.kiro-web-artifacts/`
   s'il n'existe pas. **Ne PAS faire de recherche disque (`find`)** — le chemin est
   déterministe.
3. **Écrire aussi la copie d'archivage** dans
   `AI-GENERATED/<mois-année>/<domaine>/<sujet>/<ext>/...` (règle d'emplacement existante,
   inchangée, toujours obligatoire).
4. **Référencer, dans la réponse, le chemin ABSOLU** du fichier sous
   `.kiro-web-artifacts/` (ex : `/home/nizar/.../mon-projet/.kiro-web-artifacts/diagramme.svg`)
   → kiro-web le détecte et l'affiche inline dans le fil.
5. **NE PAS lancer `cmd.exe /c start`** en contexte kiro-web (déjà couvert par l'exception
   kiro-web existante).

### PRINCIPE GÉNÉRAL — l'agent contrôle le chemin de sortie (pas de traitement cas-par-cas)

**Principe directeur (en contexte kiro-web, `KIRO_WEB=1`)** :

> L'agent doit TOUJOURS écrire l'artefact final à un chemin déterministe qu'il contrôle
> (`./.kiro-web-artifacts/<nom>.<svg|png>`, relatif au cwd de la session). Il ne doit
> JAMAIS dépendre d'un outil qui écrit dans un emplacement inconnu, ni chercher le fichier
> après coup.

**⚡ MÉTHODE PAR DÉFAUT (chemin le plus court, latence minimale) — SVG écrit par l'agent** :

En contexte kiro-web, pour afficher un visuel inline avec le minimum de latence :

1. **Format = SVG** (le plus léger, s'affiche inline aussi bien que PNG, et l'agent peut
   l'écrire lui-même sans aucun process externe).
2. **L'agent écrit le SVG DIRECTEMENT** dans `./.kiro-web-artifacts/<nom>.svg` :
   - soit via `fs_write` (contenu SVG texte) — **méthode n°1, aucune dépendance** ;
   - soit via le **binaire local** `d2 --layout elk -o ./.kiro-web-artifacts/<nom>.svg source.d2`
     (le binaire écrit exactement au chemin fourni).
3. **Référencer le chemin absolu** dans la réponse → kiro-web l'affiche inline. Fin.

**❌ INTERDIT en contexte kiro-web** : appeler le MCP `render-d2` (ou tout MCP de rendu)
qui écrit dans un emplacement qu'il ne retourne pas de façon exploitable — c'est ce qui a
causé un `find` sur `$HOME` → déconnexion WebSocket. En kiro-web, on n'utilise PAS
`render-d2` : l'agent produit le SVG lui-même (fs_write) ou via le binaire `d2` local avec
`-o` explicite. Le MCP `render-d2` reste autorisé HORS kiro-web (CLI natif).

**Règles générales (s'appliquent à TOUT outil de génération : D2, Excalidraw, draw.io, Mermaid, screenshot, etc.)** :

1. **Interdiction absolue du `find` / scan disque** pour retrouver un fichier généré. Le
   chemin de sortie est décidé par l'agent, à l'avance — jamais découvert après coup.

2. **Choisir un outil dont l'agent contrôle le chemin de sortie.** Ordre de préférence :
   - **(a)** Un outil qui écrit directement au chemin fourni par l'agent (binaire CLI
     local avec argument de sortie, ou écriture directe du fichier par l'agent).
   - **(b)** Si le seul outil disponible retourne un chemin de sortie explicite → l'agent
     le lit dans la réponse de l'outil et copie immédiatement vers `./.kiro-web-artifacts/`
     (une seule commande `cp`, pas de recherche).
   - **(c)** Un outil qui écrit dans un emplacement inconnu/sandboxé (non retourné, ou
     inaccessible depuis le filesystem de l'agent) est **à proscrire** en contexte
     kiro-web — l'agent choisit une autre méthode.

3. **Règle des « 2 secondes / 1 essai »** : si l'artefact attendu n'est pas au chemin
   prévu immédiatement après la commande de génération, l'agent **ne cherche pas et ne
   réessaie pas la même approche** — il bascule tout de suite sur une méthode où il
   contrôle le chemin (écrire le fichier lui-même, ou un binaire local avec sortie
   explicite). Jamais deux tentatives infructueuses du même type (ça déconnecte le
   WebSocket).

4. **Écriture directe en dernier recours (toujours fiable)** : si aucun outil ne garantit
   le chemin, l'agent écrit lui-même le contenu du fichier (SVG texte, ou via un binaire
   local `outil source -o ./.kiro-web-artifacts/nom.ext`). C'est la voie de repli qui
   marche toujours.

5. **Référencer le chemin absolu** de `./.kiro-web-artifacts/<nom>` dans la réponse →
   kiro-web l'affiche inline. Copie d'archivage dans `AI-GENERATED/` conservée. Aucun
   `cmd.exe /c start`.

**Pourquoi** : un test réel a montré qu'un MCP de rendu écrivait dans un sandbox
inaccessible → l'agent a fait des `find` → 2 déconnexions WebSocket → ~11 min pour un
simple diagramme. Ce principe élimine la cause racine : on ne cherche jamais, on contrôle
le chemin dès le départ.

### Comportement hors kiro-web (`KIRO_WEB` non défini — CLI natif) : INCHANGÉ

- Génération dans `AI-GENERATED/` + ouverture via `cmd.exe /c start` (navigateur Windows),
  comme la règle actuelle. Pas de `.kiro-web-artifacts/`.

### Détection du contexte (rappel, dans l'ordre)

1. **`$KIRO_WEB=1`** → contexte kiro-web (méthode fiable, déjà active).
2. Fallback : recherche de `kiro_web` dans la chaîne des process parents (méthode existante).

### Règles strictes

- ✅ En kiro-web : toujours produire un SVG/PNG dans `./.kiro-web-artifacts/` + référencer
  son chemin absolu dans la réponse + garder la copie `AI-GENERATED/`.
- ❌ En kiro-web : ne jamais faire de `find` disque pour retrouver un fichier généré ;
  ne jamais lancer `cmd.exe /c start`.
- ✅ Le nom du fichier reste descriptif en kebab-case.


---

## Règle : Analyse de la file d'attente kiro-web

**Déclencheur** : L'utilisateur demande à un agent de « regarder / analyser / traiter /
comprendre la file d'attente » (queue) — quelle que soit la formulation : « regarde la
file », « analyse les items de la file », « qu'est-ce qu'il y a dans la file d'attente »,
« transforme la file en user stories », « check the queue », etc. (**insensible à la
casse**).

**Distinct du skill `queue-topics`** (qui ne fait QUE générer des topics 1-2 mots) : ici
l'agent **analyse le contenu** en profondeur.

**Contexte technique (source de vérité — deux bases distinctes)** :

| Base | Chemin | Rôle | Accès |
|------|--------|------|-------|
| kiro-cli | `~/.local/share/kiro-cli/data.sqlite3` | Résoudre le cwd (scope) de la session courante | Lecture seule |
| kiro-web | `$KIRO_WEB_DB` sinon `~/.local/share/kiro-web/kiro-web.sqlite3` | La file d'attente | Lecture (+ écriture `summary`/`status` si demandé) |

**IMPORTANT — la file est par DOSSIER, pas par session** : la table `queue_items` est
clé par la colonne **`scope`** (= le cwd du dossier). Toutes les sessions d'un même
dossier partagent la même file. Il faut donc lire **par scope, jamais par session_id**.

Schéma : `queue_items(session_id, position, text, summary, status, processed_at, topic_processed, created_at, scope)`.

### Procédure OBLIGATOIRE (dans cet ordre)

**1. Résoudre le scope (dossier) de la session courante**
- SID explicite dans le message → l'utiliser. Sinon fallback :

```bash
SID=$(sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT conversation_id FROM conversations_v2 ORDER BY updated_at DESC LIMIT 1")
SCOPE=$(sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT key FROM conversations_v2 WHERE conversation_id='$SID'")
```

- `SCOPE` = le cwd du dossier (ex : `/home/nizar/HomeWspce/kiro-web`).

**2. Récupérer les items de ce scope**

```bash
DB="${KIRO_WEB_DB:-$HOME/.local/share/kiro-web/kiro-web.sqlite3}"
sqlite3 "$DB" "SELECT position, status, summary, text FROM queue_items WHERE scope='$SCOPE' AND status='pending' ORDER BY position;"
```

Si aucun item n'est retourné → le dire simplement (file vide pour ce dossier). Ne rien inventer.

**3. Comprendre et analyser chaque item** — pour chaque item, produire :
- Un **titre court** (le sujet).
- Une **user story** : « En tant que [rôle], je veux [besoin], afin de [bénéfice]. »
- Le **contexte / catégorie** (bug, feature, refactor, doc, question…).
- Une **estimation de complexité** indicative (S/M/L) si pertinent.

**4. Détecter les duplications / recoupements** — signaler les items qui parlent de la
même chose ou se chevauchent, avec leurs positions, et proposer une fusion.

**5. Restituer** — présenter l'analyse structurée (une section par item + une section
« Doublons/recoupements » + une section « Regroupements suggérés » si pertinent). Utiliser
le **contexte de domaine de l'agent** (exp2 = technique, compass = perso…) pour enrichir.

**6. Ne rien modifier par défaut** (analyse en lecture seule). Modifier la file (marquer
traité, réécrire un texte, fusionner) UNIQUEMENT si l'utilisateur le demande explicitement.

### Règles strictes

- ✅ Toujours résoudre le scope (cwd) et lire `WHERE scope=...` (jamais `session_id`).
- ✅ Respecter `$KIRO_WEB_DB` s'il est défini.
- ✅ Une user story par item + détection des doublons.
- ✅ Analyse en lecture seule par défaut.
- ❌ Ne jamais inventer d'items absents de la DB.
- ❌ Ne pas confondre avec `queue-topics` (topics courts) — ici c'est une analyse approfondie.


---

## Règle : Tableaux Markdown → HTML cliquable

**Déclencheur** : La réponse contient un tableau Markdown de **3+ colonnes ET 3+ lignes**.

**Action OBLIGATOIRE** :

1. Afficher le tableau en Markdown dans le chat (contexte rapide)
2. Générer un fichier HTML stylisé et le sauvegarder dans `AI-GENERATED/<mois-année>/<nom-descriptif>.html`
3. Afficher le lien cliquable à la fin :

```
📊 Voir formaté : file:///C:/Users/nizar/Documents/AI-GENERATED/<mois-année>/<nom>.html
```

**Template HTML obligatoire** (CSS intégré) :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>TITRE</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 2rem; background: #fafafa; }
  h1 { color: #1a1a1a; font-size: 1.4rem; margin-bottom: 1rem; }
  table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  th { background: #2563eb; color: white; padding: 10px 14px; text-align: left; font-size: 0.85rem; }
  td { padding: 9px 14px; border-bottom: 1px solid #e5e7eb; font-size: 0.85rem; }
  tr:nth-child(even) { background: #f9fafb; }
  tr:hover { background: #eff6ff; }
</style>
</head>
<body>
<h1>TITRE</h1>
<table>CONTENU</table>
</body>
</html>
```

**Règles** :
- Nom du fichier : kebab-case, descriptif (ex: `clubs-radhouane-comparatif.html`)
- Ne PAS générer de HTML pour les petits tableaux (2 colonnes ou ≤3 lignes)
- Le tableau Markdown reste TOUJOURS affiché dans le chat en plus du lien


---

## Règle : MCP Discovery

**Déclencheur** : L'utilisateur demande de chercher/trouver/recommander un MCP server pour un sujet donné.

**Procédure obligatoire** (dans cet ordre de priorité) :

1. **Officiel du vendor** — Chercher dans `modelcontextprotocol/servers` (README), dans l'org GitHub du vendor (ex: `github/`, `dropbox/`, `linkedin/`), et dans la documentation officielle du produit.
2. **Plus étoilé sur GitHub** — `github.com/search?q=<topic>+mcp+server&sort=stars`
3. **Registres MCP reconnus** — Vérifier sur mcpservers.org, mcp.so, Awesome MCP Servers

**Retourner obligatoirement** :
- URL du repo
- Nombre de stars
- Date du dernier commit
- Commande d'installation
- Verdict : officiel / communautaire / non-maintenu

**Ne jamais** recommander un serveur sans avoir vérifié les 3 niveaux.


---

## ⚠️ Checklist de sortie (VÉRIFIER AVANT CHAQUE RÉPONSE)

Avant d'envoyer une réponse, l'agent DOIT scanner sa propre sortie et vérifier :

- [ ] **Tableau ≥3 colonnes ET ≥3 lignes ?** → Générer le fichier HTML dans `AI-GENERATED/<mois-année>/` + afficher le lien `📊 Voir formaté : file:///C:/Users/nizar/Documents/AI-GENERATED/...`
- [ ] **TOUT tableau (≥2 colonnes) dans le CLI ?** → Vérifier OBLIGATOIREMENT que TOUTES les colonnes sont alignées (même nombre de caractères par cellule, séparateurs = même largeur que header). **SI NON ALIGNÉ → NE PAS ENVOYER.**
- [ ] **Page Notion créée ?** → Afficher le lien URL direct : `📄 Page créée : [Titre](URL)`
- [ ] **Image/diagramme généré ?** → Sauvegarder dans `AI-GENERATED/<mois-année>/` (JAMAIS /tmp/)
- [ ] **Artefact généré en contexte kiro-web (`KIRO_WEB=1`) ?** → Écrit à un chemin déterministe `./.kiro-web-artifacts/<nom>.<svg|png>` que l'agent contrôle (jamais découvert par `find`) + chemin absolu référencé dans la réponse + copie `AI-GENERATED/` conservée. Si l'outil n'écrit pas au chemin prévu du premier coup → basculer immédiatement sur une méthode à chemin contrôlé (max 1 essai, jamais de scan disque, jamais 2 tentatives du même type).
- [ ] **Analyse de la file d'attente demandée ?** → Résoudre le scope (cwd), lire `queue_items WHERE scope=...`, produire une user story par item + détecter les doublons (lecture seule sauf demande explicite de modification).
- [ ] **Explication en tunisien demandée ?** → Créer la page Notion avec caractères RTL (U+202B)
- [ ] **Explication tunisienne demandée avec « ici / inline / dans le chat / sans Notion » ?** → Répondre DIRECTEMENT dans le chat (format RTL U+202B), NE PAS créer de page Notion
- [ ] **Visuel tunisien demandé ?** → Utiliser `rtl-visual-mcp` (JAMAIS Excalidraw/Mermaid pour du RTL arabe)

**Cette checklist est NON-NÉGOCIABLE.** Si une condition est remplie et l'action correspondante n'est pas faite, la réponse est INCOMPLÈTE.


---

## Règle : Cache Factuel des Données Extraites

**Déclencheur** : Toute extraction d'une donnée factuelle importante (montant, date, condition, échéance) obtenue via :
- Parsing d'un fichier attaché (PDF, DOC, Excel) dans Gmail
- Deep dive dans un document difficile d'accès (image-PDF, .doc binaire)
- Calcul dérivé d'un document officiel
- Correction explicite de l'utilisateur sur une donnée

**Action OBLIGATOIRE — Après avoir répondu à l'utilisateur** :

Stocker le fait extrait dans `memory-compass` (knowledge graph) avec :
1. **Le fait** : donnée claire et concise
2. **La source précise** : nom du fichier, email (expéditeur + date + sujet), page Notion, ou correction utilisateur
3. **La date d'extraction** : quand l'info a été extraite/confirmée

**Format de stockage (entity dans memory-compass)** :
- **entityName** : clé descriptive (ex: `notaire-paiement-8-juin-2026`)
- **entityType** : `fait-extrait`
- **observations** :
  - `Fait : [donnée]`
  - `Source : [type] [détails] — [date du document]`
  - `Extrait le : [date]`

**Comportement lors d'une question** :
1. Chercher dans `memory-compass` d'abord (`search_nodes`)
2. Si trouvé → répondre immédiatement avec le fait + la source
3. Si pas trouvé → extraire normalement, répondre, PUIS stocker

**Règles strictes** :
- ✅ Ne stocker QUE les faits clairs, vérifiés, avec source
- ✅ Consulter le cache EN PREMIER avant de re-parser un fichier
- ✅ Si le fait date de >6 mois, le revalider avant de le servir
- ❌ Ne PAS stocker des données volatiles (soldes de compte, statut de tâche en cours)
- ❌ Ne PAS dupliquer ce qui est déjà facilement accessible en texte (contenu lisible de pages Notion, emails textuels)
- ✅ TOUJOURS stocker ce qui provient de fichiers binaires/images difficiles à re-parser

**Ajout à la checklist de sortie** :
- [ ] **Fait extrait d'un fichier difficile ?** → Stocker dans `memory-compass` avec source avant de terminer


---

## Règle : ADR — Architecture Decision Records de vie personnelle

**Déclencheur** : Toute décision significative prise pendant une conversation, sur n'importe quel sujet personnel :
- Choix financier (institution, stratégie, investissement)
- Choix de carrière (employeur, poste, formation)
- Choix logistique (fournisseur, prestataire, service)
- Choix familial (école, activité, santé)
- Choix immobilier (travaux, assurance, hypothèque)

**Action OBLIGATOIRE — Dès qu'une décision est prise** :

Stocker dans `memory-compass` avec :
- **entityType** : `decision`
- **entityName** : clé descriptive (ex: `decision-reer-bncd-2026`)

**Format des observations** :
- `Décision : [ce qui a été décidé]`
- `Contexte : [pourquoi cette question s'est posée]`
- `Options considérées : [les alternatives évaluées]`
- `Raison du choix : [pourquoi cette option et pas les autres]`
- `Conséquences : [ce que ça implique concrètement]`
- `Date : [quand la décision a été prise]`
- `Statut : Active | Révisée | Annulée`

**Comportement** :
- Si une nouvelle discussion remet en cause une décision passée → chercher l'ADR existant, mettre à jour le statut (« Révisée ») et créer le nouvel ADR
- Si l'utilisateur demande « pourquoi on a choisi X ? » → retrouver l'ADR immédiatement
- Ne PAS stocker les micro-décisions (« on mange quoi ce soir ») — uniquement celles qui ont un impact durable (> 1 semaine)

**Ajout à la checklist de sortie** :
- [ ] **Décision prise dans la conversation ?** → Créer un ADR dans `memory-compass` avant de terminer


---

## Règle : Anti-duplication TickTick

**Déclencheur** : Toute création de rappel ou tâche TickTick.

**AVANT toute création** :

Chercher dans `memory-compass` (query: sujet + `ticktick`) si un rappel existe déjà pour ce sujet/cette date. Si oui → ne PAS créer de doublon. Informer l'utilisateur que le rappel existe déjà.

**APRÈS création** :

Stocker dans `memory-compass` avec :
- **key** : `reminder-<sujet>` (ex: `reminder-rap-remboursement-2028`)
- **memory_type** : `project`
- **contenu** : titre du rappel, date, ID TickTick

**Ajout à la checklist de sortie** :
- [ ] **Rappel TickTick créé ?** → Stocker dans memory-compass (titre + date + ID) pour éviter les doublons


---

## Règle : Nouvelle procédure en cours

**Déclencheur** : L'utilisateur demande de créer une nouvelle « procédure en cours » ou « procédure » sur un sujet donné.

**Actions OBLIGATOIRES (les deux en parallèle)** :

1. **Page Notion** — Créer une sous-page sous « Procédures en cours » (ID parent : `da0e66ac-2c07-442b-95ca-870a423498e0`) avec le titre = sujet demandé.

2. **Dossier Dropbox** — Créer un dossier à :
   ```
   /mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Procedures-en-cours/<nom-du-sujet>/
   ```
   Le nom du dossier = même nom que le titre de la page Notion (kebab-case ou tel quel selon la lisibilité).

**Règles strictes** :
- ✅ TOUJOURS créer les deux (page Notion + dossier Dropbox) ensemble
- ✅ Le titre/nom doit être identique ou très proche entre les deux
- ❌ JAMAIS créer l'un sans l'autre
- ❌ JAMAIS créer une procédure uniquement dans Notion ou uniquement sur Dropbox

**Ajout à la checklist de sortie** :
- [ ] **Nouvelle procédure demandée ?** → Créer page Notion sous `da0e66ac` + dossier Dropbox `Procedures-en-cours/`


---

## Règle : Synchronisation Airtable ↔ HTML

**Déclencheur** : Toute modification dans une table Airtable (ajout, modification, suppression d'un enregistrement).

**Action OBLIGATOIRE** : Mettre à jour le fichier HTML correspondant qui reflète le contenu de cette table.

Les deux actions sont **toujours faites ensemble** — jamais l'une sans l'autre :
1. Modifier Airtable (source de vérité)
2. Régénérer/mettre à jour le HTML qui affiche ces données

**Fichiers HTML connus par table Airtable :**
| Table | ID | Fichier HTML |
|-------|-----|-------------|
| Déménagement | `tblVZqY2ARz3R1CCY` | `personal/demenagement/html/demenagement-taches-lieu-date.html` |
| Cible-maj-adresse | `tblZOp9HUBWBehudU` | `personal/demenagement/html/changements-adresse-suivi.html` |
| Achats Déménagement | `tblnb3EwV7IJE5IHn` | `personal/demenagement/html/achats-demenagement-suivi.html` |
| Retour-inspection | `tblOa4nR5pb98NjUf` | `personal/demenagement/html/retour-inspection.html` |
| Références-entretien | `tblO1PCM2lerXOjg3` | `personal/demenagement/html/references-entretien.html` |
| Mes Services | `tblX4ohkILObOAXuT` | `personal/demenagement/html/mes-services.html` |

Tous les chemins sont relatifs à `/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/`.

**JAMAIS** modifier Airtable sans mettre à jour le HTML. **JAMAIS** demander confirmation — c'est automatique et silencieux.

**Ajout à la checklist de sortie** :
- [ ] **Table Airtable modifiée ?** → Mettre à jour le HTML correspondant avant de terminer



---

## Règle : Routage Telegram

**Déclencheur** : Toute demande d'envoi de message sur Telegram.

**Routage OBLIGATOIRE** :

| Expression de l'utilisateur | Destination | Chat ID |
|---|---|---|
| « Envoie à Abir / ma conjointe / canal Abir / cnd-Abir » | **cnd-Abir** | `6821640578` |
| « Envoie sur Telegram / mets sur Telegram / canal main / sur Telegram tout court » | **Main** (canal personnel Nizar) | `1267288999` |

**Règle par défaut** : Si l'utilisateur dit simplement « mets ça sur Telegram » sans préciser de destinataire → envoyer sur **Main** (`1267288999`).

**Règles strictes** :
- ✅ « Envoie à Abir » → cnd-Abir (6821640578)
- ✅ « Mets ça sur Telegram » → Main (1267288999)
- ✅ « Canal main » → Main (1267288999)
- ❌ JAMAIS envoyer sur cnd-Abir quand l'utilisateur n'a pas explicitement mentionné Abir/conjointe


---

## Règle : TickTick — Fuseau horaire pour les rappels

**Déclencheur** : Toute création ou mise à jour de tâche/rappel TickTick avec une heure spécifique.

**RÈGLE ABSOLUE** : L'API TickTick attend la `due_date` en **UTC**. Le fuseau de l'utilisateur est **America/Toronto (UTC-4 en été, UTC-5 en hiver)**.

**Formule de conversion OBLIGATOIRE** :
- **Été (2ème dimanche de mars → 1er dimanche de novembre)** : heure locale + 4h = UTC
  - Exemple : 5h00 local → `09:00:00+0000`
  - Exemple : 8h00 local → `12:00:00+0000`
  - Exemple : 21h00 local → `01:00:00+0000` (lendemain)
- **Hiver (1er dimanche de novembre → 2ème dimanche de mars)** : heure locale + 5h = UTC
  - Exemple : 5h00 local → `10:00:00+0000`
  - Exemple : 8h00 local → `13:00:00+0000`

**Vérification OBLIGATOIRE avant envoi** :
1. Identifier l'heure locale demandée par l'utilisateur
2. Déterminer si on est en heure d'été (EDT = UTC-4) ou heure d'hiver (EST = UTC-5)
3. Ajouter le décalage pour obtenir UTC
4. Vérifier : `heure_UTC - 4 (été) ou -5 (hiver) = heure demandée par l'utilisateur` ?

**❌ ERREUR FRÉQUENTE** : Passer l'heure locale directement dans `+0000` sans conversion. Résultat = rappel déclenché 4-5h trop tôt.

**✅ CORRECT** : `due_date="2026-06-22T09:00:00+0000"` pour un rappel à 5h00 AM Montréal en été.

**Ajout à la checklist de sortie** :
- [ ] **Rappel TickTick créé avec heure ?** → Vérifier que due_date UTC = heure locale + 4h (été) ou +5h (hiver)


---

## Règle : Cache automatique des faits structurels

**Déclencheur** : Toute extraction d'une donnée **structurelle fixe** (qui ne change pas dans le temps) obtenue via une source externe (NotebookLM, Gmail, PDF, scraping).

**Exemples de faits structurels fixes** :
- Dimensions des pièces d'une propriété
- Caractéristiques permanentes de la maison (année construction, type de fondation, superficie terrain)
- Distances entre lieux fréquentés (maison → gym, maison → école)
- Numéros de contrats/polices/dossiers
- Coordonnées de prestataires confirmés
- Données d'identité (passeports, dates de naissance, NAS)
- Adresses d'employeurs, écoles, institutions fréquentées

**Critère de jugement — stocker SI** :
1. L'information est **fixe** (ne change pas au fil du temps ou rarement)
2. L'information a été **extraite d'une source externe** (pas déjà facilement accessible en texte)
3. L'information est **susceptible d'être réutilisée** dans une future conversation

**Action AUTOMATIQUE (sans demande de l'utilisateur)** :
Stocker dans `memory-compass` avec :
- **entityType** : `fait-structurel`
- **entityName** : clé descriptive (ex: `dimensions-maison-2745-roland-therrien`)
- **observations** : le fait + la source

**NE PAS stocker** :
- Des données volatiles (soldes, statuts de tâche en cours, météo)
- Des données déjà dans un steering file local
- Des données facilement re-queryables en <5 secondes (ex: nom d'une page Notion)

**Ajout à la checklist de sortie** :
- [ ] **Fait structurel extrait d'une source externe ?** → Stocker dans `memory-compass` automatiquement


---

## Règle : Format des tableaux en session Kiro (ASCII aligné)

### ⛔⛔⛔ AVERTISSEMENT CRITIQUE — VIOLATION = RÉPONSE INCOMPLÈTE ⛔⛔⛔

**CETTE RÈGLE EST NON-NÉGOCIABLE. AUCUNE EXCEPTION. JAMAIS.**

Avant d'écrire UN SEUL caractère `|` dans une réponse :
1. STOP — Ai-je calculé les largeurs de TOUTES les colonnes ?
2. STOP — Le séparateur `|---|` a-t-il la MÊME largeur que le header ?
3. STOP — TOUTES les cellules d'une même colonne ont-elles le MÊME nombre de caractères (padding inclus) ?

**Si la réponse à l'une de ces 3 questions est NON → NE PAS AFFICHER LE TABLEAU.**

**Conséquence d'une violation** : La réponse entière est considérée INCOMPLÈTE et DÉFECTUEUSE, au même titre qu'une réponse sans source citation.

---

**Déclencheur** : Toute sortie contenant un tableau (2+ colonnes) dans une session Kiro CLI.

**RÈGLE ABSOLUE** : Ne JAMAIS utiliser de tableaux GFM Markdown non-paddés. Toujours utiliser des tableaux ASCII avec colonnes alignées par padding d'espaces.

**Format OBLIGATOIRE** :
- Chaque cellule est paddée avec des espaces pour matcher la valeur la plus large de la colonne
- La ligne de séparation (`---`) est alignée à la même largeur que le header
- Les URLs sont affichées en raw (pas de `[text](url)`), tronquées avec `…` si > 50 caractères
- Les colonnes numériques sont alignées à droite
- Appliquer automatiquement dès qu'un tableau de 2+ colonnes est produit, sans demande explicite

**❌ INTERDIT** :
```
| Prix | Annonce | Lieu |
|---|---|---|
| Gratuit | Table and art form | Longueuil |
```

**✅ OBLIGATOIRE** :
```
| Prix    | Annonce            | Lieu      |
|---------|--------------------|-----------| 
| Gratuit | Table and art form | Longueuil |
```

**Règles de padding** :
- Largeur colonne = max(largeur header, largeur valeur la plus longue) + 1 espace de chaque côté
- Séparateur = tirets (`-`) de la même largeur que la colonne
- Texte : aligné à gauche
- Nombres : alignés à droite

**Règle 1 — Cellules vides** :
Les cellules vides ne sont JAMAIS laissées vierges. Remplir avec un tiret `-` aligné à la largeur de la colonne.
- ❌ `| Gratuit |          | Longueuil |`
- ✅ `| Gratuit | -        | Longueuil |`

**Règle 2 — Compensation largeur emoji** :
Les emojis (✅ ❌ ⚠️ 🟩) font 2 caractères de large en monospace mais comptent pour 1 en longueur. Compenser en retirant 1 espace de padding après tout emoji dans une cellule.
- ❌ `| ✅ Acheté  |` (trop large)
- ✅ `| ✅ Acheté |` (1 espace en moins après emoji)

**Règle 3 — Largeur colonne** :
Calculer la largeur de colonne AVANT le rendu. = max(header, toutes les valeurs incluant cellules vides/tirets). Chaque ligne doit matcher cette largeur exactement.

**Règle 4 — Séparateur = même largeur que header** :
`| Statut   |` → `|----------|`

**Règle 5 — Contexte monospace** :
Toutes les tables sont rendues en monospace (terminal, Kiro chat). PAS de tricks proportionnels. Padding par espaces uniquement.

**Règle 6 — Troncature** :
Si une colonne Description dépasse ~45 chars, tronquer avec `…` plutôt que wrapper, pour préserver l'alignement single-line.

**Règle 7 — Word-wrap intra-cellule (lignes multiples)** :
Quand le contenu d'une cellule dépasse la largeur allouée, wrapper sur la ligne physique suivante DANS la même ligne logique. Toutes les colonnes doivent continuer sur chaque ligne wrappée avec du padding vide.

Budget de colonnes (console ~120 chars) :
```
| Statut | Article          | Fournisseur  | Prix | Description              |
| 8      | 30               | 18           | 6    | 45                       |
```

Exemple wrap :
```
| Statut    | Article                        | Fournisseur     | Prix | Description                    |
|-----------|--------------------------------|-----------------|------|--------------------------------|
| ✅ Acheté | Peinture                       | Bétonel du Luxe | -    | Expert du Luxe 140 10A, Blanc, |
|           |                                |                 |      | coquille d'œuf, 925 ml         |
|-----------|--------------------------------|-----------------|------|--------------------------------|
| À ach.    | Patins vissables feutre        | Canadian Tire   | 8$   | Protection plancher bois —     |
|           | (paq. 20)                      |                 |      | vissés dans pieds de chaise    |
```

Règles du wrap :
- Les lignes wrappées répètent la structure `|` avec des cellules vides paddées
- Un séparateur `|---|` est ajouté ENTRE chaque ligne logique (pas juste au header)
- Jamais de troncature `…` quand le wrap est actif — afficher le contenu complet
- Wrapper aux limites de mots (pas de coupure mid-word)
- Le séparateur inter-lignes utilise les mêmes largeurs que le header

**Règle 8 — Golden Rule : Pre-compute, then render (strict two-pass)** :

JAMAIS écrire le contenu et ajuster les largeurs en même temps. Toujours suivre ce processus en deux passes :

**PASS 1 — Mesure** (avant d'écrire un seul caractère) :
1. Collecter TOUT le contenu de chaque cellule, incluant les fragments wrappés
2. Pour chaque colonne : largeur minimale = max(longueur header, plus long fragment de cellule)
3. Calculer la largeur totale minimale = somme(toutes largeurs colonnes) + pipes + padding
4. **EXPANSION OBLIGATOIRE** : Si total < 120 chars → distribuer l'espace restant (120 - total) entre les colonnes proportionnellement à leur contenu. Le tableau DOIT occuper ~120 chars de large. JAMAIS un tableau étroit avec de l'espace vide à droite.
5. Si total > 120 chars → réduire la colonne la plus large d'abord, puis re-fragmenter son contenu avec word-wrap
6. Verrouiller toutes les largeurs. Elles NE CHANGENT PAS pendant le rendu

**PASS 2 — Rendu** (avec les largeurs verrouillées) :
- Chaque fragment de cellule est paddé avec des espaces pour remplir exactement sa largeur
- Les cellules de continuation vides sont remplies UNIQUEMENT d'espaces (pas de `-`, pas de `|` à l'intérieur)
- Le `|` de fermeture de chaque ligne est placé à la MÊME position caractère sur chaque ligne physique, incluant les lignes wrappées
- Les fragments de wrap sont coupés au dernier mot AVANT d'atteindre la largeur de colonne. Jamais couper À la frontière (collision avec la bordure). Laisser au moins 1 espace de marge avant le `|` de fermeture

**Vérification mentale avant output** :
- Le `|` de fermeture de la colonne N est au même index caractère sur TOUTES les lignes de la row
- Aucune cellule ne contient un `|` parasite qui appartient à la structure
- Les lignes de continuation wrappées ont UNIQUEMENT des espaces dans les colonnes sans overflow

**Scope** : Sessions Kiro CLI uniquement. Les tableaux générés pour Notion ou HTML ne sont pas concernés.


---

## Règle : Tableaux dans Notion

**Déclencheur** : Toute demande de tableau dans une page Notion.

**RÈGLE ABSOLUE** : Utiliser les blocs natifs `table` + `table_row` de l'API Notion.
JAMAIS de texte séparé par des pipes `|` dans des paragraphes.

**Format API obligatoire** :
- Créer un bloc `type: "table"` avec `table_width` = nombre de colonnes et `has_column_header: true`
- Chaque ligne = un bloc enfant `type: "table_row"` avec `cells` = array de rich_text arrays (un array par cellule)
- La première table_row = le header (noms des colonnes)

**Exemple API correct** :
```json
{
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "children": [
      {
        "type": "table_row",
        "table_row": {
          "cells": [
            [{"type": "text", "text": {"content": "Col 1"}}],
            [{"type": "text", "text": {"content": "Col 2"}}],
            [{"type": "text", "text": {"content": "Col 3"}}]
          ]
        }
      }
    ]
  }
}
```

**❌ INTERDIT** : paragraphes avec "Col1 | Col2 | Col3" — ça rend du texte brut, pas un tableau
**✅ OBLIGATOIRE** : table block natif Notion — rend un vrai tableau visuel avec cellules

**Ajout à la checklist de sortie** :
- [ ] **Tableau demandé dans Notion ?** → Utiliser table + table_row blocks natifs (JAMAIS de pipes dans des paragraphes)


---

## Règle : Speechs de maintenance

**Déclencheur** : Toute demande de préparer un speech / discours / appel vers un professionnel pour une tâche de maintenance de la maison.

**Actions OBLIGATOIRES (dans cet ordre)** :

1. **Créer le speech dans Notion** — sous le toggle "🗣️ Speechs" de la page Entretien maison (`389174cb-5dcc-8165-894e-ddbd82b0364b`), ajouter un toggle enfant nommé :
   - Format du titre : `[Nom intervenant/domaine] — [Date du jour YYYY-MM-DD]`
   - Contenu structuré OBLIGATOIRE :
     1. **Coordonnées** (EN PREMIER) — Chercher sur Internet (FireCrawl/web_search) les coordonnées du professionnel et les mettre sous forme de liste :
        - Téléphone
        - Email
        - Adresse / site web
        - Toute autre info utile (horaires, licence RBQ, etc.)
     2. **Speech recommandé** — Ce que dire au téléphone/email
     3. **Points clés à ne pas oublier** — Liste de rappels

2. **Ajouter la colonne "Speech" dans Airtable** (si elle n'existe pas encore) — table Tâches de maintenance (`tblOa4nR5pb98NjUf`)

3. **Lier le speech à la tâche** — copier l'URL du bloc Notion du speech et la mettre dans la colonne "Speech" de la tâche concernée dans Airtable

**Périmètre** : Uniquement les tâches de maintenance de la maison 2745 Roland-Therrien (table Airtable `tblOa4nR5pb98NjUf`).

**Ajout à la checklist de sortie** :
- [ ] **Speech de maintenance demandé ?** → Créer toggle dans Notion Speechs + lier dans Airtable colonne Speech


---

## Règle : Accès aux sessions de chat sur WSL distantes (via SSH)

**Déclencheur** : L'utilisateur demande de "regarder les sessions de chat", "lire la conversation sur CSBEN", "comprendre ce qui a été discuté sur l'autre WSL", ou toute référence à une session de clavardage sur une machine distante.

**Source de vérité** : Base SQLite Kiro CLI

```
~/.local/share/kiro-cli/data.sqlite3
```

Table : `conversations_v2`
Colonnes : `key`, `conversation_id`, `value` (JSON complet), `updated_at`

**Machines connues** :

| Nom SSH | Machine | Usage |
|---------|---------|-------|
| `csben` | WSL-CSBEN (Alithya/Beneva) | Projets client : SALSA, SFTP, Observabilité |

**Procédure OBLIGATOIRE** (dans cet ordre) :

1. **Lister les sessions récentes** :
```bash
sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT conversation_id, updated_at, json_extract(value, '$.history[0].user.env_context.env_state.current_working_directory'), substr(json_extract(value, '$.history[0].user.content'), 1, 120) FROM conversations_v2 ORDER BY updated_at DESC LIMIT 10"
```

2. **Présenter les sessions** à l'utilisateur avec : dossier, sujet (premier message), date

3. **Lire la session demandée** — extraire user messages + assistant responses :
```bash
sqlite3 ~/.local/share/kiro-cli/data.sqlite3 "SELECT value FROM conversations_v2 WHERE conversation_id='<ID>'"
```
Puis parser le JSON : `history[].user.content` (messages utilisateur) et `history[].assistant.content` (réponses agent)

4. **Exploiter le contexte** avec les outils enrichis de cette WSL (visuel tunisien, Notion, diagrammes, etc.)

**Raccourcis de langage** :
- "regarde sur CSBEN" / "la conversation CSBEN" / "la session SALSA" → SSH vers `csben`, lire la DB
- "la dernière session" → trier par `updated_at DESC LIMIT 1`
- "la session SALSA-XXX" → chercher dans le `current_working_directory` qui contient "SALSA-XXX"

**Règles strictes** :
- ✅ Toujours utiliser SSH MCP (`executecommand` avec `connectionName: csben`)
- ✅ La DB SQLite est la source de vérité (contenu complet user + agent + tool calls)
- ✅ Après lecture, proposer les livrables possibles (explication tunisienne, visuel, diagramme, résumé)
- ❌ JAMAIS inventer du contenu — uniquement ce qui est dans la DB
- ❌ JAMAIS modifier la DB distante — lecture seule

**Ajout à la checklist de sortie** :
- [ ] **Session distante lue ?** → Confirmer la session ID et le sujet avant d'agir dessus


---

## Règle : Recherche produit RONA — Magasin et rangée/section

**Déclencheur** : Toute demande de recherche de produit sur rona.ca (prix, disponibilité, localisation en magasin).

**Magasins de référence (par ordre de priorité)** :

| Priorité | Magasin                          | viewStore | Distance de la maison |
|----------|----------------------------------|-----------|-----------------------|
| 1        | RONA Longueuil (Roland-Therrien) | `42420`   | ~1 km                 |
| 2        | RONA+ Saint-Bruno-de-Montarville | `41040`   | ~11 km                |

**Procédure OBLIGATOIRE** :

1. Chercher le produit sur rona.ca (`firecrawl_search` avec `site:rona.ca`)
2. Scraper la page produit avec `?viewStore=42420` (Longueuil Roland-Therrien) + `waitFor=5000`
3. Extraire : **prix**, **stock**, **Rangée X | Section Y**
4. **Si le produit n'est PAS en stock à Longueuil** OU si la rangée/section n'est pas disponible → fallback avec `?viewStore=41040` (Saint-Bruno)
5. Afficher les deux magasins si le fallback est utilisé

**Format de sortie OBLIGATOIRE** :

| Info     | Valeur                              |
|----------|-------------------------------------|
| Prix     | XX,XX $                             |
| Magasin  | RONA Longueuil (Roland-Therrien)    |
| Stock    | X en magasin                        |
| Rangée   | XX                                  |
| Section  | X                                   |
| Ramassage| [info disponibilité]                |

**Règles strictes** :
- ✅ TOUJOURS afficher Rangée et Section quand disponible
- ✅ TOUJOURS utiliser Longueuil (42420) en PREMIER
- ✅ Si rupture de stock → chercher Saint-Bruno (41040) automatiquement
- ✅ Si les deux ont le produit → montrer les deux avec leurs rangées respectives
- ❌ JAMAIS utiliser un autre magasin sans demande explicite de l'utilisateur
- ❌ JAMAIS afficher un résultat sans avoir tenté d'obtenir la rangée/section

**Technique de scraping** :
- URL : `https://www.rona.ca/fr/produit/<slug>?viewStore=<code>`
- Outil : `firecrawl_scrape` avec `formats: ["markdown"]`, `onlyMainContent: true`, `waitFor: 5000`
- La rangée/section apparaît dans le markdown sous forme : `Rangée XX \| Section Y`

**Ajout à la checklist de sortie** :
- [ ] **Produit RONA cherché ?** → Vérifier que Rangée + Section sont affichées (Longueuil en premier, Saint-Bruno en fallback)


---

## Règle : Restructuration de transcription speech (Buzz)

**Déclencheur** : L'utilisateur fournit un fichier .txt de transcription et utilise une de ces formulations :
- "restructure ce speech"
- "nettoie cette transcription"
- "organise ce meeting"
- "rends ce fichier cohérent"
- "transcription Buzz"
- Ou : fournit un fichier .txt + mentionne que c'est un speech/transcription/réunion

**Input** : Fichier .txt (transcription brute Buzz — bloc monolithique sans séparation de speakers)

**Processus OBLIGATOIRE** :

1. Lire le fichier intégralement
2. Identifier les thèmes/sujets abordés → chaque changement de sujet = nouveau heading
3. Deviner les intervenants si possible (noms mentionnés dans le texte, contexte)
4. Restructurer en prose cohérente :
   - **Éliminer** : hésitations, répétitions, mots parasites ("euh", "genre", "tsé", "là")
   - **Conserver** : 100% de l'information factuelle, décisions, engagements, chiffres
   - **Fusionner** : phrases incomplètes/coupées en phrases complètes et fluides
   - **NE JAMAIS** inventer de contenu absent de l'original
   - **NE JAMAIS** supprimer une information factuelle même si elle semble mineure

**Format de sortie (dans Notion)** :
- H1 : Titre de la réunion/discussion (déduit du contenu ou demandé à l'utilisateur)
- H2 : Par thème/sujet majeur abordé
- H3 : Sous-thèmes si nécessaire
- Prose cohérente en paragraphes (pas de bullet points sauf listes explicites dans le speech)
- **Section finale "Décisions et engagements"** (si applicables)
- **Section finale "Points en suspens / À suivre"** (si applicables)

**Livrable OBLIGATOIRE** :

**Page Notion** — Créer une sous-page sous « Meetings-Reports » (ID parent : `84c17364-a96f-44a0-8a5b-235035d7deba`)
- Titre : `[Sujet] — [Date YYYY-MM-DD]`
- Contenu : le texte restructuré complet

**Détermination du domaine/sujet** : Demander à l'utilisateur si non évident du contexte (work = réunion professionnelle | personal = RDV médical, notaire, etc.)

**Langue** : Même langue que le speech original. Si mixte FR/EN → garder le mix naturel.

**Affichage final** :
```
📄 Page créée : [Titre](URL Notion)
```

**Ajout à la checklist de sortie** :
- [ ] **Transcription speech à restructurer ?** → Page Notion créée sous Meetings-Reports avec texte structuré complet


---

## Règle : Liens AWS Console dans les diagrammes Draw.io

**Déclencheur** : Toute génération de diagramme draw.io contenant des ressources AWS avec des IDs ou noms connus.

**Source de vérité** : `/home/nizar/HomeWspce/aws-console-url-patterns/patterns.yaml`

**Action OBLIGATOIRE (dans cet ordre)** :

1. **Consulter** `patterns.yaml` pour trouver le format d'URL de chaque service AWS présent dans le diagramme
2. **Appliquer** : chaque icône AWS avec un ID/nom connu → `UserObject` avec `link=` vers la console AWS
3. **Enrichir** : si un pattern utilisé n'existe PAS encore dans `patterns.yaml` :
   - Déterminer le bon format (naviguer dans la console ou demander à l'utilisateur)
   - L'ajouter dans `patterns.yaml` avec : pattern, placeholders, example, verified, discovered
   - Commit + push dans le repo `aws-console-url-patterns`

**Format draw.io obligatoire** (UserObject wrapping mxCell) :
```xml
<UserObject label="Service Name&lt;br&gt;(resource-id)" link="https://..." id="node_id">
  <mxCell style="..." vertex="1" parent="...">
    <mxGeometry ... />
  </mxCell>
</UserObject>
```

**Règles strictes** :
- ✅ TOUJOURS utiliser `UserObject` avec `link=` quand un ID/nom de resource est connu
- ✅ TOUJOURS vérifier le format dans `patterns.yaml` avant de construire le lien
- ✅ TOUJOURS commiter les nouveaux patterns découverts dans le repo
- ✅ Les patterns utilisent les NOMS des resources (pas les IDs auto-générés) quand le service l'exige
- ❌ JAMAIS deviner un format d'URL sans vérifier dans patterns.yaml
- ❌ JAMAIS générer un drawio avec des mxCell simples quand les IDs sont disponibles

**Ajout à la checklist de sortie** :
- [ ] **Diagramme draw.io avec ressources AWS ?** → Vérifier que chaque icône a un `UserObject link=` correct (consulter patterns.yaml)


---

## Règle : Liens AWS Console dans les diagrammes Draw.io

**Déclencheur** : Toute génération de diagramme draw.io contenant des ressources AWS avec des IDs ou noms connus.

**Source de vérité** : `/home/nizar/HomeWspce/aws-console-url-patterns/patterns.yaml`

**Action OBLIGATOIRE (dans cet ordre)** :

1. **Consulter** `patterns.yaml` pour trouver le format d'URL de chaque service AWS présent dans le diagramme
2. **Appliquer** : chaque icône AWS avec un ID/nom connu → `UserObject` avec `link=` vers la console AWS
3. **Enrichir** : si un pattern utilisé n'existe PAS encore dans `patterns.yaml` :
   - Déterminer le bon format (naviguer dans la console ou demander à l'utilisateur)
   - L'ajouter dans `patterns.yaml` avec : pattern, placeholders, example, verified, discovered
   - Commit + push dans le repo `aws-console-url-patterns`

**Format draw.io obligatoire** (UserObject wrapping mxCell) :
```xml
<UserObject label="Service Name&lt;br&gt;(resource-id)" link="https://..." id="node_id">
  <mxCell style="..." vertex="1" parent="...">
    <mxGeometry ... />
  </mxCell>
</UserObject>
```

**Règles strictes** :
- ✅ TOUJOURS utiliser `UserObject` avec `link=` quand un ID/nom de resource est connu
- ✅ TOUJOURS vérifier le format dans `patterns.yaml` avant de construire le lien
- ✅ TOUJOURS commiter les nouveaux patterns découverts dans le repo
- ✅ Les patterns utilisent les NOMS des resources (pas les IDs auto-générés) quand le service l'exige
- ❌ JAMAIS deviner un format d'URL sans vérifier dans patterns.yaml
- ❌ JAMAIS générer un drawio avec des mxCell simples quand les IDs sont disponibles

**Ajout à la checklist de sortie** :
- [ ] **Diagramme draw.io avec ressources AWS ?** → Vérifier que chaque icône a un `UserObject link=` correct (consulter patterns.yaml)


---

## Règle : Speechs et préparations de communication — RÈGLE D'OR (TOLÉRANCE ZÉRO)

**Déclencheur** : Toute demande de :
- Speech, discours, texte à dire à quelqu'un
- Préparation de réunion (physique, téléphone, Teams, Zoom)
- Points clés à aborder, argumentaire, script d'appel
- Formulation d'un message à transmettre oralement
- Toute communication préparatoire avant un échange (personnel OU professionnel)

**Action OBLIGATOIRE (AUCUNE EXCEPTION)** :

1. **Créer une page Notion** sous « Mes Speechs » (ID parent : `398174cb-5dcc-81e7-a48b-cab097d0e176`)
   - **Déterminer le contexte** : Personnel ou Work
   - **Personnel** (famille, santé, admin, finances, déménagement, etc.) → créer sous toggle `🏠 PERSONNEL` (ID : `398174cb-5dcc-817e-9792-c8b40f4cab4f`)
   - **Work** (client, manager, collègue, réunion pro, etc.) → créer sous toggle `💼 WORK` (ID : `398174cb-5dcc-8110-959d-ec74cf84dedc`)
   - Contenu : le speech complet, structuré (points clés, formulations, notes)

2. **EN PLUS** de tout autre livrable demandé :
   - Si l'utilisateur demande aussi d'envoyer sur Telegram → faire les deux
   - Si l'utilisateur demande aussi par email → faire les deux
   - Si l'utilisateur demande juste dans le chat → afficher dans le chat ET créer la page Notion
   - La page Notion est TOUJOURS créée, peu importe ce qui est demandé à côté

3. **Si on est dans le contexte d'une autre page Notion** (ex: Procédure en cours, Entretien maison, etc.) :
   - Créer le speech sous « Mes Speechs » (comme toujours)
   - PUIS ajouter un **lien** dans la page contextuelle qui pointe vers la page speech créée
   - Format du lien : bloc paragraphe avec `🗣️ Speech : [Titre du speech](URL de la page créée)`

**Règles strictes** :
- ✅ TOUJOURS créer sous « Mes Speechs » — peu importe le sujet (perso, travail, maintenance, médical, administratif)
- ✅ TOUJOURS en plus de ce que l'utilisateur demande (jamais à la place)
- ✅ Si contexte Notion existe → lien croisé vers le speech
- ❌ JAMAIS répondre uniquement dans le chat sans créer la page Notion
- ❌ JAMAIS créer le speech sous une autre page parent que « Mes Speechs »
- ❌ AUCUNE EXCEPTION — cette règle est absolue

**Ajout à la checklist de sortie** :
- [ ] **Speech/préparation de communication demandé ?** → Page Notion créée sous « Mes Speechs » (`398174cb`) + lien croisé si contexte Notion existant




---

## Règle : Meeting Reports — POST-réunion (TOLÉRANCE ZÉRO)

**Déclencheur** : Toute demande de restitution APRÈS un échange :
- Compte-rendu de réunion, résumé d'appel, notes de meeting
- Restructuration d'une transcription (Buzz, audio, etc.)
- "Qu'est-ce qu'on a dit/décidé pendant le call?"
- Résumé d'une rencontre (physique, téléphone, Teams, Zoom)
- Toute restitution POST-échange (personnel OU professionnel)

**Action OBLIGATOIRE (AUCUNE EXCEPTION)** :

1. **Créer une page Notion** sous « Meetings-Reports » (ID parent : `84c17364-a96f-44a0-8a5b-235035d7deba`)
   - **Déterminer le contexte** : Personnel ou Work
   - **Personnel** (médecin, notaire, école, famille, admin, etc.) → créer sous toggle `PERSONNEL` (ID : `398174cb-5dcc-807b-82cc-e3f38eea7163`)
   - **Work** (client, manager, collègue, réunion pro, etc.) → créer sous toggle `WORK` (ID : `398174cb-5dcc-801a-b98e-cf9b0de4b0ce`)
   - Titre : `[Sujet/Interlocuteur] — [Date YYYY-MM-DD]`
   - Contenu structuré :
     - Résumé des échanges
     - Décisions prises
     - Actions à faire (qui fait quoi, quand)
     - Points en suspens / à suivre

2. **EN PLUS** de tout autre livrable demandé :
   - Si l'utilisateur demande aussi d'envoyer sur Telegram → faire les deux
   - Si l'utilisateur demande aussi par email → faire les deux
   - Si l'utilisateur demande juste dans le chat → afficher dans le chat ET créer la page Notion
   - La page Notion est TOUJOURS créée, peu importe ce qui est demandé à côté

3. **Si on est dans le contexte d'une autre page Notion** (ex: Procédure en cours, Entretien maison, etc.) :
   - Créer le meeting report sous « Meetings-Reports » (comme toujours)
   - PUIS ajouter un **lien** dans la page contextuelle qui pointe vers la page créée
   - Format du lien : bloc paragraphe avec `📋 Report : [Titre du report](URL de la page créée)`

**Règles strictes** :
- ✅ TOUJOURS créer sous « Meetings-Reports » — peu importe le sujet
- ✅ TOUJOURS en plus de ce que l'utilisateur demande (jamais à la place)
- ✅ Si contexte Notion existe → lien croisé vers le report
- ❌ JAMAIS répondre uniquement dans le chat sans créer la page Notion
- ❌ JAMAIS créer le report sous une autre page parent que « Meetings-Reports »
- ❌ AUCUNE EXCEPTION — cette règle est absolue

**Ajout à la checklist de sortie** :
- [ ] **Compte-rendu/résumé post-réunion demandé ?** → Page Notion créée sous « Meetings-Reports » (`84c17364`) + lien croisé si contexte Notion existant


---

## ⚠️ Checklist de sortie (VÉRIFIER AVANT CHAQUE RÉPONSE)

Avant d'envoyer une réponse, l'agent DOIT scanner sa propre sortie et vérifier :

- [ ] **Speech/préparation de communication créé ?** → OBLIGATOIREMENT créer une **PAGE** (pas un toggle, pas un bloc) sous « Mes Speechs » (ID : `398174cb-5dcc-81e7-a48b-cab097d0e176`), **DANS** le toggle correspondant :
  - Sujet personnel (santé, famille, admin, finances) → parent = toggle 🏠 PERSONNEL (`398174cb-5dcc-817e-9792-c8b40f4cab4f`)
  - Sujet professionnel (client, manager, collègue) → parent = toggle 💼 WORK (`398174cb-5dcc-8110-959d-ec74cf84dedc`)
  - **Le parent de la page DOIT être l'ID du toggle, PAS l'ID de "Mes Speechs"**. JAMAIS un toggle. JAMAIS ailleurs. Si contexte existant → ajouter un lien croisé.
- [ ] **Page Notion créée ?** → Afficher le lien URL direct : `📄 Page créée : [Titre](URL)`
- [ ] **Explication en tunisien demandée ?** → Créer la page Notion avec caractères RTL (U+202B)
- [ ] **Explication tunisienne demandée avec « ici / inline / dans le chat / sans Notion » ?** → Répondre DIRECTEMENT dans le chat (format RTL U+202B), NE PAS créer de page Notion
- [ ] **Tableau ≥3 colonnes ET ≥3 lignes ?** → Générer le fichier HTML dans `AI-GENERATED/<mois-année>/`
- [ ] **Image/diagramme généré ?** → Sauvegarder dans `AI-GENERATED/<mois-année>/` (JAMAIS /tmp/)
- [ ] **Artefact généré en contexte kiro-web (`KIRO_WEB=1`) ?** → Écrit à un chemin déterministe `./.kiro-web-artifacts/<nom>.<svg|png>` que l'agent contrôle (jamais découvert par `find`) + chemin absolu référencé dans la réponse + copie `AI-GENERATED/` conservée. Si l'outil n'écrit pas au chemin prévu du premier coup → basculer immédiatement sur une méthode à chemin contrôlé (max 1 essai, jamais de scan disque, jamais 2 tentatives du même type).
- [ ] **Analyse de la file d'attente demandée ?** → Résoudre le scope (cwd), lire `queue_items WHERE scope=...`, produire une user story par item + détecter les doublons (lecture seule sauf demande explicite de modification).
- [ ] **Visuel tunisien demandé ?** → Utiliser `rtl-visual-mcp` (JAMAIS Excalidraw/Mermaid pour du RTL arabe)

**Cette checklist est NON-NÉGOCIABLE.** Si une condition est remplie et l'action correspondante n'est pas faite, la réponse est INCOMPLÈTE.


---

## Règle d'or : Inventaires → Airtable est la source de vérité

**Déclencheur** : Toute question, confirmation ou action concernant :
- L'inventaire des équipements de la maison (thermopompe, climatiseur, électroménagers, domotique, sécurité, etc.)
- L'inventaire des outils de maintenance (tondeuse, perceuse, pelles, etc.)
- Un accessoire, une pièce ou un consommable lié à un équipement de l'inventaire (ex: filtre de climatiseur, ampoule, batterie de perceuse, télécommande, serrure)
- La confirmation d'un achat d'un item en relation avec l'inventaire

**Action OBLIGATOIRE** : Consulter DIRECTEMENT la table Airtable comme source de vérité, AVANT toute autre source (Notion, mémoire, etc.).

**Table de référence** :
- **Base** : Personal Life (`appt4WObx12eJVPvK`)
- **Table** : Inventaire équipements (`tblX7FALSiSXiMv2S`)
- **URL** : https://airtable.com/appt4WObx12eJVPvK/tblX7FALSiSXiMv2S
- **Champs** : Équipement, Catégorie, Marque / Modèle, Emplacement, Consigne / Configuration, Fonctionnement / Notes, Année / Date d'acquisition, Provenance / Achat, Prix payé, Statut, Entretien requis, Fréquence entretien, Manuel / Lien, Tâche maintenance liée

**Catégories** : CVC / Climatisation · Électroménagers · Sécurité · Serrures & Quincaillerie · Électronique / Domotique · Éclairage · Portes & Ouvertures · Outils de maintenance · Extérieur / Terrain · Mobilier / Rangement · Plomberie

**Comportement** :
1. **Question sur un équipement/outil** → lire l'enregistrement correspondant dans Airtable (`search_records` ou `list_records`) et répondre avec les infos (marque, modèle, emplacement, consigne, entretien).
2. **Achat confirmé d'un nouvel équipement/outil** → créer l'enregistrement dans Airtable avec la bonne catégorie + toutes les infos connues.
3. **Accessoire/pièce lié** (ex: filtre du Danby, ampoule E26) → retrouver l'équipement parent dans Airtable pour donner les specs compatibles (modèle, dimensions, type).
4. **Notion** : ne contient plus qu'un lien vers Airtable. Ne PAS chercher dans Notion pour l'inventaire — aller directement à Airtable.

**Règles strictes** :
- ✅ TOUJOURS Airtable en premier pour toute question d'inventaire équipements/outils
- ✅ TOUJOURS créer/mettre à jour l'enregistrement Airtable lors d'un achat confirmé lié à l'inventaire
- ❌ JAMAIS répondre de mémoire seule pour une info d'inventaire sans vérifier Airtable
- ❌ JAMAIS chercher l'inventaire dans Notion (obsolète — juste un lien)

**Ajout à la checklist de sortie** :
- [ ] **Question/achat lié à l'inventaire équipements ou outils ?** → Consulter/mettre à jour la table Airtable `tblX7FALSiSXiMv2S` (source de vérité)


---

## Règle d'or : Fermeture des stories GitHub après déploiement prod (TOLÉRANCE ZÉRO)

**Déclencheur** : Tout déploiement en production d'une fonctionnalité tracée par une issue/story GitHub (ex: `git checkout <tag>` dans le dossier prod + restart du service).

**Action OBLIGATOIRE (AUCUNE EXCEPTION)** : Dès que le déploiement prod est confirmé (service actif + vérification), FERMER immédiatement l'issue/story GitHub correspondante (`update_issue` avec `state: closed`). Fermer aussi l'épic parent quand toutes ses sous-issues sont fermées.

**Règles strictes** :
- ✅ Déploiement prod confirmé → fermeture GitHub dans la foulée, sans que l'utilisateur le demande
- ✅ Épic → fermé quand toutes les sous-issues sont fermées
- ✅ Fermer avec `state_reason: completed`
- ❌ JAMAIS laisser une story "done" ouverte après une mise en prod
- ❌ JAMAIS attendre que l'utilisateur demande de fermer

**Ajout à la checklist de sortie** :
- [ ] **Mise en prod d'une story tracée GitHub ?** → Fermer l'issue (+ l'épic si toutes les sous-issues sont fermées) immédiatement


---

## Règle d'or : Fichier Excel `suivi-des-affaires.xlsx` = source de vérité (disponibilités, vacances, sorties, finances)

**Chemin** : `/mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Procedures-en-cours/Suivi-des-affaires-perso/suivi-des-affaires.xlsx`

**Déclencheur** : Toute question, planification ou action concernant :
- La **disponibilité des membres de la famille** (Nizar, Abir, Yasmine, Radhouane)
- La **planification de vacances**
- La **planification de sorties / événements**
- Un **nouveau club / activité / inscription**
- Les **finances** (revenus, dépenses, cotisations, allocations)

**Action OBLIGATOIRE** :

1. **Consulter ce fichier EN PREMIER** comme source de vérité pour connaître la disponibilité de chaque membre de la famille avant de planifier quoi que ce soit (sortie, vacances, rendez-vous, événement).
   - Onglet **`Absence-Calendrier-2026`** : congés/fériés/pédago + sessions (début/fin) des clubs → indique QUAND chaque membre est occupé/libre.
   - Onglet **`Routine-Club-2026`** : routine hebdomadaire des clubs.
   - Onglet **`Main-finance-2026`** : finances (déjà couvert par la règle finances/Excel existante).

2. **Écrire noir sur blanc dans ce fichier** dès qu'il y a :
   - Un **nouvel événement** ou une **sortie** planifiée
   - De **nouvelles vacances**
   - Un **nouveau club / activité / session** (ajouter une ligne dans la section Sessions de `Absence-Calendrier-2026`)
   - Une info financière (onglet finances)

3. **Se référer à la disponibilité** des membres (via `Absence-Calendrier-2026`) pour répondre à toute question du type « est-ce que X est libre tel jour ? », « quand peut-on planifier Y ? », « y a-t-il un conflit ? ».

**Structure de `Absence-Calendrier-2026`** :
- Section « Sessions — Début et Fin » (colonne Session : « Session Automne », « Session 2026-2027 », etc. — extensible pour futures sessions hiver/printemps)
- Calendrier vertical mois par mois (sept 2026 → juin 2027), sections repliables, avec 🟡 jaune = absence, 🟢 D = début session, 🟠 F = fin session.

**Règles strictes** :
- ✅ TOUJOURS consulter ce fichier avant de planifier une sortie, des vacances, un événement ou de répondre à une question de disponibilité familiale.
- ✅ TOUJOURS y inscrire tout nouvel événement/sortie/club/vacances.
- ✅ Respecter la règle Excel (demander la fermeture avant écriture) et relire l'état actuel avant de modifier (l'utilisateur fait des modifications manuelles).
- ⚠️ Le dossier a été renommé : `Suivi-des-affaires-perso` (anciennement `Suivi-tresorie-perso`).
- ❌ JAMAIS planifier une sortie/vacances sans vérifier les disponibilités dans ce fichier.

**Ajout à la checklist de sortie** :
- [ ] **Planification (sortie/vacances/événement) ou question de disponibilité famille ?** → Consulter/mettre à jour `suivi-des-affaires.xlsx` (onglet Absence-Calendrier-2026) — source de vérité.


---

## Règle d'or : Liens YouTube toujours cliquables (TOLÉRANCE ZÉRO)

**Déclencheur** : Toute demande impliquant la fourniture d'un ou plusieurs liens YouTube (vidéo, tutoriel, review, transcript, chaîne, playlist) — quelle que soit la formulation.

**Action OBLIGATOIRE** : Donner le lien YouTube **cliquable directement**, sous forme d'URL complète commençant par `https://www.youtube.com/watch?v=<id>` (ou `https://youtu.be/<id>`), affichée telle quelle dans la réponse pour qu'elle soit cliquable immédiatement.

**Règles strictes** :
- ✅ TOUJOURS afficher l'URL complète `https://www.youtube.com/watch?v=<videoId>` — jamais juste l'ID de la vidéo
- ✅ Le lien principal recommandé doit être mis en évidence et cliquable
- ✅ Si plusieurs vidéos sont listées dans un tableau, mettre l'URL complète cliquable (pas `youtube.com/watch?v=...` tronqué sans `https://`)
- ❌ JAMAIS donner uniquement un `videoId` seul (ex: `TO6JnXgP-rg`) sans l'URL complète
- ❌ JAMAIS tronquer le lien d'une façon qui le rend non-cliquable

**Ajout à la checklist de sortie** :
- [ ] **Lien(s) YouTube fourni(s) ?** → Vérifier que chaque lien est une URL complète `https://www.youtube.com/watch?v=<id>` cliquable directement
