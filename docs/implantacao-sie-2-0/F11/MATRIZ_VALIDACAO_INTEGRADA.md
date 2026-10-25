# F11 — matriz de validação integrada por motor

Base congelada para esta revisão: F10 `540f2c8e7e61a1efb6bf71abcedc8768d7086914`. Estados abaixo referem-se ao **recorte computacional**; nenhum `APROVADO` atesta projeto, instalação, norma integral ou concessionária.

| Motor / requisito | Evidência de software | Fonte e aplicabilidade | Computação | Homologação técnica |
|---|---|---|---|---|
| F01 — seleção Ib/In/Iz e queda simplificada, AC-11.02 | `tests/test_f01_independent_math_examples.py`; referência aritmética sintética independente | Oito células/seis casos de lote com aceite limitado; NBR integral não confirmada por estes ensaios | APROVADO no modelo declarado | PENDENTE |
| F06 — demanda EDP V09, AC-11.03 | `tests/test_demand_f06.py`, `tests/test_demand_binding_f06.py`; 118 passed nesta revisão | `F06/VINCULACAO_FONTES.md`, EDP V09 no contexto INDIVIDUAL; classificações/partidas explícitas | APROVADO no contexto vinculável | PENDENTE para projeto real/distribuidora |
| F07 — capacidade e queda AC por trecho, AC-11.02/03 | `tests/test_conductor_f07.py`, `tests/test_conductor_binding_f07.py`; resultados nas suites QA-02 | `F07/VINCULACAO_FONTES.md`; células F01 limitadas, Rca/XL e mínimos dependem de escopo/fonte declarados | APROVADO como estudo limitado com bloqueios | PENDENTE para catálogo completo e casos normativos |
| F08 — proteção e seletividade, AC-11.02/03 | `tests/test_protection_f08.py`, `tests/test_protection_independent_f08.py`; resultados nas suites QA-02 | `F08/FONTES.md`; produto/par finito e condições específicas; IT, T3, outros pares fora do modelo | APROVADO no catálogo restrito | PENDENTE para avaliação global |
| F09 — diagnóstico da concessionária, AC-11.03/04 | `docs/implantacao-sie-2-0/F09/`, testes F09 existentes; não reexecutados nesta revisão QA-02 | Evidências F06–F08 por IDs/hashes, análise consultiva; aceite de itens 1/2 no escopo | NÃO VERIFICADO nesta revisão | PENDENTE |
| F10 — representação e memorial/PDF, AC-11.04/08 | `tests/test_full_f10_integration.py`; run por circuito, dois quadros, snapshot e exportação | Simbologia esquemática interna, importação SVG limitada; cálculo legado com limites explícitos | APROVADO no cenário executado | PENDENTE para projeto/obra reais |

**Não verificado por esta matriz:** cobertura integral de ACs do release, ensaios físicos, autorização profissional, fontes para cenários fora do catálogo, browser/segurança/desempenho e CI F11. Os demais QA e o relatório consolidado governam esses gates.
