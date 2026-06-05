---
name: demenagement-index
description: Index des steering files du déménagement — structure et liens.
---
# 🏠 Projet Déménagement — Index des Steering Files

> Planification du déménagement : Longueuil, juin 2026
> Ces fichiers sont évolutifs — ajouter les nouvelles contraintes au fur et à mesure.

## Sources de vérité — Consultation PARALLÈLE + Synthèse avec déduplication

> **Stratégie : consulter TOUTES les sources en parallèle, dédupliquer, et faire une synthèse consolidée.**

### Processus de réponse

1. **Consulter toutes les sources en parallèle** (steering + NotebookLM + Notion + Gmail)
2. **Dédupliquer** — identifier les infos copiées entre sources (ne pas répéter)
3. **Synthétiser** — une seule réponse avec :
   - L'info elle-même
   - La **source primaire** (d'où vient l'info à l'origine)
   - Les **sources qui confirment** (cross-validation = plus fiable)
   - Les **éléments exclusifs** à une source (info qu'on ne trouve nulle part ailleurs)

### Sources

| Source | Serveur MCP | Contenu | Utile pour |
|--------|-------------|---------|------------|
| **Steering files** (`steering/`) | — | Tout ce qui est confirmé et validé. Chronologie, actions, décisions. | État actuel du plan, décisions prises |
| **[NotebookLM — "2745 rolland therrian"](https://notebooklm.google.com/notebook/ecb14fdb-e9e8-40fe-9e1e-2130ab7c370c)** | `notebooklm` | 36 sources : contrats, inspection, certificat localisation, factures, déclarations vendeur. | Données techniques, légales, financières de la propriété |
| **[Page Notion — 2745 Boul. Roland-Therrien](https://app.notion.com/p/2745-Boul-Roland-Therrien-309174cb5dcc8060857be40d291d49b7)** | `notion-workspace` | Baklog, actions, notes de suivi, étapes du projet. | Suivi opérationnel, listes, notes personnelles |
| **Gmail** | `gmail` (mcp-gsuite) | Échanges avec parties prenantes (notaire, propriétaire, courtier, assurance). | Confirmations, dates, montants, pièces jointes, contexte des échanges |

### Quand Gmail est utile vs pas utile

- ✅ **Utile** : confirmations, dates convenues, montants, échanges avec des personnes, pièces jointes, contexte des demandes
- ❌ **Pas utile** : données techniques de la maison (déjà dans NotebookLM via les documents indexés)

### Autres sources complémentaires

- PDFs contractuels : ~/My-KB-Documents/Projet-immobilier/ (serveur MCP `pdf-reader`)

## Dates clés

| Date | Événement |
|------|-----------|
| **8 juin** | Acte de vente + remise des clés |
| **8–17 juin** | Préparation maison (nettoyage, serrures) — pas d'occupation |
| **18 juin 11h30** | Déménageur arrive (ancien logement) |
| **18 juin 13h00** | Occupation officielle nouvelle maison |
| **30 juin** | Fin du bail ancien logement |

## Steering Files

| # | Fichier | Contenu |
|---|---------|---------|
| 01 | [Contexte familial](./01-contexte-familial.md) | Famille (Nizar, Abir, Radwan, Yasmine), emplois, transport |
| 02 | [Dates et calendrier](./02-dates-calendrier.md) | Dates confirmées : acte 8 juin, occupation 18 juin 13h |
| 03 | [Tâches logistiques](./03-taches-logistiques.md) | Déménageur (Maher/Lamunia 18 juin 11h30), internet, serrures, électroménagers |
| 04 | [Répartition des rôles](./04-repartition-roles.md) | Qui fait quoi, disponibilités, coordination voiture |
| 05 | [Budget](./05-budget.md) | Objectif coûts, DIY vs prestataire, déménageur ~600$ |
| 06 | [Fiche maison](./06-fiche-maison.md) | Détails propriété (Centris, 4 chambres, taxes, inclusions) |
| 07 | [Inventaire des biens](./07-inventaire-biens.md) | Liste complète meubles, électroménagers, cartons |
| 08 | [Changements d'adresse](./08-changements-adresse.md) | 20+ cibles à notifier |
| 09 | [Données contractuelles](./09-donnees-contractuelles.md) | Promesse d'achat, prix 735 000 $, travaux inspection |
| 10 | [**Chronologie complète**](./10-chronologie-complete.md) | **80+ tâches sur 5 phases**, du 1er mai au juillet |
| 11 | [**Baklog actions**](./11-baklog-actions.md) | Toutes les actions Notion avec statut (fait/à faire) |
| 12 | [**🚨 Actions urgentes**](./12-actions-urgentes.md) | **NOUVEAU** — Actions à prendre DÈS QUE POSSIBLE |

## Décisions en attente

- [ ] ⚠️ **CETTE SEMAINE** : Envoyer un email au propriétaire — nouvelle date de remise des clés (distincte du jour de déménagement) + récupérer dépôt 1 500 $
- [ ] Serrures : DIY ou serrurier ?
- [ ] ~~Lave-vaisselle~~ → ✅ RÉSOLU : on garde celui de la maison
- [ ] Sécheuse : DIY ou professionnel ?
- [ ] Nettoyage nouvelle maison : Abir ou femme de ménage ?
- [ ] Nettoyage ancien logement : nous ou femme de ménage ?
- [ ] ~~Peinture ancien logement~~ → **optionnel**, à évaluer lors du nettoyage final
- [ ] Cuisinière : garder les deux ou se débarrasser de l'ancienne ?
- [ ] Chauffe-eau : prendre en charge le contrat de location
- [ ] Congés à poser : 8 juin (notaire) + 18 juin (déménagement) + 19 juin (optionnel)
- [ ] Planifier les 5 travaux d'inspection (juillet)

## Sources

- [Liste des contraintes originale](../listes%20des%20contraintes)
- [Page Notion](https://app.notion.com/p/2745-Boul-Roland-Therrien-309174cb5dcc8060857be40d291d49b7)
- PDFs : promesse-d-achat.pdf, MO dates Roland Therrien.pdf, Modifications-promesse-d-achat.pdf

## Diagrammes PDF (lisibles via `pdf-reader`)

| Fichier | Contenu |
|---------|---------|
| `knowledges/personal/domains/demenagement/les Diagrams/01-gantt-timeline-projet.pdf` | Gantt — timeline complète du projet |
| `knowledges/personal/domains/demenagement/les Diagrams/02-flowchart-jour-j.pdf` | Flowchart — déroulement du jour J |
| `knowledges/personal/domains/demenagement/les Diagrams/03-checklist-par-phase.pdf` | Checklist par phase |
| `knowledges/personal/domains/demenagement/les Diagrams/04-coordination-nizar-abir.pdf` | Coordination Nizar/Abir |

---

_Dernière mise à jour : 2026-05-01_
