---
name: diagram-prompt-templates
description: Standardized prompt templates for AWS architecture diagrams with pre-configured Graphviz settings.
---
# Diagram Prompt Templates

- **Status**: installed
- **JSON key**: `local.diagram-prompt-templates`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `python3 -u /home/nizar/HomeWspce/diagram-prompts-mcp/server.py`
- **Source**: Custom local server
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| (prompt templates) | Get correct prompt format for consistent diagram output |

## Auth

- None required

## Limitations

- Companion to `aws-diagram-generator` — use BEFORE generating diagrams
- Provides Graphviz settings (font sizes, DPI, layout, spacing)
- Does not generate diagrams itself
