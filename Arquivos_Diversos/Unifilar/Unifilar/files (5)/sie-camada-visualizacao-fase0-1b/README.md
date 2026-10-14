# SIE — Camada de Visualização · Implementação Fase 0 + Fase 1b

Implementação conforme **PRD — Camada de Visualização v1.0 (Julho 2026)**.
Escopo entregue: **Fase 0** (Contrato de Circuito Canônico + Adaptador 1:1) e
**Fase 1b — Unifilar Hero (Camada B)** com exportação DXF.

## Estrutura

```
sie_visualizacao/
├── backend/
│   ├── contrato_circuito.py    # Seção 5 — schema Pydantic v2 canônico
│   ├── adaptador_1x1.py        # Fase 0 — ponto→circuito provisório (R-04)
│   ├── router_visualizacao.py  # Seção 2.2 — GET /api/v1/projetos/{id}/visualizacao
│   └── export_dxf.py           # 4.1/UF-05 — ezdxf R2010, BLK_*, layers SIE_*
├── frontend/
│   ├── simbolos_iec.tsx        # DT-03 — biblioteca IEC 60617 (espelho dos BLK_*)
│   └── UnifilarHero.tsx        # 4.1 — layout DT-02, click-to-trace, WCAG AA
└── tests/
    └── test_fase0_unifilar.py  # T1–T6 (6/6 passando)
```

## Decisões do operador incorporadas (08/07/2026 — ver ANEXO-A do roteiro)

- **CONF-01:** convenção oficial de fases é **R/S/T**; o loader converte a coluna
  legada A/B/C com `mapear_fase_abc_para_rst` (adaptador_1x1.py).
- **CONF-02:** o id do circuito é o **id real do banco** (`ILUM-*`, `TUG-*`, `ADD-*`) —
  o adaptador não gera ids.
- **CONF-03:** ILU/TUG com tensão resolvida pela Saída A entram com 127 V e
  `fonte_linha` rastreável (`tensao_resolvida_por_contrato=True` no PontoCarga);
  TUE/outra sem `tensaoFixa` => `None` + ATENÇÃO. O adaptador rejeita TUE marcada
  como resolvida por contrato (guarda INC-04). Suíte agora com 10 testes (T1–T10).

## Integração no backend do SIE

```python
from sie_visualizacao.backend.router_visualizacao import router, registrar_repositorio

app.include_router(router)
registrar_repositorio(carregar_pontos_do_projeto)  # sua função SQLAlchemy → list[PontoCarga]
```

O loader deve mapear cada ponto do módulo IB para `PontoCarga`. Regras:
- `va` = valor VA armazenado, direto (INC-01) — nunca dividir por FP.
- `tensao_v=None` quando não declarada (INC-04) — o adaptador propaga
  `[VERIFICAR]` + `ATENÇÃO`; jamais 127V implícito.
- `corrente_ib_a` = IB já calculado pelo módulo IB (a visualização não recalcula).
- `zona_molhada=None` quando a dependência não tem classificação (INC-03).

## Integração no frontend (React + Carbon)

```tsx
import UnifilarHero from "./sie_visualizacao/frontend/UnifilarHero";

const { data } = useQuery(["viz", id], () =>
  fetch(`/api/v1/projetos/${id}/visualizacao`).then(r => r.json()));

<UnifilarHero
  circuitos={data.circuitos}
  provisorio={data.provisorio}
  onTrace={(c) => abrirMemorial(c)}  // painel/modal Carbon com c.derivacao
/>
```

Cores via tokens CSS do Carbon (`--cds-*`) com fallback g10 — RNF-04.

## Exportação DXF (UF-05)

```python
from sie_visualizacao.backend.export_dxf import exportar_unifilar_dxf
exportar_unifilar_dxf(circuitos, "unifilar-proj-1.dxf", projeto_id="proj-1")
```

DXF R2010 (AC1024, mitigação R-05); blocos `BLK_MEDIDOR`, `BLK_DISJUNTOR`,
`BLK_DR`, `BLK_ILU`, `BLK_TUG`, `BLK_TUE`, `BLK_BARR`, `BLK_MOTOR`; layers
`SIE_RAMAL/MEDICAO/PROTECAO/DR/CARGAS/CONDUTORES/ANOTACOES/PENDENCIAS`.

SVG → PDF (server-side Puppeteer/Playwright) **não** foi incluído — depende de
infraestrutura Node no servidor do SIE; o SVG do `UnifilarHero` é o insumo direto.

## Critérios de aceite — estado

| Critério | Estado | Como verificar |
|---|---|---|
| UF-01 | ✅ | Demo com 44 circuitos, ROW_H fixo — sem sobreposição |
| UF-02 | ✅ | `tensao_v=null` → tracejado + badge ATENÇÃO (demo: Churrasqueira) |
| UF-03 | ✅ | Clique/Enter → memorial com `IB = S/V` + ref. NBR 5410 §6.2.7 |
| UF-04 | ✅ (dados) | T4: mesma entrada → JSON idêntico; SVG sem fontes de não-determinismo |
| UF-05 | ✅ | T6: DXF R2010 com layers e blocos BLK_* (validar em AutoCAD real) |
| UF-06 | ✅ | role=button, aria-label, Tab + Enter/Espaço, foco visível |

`[VERIFICAR]` pendentes: cláusula NBR exata para IB (usei §6.2.7 como
placeholder rastreável em `SIE-IB-01` — confirme contra o texto da norma);
geometria fina dos símbolos IEC 60617 contra as folhas oficiais da norma.

## Fora de escopo (Seção 9 do PRD — NÃO TOCADO)

Módulos de cálculo, Divisão de Circuitos, P1/proteção, motor de geometria,
relatório final, Camada A (Fable 5 — produto externo, exige POC de embed R-01),
Trifilar do Padrão de Entrada (4.2), Multifilar (4.3), Planta (4.4).
