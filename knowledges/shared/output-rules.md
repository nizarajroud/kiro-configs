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
| Base | Table | Fichier HTML |
|------|-------|-------------|
| Personal Life (`appt4WObx12eJVPvK`) | Déménagement (`tblVZqY2ARz3R1CCY`) | `/mnt/c/Users/nizar/Documents/AI-GENERATED/juin-2026/personal/demenagement/html/demenagement-taches-lieu-date.html` |

**Ajout à la checklist de sortie** :
- [ ] **Table Airtable modifiée ?** → Mettre à jour le HTML correspondant avant de terminer

