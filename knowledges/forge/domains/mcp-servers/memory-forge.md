---
name: memory-forge
description: Persistent memory for forge agent — discovered tools, experiment verdicts, installation notes.
---
# Memory — forge

- **Status**: installed
- **JSON key**: `memory-forge`
- **Location**: agents/forge.json
- **Wrapper**: none
- **Command**: `mcp-server-memory`
- **Source**: https://github.com/modelcontextprotocol/servers (official MCP)
- **Verdict**: adopted

## Storage

- File: `/home/nizar/HomeWspce/kiro-configs/memories/memory-forge.jsonl`
- Format: JSONL (entities + relations)

## Tools

Same as all memory servers (create_entities, search_nodes, read_graph, etc.)

## Auth

- None (local file)

## Limitations

- Max ~50 entities recommended
- Never write without user confirmation
