# Repo Metrics — Clones Open-Source

Métricas coletadas localmente em 2026-05-17 a partir dos clones em `../bench/`, ignorando `.git`, `node_modules`, `.next`, `dist`, `build` e `__pycache__`.

| Projeto | Arquivos | Principais extensões | Arquivos raiz relevantes | Leitura |
|---|---:|---|---|---|
| `ppt-master` | 13.196 | `.svg` 12.447, `.md` 319, `.png` 235, `.py` 105, `.pptx` 23 | `requirements.txt`, `README.md`, `LICENSE` | Grande volume de exemplos/assets. Forte em renderer, templates e documentação. |
| `banana-slides` | 472 | `.py` 181, `.ts` 91, `.tsx` 54, `.mdx` 30, `.md` 19 | `package.json`, `pyproject.toml`, `docker-compose.yml`, `README.md`, `LICENSE` | Stack full app com backend/frontend e UX forte. Risco AGPL. |
| Presenton | 2.343 | `.svg` 1.525, `.tsx` 366, `.py` 188, `.ts` 120, `.json` 33 | `package.json`, `docker-compose.yml`, `README.md`, `LICENSE` | Produto mais completo para API/app/self-hosted. |
| PPTAgent | 218 | `.py` 71, `.jpg` 53, `.txt` 21, `.json` 16, `.yaml` 14 | `pyproject.toml`, `docker-compose.yml`, `README.md`, `LICENSE` | Framework agentic mais relevante para planning/reflection. |
| presentation-ai | 878 | `.tsx` 662, `.ts` 190, `.json` 7, `.woff` 3, `.css` 3 | `package.json`, `README.md`, `LICENSE` | Editor web rico com outline-first e temas. |
| slide-deck-ai | 439 | `.png` 319, `.rst` 52, `.py` 27, `.json` 7, `.pptx` 5 | `pyproject.toml`, `requirements.txt`, `README.md`, `LICENSE` | Baseline Python/CLI simples. |
| powerpoint-skill | 19 | `.md` 6, `.py` 6, `.json` 2, `.js` 1, `.pptx` 1 | `README.md`, `LICENSE` | Pequeno, mas denso para math/diagramas/hard rules. |
| PresentAgent-2 | 626 | `.py` 285, `.png` 98, `.txt` 42, `.jpg` 35, `.md` 27 | `requirements.txt`, `README.md` | Pesado em pesquisa/multimodal/vídeo. Licença precisa confirmação. |

## Implicações

- `ppt-master` tem massa de assets/exemplos muito maior que o restante; a absorção deve focar arquitetura e scripts centrais, não copiar volume bruto.
- Presenton e banana-slides são os únicos com aparência clara de produto full-stack entre os principais analisados.
- presentation-ai é a melhor referência de editor React/Next.js.
- powerpoint-skill é pequeno o suficiente para virar checklist técnico quase diretamente.
- PresentAgent-2 é mais pesquisa/protótipo avançado do que MVP.
