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
