---
name: github
description: GitHub operations — repos, PRs, issues, Actions, code search, file management.
---
# GitHub

- **Status**: installed
- **JSON key**: `github`
- **Location**: settings/mcp.json
- **Wrapper**: `wrappers/github_wrapper.py`
- **Command**: `npx -y @modelcontextprotocol/server-github`
- **Source**: https://github.com/modelcontextprotocol/servers (official MCP)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `create_or_update_file` | Create/update a file in a repo |
| `push_files` | Push multiple files in one commit |
| `search_repositories` | Search repos |
| `search_code` | Search code across repos |
| `create_issue` / `list_issues` | Issue management |
| `create_pull_request` / `merge_pull_request` | PR management |
| `get_file_contents` | Read file/directory contents |
| `create_branch` | Create branches |
| `list_commits` | Browse commit history |
| `fork_repository` | Fork repos |

## Auth

- `GITHUB_PERSONAL_ACCESS_TOKEN` in `.env`

## Limitations

- Token scope determines available operations
- Rate limited (5000 req/hour authenticated)
