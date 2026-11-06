# Documentation de kiro-configs

Ce dossier regroupe la documentation du projet `kiro-configs`. Pour la structure du repo et les conventions, voir aussi :

- `knowledges/forge/steering/kiro-configs-architecture.md` : architecture maître
- `knowledges/forge/steering/conventions-kiro-configs.md` : conventions et bonnes pratiques

## Contenu de ce dossier

| Fichier | Contenu |
|---------|---------|
| `architecture-globale-agents.drawio` | Diagramme des agents et de leurs MCP. À mettre à jour à chaque création, suppression ou changement d'agent ou de MCP. |
| `README.md` | Ce fichier. |

## Éléments qui vivent hors de ce repo

Certains éléments installés ou modifiés pendant le travail sur kiro-configs ne sont pas dans ce repo, donc pas couverts par son git. Ils sont documentés en détail sur une page Notion (emplacement, versionné ou non, état, commandes de reprise et de rollback) :

**Page Notion : [Kiro-configs — éléments hors repo](https://app.notion.com/p/Kiro-configs-l-ments-hors-repo-proxy-MCP-partag-qq-kiro-web-topics-db-410174cb5dcc818da6d1e7d79c71190f)**

Chemin dans Notion : Tooling, puis « Kiro-configs — éléments hors repo (proxy MCP partagé, qq, kiro-web, topics.db) ».

Aperçu (le détail et l'état à jour sont sur la page Notion) :

| Élément | Emplacement | Versionné |
|---------|-------------|-----------|
| Proxy MCP partagé (POC avelino/mcp) : binaire, config, service systemd | `~/.cargo/bin/mcp`, `~/.config/mcp/`, `~/.config/systemd/user/avelino-mcp-proxy.service`, `~/HomeWspce/avelino-mcp-poc/` | Non |
| Agent sandbox pointant sur le proxy | `agents/sandbox.json` | Non (gitignored) |
| Fix `qq` : forcer l'agent sandbox | `~/workspace/PROC/xxxxuseful-scripts/common-functions.bash` | Oui, dans le repo PROC (commit 0771218, branche main, non poussé) |
| `KIRO_WEB=1` dans les sous-process ACP | `~/HomeWspce/kiro-web/src/kiro_web/acp/process_manager.py` | Oui, dans le repo kiro-web |
| Base des sujets (`session_catalog`, `topic_log`) | `~/.kiro/sessions/topics.db` | Non (`sessions/` gitignored) |

## Règle de maintenance

Toute chose installée ou modifiée en dehors de ce repo (binaire, service, config utilisateur, script d'un autre projet) doit être ajoutée à la page Notion ci-dessus, avec son emplacement, son état de versionnement et la procédure de rollback. Ce tableau d'aperçu doit rester cohérent avec la page.
