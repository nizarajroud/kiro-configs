---
name: tfmcp
description: Terraform MCP operator — execute terraform commands, generate dependency graphs (DOT), analyze state/drift, manage workspaces via MCP.
---
# tfmcp — Terraform MCP Operator

- **Status**: installed
- **JSON key**: `tfmcp`
- **Agent**: exp2
- **Wrapper**: none (direct binary)
- **Command**: `/home/nizar/.cargo/bin/tfmcp mcp`
- **Source**: https://github.com/nwiizo/tfmcp (⭐369)
- **Verdict**: adopted — unique MCP server that operates Terraform in real-time

## Tools (31)

### Core Operations
| Tool | Description |
|------|-------------|
| `init_terraform` | Initialize Terraform working directory |
| `get_terraform_plan` | Generate and show execution plan |
| `apply_terraform` | Apply configuration (disabled by default) |
| `destroy_terraform` | Destroy infrastructure (disabled by default) |
| `validate_terraform` | Validate configuration syntax |
| `set_terraform_directory` | Change active project directory |

### Graph & Dependencies
| Tool | Description |
|------|-------------|
| `terraform_graph` | **Generate dependency graph in DOT format** |
| `get_resource_dependency_graph` | Show resource relationships |

### Analysis
| Tool | Description |
|------|-------------|
| `analyze_plan` | Plan analysis with risk scoring |
| `analyze_state` | State analysis with drift detection |
| `analyze_module_health` | Module health (cohesion/coupling metrics) |

### State & Workspace
| Tool | Description |
|------|-------------|
| `get_terraform_state` | Show current state |
| `terraform_workspace` | Workspace management |
| `terraform_import` | Import existing resources |
| `terraform_output` | Get output values |

## Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `TERRAFORM_DIR` | `/home/nizar/HomeWspce/poc-bnc-terraform-modules` | Default project |
| `TFMCP_ALLOW_DANGEROUS_OPS` | `false` | Blocks apply/destroy |
| `TFMCP_ALLOW_AUTO_APPROVE` | `false` | Requires manual approval |
| `TFMCP_AUDIT_ENABLED` | `true` | Logs all operations |

## Usage Chain

```
tfmcp (terraform_graph → DOT text) → quickchart-mcp (DOT → PNG/SVG image)
```

## Security

- apply/destroy disabled by default (set `TFMCP_ALLOW_DANGEROUS_OPS=true` to enable)
- Audit log at `~/.tfmcp/audit.log`
- Max 50 managed resources limit
