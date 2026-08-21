---
name: image-annotator-mcp
description: Annotate screenshots/images with markers, arrows, callouts, text labels (supports Arabic), rectangles, blur, and spotlight. Input = PNG image, output = annotated image.
---
# image-annotator-mcp — Screenshot & Image Annotation

- **Status**: installed
- **JSON key**: `image-annotator`
- **Agent**: exp2, compass (disabled by default)
- **Type**: Local (Node.js, stdio)
- **Command**: `node /home/nizar/HomeWspce/image-annotator-mcp/server.js`
- **Source**: https://github.com/vapvarun/image-annotator-mcp
- **Version**: v1.2.0
- **Dependencies**: Node.js ≥ 18, sharp
- **Verdict**: adopted — local image annotation, no API key, supports Arabic text

## Tools (7)

| Tool                  | Description                                              |
|-----------------------|----------------------------------------------------------|
| `annotate_screenshot` | Add professional annotations (markers, arrows, labels)   |
| `get_image_dimensions`| Get width, height, and format of an image                |
| `create_step_guide`   | Create a numbered step-by-step guide on a screenshot     |
| `highlight_area`      | Highlight a specific area with a shape + optional label  |
| `add_callout`         | Add a callout (speech bubble) pointing to a location     |
| `blur_area`           | Blur a rectangular area to hide sensitive information     |
| `frame_screenshot`    | Wrap a screenshot in a premium frame (rounded corners)   |

## Configuration

```json
"image-annotator": {
  "description": "Annotate screenshots/images with markers, arrows, callouts, text labels, blur, spotlight.",
  "command": "node",
  "args": ["/home/nizar/HomeWspce/image-annotator-mcp/server.js"],
  "disabled": true
}
```

## Use Cases

- Annotating architecture screenshots for documentation
- Creating step-by-step guides from UI screenshots
- Blurring sensitive data (emails, tokens, passwords) in screenshots
- Adding callouts/arrows to highlight specific elements
- Framing screenshots for professional docs/blog posts

## Notes

- No API key needed — 100% local processing via sharp
- Supports Arabic text in annotations (relevant for Tunisian explanations)
- Input/output: PNG images
- No secrets, no wrapper needed
