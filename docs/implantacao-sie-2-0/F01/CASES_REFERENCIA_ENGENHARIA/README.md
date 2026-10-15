# F01 — Casos de referência de engenharia

O material atualmente existente cobre **somente triagem de aplicabilidade**, não cálculos elétricos homologados.

- `casos_escopo.json`: contexto por tipologia, UF, distribuidora e data, estado esperado, sem valores elétricos normativos.
- `restructuring/apps/api/tests/test_normative_f01.py`: valida HTTP 422 para campos de aprovação enviados pelo cliente, transição NR-10, triagem EDP e catálogo não verificado.
- `restructuring/apps/api/tests/test_legacy_golden.py`: F00 caracteriza 34 cenários do motor legado no SHA original, inclusive anomalias. **Não reutilizar os resultados herdados como valores esperados normativos.**

## Casos numéricos ainda bloqueados

| ID | Entradas e grandezas necessárias | Fórmula/seleção | Resultado de referência | Evidência |
|---|---|---|---|---|
| F01-NUM-COND | Ib [A], Iz [A], método, isolação, material, número de carregados, correção térmica/agrupamento | Por documentação primária/tabela adequada | PENDENTE | Origem, página, tabela, célula, notas, revisão técnica |
| F01-NUM-QT | I [A], comprimento [m], seção [mm²], Rca e XL [Ω/km], regime, cos(phi), temperatura | Por metodologia documentada aplicável | PENDENTE | Valores primários independentes; Rdc20 não substitui Rca |
| F01-NUM-EDP | Instalação, localidade, vigência, demanda e modalidade | Células e limites EDP pertinentes | PENDENTE | PDF oficial confirmado, tabela/coluna, dupla conferência |

**Gate:** nenhum teste com mock ou valor inventado altera `normative_conformity_verified=false`. Antes de liberar cálculo, a fixture numérica deve possuir fórmula, fonte, revisão, conferentes e resultado independente do próprio algoritmo.
