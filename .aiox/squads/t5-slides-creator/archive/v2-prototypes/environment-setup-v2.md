# Environment Setup -- slides-creator v2

Guia completo para configurar o ambiente de desenvolvimento do slides-creator v2, incluindo os 4 upgrades: Auto Illustration Pipeline, Visual Rendering Tools, Andragogic Slide Design System e YouTube to Presentation Pipeline.

---

## Pre-requisitos

### Sistema Operacional

| Requisito | Versao Minima | Verificacao |
|-----------|---------------|-------------|
| macOS / Linux | macOS 13+ ou Ubuntu 22.04+ | `uname -a` |
| Node.js | >= 18.0.0 | `node --version` |
| npm | >= 9.0.0 | `npm --version` |
| Python | >= 3.10 | `python3 --version` |
| Docker | >= 24.0 | `docker --version` |
| Docker Compose | >= 2.20 | `docker compose version` |
| Git | >= 2.40 | `git --version` |

### CLI Tools

| Ferramenta | Instalacao | Verificacao | Usado por |
|------------|------------|-------------|-----------|
| D2 | `brew install d2` | `d2 --version` (>= 0.6) | Upgrade 1, 2 -- geracao de diagramas |
| Cairo (nativo) | `brew install cairo pango gdk-pixbuf libffi` | `python3 -c "import cairosvg"` | Upgrade 2 -- conversao SVG -> PNG |
| FFmpeg | `brew install ffmpeg` | `ffmpeg -version` | Upgrade 4 -- processamento de video |

---

## Instalacao

### 1. Dependencias Node.js

```bash
npm install
```

### 2. Dependencias Python

```bash
pip install python-pptx cairosvg PySceneDetect[opencv] plotly kaleido EasyPPTX
```

### 3. Cairo e bibliotecas nativas (macOS)

```bash
brew install cairo pango gdk-pixbuf libffi
```

Verificar instalacao:

```bash
python3 -c "import cairosvg; print('cairosvg OK')"
```

### 4. D2 CLI

```bash
brew install d2
d2 --version  # deve retornar >= 0.6
```

Teste rapido:

```bash
echo 'x -> y -> z' | d2 - test-output.svg
```

---

## Kroki Docker Setup

Kroki e o servidor de rendering de diagramas (Mermaid, D2 via API, PlantUML, etc.).

### docker-compose.slides-v2.yml

```yaml
services:
  kroki:
    image: yuzutech/kroki
    ports:
      - "8000:8000"
    environment:
      - KROKI_MERMAID_HOST=mermaid
    mem_limit: 512m
    depends_on:
      - mermaid

  mermaid:
    image: yuzutech/kroki-mermaid
    mem_limit: 256m
    expose:
      - "8002"
```

### Iniciar Kroki

```bash
docker compose -f docker-compose.slides-v2.yml up -d
```

### Verificar Health

```bash
curl http://localhost:8000/health
# Deve retornar: 200 OK
```

### Parar Kroki (quando nao estiver em uso)

```bash
docker compose -f docker-compose.slides-v2.yml down
```

**Nota:** Kroki e on-demand. Iniciar apenas quando for gerar diagramas via API. D2 CLI local e preferido para renders simples.

---

## Variaveis de Ambiente

8 novas variaveis adicionadas ao `.env.example` para v2:

| Variavel | Descricao | Valor Default | Upgrade |
|----------|-----------|---------------|---------|
| `RECRAFT_API_KEY` | API key para Recraft (geracao de imagens) | (obrigatorio se visual gen ativo) | 1, 2 |
| `KROKI_URL` | URL do servidor Kroki | `http://localhost:8000` | 2 |
| `SLIDES_COST_CAP` | Custo maximo por deck em USD | `2.00` | 1, 2 |
| `SLIDES_VIDEO_COST_CAP` | Custo maximo por video->deck em USD | `5.00` | 4 |
| `SLIDES_CACHE_DIR` | Diretorio base para cache v2 | `cache/slides-v2` | 1, 2, 4 |
| `ENABLE_VISUAL_GENERATION` | Feature flag: Auto Illustration Pipeline | `false` | 1, 2 |
| `ENABLE_ANDRAGOGIC_VALIDATION` | Feature flag: Andragogic Design System | `false` | 3 |
| `ENABLE_YOUTUBE_ENTRYPOINT` | Feature flag: YouTube to Presentation | `false` | 4 |

