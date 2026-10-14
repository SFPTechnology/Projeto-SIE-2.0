---
epic_id: MOD-CC-SEC-QT-1
title: "MOD-CC/SEC/QT — Validação de Critérios Downstream (C3/C4/C5)"
created_date: 2026-07-15
created_by: "@sm (River)"
status: "Backlog"
priority: "P0"
---

# EPIC: MOD-CC/SEC/QT — Critérios Downstream

## 📋 Vision

Integrar três módulos de validação especializados (MOD-CC, MOD-SEC, MOD-QT) com MOD-DC para completar o dimensionamento de condutores conforme NBR5410:

- **C3 (Curto-circuito):** MOD-CC valida `Icc_presumida` vs integridade térmica
- **C4 (Seccionamento automático):** MOD-SEC valida tempo de atuação de dispositivos
- **C5 (Queda de tensão):** MOD-QT valida queda percentual conforme esquema aterramento

## 🎯 Business Value

**Antes:** Dimensionamento parcial (PENDENTE para C3/C4/C5)  
**Depois:** Dimensionamento completo com rastreabilidade de todos critérios

- ✅ Conformidade NBR5410 100% (C1 a C6)
- ✅ Documentação técnica para auditoria
- ✅ Integração com sistemas de engenharia elétrica

## 📊 Scope

### IN (Incluído)

1. **API contracts** entre MOD-DC ↔ MOD-CC/SEC/QT
2. **Backend orchestration** (paralelo com Promise.all())
3. **Database schema** para persistência de retornos
4. **Tests & validation** para cada integração
5. **Documentation** de contratos e fluxos

### OUT (Excluso)

- Implementação interna de C3/C4/C5 (esses módulos são externos)
- UI para configurar parâmetros de MOD-CC/SEC/QT
- Relatórios ou exportação de dados derivados

## 📈 Dependencies

### Bloqueadores (Pré-requisito)

- ✅ MOD-DC v3.0 implementado e QA PASS
- ✅ Contratos HTTP validados com @pm/@architect
- ✅ Schema migration aprovado

### Paralelos (Podem iniciar juntos)

- MOD-CC desenvolvimento (C3)
- MOD-SEC desenvolvimento (C4)
- MOD-QT desenvolvimento (C5)

## 🎬 Stories (Backlog)

### Story 1: MOD-CC-1 — Validação de Curto-Circuito (C3)

**ID:** MOD-CC-1  
**Status:** Backlog  
**Esforço:** 5 dias  
**Priority:** P0

**Description:**
Integrar MOD-CC com MOD-DC para validação de curto-circuito (`Icc_presumida`) conforme ABNT NBR5410 5.3.5.

**Acceptance Criteria:**
1. Endpoint POST `/api/v1/modulos/mod-cc/validar` implementado
2. Contrato `RetornoMODCC` recebido e armazenado em BD
3. MOD-DC revalida C3 com retorno recebido
4. Testes: Happy path (aprovado), Fail path (reprovado), Timeout (5s)
5. Rastreamento: `resultado.rastreio.c3_curto` registra valor + fonte

**Technical Details:**
- Endpoint recebe: `icc_presumida_a`, `tempo_atuacao_s`, `integral_joule_dispositivo`
- Retorna: `aprovado: boolean`, `fonte: string`
- Database: Persistir em `dependencia_retornos_downstream` (modulo='MOD-CC')
- Performance: < 1s para resposta

---

### Story 2: MOD-SEC-1 — Validação de Seccionamento (C4)

**ID:** MOD-SEC-1  
**Status:** Backlog  
**Esforço:** 4 dias  
**Priority:** P0

**Description:**
Integrar MOD-SEC com MOD-DC para validação de seccionamento automático conforme ABNT NBR5410 5.1.2.2.4.

**Acceptance Criteria:**
1. Endpoint POST `/api/v1/modulos/mod-sec/validar` implementado
2. Contrato `RetornoMODSEC` recebido e armazenado em BD
3. MOD-DC revalida C4 com retorno recebido
4. Regra TT: C4 permanece NAO-APLICAVEL se esquema TT (não aguarda retorno)
5. Testes: TN-S/TN-C-S (aguarda), TT (skipped), Timeout
6. Rastreamento: `resultado.rastreio.c4_seccionamento` registra `tempo_seccionamento_s` + fonte

**Technical Details:**
- Endpoint recebe: `esquema_aterramento`, `tempo_atuacao_s`
- Retorna: `aprovado: boolean`, `tempo_seccionamento_s: number`, `fonte: string`
- Database: Persistir em `dependencia_retornos_downstream` (modulo='MOD-SEC')
- Regra: se esquema TT, não chamar MOD-SEC

---

### Story 3: MOD-QT-1 — Validação de Queda de Tensão (C5)

**ID:** MOD-QT-1  
**Status:** Backlog  
**Esforço:** 6 dias  
**Priority:** P0

**Description:**
Integrar MOD-QT com MOD-DC para validação de queda de tensão conforme ABNT NBR5410 6.2.7.

**Acceptance Criteria:**
1. Endpoint POST `/api/v1/modulos/mod-qt/validar` implementado
2. Contrato `RetornoMODQT` recebido e armazenado em BD
3. MOD-DC revalida C5 com retorno recebido
4. Se `secao_requerida_mm2` retornado: MOD-DC revalida seção (laco iterativo)
5. Testes: Happy path (atende), Fail path (não atende), Revalidação (seção elevada)
6. Rastreamento: `resultado.rastreio.c5_queda_tensao` registra `queda_percentual` + `secao_requerida_mm2` + fonte

**Technical Details:**
- Endpoint recebe: `corrente_a`, `comprimento_m`, `secao_mm2`, `limite_percentual`
- Retorna: `atende: boolean`, `queda_percentual: number`, `secao_requerida_mm2?: number`, `fonte: string`
- Database: Persistir em `dependencia_retornos_downstream` (modulo='MOD-QT')
- Laco: Se `secao_requerida_mm2` > atual, revalida C1/C2/C6 com nova seção

---

## 🔄 Timeline

| Sprint | Story | Esforço | Fim Estimado |
|--------|-------|---------|--------------|
| Sprint 1 | MOD-CC-1 | 5 dias | 2026-07-22 |
| Sprint 2 | MOD-SEC-1 | 4 dias | 2026-07-29 |
| Sprint 2 | MOD-QT-1 | 6 dias | 2026-08-05 |

**Total:** ~15 dias (3 sprints)

---

## ✅ Acceptance Criteria (EPIC)

1. ✅ Todas 3 stories criadas e em backlog
2. ✅ Contratos HTTP documentados
3. ✅ Database schema migration definido
4. ✅ Testes de integração planejados
5. ✅ Timeline e esforço estimados
6. ✅ Dependencies mapeadas

---

## 📝 Notes

- Orquestração: Paralelo com `Promise.all()` conforme validação @pm
- Persistência: Tabela `dependencia_retornos_downstream` conforme validação @pm
- Ordem de implementação: CC → SEC → QT (dependências)
- Release: Agrupar 3 stories em release `v3.1.0` (Minor bump)

---

**EPIC Status:** Ready for Development  
**Created by:** @sm (River)  
**Date:** 2026-07-15
