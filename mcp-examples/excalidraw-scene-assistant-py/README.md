# excalidraw-scene-assistant-py

Python FastMCP server for scene-aware Excalidraw analysis.

## Tools

| Tool | Description |
|------|-------------|
| `summarize_scene(path)` | Returns scene metrics (counts, labels, complexity) |
| `extract_text_labels(path, unique=False)` | Extracts text labels from text elements |
| `validate_scene(path)` | Runs lightweight scene consistency checks |

## Resource

- `excalidraw://scene-guidelines` — best-practice guidelines for clean scene files.

## Run locally

```bash
cd mcp-examples/excalidraw-scene-assistant-py
uv sync
uv run excalidraw-scene-assistant-mcp
```

## Wire into Cursor

Add this server entry to `.cursor/mcp.json`:

```json
"excalidraw-scene-assistant-py": {
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "./mcp-examples/excalidraw-scene-assistant-py",
    "excalidraw-scene-assistant-mcp"
  ],
  "disabled": true
}
```
