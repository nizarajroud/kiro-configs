---
inclusion: always
---

# AWS Source Routing — Official GitHub Organizations

## Trigger

When the user asks for:
- "Official AWS documentation"
- "AWS labs", "awslabs", "aws samples", "aws-samples"
- "Official repo", "official source code"
- "AWS reference implementation"
- "Inspired from AWS", "based on AWS patterns"
- Any request mentioning AWS + (documentation | source | repo | example | sample | pattern | reference | official)

## Priority Order

### Tier 1 — ALWAYS search here FIRST

| Priority | Organization | URL | When to use |
|----------|---|---|---|
| 🥇 1 | **awslabs** | github.com/awslabs | MCP servers, experimental tools, innovative libraries, new features |
| 🥈 2 | **aws-samples** | github.com/aws-samples | Working sample apps, workshops, demos, PoCs |
| 🥉 3 | **aws** | github.com/aws | Official SDKs, CDK, SAM, CLI, core tooling |

### Tier 2 — Search when domain-specific

| Organization | URL | When to use |
|---|---|---|
| **aws-ia** | github.com/aws-ia | Terraform modules, partner integrations, IaC patterns |
| **aws-cloudformation** | github.com/aws-cloudformation | CloudFormation resource providers, templates |
| **aws-observability** | github.com/aws-observability | Monitoring, OpenTelemetry, CloudWatch tooling |
| **aws-controllers-k8s** | github.com/aws-controllers-k8s | Kubernetes controllers for AWS services |
| **aws-containers** | github.com/aws-containers | ECS, EKS, Fargate specific tooling |
| **aws-amplify** | github.com/aws-amplify | Frontend/mobile, Amplify framework |
| **aws-powertools** | github.com/aws-powertools | Lambda best practices (Python, TS, Java, .NET) |
| **aws-actions** | github.com/aws-actions | GitHub Actions for AWS |
| **aws-solutions-constructs** | github.com/aws-solutions-constructs | Vetted CDK architecture patterns |
| **aws-solutions-library-samples** | github.com/aws-solutions-library-samples | Solutions Library implementations |

### Tier 3 — Product-specific (use when explicitly relevant)

| Organization | URL | Domain |
|---|---|---|
| **opensearch-project** | github.com/opensearch-project | OpenSearch / vector search / RAG |
| **cedar-policy** | github.com/cedar-policy | Cedar authorization (Bedrock AgentCore) |
| **firecracker-microvm** | github.com/firecracker-microvm | Firecracker hypervisor |
| **bottlerocket-os** | github.com/bottlerocket-os | Bottlerocket container OS |
| **smithy-lang** | github.com/smithy-lang | Smithy API modeling |
| **modelcontextprotocol** | github.com/modelcontextprotocol | MCP protocol (Anthropic + AWS) |
| **amazonlinux** | github.com/amazonlinux | Amazon Linux OS |
| **amazon-science** | github.com/amazon-science | Research, ML papers |
| **amzn** | github.com/amzn | Amazon open source (non-AWS) |

## Search Strategy

When searching for AWS official content:

1. **GitHub search scoped to org**: `org:awslabs <keyword>` or `org:aws-samples <keyword>`
2. **Sort by stars** (most popular = most maintained)
3. **Check last commit date** (reject if >12 months stale)
4. **Verify README exists** with clear setup instructions

## Rules

- **NEVER recommend a community repo when an official one exists** in Tier 1-2
- **ALWAYS check awslabs FIRST** for MCP servers, new tools, experimental features
- **ALWAYS check aws-samples FIRST** for working examples and PoCs
- **Report the org** in your answer: "Source: awslabs (official AWS experimental)"
- **If nothing found** in Tier 1-3, then search the broader GitHub ecosystem
