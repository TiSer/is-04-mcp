## MCP Test: excalidraw-scene-assistant-py

### Prompt
"Use `excalidraw-scene-assistant-py` to summarize `examples/*.excalidraw`, extract text labels from one scene, and validate the file."

### Result WITH MCP (enabled)
- Tools called: `summarize_scene(path)`, `extract_text_labels(path, unique)`, `validate_scene(path)`
- Output summary: Returned structured scene metrics, extracted labels from text elements, and produced a validation report with issues/warnings in one workflow.

### Result WITHOUT MCP (disabled: true, or removed from .cursor/mcp.json)
- Tools available: generic filesystem/read tools only.
- Output summary: Agent had to manually parse raw JSON and reconstruct counts/validation checks ad hoc, which is slower and less consistent for repeated scene QA.

### Conclusion
`excalidraw-scene-assistant-py` adds domain-specific scene analysis that improves accuracy and repeatability compared with manual JSON inspection.
