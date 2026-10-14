# Matriz de Comparação — OpenShorts × MoneyPrinterTurbo × Captacity

**Lente:** proximidade ao Submagic-style (auto B-roll + captions animadas + render MP4) com setup baixo e atividade alta.

**Legenda:**
- **Forte** = entrega o item com qualidade comparável ou superior à categoria comercial
- **Parcial** = entrega o item mas com limitações relevantes
- **Sem equivalente** = não entrega o item

---

## Tabela 1 — Identidade e Saúde do Projeto

| Dimensão | OpenShorts | MoneyPrinterTurbo | Captacity |
|---|---|---|---|
| **Stars** | 1.819 | **56.832** | 135 |
| **Forks** | 488 | **8.179** | 40 |
| **Idade** | 5 meses (greenfield) | 26 meses (maturo) | 26 meses (mas dormente) |
| **Último commit** | 2026-05-06 | 2026-04-22 | **2024-06-07** |
| **Commits últimos 90d** | **39** | **48** | **0** |
| **Releases tagged** | 0 (pré-1.0) | v1.2.7 + 2 anteriores | v0.3.1 (2024) |
| **Issues abertas** | 22 | 3 | 9 (sem resposta) |
| **Stack primária** | Python 3.11 + React 18 + Vite | Python 3.11 + Streamlit | Python (lib) |
| **Atividade** | **Forte** | **Forte** | **Sem equivalente** |
| **Stars (proxy de adoção)** | Parcial | **Forte** | Sem equivalente |

