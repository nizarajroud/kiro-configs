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

## Contacts

- **Lauriane Arcand** (lauriane.arcand@bnc.ca) — Adjointe admin BNC, gère les accès/VDI/SecurID
- **Gabrielle Soucy** (gabsoucy@amazon.com) — Sr. Engagement Manager, AWS ProServe
- **Ashwin Bhargava** (bharashw@amazon.com) — Delivery Consultant (Security), AWS ProServe
- **Denise Ho** (denisehp@amazon.com) — Senior Engagement Manager, AWS ProServe
- **Martin Villette** — Manager Alithya (backup de Sylvain pendant vacances)

- **50h/semaine total** : 30h BNC + 20h Beneva
- Arrangé avec Sylvain (manager Alithya) et les deux clients
- Mission BNC : ~9 semaines

## Équipement reçu (2026-06-29)

- **Laptop** : Microsoft Surface Laptop 7 (MSF-Ep2-22195)
- Specs : 32GB RAM, 256GB SSD, Black, Copilot+, Windows 11 Pro
- Usage : accès au VDI BNC
- Token RSA : ✅ configuré et fonctionnel (PIN + OTP sur iPhone)
- Mot de passe Windows : ❌ en attente (réinitialisé, envoyé à Jérémy Leblanc)

## Assignment AWS (système Certinia/PSA)

- **Assignment** : [Sub-Project 6] BNC - ISOW CTP SOB Lead Outcome Based-Project
- **Assignment Number** : A-1068291
- **Nom complet** : [Billable] [APD] [NAMER] [Sub-Project 6] BNC - ISOW CTP SOB Lea - Nizar A
- **Rôle** : Senior Consultant
- **Allocation** : 100%
- **Start Date** : 28 juin 2026
- **End Date** : 1 août 2026
- **Scheduled Hours** : 200h (25 jours × 8h)
- **Scheduled Days** : 25
- **Statut** : Scheduled
- **Billable Hours Submitted** : 0
- **Créé** : 27 juin 2026, 17h17
- **Modifié** : 29 juin 2026, 08h10

### Décodage des acronymes

| Acronyme | Signification |
|----------|---------------|
| APD | Amazon Partner Delivery (Alithya livre sous cadre AWS) |
| NAMER | North America Region |
| ISOW | Internal Statement of Work |
| CTP | Cloud Technology & Platform |
| SOB Lead | Solution/Outcome-Based Lead |
| WAR | Work Authorization Request (approuvé par Mathieu) |

### Notes timesheet

- Logger les heures à partir du 21 juin (rétroactif, confirmé par email Amazon)
- Système : Certinia/PSA (portail Amazon)
- Budget = 200h sur 25 jours (8h/jour sur le papier, réalité = 30h/sem BNC)

---

_Dernière mise à jour : 2026-06-29_
