# MCP Contract — Sinkra Research MCP Server

> Contrato da MCP server `@sinkra/research-mcp` (GAP-03).

## Server Identity

```json
{
  "name": "sinkra-research",
  "version": "0.1.0",
  "description": "Sinkra deep-research tools via MCP. Wraps /tech-research skill with governance gates.",
  "vendor": "Sinkra (alanicolas.com)",
  "license": "Apache-2.0",
  "homepage": "https://github.com/SynkraAI/sinkra-hub/tree/main/packages/@sinkra/research-mcp"
}
```

## Tools Exposed

### tool 1: `tech_research_query`

**Description:** Run a full deep technical research pipeline (7 molecules) and return the report path.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string", "description": "The research question or topic."},
    "mode": {"type": "string", "enum": ["default", "product-discovery", "deep"], "default": "default"},
    "max_waves": {"type": "integer", "default": 3, "minimum": 1, "maximum": 5},
    "language": {"type": "string", "enum": ["pt-BR", "en"], "default": "pt-BR"}
  },
  "required": ["query"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["success", "veto_coverage", "veto_citation", "halted"]},
    "report_path": {"type": "string"},
    "summary_md": {"type": "string"},
    "coverage_score": {"type": "number"},
    "citation_verified_ratio": {"type": "number"},
    "learning_log_path": {"type": "string"},
    "duration_seconds": {"type": "number"}
  }
}
```

### tool 2: `tech_research_followup`

**Description:** Add a follow-up question to an existing research folder.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "existing_slug": {"type": "string", "description": "Existing docs/research/{date}-{slug}/ folder"},
    "followup_question": {"type": "string"}
  },
  "required": ["existing_slug", "followup_question"]
}
```

### tool 3: `tech_research_status`

**Description:** Get status of a running or completed research.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "slug": {"type": "string"}
  },
  "required": ["slug"]
}
```

**Output:** YAML content of `.aiox/learning/logs/tech-research/{slug}-*.yaml` parsed.

## Transport

- **stdio:** default for Claude Desktop integration
- **HTTP/SSE:** opt-in for remote MCP server hosting

## Auth

- **stdio:** no auth (local process)
- **HTTP/SSE:** Bearer token + rate limit per client

## Error Codes

| Code | Description |
|---|---|
| `MCP_ERR_NO_HUB` | Sinkra Hub not detected in cwd |
| `MCP_ERR_NO_SKILL` | tech-research skill not installed |
| `MCP_ERR_INSUFFICIENT_DATA` | Query unclear after auto-clarify |
| `MCP_ERR_VETO_COVERAGE` | COVERAGE_GATE veto halt |
| `MCP_ERR_VETO_CITATION` | CITATION_GATE veto halt |
| `MCP_ERR_TIMEOUT` | Exceeded max_waves * timeout |

## Lifecycle

1. Client connects (stdio or HTTP)
2. Server responds with capabilities (3 tools above)
3. Client invokes tool with input
4. Server validates input schema
5. Server delegates to `/tech-research` skill (via Bash subprocess or direct Python import)
6. Server streams progress (if HTTP/SSE) via incremental log updates
7. Server returns output schema on completion

## Caching

- Same query within 24h returns cached `report_path` (skill detects existing folder)
- Cache invalidation via `--force` flag

## Reference Implementations

- LangChain Open Deep Research MCP integration: `../bench/langchain-open-deep-research/src/`
- GPT-Researcher MCP server: `../bench/gpt-researcher/` (search "mcp")
- MCP spec: https://modelcontextprotocol.io/

## Versioning

Semver. Breaking changes bump major. Tool schemas in `packages/@sinkra/research-mcp/schemas/v1/`.

## Compliance

- Apache-2.0 license
- NOTICE.txt listing dependencies
- Inspired by: LangChain Open Deep Research (MIT), GPT-Researcher (Apache-2.0)
- Original copyright: Sinkra (alanicolas.com)
