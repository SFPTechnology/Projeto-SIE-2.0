---
title: "MOD-DC Pré-requisitos Residuais — Validação para Integração Downstream"
date: 2026-07-15
author: "@pm (Morgan)"
status: "Em Validação"
---

# MOD-DC Pré-requisitos Residuais — Validação Estratégica

## 📋 Contexto

MOD-DC v3.0 (DC-1 a DC-11) foi implementado com sucesso e QA PASS (637/637 tests).

**Extensão C3/C4/C5** foi implementada como **pull-based integration model** com contratos bem-definidos:
- `RetornoMODCC` (curto-circuito, C3)
- `RetornoMODSEC` (seccionamento automático, C4)
- `RetornoMODQT` (queda de tensão, C5)

**Status:** Funcional e testado, mas **aguarda integração com módulos downstream**

---

## 🔍 Pré-requisitos Críticos a Validar

### **PRÉ-REQ 1: Orquestração de Retornos Downstream**

**Questão Estratégica:** Como coordenar as chamadas a MOD-CC, MOD-SEC e MOD-QT?

#### Opção A: Síncrono (Sequencial)
```
MOD-DC chama MOD-CC → aguarda retorno → chama MOD-SEC → aguarda → chama MOD-QT
Tempo estimado: T_cc + T_sec + T_qt (sequencial)
Vantagem: Simples, sem paralelismo
Desvantagem: Latência acumulada
```

#### Opção B: Assíncrono (Paralelo)
```
MOD-DC inicia 3 chamadas em paralelo (CC, SEC, QT)
Aguarda Promise.all()
Tempo estimado: max(T_cc, T_sec, T_qt)
Vantagem: Mais rápido
Desvantagem: Complexidade, timeout handling
```

#### Opção C: Webhook/Callback
```
MOD-DC inicia cálculo parcial
MOD-CC/SEC/QT retornam via webhook quando prontos
MOD-DC recalcula ao receber cada retorno
Vantagem: Desacoplado, escalável
Desvantagem: Complexo, estado distribuído
```

**Recomendação @pm:** **Opção B (Paralelo)** é melhor para MVP
- Latência < 2s mesmo com 3 módulos
- Código mais simples que webhook
- Promise.all() com timeout de 5s é suficiente

**Decisão:** ✅ **APPROVE Opção B para Roadmap MOD-CC/SEC/QT**

---

### **PRÉ-REQ 2: Persistência de Retornos Downstream**

**Questão Estratégica:** Onde armazenar os retornos retorno_cc, retorno_seccionamento, retorno_qt?

#### Opção A: Extensão da Tabela `dependencias`
```sql
ALTER TABLE dependencias ADD COLUMN:
  - retorno_cc_json jsonb
  - retorno_sec_json jsonb
  - retorno_qt_json jsonb
  - timestamps de cada retorno
```
Vantagem: Uma tabela, menos JOINs
Desvantagem: Denormaliza estrutura

#### Opção B: Tabela Separada `dependencia_retornos_downstream`
```sql
CREATE TABLE dependencia_retornos_downstream (
  dependencia_id UUID,
  modulo ENUM ('MOD-CC', 'MOD-SEC', 'MOD-QT'),
  payload JSONB,
  recebido_em TIMESTAMP
)
```
Vantagem: Separação limpa, auditoria fácil
Desvantagem: JOINs adicionais

#### Opção C: Não persistir (Cache TTL)
```
Retornos apenas em memória durante sessão
Redis cache com TTL 1h
```
Vantagem: Sem migração DB
Desvantagem: Perda de dados em crash

**Recomendação @pm:** **Opção B (Tabela separada)** é mais profissional
- Auditoria completa: quem retornou quando
- Permite histórico de retornos
- Facilita debugging de inconsistências

**Decisão:** ✅ **APPROVE Opção B para Schema Migration**

---

### **PRÉ-REQ 3: Contratos HTTP entre Módulos**

**Questão Estratégica:** Qual é a interface HTTP entre MOD-DC e MOD-CC/SEC/QT?

#### Contrato MOD-DC → MOD-CC

