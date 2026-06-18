---
name: graphistry-mcp
description: GPU-accelerated interactive graph visualization via Graphistry cloud. Takes edge/node data → produces interactive web views (zoom, pan, filter, community detection).
---
# graphistry-mcp — Interactive Graph Visualization

- **Status**: installed
- **JSON key**: `graphistry-mcp`
- **Agent**: exp2
- **Wrapper**: `wrappers/graphistry_wrapper.py`
- **Source**: https://github.com/graphistry/graphistry-mcp
- **Credentials**: Personal API Key in `.env` (GRAPHISTRY_USERNAME/PASSWORD)
- **Verdict**: adopted — best option for large Terraform dependency graphs (70+ nodes)

## Tools

| Tool | Description |
|------|-------------|
| `visualize_graph` | Upload edge/node data → interactive web visualization |
| `get_graph_info` | Get info about a rendered graph |
| `get_graph_ids` | List all rendered graphs |
| `apply_layout` | Change layout algorithm |
| `detect_patterns` | Community detection, centrality analysis |
| `encode_point_color` | Color nodes by attribute |
| `encode_point_size` | Size nodes by attribute |
| `apply_tree_layout` | Hierarchical tree layout (good for dependencies) |
| `health_check` | Verify connection to Graphistry |

## Auth

Uses Personal API Key (not username/password):
- `GRAPHISTRY_USERNAME` = Personal Key ID
- `GRAPHISTRY_PASSWORD` = Personal Secret Key
- Registered via `personal_key_id` / `personal_key_secret` in SDK

## Usage Chain

```
tfmcp (terraform_graph → nodes/edges) → graphistry-mcp (visualize_graph) → interactive URL
```

## When to Use

- Graph has 50+ nodes (static PNG unreadable)
- Need to explore relationships interactively
- Want community detection or centrality analysis
- Need to filter/search specific resources in a large graph

## When NOT to Use

- Small graphs (<20 nodes) → use quickchart-mcp (simpler, faster)
- Need a static image file → use quickchart-mcp or graphviz CLI
