# Coverage Map — Bench Completeness

> Que dimensões/scenarios o bench cobre, e onde tem gaps assumidos.

## Coverage Heatmap

| Dimension | Coverage | Confidence |
|---|---|---|
| Static metrics (file counts, LOC) | ✅ 100% | ALTA |
| License inspection | ✅ 100% | ALTA |
| README claims comparison | ✅ 100% | ALTA |
| Architecture pattern identification | ✅ 90% | ALTA |
| Runtime behavior verification | ⚠️ 0% | N/A (would require running each player) |
| Benchmark score verification | ⚠️ 50% | MEDIA (paper claims taken at face value) |
| Cost/performance benchmarks | ⚠️ 0% | N/A (would require running) |
| Security audit | ⚠️ 10% | LOW (only spot-check) |
| Community vibrancy (Discord/GitHub activity) | ⚠️ 30% | MEDIA |
| Real-user reviews / case studies | ⚠️ 10% | LOW |

## What's IN the bench

✅ **Static analysis:** file counts, LOC, license, structure
✅ **Architectural claims:** README + paper + clone structure
✅ **Comparison matrix:** 24 dimensions × 10 players
✅ **Scoring:** weighted aggregate with persona-specific overrides
✅ **Gap analysis:** 10 GAPs bidirecional
✅ **License risk:** per-player + cross-contamination matrix
✅ **Absorption playbook:** 3 waves × 12 sprints + decision table
✅ **Architecture blueprint:** mermaid + adoption map
✅ **8 scenario scorecards:** academic, founder, agency, enterprise, etc

## What's OUT of the bench (deliberate omissions)

❌ **Runtime performance benchmarks:** rodar cada player em hardware igual = ~40h work. Out of scope.
❌ **Cost per run real:** $0.08/run claim de GPT-Researcher não foi reproduzido — taken at face value.
❌ **Production case studies:** Hebbia $13M ARR / NVIDIA Nemotron adoption etc são single sources.
❌ **Security audit profundo:** OpenSSF Scorecard mencionado mas não verificado nos clones AIOX.
❌ **Internationalization:** DeerFlow tem 4 idiomas, AIOX PT-BR — não comparado quantitativamente.
❌ **UI/UX comparison:** apenas inventário, sem comparação visual ou usability test.

## Coverage Confidence vs Time Invested

| Activity | Time invested | Confidence delta |
|---|---|---|
| Clone 9 repos local | ~3 min | +20 |
| Read main READMEs | ~30 min | +25 |
| File count + license scan | ~5 min | +15 |
| Cross-research integration | ~45 min | +20 |
| Matrix scoring + aggregation | ~60 min | +15 |
| Deep dives (this folder) | ~90 min | +5 |
| **Total** | **~3.5h** | **88% confidence overall** |

Para ir de 88% → 95% confidence:
- Run actual deep-research-bench (~8h)
- Reproduce GPT-Researcher cost claims (~4h)
- Customer interviews on each tool (~16h)
- Total: ~28h extra. ROI marginal post-decision-making.

## Honest Limitations Disclosed

1. **AIOX score 60.25 é nosso self-assessment.** Bias minimizado mas presente.
2. **Scores subjetivos em algumas dimensões:** "MCP native quality" depende de implementation detail não verificada para todos.
3. **Stars/popularidade não verificada em real-time:** valores do research dossier original (16 maio 2026).
4. **Conference papers existence:** assumido baseado em README claims — não verificado em ACL/NeurIPS proceedings.

## Recommendation

**Bench atual é suficiente para decisões estratégicas P0/P1.** Para implementation (Wave 1+), validar específicos via:
- Reproducir GPT-Researcher PyPI install + MCP integration (1h)
- Reproduzir AutoResearchClaw Docker sandbox setup (2h)
- Rodar LocalDR para confirmar scholarly DB adapters (1h)

Total validation ~4h antes de Sprint 1 = ROI ótimo.
