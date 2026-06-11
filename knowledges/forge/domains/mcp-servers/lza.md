---
name: lza
description: Landing Zone Accelerator MCP Server (READ-ONLY) — search schemas, check pipeline, retrieve configs.
---
# LZA (Landing Zone Accelerator)

- **Status**: disabled (remote on PC Alithya)
- **JSON key**: `lza`
- **Location**: agents/exp2.json
- **Wrapper**: `/home/nizar/.kiro/wrappers/lza_wrapper.sh`
- **Command**: `npx mcp-remote http://192.168.2.56:3214/mcp`
- **Source**: Custom local server
- **Verdict**: adopted (when available)

## Tools

| Tool | Description |
|------|-------------|
| `checkAwsConnectivity` | Verify AWS access |
| `listLzaSupportedVersions` | Available LZA versions |
| `searchJsonSchema` | Search LZA config schemas |
| `getFullSchema` | Get complete schema |
| `getPipelineStatus` | Pipeline state |
| `getConfigurationFromS3` | Read LZA config from S3 |
| `getDeployedLzaVersion` | Current deployed version |
| `diagnosePipelineErrors` | Troubleshoot failures |
| `getMinimumConfiguration` | Minimal config template |

## Auth

- AWS SSO (via remote on PC Alithya)

## Limitations

- READ-ONLY — no pipeline release or config upload without explicit approval
- Currently disabled (remote unavailable)
