---
name: gitlab
description: GitLab MCP (official, Alithya CSNA) — projects, issues, merge requests, pipelines via OAuth.
---
# GitLab

- **Status**: installed
- **JSON key**: `gitlab`
- **Location**: agents/exp2.json
- **Wrapper**: none (remote MCP)
- **Command**: `npx -y mcp-remote https://gitlab.com/api/v4/mcp`
- **Source**: https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/ (official GitLab)
- **Verdict**: adopted

## Tools

Projects, issues, merge requests, pipelines, and GitLab operations via AI.
(Full list: https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server_tools/)

## Auth

- OAuth 2.0 Dynamic Client Registration (auto on first connect)
- Browser opens for authorization — approve once
- Group: `alithya-csna` (Premium SaaS)

## Prerequisites

- GitLab Premium or Ultimate
- GitLab Duo Core: ON
- Beta and experimental features: ON

## Limitations

- Requires GitLab Premium tier minimum
- Beta status (may change)
- OAuth token may expire — re-auth via browser if needed