Fontes: [OpenShorts API](https://api.github.com/repos/mutonby/openshorts), [MPT API](https://api.github.com/repos/harry0703/MoneyPrinterTurbo), [Captacity API](https://api.github.com/repos/unconv/captacity).

---

## Tabela 2 — Capabilities Funcionais (Submagic Lens)

| Capability Submagic | OpenShorts | MoneyPrinterTurbo | Captacity |
|---|---|---|---|
| **Captions animadas word-level** | Forte (ASS burned + Gemini styling) | Forte (faster-whisper + estilização configurável) | Forte (word_highlight_color + stroke + shadow) |
| **B-roll automático** | **Forte** (Flux 2 Pro + Ken Burns AI-generated) | Parcial (apenas stock Pexels) | Sem equivalente |
| **Highlight / viral moment detection** | **Forte** (Gemini 3.0 Flash em transcript + scene) | Sem equivalente (parte de tema, não de vídeo longo) | Sem equivalente |
| **9:16 smart reframe (face/subject tracking)** | **Forte** (TRACK = MediaPipe + YOLOv8; GENERAL = blurred bg) | N/A (gera nativo 9:16) | Sem equivalente |
| **Hook text overlays AI-generated** | **Forte** (Gemini-generated) | Sem equivalente | Sem equivalente |
| **AI Video Effects (filters)** | **Forte** (Gemini → FFmpeg filters) | Sem equivalente | Sem equivalente |
| **Voice dubbing multi-idioma** | **Forte** (ElevenLabs 30+ idiomas, voice cloning) | Parcial (TTS multi mas sem dubbing automático) | Sem equivalente |
| **AI Avatar / UGC actors** | **Forte** (Flux 2 Pro + Hailuo + VEED Lipsync) | Sem equivalente | Sem equivalente |
| **Render para MP4** | Forte (FFmpeg + Remotion) | Forte (moviepy + ffmpeg) | Forte (moviepy) |
| **Watermark policy** | **Forte** (zero, declarado no README) | **Forte** (zero) | **Forte** (zero) |
| **Social auto-publish** | **Forte** (TikTok + IG + YT via Upload-Post; com schedule) | Parcial (`upload_post.py` existe mas docs removidos abr/26) | Sem equivalente |
| **Stock library nativa** | Parcial (foca em AI gen) | Forte (Pexels integrado) | Sem equivalente |
| **YouTube Studio (titles, thumbnails, descriptions)** | **Forte** | Sem equivalente | Sem equivalente |
| **Schedule uploads** | **Forte** | Sem equivalente | Sem equivalente |
| **Multi-LLM provider** | Parcial (Gemini-locked) | **Forte** (13 providers: OpenAI, Moonshot, Azure, Qwen, Gemini, Ollama, DeepSeek, MiniMax, etc.) | Parcial (OpenAI Whisper + local) |
| **Idiomas suportados (legendas/script)** | Parcial (script EN/ES; subtitles via Whisper qualquer idioma) | Forte (chinês/inglês first-class; outros via TTS) | Forte (Whisper multilang, mas sem RTL — issue aberta) |

---

## Tabela 3 — DX, Setup e Operação

| Aspecto | OpenShorts | MoneyPrinterTurbo | Captacity |
|---|---|---|---|
| **Comando de setup mínimo** | `docker compose up --build` | `uv sync --frozen && uv run streamlit run …` (ou docker) | `pip install captacity` |
| **Tempo de setup estimado** | 10-30 min | 30-90 min | **3 min** |
| **Dependências externas (não-pip)** | Docker | Docker **OU** ImageMagick + uv | nenhuma (moviepy traz o necessário) |
| **API keys obrigatórias** | 4 (Gemini + fal.ai + ElevenLabs + Upload-Post) | 2 (LLM provider + Pexels) | 1 (OpenAI, ou nenhuma com `[local_whisper]`) |
| **Custo médio por vídeo** | $0.65-2 (AI Shorts) / <$0.01 (Clip) | <$0.05 (LLM cheap + Pexels grátis) | $0 (local) ou ~$0.01 (Whisper API) |
| **WebUI** | React custom (Vite) | Streamlit | CLI only |
| **API HTTP** | FastAPI nativo | FastAPI + Streamlit | Não (lib Python) |
| **Job queue / batch** | Async com `MAX_CONCURRENT_JOBS` | Batch nativo (gera N variações) | N/A |
| **Documentação** | README + comparativo + tutorial vídeo | README PT-CN/EN + Colab + Douyin tutorials | README curto e direto |
| **DX (overall)** | **Forte** | Parcial (ImageMagick é fricção real) | **Forte** (mas escopo mínimo) |

---

## Tabela 4 — Licenciamento e Distribuição

| Aspecto | OpenShorts | MoneyPrinterTurbo | Captacity |
|---|---|---|---|
| Licença | MIT | MIT | MIT |
| Permissive (uso comercial) | Forte | Forte | Forte |
| CLA / DCO requerido | Não | Não | Não |
| Pacote pip publicado | Não | Não | **Sim** (`captacity==0.3.1`) |
| Docker image oficial | Sim (Compose) | Sim (CPU + GPU) | Não |
| Colab notebook | Não | **Sim** ([docs/MoneyPrinterTurbo.ipynb](https://github.com/harry0703/MoneyPrinterTurbo/blob/main/docs/MoneyPrinterTurbo.ipynb)) | Não |

---

## Tabela 5 — Adequação ao Use Case "Substituir Submagic"

| Use case Alan | Quem ganha | Porquê |
|---|---|---|
| Cortar podcast/live em shorts virais com captions+B-roll | **OpenShorts** | É o único do trio com viral moment detection + smart reframe + AI B-roll |
| Gerar shorts faceless (tema → vídeo) | **MoneyPrinterTurbo** | Único com pipeline tema→vídeo end-to-end estabilizado |
| Adicionar captions a vídeos já editados | **Captacity** | Lib pip mais leve para essa única tarefa |
| Fork como base de produto Sinkra próprio | **OpenShorts** | Greenfield, modular, FastAPI+React, README polido, MIT, mantenedor ativo |
| Pipeline auto-publish daily (cronjob) | **OpenShorts** | Único com schedule + multi-platform publish nativo |

---

## Resumo Executivo da Matriz

1. **OpenShorts é o único com proximidade real ao Submagic** (B-roll AI + captions + reframe + publish em um stack só). Custo: dependência forte de fal.ai e ElevenLabs.
2. **MoneyPrinterTurbo é o gigante adjacente**: 56k stars validam o nicho mas o pipeline é "tema → faceless video", não "vídeo longo → shorts". Não é Submagic substitute.
3. **Captacity é uma capability isolada e abandonada.** Útil como referência de código para um caption-renderer próprio, sem mais.
