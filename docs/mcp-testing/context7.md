# MCP Test: context7

### Prompt

"Using MCP, find the latest official docs guidance for React hooks rules and summarize the key constraints with one source link."

### Result WITH MCP (enabled)

- Tools called: `context7` MCP documentation lookup and fetch.
- Output summary: Returned React guidance aligned to the official Rules of Hooks docs and provided a concrete source link for verification.

### Result WITHOUT MCP (disabled: true, or removed from .cursor/mcp.json)

- Tools available: no Context7 docs MCP.
- Output summary: Relied on model memory/general web fallback; response was less grounded in up-to-date official docs and lacked MCP-provided structured retrieval.

### Conclusion

With `context7`, the answer included a verifiable official docs source for Rules of Hooks; without MCP, the answer had no authoritative link and was harder to trust/review.
