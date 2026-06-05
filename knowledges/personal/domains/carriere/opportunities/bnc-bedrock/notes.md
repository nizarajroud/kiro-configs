---
name: opportunity-bnc-bedrock-notes
description: Notes et stratégie pour l'opportunité BNC Bedrock.
---
# Notes — Opportunité BNC Bedrock

## État actuel (2026-06-05)

- ✅ CV V17 généré (basé sur V16 + 3 expériences + certification + ajustements BNC)
- ✅ Script `build-cv-format-alithya.py` fonctionnel et documenté (README.md)
- ✅ Copié dans Dropbox (`CV_officiels-Format-Alithya/`)

## Décisions prises

- Les nouvelles expériences continuent la numérotation (#8, #9, #10) — les existantes ne bougent pas
- Le script détecte auto la dernière version et incrémente
- Chaque expérience = 1 fichier .md autonome dans `assets/experiences/`

## Patterns techniques découverts (styles Alithya .docx)

- **Gras** : titres d'expérience (format `# ` + numéro + `<w:tab/>` + titre)
- **Puce1** : bullet points (avec `<w:spacing w:line="360"/>` = interligne 1.5)
- **NormalArial** : paragraphes normaux
- Date alignée à droite : `<w:tabs><w:tab w:val="right" w:pos="9354"/></w:tabs>` + `<w:tab/>`
- Certification : style Gras + `<w:tab/>` + année, suivi de "Amazon Web Services." en Gras non-bold
- Interligne 1.5 = `w:line="360"` (360 twips / 240 = 1.5)

## Ajustements faits pour aligner avec la fiche BNC

- #10 Beneva/SALSA : ajouté SCPs, Permission Boundaries, AWS Config, VPC Endpoints, KMS
- #8 Bedrock : ajouté Guardrails, Knowledge Bases, Inference Profiles, org policies, observabilité
- #9 BIXI : ajouté documentation architecturale + support revue sécurité
- Certification ajoutée : AWS Generative AI Developer – Professional Early Adopter 2026
- Simplifications texte : Méthodologies raccourcies, Client sans "(Assurance)", Projet sans sous-titre

## Prochaines étapes possibles

- [ ] Valider visuellement le V17 dans Word
- [ ] Adapter le résumé d'introduction si nécessaire
- [ ] Ajouter l'expérience AgentCore si l'opportunité évolue

---

_Dernière mise à jour : 2026-06-05_
