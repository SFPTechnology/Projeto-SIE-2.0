# Scorecard — OpenShorts × MoneyPrinterTurbo × Captacity

**Escala:** 0-100 por dimensão.
**Método:** rubric direta com referência ao Submagic Pro como ceiling (≈85-95) em features comparáveis.
**Composite:** média aritmética simples + duas variantes persona-weighted.

---

## Tabela Bruta — 7 Dimensões

| Dimensão | OpenShorts | MoneyPrinterTurbo | Captacity | Justificativa |
|---|---:|---:|---:|---|
| **Features (proximidade Submagic)** | **88** | 52 | 18 | OpenShorts é único com viral detection + B-roll AI + reframe + publish; MPT cobre só geração faceless; Captacity só captions |
| **Maintenance & Activity (90d)** | **90** | 82 | 5 | OpenShorts: 39 commits/90d em repo de 5 meses + 9 commits/dia 2026-05-06; MPT: 48 commits/90d + release v1.2.7 cadenciada; Captacity: 0 commits 365d |
| **DX & Setup Effort** | 78 | 58 | **92** | Captacity: `pip install` em 3 min; OpenShorts: `docker compose up`; MPT: ImageMagick + uv + 2 keys (fricção real Windows) |
| **Output Quality (Submagic-like)** | **82** | 60 | 70 | OpenShorts: AI B-roll + word-level subs + AI effects; MPT: stock Pexels (visualmente repetitivo); Captacity: caption quality high mas só captions |
| **Customization (extensibilidade do código)** | **80** | **80** | 65 | OpenShorts: FastAPI+React modular, Remotion subdir; MPT: MVC limpo, 13 LLM providers swappable; Captacity: lib pequena, fácil hack mas escopo trivial |
| **Documentation** | **85** | 78 | 60 | OpenShorts: README extensivo com comparativo competitivo; MPT: PT-CN + EN + Colab + tutoriais Douyin; Captacity: README curto, sem changelog atualizado |
| **License Permissiveness** | **100** | **100** | **100** | Todos MIT, sem CLA, uso comercial OK |

---

## Composite — Média Simples

| Repo | Composite (média 7 dims) |
|---|---:|
| **OpenShorts** | **(88+90+78+82+80+85+100)/7 = 86,1** |
| **MoneyPrinterTurbo** | (52+82+58+60+80+78+100)/7 = **72,9** |
| **Captacity** | (18+5+92+70+65+60+100)/7 = **58,6** |

---

## Persona A — "Solo creator, daily use" (substituir Submagic já)

**Pesos:**
- Features: 0,30
- Maintenance: 0,15
- DX/Setup: 0,20
- Output Quality: 0,20
- Customization: 0,05
- Documentation: 0,05
- License: 0,05

| Repo | Cálculo | Score |
|---|---|---:|
| **OpenShorts** | 88·0,30 + 90·0,15 + 78·0,20 + 82·0,20 + 80·0,05 + 85·0,05 + 100·0,05 = 26,4+13,5+15,6+16,4+4,0+4,25+5,0 | **85,2** |
| MoneyPrinterTurbo | 52·0,30 + 82·0,15 + 58·0,20 + 60·0,20 + 80·0,05 + 78·0,05 + 100·0,05 = 15,6+12,3+11,6+12,0+4,0+3,9+5,0 | **64,4** |
| Captacity | 18·0,30 + 5·0,15 + 92·0,20 + 70·0,20 + 65·0,05 + 60·0,05 + 100·0,05 = 5,4+0,75+18,4+14,0+3,25+3,0+5,0 | **49,8** |

**Veredicto persona A:** OpenShorts vence por ampla margem (≈21 pts). Captacity é descartado pelo abandono e escopo.

---

## Persona B — "Developer fork target" (base para produto Sinkra)

**Pesos:**
- Features: 0,15
- Maintenance: 0,20
- DX/Setup: 0,10
- Output Quality: 0,10
- Customization: 0,25
- Documentation: 0,15
- License: 0,05

| Repo | Cálculo | Score |
|---|---|---:|
| **OpenShorts** | 88·0,15 + 90·0,20 + 78·0,10 + 82·0,10 + 80·0,25 + 85·0,15 + 100·0,05 = 13,2+18,0+7,8+8,2+20,0+12,75+5,0 | **85,0** |
| MoneyPrinterTurbo | 52·0,15 + 82·0,20 + 58·0,10 + 60·0,10 + 80·0,25 + 78·0,15 + 100·0,05 = 7,8+16,4+5,8+6,0+20,0+11,7+5,0 | **72,7** |
| Captacity | 18·0,15 + 5·0,20 + 92·0,10 + 70·0,10 + 65·0,25 + 60·0,15 + 100·0,05 = 2,7+1,0+9,2+7,0+16,25+9,0+5,0 | **50,2** |

**Veredicto persona B:** OpenShorts ainda lidera (~12 pts), com MPT como fallback respeitável (codebase MVC sólida, 13 providers LLM, comunidade enorme).

---

## Heatmap (visualização por dimensão)

```
                          OpenShorts  MPT   Captacity
Features                      ████   ██▌    ▎
Maintenance                   ████▌  ████   ▏
DX/Setup                      ███▌   ██▌    █████
Output Quality                ████   ███    ███▌
Customization                 ████   ████   ███▎
Documentation                 ████   ███▌   ███
License                       █████  █████  █████
```

---

## Conclusão Quantitativa

1. **OpenShorts vence ambas as personas** (85,2 solo / 85,0 dev fork). Único score 85+ no bench.
2. **MoneyPrinterTurbo** é segundo confortável em ambas (64,4 / 72,7). É a opção de fork se Alan quiser ecossistema chinês de stock-based generation; **não é** Submagic substitute para podcast clipping.
3. **Captacity** abaixo do threshold de adoção (49,8 / 50,2). Use apenas como referência de código.
