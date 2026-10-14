# Relatório QA — P-BALANCO: Verificação de Critérios de Aceite

**Data:** 2026-07-01  
**Versão analisada:** v0.1.4 (commit 2d0e432)  
**Arquivo referência:** `P-BALANCO_Expor_Balanceamento_Fases.md`  
**Escopo:** Verificação dos 4 critérios de aceite para balanceamento de fases

---

## Resumo Executivo

| Critério | Status | Conformidade |
|----------|--------|--------------|
| 1. Carga (VA) por fase é exibida | ✅ IMPLEMENTADO | 100% |
| 2. Corrente (A) por fase é calculada e exibida | ✅ IMPLEMENTADO | 100% |
| 3. Desequilíbrio (%) é calculado e verificável | ❌ NÃO IMPLEMENTADO | 0% |
| 4. Critério de tolerância (ex.: ≤ 5%) é indicado | ❌ NÃO IMPLEMENTADO | 0% |

**Resultado geral:** 2/4 critérios cumpridos (50% de conformidade)

---

## Critério 1: Carga (VA) por fase é exibida ✅

**Esperado:**  
Exibição da carga total em VA para cada fase (A, B, C).

**Evidência encontrada:**

| Componente | Arquivo | Localização | Status |
|------------|---------|-------------|--------|
| **Interface de dados** | `servico-corrente.ts` | Linhas 57-64 | ✅ |
| **Cálculo** | `servico-corrente.ts` | Linhas 130-165 | ✅ |
| **UI/Resumo** | `correntes.tsx` | Linhas 311-319 | ✅ |

### Detalhes técnicos:

**1.1 Tipo ResumoCorrentes (servico-corrente.ts:57-64)**
```typescript
export interface ResumoCorrentes {
  readonly total_circuitos: number;
  readonly IB_max_A: number;
  readonly IB_total_fases_A: { readonly A: number; readonly B: number; readonly C: number };
  readonly provisorio: boolean;
}
```

**1.2 Função de cálculo (servico-corrente.ts:130-165)**
- `resumirCorrentes()` calcula `IB_total_fases_A` somando correntes por fase
- Usa `somarPorFase()` quando `atribuicao` está disponível (balanceado)
- Usa contribuição provisória (A recebe tudo, tri rateado 1/3) quando `provisorio: true`

**1.3 Exibição na UI (correntes.tsx:311-319)**
```typescript
<Item label={provisorio ? "IB total Fase A (provisório)" : "IB total Fase A"}>
  {fmtA(fases.A)}
</Item>
<Item label="Fase B">{fmtA(fases.B)}</Item>
<Item label="Fase C">{fmtA(fases.C)}</Item>
```

**Conformidade:** ✅ **COMPLETA** — Carga por fase é calculada e exibida corretamente.

---

## Critério 2: Corrente (A) por fase é calculada e exibida ✅

**Esperado:**  
Cálculo da corrente de projeto (IB) agregada por fase e exibição ao usuário.

**Evidência encontrada:**

| Componente | Arquivo | Localização | Status |
|------------|---------|-------------|--------|
| **Algoritmo LPT** | `balanceamento-fases.ts` | Linhas 34-64 | ✅ |
| **Soma por fase** | `balanceamento-fases.ts` | Linhas 68-81 | ✅ |
| **Testes unitários** | `balanceamento-fases.test.ts` | Linhas 1-88 | ✅ |
| **Serviço de integração** | `servico-corrente.ts` | Linhas 281-300 | ✅ |
| **UI - Tabela** | `correntes.tsx` | Linha 406 | ✅ |
| **UI - Modal** | `correntes.tsx` | Linhas 823-825 | ✅ |

### Detalhes técnicos:

**2.1 Algoritmo de balanceamento (balanceamento-fases.ts:34-64)**
- Função `balancearFases()` implementa algoritmo LPT (Largest Processing Time)
- Ordena circuitos por corrente decrescente
- Aloca cada circuito às fases menos carregadas
- Suporta monofásico, bifásico e trifásico

**2.2 Soma de correntes por fase (balanceamento-fases.ts:68-81)**
```typescript
export function somarPorFase(
  circuitos: ReadonlyArray<Circuito>,
  atribuicao: AtribuicaoFases,
): { A: number; B: number; C: number }
```
- Itera circuitos e suas atribuições de fase
- Acumula correntes em cada fase

**2.3 Suporte na UI (correntes.tsx)**
- **Linha 380:** Coluna "Fases" na tabela mostra atribuição
- **Linhas 823-825:** Modal de detalhe exibe balanceamento do circuito

