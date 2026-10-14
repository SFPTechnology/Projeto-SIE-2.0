# Battle Card — OSS Shortform Pipelines

**Para:** Alan Nicolas (Sinkra Hub) — decisão de qual repo clonar primeiro.
**Lente:** substituir Submagic OU base de fork para produto Sinkra.

---

## TL;DR — Em 30 segundos

| | OpenShorts | MoneyPrinterTurbo | Captacity |
|---|:---:|:---:|:---:|
| **Substitui Submagic?** | **Sim** | Não (categoria diferente) | Não (parcial) |
| **Bom para fork?** | **Sim** | Sim (fallback) | Não (abandonado) |
| **Setup time** | 10-30 min | 30-90 min | 3 min |
| **Composite score** | **86,1** | 72,9 | 58,6 |
| **Veredicto** | **CLONE FIRST** | Avaliar como referência | Skip (use só p/ inspiração de código) |

---

## OpenShorts — Battle Card

### Vence quando…
- Você quer **substituir Submagic agora** com self-host
- Use case = cortar podcast/live em shorts (Clip Generator) **OU** gerar UGC com AI avatar
- Você aceita custo variável ($0,65-2/short) em troca de zero watermark + dados privados
- Você quer fork ativo com mantenedor responsivo

### Perde quando…
- Você precisa de editor visual de timeline (não tem)
- Você precisa de analytics pós-publish integrado
- Você precisa de templates curados de captions (tem styling, sem catálogo)
- Custos AI > $50/mês não cabem no budget

### Killer features
1. **Viral moment detection via Gemini 3.0** — única do trio
2. **Dual-mode 9:16 reframe** (TRACK face + GENERAL blur)
3. **AI Shorts UGC** (Flux 2 Pro + Hailuo + VEED Lipsync) — **acima do tier Submagic**
4. **YouTube Studio** completo (thumbs + titles + descriptions + publish)
5. **Schedule + multi-platform publish** nativo

### Riscos
- Repo tem 5 meses (greenfield) → APIs vão quebrar
- 80% das features AI passam por fal.ai → vendor risk
- 0 releases tagged → instabilidade entre commits
- Sem testes automatizados visíveis

### Stack
Python 3.11 + FastAPI + faster-whisper + MediaPipe + YOLOv8 + PySceneDetect + React 18 + Vite + Tailwind + Docker + Remotion (subdir).

---

## MoneyPrinterTurbo — Battle Card

### Vence quando…
- Você quer **faceless content factory** (tema → vídeo, sem usar vídeo existente)
- Você quer **multi-LLM provider flexibility** (13 providers, inclui Ollama local)
- Você quer rodar em **GPU local** com batch generation
- Você precisa de pipeline maduro com 56k stars de validação social

### Perde quando…
- Use case é cortar vídeo longo (não suporta)
- Você quer B-roll AI-generated (só Pexels stock)
- Setup precisa ser fácil (ImageMagick é fricção real)
- Você quer evitar streamlit como UI (form-based, sem editor)

### Killer features
1. **13 LLM providers** swappable em runtime
2. **Batch generation** (N variações por execução)
3. **Comunidade enorme** (8k forks, 1 issue ≈ 50 forks resolvendo)
4. **Colab notebook oficial** (zero setup)
5. **Codebase MVC limpa** (`app/services/{llm,material,task,subtitle,voice,video}.py`)

### Riscos
- Categoria errada para use case Submagic
- Mantenedor pivota lentamente (release v1.2.7 em abr/26 é manutenção, não feature)
- README primário em chinês → PRs em inglês podem ficar parados
- `upload-post` doc removido em abr/26 → social publishing está em flux

### Stack
Python 3.11 + Streamlit + FastAPI + moviepy + faster-whisper + edge-tts + Azure TTS + 13 LLM providers + Redis + Docker + ImageMagick.

---

## Captacity — Battle Card

### Vence quando…
- Você quer **só captions** num vídeo já editado
- Você precisa de uma **lib pip** ao invés de pipeline
- Você quer ler código didático de caption rendering

### Perde quando…
- Você precisa de qualquer outra capability além de captions
- Você precisa de manutenção (0 commits 365d)
- Você usa `openai>=1.0` (TypeError aberto sem fix)
- Você precisa de RTL ou idiomas exóticos

### Killer features
1. **3 minutos de setup** (`pip install captacity`)
2. **API minimalista** e clara (`add_captions()` com 12 kwargs)
3. **MIT** + pacote pip publicado

### Riscos
- **Abandonado** (0 commits 365d, issues sem resposta)
- Bug bloqueante com SDK OpenAI moderno
- Sem evolução para acompanhar Whisper / OpenAI changes

### Stack
Python + moviepy + pillow + openai (+ openai-whisper opcional).

---

## Decision Tree para Alan

```
Você quer substituir Submagic AGORA?
├── Sim → Clone OpenShorts. Setup 10-30 min. 4 keys (Gemini grátis, fal.ai/EL/UP pagas).
│
└── Não → Você quer faceless content factory?
        ├── Sim → Clone MoneyPrinterTurbo. Setup 30-90 min. ImageMagick + 2 keys.
        │
        └── Não → Você só precisa de captions em vídeos prontos?
                ├── Sim → `pip install captacity`. Mas saiba que está abandonado.
                │
                └── Não → Nenhum dos três. Considere outras opções (Auto-Editor, OpenAI Sora API, custom).
```

---

## Para fork como produto Sinkra

**Recomendado:** **OpenShorts** como base.

**Razão:**
- Greenfield (sem dívida técnica histórica)
- FastAPI + React (alinhado com stack Sinkra Hub)
- Modular (`saasshorts.py`, `editor.py`, `subtitles.py`, `thumbnail.py` separados)
- MIT, mantenedor ativo, zero CLA
- Já tem Remotion subdir → editor visual extensível

**Roadmap de hardening pós-fork (proposto):**
1. Swap fal.ai por providers mais baratos (Kling/Wan2/SVD) onde aplicável
2. PT-BR first-class nos prompts (script gen + hooks)
3. Catálogo curado de caption presets (5-10 styles)
4. Editor visual de timeline (extender Remotion)
5. Integração analytics (TikTok Display API + YT Data API)
6. Testes automatizados (pytest + golden frames)

---

## Comparação de "tempo até primeiro vídeo gerado"

| Repo | Setup | Configuração de keys | Primeiro vídeo |
|---|---|---|---|
| **OpenShorts** | 10 min | 5-15 min (4 keys) | **20-30 min total** |
| MoneyPrinterTurbo | 30-60 min | 5-15 min (2 keys) | 45-90 min total |
| Captacity | 1 min | 1 min | **5 min total** (mas só captions) |

---

## One-line Verdict

> **Clone OpenShorts primeiro. Mantenha MoneyPrinterTurbo bookmarkado para roubar o `app/services/llm.py` (multi-provider) caso vá fortalecer o fork. Ignore Captacity em produção.**