### Configurar

Copiar as variaveis para o `.env`:

```bash
# slides-creator v2
RECRAFT_API_KEY=your_key_here
KROKI_URL=http://localhost:8000
SLIDES_COST_CAP=2.00
SLIDES_VIDEO_COST_CAP=5.00
SLIDES_CACHE_DIR=cache/slides-v2
ENABLE_VISUAL_GENERATION=false
ENABLE_ANDRAGOGIC_VALIDATION=false
ENABLE_YOUTUBE_ENTRYPOINT=false
```

### Feature Flags

Cada upgrade pode ser ativado/desativado independentemente:

| Flag | Upgrade | Efeito quando `false` |
|------|---------|-----------------------|
| `ENABLE_VISUAL_GENERATION` | 1 + 2 (Auto Illustration + Visual Rendering) | Pipeline v1 intacta, sem geracao de visuais |
| `ENABLE_ANDRAGOGIC_VALIDATION` | 3 (Andragogic Design System) | QA scoring usa pesos v1, sem dimensao andragogy |
| `ENABLE_YOUTUBE_ENTRYPOINT` | 4 (YouTube Pipeline) | Input type youtube_url nao disponivel |

---

## Diretorios de Cache

Criar os diretorios de cache antes da primeira execucao:

```bash
mkdir -p cache/slides-v2/{diagrams,images,videos}
```

| Diretorio | Conteudo | TTL |
|-----------|----------|-----|
| `cache/slides-v2/diagrams` | SVG/PNG de diagramas D2/Mermaid | Indefinido (key = SHA-256 do codigo + theme) |
| `cache/slides-v2/images` | Imagens geradas por AI (GPT Image, Recraft) | 30 dias |
| `cache/slides-v2/videos` | Transcricoes e keyframes de video | 7 dias |

---

## Verificacao

### health-check-v2.sh

Script de verificacao completa do ambiente:

```bash
#!/bin/bash
echo "=== slides-creator v2 Health Check ==="

# D2
echo -n "D2 CLI: "
d2 --version 2>/dev/null && echo "OK" || echo "FAIL -- brew install d2"

# Kroki
echo -n "Kroki: "
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q 200 && echo "OK" || echo "FAIL -- docker compose up"

# cairosvg
echo -n "cairosvg: "
python3 -c "import cairosvg; print('OK')" 2>/dev/null || echo "FAIL -- pip install cairosvg + brew install cairo"

# Python deps
echo -n "Python deps: "
python3 -c "import pptx, cairosvg, plotly; print('OK')" 2>/dev/null || echo "FAIL -- pip install python-pptx cairosvg plotly kaleido"

# Cache dirs
echo -n "Cache dirs: "
[ -d "cache/slides-v2/diagrams" ] && [ -d "cache/slides-v2/images" ] && [ -d "cache/slides-v2/videos" ] && echo "OK" || echo "FAIL -- mkdir -p cache/slides-v2/{diagrams,images,videos}"

# Env vars
echo -n "Env vars: "
if [ -f .env ]; then
  MISSING=""
  for var in RECRAFT_API_KEY KROKI_URL SLIDES_COST_CAP SLIDES_VIDEO_COST_CAP SLIDES_CACHE_DIR ENABLE_VISUAL_GENERATION ENABLE_ANDRAGOGIC_VALIDATION ENABLE_YOUTUBE_ENTRYPOINT; do
    grep -q "^${var}=" .env || MISSING="${MISSING} ${var}"
  done
  [ -z "$MISSING" ] && echo "OK" || echo "MISSING:${MISSING}"
else
  echo "FAIL -- .env not found"
fi

echo "=== Done ==="
```

### test-renders-v2.sh

Script de teste de rendering:

