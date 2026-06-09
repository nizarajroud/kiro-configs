---
name: figma
description: Figma MCP — generate diagrams (FigJam), write to canvas, extract design context. Official remote server by Figma.
---
# Figma MCP Server

- **Status**: installed
- **JSON key**: `figma`
- **Type**: Remote (HTTP via mcp-remote bridge)
- **URL**: `https://mcp.figma.com/mcp`
- **Auth**: OAuth (browser prompt on first use)
- **Source**: https://github.com/figma/mcp-server-guide (1559 ⭐)
- **Docs**: https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP

## Skills disponibles

| Skill | Description |
|-------|-------------|
| `figma-generate-diagram` | Génère des diagrammes éditables dans FigJam (flowchart, sequence, ER, state, Gantt) |
| `figma-use` | Écrire du contenu sur le canvas Figma (frames, components, variables) |
| `figma-use-figjam` | Créer/modifier du contenu FigJam (stickies, sections, connecteurs) |
| `figma-use-slides` | Créer des présentations Figma Slides |
| `figma-create-new-file` | Créer un fichier Figma/FigJam vierge |
| `figma-code-connect` | Connecter composants Figma → code |
| `figma-generate-design` | Construire des écrans complets à partir du code |

## Rate limits

- **Starter (gratuit)**: 6 tool calls/mois
- **Dev/Full seat (payant)**: per-minute limits (Tier 1 REST API)
- Beta actuelle = fonctionnalités write-to-canvas gratuites

## Notes

- Pas d'API key nécessaire — OAuth via navigateur
- Les diagrammes FigJam sont des vrais nœuds + connecteurs (éditables, pas des images)
- Pour animation : utiliser Smart Animate dans Figma après génération
