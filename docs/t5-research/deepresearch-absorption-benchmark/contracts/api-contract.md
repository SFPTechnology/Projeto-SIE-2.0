# API Contract — apps/research REST/SSE

> Endpoints REST + SSE em `apps/research/src/app/api/research/*`. Sinkra-specific.

## Base URL

- Local dev: `http://localhost:3001/api/research`
- Production: `https://research.sinkra.ai/api/research`

## Auth

- **Visitante público (demo only):** sem auth
- **AIOX Pro/Enterprise:** Bearer token (workspace-scoped)

## Endpoints

### POST `/api/research/runs`

Cria um novo research run.

**Request:**
```json
{
  "query": "string",
  "mode": "default | product-discovery | deep",
  "language": "pt-BR | en",
  "max_waves": 3,
  "model_backend": "claude | gpt | gemini | openresearcher | deepresearcher (post-GAP-04)"
}
```

**Response 201:**
```json
{
  "run_id": "string",
  "slug": "string",
  "status": "queued",
  "estimated_duration_seconds": 600
}
```

### GET `/api/research/runs`

Lista runs.

**Query params:** `limit`, `offset`, `status_filter`

### GET `/api/research/runs/[runId]`

Detalhes de um run.

**Response:**
```json
{
  "run_id": "string",
  "slug": "string",
  "status": "queued | running | completed | halted | failed",
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601 | null",
  "current_phase": "string",
  "coverage_score": 0.88,
  "citation_verified_ratio": 0.92,
  "artifacts": [
    {"path": "docs/research/{date}-{slug}/02-research-report.md", "size_bytes": 12000}
  ],
  "learning_log_path": ".aiox/learning/logs/tech-research/..."
}
```

### GET `/api/research/runs/[runId]/stream` (SSE)

Server-Sent Events stream of phase transitions and partial results.

**Event types:**
- `phase_start`: `{"phase": "phase-3-execute-research"}`
- `phase_complete`: `{"phase": "phase-3-execute-research", "outcome": "completed", "metrics": {...}}`
- `gate_evaluation`: `{"gate": "COVERAGE_GATE", "verdict": "APPROVE", "coverage": 0.88}`
- `artifact_written`: `{"path": "...", "format": "md"}`
- `run_complete`: `{"status": "success"}`
- `run_failed`: `{"status": "failed", "reason": "veto_coverage"}`

### POST `/api/research/uploads/audio`

Upload audio para transcription.

### POST `/api/research/uploads/files`

Upload files (PDFs, docs) para be referenced em research.

### GET `/api/research/clis`

Detect local CLIs (Claude Code, Codex, Gemini, OpenRouter). Post-GAP-04: detect GPU + local models.

### GET `/api/research/consolidations`

Aggregate múltiplos runs em consolidated report.

### POST `/api/research/runs/[runId]/sandbox/execute` (post-GAP-01)

**Request:**
```json
{
  "command": "python analyze.py",
  "timeout_seconds": 60,
  "network_allowlist": ["arxiv.org"]
}
```

**Response (SSE stream):**
- `stdout`: incremental output
- `stderr`: incremental errors
- `exit`: final exit code + duration

## Rate Limiting

- Visitante público (demo): 5 runs/dia
- Pro: 100 runs/dia
- Enterprise: ilimitado

## Error Codes

| HTTP | Code | Description |
|---|---|---|
| 400 | `INVALID_QUERY` | Query empty or malformed |
| 401 | `AUTH_REQUIRED` | Bearer token missing |
| 403 | `TIER_INSUFFICIENT` | Requires Pro/Enterprise |
| 409 | `EXISTING_RUN` | Same query already running |
| 429 | `RATE_LIMIT` | Rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Generic server error |
| 503 | `MAINTENANCE` | Server in maintenance |

## SSE Reconnection

Cliente deve enviar `Last-Event-ID` header para retomar stream após disconnect.

## Compatibility

- ✅ Compatible with `/observatory/[source]` UI consumption
- ✅ Compatible with MCP server (it can invoke API internally)
- ✅ Compatible with PyPI CLI (it can invoke API or skill directly)
