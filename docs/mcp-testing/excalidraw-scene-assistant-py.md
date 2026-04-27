# MCP Test: excalidraw-scene-assistant-py

### Prompt

"Use `excalidraw-scene-assistant-py` to summarize `examples/*.excalidraw`, extract text labels from one scene, and validate the file."

### Result WITH MCP (enabled)

- Tools called: `summarize_scene(path)`, `extract_text_labels(path, unique)`, `validate_scene(path)`
- Output summary: Returned structured scene metrics, extracted labels from text elements, and produced a validation report with issues/warnings in one workflow.

### Result WITHOUT MCP (disabled: true, or removed from .cursor/mcp.json)

- Tools available: generic filesystem/read tools only.
- Output summary: Agent had to manually parse raw JSON and reconstruct counts/validation checks ad hoc, which is slower and less consistent for repeated scene QA.

### Conclusion

With MCP, validation and metrics came from dedicated tools in one pass; without MCP, equivalent checks required manual JSON inspection and could easily miss consistency issues like duplicate IDs or missing fields.
