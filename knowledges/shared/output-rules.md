---
inclusion: always
---
# Output Rules — Règles de formatage et d'action spéciales

## Règle : "Explication en tunisien"

**Déclencheur** : L'utilisateur demande une explication ou traduction "en tunisien" (ou formulation similaire : "explique en derja", "dis-le en tunisien", "traduis en tunisien", etc.)

### Action — Création de page Notion

1. **Si on est déjà dans le contexte d'une page Notion** → créer une **sous-page** de cette page, titrée "Explication en tunisien — [sujet]"
2. **Si on n'est PAS dans un contexte de page Notion** → créer une page sous la page **"Mes notes"**, titrée "Explication en tunisien — [sujet]"

### Format du contenu (OBLIGATOIRE — STRICT)

- **Langue** : arabe dialectal tunisien, termes techniques en anglais tels quels
- **Sens d'écriture** : RTL — chaque bloc de texte DOIT commencer par le caractère Unicode RTL mark (U+202B : `‫`)
- **Style** : prose conversationnelle naturelle (comme si tu expliques à l'oral à un tunisien). Les termes anglais sont insérés naturellement dans la phrase arabe.

### Technique RTL (CRITIQUE)

Chaque rich_text envoyé à Notion DOIT commencer par `‫` (U+202B) pour forcer le rendu RTL correct. Sans ce caractère, le bidi casse le rendu.

### ❌ INTERDIT

- Structure forcée type `[terme] : [explication] → [détails]`
- Puces avec séparation artificielle anglais/arabe
- Texte sans le caractère RTL mark au début

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
- [ ] **Explication en tunisien demandée ?** → Créer la page Notion avec caractères RTL (U+202B)
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
