# Inventory — MoneyPrinterTurbo

**Repo:** https://github.com/harry0703/MoneyPrinterTurbo
**Tagline:** *"利用AI大模型，一键生成高清短视频 — Generate short videos with one click using AI LLM."*

## Identidade & Atividade

| Atributo | Valor | Fonte |
|---|---|---|
| Stars | **56.832** | [GitHub API](https://api.github.com/repos/harry0703/MoneyPrinterTurbo) |
| Forks | **8.179** | idem |
| Issues abertas | 3 | idem |
| Linguagem dominante | Python | idem |
| Licença | MIT | idem |
| Criado em | 2024-03-11 | idem |
| Último commit | 2026-04-22 01:17 UTC | [commits](https://github.com/harry0703/MoneyPrinterTurbo/commits/main) |
| Commits últimos 90d | **48** | API |
| Última release | `v1.2.7` em 2026-04-03 | [releases](https://github.com/harry0703/MoneyPrinterTurbo/releases) |
| Releases totais | 3+ tagged (v1.2.5, v1.2.6, v1.2.7) | idem |
| Tamanho do repo | 532 MB (inclui assets/docs) | API |

**Sinal de atividade:** ALTO mas em modo manutenção. Commits recentes (abr/26) são fixes (Windows portable, Azure TTS, Gemini TTS subtitles, Redis Docker, sanitize subprocess). Sem grandes features novas; estabilidade incremental.

**Maturidade:** 2+ anos de vida, badge Trendshift, cobertura por publishers chineses. **É o repo mais notório do nicho.**

## Stack & Dependências

**Backend (Python 3.11):**
- `fastapi==0.115.6`, `uvicorn==0.32.1`
- `streamlit==1.45.0` — Web UI
- `moviepy==2.1.2` — composição
- `faster-whisper==1.1.0` — subtitle generation
- `edge_tts==7.2.7` — TTS Microsoft
- `azure-cognitiveservices-speech==1.41.1` — Azure TTS
- `openai==1.56.1`, `google.generativeai==0.8.6`, `dashscope` (Qwen), `g4f` (gpt4free)
- `redis==5.2.0` — queue
- `pydub==0.25.1` — audio

**Empacotamento:**
- `pyproject.toml` (primário) + `uv.lock` (recomendado) + `requirements.txt` (legacy pip)
- Python 3.11 fixado via `.python-version`

**Infra:**
- Docker + Docker Compose (CPU + GPU variants)
- Google Colab notebook oficial em `docs/MoneyPrinterTurbo.ipynb`
- ImageMagick **dependência externa obrigatória** (Windows precisa static build)
- Windows one-click pack (legacy v1.2.6)

**Estrutura `app/services/`:**
- `llm.py` — múltiplos providers (OpenAI, Moonshot, Azure, gpt4free, one-api, Qwen, Gemini, Ollama, DeepSeek, MiniMax, Wenxin, Pollinations, ModelScope)
- `material.py` — fontes de stock (Pexels obrigatório)
- `subtitle.py` — captions
- `task.py` — orquestração
- `voice.py` — TTS multi-provider
- `video.py` — composição
- `upload_post.py` — publish

Fonte: [requirements.txt](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/requirements.txt) + [README](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/README.md).

## Features (declaradas no README)

- Geração 100% automática a partir de **tema/keyword** (não de vídeo longo)
- Pipeline: tema → script (LLM) → busca de stock (Pexels) → TTS → legendas → BGM → composição
- **MVC architecture** clara, com API + WebUI Streamlit
- **9:16 (1080×1920)** e **16:9 (1920×1080)**
- Geração em **batch** (múltiplos vídeos por execução)
- Subtitle styling: fonte/posição/cor/tamanho/stroke
- BGM aleatória ou específica, com volume ajustável
- Suporta **PT-BR** indiretamente via TTS multi-language e modelos
- Multi-provider LLM (treze providers listados)
- Pexels API key **obrigatória** para fontes de B-roll

## Setup Effort

**Recomendado:**
```
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
uv python install 3.11
uv sync --frozen
# instalar ImageMagick (apt/brew/exe estático)
# editar config.toml (pexels_api_keys + llm_provider)
uv run streamlit run ./webui/Main.py
```

**Docker:**
```
docker-compose up
# WebUI http://localhost:8501, API http://localhost:8080/docs
```

**Friction points:**
- ImageMagick external dep (especialmente chato em Windows — precisa **static build** específico, path fixo)
- Pexels API key obrigatória
- LLM provider key obrigatória
- README primário em chinês (English `README-en.md` mas menos atualizado)
- Caminhos com caracteres não-ASCII quebram

**Tempo estimado:** **30-90 min** primeira vez (ImageMagick + uv + keys + config).

## Sinais de saúde do projeto

- 48 commits/90d, 56k stars, 8k forks → **referência absoluta do nicho**
- 3 releases tagged em 2026-2025 → cadência semestral
- Issues 3 abertas → mantenedor reativo (issues novas são geralmente PRs em formato issue)
- Trendshift award
- 2+ anos sem morrer

## Watermark / Render / Output

- **Watermark:** Nenhum
- **Render:** moviepy + ImageMagick + ffmpeg
- **Output:** MP4 9:16 ou 16:9 HD

## Equivalência funcional vs Submagic

| Submagic feature | MoneyPrinterTurbo? |
|---|---|
| Auto-captions animadas | Sim — faster-whisper + estilização |
| B-roll automático | **Parcial** — só **stock Pexels** (não AI-generated) |
| Highlight clipping de podcast | **Não** — pipeline é tema→video, não vídeo longo→shorts |
| 9:16 smart reframe | N/A (gera vertical já) |
| Hook overlays | Não (subtitle styling sim, mas sem hook overlays animados) |
| Multi-platform publish | Existe `upload_post.py` mas é integration-tier |
| AI Avatar / UGC | **Não** |

**Categoria:** "Faceless content factory" tipo MoneyPrinterV1 → diferente do escopo Submagic (que parte de vídeo existente).

## Riscos

- **Não é Submagic substitute direto:** o use case é diferente (tema → vídeo, não corte de podcast)
- **ImageMagick dep** quebra setup pra usuários menos técnicos
- **Pexels** como única fonte de B-roll → repetição visual em produção em escala
- **Codebase chinesa primária:** PRs em inglês podem ser ignoradas
- README declara que **upload-post** doc foi removido em 2026-04-03 → social publishing está deprecado/instável
