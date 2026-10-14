# Capability Matrix — Granular

> Cada feature × cada player, status binário ou tier.

## Core Capabilities

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| Multi-wave search | ✅ (max 3) | ✅ | ✅ | ✅ | ✅ | ⚠️ trained-in | ⚠️ trained-in | ✅ (budget) | ✅ | ✅ |
| Auto-clarify | ✅ phase-0 | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Decompose subqueries | ✅ phase-1.5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Multi-agent orchestration | ⚠️ inline | ✅ true parallel | ✅ LangGraph | ❌ single | ❌ single | ❌ | ❌ | ❌ | ✅ | ✅ |
| Citation verify | ✅ CITATION_GATE | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Coverage gate | ✅ COVERAGE_GATE | ⚠️ | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ❌ |
| Wave compression | ✅ phase-3.6 | ⚠️ | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Deep read protocol | ✅ phase-3.2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Persona-fidelity inline | ✅ unique | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Models & Backends

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| BYOK (Claude/GPT/Gemini) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ self | ❌ self | ⚠️ Gemini default | ✅ | ⚠️ Qwen focus |
| Local LLM (Ollama) | ⚠️ partial | ✅ | ✅ | ✅ | ✅ | ✅ (own 30B) | ✅ (own 7B) | ✅ LocalLLM | ✅ | ✅ |
| Purpose-trained model | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 30B | ✅ 7B | ❌ | ❌ | ✅ 30B |
| HuggingFace model card | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |

## Storage & Memory

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| Cross-session memory | ❌ | ✅ TIAMAT | ❌ | ❌ | ✅ SQLCipher | ❌ | ❌ | ❌ | ⚠️ run-scoped | ❌ |
| Confidence scores stored | ⚠️ per-run | ✅ | ❌ | ❌ | ⚠️ | ❌ | ⚠️ | ❌ | ❌ | ❌ |
| Encrypted storage | ❌ | ❌ | ❌ | ❌ | ✅ SQLCipher | ❌ | ❌ | ❌ | ❌ | ❌ |
| Per-run learning log | ✅ incremental | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ |

## Sandbox & Code Execution

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| Docker code execution | ❌ | ✅ persistent | ⚠️ | ❌ | ✅ Docker GPU | ❌ | ⚠️ training | ⚠️ Dockerfile | ✅ hardened | ❌ |
| Network policy aware | ❌ | ⚠️ | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ✅ explicit | ❌ |
| Resource limits enforced | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ⚠️ | ✅ | ❌ |
| Read-only base FS | ❌ | ✅ | ❌ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ✅ | ❌ |

## Distribution & Integration

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| PyPI / npm package | ❌ | ⚠️ | ✅ PyPI | ⚠️ uv | ✅ PyPI | ❌ | ❌ | ✅ npm | ❌ | ❌ |
| Docker Hub image | ❌ | ✅ | ✅ | ⚠️ | ✅ | ❌ | ⚠️ | ✅ | ❌ | ❌ |
| MCP server native | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Headless API standalone | ⚠️ via skill | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ jina.ai/deepsearch | ⚠️ | ⚠️ |
| Claude Skill marketplace | ❌ | ❌ | ✅ skills.sh | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Multi-language docs | ❌ PT-BR only | ✅ 4 lang | ⚠️ EN+ZH | ❌ EN | ❌ EN | ❌ EN | ❌ EN | ❌ EN | ❌ EN | ⚠️ EN+ZH |

## Search Sources

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| Web search generic | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ corpus offline | ✅ | ✅ Jina Reader | ✅ | ✅ |
| arXiv | ❌ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ corpus | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| PubMed | ❌ | ❌ | ⚠️ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Semantic Scholar | ❌ | ❌ | ⚠️ | ❌ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| SearXNG self-hosted | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Custom MCP search tool | ❌ | ⚠️ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Output & Reports

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| Markdown report | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ Q&A only | ✅ | ✅ |
| PDF output | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | ❌ | ❌ | ❌ | ✅ paper | ❌ |
| DOCX output | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| HTML output | ⚠️ via app | ✅ | ✅ | ❌ | ✅ | ⚠️ HF demo | ❌ | ✅ jina.ai | ❌ | ❌ |
| Figures/charts generated | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ FigureAgent | ❌ |
| Structured artifacts (YAML) | ✅ players.yaml etc | ❌ | ⚠️ | ❌ | ⚠️ | ⚠️ | ❌ | ❌ | ✅ prompts.yaml | ❌ |

