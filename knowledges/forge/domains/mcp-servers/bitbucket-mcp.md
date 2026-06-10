---
name: bitbucket-mcp
description: Atlassian Bitbucket Cloud MCP — manage repos, PRs, pipelines, branches, files.
---
# Bitbucket MCP Server

- **Status**: installed (pending auth)
- **JSON key**: `bitbucket-mcp`
- **Wrapper**: `wrappers/bitbucket_wrapper.py`
- **Command**: `npx -y @aashari/mcp-server-atlassian-bitbucket`
- **Source**: https://github.com/aashari/mcp-server-atlassian-bitbucket (⭐155)
- **Notion**: [MCP: Bitbucket](pending)
- **Verdict**: adopted — most starred Bitbucket MCP, communautaire

## Auth

Requires in `.env`:
- `BITBUCKET_USERNAME` — Bitbucket username
- `BITBUCKET_APP_PASSWORD` — App Password (Settings → App passwords → Create with repos + pipelines permissions)

## Capabilities

- List/get workspaces and repositories
- Manage pull requests (create, list, merge)
- Trigger and monitor pipelines
- Browse branches and files
- Search code

## Limitations

- Bitbucket Cloud only (not Bitbucket Server/Data Center)
- App Password will be deprecated June 2026 → migrate to API Token (ATATT format)
