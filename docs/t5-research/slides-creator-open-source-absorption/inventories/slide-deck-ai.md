# Inventory — slide-deck-ai

## Identidade

- **Repo:** `barun-saha/slide-deck-ai`
- **Clone local:** `../bench/slide-deck-ai`
- **Licença:** MIT
- **Prioridade:** P2
- **Papel na stack:** baseline simples para CLI/API Python, provider abstraction e python-pptx.

## Evidência Lida

- `../bench/slide-deck-ai/README.md`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| Python API | Quickstart simples para geração. |
| CLI/Streamlit | Bom para smoke tests e prototipagem. |
| LiteLLM | Provider abstraction. |
| Ollama | Modo offline/local documentado. |
| python-pptx | Simples e conhecido para geração básica. |

## Limitações

- Não chega ao nível de editabilidade/visual fidelity de `ppt-master`.
- Menos profundo em narrativa, UX e agentic planning.
- Melhor como referência de simplicidade do que como base final.

## O Que Absorver

1. CLI mínima para smoke tests.
2. Provider abstraction via LiteLLM ou equivalente.
3. Modo offline explícito com Ollama.

## Critério de Aceite

- Um comando local gera deck básico sem UI.
- Provider local pode ser usado em CI/smoke test.
- Não vira renderer principal.
