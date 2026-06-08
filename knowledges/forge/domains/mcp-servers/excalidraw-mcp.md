---
name: excalidraw-mcp
description: Generate 20+ types of hand-drawn diagrams (flowcharts, mindmaps, architecture, sequence, ER, class, state, timeline, kanban, wireframes) as .excalidraw files with Sugiyama auto-layout and CJK support.
---
# Excalidraw MCP (maaker-ai)

- **Status**: installed
- **JSON key**: `excalidraw-mcp`
- **Wrapper**: none (no secrets needed)
- **Command**: `uvx maaker-excalidraw-mcp`
- **Notion**: [MCP: Excalidraw (maaker-ai)](https://app.notion.com/p/MCP-Excalidraw-maaker-ai-379174cb5dcc814ab649e14ccd4bc06d)
- **Source**: https://github.com/maaker-ai/excalidraw-mcp
- **Verdict**: adopted — local diagram generation with auto-layout, no API key needed

## Tools (20+)

| Tool | Description |
|------|-------------|
| `create_flowchart` | Flowcharts with Sugiyama layout (directions: LR, RL, TB, BT) |
| `create_architecture_diagram` | Layered architecture diagrams |
| `create_sequence_diagram` | UML sequence diagrams |
| `create_class_diagram` | UML class diagrams |
| `create_state_diagram` | UML state machines |
| `create_er_diagram` | Entity-Relationship diagrams |
| `create_mindmap` | Tree-style mind maps |
| `create_timeline` | Timeline/Gantt charts |
| `create_pie_chart` | Pie charts |
| `create_kanban_board` | Kanban boards |
| `create_network_diagram` | Network topology |
| `create_quadrant_chart` | 2x2 matrices |
| `create_user_journey` | User journey maps |
| `create_wireframe` | UI wireframes |
| `create_org_chart` | Org charts |
| `create_swot_analysis` | SWOT 2x2 matrices |
| `import_mermaid` | Import Mermaid syntax |
| `modify_diagram` | Add/remove nodes in existing diagrams |
| `read_diagram` | Analyze existing .excalidraw files |
| `export_to_svg` | Export to SVG |
| `list_diagram_types` | List available types |

## Usage Notes

- Output: `.excalidraw` files (editable at excalidraw.com) + SVG export
- Direction `RL` available for flowcharts (useful for future RTL adaptation)
- CJK text width estimation built-in
- No API key, no rate limits, fully local
- Future: fork for RTL Arabic/Tunisian text support
