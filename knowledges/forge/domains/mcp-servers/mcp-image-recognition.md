---
name: mcp-image-recognition
description: Image analysis MCP (READ-ONLY) — analyzes images using Amazon Bedrock vision models (Nova Pro, Claude).
---
# MCP Image Recognition

- **Status**: installed
- **JSON key**: `mcp-image-recognition`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `python3 /home/nizar/HomeWspce/mcp-image-recognition/server.py`
- **Source**: Custom local server
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `describe_image` | Analyze image from base64 data |
| `describe_image_from_file` | Analyze image from file path |

## Auth

- AWS credentials (Bedrock access via local gateway on localhost:8766)

## Limitations

- READ-ONLY — cannot generate or modify images
- Requires Bedrock Access Gateway running locally
- Supports: diagrams, screenshots, documents, photos
- Custom prompt supported for targeted analysis
