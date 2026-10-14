# Evidence Strength Map

> Cada claim no bench tem confidence rastreável. Esta tabela é o índice.

## Confidence Tiers

- **ALTA** (>80%): Direct evidence (file path, line number, URL verificada, paper arXiv)
- **MEDIA** (50-80%): Inferred from README + paper claims sem reprodução local
- **BAIXA** (<50%): Especulativo, baseado em sinal indireto

## Evidence Index

| Claim | Confidence | Source |
|---|---|---|
| AIOX squad/research v5.0.0 (14 agents) | ALTA | `squads/research/config.yaml:1-32` |
| AIOX skill /tech-research v2.0.0 (7 molecules) | ALTA | `.claude/skills/tech-research/SKILL.md:1-50` |
| AIOX app Elastic License v2 | ALTA | `apps/research/README.md` |
| AIOX 129 .md files no squad | ALTA | `find squads/research -name '*.md' \| wc -l` = 129 |
| AIOX 13 phase YAMLs | ALTA | `ls squads/research/workflows/tech-research/` |
| DeerFlow 474py + 138ts | ALTA | `find ../bench/deer-flow -name '*.py'` = 474 |
| DeerFlow MIT license | ALTA | `cat ../bench/deer-flow/LICENSE` |
| DeerFlow 66k+ stars | MEDIA | original research dossier (não verificado direto no GitHub API) |
| GPT-Researcher 191 py files | ALTA | clone scan |
| GPT-Researcher Apache-2.0 | ALTA | LICENSE 11357 bytes |
| GPT-Researcher MCP Server | ALTA | README badge + skills.sh listing |
| LangChain ODR #6 DeepResearchBench 0.4344 | ALTA | README explicit + HF leaderboard link |
| LangChain ODR 22 py files | ALTA | clone scan |
| Local DR ~95% SimpleQA | ALTA | README badge |
| Local DR 2269 py files | ALTA | clone scan |
| Local DR SQLCipher encrypted | ALTA | docker-compose includes |
| Local DR Vitalik endorsement | MEDIA | original research dossier — URL verificada |
| OpenResearcher 30B-A3B BrowseComp-Plus 54.8% | MEDIA | arXiv paper + HF model card (não reproduzido) |
| OpenResearcher NVIDIA Nemotron adoption | ALTA | README banner |
| OpenResearcher 10 py files | ALTA | clone scan |
| DeepResearcher 7B (Qwen2.5 + GRPO) | ALTA | arXiv 2504.03160 + README |
| DeepResearcher +28.9 pts | MEDIA | paper claim, não reproduzido |
| Jina node-DR 57 ts files | ALTA | clone scan |
| Jina proprietary license | ALTA | LICENSE first line "Copyright 2020-2025 Jina AI Limited. All rights reserved." |
| AutoResearchClaw 23 stages | MEDIA | README claim, não validated stage-by-stage |
| AutoResearchClaw network-policy-aware Docker | MEDIA | README claim |
| AutoResearchClaw 363 py files | ALTA | clone scan |
| Tongyi 30B-A3B model | ALTA | HF model card + arXiv 2510.24701 |
| Tongyi WebWalker ACL 2025 + WebDancer NeurIPS 2025 | MEDIA | README claims, papers existem em respective venues |
| Tongyi 174 py files | ALTA | clone scan |
| Scorecard AIOX = 60.25 | ALTA | Computed from comparison-matrix.json via weighted aggregation |
| AIOX wins 3/8 scenarios | ALTA | scenario-scorecards.json |
| 10 GAPs identified | ALTA | gap-analysis.json |

## Confidence Distribution

- **ALTA:** ~75% of claims
- **MEDIA:** ~25%
- **BAIXA:** 0% (deliberadamente nenhum claim sem evidence)

## Anti-fabrication Policy

Toda métrica numérica (file counts, scores, dates) é **verificada por scan local** ou **citação direta de README/paper**. Não há claims fabricados.

Se confidence é MEDIA, está explicitamente marcado no inventory MD do player ou nesta tabela.
