# QA — Resultado da Verificação: P-KVVA
## Corrigir rótulo de unidade kW → kVA na carga instalada

**Agente:** Quinn (QA Guardian)
**Data:** 2026-07-01
**Branch:** `feature/nbr5410-conformidade-closeout`
**Arquivos auditados:**
- `src/components/app/edp-sp/CategoriaSubcategoriaCard.tsx`
- `src/components/app/edp-sp/DemandaPorGrupoEDPCard.tsx`
- `src/domain/distribuidora/edp-sp/validacao.ts`

**Prompt de origem:** `C:\Users\User\Downloads\P-KVVA_Corrigir_Rotulo_Unidade_kVA.md`

---

## Decisão do Gate

| Resultado | Veredicto |
|-----------|-----------|
| **GATE DECISION** | ✅ **PASS** |
| Critérios PASS | 9 / 10 |
| Critérios PARCIAL (fora de escopo, documentado) | 1 / 10 |
| Critérios FAIL | 0 / 10 |
| Regressão de testes | ✅ 129/129 passaram |

> Nenhum critério bloqueante falhou. O rótulo da carga instalada foi corrigido em todas as ocorrências user-facing. A única ressalva (CA-06) é um item explicitamente marcado como fora de escopo pelo próprio documento de origem (seção 8) — não é uma falha de implementação.

---

## Análise por Critério de Aceitação

### CA-01 — Rótulo "kVA" no card "Categoria e sub-categoria" (tela Padrão de entrada)

**Status: ✅ PASS**

**Evidência de código** (`CategoriaSubcategoriaCard.tsx:79`):
```tsx
{resultado.carga_instalada_kW.toFixed(2)} <span ...>kVA</span>
```

Antes: `... kW`. O valor numérico (`.toFixed(2)`) não foi alterado — apenas o sufixo textual.

---

### CA-02 — Mensagem de erro "sem-categoria" (carga > 75) usa kVA para a carga instalada

**Status: ✅ PASS**

**Evidência de código** (`CategoriaSubcategoriaCard.tsx:50`):
```tsx
title={`Carga instalada ${resultado.carga_instalada_kW.toFixed(2)} kVA excede 75 kW`}
```

O primeiro termo (grandeza medida) virou `kVA`; o limite `75 kW` foi mantido intocado por pertencer à tabela de categoria/limite de média tensão (fora de escopo — ver CA-06).

---

### CA-03 — Tag "Carga instalada" no drill-down por grupo (DemandaPorGrupoEDPCard)

**Status: ✅ PASS**

**Evidência de código** (`DemandaPorGrupoEDPCard.tsx:329`):
```tsx
Carga instalada: <strong>{d.carga_instalada_kW.toFixed(2)} kVA</strong>
```

---

### CA-04 — Diagnósticos de validação (`validacao.ts`) referenciam a carga instalada em kVA

**Status: ✅ PASS**

Três mensagens de diagnóstico corrigidas:

| Código | Linha | Trecho corrigido |
|--------|-------|-------------------|
| `ERR-CARGA-INSTALADA-ACIMA-75KW` | 224 | `Carga instalada ${...} kVA excede 75 kW` |
| `ATN-FRONTEIRA-CATEGORIA` | 396 | `Carga instalada ${...} kVA está a ${delta} kW da fronteira` |
| `ATN-TRIFASICA-FORCOU-CATEGORIA-T` | 423 | `(${...} kVA) sozinha a categoria seria ${hipotetica}` |

Em `ATN-FRONTEIRA-CATEGORIA` o `delta` (distância até a fronteira da faixa) permanece em "kW" — coerente com CA-06, pois é uma grandeza derivada da faixa de categoria, não da carga instalada em si.

---

### CA-05 — Nenhuma mudança no valor numérico 53,60 (ou qualquer outro) — apenas a unidade

**Status: ✅ PASS**

Nenhuma edição tocou em `carga_instalada_kW`, na soma de cargas (`motor-demanda.ts`), ou em qualquer fórmula. Confirmado por:
- Diff revisado manualmente — apenas literais de string (`"kW"` → `"kVA"`) foram alterados.
- Suíte de testes de domínio (`motor-demanda`, `motor-edp-sp`, `validacao`, `seletor-categoria`, `categorias-fornecimento`) sem alterações e 100% passando.

---

### CA-06 — Faixa de categoria ("25–75 kW") coerente com a unidade da carga instalada

**Status: ⚠️ PARCIAL — fora de escopo (conforme o próprio documento, seção 8)**

