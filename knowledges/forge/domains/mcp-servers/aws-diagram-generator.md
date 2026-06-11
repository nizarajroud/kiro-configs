---
name: aws-diagram-generator
description: Generates AWS architecture diagrams as PNG using Python diagrams package.
---
# AWS Diagram Generator

- **Status**: installed
- **JSON key**: `local.aws-diagram-generator`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `.venv/bin/python -m awslabs.aws_diagram_mcp_server.server`
- **Source**: https://github.com/awslabs/mcp (awslabs official)
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `list_available_icons` | Browse available AWS service icons |
| `get_code_examples` | Get diagram code examples |
| `generate_diagram` | Generate PNG from Python diagrams code |

## Auth

- None required (local generation)

## Limitations

- Output: PNG only
- Requires Python `diagrams` package with Graphviz
- Complex layouts may need manual DPI/spacing tuning
- Use `diagram-prompt-templates` first for consistent output
