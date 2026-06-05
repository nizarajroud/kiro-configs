# kiro-configs

> Configuration multi-agent pour Kiro CLI — agents, prompts, MCP servers, knowledge bases, mémoire.

## Quick Start

```bash
# Symlink vers ~/.kiro (requis par Kiro CLI)
ln -s /home/nizar/HomeWspce/kiro-configs /home/nizar/.kiro

# Lancer un agent
kiro chat --agent it-supervisor
```

## Structure

| Dossier | Rôle |
|---------|------|
| `agents/` | Définitions JSON des agents |
| `prompts/` | System prompts (.md) |
| `cao-profiles/` | Profils CAO (orchestration multi-agent) |
| `knowledges/` | Données de steering + domaines (personal, work, forge, shared) |
| `settings/` | mcp.json, cli.json, servers.yaml |
| `memories/` | Mémoire persistante JSONL par agent |
| `wrappers/` | Lanceurs MCP (chargent .env + exec) |
| `scripts/` | Scripts opérationnels |
| `hooks/` | Guards (destructive commands, secrets) |
| `steering/` | Règles globales CLI (non-interactive) |
| `zzz/` | Archive d'anciens agents |

## Documentation complète

Voir `knowledges/forge/steering/`:
- `kiro-configs-architecture.md` — architecture maître
- `conventions-kiro-configs.md` — conventions et bonnes pratiques

## Agents actifs

| Agent | Scope |
|-------|-------|
| `it-supervisor` | Tout (personal + work + forge) |
| `compass` | Vie personnelle |
| `exp2` | Travail technique |
| `forge` | Outillage et découverte |
| `supervisor` | Orchestrateur CAO |

## Secrets

Tous dans `.env` (gitignored). Jamais dans les fichiers JSON.
