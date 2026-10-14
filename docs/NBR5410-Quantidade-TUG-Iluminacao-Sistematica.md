# Sistemática de Quantidade — TUG e Iluminação (NBR 5410)

**Documento:** Análise e implementação da sistemática de cálculo de quantidade com suporte a Automático/Manual  
**Data:** 2026-07-05  
**Contexto:** Auditoria técnica EDP V09 — Projeto SIE `feature/nbr5410-conformidade-closeout`  
**Baseado em:** REFERENCIA-INTEGRAL-SISTEMA.md (fórmulas F-03 a F-08)

---

## Índice

1. [Sistemática Atual: Quantidade de TUG](#1-sistemática-atual-quantidade-de-tug)
2. [Análise de Parâmetros de Quantidade](#2-análise-de-parâmetros-de-quantidade)
3. [Aplicação em Pontos de Iluminação](#3-aplicação-em-pontos-de-iluminação)
4. [Origem Automática vs. Manual](#4-origem-automática-vs-manual)
5. [Implementação Técnica](#5-implementação-técnica)

---

## 1. Sistemática Atual: Quantidade de TUG

### 1.1 Conceito Geral

A **Quantidade de TUG** (Tomadas de Uso Geral) é calculada automaticamente conforme a NBR 5410:2004, baseado em:
- **Perímetro** da dependência (P)
- **Categoria** da dependência (CAT-A, CAT-B, CAT-C)
- **Tipo específico** (cozinha, banheiro, área de serviço, etc.)

### 1.2 Fórmulas Normativas (F-03 a F-06)

| ID | Categoria | Fórmula | Carga por tomada | Fonte NBR |
|---|---|---|---|---|
| **F-03** | **CAT-A** (Salas, Dormitórios, Hall) | `qtd = ceil(P / 5)` mínimo 1 | 100 VA | 9.5.2.2.1.c |
| **F-04a** | **CAT-B** (Cozinha, Copa, Área de Serviço) | `qtd = ceil(P / 3.5)` | 3 primeiras: 600 VA cada; demais: 100 VA | 9.5.2.2.1.a |
| **F-04b** | **CAT-B** (Banheiro) | `qtd = 1` (mínimo) | 600 VA | 9.5.2.2.1.b |
| **F-06** | **CAT-C** (Varanda, Área externa) | Se A > 6 m²: `ceil(P / 5)`; senão 1 | 100 VA | 9.5.2.2.1.d |

### 1.3 Exemplo Prático: Quantidade de TUG

**Cenário:** Sala (CAT-A) com 5m de largura × 4m de comprimento, sem perímetro excluído

```
Cálculos:
├─ Área (F-01): A = 5 × 4 = 20 m²
├─ Perímetro (F-02): P = 2(5 + 4) - 0 = 18 m
├─ Categoria: CAT-A (sala)
└─ Quantidade TUG (F-03): ceil(18 / 5) = ceil(3.6) = 4 tomadas

Carga total: 4 × 100 VA = 400 VA
```

**UI esperada:**
```
Pontos de Tomada
─ ─ ────── ─ ─ ┌─────┐
[4 tomadas]     │  A  │ ← Badge de AUTOMÁTICO
                └─────┘
Sobrescrever o mínimo calculado por área. Vá recalculado pela fórmula.

┌─ Motivo (opcional) ──────────────────────────┐
│ [Editar para 5 tomadas por layout real]      │
└──────────────────────────────────────────────┘
```

### 1.4 Lógica Automática vs. Manual

```
Estado inicial:
├─ origem = "AUTOMATICO"
├─ valor = 4 (conforme F-03)
├─ justificativa = null
└─ badge = [A]

Se usuário edita para 5:
├─ origem = "MANUAL"
├─ valor = 5 (user input)
├─ justificativa = "Ajustado conforme layout real" (user types)
└─ badge = [M]

Se usuário edita novamente para 4:
├─ origem = "MANUAL" (permanece, pois foi editado uma vez)
├─ valor = 4 (user changed back)
├─ justificativa = "Corrigido"
└─ badge = [M]
```

---

## 2. Análise de Parâmetros de Quantidade

### 2.1 Parâmetros Identificados (Quantidade de TUG)

| Parâmetro | Tipo | Fonte | Aplicável em |
|---|---|---|---|
| **Perímetro (P)** | Entrada | Medição de campo, cálculo F-02 | F-03, F-04a, F-06 |
| **Área (A)** | Entrada | Medição de campo, cálculo F-01 | F-06 (condicional > 6 m²) |
| **Categoria** | Entrada | Mapeamento tipo→CAT | F-03 a F-06 |
| **Tipo específico** | Entrada | Usuario (cozinha, banheiro, etc.) | F-04a, F-04b (diferencial) |
| **Percentual mínimo normativo** | Constante | NBR 5410 | Aplicado em todas as fórmulas |

### 2.2 Lógica de Cálculo (Diagrama)

```
INPUT: tipo, largura_m, comprimento_m, perimetro_excluido_m
   ↓
┌─ Calcular área ─────────────────────┐
│ A = largura_m × comprimento_m (F-01)│
└─────────────────────┬───────────────┘
                      ↓
┌─ Calcular perímetro ────────────────────────────────────┐
│ P = 2(largura + comprimento) - perimetro_excluido (F-02)│
└─────────────────────┬─────────────────────────────────┘
                      ↓
┌─ Mapear tipo → categoria ────────┐
│ tipo == "cozinha" → CAT-B        │
│ tipo == "sala" → CAT-A           │
│ tipo == "varanda" → CAT-C        │
│ etc.                             │
└─────────────────────┬────────────┘
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
    CAT-A/B/C?             Se tipo == "banheiro"
         │                        │
         │                  ┌─────↓─────┐
         │                  │ qtd = 1   │
         │                  │ carga:600 │
         │                  └───────────┘
         ↓
  ┌──────────────────────┐
  │ Aplicar fórmula NBR  │
  │ para categoria       │
  └──────┬───────────────┘
         ↓
  ┌──────────────────────┐
  │ qtd_minima = F-03    │
  │ ou F-04 ou F-06      │
  └──────┬───────────────┘
         ↓
  OUTPUT: {
    quantidade: 4,
    origem: "AUTOMATICO",
    justificativa: null,
    formula_aplicada: "F-03",
    categoria: "CAT-A"
  }
```

### 2.3 Parâmetros de Análise de Quantidade (conforme NBR 5410)

Cada cálculo de quantidade deve registrar:

```json
{
  "id": "qtd-tug-dep-001",
  "dependencia_id": "dep-001",
  "tipo_quantidade": "TUG",
  "categoria": "CAT-A",
  "parametros_entrada": {
    "largura_m": 5.0,
    "comprimento_m": 4.0,
    "perimetro_excluido_m": 0.0,
    "tipo_dependencia": "sala"
  },
  "parametros_calculados": {
    "area_m2": 20.0,
    "perimetro_m": 18.0,
    "fator_divisao": 5.0
  },
  "calculo": {
    "divisao": "ceil(18 / 5)",
    "resultado": 4,
    "minimo_normativo": 1,
    "quantidade_final": 4
  },
  "origem": "AUTOMATICO",
  "justificativa": null,
  "formula_nbr": "F-03",
  "referencia_norma": "NBR 5410:2004 item 9.5.2.2.1.c",
  "carga_total_va": 400,
  "timestamp": "2026-07-05T10:30:00Z"
}
```

---

## 3. Aplicação em Pontos de Iluminação

### 3.1 Situação Atual (antes)

Pontos de iluminação são tratados de forma **simplista:**
- **Mínimo normativo:** 1 ponto por dependência (F-07)
- **Carga:** Fixa ou fórmula por área (F-08)
- **Quantidade:** Não é calculada automaticamente; depende de input manual do usuário

**Problema:** Sem suporte a cálculo automático e rastreabilidade de origem.

### 3.2 Nova Sistemática (após)

Aplicar a mesma sistemática de TUG aos **Pontos de Iluminação**:

#### **Regra 1: Mínimo Normativo (F-07)**

```
┌─ Todos os tipos ──────────────────┐
│ Quantidade mínima = 1 por recinto  │
│ Fonte: NBR 5410 item 9.5.2.1.2    │
│ Origem: AUTOMATICO                │
└───────────────────────────────────┘
```

**Lógica:** Sempre há pelo menos 1 ponto de luz em qualquer dependência.

#### **Regra 2: Aumento por Área (F-08) — Novo**

Para dependências com **Área > 6 m²**, adicionar pontos extras:

```
Se A ≤ 6 m²:
  └─ quantidade = 1 ponto (mínimo)

Se A > 6 m²:
  └─ quantidade = 1 + ceil((A - 6) / 4)
     
Exemplos:
├─ A = 6 m²    → qtd = 1
├─ A = 10 m²   → qtd = 1 + ceil(4/4) = 1 + 1 = 2
├─ A = 12 m²   → qtd = 1 + ceil(6/4) = 1 + 2 = 3
├─ A = 20 m²   → qtd = 1 + ceil(14/4) = 1 + 4 = 5
└─ A = 50 m²   → qtd = 1 + ceil(44/4) = 1 + 11 = 12
```

**Fonte:** Interpretação prática da NBR 5410 (distribuição de pontos por área).

#### **Regra 3: Parâmetros Específicos (conforme NBR)**

| Parâmetro | Valor | Significado |
|---|---|---|
| Mínimo normativo | 1 | Pelo menos 1 ponto de luz fixo |
| Aumento por área | A cada 4 m² > 6 m² | Distribuição uniforme da iluminação |
| Carga por ponto | Conforme F-08 (100-760 VA) | Depende de A |
| Tipo de aparelho | Luminária fixa | Conforme NBR |
| Distribuição | Uniforme na dependência | Conceitual (implementação física) |

### 3.3 Fórmulas para Pontos de Iluminação

#### **F-07-QTD: Quantidade de Pontos de Luz**

```
Se A ≤ 6 m²:
  qtd_ilum = 1

Se A > 6 m²:
  qtd_ilum = 1 + floor((A - 6) / 4)

Mínimo: 1
Máximo: sem limite
```

**Exemplo prático:**
```
Dependência: Sala de 20 m²
├─ Área (F-01): A = 20 m²
├─ Quantidade (F-07-QTD): qtd = 1 + floor((20 - 6) / 4) = 1 + floor(3.5) = 1 + 3 = 4 pontos
└─ Carga por ponto (F-08): 100 + 60 × floor((20 - 6) / 4) = 100 + 60 × 3 = 280 VA
   (Mas isso é carga TOTAL, não por ponto se distribuído)
```

#### **F-08-CARGA: Carga Total de Iluminação (já implementada)**

```
Se A ≤ 6 m²:
  carga_total_ilum = 100 VA

Se A > 6 m²:
  carga_total_ilum = 100 + 60 × floor((A - 6) / 4) VA

Exemplo:
├─ A = 6 m² → carga = 100 VA
├─ A = 10 m² → carga = 100 + 60×1 = 160 VA
├─ A = 20 m² → carga = 100 + 60×3 = 280 VA
└─ A = 50 m² → carga = 100 + 60×11 = 760 VA
```

**Distribuição de carga por ponto:**
```
carga_por_ponto = carga_total_ilum / qtd_ilum

Exemplo A = 20 m²:
├─ carga_total = 280 VA
├─ qtd_ilum = 4 pontos
└─ carga_por_ponto = 280 / 4 = 70 VA por ponto
```

### 3.4 Estrutura de Dados para Iluminação

```json
{
  "id": "qtd-ilum-dep-001",
  "dependencia_id": "dep-001",
  "tipo_quantidade": "ILUMINACAO",
  "categoria": "Ponto de luz fixo",
  "parametros_entrada": {
    "largura_m": 5.0,
    "comprimento_m": 4.0,
    "tipo_dependencia": "sala"
  },
  "parametros_calculados": {
    "area_m2": 20.0,
    "limite_area_m2": 6.0,
    "passo_area_m2": 4.0,
    "acima_limite": true,
    "multiplicador": 3.0
  },
  "calculo": {
    "fator_minimo": 1,
    "fator_adicional": "floor((20 - 6) / 4) = 3",
    "quantidade_final": 4
  },
  "carga": {
    "va_base": 100,
    "va_adicional": 60,
    "multiplos": 3,
    "carga_total_va": 280,
    "carga_por_ponto_va": 70
  },
  "origem": "AUTOMATICO",
  "justificativa": null,
  "formula_nbr": "F-07-QTD + F-08",
  "referencia_norma": "NBR 5410:2004 item 9.5.2.1.2",
  "timestamp": "2026-07-05T10:30:00Z"
}
```

---

## 4. Origem Automática vs. Manual

### 4.1 Estados de Origem

Todo cálculo de quantidade deve ter origem rastreada:

| Origem | Sinal | Descrição | Editável? | Reabrir ao salvar? |
|---|---|---|---|---|
| **AUTOMATICO** | `[A]` | Calculado por fórmula NBR, sem intervenção | Sim → vira MANUAL | Sim, com valor preenchido |
| **MANUAL** | `[M]` | Editado pelo usuário, com justificativa | Sim, mas mantém MANUAL | Sim, com valor preenchido |

### 4.2 Fluxo de Edição (Estado Máquina)

```
┌─────────────────────────────────────────────────────────────┐
│ Cálculo automático: origem = AUTOMATICO, valor = 4, [A]     │
└─────────────────────────────────────────────────────────────┘
                             ↓
                    Usuário edita campo?
                      ↙               ↘
                    SIM               NÃO
                     ↓                 ↓
            Modal de edição    Permanece AUTOMATICO
                     ↓
  ┌──────────────────────────────────┐
  │ Campo: 4 (preenchido com valor)  │
  │ Motivo: [campo vazio]            │
  └──────────────────────────────────┘
                     ↓
          Usuário muda para 5
          e digita motivo
                     ↓
  ┌──────────────────────────────────┐
  │ Campo: 5                         │
  │ Motivo: "Layout real exige"      │
  └──────────────────────────────────┘
                     ↓
            Salvar clica
                     ↓
  ┌──────────────────────────────────────────────────────────┐
  │ origem = MANUAL                                          │
  │ valor = 5                                                │
  │ justificativa = "Layout real exige"                      │
  │ badge = [M]                                              │
  │ reabrir modal? = SIM (com 5 e motivo preenchidos)       │
  └──────────────────────────────────────────────────────────┘
                     ↓
        Usuário reabre edição
                     ↓
  ┌──────────────────────────────────────────────────────────┐
  │ Campo JÁ PREENCHIDO com 5                                │
  │ Motivo JÁ PREENCHIDO com "Layout real exige"             │
  │ (Não abre vazio como antes)                              │
  └──────────────────────────────────────────────────────────┘
```

### 4.3 Sinalização Visual (UI/UX)

#### **Badge de Origem**

```html
<!-- Automático -->
<span class="badge bg-success">[A]</span>

<!-- Manual -->
<span class="badge bg-warning">[M]</span>
```

#### **Campo de Edição (Modal)**

```
┌─ Ajustes de pontos (opcional) ────────────────────────────┐
│                                                            │
│  Essas informações são opcionais. Deixe em branco para   │
│  usar o valor calculado pelas dimensões. Preencha para   │
│  sobrescrever o mínimo normativo com o número real do    │
│  projeto.                                                 │
│                                                            │
├─ Pontos de iluminação ─────────────────────────────────┐ │
│                                                        │ │
│  ┌─ ─ ┐  (3)                                   ┌─ ─ ┐ │ │
│  [◄] [Quantidade de iluminação]  [►]           │ [A] │ │ │
│                                                │ ou  │ │ │
│  Sobrescrever o mínimo calculado por área.    │ [M] │ │ │
│  Vá recalculado pela fórmula.                 └─ ─ ┘ │ │
│                                                        │ │
├─ Motivo (opcional) ──────────────────────────────────┐ │ │
│ [Editar apenas se usar quantidade diferente]         │ │ │
└──────────────────────────────────────────────────────┘ │ │
│                                                        │ │
│                                      [Cancelar] [Salva] │ │
└────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

#### **Tabela de Resultados**

```
┌─ Pontos de iluminação ─────────────────────────────────────┐
│                                                            │
│ Quantidade: 4 [A]                                          │
│ Carga total: 280 VA                                        │
│ Carga por ponto: 70 VA                                     │
│ Fórmula aplicada: F-07-QTD + F-08                          │
│ Origem: AUTOMATICO                                         │
│                                                            │
│ [Editar]                                                   │
└────────────────────────────────────────────────────────────┘
```

---

## 5. Implementação Técnica

### 5.1 Estrutura de Tipos (TypeScript)

```typescript
// Origem da quantidade
type OrigemQuantidade = "AUTOMATICO" | "MANUAL";

// Parâmetros de entrada
interface ParametrosQuantidade {
  largura_m: number;
  comprimento_m: number;
  perimetro_excluido_m?: number;
  tipo_dependencia: string;
  categoria: string;
}

// Resultado do cálculo
interface CalculoQuantidade {
  quantidade: number;
  origem: OrigemQuantidade;
  justificativa?: string;
  formula_nbr: string;
  parametros_entrada: ParametrosQuantidade;
  parametros_calculados: {
    area_m2: number;
    perimetro_m?: number;
    [key: string]: any;
  };
  referencia_norma: string;
  timestamp: string;
}

// Para TUG
interface CalculoTUG extends CalculoQuantidade {
  tipo_quantidade: "TUG";
  carga_total_va: number;
  carga_por_tomada: number;
}

// Para Iluminação
interface CalculoIluminacao extends CalculoQuantidade {
  tipo_quantidade: "ILUMINACAO";
  carga_total_va: number;
  carga_por_ponto_va: number;
  distribuicao_uniforme: boolean;
}
```

### 5.2 Algoritmo de Cálculo (Pseudocódigo)

#### **Para Quantidade de TUG**

```javascript
function calcularQuantidadeTUG(dependencia) {
  // 1. Calcular dimensões
  const area = dependencia.largura_m * dependencia.comprimento_m;
  const perimetro = 
    2 * (dependencia.largura_m + dependencia.comprimento_m) 
    - (dependencia.perimetro_excluido_m || 0);

  // 2. Mapear tipo → categoria
  const categoria = mapear_tipo_para_categoria(dependencia.tipo);

  // 3. Aplicar fórmula conforme categoria
  let quantidade;
  let formula_aplicada;
  
  if (categoria === "CAT-A") {
    quantidade = Math.max(Math.ceil(perimetro / 5), 1);
    formula_aplicada = "F-03";
  } else if (categoria === "CAT-B") {
    if (dependencia.tipo === "banheiro") {
      quantidade = 1;
      formula_aplicada = "F-04b";
    } else {
      quantidade = Math.ceil(perimetro / 3.5);
      formula_aplicada = "F-04a";
    }
  } else if (categoria === "CAT-C") {
    quantidade = area > 6 ? Math.ceil(perimetro / 5) : 1;
    formula_aplicada = "F-06";
  }

  // 4. Calcular carga
  let carga_por_tomada;
  if (categoria === "CAT-B" && dependencia.tipo !== "banheiro") {
    // 3 primeiras a 600 VA, demais a 100 VA
    const carga_600 = Math.min(3, quantidade) * 600;
    const carga_100 = Math.max(0, quantidade - 3) * 100;
    carga_por_tomada = (carga_600 + carga_100) / quantidade;
  } else if (categoria === "CAT-B" && dependencia.tipo === "banheiro") {
    carga_por_tomada = 600;
  } else {
    carga_por_tomada = 100;
  }

  return {
    quantidade,
    origem: "AUTOMATICO",
    justificativa: null,
    formula_nbr: formula_aplicada,
    parametros_entrada: {
      ...dependencia.dimensoes
    },
    parametros_calculados: { area, perimetro },
    carga_total_va: quantidade * carga_por_tomada,
    carga_por_tomada,
    referencia_norma: "NBR 5410:2004",
    timestamp: new Date().toISOString()
  };
}
```

#### **Para Quantidade de Iluminação**

```javascript
function calcularQuantidadeIluminacao(dependencia) {
  // 1. Calcular área
  const area = dependencia.largura_m * dependencia.comprimento_m;

  // 2. Quantidade mínima: 1 ponto
  let quantidade = 1;
  
  // 3. Adicionar conforme área > 6 m²
  if (area > 6) {
    const multiplos = Math.floor((area - 6) / 4);
    quantidade = 1 + multiplos;
  }

  // 4. Carga total (F-08)
  let carga_total_va;
  if (area <= 6) {
    carga_total_va = 100;
  } else {
    const multiplos = Math.floor((area - 6) / 4);
    carga_total_va = 100 + 60 * multiplos;
  }

  // 5. Carga por ponto (distribuído uniformemente)
  const carga_por_ponto = carga_total_va / quantidade;

  return {
    quantidade,
    origem: "AUTOMATICO",
    justificativa: null,
    formula_nbr: "F-07-QTD + F-08",
    parametros_entrada: {
      largura_m: dependencia.largura_m,
      comprimento_m: dependencia.comprimento_m,
      tipo_dependencia: dependencia.tipo
    },
    parametros_calculados: { 
      area_m2: area,
      limite_area_m2: 6,
      passo_area_m2: 4,
      acima_limite: area > 6,
      multiplicador: area > 6 ? Math.floor((area - 6) / 4) : 0
    },
    carga_total_va,
    carga_por_ponto_va: carga_por_ponto,
    distribuicao_uniforme: true,
    referencia_norma: "NBR 5410:2004 item 9.5.2.1.2",
    timestamp: new Date().toISOString()
  };
}
```

### 5.3 Persistência (Supabase)

#### **Nova tabela: `dependencia_quantidade_analise`**

```sql
CREATE TABLE IF NOT EXISTS dependencia_quantidade_analise (
  id TEXT PRIMARY KEY,
  dependencia_id TEXT NOT NULL REFERENCES dependencias(id) ON DELETE CASCADE,
  tipo_quantidade TEXT NOT NULL CHECK (tipo_quantidade IN ('TUG', 'ILUMINACAO')),
  quantidade INTEGER NOT NULL,
  origem TEXT NOT NULL CHECK (origem IN ('AUTOMATICO', 'MANUAL')),
  justificativa TEXT,
  
  -- Parâmetros de entrada
  parametros_entrada JSONB NOT NULL,
  
  -- Parâmetros calculados
  parametros_calculados JSONB NOT NULL,
  
  -- Carga
  carga_total_va NUMERIC NOT NULL,
  carga_por_unidade_va NUMERIC NOT NULL,
  
  -- Referência normativa
  formula_nbr TEXT NOT NULL,
  referencia_norma TEXT NOT NULL,
  
  criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  atualizado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  versao INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_dependencia_quantidade_analise_dependencia_id 
  ON dependencia_quantidade_analise(dependencia_id);
CREATE INDEX idx_dependencia_quantidade_analise_tipo 
  ON dependencia_quantidade_analise(tipo_quantidade);
```

#### **Modificação em `dependencias`**

Adicionar colunas para rastreamento:

```sql
ALTER TABLE dependencias ADD COLUMN IF NOT EXISTS
  resultado JSONB DEFAULT NULL;

-- O campo resultado.tomadas.origem e resultado.iluminacao.origem
-- armazenam a origem do cálculo (AUTOMATICO ou MANUAL)
```

### 5.4 Serviço de Domínio (Domain Service)

```typescript
class ServicoCalculoQuantidade {
  async calcularTUG(dependencia: Dependencia): Promise<CalculoTUG> {
    // Verificar se há override manual
    const override = dependencia.resultado?.tomadas?.override;
    
    if (override && override.origem === "MANUAL") {
      // Retornar valor manual, mantendo MANUAL como origem
      return {
        quantidade: override.quantidade,
        origem: "MANUAL",
        justificativa: override.justificativa,
        ...
      };
    }
    
    // Caso contrário, calcular automaticamente
    return calcularQuantidadeTUG(dependencia);
  }

  async calcularIluminacao(dependencia: Dependencia): Promise<CalculoIluminacao> {
    const override = dependencia.resultado?.iluminacao?.override;
    
    if (override && override.origem === "MANUAL") {
      return {
        quantidade: override.quantidade,
        origem: "MANUAL",
        justificativa: override.justificativa,
        ...
      };
    }
    
    return calcularQuantidadeIluminacao(dependencia);
  }

  async editarQuantidade(
    dependencia: Dependencia,
    tipo: "TUG" | "ILUMINACAO",
    novaQuantidade: number,
    justificativa: string
  ): Promise<Dependencia> {
    // Validar entrada
    if (novaQuantidade < 1) {
      throw new Error("Quantidade deve ser >= 1");
    }
    
    // Gravar override
    const calculo_automatico = tipo === "TUG" 
      ? calcularQuantidadeTUG(dependencia)
      : calcularQuantidadeIluminacao(dependencia);
    
    dependencia.resultado = {
      ...dependencia.resultado,
      [tipo === "TUG" ? "tomadas" : "iluminacao"]: {
        ...calculo_automatico,
        override: {
          quantidade: novaQuantidade,
          origem: "MANUAL",
          justificativa,
          timestamp: new Date().toISOString()
        },
        // Manter o cálculo automático para referência
        quantidade_automatica: calculo_automatico.quantidade
      }
    };
    
    // Persistir
    await repoDepend
encias.atualizar(dependencia);
    
    return dependencia;
  }
}
```

### 5.5 API REST (se aplicável)

```typescript
// PATCH /api/v1/dependencias/:id/quantidade
export async function handleEditarQuantidade(request: Request) {
  const { tipo, quantidade, justificativa } = await request.json();
  
  const dependencia = await repoDependencias.buscarPorId(id);
  const servico = new ServicoCalculoQuantidade();
  
  const atualizada = await servico.editarQuantidade(
    dependencia,
    tipo,
    quantidade,
    justificativa
  );
  
  return Response.json({
    sucesso: true,
    resultado: {
      quantidade: atualizada.resultado[tipo].quantidade,
      origem: atualizada.resultado[tipo].override.origem,
      justificativa: atualizada.resultado[tipo].override.justificativa
    }
  });
}
```

---

## 6. Exemplos Práticos de Implementação

### Exemplo 1: Sala de 20 m² (TUG + Iluminação)

**Entrada:**
```json
{
  "tipo": "sala",
  "largura_m": 5,
  "comprimento_m": 4,
  "perimetro_excluido_m": 0
}
```

**Cálculos automáticos:**

```
QUANTIDADE DE TUG:
├─ Área: A = 5 × 4 = 20 m²
├─ Perímetro: P = 2(5+4) = 18 m
├─ Categoria: CAT-A (sala)
├─ Fórmula F-03: ceil(18/5) = 4 tomadas
├─ Carga: 4 × 100 VA = 400 VA
└─ Origem: [A] AUTOMATICO

QUANTIDADE DE ILUMINAÇÃO:
├─ Área: A = 20 m²
├─ Mínimo: 1 ponto
├─ Acréscimo: floor((20-6)/4) = 3 pontos
├─ Total: 1 + 3 = 4 pontos
├─ Carga total (F-08): 100 + 60×3 = 280 VA
├─ Carga por ponto: 280 / 4 = 70 VA
└─ Origem: [A] AUTOMATICO
```

**Edição manual (TUG):**

```
Usuário quer 5 tomadas (layout real diferente)

┌─ Modal de edição ──────────────────────┐
│ Quantidade: [5]                        │
│ Motivo: [Layout com 5 pontos fixos]    │
└────────────────────────────────────────┘

Após salvar:
├─ Quantidade: 5 [M] MANUAL
├─ Carga: 5 × 100 VA = 500 VA
├─ Justificativa: "Layout com 5 pontos fixos"
└─ Origem: MANUAL (persiste ao reabrir)
```

### Exemplo 2: Banheiro (CAT-B Especial)

**Entrada:**
```json
{
  "tipo": "banheiro",
  "largura_m": 2,
  "comprimento_m": 1.5,
  "perimetro_excluido_m": 0
}
```

**Cálculos automáticos:**

```
QUANTIDADE DE TUG:
├─ Área: A = 2 × 1.5 = 3 m²
├─ Perímetro: P = 2(2+1.5) = 7 m
├─ Categoria: CAT-B (banheiro)
├─ Fórmula F-04b: qtd = 1 (mínimo para banheiro)
├─ Carga: 1 × 600 VA = 600 VA
└─ Origem: [A] AUTOMATICO

QUANTIDADE DE ILUMINAÇÃO:
├─ Área: A = 3 m² (≤ 6 m²)
├─ Quantidade: 1 ponto (mínimo)
├─ Carga total (F-08): 100 VA
├─ Carga por ponto: 100 VA
└─ Origem: [A] AUTOMATICO
```

---

## 7. Checklist de Implementação

- [ ] **Estrutura de dados:** Criar tipos TypeScript para CalculoTUG e CalculoIluminacao
- [ ] **Algoritmo:** Implementar calcularQuantidadeTUG() e calcularQuantidadeIluminacao()
- [ ] **Serviço:** Criar ServicoCalculoQuantidade com métodos de cálculo e edição
- [ ] **Persistência:** Criar tabela dependencia_quantidade_analise em Supabase
- [ ] **API:** Criar endpoints PATCH para edição de quantidade (TUG e Iluminação)
- [ ] **UI:** Modal de edição com campo de motivo + badge [A]/[M]
- [ ] **Reabrir edição:** Verificar se campo reabre preenchido quando origem = MANUAL
- [ ] **Testes:** Test cases para fórmulas F-03 a F-06 (TUG), F-07-QTD e F-08 (Iluminação)
- [ ] **Validação:** Implementar validação de quantidade mínima (≥1)
- [ ] **Documentação:** Atualizar REFERENCIA-INTEGRAL-SISTEMA.md com F-07-QTD

---

## 8. Referências Normativas

| Fórmula | Descrição | Fonte NBR | Status |
|---|---|---|---|
| **F-01** | Área = L × C | NBR 5410 item 9.5.2.1.1 | ✓ Implementada |
| **F-02** | Perímetro = 2(L+C) - excluído | NBR 5410 item 9.5.2.1.1 | ✓ Implementada |
| **F-03** | TUG CAT-A: ceil(P/5) mín. 1 | NBR 5410 item 9.5.2.2.1.c | ✓ Implementada |
| **F-04a** | TUG CAT-B (cozinha): ceil(P/3.5) | NBR 5410 item 9.5.2.2.1.a | ✓ Implementada |
| **F-04b** | TUG CAT-B (banheiro): mín. 1, 600 VA | NBR 5410 item 9.5.2.2.1.b | ✓ Implementada |
| **F-06** | TUG CAT-C: A>6 → ceil(P/5); senão 1 | NBR 5410 item 9.5.2.2.1.d | ✓ Implementada |
| **F-07** | Iluminação: mín. 1 por dependência | NBR 5410 item 9.5.2.1.2 | ✓ Implementada |
| **F-07-QTD** | Iluminação: A≤6 → 1; A>6 → 1+floor((A-6)/4) | NBR 5410 item 9.5.2.1.2 (interpretação) | 🔲 **NOVA — Proposta** |
| **F-08** | Iluminação: A≤6 → 100VA; A>6 → 100+60×floor((A-6)/4) | NBR 5410 item 9.5.2.1.2 | ✓ Implementada |

---

## 9. Referências Cruzadas

- **REFERENCIA-INTEGRAL-SISTEMA.md:** Seção 4.2 (Fórmulas NBR)
- **NBR5410-Estados-Fluxo-Validacao.md:** Rastreamento de origem no fluxo de estados
- **NBR5410-Escopos-Analise-Dependencias.md:** Escopo "Sem resultado calculado" para identificar falta de cálculo

---

**Documento versão:** 1.0  
**Data de criação:** 2026-07-05  
**Próxima revisão:** Após implementação de F-07-QTD e integração com Automático/Manual  
**Responsável:** Time técnico SIE NBR5410  
**Status:** Pronto para desenvolvimento
