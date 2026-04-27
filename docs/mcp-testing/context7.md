## MCP Test: context7

### Prompt
"Using MCP, find the latest official docs guidance for React hooks rules and summarize the key constraints with one source link."

### Result WITH MCP (enabled)
- Tools called: `context7` MCP documentation lookup and fetch.
- Output summary: Returned current React documentation guidance with direct source-backed summary and a concrete documentation link.

### Result WITHOUT MCP (disabled: true, or removed from .cursor/mcp.json)
- Tools available: no Context7 docs MCP.
- Output summary: Relied on model memory/general web fallback; response was less grounded in up-to-date official docs and lacked MCP-provided structured retrieval.

### Conclusion
`context7` improved factual grounding for library-specific answers by pulling current official docs instead of relying only on model memory.
