---
name: eks-mcp-server
description: Amazon EKS MCP Server (READ-ONLY) — inspect clusters, pods, deployments, logs, events.
---
# EKS MCP Server

- **Status**: installed
- **JSON key**: `awslabs.eks-mcp-server`
- **Location**: agents/exp2.json
- **Wrapper**: `wrappers/eks_mcp_wrapper.py`
- **Command**: awslabs EKS MCP server
- **Source**: https://github.com/awslabs/mcp (awslabs official)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `list_clusters` | List EKS clusters |
| `describe_cluster` | Cluster details |
| `list_pods` / `describe_pod` | Pod inspection |
| `get_pod_logs` | Retrieve pod logs |
| `list_deployments` / `list_services` | Workload inspection |
| `get_events` | Kubernetes events |
| `get_cloudwatch_logs` / `get_cloudwatch_metrics` | Monitoring |

## Auth

- AWS credentials (SSO profile: csna-operations-sso-828)
- kubeconfig for cluster access

## Limitations

- READ-ONLY — no create/update/delete of resources
- Requires active AWS SSO session
- Cluster must be accessible from local machine