## Observability & Eval

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| Public benchmark score | ❌ | ❌ | ❌ | ✅ #6 DRB | ✅ 95% SQA | ✅ 54.8% BCP | ✅ +28.9pts | ❌ | ❌ | ❌ |
| Public eval logs | ❌ | ⚠️ | ⚠️ LangSmith | ⚠️ | ✅ community_bench/ | ✅ HF eval-logs | ⚠️ | ❌ | ⚠️ | ⚠️ |
| Dashboard UI | ✅ apps/research | ✅ frontend | ⚠️ | ⚠️ LangGraph | ⚠️ web basic | ⚠️ Gradio | ❌ | ✅ jina.ai/deepsearch | ❌ | ❌ |
| Security scan badges | ❌ | ❌ | ❌ | ❌ | ✅ OpenSSF+CodeQL+Semgrep | ❌ | ❌ | ❌ | ❌ | ❌ |

## Governance

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| COVERAGE_GATE | ✅ unique | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ 4-round audit | ❌ |
| CITATION_GATE | ✅ unique | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ❌ |
| Incremental learning log | ✅ per-phase | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ❌ |
| HITL granular modes | ❌ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 6 modes | ❌ |
| Multi-mode unified | ✅ 5 modes | ❌ 1 | ❌ 1 | ❌ 1 | ❌ 1 | ❌ 1 | ❌ 1 | ❌ 1 | ❌ 1 | ❌ 1 |

## License & Community

| Feature | AIOX | DeerFlow | GPT-R | LCO-DR | LDR | OpenR | DeepR | Jina | ARC | Tongyi |
|---|---|---|---|---|---|---|---|---|---|---|
| OSI license | ⚠️ Elastic v2 | ✅ MIT | ✅ Apache-2.0 | ✅ MIT | ✅ MIT | ✅ Apache-2.0 | ✅ Apache-2.0 | ❌ proprietary | ✅ MIT | ✅ Apache-2.0 |
| Discord/community channel | ⚠️ Sinkra Hub | ⚠️ | ✅ active | ⚠️ LangChain | ⚠️ | ⚠️ | ⚠️ academic | ⚠️ Jina | ⚠️ | ⚠️ WeChat |
| Top conference papers | ❌ | ❌ | ❌ | ⚠️ blog | ❌ | ✅ arXiv | ✅ arXiv | ❌ | ❌ | ✅ ACL+NeurIPS+more |

Legend: ✅ Yes | ⚠️ Partial / Inferred | ❌ No

## Capability Heatmap Summary

| Player | Total ✅ | Total ⚠️ | Total ❌ |
|---|---:|---:|---:|
| DeerFlow | 31 | 11 | 13 |
| **AIOX Research** | **27** | **10** | **18** |
| GPT-Researcher | 26 | 13 | 16 |
| AutoResearchClaw | 25 | 9 | 21 |
| Local DR | 24 | 12 | 19 |
| Tongyi | 17 | 11 | 27 |
| LangChain ODR | 16 | 10 | 29 |
| OpenResearcher | 14 | 12 | 29 |
| DeepResearcher | 14 | 13 | 28 |
| Jina | 13 | 11 | 31 |

AIOX está em **#2 em capabilities count** (atrás de DeerFlow), MAS perde em weighted scoring (60.25 vs 72.05) porque **muitos dos AIOX ✅ são em dimensões de menor peso (Governance, Planejamento)** e os ❌ estão em dimensões de maior peso (Sandbox, Distribuição, Modelo).