```bash
#!/bin/bash
echo "=== slides-creator v2 Render Tests ==="

TMPDIR=$(mktemp -d)

# Test 1: D2 -> SVG
echo -n "D2 -> SVG: "
echo 'a -> b -> c' | d2 - "${TMPDIR}/test-d2.svg" 2>/dev/null && echo "OK" || echo "FAIL"

# Test 2: D2 -> SVG with theme overrides
echo -n "D2 themed: "
echo 'x -> y' | d2 --theme-overrides='N1:#FF6B6B,B1:#4ECDC4' - "${TMPDIR}/test-d2-themed.svg" 2>/dev/null && echo "OK" || echo "FAIL"

# Test 3: SVG -> PNG via cairosvg
echo -n "SVG -> PNG: "
if [ -f "${TMPDIR}/test-d2.svg" ]; then
  python3 -c "
import cairosvg
cairosvg.svg2png(url='${TMPDIR}/test-d2.svg', write_to='${TMPDIR}/test-d2.png', dpi=300)
print('OK')
" 2>/dev/null || echo "FAIL"
else
  echo "SKIP (no SVG from test 1)"
fi

# Test 4: Mermaid via Kroki
echo -n "Mermaid via Kroki: "
curl -s -o "${TMPDIR}/test-mermaid.svg" \
  -H "Content-Type: text/plain" \
  -d 'graph LR; A-->B; B-->C;' \
  "http://localhost:8000/mermaid/svg" 2>/dev/null && \
  [ -s "${TMPDIR}/test-mermaid.svg" ] && echo "OK" || echo "FAIL (Kroki running?)"

# Test 5: Plotly static
echo -n "Plotly static: "
python3 -c "
import plotly.graph_objects as go
fig = go.Figure(data=[go.Bar(x=['A','B','C'], y=[1,2,3])])
fig.write_image('${TMPDIR}/test-plotly.png')
print('OK')
" 2>/dev/null || echo "FAIL"

# Cleanup
rm -rf "${TMPDIR}"

echo "=== Done ==="
```

---

## Troubleshooting

### D2 nao encontrado

```
d2: command not found
```

**Solucao:** `brew install d2` e reiniciar o terminal.

### cairosvg falha ao importar

```
ModuleNotFoundError: No module named 'cairosvg'
```

**Solucao:**

1. Instalar bibliotecas nativas: `brew install cairo pango gdk-pixbuf libffi`
2. Instalar pacote Python: `pip install cairosvg`
3. Se ainda falhar, verificar que o Python esta usando o brew-installed cairo: `pkg-config --libs cairo`

### Kroki retorna connection refused

```
curl: (7) Failed to connect to localhost port 8000
```

**Solucao:** Iniciar os containers:

```bash
docker compose -f docker-compose.slides-v2.yml up -d
docker compose -f docker-compose.slides-v2.yml logs kroki  # verificar logs
```

### Kroki retorna 503 para Mermaid

```
503 Service Unavailable
```

**Solucao:** O container `mermaid` pode nao ter inicializado ainda. Aguardar 10-15 segundos apos `docker compose up` e tentar novamente. Se persistir:

```bash
docker compose -f docker-compose.slides-v2.yml restart mermaid
```

### Plotly/Kaleido falha ao exportar imagem

```
ValueError: Image export requires the kaleido package
```

**Solucao:** `pip install kaleido`

### FFmpeg nao encontrado (YouTube Pipeline)

```
ffmpeg: command not found
```

**Solucao:** `brew install ffmpeg`

### Memoria insuficiente com Kroki + processamento de video

**Sintoma:** Containers reiniciando, processamento lento.

**Solucao:** Nao rodar Kroki e video processing simultaneamente. O `mem_limit` dos containers esta configurado para 512m (Kroki) + 256m (Mermaid). Se necessario, parar Kroki durante processamento de video:

```bash
docker compose -f docker-compose.slides-v2.yml down
# processar video
docker compose -f docker-compose.slides-v2.yml up -d
# gerar diagramas
```

### Cache corrompido

**Sintoma:** Renders desatualizados ou quebrados.

**Solucao:** Limpar o cache afetado:

```bash
rm -rf cache/slides-v2/diagrams/*  # diagramas
rm -rf cache/slides-v2/images/*    # imagens AI
rm -rf cache/slides-v2/videos/*    # transcricoes/keyframes
```

---

## Proximos Passos

1. Executar `health-check-v2.sh` para validar o ambiente
2. Executar `test-renders-v2.sh` para validar rendering
3. Ativar feature flags uma a uma conforme necessidade
4. Consultar `README.md` do squad para visao geral dos upgrades

---

_Versao: v2.0.0 -- compativel com slides-creator v9.0.0_
