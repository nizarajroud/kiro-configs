---
name: memory-compass
description: Persistent memory for compass agent — user preferences, routing corrections, personal patterns.
---
# Memory — compass

- **Status**: installed
- **JSON key**: `memory-compass`
- **Location**: agents/compass.json
- **Wrapper**: none
- **Command**: `mcp-server-memory`
- **Source**: https://github.com/modelcontextprotocol/servers (official MCP)
- **Priority**: critical
- **Verdict**: adopted

## Storage

- File: `/home/nizar/HomeWspce/kiro-configs/memories/memory-compass.jsonl`
- Format: JSONL (entities + relations)

## Tools

Same as all memory servers (create_entities, search_nodes, read_graph, etc.)

## Auth

- None (local file)

## Limitations

- Max ~50 entities recommended
- Never write without user confirmation
