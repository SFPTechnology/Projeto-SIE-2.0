# Recomendações para o Projeto SIE

**Base:** Análise do Prompt de Auditoria NBR5410/EDP v2.0  
**Data:** 2026-06-21

---

## 1. Usar o prompt diretamente como checklist de QA do SIE

O prompt está estruturado como framework de auditoria de terceiros. Para o projeto SIE, ele funciona como **especificação de conformidade** — cada eixo E1–E16 mapeia para um módulo do sistema que deve ser validado.

Recomendação: mapear os 16 eixos para os módulos do SIE e criar testes automatizados usando os Casos 1–5 como fixtures de teste.

## 2. Implementar os 5 casos de teste como fixtures de regressão

Os casos de teste da Seção 12 têm valores esperados explícitos. São candidatos diretos a testes unitários:

| Caso | Input | Output esperado |
|---|---|---|
| Quarto 9m² | área=9, tipo=quarto | il=100VA, TUG=3pts, P=300VA |
| Sala 12m² | área=12, perímetro=14, tipo=sala | il=160VA, TUG=3pts, P=300VA |
| Cozinha 12m² | área=12, perímetro=14, tipo=cozinha | il=160VA, TUG=4pts, P=1900VA |
| Banheiro 3m² | área=3, tipo=banheiro | il=100VA, TUG=1pt, P=600VA |
| Chuveiro 220V | P=5400W, V=220V | I=24,55A, grupo=b |

## 3. Corrigir lacuna da queda de tensão bifásica (I-02)

Para instalações Categoria D (bifásica FFN), o SIE deve implementar e exibir a fórmula correta de queda de tensão. A ausência desta fórmula no prompt sinaliza que sistemas existentes podem ter esta lacuna.

Prioridade: ALTA — afeta instalações entre 12–25 kW (faixa mais comum de comércio de pequeno porte).

## 4. Implementar regra de dimensionamento do condutor PE

Regra mínima a implementar no SIE:
- Seção fase ≤ 16 mm² → PE = fase
- 16 < seção fase ≤ 35 mm² → PE = 16 mm²
- Seção fase > 35 mm² → PE = fase/2
- [VERIFICAR NBR 5410 Tabela 54.2 para material diferente de cobre]

## 5. Declarar escopo explícito de SPDA e GD na UI

Para evitar que usuários do SIE interpretem que o sistema cobre SPDA e GD, a interface deve exibir aviso claro:
- "Este sistema não calcula SPDA. Consulte NBR 5419."
- "Este sistema não cobre microgeração distribuída. Consulte ANEEL REN vigente."

## 6. Adicionar caso de teste numérico para demanda EDP (Caso 7)

O Caso 7 do prompt é apenas um roteiro sem valores. Para o SIE, criar pelo menos um caso de teste numérico completo com grupos a+b+d+f+g e verificação de categoria resultante.

Sugestão de caso:
```
Carga instalada grupo a: 3,5 kW → FD = 0,59 → demanda a = 2,065 kW
Chuveiro (grupo b): 5,4 kW → FD = 1,00 → demanda b = 5,4 kW
Micro-ondas (grupo d): 1,2 kW → FD = 0,70 → demanda d = 0,84 kW [VERIFICAR]
Ar-cond. 12.000 BTU (grupo f): 1,32 kW → FD = 1,00 → demanda f = 1,32 kW
Demanda total = 2,065 + 5,4 + 0,84 + 1,32 = 9,625 kW → verificar categoria
```
