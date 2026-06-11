---
name: memory-supervisor
description: Persistent memory for IT-Supervisor — routing decisions, delegation patterns, user preferences.
---
# Memory — IT-Supervisor

- **Status**: installed
- **JSON key**: `memory-supervisor`
- **Location**: agents/it-supervisor.json
- **Wrapper**: none
- **Command**: `mcp-server-memory`
- **Source**: https://github.com/modelcontextprotocol/servers (official MCP)
- **Priority**: critical
- **Verdict**: adopted

## Storage

- File: `/home/nizar/HomeWspce/kiro-configs/memories/memory-supervisor.jsonl`
- Format: JSONL (entities + relations)

## Tools

Same as all memory servers (create_entities, search_nodes, read_graph, etc.)

## Auth

- None (local file)

## Limitations

- Max ~50 entities recommended
- Never write without user confirmation
