# Estados de Validação — Sistema SIE NBR5410

**Documento:** Análise estruturada dos estados de conformidade para circuitos, grupos e proteções  
**Data:** 2026-07-05  
**Contexto:** Auditoria técnica EDP V09 — Projeto SIE `feature/nbr5410-conformidade-closeout`

---

## Índice de Estados

1. [Todos os estados](#1-todos-os-estados) — Seletor principal
2. [Pendentes](#2-pendentes) — In-Queue, aguardando processamento
3. [Incompletas](#3-incompletas) — Dados faltantes ou inválidos
4. [Calculadas](#4-calculadas) — Processadas, valores aplicados
5. [Editadas manualmente](#5-editadas-manualmente) — Manual override, rastreado
6. [Exigem validação técnica](#6-exigem-validação-técnica) — Pending review, aprovação humana
7. [Validadas](#7-validadas) — Aprovadas, conforme NBR5410
8. [Erros](#8-erros) — Falha, bloqueado até correção

---

## 1. Todos os estados

### Significado
Filtro que mostra registros em qualquer estado, sem restrições.

### Função no fluxo
- Visão consolidada de todo o volume de dados
- Relatórios gerenciais e de auditoria
- Análise de distribuição entre estados

### Quando usar
- **Auditoria geral:** Verificar conformidade global
- **Relatórios executivos:** Volume total vs. conformidade
- **Análise de impacto:** Mudanças estruturais que afetam todos os registros

### Exemplo SIE
Visualizar todos os 1.200+ circuitos cadastrados, independentemente de seu estado de conformidade com EDP V09.

---

## 2. Pendentes

### Significado
Dados recebidos mas ainda não processados. Estado inicial no fluxo.

### Características
- ✓ Estrutura básica válida
- ✗ Sem cálculos aplicados
- ✗ Sem validação técnica realizada
- ⏳ Aguardando início da máquina de processamento

### Próximo passo
Processamento automático (cálculo de parâmetros NBR) ou validação manual se detectados erros estruturais.

### Exemplo SIE
- Circuitos importados de planilha EDP que chegaram ao banco de dados
- Grupos novos cadastrados manualmente, aguardando primeira análise
- Dados que sofreram re-importação após correção de fornecedor

### Ação esperada
```
[Pendentes] → Validar estrutura → [Incompletas] ou [Calculadas]
```

---

## 3. Incompletas

### Significado
Dados faltam campos obrigatórios ou falharam em validações iniciais estruturais.

### Bloqueadores
- Campos obrigatórios vazios (condutor, proteção, tensão)
- Valores fora de range (seção negativa, corrente zero)
- Incongruências internas (grupo sem categoria, categoria sem tensão)
- Relacionamentos quebrados (referência a proteção inexistente)

### Rastreamento
Cada erro deve ser registrado com:
- Campo faltante ou inválido
- Motivo (tipo de erro)
- Quem e quando detectou

### Exemplo SIE
- Grupos sem descrição → Falta nome da distribuição
- Circuitos sem tipo (TUG/TUE/Iluminação) → Impossível aplicar fórmula NBR
- Tabelas 001-002 com valores `null` → Queda de tensão não calculável
- Dispositivo de proteção referenciado mas não cadastrado → Quebra de integridade

### Ação esperada
```
[Incompletas] ← Recoleta de dados / Validação de campos / Ajustes estruturais
   ↓
[Calculadas]
```

### Impacto
Bloqueia passagem para cálculo automático. Alto volume em **Incompletas** indica problema de importação ou coleta de dados.

---

## 4. Calculadas

### Significado
Dados completos, processados com sucesso. Parâmetros NBR5410 foram aplicados.

### Valores calculados (exemplos)
- Queda de tensão (F-07: percentual e volts)
- Corrente de projeto (F-03 a F-06 para TUG; iluminação)
- Seção de condutor recomendada (tabelas ABNT)
- Corrente de curto-circuito (para análise de proteção)
- Categoria de fornecimento (U/D/T com base em demanda + tipo de rede)

### Características pós-cálculo
- ✓ Todos os parâmetros automáticos preenchidos
- ✓ Pronto para validação técnica manual
- ⚠️ Pode conter exceções (valores ajustados manualmente depois)
- ⏳ Aguardando revisão humana antes de aprovação final

### Exemplo SIE
- Circuito TUG com corrente calculada = 16A → Proteção min. 20A (norma)
- Grupo iluminação: potência = 2.000 W → Seção condutor = 2,5 mm²
- Demanda total = 45 kW, rede trifásica → Categoria D (de acordo V09)

### Fluxo sequencial
```
[Calculadas] → [Editadas manualmente] ou [Exigem validação técnica]
```

---

## 5. Editadas manualmente

### Significado
Valores foram alterados **após cálculo automático** por decisão técnica ou exceção justificada.

### Quando ocorre
- Especialista EDP aplicou correção em campo (situação real diferente do projeto)
- Norma ou código permitiu exceção (ex: menor seção em banco de dutosédificado)
- Ajuste por restrição física (ex: condutor maior não cabe no eletroduto)
- Padronização de projeto (ex: usar sempre proteção de mesmo tipo)

### Rastreabilidade obrigatória
Cada edição manual **DEVE** incluir:
- Quem editou (usuário)
- Quando (data/hora)
- Por quê (anotação técnica ou código de exceção)
- Qual valor foi alterado (antes → depois)

### Exemplo SIE
| Campo | Automático | Manual | Motivo |
|-------|-----------|--------|--------|
| Seção condutor | 2,5 mm² | 4 mm² | Eletroduto compartilhado: agrupamento 3+N |
| Proteção | Disjuntor 20A | Disjuntor 25A | Redução de queda tensão: pré-dimesionado para 1% |
| Categoria | U | D | Cliente solicitou demanda contratada maior (futuro) |

### Impacto
- ✓ Aumenta confiança na conformidade (decisão técnica rastreada)
- ⚠️ Requer validação técnica extra rigorosa
- ❌ Sem anotação = auditoria falha

### Fluxo sequencial
```
[Calculadas] → [Editadas manualmente] → [Exigem validação técnica]
```

---

## 6. Exigem validação técnica

### Significado
Dados estão corretos estruturalmente e calculados, mas precisam de aprovação **humana** de especialista técnico.

### Validador esperado
- Engenheiro eletricista especializado em NBR5410
- Ou revisor EDP/concessionária (para dados concessionária)
- Conhecimento de exceções e normas vigentes

### Critérios de validação
- Conformidade real com NBR5410 (não apenas algoritmo)
- Adequação ao projeto específico da instalação
- Viabilidade técnica (disponibilidade de materiais, restrições de campo)
- Consistência com padrão EDP (se aplicável)
- Alinhamento com decisões já validadas no mesmo projeto

### Checklist de validação típica
- [ ] Todos os valores dentro de ranges normativos
- [ ] Seção de condutor adequada para corrente de projeto
- [ ] Proteção selecionada conforme tabela ABNT
- [ ] Queda de tensão dentro de limites (3% para subgrupos, 5% geral)
- [ ] Corrente de curto-circuito > corrente de atuação da proteção
- [ ] Tipo de rede e categoria de fornecimento alinhados
- [ ] Se manual: anotação técnica presente e válida

### Exemplo SIE
**Esperando validação:**
- Circuito TUE com hidromassagem (I-04): desagregação resistência + motor
- Grupo genérico (I-08): roteamento tipo→grupo correto?
- Tabela 001 com queda de tensão recalculada: compatível com versão V09?

### Tempo médio
Depende de volume e complexidade — tipicamente 2-5 dias úteis em equipes com especialista dedicado.

### Fluxo sequencial
```
[Exigem validação técnica]
   ↓ [Aprovado]        ↓ [Reprovado]
[Validadas]           [Erros] ← Diagnóstico, retry
```

---

## 7. Validadas

### Significado
Passou em todas as validações técnicas. **Estado final de conformidade.**

### Garantias
- ✓ Conforme NBR5410 vigente (EDP V09 ou superior)
- ✓ Aprovado por especialista técnico
- ✓ Rastreado (histórico de edições, validador, data)
- ✓ Pronto para implementação ou documentação oficial

### Uso permitido
- Referência em projetos de expansão
- Documentação técnica (ART, RRT)
- Cálculos subsequentes (não requer re-validação)
- Relatórios de conformidade para órgãos fiscalizadores

### Exemplo SIE
- Circuitos e grupos aprovados pelo especialista EDP
- Tabelas 001-002 conferidas e alinhadas com V09
- Grupos de proteção com distribuição validada
- Hidromassagem com desagregação resistência+motor finalizada (I-04 resolvido)

### Impacto no projeto
Alto volume em **Validadas** = Projeto pronto para fechamento de conformidade.

### Fluxo sequencial
```
[Validadas] → Uso em produção / Documentação oficial
```

---

## 8. Erros

### Significado
Dados falharam em alguma etapa (validação estrutural, cálculo, ou revisão técnica).

### Origens possíveis
| Origem | Exemplo |
|--------|---------|
| **Estrutural** | Campo inválido não detectado em importação |
| **Cálculo** | Overflow matemático, referência quebrada |
| **Validação técnica** | Valor fora de range normativo, incompatibilidade |
| **Rastreamento** | Histórico corrompido, anotação faltante |

### Bloqueio
Registro **não pode avançar** até correção. Ativa flag de auditoria.

### Diagnóstico obrigatório
Cada erro deve incluir:
- Código de erro (E-001, E-002, etc.)
- Descrição técnica do problema
- Sugestão de correção (se automática)
- Passos para resolver (se manual)

### Exemplo SIE (da auditoria 2026-06-21)
| ID | Erro | Causa | Correção |
|----|----|-------|----------|
| I-01 | Versão `.data.json` = v06 | Dados desatualizado | Atualizar para v09 |
| I-02 | Categoria selecionada apenas por carga | Algoritmo incompleto | Incluir demanda + tipo rede + local |
| I-03 | Documentação seção 7.1 com grupos errados | Divergência docs/código | Corrigir REFERENCIA-INTEGRAL-SISTEMA.md |
| I-04 | Hidromassagem FP único | Falta desagregação | Separar resistência (FP=1.0) + motor (FP=tabela) |

### Ação esperada
```
[Erros] ← Diagnóstico → Tipo de erro
   ├─ Estrutural: Retorna a [Incompletas] → Recoleta
   ├─ Cálculo: Retorna a [Pendentes] → Reprocessamento
   └─ Validação: Volta a especialista → [Exigem validação técnica]
```

### Taxa de sucesso
Monitorar: `(Validadas) / (Validadas + Erros)` = Taxa de conformidade.  
Meta para SIE: **≥95%** ao fim do closeout.

---

## Máquina de Estados — Diagrama Completo

```
                    ┌─────────────────────────────┐
                    │  Todos os estados (filtro)  │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      PENDENTES              │
                    │   (In-Queue, recebido)     │
                    └──────────────┬──────────────┘
                                   │
                      ┌────────────┴────────────┐
                      │                         │
                      ▼                         ▼
          ┌─────────────────────┐  ┌─────────────────────┐
          │   INCOMPLETAS       │  │   CALCULADAS        │
          │ (Falta dados/inválid) │  │ (Parâmetros NBR)   │
          │  ← Recoleta dados   │  │  ← Automático       │
          └─────────────────────┘  └──────────┬──────────┘
                      │                       │
                      └───────────┬───────────┘
                                  │
                      ┌───────────▼───────────┐
                      │ EDITADAS MANUALMENTE  │
                      │ (Override rastreado)  │
                      └───────────┬───────────┘
                                  │
                      ┌───────────▼─────────────────────┐
                      │ EXIGEM VALIDAÇÃO TÉCNICA        │
                      │ (Pending review, aprovação)     │
                      └───────────┬─────────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
          ┌─────────▼────────┐      ┌──────────▼──────────┐
          │   VALIDADAS      │      │      ERROS          │
          │ (✓ Conforme)     │      │ (✗ Falha, bloqueado)│
          │ → Produção       │      │ → Diagnóstico       │
          └──────────────────┘      └─────────────────────┘
```

---

## Fluxos Esperados (Happy Path)

### Fluxo 1: Importação sem problemas
```
Pendentes → Calculadas → Exigem validação técnica → Validadas ✓
```
**Duração típica:** 1-2 dias (cálculo + validação)

### Fluxo 2: Edição técnica + validação
```
Pendentes → Calculadas → Editadas manualmente → Exigem validação técnica → Validadas ✓
```
**Duração típica:** 2-3 dias (cálculo + edição + validação)

### Fluxo 3: Recoleta após falha estrutural
```
Pendentes → Incompletas ← (recoleta de dados) → Calculadas → ... → Validadas ✓
```
**Duração típica:** 3-5 dias (aguarda cliente/técnico fornecer dados faltantes)

### Fluxo 4: Erro em validação técnica (retry)
```
... → Exigem validação técnica → Erros ← (especialista diagnostica)
  └─→ Incompletas (se estrutural) ← Recoleta → Calculadas → ...
  └─→ Pendentes (se cálculo) ← Reprocessa → Calculadas → ...
```
**Duração típica:** 2-4 dias extra (investigação + correção)

---

## Métricas e KPIs

### Distribuição ideal (por fase)
| Estado | % Esperado | Alerta se |
|--------|-----------|----------|
| Validadas | ≥95% | <90% |
| Erros | ≤3% | >5% |
| Exigem validação | ≤2% | >5% (gargalo validador) |
| Incompletas | ≤0,5% | >2% (problema qualidade dados) |
| Pendentes | ~0% | >1% (gargalo processador) |

### Indicadores por fase
- **Taxa de conversão Pendentes→Calculadas:** (Calculadas - Editadas) / Pendentes
- **Taxa de validação:** Validadas / (Validadas + Erros)
- **Taxa de retrabalho:** Erros / Total
- **Tempo médio em Exigem validação:** Indica eficiência do validador

---

## Aplicação Prática — Auditoria SIE NBR5410

### Contexto
Projeto `feature/nbr5410-conformidade-closeout` encontrou **4 incongruências críticas** em 2026-06-21.

### Mapeamento de correções
| Incongruência | Estado atual | Estado alvo | Ação |
|---|---|---|---|
| **I-01:** v06 vs v09 | Validadas (incorreto) | Erros → Recalcular | Re-importar com v09 |
| **I-02:** Categoria incompleta | Calculadas (parcial) | Editadas manualmente | Incluir demanda+rede+local |
| **I-03:** Docs diverge código | Validadas (docs) | Validadas (código) | Atualizar REFERENCIA-INTEGRAL |
| **I-04:** Hidromassagem FP | Validadas (incorreto) | Editadas manualmente | Desagregar resistência+motor |

### Projeto
```
SIE CLOSEOUT (2026-07-XX)
├─ [Pendentes]        0
├─ [Incompletas]      12 (grupos genéricos, i-08)
├─ [Calculadas]       200 (esperando revisão I-01 a I-04)
├─ [Editadas man.]    50 (correções em andamento)
├─ [Exigem valid.]    450 (gargalo: aguarda especialista)
├─ [Validadas]        680 (aprovadas, conforme v09)
└─ [Erros]            8 (diagnóstico em andamento)

Total: 1.400 registros
Conformidade atual: 680 / 1.400 = 48,5%
Meta: 1.330 / 1.400 = 95% (até 2026-07-30)
```

---

## Referências

- **NBR 5410:2015** — Instalações elétricas de baixa tensão
- **EDP V09** — Catálogo de especificações (vigente desde 14/04/2026)
- **Auditoria:** `docs/research/2026-06-21-auditoria-prompt-nbr5410-edp-sp/ANALISE-PROMPT-PLANO-CORRECAO.md`
- **Configuração SIE:** `REFERENCIA-INTEGRAL-SISTEMA.md` (Seção 7.1 — Grupos EDP)

---

**Documento versão:** 1.0  
**Próxima revisão:** 2026-07-30 (após implementação de I-01 a I-04)  
**Responsável:** Tim técnico SIE NBR5410
