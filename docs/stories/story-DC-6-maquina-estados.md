# Story DC-6: Máquina de Estados e Contratos Downstream

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-6  
**Status:** Ready  
**Priority:** CRITICAL (orquestração)  
**Complexity:** L (11 estados + contratos downstream)  
**Dependency:** DC-1 a DC-5  
**Assignee:** @dev (Dex)

---

## Story

Como serviço de dimensionamento, preciso implementar uma máquina de estados por circuito que rastreie o fluxo de cálculo (rascunho → dados incompletos → dimensional parcial → verificado ou reprovado) e integre com MOD-QT, MOD-CC, MOD-SEC para receber retornos que acionem revalidação automática.

---

## Acceptance Criteria

### AC-DC-09, AC-DC-20, AC-DC-21

- [ ] **AC-DC-09:** Nenhum circuito atinge `VERIFICADO-COMPLETO` enquanto C3, C4 ou C5 pendentes
- [ ] **AC-DC-20:** Nenhuma seção atende → `REQUER-ESTUDO-PARALELO`, sem dimensionamento automático
- [ ] **AC-DC-21:** Retorno MOD-QT exigindo seção maior → revalidação completa, critério decisivo atualizado

**Verificação:** Testes de máquina de estados; simulação de retornos downstream.

---

## Dev Notes

### Máquina de estados

```
RASCUNHO
  ↓ (dados mínimos preenchidos)
DADOS-INCOMPLETOS
  ├─ Aguardando entrada obrigatória
  ↓ (cálculo bem-sucedido)
DIMENSIONAMENTO-PARCIAL
  ├─ AGUARDANDO-QT (C5 bloqueado)
  ├─ AGUARDANDO-CC (C3 bloqueado)
  ├─ AGUARDANDO-SECCIONAMENTO (C4 bloqueado)
  ├─ PENDENTE-I2
  ├─ VERIFICAR-NEUTRO-HARMONICAS
  └─ REQUER-ESTUDO-PARALELO
  
  ↓ (todos retornos OK)
VERIFICADO-COMPLETO
  └─ Todos critérios C1-C6 APROVADO ou NAO-APLICAVEL

REPROVADO (se In > Iz ou outro erro bloqueante)
```

### Classes principais

```typescript
class ServicoMaquinaEstados {
  transicionar(circuito: Circuito, evento: Evento): NovoEstado {
    // Validar transição conforme máquina definida
    // Acumular pendências: AGUARDANDO-QT, AGUARDANDO-CC, etc.
    // Retornar novo estado + lista de pendências
  }
}

class ServicoIntegracaoDownstream {
  receberRetornoQT(circuito: Circuito, retorno: RetornoQT): void {
    // Revalidar todos critérios com nova restrição de queda
    // Atualizar critério decisivo
    // Transicionar estado
  }
}
```

### Tarefas

1. [ ] Implementar máquina de estados (11 estados)
2. [ ] Contratos com MOD-QT, MOD-CC, MOD-SEC (§19 PRD)
   - [x] MOD-CC: anexar `retorno_cc` persistido por dependência ao circuito antes do lote
   - [x] MOD-SEC: anexar `retorno_seccionamento` persistido e preservar TT como `NAO-APLICAVEL`
   - [ ] MOD-QT: anexar `retorno_qt` persistido e revalidar C5
3. [ ] Revalidação automática em retorno downstream
   - [x] MOD-CC: C3 revalida quando `retorno_cc` válido está persistido
   - [x] MOD-SEC: C4 revalida quando `retorno_seccionamento` válido está persistido; TT permanece `NAO-APLICAVEL`
   - [ ] MOD-QT
4. [ ] Testes de transição de estado (happy path + edge cases)

### Bloqueadores

- Nenhum novo

---

## File List

**Created/Modified:**
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/modelo/circuito.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/calculo/contratos-corrente.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/calculo/divisao-circuitos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/adaptadores/adaptador-correntes.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-corrente.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts`

---

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `npx vitest run tests/api/dimensionamento-condutores-flow.test.ts tests/api/modulos-mod-cc.test.ts` - PASS 13/13
- `npx vitest run tests/api/dimensionamento-condutores-flow.test.ts tests/api/modulos-mod-sec.test.ts` - PASS 18/18
- `npx tsc --noEmit --pretty false` - PASS
- `npm run typecheck` - PASS
- `npm test` - PASS 698/698
- `npm run lint` - FAIL sem diagnóstico capturado; `npx eslint` focado nos arquivos alterados PASS

### Completion Notes

- Implementado enriquecimento do fluxo de projeto/lote com `retorno_cc` válido já persistido em `dependencia_retornos_downstream`.
- Implementado enriquecimento do fluxo de projeto/lote com `retorno_seccionamento` válido já persistido em `dependencia_retornos_downstream`.
- Em esquema TT, a orquestração não anexa retorno MOD-SEC, mesmo se existir registro persistido; o motor resolve C4 como `NAO-APLICAVEL` sem `AGUARDANDO-SECCIONAMENTO`.
- O motor puro `dimensionarCircuito()` permanece sem I/O; a orquestração ocorre em `servico-dimensionamento-condutores`.
- Propagado metadado opcional `origem_dependencia_ids` do plano de divisão/correntes até `CircuitoParaDimensionamento` para correlacionar circuitos com retornos downstream persistidos.
- Retorno MOD-CC inválido é ignorado e preserva `AGUARDANDO-CC`.
- Retorno MOD-SEC inválido é ignorado e preserva `AGUARDANDO-SECCIONAMENTO` em TN/IT.
- Não foi implementada chamada automática ao endpoint MOD-CC porque os parâmetros `icc_presumida_a`, `tempo_atuacao_s` e `integral_joule_dispositivo` não existem como fonte de produção no fluxo atual.
- Não foi implementada chamada automática ao endpoint MOD-SEC porque `tempo_atuacao_s` não existe como fonte de produção no fluxo atual.

---

## Change Log

- **2026-07-12:** Story criada por @sm River
- **2026-07-12:** Validada por @po Pax — 10-point checklist GO (9→10/10); complexity L adicionada; Status Draft → Ready
- **2026-07-16:** @dev implementou workflow `WORKFLOW-AGUARDANDO-CC-RETORNO-MOD-CC.md` para consumir retorno MOD-CC persistido e resolver C3 no lote quando `retorno_cc` válido existir.
- **2026-07-16:** @dev implementou workflow `WORKFLOW-AGUARDANDO-SECCIONAMENTO-RETORNO-MOD-SEC.md` para consumir retorno MOD-SEC persistido em TN/IT e manter TT como `NAO-APLICAVEL` sem pendência.
