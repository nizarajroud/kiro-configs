> Projet interne · 03/2026 à 04/2026

# 9 AWS Solutions Architect

**Projet :** AWS Migration & Infrastructure Modernization — BIXI Montréal

En tant que AWS Solutions Architect, j'ai dirigé l'analyse complète et la conception de la stratégie de migration cloud pour BIXI Montréal, dans le cadre d'un mandat couvrant la migration de l'infrastructure opérationnelle vers AWS, parallèlement à une migration de fournisseur (Lyft → Helium).

* Analyse et documentation de l'infrastructure existante : 20 scripts Python sur des VMs Windows (automatisation opérationnelle), l'application Panorama (Vue3 + Express, Docker on-prem), et leurs dépendances aux APIs Lyft, au Datamart MySQL et à 8 services externes.
* Conception et évaluation de 3 scénarios de migration AWS (Big Bang, Hybride + Shadow Mode, Conservateur) avec estimations de coûts (AWS Pricing Calculator), matrices de risques, tableaux d'effort par script, et alignement avec le AWS Well-Architected Framework.
* Production de documentation architecturale détaillée et support du processus de revue sécurité avec les équipes plateforme et infrastructure du client.

Environnement technologique :

* Cloud & AWS Services : Lambda, ECS Fargate, EventBridge Scheduler, AppConfig, Secrets Manager, CloudWatch (EMF), NAT Gateway, VPC, ECR, ALB, S3, KMS, IAM
* Infrastructure : Windows VM (Task Scheduler), Docker, GitHub Actions (CI/CD)
* Données : Snowflake, MySQL (Datamart), Parquet/S3 (HDP), REST APIs (HCP/Helium)
* Outils : AWS Pricing Calculator, Python (diagrams library), Notion API, python-pptx

**Méthodologies :** AWS Well-Architected Framework, Strangler Fig Pattern, Shadow Mode, GitOps, Agile
