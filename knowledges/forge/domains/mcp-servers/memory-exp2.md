---
name: memory-exp2
description: Persistent memory for exp2 agent — technical context, decisions, project patterns.
---
# Memory — exp2

- **Status**: installed
- **JSON key**: `memory-exp2`
- **Location**: agents/exp2.json
- **Wrapper**: none
- **Command**: `mcp-server-memory`
- **Source**: https://github.com/modelcontextprotocol/servers (official MCP)
- **Priority**: critical
- **Verdict**: adopted

## Storage

- File: `/home/nizar/HomeWspce/kiro-configs/memories/memory-exp2.jsonl`
- Format: JSONL (entities + relations)

## Tools

| Tool | Description |
|------|-------------|
| `create_entities` | Store new knowledge |
| `add_observations` | Add facts to existing entities |
| `search_nodes` | Search memory by query |
| `read_graph` | Read full graph |
| `delete_entities` / `delete_observations` | Remove knowledge |
| `create_relations` / `delete_relations` | Link entities |
| `open_nodes` | Retrieve specific entities |

## Auth

- None (local file)

## Limitations

- Max ~50 entities recommended before migrating to steering files
- Never write without user confirmation
