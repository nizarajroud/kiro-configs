---
inclusion: always
---
# Output Rules — Règles de formatage et d'action spéciales

## Règle : "Explication en tunisien"

**Déclencheur** : L'utilisateur demande une explication ou traduction "en tunisien" (ou formulation similaire : "explique en derja", "dis-le en tunisien", "traduis en tunisien", etc.)

### Action — Création de page Notion

1. **Si on est déjà dans le contexte d'une page Notion** → créer une **sous-page** de cette page, titrée "Explication en tunisien — [sujet]"
2. **Si on n'est PAS dans un contexte de page Notion** → créer une page sous la page **"Mes notes"**, titrée "Explication en tunisien — [sujet]"

### Format du contenu (OBLIGATOIRE)

- **Langue** : arabe dialectal tunisien, termes techniques en anglais tels quels
- **Sens d'écriture** : RTL (droite à gauche)
- **Structure de chaque puce** (dans l'ordre de lecture RTL) :
  ```
  [terme anglais] : [explication en arabe tunisien] → [détails techniques en anglais]
  ```
- **Exemple attendu** :
  ```
  lab-base متاع workspace يستعمل : pr-merge
  خاوي workspace يخلّي : branch
  ```

### Règles supplémentaires

- Ne PAS traduire les termes techniques anglais — les garder tels quels
- L'explication en arabe doit être simple, conversationnelle (comme si tu expliques à quelqu'un à l'oral)
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
