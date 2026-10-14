# Executive Report — OSS Shortform Pipelines

**Para:** Alan Nicolas (Sinkra Hub)
**Data:** 2026-05-06
**Lente:** substituir Submagic OU prover starting fork para produto Sinkra
**Subjects:** OpenShorts, MoneyPrinterTurbo, Captacity

---

## Veredicto Direto

**Clone primeiro: [OpenShorts](https://github.com/mutonby/openshorts).**

Em uma frase: é o **único OSS do trio** que entrega o pipeline-shape correto (vídeo longo → highlights → reframe 9:16 → captions animadas → B-roll AI → publish multi-plataforma) com **zero watermark**, **zero limit**, **MIT**, mantenedor ativo (39 commits/90d, 9 commits no dia do bench), e arquitetura compatível com a stack Sinkra Hub (FastAPI + React + Docker).

**Score composite:** OpenShorts **86,1** vs MoneyPrinterTurbo **72,9** vs Captacity **58,6**.
**Persona "solo creator":** OpenShorts **85,2** vs MPT **64,4** vs Captacity **49,8**.
**Persona "developer fork":** OpenShorts **85,0** vs MPT **72,7** vs Captacity **50,2**.

---

## Ordem de Avaliação Recomendada

### Fase 1 — Confirmação (1 hora)
1. **Clonar OpenShorts** localmente (não no Sinkra Hub).
2. `docker compose up --build`.
3. Configurar 4 keys (Gemini grátis em [aistudio](https://aistudio.google.com/app/apikey), fal.ai pay-per-use, ElevenLabs free tier, Upload-Post free tier 10/mês).
4. Rodar Clip Generator num podcast existente seu (Allfluence ou Bilhon).
5. Avaliar 3 outputs: qualidade da reframe 9:16, qualidade da viral moment detection, qualidade dos hooks.
6. **Decisão:** se output ≥ 70% Submagic-quality → Fase 2. Senão → Fase 3.

### Fase 2 — Daily Driver (1 semana)
7. Substituir Submagic no fluxo daily de uma das 4 businesses (sugestão: AllFluence, que tem mais shorts).
8. Medir: custo médio/vídeo, tempo de geração, NPS interno.
9. Se passar → adotar como fluxo padrão em todas as 4 businesses.

### Fase 3 — Fork Estratégico (3-4 semanas, opcional)
10. **Fork** (não clone vanilla) como `@sinkra/shortform-engine` (gh + Sinkra Hub).
11. Hardening prioritário (em ordem):
    - PT-BR first-class nos prompts (script gen + hooks + thumbnails)
    - Catálogo curado de caption presets (5-10 estilos Sinkra)
    - Swap parcial fal.ai → providers mais baratos para reduzir custo unitário
    - Testes automatizados (pytest + golden frames + CI matrix Python 3.11)
    - Integração com Sinkra Hub (CODEOWNERS, story-driven, validators YAML)
12. Roubar do MoneyPrinterTurbo: `app/services/llm.py` multi-provider abstraction (13 providers swappable, código MVC limpo).

### Fase 4 — Componentização (futuro)
13. Extrair packages reutilizáveis:
    - `@sinkra/whisper-captions` (substitui Captacity, com manutenção)
    - `@sinkra/viral-moment-detector` (Gemini-based)
    - `@sinkra/smart-reframe` (MediaPipe + YOLOv8)
14. Publicar via GitHub Package Registry (`@sinkra/*` pattern já existente).

---

## Arquitectural Learnings — O Que Roubar de Cada Repo Antes de Forkar

### De OpenShorts (the base)
- **Pipeline shape correto** para Submagic-replacement (long-form → shorts).
- **Dual-mode reframe** (TRACK vs GENERAL): fallback inteligente quando face tracking falha. Ver `subtitles.py`, `editor.py`.
- **AI Shorts UGC pipeline** (Flux 2 Pro + Hailuo + VEED Lipsync) — única referência OSS dessa categoria.
- **Encrypted client-side keys** + non-root container + auto-cleanup 1h: padrão de segurança para self-host.
- **Gallery SEO** (JSON-LD + og:video) — pattern de publish público.
- **`MAX_CONCURRENT_JOBS` semáforo** — modelo de queue simples sem Redis.

### De MoneyPrinterTurbo (the giant)
- **`app/services/llm.py`** — abstração multi-provider (OpenAI/Moonshot/Azure/Qwen/Gemini/Ollama/DeepSeek/MiniMax/etc.) é provavelmente a melhor referência OSS dessa abstração. **Roubar inteiro.**
- **MVC structure** (`app/services/{llm,material,task,subtitle,voice,video}.py`) — 6 services bem cortados, alinha com o KISS/no-overengineering Sinkra.
- **uv + pyproject.toml + uv.lock + requirements.txt fallback** — modelo dual de empacotamento Python.
- **Colab notebook oficial** — pattern de zero-setup demo. Útil para Sinkra Hub fazer onboarding/demo.
- **Multi-language READMEs** (PT-CN/EN) — pattern de internacionalização desde dia 1.

### De Captacity (the abandoned)
- **API minimalista** `add_captions(video, output, **styling)` — referência de DX limpa para um caption-renderer próprio.
- **`text_drawer.py`** — código didático de rendering de captions com stroke/shadow/highlight. Use como base de leitura, não de import.
- **Lição:** abandono de single-maintainer projects é a regra, não exceção. Decisão Sinkra: **fork sempre, depend nunca** em libs sem governança visível.

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| OpenShorts vendor-lock em fal.ai | Alta | Alto (custo $0,65-2/short) | Fork e abstrair providers (roubar de MPT) |
| OpenShorts API breaks frequentes (5 meses, 0 releases tagged) | Alta | Médio | Pin commit hash, não branch |
| Submagic subir feature crítica que OSS não tem | Média | Médio | Manter fluxo dual durante 30 dias; migração reversível |
| Custos AI explodirem em escala | Média | Alto | Budget cap + provider swap + cache de B-roll |
| Mantenedor de OpenShorts mudar foco | Baixa-Média | Alto | Fork interno Sinkra desde o dia 1 |

---

## O que NÃO fazer

1. **Não usar Captacity em produção.** Está abandonado.
2. **Não tentar adaptar MoneyPrinterTurbo para virar Submagic.** Pipeline-shape é incompatível; reescrever seria comparable a forkar OpenShorts.
3. **Não fazer fork-and-merge-back upstream para OpenShorts** sem antes alinhar com mantenedor (greenfield repos têm style fortemente do criador, especialmente com CLAUDE.md no repo indicando dev assistido por Claude).
4. **Não subir Sinkra fork para produção sem testes.** OpenShorts não tem CI/testes visíveis — Sinkra Hub adiciona como blocker pré-merge.
5. **Não publicar `@sinkra/shortform-engine` sem story.** Constitution exige story-driven.

---

## Conclusão

**OpenShorts é o caminho.** Score, atividade, escopo e DX convergem. MoneyPrinterTurbo é referência arquitetural valiosa mas categoria errada para Submagic-replacement. Captacity é leitura de código, não dependência viva.

**Próximo passo concreto:**
1. Criar story `sinkra-shortform-engine-fase-1-confirmation` em `docs/stories/`.
2. Spike de 1h em ambiente local (não Sinkra Hub repo).
3. Decisão go/no-go até 2026-05-13.

---

## Referências

- [Bench Submagic vs Eddie AI (anterior)](../submagic-vs-eddie-ai/)
- [Inventário OpenShorts](./inventory-openshorts.md)
- [Inventário MoneyPrinterTurbo](./inventory-moneyprinterturbo.md)
- [Inventário Captacity](./inventory-captacity.md)
- [Matriz de comparação](./comparison-matrix.md)
- [Scorecard](./scorecard.md)
- [Gap analysis](./gap-analysis.md)
- [Battle card](./battle-card.md)