**Evidência de código** (`CategoriaSubcategoriaCard.tsx:92`, `ParametrosEDPEditor.tsx:355,431-432`):
```tsx
<Tag type="cool-gray" size="sm">
  {cat.carga_instalada_min_kW}–{cat.carga_instalada_max_kW} kW
</Tag>
```

Este rótulo **não foi alterado**. O documento de origem classifica esta mudança como fora de escopo até confirmação normativa (seção 8: *"Faixa de categoria em kW vs kVA — confirmação normativa é pré-requisito, não parte desta correção"*) e a lista explicitamente em "NÃO TOCAR" (seção 5). Portanto este não é um defeito da implementação — é uma decisão de escopo já prevista e respeitada.

**Ação pendente (não bloqueante):** confirmar com a documentação EDP (PT.DT.PDN.00068 v09) se a base das Tabelas 001/002 é kW ou kVA, conforme dúvida crítica levantada na seção 4.3 do documento. Se confirmado que a base é kW, será necessário abrir P-KVWA-ADV para implementar a conversão VA→kW.

---

### CA-07 — Nenhuma referência a "kW" como unidade de carga instalada fora do contexto de faixa

**Status: ✅ PASS**

Varredura em `src/components/app/edp-sp/` e `src/domain/distribuidora/edp-sp/` confirma que todas as ocorrências restantes de `"kW"` pertencem exclusivamente a:
- Faixas de categoria (`carga_instalada_min_kW`/`max_kW`, tags de classificação, editor de parâmetros) — fora de escopo (CA-06).
- Limite de média tensão (`75 kW`) — fora de escopo (CA-06/parte da tabela de categoria).

Nenhum outro módulo do sistema (fora de `edp-sp`) referencia "carga instalada" — confirmado por busca em todo `src/`.

---

### CA-08 — Cálculo de carga instalada, demanda, ID e seleção de categoria permanecem idênticos (NÃO TOCAR respeitado)

**Status: ✅ PASS**

Nenhum arquivo de lógica de cálculo (`motor-demanda.ts`, `motor-edp-sp.ts`, `seletor-categoria.ts`, `categorias-fornecimento.ts`, `seletor-subcategoria.ts`) foi modificado nesta correção. Apenas literais de exibição em 2 componentes React e 1 arquivo de mensagens de diagnóstico.

---

### CA-09 — Suíte de testes de não-regressão

**Status: ✅ PASS**

```
Test Files  15 passed (15)
     Tests  129 passed (129)
```

Testes cobrem `motor-edp-sp`, `motor-demanda`, `validacao`, `seletor-categoria`, `seletor-subcategoria`, `categorias-fornecimento`, `parametros`, `contratos`, `classificacao`, `fatores-potencia`, `tabelas-demanda`, `adaptador-projeto`, `subcategorias-fornecimento`. Nenhum teste depende do texto exato das mensagens de diagnóstico com "kW"/"kVA" (asserts usam `codigo`, não `mensagem`), portanto a mudança de rótulo não quebrou nenhuma asserção existente.

---

### CA-10 — Documentação da dúvida crítica (base da faixa EDP: kW ou kVA?)

**Status: ✅ PASS (documentado, não respondido — como esperado)**

Conforme seção 10.3 do documento de origem, esta correção **não deveria** responder a essa dúvida, apenas documentá-la. Está registrada neste relatório em CA-06 como ação pendente não bloqueante.

---

## Checklist de Entrega (seção 11 do documento de origem)

- [x] Localização de todas as ocorrências do rótulo "carga instalada kW" na interface.
- [x] Mudança aplicada (rótulo antes/depois confirmado nos trechos de código acima).
- [x] Confirmação de que o valor numérico não muda, apenas a unidade.
- [x] Suíte de testes executada (129 testes, 0 falhas).
- [x] Documentação da dúvida crítica: base da faixa EDP é kW ou kVA? (permanece em aberto, aguardando confirmação normativa).
- [x] Confirmação de que "NÃO TOCAR" foi respeitado (cálculo, faixas de categoria, tabelas 001/002 intocados).

---

## Resumo Executivo

A correção **P-KVVA** foi implementada corretamente e dentro do escopo definido. Todas as 4 ocorrências user-facing do rótulo "kW" referentes à **carga instalada** (valor medido) foram alteradas para "kVA", sem qualquer alteração de valores numéricos ou lógica de cálculo/classificação. O único item não resolvido — a unidade da faixa de categoria EDP (min/max) — é explicitamente fora de escopo desta correção por decisão do próprio documento de origem, pendente de confirmação normativa formal antes de qualquer ajuste (potencial P-KVWA-ADV).

**Gate: PASS — pronto para revisão de código / handoff a @devops para push.**
