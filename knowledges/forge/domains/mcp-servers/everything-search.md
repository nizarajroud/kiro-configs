---
name: mcp-everything-search
description: Fast file search across all disks (Windows /mnt/c/ + Linux /home/) using plocate. Cross-platform, cross-cutting on all domain agents.
---
# mcp-everything-search — Universal File Search

- **Status**: installed
- **JSON key**: `mcp-everything-search`
- **Agent**: **cross-cutting** (it-supervisor, compass, exp2, forge, light)
- **Type**: Local (uvx, stdio)
- **Command**: `uvx mcp-server-everything-search`
- **Source**: https://github.com/mamertofabian/mcp-everything-search (⭐344)
- **Package**: mcp-server-everything-search v1.28.1 (PyPI, nom interne 'universal-search')
- **Verdict**: adopted — le plus populaire, cross-platform, gratuit, 100% local

## Tools

| Tool | Description |
|------|-------------|
| `search` | Recherche de fichiers par nom, extension, pattern. Retourne : chemin, taille, dates (created, modified, accessed) |

## Paramètres

| Param | Requis | Description |
|-------|--------|-------------|
| `base.query` | ✅ | Pattern de recherche (wildcards *, ?, []) |
| `base.max_results` | Non | Max résultats (défaut 100, max 1000) |
| `linux_params.ignore_case` | Non | Ignorer la casse (défaut: true) |
| `linux_params.regex_search` | Non | Activer regex (défaut: false) |
| `linux_params.existing_files` | Non | Seulement fichiers existants (défaut: true) |
| `linux_params.count_only` | Non | Retourner seulement le count (défaut: false) |

## Prérequis

- plocate 1.1.15 (installé)
- Indexation : cron `updatedb` toutes les 30 minutes
- Couvre : `/home/` + `/mnt/c/` (disque Windows entier)

## Exemples de recherche

- `suivi-des-affaires` → trouve le fichier Excel sur Dropbox
- `*.pdf` → tous les PDFs
- `*facture*2026*` → factures de 2026
- `kiro-configs` → tous les fichiers du projet

## Notes

- Première indexation : ~10-15 min (scan complet /mnt/c/)
- Mises à jour suivantes : ~1-2 min (cron toutes les 30 min)
- Pas de recherche temps réel — délai max 30 min pour les nouveaux fichiers
- Pour forcer l'index : `sudo updatedb`
