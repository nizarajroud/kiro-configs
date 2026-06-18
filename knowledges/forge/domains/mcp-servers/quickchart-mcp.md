---
name: quickchart-mcp
description: Visual chart/graph renderer — takes DOT (Graphviz), Chart.js, or natural language and produces PNG/SVG/PDF images via QuickChart.io API.
---
# quickchart-mcp — Visual Graph & Chart Renderer

- **Status**: installed
- **JSON key**: `quickchart-mcp`
- **Agent**: exp2
- **Wrapper**: none (direct node)
- **Command**: `node /home/nizar/HomeWspce/kiro-configs/wrappers/quickchart-mcp-server/dist/index.js`
- **Source**: https://github.com/TakanariShimbo/quickchart-mcp-server (⭐50+)
- **Verdict**: adopted — renders DOT/Graphviz to images via MCP (chain with tfmcp)

## Tools (12)

| Tool | Description |
|------|-------------|
| `create-diagram-using-graphviz` | **DOT text → PNG/SVG image** (key for terraform graph chain) |
| `create-chart-using-chartjs` | Chart.js config → image |
| `create-chart-using-apexcharts` | ApexCharts config → image |
| `create-chart-using-googlecharts` | Google Charts → image |
| `create-chart-using-natural-language` | Natural language → chart image |
| `create-sparkline-using-chartjs` | Sparkline chart |
| `create-wordcloud` | Word cloud image |
| `create-barcode` | Barcode generation |
| `create-qr-code` | QR code generation |
| `create-table` | Table → image |
| `create-watermark` | Add watermark to image |
| `get-visualization-tool-help` | Help on available tools |

## Key Tool: `create-diagram-using-graphviz`

Input: DOT format string (from `terraform graph` or `tfmcp`)
Output: PNG or SVG image (URL or base64)

## Usage Chain

```
Step 1: tfmcp → terraform_graph → DOT text output
Step 2: quickchart-mcp → create-diagram-using-graphviz(dot=<DOT text>) → PNG image
```

## No Credentials Needed

Uses the public QuickChart.io API (free, no API key required).
