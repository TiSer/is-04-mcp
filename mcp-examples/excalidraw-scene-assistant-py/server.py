"""excalidraw-scene-assistant-py - scene-aware MCP for Excalidraw files.

Tools:
    summarize_scene(path):      scene metrics and complexity hints
    extract_text_labels(path):  text labels from text elements
    validate_scene(path):       lightweight scene consistency checks

Resource:
    excalidraw://scene-guidelines
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("excalidraw-scene-assistant-py")
# server.py -> excalidraw-scene-assistant-py -> mcp-examples -> repo root
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def _ensure_workspace_path(path: str) -> Path:
    resolved = Path(path).resolve()
    try:
        resolved.relative_to(WORKSPACE_ROOT)
    except ValueError as exc:
        raise ValueError(f"Path must stay inside workspace: {path}") from exc
    if resolved.suffix != ".excalidraw":
        raise ValueError(f"Only .excalidraw files are allowed: {path}")
    return resolved


def _read_scene(path: str) -> dict[str, Any]:
    try:
        scene_path = _ensure_workspace_path(path)
        return json.loads(scene_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Scene file not found: {path}") from exc
    except PermissionError as exc:
        raise ValueError(f"Permission denied reading scene: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in scene file: {path}") from exc
    except OSError as exc:
        raise ValueError(f"Failed to read scene file: {path}") from exc


@mcp.tool()
def summarize_scene(path: str) -> dict[str, Any]:
    """Return high-level scene metrics and complexity hints."""
    scene = _read_scene(path)
    elements = scene.get("elements", [])
    active = [el for el in elements if not el.get("isDeleted", False)]

    counts_by_type: dict[str, int] = {}
    for element in active:
        key = str(element.get("type", "unknown"))
        counts_by_type[key] = counts_by_type.get(key, 0) + 1

    text_labels = [
        el.get("text", "").strip()
        for el in active
        if el.get("type") == "text" and isinstance(el.get("text"), str)
    ]
    text_labels = [label for label in text_labels if label]

    active_count = len(active)
    complexity = "low"
    if active_count > 80:
        complexity = "high"
    elif active_count > 30:
        complexity = "medium"

    return {
        "sceneType": scene.get("type", "unknown"),
        "version": scene.get("version"),
        "source": scene.get("source"),
        "totalElements": len(elements),
        "activeElements": active_count,
        "deletedElements": len(elements) - active_count,
        "countsByType": counts_by_type,
        "textLabelCount": len(text_labels),
        "sampleTextLabels": text_labels[:10],
        "hasFrames": counts_by_type.get("frame", 0) > 0,
        "hasConnectors": counts_by_type.get("arrow", 0) > 0,
        "estimatedComplexity": complexity,
    }


@mcp.tool()
def extract_text_labels(path: str, *, unique: bool = False) -> list[str]:
    """Extract text labels from non-deleted text elements."""
    scene = _read_scene(path)
    labels = [
        el.get("text", "").strip()
        for el in scene.get("elements", [])
        if el.get("type") == "text"
        and isinstance(el.get("text"), str)
        and not el.get("isDeleted", False)
    ]
    labels = [label for label in labels if label]
    if unique:
        labels = list(dict.fromkeys(labels))
    return labels


@mcp.tool()
def validate_scene(path: str) -> dict[str, Any]:
    """Run basic scene consistency checks."""
    scene = _read_scene(path)
    issues: list[str] = []
    warnings: list[str] = []

    if scene.get("type") != "excalidraw":
        warnings.append(f"Unexpected scene type: {scene.get('type', 'missing')}")

    elements = scene.get("elements")
    if not isinstance(elements, list):
        issues.append("Missing or invalid `elements` array.")
        elements = []

    if not isinstance(scene.get("appState"), dict):
        warnings.append("Missing or invalid `appState` object.")
    if not isinstance(scene.get("files"), dict):
        warnings.append("Missing or invalid `files` object.")

    seen_ids: set[str] = set()
    allowed_types = {
        "rectangle",
        "ellipse",
        "diamond",
        "line",
        "arrow",
        "text",
        "freedraw",
        "image",
        "frame",
        "embeddable",
        "magicframe",
        "iframe",
    }

    for index, element in enumerate(elements):
        element_id = element.get("id")
        element_type = element.get("type")

        if not element_id:
            issues.append(f"Element at index {index} is missing id.")
        elif element_id in seen_ids:
            issues.append(f"Duplicate element id found: {element_id}")
        else:
            seen_ids.add(element_id)

        if not element_type:
            issues.append(f"Element {element_id or f'#{index}'} is missing type.")
        elif element_type not in allowed_types:
            warnings.append(
                f"Element {element_id or f'#{index}'} uses unknown type: {element_type}",
            )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "elementCount": len(elements),
    }


@mcp.resource("excalidraw://scene-guidelines")
def scene_guidelines() -> str:
    """Return best practices for maintainable scene files."""
    return """# Excalidraw Scene Guidelines

- Use clear text labels so scene intent is readable in diffs and exports.
- Group related elements with frames when a diagram has multiple sections.
- Keep connector flow consistent (left-to-right or top-to-bottom).
- Avoid overlapping labels and connector arrows whenever possible.
- Prefer reusable style patterns for color and stroke to reduce visual noise.
"""


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
