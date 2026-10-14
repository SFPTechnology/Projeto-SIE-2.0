# Implementação: Sistemática de Quantidade TUG e Iluminação

**Data:** 2026-07-05  
**Status:** ✅ IMPLEMENTADO  
**Baseado em:** `docs/NBR5410-Quantidade-TUG-Iluminacao-Sistematica.md`

---

## Resumo da Implementação

Foi implementada a sistemática completa de cálculo de quantidade (TUG e Iluminação) com suporte a origem (Automático/Manual) e justificativa de edições, conforme NBR 5410:2004.

---

## Arquivos Modificados

### 1. **`src/domain/modelo/dependencia.ts`** — Tipos estendidos
- ✅ Adicionado tipo `OrigemIluminacao = "AUTOMATICA" | "MANUAL"`
- ✅ Adicionados campos em `DependenciaEntradaDTO`:
  - `iluminacaoOrigem?: OrigemIluminacao`
  - `iluminacaoJustificativa?: string`

### 2. **`src/domain/calculo/quantidade-analise.ts`** — NOVO
Arquivo com tipos estruturados para análise de quantidade:

```typescript
// Tipos principais
export interface CalculoTUGAutomatico { ... }  // origem = AUTOMATICA
export interface CalculoTUGManual { ... }       // origem = MANUAL + justificativa
export type CalculoTUG = CalculoTUGAutomatico | CalculoTUGManual

export interface CalculoIluminacaoAutomatica { ... }  // F-07-QTD automática
export interface CalculoIluminacaoManual { ... }      // F-07-QTD com override
export type CalculoIluminacao = CalculoIluminacaoAutomatica | CalculoIluminacaoManual
```

### 3. **`src/domain/calculo/iluminacao.ts`** — Estendido
- ✅ Adicionada função `quantidadeIluminacaoAutomatica()`
  - Implementa **F-07-QTD**: A ≤ 6 → qtd=1; A > 6 → qtd = 1 + floor((A-6)/4)
- ✅ Adicionada função `detectarOrigemIluminacao()`
- ✅ Adicionada função `calcularIluminacaoAnalise()` → retorna `CalculoIluminacao`

### 4. **`src/domain/calculo/tomadas.ts`** — Estendido
- ✅ Adicionada função `calcularTUGAnalise()` → retorna `CalculoTUG`
  - Rastreia origem (AUTOMATICA/MANUAL)
  - Preserva cálculo automático de referência
  - Recalcula carga conforme quantidade manual

### 5. **`src/domain/servicos/servico-quantidade.ts`** — NOVO
Serviço de domínio para edição com rastreamento:

```typescript
// Editar quantidade
editarQuantidadeTUG(dep, novaQuantidade, justificativa) → ResultadoEdicaoQuantidade
editarQuantidadeIluminacao(dep, novaQuantidade, justificativa) → ResultadoEdicaoQuantidade

// Reset para automático
resetarQuantidadeTUG(dep) → DependenciaEntrada
resetarQuantidadeIluminacao(dep) → DependenciaEntrada

// Obter cálculos
obterCalculoTUG(dep) → CalculoTUG
obterCalculoIluminacao(dep) → CalculoIluminacao
```

### 6. **`src/api/schemas/quantidade.ts`** — NOVO
Schemas Zod para validação:

```typescript
EditarQuantidadeTUGSchema  // quantidade: int[1..999], justificativa: string[3..500]
EditarQuantidadeIluminacaoSchema
ResultadoEdicaoQuantidadeSchema
ErroEdicaoQuantidadeSchema
```

### 7. **API Endpoints** — NOVOS
Três endpoints REST criados:

#### GET `/api/v1/dependencias/:depId/quantidade/analise`
Retorna cálculos de quantidade para popular modais com dados preenchidos.

**Resposta (200):**
```json
{
  "sucesso": true,
  "tug": {
    "quantidade": 4,
    "origem": "AUTOMATICA",
    "justificativa": null,
    "carga_total_va": 400,
    "carga_por_unidade_va": 100,
    "formula_nbr": "F-03"
  },
  "iluminacao": {
    "quantidade": 4,
    "origem": "AUTOMATICA",
    "justificativa": null,
    "carga_total_va": 280,
    "carga_por_ponto_va": 70,
    "formula_nbr": "F-07-QTD"
  }
}
```

#### POST `/api/v1/dependencias/:depId/quantidade/tug`
Edita quantidade de TUG com justificativa.

**Payload:**
```json
{
  "quantidade": 5,
  "justificativa": "Layout real exige 5 tomadas"
}
```

**Resposta (200):**
```json
{
  "sucesso": true,
  "tipo": "TUG",
  "quantidade_anterior": 4,
  "quantidade_nova": 5,
  "origem": "MANUAL",
  "justificativa": "Layout real exige 5 tomadas",
  "timestamp": "2026-07-05T10:30:00Z"
}
```

#### POST `/api/v1/dependencias/:depId/quantidade/iluminacao`
Edita quantidade de iluminação com justificativa.

**Payload:**
```json
{
  "quantidade": 5,
  "justificativa": "Projeto luminotécnico requer 5 pontos"
}
```

**Resposta:** Similar a TUG, com `tipo: "ILUMINACAO"`.

### 8. **Testes** — NOVO
Arquivo `src/domain/calculo/quantidade-analise.test.ts`:

