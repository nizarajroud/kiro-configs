> Projet interne : Chatbot Alithya 02/2026 à 03/2026

# 8 Generative AI Architect

**Projet :** Intégration du support multi-modèles AWS Bedrock dans le Chatbot interne Alithya

En tant que Generative AI Architect, j'ai conçu et implémenté une architecture IA générative multi-fournisseur pour le chatbot interne d'Alithya, intégrant les modèles fondation d'AWS Bedrock (Claude pour la génération de texte, Titan pour les embeddings) aux capacités OpenAI existantes. Cette amélioration permet à la plateforme de tirer parti des services IA managés d'Amazon avec une sélection flexible de modèles, offrant des alternatives rentables tout en maintenant des réponses conversationnelles de haute qualité via une architecture RAG (Retrieval-Augmented Generation).

* Intégration de l'API AWS Bedrock Converse avec support de plusieurs modèles fondation Claude (3.5 Haiku, 3.5 Sonnet, 4.5 Haiku, Opus) pour la génération en langage naturel et des embeddings Amazon Titan pour la recherche sémantique, implémentant une logique intelligente de détection et d'instanciation de modèles.
* Conception et configuration du pipeline RAG (Retrieval-Augmented Generation) utilisant PostgreSQL avec l'extension pgvector pour la recherche par similarité vectorielle, permettant des réponses contextuelles en récupérant les documents pertinents de la base de connaissances via des embeddings sémantiques.
* Mise en place de Bedrock Guardrails pour le filtrage de contenu, la détection de PII et la protection contre les attaques de prompt, avec application de politiques organisationnelles pour contrôler l'accès aux modèles et l'inférence cross-région via les Inference Profiles.
* Configuration de la stratégie de déploiement multi-environnement à travers Docker Compose (développement local) et Kubernetes/Helm (production), gérant les credentials des services IA et les variables d'environnement pour 4 environnements (dev, qa, demo, production).
* Implémentation de l'observabilité avec CloudWatch (logging, métriques de latence et de coût par modèle) et traçage des invocations Bedrock pour le monitoring de la qualité des réponses.

Environnement technologique :

* Cloud & IA : AWS Bedrock (Claude, Titan), Bedrock Guardrails, Bedrock Knowledge Bases, Inference Profiles, OpenAI API, AWS IAM
* Bases de données : PostgreSQL avec extension pgvector pour la recherche par similarité vectorielle
* Sécurité & Gouvernance : KMS (chiffrement des données), IAM roles, Bedrock organizational policies
* Infrastructure : Docker Compose, Kubernetes (EKS), Helm, FluxCD (GitOps)
* CI/CD : Bitbucket Pipelines, Changesets pour le versioning
* Observabilité : CloudWatch (logging, metrics, tracing)
* Monorepo : Turborepo avec pnpm workspaces

**Méthodologies :** Agile/Scrum
