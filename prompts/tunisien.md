Traduis le contenu suivant en dialecte tunisien (darija tunisienne) et publie-le sur une page Notion.

## Destination Notion

- Page parente OBLIGATOIRE : Quick-GotIt (ID: 34f174cb-5dcc-80fc-bb40-d6e91b755989)
- Créer une NOUVELLE sous-page à chaque demande
- Le TITRE de la page doit être en ANGLAIS (résumé court du sujet)
- Le contenu de la page est en tunisien

## Règles de traduction

1. Traduire le texte narratif en tunisien (arabe tunisien)
2. Garder les termes techniques en anglais/français tels quels (noms de fichiers, commandes, noms de services AWS, noms de repos, etc.)
3. Garder les blocs de code, YAML, JSON tels quels sans traduction

## Règles de formatage RTL pour Notion

1. Pour chaque bloc de texte en tunisien, encadrer avec les caractères Unicode de contrôle de direction :
   - Insérer U+202B (Right-to-Left Embedding) au DÉBUT de chaque ligne/paragraphe arabe
   - Insérer U+202C (Pop Directional Formatting) à la FIN de chaque ligne/paragraphe arabe
   - En Python : "\u202b" + texte_arabe + "\u202c"

2. Les termes techniques inline doivent être en format `code` (backticks) dans Notion — ils gardent naturellement leur direction LTR

3. Les tableaux Notion : garder les headers en tunisien (avec marqueurs RTL), mais les valeurs techniques (noms de fichiers, paths, commandes) restent en LTR sans marqueurs

4. Les titres (headings) en tunisien doivent aussi avoir les marqueurs RTL

5. Les bullet points et listes numérotées : marqueur RTL sur le texte de chaque item

## Structure de la page Notion

- Titre de la page en ANGLAIS (résumé du sujet, ex: "Flux Migration Analysis - Old vs New Mechanics")
- Emoji pertinent comme icône de page
- Callout en haut : "📝 \u202bترجمة بالتونسي للمحتوى التقني. المصطلحات التقنية محفوظة بلغتها الأصلية.\u202c"
- Garder la même structure (headings, tableaux, listes, code blocks) que le contenu original

## Exemple de transformation

Original : "Le patch-sync.yaml pointe encore vers l'ANCIEN dossier"
Tunisien avec RTL : "\u202bالـ `patch-sync.yaml` مازال يشير للدوسي القديم\u202c"

Original : "Ça veut dire que Flux déploie actuellement les workflows depuis l'ancien dossier"
Tunisien avec RTL : "\u202bهذا يعني إلي `Flux` توا يديبلوايي الـ workflows من الدوسي القديم\u202c"

## Contenu à traduire

Si du contenu est fourni ci-dessous, traduis-le. Sinon, traduis la DERNIÈRE réponse de l'assistant dans cette conversation (le message juste avant cette demande).

${1}
