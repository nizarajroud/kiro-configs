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
- **Sens d'écriture** : RTL (droite à gauche)
- **Structure de chaque puce** : TOUJOURS suivre ce format EXACT :

```
[terme/concept anglais] : [explication courte en tunisien] → [détails techniques en anglais si pertinent]
```

### ❌ INTERDIT — Prose libre en arabe

Ne JAMAIS écrire des paragraphes ou des phrases longues en arabe mélangé avec de l'anglais.

**Exemple INTERDIT :**
```
Lift and Shift : يحبّو ياخذو ال application متاعهم Oracle EBS إلّي موجودة on-premise ويحطّوها في cloud (Oracle Cloud Infrastructure) → migration يعني بدون ما يبدّلو فيها برشا
```

### ✅ OBLIGATOIRE — Format structuré, une idée par ligne

**Exemple CORRECT :**
```
• Lift and Shift : ياخذو ال app من on-premise للـ cloud → migration sans changements majeurs
• Oracle EBS : application كبيرة متاع ERP → AP, AR, GL modules
• Environnement Production : 4 CPU, 192 GB RAM → utilisation 50%
• Environnement Test : 4 CPU, 72 GB RAM → utilisation 9%
• DR : موجود في data center آخر (Ste-Julie) → disaster recovery
```

### Règles STRICTES

- **UNE idée par puce** — jamais 2 concepts dans la même ligne
- **Phrases COURTES** — max 10 mots en arabe par puce
- **Le terme anglais EN PREMIER** (à droite en RTL), suivi de `:`, suivi de l'explication tunisienne
- Ne PAS écrire de prose/paragraphes — UNIQUEMENT des puces structurées
- Ne PAS traduire les termes techniques anglais — les garder tels quels
- L'explication en arabe doit être simple, conversationnelle (comme à l'oral)
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
