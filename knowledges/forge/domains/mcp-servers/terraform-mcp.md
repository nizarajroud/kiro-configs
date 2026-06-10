---
name: terraform-mcp
description: HashiCorp official Terraform MCP Server. Searches Terraform Registry for providers, modules, and policies to write informed IaC.
---
# Terraform MCP Server (HashiCorp Official)

- **Status**: installed
- **JSON key**: `terraform-mcp`
- **Agent**: exp2
- **Command**: `/home/nizar/go/bin/terraform-mcp-server stdio --toolsets=registry`
- **Source**: https://github.com/hashicorp/terraform-mcp-server (⭐1397)
- **Notion**: [link pending]
- **Verdict**: adopted — official, well-maintained, essential for Terraform workflows

## Tools (9 — registry toolset)

| Tool | Description |
|------|-------------|
| `search_providers` | Search Terraform providers in registry |
| `get_provider_details` | Get provider info (versions, docs) |
| `get_provider_capabilities` | List resources/data-sources of a provider |
| `get_latest_provider_version` | Latest version of a provider |
| `search_modules` | Search reusable Terraform modules |
| `get_module_details` | Get module inputs/outputs/dependencies |
| `get_latest_module_version` | Latest version of a module |
| `search_policies` | Search Sentinel/OPA policies |
| `get_policy_details` | Get policy details |

## Future

- Add `--toolsets=terraform` with `TFE_TOKEN` for HCP Terraform Cloud workspace management
- Add `--toolsets=registry-private` for private registry access
