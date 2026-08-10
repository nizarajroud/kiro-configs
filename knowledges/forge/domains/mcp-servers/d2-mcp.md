---
name: d2-mcp
description: D2 diagram language MCP — compile, validate, and render diagrams (SVG, PNG, ASCII). Supports sketch mode (hand-drawn look), multiple layouts, themes. Go binary, 100% local.
---
# d2-mcp — D2 Declarative Diagramming

- **Status**: installed
- **JSON key**: `d2-mcp`
- **Agent**: **diagram1**
- **Type**: Local (Go binary, stdio)
- **Binary**: `/home/nizar/go/bin/d2-mcp`
- **Source**: https://github.com/h0rv/d2-mcp (⭐19)
- **Version**: v1.0.0
- **D2 CLI**: v0.7.1 (`~/.local/bin/d2`)
- **Verdict**: adopted — le plus populaire D2 MCP, Go, ASCII mode, cheat sheet intégré

## Tools

| Tool                  | Description                                              |
|-----------------------|----------------------------------------------------------|
| `compile-d2`          | Valider du code D2, détecter les erreurs de syntaxe      |
| `render-d2`           | Rendre un diagramme en SVG, PNG, ou ASCII                |
| `fetch_d2_cheat_sheet`| Retourner la cheat sheet D2 en Markdown                  |

## Formats de sortie

| Format | Usage                                        |
|--------|----------------------------------------------|
| SVG    | Diagrammes vectoriels (défaut)               |
| PNG    | Images raster (nécessite `rsvg-convert`)     |
| ASCII  | Diagrammes texte directement dans le CLI     |

## Configuration

```json
"d2-mcp": {
  "description": "D2 diagram language — compile, validate, and render diagrams (SVG, PNG, ASCII).",
  "command": "/home/nizar/go/bin/d2-mcp",
  "args": ["--image-type", "svg"],
  "disabled": false
}
```

## Exemples d'usage

- "Génère un diagramme D2 de l'architecture VPC avec 2 AZ"
- "Dessine un flowchart en style sketch (hand-drawn)"
- "Valide ce code D2 avant de le rendre"

## Notes

- 100% local, gratuit, pas d'API
- D2 supporte le mode sketch natif (hand-drawn look)
- ASCII mode = diagrammes lisibles directement dans le terminal
- Cheat sheet intégrée pour aider l'agent à écrire du D2 correct
