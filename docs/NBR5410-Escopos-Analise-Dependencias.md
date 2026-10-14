# Escopos de Análise de Dependências — Sistema SIE NBR5410

**Documento:** Análise estruturada dos escopos de filtro para visualização e validação de dependências  
**Data:** 2026-07-05  
**Contexto:** Auditoria técnica EDP V09 — Projeto SIE `feature/nbr5410-conformidade-closeout`

---

## Índice de Escopos

1. [Todas as dependências](#1-todas-as-dependências) — Seletor principal, sem filtros
2. [Com pendências ou alertas](#2-com-pendências-ou-alertas) — Registros bloqueados ou com avisos
3. [Com cargas adicionais](#3-com-cargas-adicionais) — Deps extras além da especificação
4. [Sem resultado calculado](#4-sem-resultado-calculado) — Dados OK, mas cálculo não feito
5. [Automático](#5-automático) — Processado por máquina, sem intervenção humana

---

## 1. Todas as dependências

### Significado
Filtro que mostra **100% das relações e dependências** do projeto, sem restrições.

### Escopo completo
- ✓ Dependências diretas (circuito → grupo → proteção)
- ✓ Dependências indiretas (mudança em tabela afeta todos os cálculos)
- ✓ Referências cruzadas (grupo A compartilha barramento com B)
- ✓ Alertas técnicos (todos, críticos e avisos)
- ✓ Cargas normais e cargas adicionais
- ✓ Resultados calculados e não calculados

### Características
- Visão holística da arquitetura de dados
- Grafo completo de dependências
- Acesso irrestrito a todas as relações

### Uso principal
- **Auditoria arquitetural:** Verificar se tudo está conectado corretamente
- **Análise de impacto sistêmico:** Mudança em um ponto afeta onde mais?
- **Planejamento de refatoração:** Quais componentes se mexem juntos?
- **Conformidade geral:** Visualizar cobertura de validação
- **Documentação técnica:** Gerar diagramas completos

### Quando usar
- Avaliação geral de arquitetura
- Reunião de planejamento (full picture)
- Relatório executivo (visão 10.000 pés)
- Análise de risco de mudança estrutural
- Onboarding de novo técnico (entender grafo)

### Métricas típicas (SIE)
```
Todas as dependências:
├─ 1.400 registros (circuitos + grupos + proteções)
├─ ~3.200 dependências diretas (circuit→group, group→protection)
├─ ~8.500 dependências indiretas (via tabelas compartilhadas)
├─ 680 validadas (48,5%)
├─ 450 exigem validação (32,1%)
├─ 8 em erro (0,6%)
└─ Taxa conformidade: 95% meta
```

### Exemplo de análise
```
"Se eu atualizar tabela-005.json de v06 para v09, o que quebra?"
→ Escopo: Todas as dependências
→ Impacto: 1.200 circuitos dependem dessa tabela
→ Decisão: Reprocessar todos com v09 (I-01 da auditoria)
```

### Limitação
Volume grande pode dificultar visualização. Para foco, use escopos específicos.

---

## 2. Com pendências ou alertas

### Significado
Mostra **APENAS registros que têm dependências bloqueadas ou avisos técnicos**.

### O que são "pendências"
Bloqueadores que impedem avanço:

| Tipo | Exemplo | Impacto |
|------|---------|--------|
| **Referência pendente** | Grupo referencia proteção em estado Pendentes | Cálculo não pode rodar |
| **Pré-requisito incompleto** | Circuito aguarda desagregação de outro (I-04) | Validação não pode rodar |
| **Falha cascata** | Tabela com erro bloqueia 200 cálculos | Reprocessamento necessário |
| **Flag de bloqueio** | Registro marcado como "não processar até..." | Interpretação manual necessária |

### O que são "alertas"
Avisos não-bloqueadores, mas requerem atenção:

| Tipo | Exemplo | Severidade |
|------|---------|-----------|
| **Aviso normativo** | Queda tensão = 3,5% (limite = 3%) | 🟡 Atenção |
| **Incongruência padrão** | Proteção fora de tabela EDP recomendada | 🟡 Atenção |
| **Depreciação** | Usando versão v06 em sistema v09 | 🔴 Crítico |
| **Risco conformidade** | FP incorreto para hidromassagem | 🔴 Crítico |
| **Recomendação não seguida** | Seção < seção mínima recomendada | 🟡 Atenção |
| **Divergência docs/código** | Documentação contradiz implementação | 🔴 Crítico |

### Composição de pendências
```
Registros com pendências = Incompletas + Erros + Exigem validação + Editadas manualmente
(Estados que indicam algo não está resolvido)
```

### Uso principal
- **Triage:** "Quais são os críticos que precisam atenção agora?"
- **Sprint planning:** "O que bloqueia outras tarefas?"
- **QA focus:** "Onde estão os pontos de risco?"
- **Escalação:** "O que não pode avançar sem help?"

### Quando usar
- Reunião daily (status de blockers)
- Planejamento de sprint (priorização)
- QA gate (focar nos alerts)
- Auditoria de risco (vulnerabilidades)
- Análise de dependência (cascata de bloqueios)

### Taxa esperada
- **Saudável:** 5-15% do total
- **Atenção:** 15-25% (muitas pendências)
- **Crítico:** >25% (projeto bloqueado)

### Exemplo SIE — Pendências
```
Com pendências ou alertas (2026-07-05):

🔴 CRÍTICAS:
├─ Circuito TUE-053: Aguarda desagregação hidromassagem (I-04)
├─ Tabela 001: 12 registros com versão v06 (I-01)
├─ Grupo Genérico-8: Roteamento não validado (I-08)
└─ Hidromassagem: FP único, requer motor+resistência (I-04)

🟡 ATENÇÃO:
├─ 8 circuitos com queda tensão > 3%
├─ 5 grupos com proteção fora da tabela EDP
├─ 20 registros com FP incorreto
└─ Docs vs código: REFERENCIA-INTEGRAL (seção 7.1)

Total: 45 registros (~3,2% do sistema)
```

### Exemplo SIE — Alertas
```
Com alertas (filtrando apenas avisos não-bloqueadores):

Status quo (antes da correção):
├─ Versão v06 vs v09: 200 registros (I-01)
├─ Categoria incompleta: 450 registros (I-02)
├─ Docs divergente: 1 seção (I-03)
└─ Hidromassagem FP: 8 registros (I-04)

Total: 659 registros com alert (~47% do sistema)
```

### Diagrama de fluxo
```
[Registro] 
   ↓
Tem pendência? 
   ├─ SIM → [Mostra neste escopo] → Ação necessária
   └─ NÃO → [Não mostra] → Segue normalmente
   
Tem alerta?
   ├─ SIM (crítico) → [Mostra] → Revisão técnica
   ├─ SIM (atenção) → [Mostra] → Monitorar
   └─ NÃO → [Não mostra] → OK
```

---

## 3. Com cargas adicionais

### Significado
Mostra registros que têm **dependências extras além da especificação original**.

### O que são "cargas adicionais"

Fatores que adicionam complexidade técnica e dependência:

| Tipo de carga | Descrição | Impacto técnico |
|---|---|---|
| **Agrupamento de circuitos** | Múltiplos circuitos no mesmo eletroduto | Reduz capacidade de cada um (fator de agrupamento) |
| **Compartilhamento de proteção** | Proteção protege 2+ circuitos | Uma falha afeta vários; coordenação necessária |
| **Barramento compartilhado** | Grupos em paralelo no mesmo bus | Distribuição de carga desigual possível |
| **Fusão de grupos** | Múltiplos grupos combinados em um | Aumento de complexidade, interdependência |
| **Redundância/reserva** | Capacidade extra instalada no ponto | Termal crítica, espaço físico limitado |
| **Influência térmica** | Circuitos próximos aumentam temperatura | Reduz capacidade nominal dos condutores |
| **Dependência de coordenação** | Proteção A coordena com proteção B | Mudança em um afeta outro; validação extra |
| **Revisão manual adicional** | Especialista adicionou restrições | Mais parâmetros para manter consistentes |

### Por que rastrear
- ✓ Aumentam complexidade de validação
- ✓ Mudança em um circuito pode quebrar todo o grupo
- ✓ Risco de incumprimento normativo maior
- ✓ Importante para auditoria de conformidade
- ✓ Necessário documentar em ART/RRT
- ✓ Afetam manutenção futura

### Uso principal
- **Validação rigorosa:** Requer especial atenção
- **Análise de robustez:** O sistema agüenta as dependências extras?
- **Preparação de ART/RRT:** Documentar todas as deps para órgão fiscalizador
- **Análise de impacto:** Mudança aqui afeta outras? Cascata?
- **Manutenção preventiva:** Identificar pontos críticos de falha

### Quando usar
- Antes de liberar circuitos para produção
- Ao revisar mudanças em circuitos críticos
- Preparação de documentação técnica oficial
- Análise de impacto antes de refatoração
- Auditoria de confiabilidade (FMEA, análise de risco)
- Planejamento de ampliação futura

### Taxa esperada
- **Tipicamente:** 20-40% (comum em instalações reais)
- **Simples (casa pequena):** 5-10%
- **Complexa (indústria):** 60-80%

### Exemplo SIE — Cargas adicionais
```
Com cargas adicionais (2026-07-05):

AGRUPAMENTO DE CIRCUITOS:
├─ Eletroduto-A: Circuitos TUG-01, TUG-02, TUG-03 agrupados
│  → Fator agrupamento = 0,80 (reduz capacidade em 20%)
│  → Impacto: Seção de cada um deve aumentar
│
├─ Eletroduto-B: 5 circuitos TUE agrupados
│  → Fator agrupamento = 0,70 (reduz em 30%)
│  → Impacto: Crítico, reque validação
│
└─ Eletroduto-C: 2 circuitos (iluminação + força)
   → Fator agrupamento = 0,85 (reduz em 15%)
   → Impacto: Aceitável com documentação

COMPARTILHAMENTO DE PROTEÇÃO:
├─ Proteção-A: Protege 5 TUGs
│  → Coordenação necessária
│  → Dependência cruzada: mudança em 1 afeta 5
│
└─ Proteção-B: Protege 3 TUEs
   → Motor + resistência + força
   → Requer validação de seletividade

INFLUÊNCIA TÉRMICA:
├─ Cabine de climatização: 4 condutores de cobre em paralelo
│  → Aumento de temperatura = reduz capacidade
│  → Necessário fator de temperatura
│
└─ Eletrocalefação: Circuitos lado a lado, calor irradiado
   → Reduz capacidade dos vizinhos
   → Requer verificação periódica

Total: 180 registros com cargas adicionais (~12,9% do sistema)
Risco: ALTO (maior complexidade de validação)
```

### Checklist de validação (Com cargas adicionais)
```
[ ] Fator de agrupamento aplicado corretamente
[ ] Seção de condutor recalculada com fator
[ ] Proteção dimensionada para TODAS as cargas compartilhadas
[ ] Coordenação entre proteções verificada
[ ] Temperatura ambiente considerada
[ ] Queda de tensão recalculada
[ ] Documentação atualizada com deps
[ ] Especialista EDP validou (crítico para cargas adicionais)
```

---

## 4. Sem resultado calculado

### Significado
Mostra registros que **ainda não têm resultado de cálculo**, apesar de dados estruturais estarem OK.

### O que é "sem resultado calculado"

| Aspecto | Status |
|--------|--------|
| **Estrutura** | ✓ Válida (todos os campos obrigatórios preenchidos) |
| **Resultado de cálculo** | ✗ Não existe |
| **Por quê falta** | Processador não rodou, foi skipped, ou falhou |
| **Tipo de registro** | Pode estar em estado Pendentes ou outro |

### Diferença vs. Estados
```
Incompletas:
├─ Dados faltam
├─ Não pode ser calculado
└─ Recoleta necessária

Sem resultado calculado:
├─ Dados OK
├─ Não foi processado
└─ Processamento necessário
```

### Razões possíveis

| Razão | Evidência | Ação |
|-------|-----------|------|
| **Importação recent** | Timestamp recente | Aguardar processamento (batch job), ou disparar manualmente |
| **Processador bloqueado** | Timeout/erro temporário | Reprocessar lote, verificar logs |
| **Registro skippado** | Flag `skip_calculation=true` | Revisar por quê foi skipped; liberar se OK |
| **Fila congestionada** | Backlog alto no processador | Aumentar capacidade, paralelizar, ou fazer manualmente |
| **Tipo desconhecido** | `tue_generico` não em tabela | Adicionar tipo à tabela ou documentar exceção (I-08) |
| **Erro silencioso** | Processador falhou, sem log | Verificar error log, corrigir, reprocessar |
| **Batch job com atraso** | Job scheduled mas não rodou | Disparar job manualmente |

### Uso principal
- **Monitoramento de saúde:** O processador está funcionando?
- **Triage de importação:** Quantos ainda aguardam processamento?
- **Reprocessamento:** Força cálculo em lote grande
- **Debugging:** "Por que esse circuito não tem resultado?"
- **SLA tracking:** % de registros processados vs. tempo

### Quando usar
- Monitoramento contínuo (dashboard de saúde)
- Pós-importação (aceitar? quantos faltam?)
- Pós-mudança de versão (reprocessamento necessário)
- Troubleshooting de circuitos específicos
- Relatório de throughput

### Métrica de saúde
```
Taxa de registros SEM cálculo:

<2% do total     = NORMAL   (processador em dia)
2-5%             = ATENÇÃO  (revisar backlog)
>5%              = CRÍTICO  (processador parado?)
```

### Exemplo SIE — Sem resultado calculado
```
Sem resultado calculado (2026-07-05):

IMPORTAÇÃO RECENT (últimas 24h):
├─ Lote EDP tabela-005: 80 registros (importado ontem 23:00)
│  Status: Aguardando batch job das 08:00 → OK
│
└─ Revisão manual: 15 registros (entrada via UI hoje)
   Status: Disparar processador manualmente → TBD

PROCESSADOR CONGESTIONADO:
├─ Backlog: 30 registros
│  Tempo aguardando: 6 horas
│  Status: Normal (job rodar tonight) → MONITOR
│
└─ Fila: 5 registros (erro temporiário)
   Status: Reprocessar → AÇÃO

TIPO NÃO RECONHECIDO:
├─ tue_generico: 12 registros
│  Status: Skipped pelo processador
│  Razão: Tipo não em tabela EDP V09 (I-08)
│  Ação: Adicionar tipo ou documentar exceção → BLOCKER

BATCH JOB SEM RESULTADO:
├─ Job 20260704-batch-001: Iniciado 04:30, status?
│  Status: TBD (verificar logs) → INVESTIGATE
│
└─ Job 20260703-batch-002: Falhado
   Logs: "Memory limit exceeded"
   Status: Reprocessar com chunks menores → AÇÃO

TOTAIS:
├─ Sem resultado calculado: 42 registros (~3%)
├─ Esperado normal: <1% em steady-state
├─ Status: ATENÇÃO (acima do normal)
└─ Ação: Investigar processador, disparar jobs faltando
```

### Fluxo de resolução
```
Registro [Sem resultado calculado]
   ├─ Investigar razão
   ├─ Se import recent → Aguardar batch job
   ├─ Se processador bloqueado → Disparar manualmente
   ├─ Se tipo desconhecido → Adicionar tipo (I-08) ou documentar
   ├─ Se erro → Corrigir root cause, reprocessar
   └─ Resultado: [Calculadas] ou [Erros] ou [Incompletas]
```

---

## 5. Automático

### Significado
Mostra registros que foram **processados de forma automática** por máquina, sem intervenção humana.

### O que é "automático"

| Aspecto | Descrição |
|--------|-----------|
| **Origem** | Resultado gerado por algoritmo/máquina de cálculo |
| **Intervenção humana** | NENHUMA após processamento |
| **Flag de override** | Não tem `edited_manually=true` |
| **Processo** | Import → Validação automática → Cálculo → Resultado |
| **Confiabilidade** | Algoritmicamente correto, mas não validado por especialista ainda |

### Diferença vs. Estados
```
Calculadas:
├─ Pode ser automático (puro algoritmo)
└─ Pode ser com edição manual depois

Automático:
├─ Definitivamente SEM edição manual
├─ Resultado algoritmo puro
└─ Aguardando validação técnica
```

### Composição esperada
```
Registros totais = Automático + Editados manualmente

Exemplo SIE:
├─ Automático: 1.100 (~78%)
├─ Editados manualmente: 300 (~22%)
└─ Total: 1.400

Interpretação:
├─ Algoritmo é confiável (78% não precisa edição)
├─ 22% requer ajuste técnico (normal para instalações reais)
└─ Taxa edição: 22% = dentro do esperado
```

### Uso principal
- **Análise de acurácia:** Qual é a taxa de erro do algoritmo?
- **Validação de modelo:** Necessário ajustar fórmulas?
- **QA focus:** Focar validação onde algoritmo tem dúvida
- **Comparação:** Automático vs. manual, qual a diferença?
- **Diagnóstico:** Se muita edição, por que?

### Quando usar
- Avaliação de modelo (acurácia)
- Comparação automático vs. manual
- Análise de viés/erro sistemático
- Identificar áreas com baixa confiança do algoritmo
- QA strategy (onde focar validação?)

### Taxa esperada por tipo

| Tipo | % Automático OK | % Requer edição | Interpretação |
|------|-----------------|-----------------|---------------|
| **TUG** | 95-98% | 2-5% | Alto, poucos ajustes |
| **TUE** | 85-92% | 8-15% | Médio, algumas exceções |
| **Iluminação** | 98-99% | 1-2% | Muito alto, fórmula simples |
| **Proteção** | 80-88% | 12-20% | Baixo, muitos ajustes |
| **Categoria U/D/T** | 60-70% | 30-40% | Muito baixo, requer V09 (I-02) |

### Exemplo SIE — Análise de automático
```
Distribuição automático vs. manual (2026-07-05):

ANTES DA AUDITORIA (com bugs):
├─ Automático: 900 registros (64%)
├─ Editados manualmente: 500 registros (36%)
└─ Taxa edição: 36% ← MUITO ALTA (sinais de problema no algoritmo)

ANÁLISE DO PROBLEMA:
├─ I-01: Versão v06 → Cálculos desatualizados → Mais edições
├─ I-02: Categoria incompleta → Especialista refazia → 40% editado
├─ I-04: Hidromassagem FP único → Requeria desagregação → 100% editado
└─ Conclusão: Taxa alta era por bugs, não por variabilidade normal

DEPOIS DA CORREÇÃO (esperado):
├─ Automático: 1.100 registros (78%)
├─ Editados manualmente: 300 registros (22%)
└─ Taxa edição: 22% ← NORMAL (ajustes legítimos de campo)

ANÁLISE DE ACURÁCIA:
├─ TUG automático vs. manual: 96% automático OK
├─ TUE automático vs. manual: 88% automático OK
├─ Iluminação automático vs. manual: 99% automático OK
├─ Proteção automático vs. manual: 82% automático OK
├─ Categoria automático vs. manual: 85% automático OK (após V09)
└─ Conclusão: Algoritmo confiável em todas as áreas
```

### Padrão de análise
```
Query 1: Automático + Validadas
→ Qual % passa direto sem edição?
→ Se >90%: Algoritmo muito bom
→ Se 60-80%: OK, algumas exceções
→ Se <60%: Problema no algoritmo

Query 2: Automático + Erros
→ Qual % automático falhou na validação?
→ Se >5%: Algoritmo tem bug
→ Se <2%: Normal (casos edge)

Query 3: Editados manualmente + Validadas
→ Qual % de edições passou na validação?
→ Se >95%: Edições são corretas
→ Se <80%: Edições questionáveis
```

---

## Matriz de Escopos — Casos de Uso Consolidados

| Escopo | Pergunta-chave | Decisão esperada |
|--------|-----------------|-----------------|
| **Todas as dependências** | Como tudo se conecta? | Análise arquitetural completa |
| **Com pendências/alertas** | Onde estão os bloqueadores? | Priorização de triage |
| **Com cargas adicionais** | Que deps extras aumentam risco? | Validação extra rigorosa |
| **Sem resultado calculado** | O que ainda precisa processar? | Health check do processador |
| **Automático** | Qual taxa de edição existe? | Análise de acurácia do algoritmo |

---

## Filtros Combinados — Receitas Práticas

### 1. Triage de problemas (daily standup)
```
Escopo: Com pendências ou alertas
Estado: Pendentes + Incompletas + Erros + Exigem validação
Ordenar: Por severidade
Exibir: Top 10
Pergunta: "O que precisa de ação hoje?"
```

### 2. Validação de robustez (antes de liberar)
```
Escopo: Com cargas adicionais
Estado: Calculadas + Editadas manualmente
Filtro: Tipo = TUE, TUG, Proteção
Validador: [seu nome]
Pergunta: "Essas deps extras aguentam?"
```

### 3. Health check do processador
```
Escopo: Sem resultado calculado
Filtro: Timestamp = últimas 24h
Gráfico: Taxa de conclusão por hora
Alerta se: >5% sem resultado
Pergunta: "O processador está em dia?"
```

### 4. Análise de acurácia do modelo
```
Escopo: Automático
Estado: Validadas
Gráfico: % por tipo (TUG, TUE, iluminação, etc)
Pergunta: "Qual tipo tem maior confiança?"
```

### 5. Resolução de I-01 (Versão v06→v09)
```
Escopo: Sem resultado calculado
Filtro: Versão = v06
Versão alvo: v09
Ação: Reprocessar com v09
Pergunta: "Quantos faltam atualizar?"
```

### 6. Resolução de I-02 (Categoria incompleta)
```
Escopo: Com pendências ou alertas
Filtro: Campo = "seleção_categoria"
Estado: Editadas manualmente
Validador: Especialista EDP
Pergunta: "Categoria incluindo demanda+rede+local?"
```

### 7. Resolução de I-04 (Hidromassagem FP)
```
Escopo: Com cargas adicionais
Filtro: Aparelho = "hidromassagem"
Tipo = TUE
Ação: Desagregar em resistência + motor
Pergunta: "Todas as hidromassagens desagregadas?"
```

### 8. Resolução de I-08 (tue_generico)
```
Escopo: Sem resultado calculado
Filtro: Tipo = "tue_generico"
Estado: Erros (skipped)
Ação: Adicionar tipo a tabela OU documentar exceção
Pergunta: "tue_generico é válido ou exceção?"
```

---

## Fluxo de Análise — Passo a Passo

### Cenário: Auditoria de conformidade pós-correção

**Passo 1:** Todas as dependências
```
Escopo: Todas as dependências
Objetivo: Visão geral da cobertura
Métrica: 1.400 registros totais, distribuição por estado
Resultado: Baseline para comparação
```

**Passo 2:** Com pendências ou alertas
```
Escopo: Com pendências ou alertas
Objetivo: Identificar bloqueadores
Métrica: <5% do total = saudável
Resultado: Lista de problemas críticos
```

**Passo 3:** Com cargas adicionais
```
Escopo: Com cargas adicionais
Objetivo: Validação de robustez
Métrica: 100% validado por especialista
Resultado: Conformidade de deps complexas
```

**Passo 4:** Sem resultado calculado
```
Escopo: Sem resultado calculado
Objetivo: Health check do processador
Métrica: <1% em steady-state
Resultado: Confirmar processamento completo
```

**Passo 5:** Automático
```
Escopo: Automático + Validadas
Objetivo: Análise de acurácia
Métrica: >90% automático aprovado = bom
Resultado: Confiança no algoritmo
```

**Resultado final:**
```
✓ Tudo conectado (Todas as deps)
✓ Sem bloqueadores críticos (Sem pendências)
✓ Deps extras validadas (Com cargas)
✓ Processador em dia (Sem cálculo <1%)
✓ Algoritmo confiável (Automático >90%)

→ PRONTO PARA CLOSEOUT ✅
```

---

## Integração com Estados

### Matriz Escopo × Estado

```
                    Pendentes | Incompletas | Calculadas | Editadas | Exigem val | Validadas | Erros
Todas as deps         X            X            X           X           X          X          X
Com pendências    ✓ SIM        ✓ SIM         NUNCA        NUNCA    ✓ SIM         NUNCA     ✓ SIM
Com cargas            X            X          ✓ SIM        ✓ SIM       ✓ SIM       ✓ SIM       X
Sem resultado         X            X          NUNCA        NUNCA       NUNCA       NUNCA      X
Automático            X            X          ✓ SIM        NUNCA       NUNCA       ✓ SIM      X

Legenda:
✓ SIM = Combinação válida e útil
X = Combinação possível mas menos comum
NUNCA = Combinação contraditória ou impossível
```

---

## Recomendações Operacionais

### Para QA
```
Monitore regularmente:
├─ Escopo: Com pendências ou alertas + Estado: Todos
├─ Frequência: Daily
├─ Ação se >10%: Escalar
├─ Ação se >25%: Projeto bloqueado
└─ Alert: Críticos priorizam validação
```

### Para Engenheiros
```
Use escopos para:
├─ Antes de commit: Sem pendências + Automático OK?
├─ Pós-merge: Sem resultado calculado <1%?
├─ Refatoração: Com cargas adicionais → impacto?
└─ Validação: Automático + Validadas → confiança?
```

### Para Especialista EDP
```
Use escopos para:
├─ Workflow: Com pendências/alertas → Exigem validação
├─ Foco: Com cargas adicionais (requer atenção extra)
├─ Acurácia: Automático vs. Editados manualmente (ratio)
└─ Completude: Sem resultado calculado = problemas?
```

### Para PM/Acompanhamento
```
Dashboards úteis:
├─ Pizza: Distribuição por escopo + estado
├─ Timeline: % conformidade ao longo do tempo
├─ Heatmap: Qual escopo tem mais problemas?
├─ SLA: Tempo médio por escopo até resolução
└─ Forecast: ETA para 95% conformidade?
```

---

## Referências Cruzadas

- **Documento de Estados:** `NBR5410-Estados-Fluxo-Validacao.md`
- **Incongruências da auditoria:** `docs/research/2026-06-21-auditoria-prompt-nbr5410-edp-sp/ANALISE-PROMPT-PLANO-CORRECAO.md`
- **Plano de correção:** Fases I-01, I-02, I-03, I-04, I-08
- **Configuração SIE:** `REFERENCIA-INTEGRAL-SISTEMA.md`

---

## Evolução Futura

### v1.1 (planejado)
- [ ] Adicionar exemplos visuais (screenshots)
- [ ] Criar dashboard template para Grafana/Tableau
- [ ] Documentar API para queries de escopo

### v2.0 (roadmap)
- [ ] Escopo dinâmico (criar custom scopes)
- [ ] Machine learning para predição de pendências
- [ ] Auto-routing de alertas por severidade

---

**Documento versão:** 1.0  
**Data de criação:** 2026-07-05  
**Próxima revisão:** 2026-07-30 (após implementação de I-01 a I-04)  
**Responsável:** Time técnico SIE NBR5410  
**Status:** Ativo