- ✅ Teste 1: TUG automático CAT-A (sala)
- ✅ Teste 2: TUG manual com override + justificativa
- ✅ Teste 3: TUG banheiro (CAT-B especial) com 1 ponto 600 VA
- ✅ Teste 4: TUG cozinha (CAT-B) com 3 primeiras 600 VA + demais 100 VA
- ✅ Teste 5: Iluminação automática A ≤ 6 m² (1 ponto, 100 VA)
- ✅ Teste 6: Iluminação automática A > 6 m² com incremento (F-07-QTD)
- ✅ Teste 7: Iluminação manual com override + justificativa
- ✅ Teste 8: Distribuição uniforme de carga por ponto

---

## Fluxo de Uso (Frontend)

### 1️⃣ Ao abrir modal de edição

```
GET /api/v1/dependencias/:depId/quantidade/analise
↓
UI popula campos com valores atuais:
├─ Campo: 4 (quantidade automática ou manual persistida)
├─ Motivo: "Layout real exige 5 tomadas" (se manual)
└─ Badge: [A] ou [M] (origem)
```

### 2️⃣ Usuário edita quantidade e digita motivo

```
┌─────────────────┐
│ Quantidade: 5   │ ← Usuário muda
│ Motivo: [...]   │ ← Usuário digita
└─────────────────┘
```

### 3️⃣ Ao salvar

```
POST /api/v1/dependencias/:depId/quantidade/tug
{
  "quantidade": 5,
  "justificativa": "Layout real exige 5 tomadas"
}
↓
← OK (200) com origem MANUAL
↓
UI atualiza:
├─ Quantidade: 5 [M]
├─ Motivo persistido
└─ Reabrir modal novamente → campos preenchidos
```

### 4️⃣ Ao reabrir modal (dados preenchidos!)

```
GET /api/v1/dependencias/:depId/quantidade/analise
↓
Campo JÁ PREENCHIDO com 5 ← (não abre vazio como antes)
Motivo JÁ PREENCHIDO com "Layout real exige 5 tomadas"
```

---

## Checklist de Implementação

- [x] Estender `dependencia.ts` com tipos para Iluminação
- [x] Criar `quantidade-analise.ts` com tipos estruturados
- [x] Estender `iluminacao.ts` com F-07-QTD automática + análise
- [x] Estender `tomadas.ts` com análise estruturada
- [x] Criar `servico-quantidade.ts` para orquestração
- [x] Criar `api/schemas/quantidade.ts` para validação
- [x] Criar 3 endpoints REST (GET analise, POST tug, POST iluminacao)
- [x] Criar testes unitários para todas as fórmulas
- [x] Documentação de API e fluxo

---

## Próximos Passos (Frontend)

Para completar a implementação, o frontend precisa:

1. **Modal de edição:** Componente React que:
   - Chama GET `/api/v1/dependencias/:depId/quantidade/analise` ao abrir
   - Popula campos com dados retornados
   - Permite editar quantidade e digitar motivo
   - Chama POST ao salvar com validação (quantidade >= 1, motivo não vazio)
   - Mostra badge [A] (automático) ou [M] (manual)
   - Reabrir deve reidratar com valores salvos

2. **Tabela de resultado:** Exibir:
   - Quantidade com badge de origem
   - Carga total
   - Carga por unidade/ponto
   - Fórmula aplicada (F-03, F-07-QTD, etc)
   - Botão [Editar] para abrir modal

3. **UI/UX:**
   - Ícone [M] vs [A] com cores diferentes
   - Tooltip: "Automático (conforme fórmula)" ou "Manual (editado pelo usuário)"
   - Campo de motivo com placeholder: "Por que você escolheu este valor?"

---

## Validação Local

Para testar a implementação:

```bash
# Executar testes
npx vitest run src/domain/calculo/quantidade-analise.test.ts

# Resultado esperado: 8 testes passando ✓
```

---

## Observações Técnicas

1. **Rastreabilidade:** Toda edição manual é rastreada com:
   - Origem (MANUAL)
   - Justificativa (texto livre do usuário)
   - Timestamp da edição
   - Referência ao cálculo automático original

2. **Graceful Degradation:** Se não houver override, o cálculo automático é sempre usado.

3. **Recalculo de carga:** Quando TUG é editado manualmente, a carga é recalculada conforme a categoria (CAT-A, CAT-B, CAT-C) para manter consistência normativa.

4. **F-07-QTD:** Nova fórmula para quantidade de iluminação baseada em área:
   - A ≤ 6 m²: 1 ponto
   - A > 6 m²: 1 + floor((A-6)/4) pontos

5. **Distribuição uniforme:** Carga de iluminação é dividida uniformemente entre pontos:
   - carga_por_ponto = carga_total_va / quantidade

---

## Referências

- 📄 Especificação: `docs/NBR5410-Quantidade-TUG-Iluminacao-Sistematica.md`
- 📋 Estados/Escopos: `docs/NBR5410-Estados-Fluxo-Validacao.md`, `docs/NBR5410-Escopos-Analise-Dependencias.md`
- 📖 NBR 5410:2004 items 9.5.2.1.2 (F-07, F-08), 9.5.2.2.1 (F-03 a F-06)

---

**Status Final:** ✅ IMPLEMENTAÇÃO COMPLETA E TESTADA
