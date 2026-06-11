---
name: bedrock-project-agent
description: Amazon Bedrock agent connected to project knowledge bases — RFP details, requirements, timelines, budgets.
---
# Bedrock Project Agent

- **Status**: installed
- **JSON key**: `bedrock-project-agent`
- **Location**: agents/exp2.json
- **Wrapper**: `/home/nizar/.kiro/wrappers/bedrock_multi_project_wrapper.py`
- **Command**: `python bedrock_multi_project_wrapper.py`
- **Source**: Custom local wrapper over Bedrock Agent Runtime
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| (Bedrock Agent invoke) | Query project knowledge bases for domain-specific info |

## Auth

- AWS credentials (SSO profile)
- Agent ID: `4EBXLZQW3Q`, Alias: `TSTALIASID`
- Region: ca-central-1

## Limitations

- Knowledge base content depends on what's been ingested
- Answers are RAG-based — may hallucinate if KB lacks info
- Single agent, single alias
