---
inclusion: always
---
# Work Context — Tech Stack

## Cloud

- **AWS** (primary): LZA, EKS, CDK, CloudFormation, Bedrock, S3, EC2, Lambda, IAM, Organizations
- **Region**: ca-central-1 (primary)
- **Multi-account**: AWS Organizations with Control Tower / LZA

## CI/CD

- **Jenkins** (jenkins.ssqti.ca) — pipelines CSBEN, read-only access via MCP
- **GitHub Actions** — beneva-int organization
- **CodePipeline** — LZA deployment pipeline

## Infrastructure as Code

- **AWS CDK** (TypeScript/Python)
- **CloudFormation** (LZA configs)
- **Terraform** (occasional)

## Languages

- Python (primary — wrappers, scripts, Lambda)
- TypeScript (CDK, frontend)
- Bash (automation, CI scripts)
- YAML/JSON (configs, CloudFormation, Kubernetes)

## Platforms

- **Jira** (jira.int.beneva.ca) — project tracking
- **Confluence** (confluence.int.beneva.ca) — documentation
- **GitHub Enterprise** (beneva-int org) — source code
- **Kubernetes/EKS** — container workloads

## Local Tools

- WSL2 (Ubuntu) on Windows
- Kiro CLI with MCP servers
- AWS CLI with SSO profiles
