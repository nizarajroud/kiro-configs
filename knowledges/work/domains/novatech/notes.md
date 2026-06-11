# NovaTech — Notes de session

## Compréhension du mandat (confirmé avec Sylvain — ~28 mai 2026)

### 3 livrables attendus

1. **Mapping infrastructure** → traduit dans un **document Word** (format Alithya)
2. **Estimation de coûts AWS** → **PDF** du AWS Pricing Calculator (auto-généré)
3. **Estimation de l'effort de migration** → **Excel** (format Plan_Effort_Migration)

### Contexte stratégique
- L'équipe Oracle d'Alithya fait son évaluation OCI en parallèle
- Nous produisons l'évaluation côté AWS pour comparaison
- Le client final (NovaTech) aura les deux propositions

---

## Artifacts de référence

| Livrable | Format | Modèle/Référence |
|----------|--------|-------------------|
| Analyse/Mapping | Word (.docx) | `reference/BIXI-Lot-2-Analyse-v1.docx` — structure high-level, pas deep dive |
| Coûts AWS | PDF | Auto-généré depuis AWS Pricing Calculator |
| Effort migration | Excel (.xlsx) | `reference/Plan_Effort_Migration.xlsx` — phases + plan de charge |

### Structure du Word (à suivre — high-level)
Basé sur BIXI-Lot-2 :
1. Contexte et portée du mandat
2. État actuel (As-Is) — architecture, sizing, analyse
3. Scénarios de migration (mapping services AWS)
4. Estimation efforts (renvoi vers Excel)
5. Estimation coûts (renvoi vers PDF Pricing Calculator)
6. Risques et mitigations
7. Recommandation

**Important** : rester HIGH-LEVEL, pas de deep dive technique comme le BIXI.

### Structure de l'Excel effort (Plan_Effort_Migration.xlsx)
- Sheet 1 : Option-1-Lift-and-Shift (phases, effort en jours, activités)
- Sheet 2 : Option-2-Modernisation (si applicable)
- Sheet 3 : Plan de charge L&S (rôles × semaines × coûts)
- Sheet 4 : Plan de charge modernisation

### Outil de génération Word
- Script : `/home/nizar/HomeWspce/word-format-alithya/format_alithya.py`
- Template : `template_ref.docx` (styles Alithya : Heading1/2/3, TexteAlithya, ListParagraph)
- Input : un fichier `content.md` avec le contenu structuré
- Output : `generated.docx` formaté Alithya

---

## État d'avancement

- [x] Documents sources parsés (questionnaire + inventory)
- [x] Notion page tunisienne lue
- [x] overview.md rempli
- [x] Références analysées (BIXI doc + effort Excel)
- [x] Mapping infra NovaTech → AWS services
- [x] content.md pour le Word Alithya (draft v1)
- [ ] AWS Pricing Calculator (produire le PDF)
- [ ] Excel Plan_Effort_Migration adapté NovaTech
- [ ] Génération du Word final
