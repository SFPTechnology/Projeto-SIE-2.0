# Inventory — Captacity

**Repo:** https://github.com/unconv/captacity
**Tagline:** *"Add Automatic Captions to YouTube Shorts with AI."*

## Identidade & Atividade

| Atributo | Valor | Fonte |
|---|---|---|
| Stars | 135 | [GitHub API](https://api.github.com/repos/unconv/captacity) |
| Forks | 40 | idem |
| Issues abertas | 9 | idem |
| Linguagem | Python | idem |
| Licença | MIT | idem |
| Criado em | 2024-03-04 | idem |
| Último commit | **2024-06-07** | [commits](https://github.com/unconv/captacity/commits/master) |
| Commits últimos 365d | **0** | API |
| Default branch | `master` | API |
| Versão pip | `0.3.1` | [setup.py](https://github.com/unconv/captacity/blob/master/setup.py) |
| Tamanho do repo | 171 KB | API |

**Sinal de atividade:** **DORMENTE.** Sem commits desde junho/2024 (~23 meses). Issues abertas relatam bugs reais (TypeError em TranscriptionWord, áudio incompatível com iOS, falta de RTL/multi-language) sem resposta do mantenedor.

**Categoria:** Biblioteca de uma capability (captions only). Não é pipeline.

## Stack & Dependências

```txt
moviepy
pillow
openai
```

**Extras:** `pip install captacity[local_whisper]` instala `openai-whisper` para transcrição local (default = OpenAI API).

**Estrutura `captacity/`:**
- `__init__.py` — `add_captions()` API
- `cli.py` — entry point `captacity <input> <output>`
- `segment_parser.py`
- `text_drawer.py`
- `transcriber.py`
- `assets/` — fontes default

Fonte: [requirements.txt](https://github.com/unconv/captacity/blob/master/requirements.txt) + [README](https://github.com/unconv/captacity/blob/master/README.md).

## Features (declaradas no README)

API minimalista e focada:

```python
captacity.add_captions(
    video_file="my_short.mp4",
    output_file="my_short_with_captions.mp4",
    font="/path/to/font.ttf",
    font_size=130,
    font_color="yellow",
    stroke_width=3,
    stroke_color="black",
    shadow_strength=1.0,
    shadow_blur=0.1,
    highlight_current_word=True,
    word_highlight_color="red",
    line_count=1,
    padding=50,
)
```

**Capabilities:**
- Whisper local (opcional) ou Whisper API (default)
- **Word-level highlighting** (palavra ativa colorida)
- Stroke/shadow customizável
- Multi-line vs single-line
- Padding configurável
- CLI: `captacity input.mp4 output.mp4`

**O que NÃO faz:**
- Não detecta highlights / viral moments
- Não corta vídeo
- Não gera B-roll
- Não publica em redes
- Não reframe 9:16
- Não TTS, não LLM, não scripting

## Setup Effort

```
pip install captacity
captacity input.mp4 output.mp4
```

**Setup:** **3 minutos.** Mais simples do bench, by far.

**Friction points:**
- Precisa OpenAI API key (a menos que use `[local_whisper]`)
- moviepy traz ImageMagick implícito em alguns paths
- Bug TypeError em versões recentes do `openai` SDK ([issue #aberto](https://github.com/unconv/captacity/issues), criado 2025-04-14)

## Sinais de saúde do projeto

- 0 commits em 365 dias
- 9 issues abertas, várias com bugs concretos sem fix
- 135 stars, 40 forks → nicho mas com tração inicial perdida
- Sem releases recentes (último pip = `0.3.1` em 2024-06)

## Watermark / Render / Output

- **Watermark:** Nenhum
- **Render:** moviepy
- **Output:** MP4 com captions burned

## Equivalência funcional vs Submagic

| Submagic feature | Captacity? |
|---|---|
| Auto-captions animadas | Sim — word-highlight, stroke, shadow |
| B-roll automático | **Não** |
| Highlight clipping de podcast | **Não** |
| 9:16 smart reframe | **Não** |
| Hook overlays | **Não** |
| Multi-platform publish | **Não** |
| AI Avatar / UGC | **Não** |

**Veredicto categoria:** Captacity ≠ pipeline. É **um componente** de uma camada (captions). Pode ser plugado num pipeline próprio mas não substitui Submagic.

## Riscos

- **Sem manutenção:** bugs novos não vão receber fix
- **Single-maintainer abandonado:** "Unconventional Coding" (canal YouTube) parece ter movido foco
- **Incompatibilidade futura:** `openai>=1.0` mudou API → captacity ainda não foi atualizada
- **Falta multi-idioma RTL:** issue aberta de 2025-01 sem progresso

## Quando ainda faz sentido usar

- **Inspiração de código** para implementar caption-renderer próprio (text_drawer.py é didático)
- **Fork e modernizar** se o objetivo é ter uma lib pip simples só de captions
- **Não use em produção sem fork ativo**
