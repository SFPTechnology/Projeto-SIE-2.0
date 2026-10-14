# DP-04 — Decisão PO sobre fluxo e autoridade para categoria superior — EDP V9

**Data:** 2026-07-27  
**Agente responsável:** @po / Pax  
**PRD base:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Gate:** DP-04  
**Status PO:** APROVADO  
**Escopo:** fluxo de intenção, solicitação e confirmação de categoria superior no contexto EDP São Paulo.

---

## 1. Decisão

O fluxo de categoria superior fica aprovado sob a ótica de produto, desde que a implementação preserve a separação obrigatória entre:

1. categoria mínima calculada pelo sistema;
2. intenção do cliente por categoria superior;
3. preparação da solicitação;
4. manifestação formal da EDP;
5. confirmação técnica/responsável;
6. categoria definitiva usada em documentos e decisões posteriores.

Essa aprovação não autoriza seleção automática de categoria superior, não libera override sem governança e não substitui os gates DP-07, GP-01, DP-09, GO-01A ou GO-01B.

---

## 2. Termos normativos do fluxo

| Termo | Definição | Regra de produto |
| --- | --- | --- |
| Categoria mínima calculada | Resultado técnico mínimo derivado das cargas, tensão e catálogo aplicável | Pode ser calculada automaticamente pelo sistema |
| Categoria superior elegível | Categoria acima da mínima tecnicamente possível dentro das regras vigentes | Pode ser apresentada como opção, mas não pode virar definitiva sem fluxo formal |
| Intenção do cliente | Registro de que o cliente deseja avaliar categoria superior | Não equivale à solicitação aprovada |
| Categoria solicitada | Categoria superior enviada ou preparada para avaliação da distribuidora | Deve ter origem rastreável e justificativa |
| Manifestação EDP | Retorno formal da distribuidora sobre a categoria solicitada | Necessária para tornar a categoria superior confirmável |
| Categoria definitiva | Categoria final usada em dimensionamento, documentos e auditoria | Exige manifestação EDP e confirmação técnica/responsável quando for superior à mínima |

---

## 3. Estados aprovados

O produto deve operar com os seguintes estados mínimos:

| Estado | Significado | Próxima transição permitida |
| --- | --- | --- |
| `SEM_INTENCAO_SUPERIOR` | Projeto segue a categoria mínima calculada | Registrar intenção superior |
| `INTENCAO_SUPERIOR_REGISTRADA` | Intenção do cliente foi registrada | Preparar solicitação ou cancelar intenção |
| `SOLICITACAO_SUPERIOR_PREPARADA` | Solicitação contém dados mínimos para envio/registro | Aguardar manifestação EDP |
| `AGUARDANDO_MANIFESTACAO_EDP` | Projeto aguarda resposta formal | Registrar manifestação |
| `MANIFESTACAO_EDP_RECEBIDA` | Manifestação foi registrada, ainda sem ratificação final | Solicitar confirmação técnica |
| `CONFIRMACAO_TECNICA_PENDENTE` | Falta confirmação de responsável autorizado | Confirmar, negar ou pedir revisão |
| `CATEGORIA_SUPERIOR_CONFIRMADA` | Categoria superior está aprovada para uso definitivo | Usar categoria definitiva em documentos |
| `CATEGORIA_SUPERIOR_NEGADA` | Categoria superior não foi aceita | Retornar à categoria mínima ou revisar |
| `REQUER_REVISAO` | Evidência insuficiente, divergente ou vencida | Corrigir evidências antes de nova decisão |

---

## 4. Matriz de autoridade de produto

| Ação | Sistema | Operador do projeto | Cliente/solicitante | EDP | Responsável técnico/autorizado |
| --- | --- | --- | --- | --- | --- |
| Calcular categoria mínima | Executa | Consulta | Não aprova | Não aprova | Consulta/valida |
| Exibir categorias superiores elegíveis | Executa | Consulta | Consulta | Não aprova | Consulta |
| Registrar intenção de categoria superior | Registra e audita | Pode registrar fonte da intenção | Origem da intenção | Não aprova | Consulta |
| Preparar solicitação superior | Valida campos mínimos | Pode preparar | Pode fornecer dados | Não aprova | Consulta |
| Registrar manifestação EDP | Armazena evidência | Pode anexar/registrar | Consulta | Origem da decisão externa | Consulta |
| Confirmar categoria definitiva superior | Bloqueia se evidência ausente | Não confirma sozinho | Não confirma sozinho | Fornece manifestação | Confirma/ratifica |
| Reverter para categoria mínima | Registra e audita | Pode solicitar | Pode solicitar | Não aprova | Confirma quando afetar documento final |

---

## 5. Critérios de aceite para stories

Uma story derivada deste gate só pode ser considerada pronta para desenvolvimento se incluir:

1. cálculo separado da categoria mínima e da categoria definitiva;
2. registro explícito da intenção de categoria superior;
3. bloqueio para uso definitivo de categoria superior sem manifestação EDP;
4. bloqueio para confirmação final sem perfil/autoridade permitida pelo modelo de governança;
5. trilha de auditoria para intenção, solicitação, manifestação, confirmação, negação e reversão;
6. tratamento de estado pendente sem mascarar a categoria mínima calculada;
7. mensagens CLI/observabilidade que deixem claro se o projeto está em categoria mínima, intenção superior pendente ou categoria superior confirmada.

---

## 6. Impacto na liberação de pacotes

| Pacote | Resultado deste documento |
| --- | --- |
| Pacote 4 | DP-04 deixa de ser bloqueador de produto; ainda depende dos demais gates aplicáveis do pacote |
| Pacote 5 | Pode usar este fluxo como entrada, mas não herda aprovação de governança ou auditoria |
| Pacote 6 | Não liberado; depende de GP-01 completo e DP-07 coaprovado |
| Pacote 7 | Não liberado por este documento |
| Pacote 8 | Não liberado; depende de DP-09 e GO-01B |

---

## 7. Encaminhamento

DP-04 está aprovado por @po. As próximas etapas devem usar esta decisão como fonte de produto para:

- refinamento de stories pelo @sm;
- validação arquitetural de enforcement, perfis e auditoria pelo @architect;
- validação QA dos cenários de intenção, pendência, confirmação, negação e reversão.
