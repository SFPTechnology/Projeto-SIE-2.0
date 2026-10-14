# Quick Wins — Análise do Prompt NBR5410/EDP v2.0

## QW-01 — Fixtures de teste dos 5 casos explícitos

**Esforço:** XS | **Valor:** Alto | **Time-to-value:** < 1 dia  
**Target:** testes do SIE  
**Ação:** Implementar os Casos 1–5 da Seção 12 como testes unitários com fixtures fixas.  
**Referência:** §12 do prompt analisado

## QW-02 — Aviso de escopo na UI (SPDA e GD)

**Esforço:** XS | **Valor:** Médio | **Time-to-value:** < 1 dia  
**Target:** interface do SIE  
**Ação:** Adicionar mensagem de aviso explícita nos módulos onde SPDA e GD não são cobertos, prevenindo uso indevido.  
**Referência:** L-01 e L-02 do relatório

## QW-03 — Implementar regra de dimensionamento do condutor PE

**Esforço:** S | **Valor:** Alto | **Time-to-value:** < 3 dias  
**Target:** módulo de condutores do SIE  
**Ação:** Implementar tabela simplificada de seção mínima do PE (fase ≤ 16 → PE=fase; etc.) e exibir na memória de cálculo.  
**Referência:** I-07 do relatório

## QW-04 — Adicionar fórmula de queda de tensão bifásica

**Esforço:** S | **Valor:** Alto | **Time-to-value:** < 3 dias  
**Target:** módulo de queda de tensão do SIE  
**Ação:** Implementar e exibir fórmula de ΔV para circuito bifásico (FFN), diferenciando de monofásico e trifásico.  
**Referência:** I-02 do relatório