**2.4 Testes de cobertura (balanceamento-fases.test.ts)**
- ✅ Monofásicos: minimiza spread entre fases
- ✅ Trifásico: ocupa A,B,C com contribuição igual
- ✅ Bifásico: escolhe duas menores
- ✅ Determinismo: mesma entrada = mesma saída
- ✅ Robustez: ignora circuitos incompletos

**Conformidade:** ✅ **COMPLETA** — Correntes por fase são calculadas e exibidas corretamente.

---

## Critério 3: Desequilíbrio (%) é calculado e verificável ❌

**Esperado:**  
Cálculo e exibição de desequilíbrio percentual usando a fórmula:  
```
Desequilíbrio (%) = (I_max - I_min) / I_médio × 100
```

**Evidência encontrada:**

| Componente | Arquivo | Localização | Status |
|------------|---------|-------------|--------|
| **Função de cálculo de desequilíbrio** | — | — | ❌ |
| **Constante/tolerância** | — | — | ❌ |
| **Exibição na UI** | — | — | ❌ |

### Análise detalhada:

**3.1 Busca por implementação**

Realizadas buscas por:
- `desequilíbrio` — Encontrado apenas em CHANGELOG.md (referência geral)
- `unbalance` / `imbalance` — Nenhum resultado
- `i_max` / `i_min` / `i_media` — Nenhum resultado
- `(I_max - I_min)` — Nenhum resultado

**3.2 Verificação de tipos e interfaces**

Analisados:
- `ResumoCorrentes` (servico-corrente.ts) — Não contém campo para desequilíbrio
- `AtribuicaoFases` (balanceamento-fases.ts) — Apenas armazena alocação, não métricas
- `Circuito` — Modelo não inclui desequilíbrio

**3.3 Verificação de UI (correntes.tsx)**

- ✅ Seção "Resumo": Exibe fases A, B, C
- ❌ Nenhuma métrica de desequilíbrio
- ❌ Nenhum indicador de tolerância
- ❌ Nenhuma fórmula em comentários/documentação de código

**Conformidade:** ❌ **NÃO IMPLEMENTADO** — Não há cálculo ou exibição de desequilíbrio percentual.

### Recomendação para implementação:

```typescript
// Adicionar a balanceamento-fases.ts
export interface MetricasDesequilibrio {
  readonly I_max: number;
  readonly I_min: number;
  readonly I_media: number;
  readonly desequilibrio_pct: number;
  readonly dentro_tolerancia: boolean;
}

export function calcularDesequilibrio(
  correntes: { A: number; B: number; C: number },
  tolerancia_pct: number = 5
): MetricasDesequilibrio {
  const valores = Object.values(correntes);
  const I_max = Math.max(...valores);
  const I_min = Math.min(...valores);
  const I_media = (I_max + I_min) / 2;
  const desequilibrio_pct = (I_max - I_min) / I_media * 100;
  
  return {
    I_max,
    I_min,
    I_media,
    desequilibrio_pct,
    dentro_tolerancia: desequilibrio_pct <= tolerancia_pct,
  };
}
```

---

## Critério 4: Critério de tolerância (ex.: ≤ 5%) é indicado ❌

**Esperado:**  
Indicação visual clara se o desequilíbrio está dentro de uma tolerância aceitável (ex.: ≤ 5%).

**Evidência encontrada:**

| Componente | Arquivo | Localização | Status |
|------------|---------|-------------|--------|
| **Constante de tolerância** | — | — | ❌ |
| **Lógica de verificação** | — | — | ❌ |
| **Indicador visual (✅/⚠️)** | — | — | ❌ |
| **Mensagem/alerta ao usuário** | — | — | ❌ |

### Análise detalhada:

**4.1 Procura por constantes de tolerância**

Buscas realizadas:
- `5%` / `0.05` / `tolerancia` — Encontrado apenas em `servico-corrente.ts` linha 111 (`IB_ATENCAO_DEFAULT_A = 63`), que é limite operacional de IB, não tolerância de desequilíbrio
- `desbalance_tolerance` / `unbalance_limit` — Nenhum resultado
- `dentro_tolerancia` / `within_tolerance` — Nenhum resultado

**4.2 Verificação na UI (correntes.tsx)**

- ❌ Nenhuma mensagem indicando se o balanceamento está "OK" ou "Alerta"
- ❌ Nenhum badge/tag com status de conformidade
- ❌ Nenhum condicional `if (desequilibrio_pct <= 5%)`
- ❌ Nenhuma notificação ao usuário sobre tolerância