```http
POST /api/v1/modulos/mod-cc/validar
Content-Type: application/json

{
  "dependencia_id": "DEP-UUID",
  "icc_presumida_a": 1500,
  "tempo_atuacao_s": 0.1,
  "integral_joule_dispositivo": 20000,
  "origem": "MOD-DC-C3"
}

Response 200:
{
  "aprovado": true,
  "icc_presumida_a": 1500,
  "tempo_atuacao_s": 0.1,
  "integral_joule_dispositivo": 20000,
  "fonte": "MOD-CC v1.0"
}
```

#### Contrato MOD-DC → MOD-SEC

```http
POST /api/v1/modulos/mod-sec/validar
Content-Type: application/json

{
  "dependencia_id": "DEP-UUID",
  "esquema_aterramento": "TN-S",
  "tempo_atuacao_s": 0.1
}

Response 200:
{
  "aprovado": true,
  "tempo_seccionamento_s": 0.4,
  "fonte": "MOD-SEC v1.0"
}
```

#### Contrato MOD-DC → MOD-QT

```http
POST /api/v1/modulos/mod-qt/validar
Content-Type: application/json

{
  "dependencia_id": "DEP-UUID",
  "corrente_a": 10,
  "comprimento_m": 50,
  "secao_mm2": 4,
  "limite_percentual": 4
}

Response 200:
{
  "atende": true,
  "queda_percentual": 1.8,
  "limite_aplicado": 4,
  "secao_requerida_mm2": null,
  "fonte": "MOD-QT v1.0"
}
```

**Status:** ✅ **CONTRATOS DEFINIDOS e DOCUMENTADOS**

**Decisão:** ✅ **APPROVE Contratos HTTP para Implementação**

---

## 📊 Matriz de Validação Pré-requisitos

| Pré-req | Decisão | Owner | Timeline | Status |
|---------|---------|-------|----------|--------|
| **Orquestração** | Paralelo (Opção B) | @architect | Sprint 1 MOD-CC/SEC/QT | ✅ APPROVED |
| **Persistência** | Tabela separada (Opção B) | @data-engineer | Sprint 1 MOD-CC/SEC/QT | ✅ APPROVED |
| **Contratos HTTP** | Definidos acima | @devops | Sprint 1 MOD-CC/SEC/QT | ✅ APPROVED |

---

## 🎯 Recomendações Finais (Validação @pm)

### ✅ **Aprovado para Prosseguir:**

1. **MOD-DC v3.0 está pronto para merge** em `master`
   - PR #1 criado
   - QA PASS 637/637
   - Documentação completa

2. **Pré-requisitos C3/C4/C5 validados:**
   - ✅ Orquestração: Paralelo com Promise.all()
   - ✅ Persistência: Tabela `dependencia_retornos_downstream`
   - ✅ Contratos HTTP: Definidos e documentados

3. **Roadmap MOD-CC/SEC/QT pode iniciar:**
   - Epic com 3 stories (1 por módulo)
   - Timeline: ~3 sprints (15 dias)
   - Backlog pronto para @sm

---

## 📝 Próximos Passos

### @pm (Morgan):
- [x] Validar pré-requisitos C3/C4/C5
- [ ] Criar epic MOD-CC/SEC/QT (delegado a @sm)
- [ ] Validar roadmap com stakeholders

### @sm (River):
- [ ] Criar 3 stories:
  - Story MOD-CC-1: Validação curto-circuito
  - Story MOD-SEC-1: Validação seccionamento
  - Story MOD-QT-1: Validação queda de tensão
- [ ] Estimar esforço por story
- [ ] Definir dependências e ordem

### @devops (Gage):
- [ ] Merge PR #1 após aprovação final
- [ ] Criar release tag v3.0.0 para MOD-DC
- [ ] Documentar release notes

---

## ✅ **Status Final: PRÉ-REQUISITOS VALIDADOS**

**Data:** 2026-07-15  
**Validador:** @pm (Morgan)  
**Verdict:** GO — Prosseguir com MOD-CC/SEC/QT Roadmap  

---

**Próxima etapa:** @sm criar epic MOD-CC/SEC/QT com 3 stories
