---
name: novatech-overview
description: Projet NovaTech — contexte, objectifs, architecture, stack technique et contacts.
---
# NovaTech

## Contexte

- **Client**: NovaTech
- **Mission**: Migration (Lift and Shift) d'Oracle E-Business Suite (EBS) depuis l'infrastructure on-premise vers Oracle Cloud Infrastructure (OCI)
- **Durée**: En cours (discovery phase — Cloud Vision Assessment)
- **Environnements**: Development, Test, Patch, Production + Standby/DR
- **Localisation actuelle**: Data centers à St-Laurent (Prod, Test) et Ste-Julie (Dev, Standby/DR) — Québec

## Objectifs

- Comprendre et quantifier l'environnement EBS actuel (discovery)
- Concevoir la future state architecture sur OCI
- Migrer l'EBS en mode lift-and-shift avec optimisation

## Architecture Actuelle

### Application Stack
- **EBS Version**: 12.2.10 (AD/TXK Delta 14)
- **Database**: Oracle 19.21.0.0.0
- **OS**: Linux x86-64 version 7.9
- **Virtualisation**: KVM (i440fx)
- **Endian**: Little endian
- **Langues**: US English + Canadian French

### Environments Sizing

| Env | Location | App Cores | App RAM | DB Cores | DB RAM | DB Size | Total Storage | CPU Util |
|-----|----------|-----------|---------|----------|--------|---------|---------------|----------|
| **Prod** | St-Laurent | 4 | 192 GB | 4 | 192 GB | 1.2 TB | 2.7 TB | 50% |
| **Test** | St-Laurent | 4 | 72 GB | 4 | 72 GB | 1.2 TB | 2.2 TB | 9% |
| **Dev** | Ste-Julie | 3 | 80 GB | 3 | 80 GB | 1.2 TB | 2.7 TB | 22% |
| **Standby/DR** | Ste-Julie | 1 | 58 GB | 1 | 58 GB | 1.2 TB | 2.5 TB | 10% |

### Users
- Total users: 274
- Concurrent users: ~37

### Backup & DR
- **Strategy**: RMAN backups
  - Weekly full backups
  - Daily incremental backups
  - Archivelog backups every 2 hours
- **DR**: Standby database (failover to standby in case of primary site failure)
- **Non-prod clones**: Full copies of production

### Security & Access
- **Authentication**: Native EBS authentication (not AD)
- **Remote access**: FortiClient VPN
- **Monitoring**: Nagios
- **Patching**: 1-2 times per year

### SDLC
- Pipeline: Development → Test → Patch → Production
- Non-prod environments are full copies of production data

## Stack Technique

- **Cloud cible**: Oracle Cloud Infrastructure (OCI)
- **ERP**: Oracle E-Business Suite 12.2.10
- **Database**: Oracle Database 19c (19.21)
- **OS**: Oracle Linux / RHEL 7.9
- **Virtualisation actuelle**: KVM

## Équipe / Contacts

| Rôle | Nom | Contact |
|------|-----|---------|
| (à compléter) | | |

## Décisions Clés

| Date | Décision | Justification |
|------|----------|---------------|
| Oct 2023 | Questionnaire Oracle v3.1 rempli | Discovery pour Cloud Vision Assessment |

## Liens

- Architecture diagram: (à créer)
- Notion summary (tunisien): https://app.notion.com/p/Explication-en-tunisien-Projet-NovaTech-Migration-EBS-vers-Oracle-Cloud-376174cb5dcc813f9e41c778370caf45

## Documents sources (lisibles via outils MCP)

| Fichier | Outil | Chemin |
|---------|-------|--------|
| EBS Lift and Shift Questionnaire | markitdown | `knowledges/work/domains/novatech/assets/EBS Lift and Shift Questionnaire TemplateNovatech.docx` |
| Current State Inventory (Oracle Workload) | markitdown | `knowledges/work/domains/novatech/assets/Current State Inventory_Oracle_Workload_TemplateNovatech.xlsx` |

## Notes — Informations manquantes (à clarifier)

- Modules EBS spécifiques en usage (AP, AR, GL, etc.)
- Applications interfacées avec EBS (ETL, SOA, SSO)
- Niveau de customisation EBS
- Fréquence de clone des environnements non-prod
- SLAs (performance, availability)
- Network bandwidth/latency requirements
- RTO/RPO formels
- Outils de développement pour customizations
- DR requirements détaillés (multi-DC connectivity)
- Compliance requirements (HIPAA/PCI)
- Mobile strategy
