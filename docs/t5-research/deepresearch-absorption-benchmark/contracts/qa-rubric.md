# QA Rubric — Post-Absorption Acceptance

Critérios de qualidade para validar que cada gap foi absorvido sem regressões.

## Per-Gap Acceptance Criteria

### GAP-01 (Docker Sandbox)

| Test | Pass criterion |
|---|---|
| Container hardened | `docker inspect` confirms network policy + read-only base FS |
| Resource limits enforced | Cgroups CPU+memory enforced |
| Timeout works | Long-running command killed at 60s |
| SSE streaming | Output streams in real-time, not batched |
| Security audit | Internal pen test: cannot exfiltrate data |
| Phase YAML invokes when needed | Test: code-execution query auto-triggers sandbox |

**Acceptance:** 6/6 pass.

### GAP-02 (PyPI + Docker Hub)

| Test | Pass criterion |
|---|---|
| `pip install` clean | Fresh venv → install → run sample query |
| Docker pull + run | `docker run sinkra/research --query "..."` works |
| CI auto-publish | Tag `v0.1.0` → PyPI + Docker Hub atomically |
| NOTICE.txt valid | License-checker tool validates Apache-2.0 attribution |
| Standalone (no hub) | Runs without sinkra-hub clone |

**Acceptance:** 5/5 pass.

### GAP-03 (MCP)

| Test | Pass criterion |
|---|---|
| Claude Desktop integration | Tool appears in tools list |
| Cursor integration | Tool appears + invokes |
| stdio transport works | local subprocess works |
| HTTP/SSE transport works | Remote MCP server functional |
| Schema validation | Bad input rejected with clear error |
| Error codes consistent | All 6 error codes documented work |

**Acceptance:** 6/6 pass.

### GAP-04 (Model Backend)

| Test | Pass criterion |
|---|---|
| Auto-detect GPU | Correctly detects CUDA/MPS/CPU |
| Switch UI works | Backend selection persists per-session |
| BYOK fallback | Without GPU, falls back gracefully |
| Performance baseline | Same query: BYOK Claude vs DeepResearcher-7B baseline comparable |
| NOTICE compliance | Apache-2.0 attribution proper |

**Acceptance:** 5/5 pass.

### GAP-05 (Memory)

| Test | Pass criterion |
|---|---|
| Persist cross-session | Run query → restart → recall facts |
| Confidence scores recalculated | Decay over time observable |
| Phase 0 reads | New run consults memory pre-execution |
| Phase 5 writes | New facts persisted post-execution |
| Schema versioned | Migration scripts work |
| Performance under load | 10k facts → query <100ms |

**Acceptance:** 6/6 pass.

### GAP-06 (Scholarly DB)

| Test | Pass criterion |
|---|---|
| arXiv adapter | Query returns papers with abstracts |
| PubMed adapter | Medical query returns NLM hits |
| Semantic Scholar adapter | API quota OK |
| CITATION_GATE prefers scholarly | When available, scholarly cited first |
| Academic query test | Test query → ≥3 scholarly citations |

**Acceptance:** 5/5 pass.

### GAP-07 (Public Benchmark)

| Test | Pass criterion |
|---|---|
| Bench reproducible | Eval logs traceable |
| Score published | HF Spaces submission accepted |
| Badge on README | Visible in repo |
| Score vs baseline | Score ≥ 0.40 (LangChain ODR was #6 at 0.4344) |

**Acceptance:** 4/4 pass.

### GAP-08 (Parallel Subagents) [DEFERRED]

Não implementado neste roadmap. Reavaliar pós-Wave-2.

### GAP-09 (FigureAgent)

| Test | Pass criterion |
|---|---|
| Sandbox available | Depends GAP-01 |
| Generates accurate figures | Test: time-series query → correct PNG |
| Embedded in report | MD/PDF inclui figures |
| Multiple formats | PNG + SVG support |

**Acceptance:** 4/4 pass.

### GAP-10 (Dual License)

| Test | Pass criterion |
|---|---|
| AGPLv3 LICENSE present | Files added to `apps/research-community/` |
| Differentiation clear | README documents what's where |
| CI lint license headers | Both editions validated |

**Acceptance:** 3/3 pass.

## Regression Tests (run BEFORE each gap merge)

| Test | Pass criterion |
|---|---|
| COVERAGE_GATE still vetos | Test: shallow query → veto halt |
| CITATION_GATE still vetos | Test: low-citation-verify run → veto halt |
| Incremental learning log | Every phase logged |
| Product-discovery mode | JTBD framework still applies |
| Multi-mode unified | All 5 modes invocable |
| PT-BR vertical | PT-BR query → PT-BR output |
| Tri-layer separation | Squad+Skill+App still distinct |
| Workflow scaffold | New research folder structure intact |

**Acceptance:** All 8 pass before merging any gap.

## Overall Bench Re-scoring (post all gaps)

Re-run `comparison-matrix.json` scoring algorithm. Target:

- AIOX score: **≥ 88** (vs 60.25 baseline)
- AIOX ranking: **#1 or #2** in segment
- AIOX wins in scenarios: **≥5 of 8**

If targets missed → re-prioritize Wave 3.

## Quality Audit Sign-off

Bench re-score sign-off requires:
- @aiox-architect approval (architectural integrity)
- @aiox-qa approval (test coverage adequate)
- @aiox-pm approval (scenarios still match user need)
- Roundtable consensus (or 2-of-3 quorum)