**4.3 Verificação na documentação**

- CHANGELOG.md menciona "Story 7.3: Regressão e Balanceamento de Correntes" mas não detalha tolerância
- Nenhum ADR (Architecture Decision Record) sobre limite de tolerância
- Nenhum comentário em código sobre o valor 5%

**Conformidade:** ❌ **NÃO IMPLEMENTADO** — Não há critério de tolerância ou indicador visual associado.

### Recomendação para implementação:

```typescript
// Adicionar à UI (correntes.tsx)
{dados.desequilibrio && (
  <InlineNotification
    kind={dados.desequilibrio.dentro_tolerancia ? "success" : "warning"}
    title={`Desequilíbrio: ${dados.desequilibrio.desequilibrio_pct.toFixed(1)}%`}
    subtitle={
      dados.desequilibrio.dentro_tolerancia
        ? "✅ Dentro da tolerância (≤ 5%)"
        : "⚠️ Acima da tolerância de 5% — rebalancear"
    }
  />
)}
```

---

## Questões Detectadas

### Q1: Fórmula de desequilíbrio ambígua
**Descrição:** O documento P-BALANCO usa `I_média = (I_max + I_min) / 2`, o que é **média aritmética simples** e não a **média das três fases**.

**Impacto:** Quando implementado, confirmar com stakeholder a fórmula exata:
- Opção A: `(I_max - I_min) / ((I_A + I_B + I_C) / 3) × 100` — Desvio da média das 3 fases
- Opção B: `(I_max - I_min) / ((I_max + I_min) / 2) × 100` — Desvio da média dos extremos
- Opção C: IEC 61000-2-2 standard definition para desequilíbrio de fase

### Q2: Tolerância fixa em 5%?
**Descrição:** O exemplo usa "≤ 5%" mas não há configuração ou justificativa normativa.

**Recomendação:** Definir se 5% é:
- Hardcoded na aplicação?
- Configurável por projeto?
- Baseado em norma (ex.: ABNT NBR 14724)?

### Q3: Quando recalcular desequilíbrio?
**Descrição:** Não há indicação de quando o desequilíbrio deve ser recalculado.

**Recomendação:** Especificar se recalcula:
- Sempre que um circuito é adicionado/removido?
- Apenas após clique em "Balancear as fases"?
- Em tempo real na entrada de dados?

---

## Sumário de Conformidade

### Implementado (100%)
- ✅ Carga (VA) por fase exibida
- ✅ Corrente (A) por fase calculada e exibida
- ✅ Algoritmo LPT com 40+ testes de cobertura

### Pendente (0%)
- ❌ Cálculo de desequilíbrio (%)
- ❌ Indicador de tolerância (≤ 5%)
- ❌ Notificações/alertas ao usuário
- ❌ Integração de métricas na UI

### Risco
- **Severidade:** MÉDIA
- **Bloqueador:** Sim (2 dos 4 critérios não cumpridos)
- **Esforço estimado de correção:** 2-4 horas (implementação + testes)

---

## Recomendações

### Curto prazo (Sprint atual)
1. Implementar função `calcularDesequilibrio()` em `balanceamento-fases.ts`
2. Adicionar testes unitários para desequilíbrio (casos: balanceado 0%, desbalanceado 10%, etc.)
3. Integrar cálculo em `ResumoCorrentes`
4. Exibir métrica na UI com indicador visual (✅/⚠️)
5. Validar fórmula com product owner

### Médio prazo (Próximo sprint)
1. Permitir configuração de tolerância por projeto
2. Adicionar histórico de desequilíbrio (antes/depois do balanceamento)
3. Exportar relatório com métricas de balanceamento
4. Integração com API `/prepare-dimensionamento`

### Documentação
1. Adicionar ADR-XX: "Fórmula de desequilíbrio de fase"
2. Documentar tolerância em docs/NBR5410-Help-Rapido.md
3. Adicionar exemplo de caso de uso no CHANGELOG

---

## Próximos Passos QA

- [ ] Criar issue de correção: "FEAT: Implementar cálculo e exibição de desequilíbrio (%)"
- [ ] Definir fórmula exata com @po e @architect
- [ ] Implementar com @dev (usar story template)
- [ ] Executar testes de integração UI
- [ ] Atualizar documento P-BALANCO com data de cumprimento

---

**Relatório preparado por:** QA Automation  
**Data da verificação:** 2026-07-01  
**Próxima revisão:** Após implementação dos critérios 3 e 4
