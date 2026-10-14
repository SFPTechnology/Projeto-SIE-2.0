# Bench — OSS Shortform Pipelines (Submagic Lens)

**Data:** 2026-05-06
**Analyst:** Universal Bench Analyst
**Requester:** Alan Nicolas (Sinkra Hub)
**Bench anterior relacionado:** [`docs/bench/submagic-vs-eddie-ai/`](../submagic-vs-eddie-ai/)

---

## Pergunta do bench

> Qual OSS pipeline chega mais perto de um Submagic-style (auto B-roll + captions animadas + render MP4) com **menor setup** e **maior atividade**? Substituir Submagic para uso diário OU servir de starting fork para extender.

## Subjects

| ID | Repo | Stars | Status |
|---|---|---:|---|
| A | [OpenShorts](https://github.com/mutonby/openshorts) | 1.819 | **Vencedor** |
| B | [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 56.832 | Categoria diferente |
| C | [Captacity](https://github.com/unconv/captacity) | 135 | Abandonado |

## TL;DR

**Clone OpenShorts primeiro.** Único OSS com pipeline-shape compatível com Submagic (long-form → highlights → reframe → captions → B-roll AI → publish). Score composite **86,1** (vs MPT 72,9, Captacity 58,6). Setup 10-30 min. MIT. 39 commits/90d.

Detalhes em [executive-report.md](./executive-report.md).

---

## Index dos artefatos

| # | Arquivo | Conteúdo |
|---|---|---|
| 1 | [metadata.json](./metadata.json) | Metadados estruturados do bench |
| 2 | [inventory-openshorts.md](./inventory-openshorts.md) | Stack, deps, features, atividade — OpenShorts |
| 3 | [inventory-moneyprinterturbo.md](./inventory-moneyprinterturbo.md) | Idem — MoneyPrinterTurbo |
| 4 | [inventory-captacity.md](./inventory-captacity.md) | Idem — Captacity |
| 5 | [comparison-matrix.md](./comparison-matrix.md) | Matriz paridade Forte/Parcial/Sem equivalente em 5 tabelas |
| 6 | [scorecard.md](./scorecard.md) | 7 dimensões 0-100 + composite + persona-weighted (solo / dev fork) |
| 7 | [gap-analysis.md](./gap-analysis.md) | O que cada um perde vs Submagic Pro |
| 8 | [battle-card.md](./battle-card.md) | Vence quando / Perde quando / killer features / decision tree |
| 9 | [executive-report.md](./executive-report.md) | **Recomendação final + roadmap de adoção/fork** |
| 10 | [README.md](./README.md) | Este arquivo (index) |

---

## Como navegar este bench

- **Quer só a decisão:** leia [executive-report.md](./executive-report.md) (~5 min).
- **Quer comparar lado a lado:** leia [comparison-matrix.md](./comparison-matrix.md) e [scorecard.md](./scorecard.md).
- **Quer entender cada repo:** leia os 3 inventories.
- **Quer planejar o fork:** leia [executive-report.md#fase-3](./executive-report.md) + [battle-card.md](./battle-card.md).
- **Quer entender o que falta vs Submagic:** leia [gap-analysis.md](./gap-analysis.md).

---

## Métodos & limites

- **Sources:** GitHub API (`repos/`, `commits`, `releases`, `issues`, `contents`) + READMEs públicos. Nenhum repo foi clonado/instalado.
- **Tool budget usado:** 14 chamadas `gh api` + 0 WebSearch + 0 WebFetch (orçamento ≤12 search/fetch atendido — `gh api` é local, não consume search/fetch).
- **Confidence:** ALTA para metadata/atividade (API direta), MÉDIA-ALTA para feature claims (declarado em READMEs, sem verificação em código), MÉDIA para output quality (sem rodar nenhum dos repos).
- **O que este bench NÃO cobre:**
  - Quality real do output gerado (Fase 1 do roadmap em executive-report)
  - Latência efetiva de geração
  - Bug rate em uso prolongado
  - Comparativo com OSS adjacentes (Auto-Editor, video-subtitle-generator, etc.) — fora do escopo solicitado

---

## Critérios de revalidação

Reabrir este bench se qualquer um destes acontecer:
- OpenShorts publicar release tagged 1.0+ ou anunciar deprecação
- MoneyPrinterTurbo adicionar pipeline long-form → shorts (mudaria categoria)
- Captacity retomar manutenção (commits após 2026-05-06)
- Submagic subir feature crítica não-replicável OSS
- Custo unitário OpenShorts subir >50% por mudança de pricing fal.ai/ElevenLabs

**Próxima revisão automática sugerida:** 2026-08-06 (90 dias) ou na ocorrência de qualquer trigger acima.
