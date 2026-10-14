# DP-09 — Decisão PO sobre destino do catálogo genérico — EDP V9

**Data:** 2026-07-27  
**Agente responsável:** @po / Pax  
**PRD base:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Gate:** DP-09  
**Status PO:** DIREÇÃO DE PRODUTO APROVADA  
**Status global do gate:** PENDENTE  

---

## 1. Decisão de produto

O catálogo genérico não deve ser removido globalmente. A decisão de produto é preservar o catálogo genérico para contextos fora da rota EDP São Paulo e remover seu uso apenas da rota específica EDP quando a migração estiver operacionalmente segura.

Essa decisão confirma a direção de produto, mas não libera o gate DP-09 global porque ainda faltam inventário real, evidência de não regressão para contextos não EDP e aprovação GO-01B.

---

## 2. Regras aprovadas

1. O catálogo genérico continua existindo como capacidade do produto para contextos não EDP.
2. A rota EDP São Paulo deve usar catálogo/regra específica aprovada para EDP, quando disponível e validada.
3. Nenhuma remoção física, migração destrutiva ou desativação global é autorizada sem GO-01B aprovado.
4. Projetos existentes precisam de estratégia de compatibilidade, inventário e rollback.
5. Contextos fora da EDP São Paulo não podem sofrer regressão por consequência da mudança EDP.

---

## 3. Critérios para aprovação global de DP-09

DP-09 só pode ser globalmente aprovado quando houver:

1. inventário real dos contextos que usam catálogo genérico;
2. classificação dos usos por EDP São Paulo, outras distribuidoras e cenários genéricos;
3. plano de migração da rota EDP sem remoção global indevida;
4. evidência de não regressão para contextos não EDP;
5. GO-01B aprovado;
6. coaprovação @architect;
7. validação QA dos cenários de compatibilidade.

---

## 4. Impacto na liberação de pacotes

| Pacote | Resultado |
| --- | --- |
| Pacote 8 | BLOQUEADO até DP-09 global e GO-01B |
| Remoção de legado | NÃO AUTORIZADA |
| Stories de inventário/mapeamento | Podem ser criadas como preparação se não executarem remoção destrutiva |
| Stories de migração/removal | Não liberadas sem GO-01B e plano de rollback validado |

---

## 5. Encaminhamento

1. @data-engineer deve produzir inventário real e evidência de impacto.
2. @architect deve coaprovar a estratégia final de destino e migração.
3. @devops/@qa devem validar readiness operacional, rollback, backup/restore e dry run no escopo de GO-01B.
