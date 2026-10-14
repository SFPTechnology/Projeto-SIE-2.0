# DP-07 — Decisão PO sobre governança de parâmetros, autorização, override e auditoria — EDP V9

**Data:** 2026-07-27  
**Agente responsável:** @po / Pax  
**PRD base:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Gate:** DP-07  
**Status PO:** CONTRIBUIÇÃO PO APROVADA  
**Status global do gate:** PENDENTE DE COAPROVAÇÃO ARQUITETURAL  

---

## 1. Decisão de produto

A política de governança de parâmetros fica aprovada pelo @po nos critérios de produto abaixo.

O gate DP-07, entretanto, não está globalmente liberado porque o PRD exige coaprovação @po/@architect. A arquitetura ainda precisa validar enforcement técnico, perfis, rastreabilidade, política de override e modelo de auditoria.

---

## 2. Princípios de governança aprovados

1. **Default-deny:** qualquer ação privilegiada fica bloqueada até que exista perfil, justificativa e trilha de auditoria.
2. **Separação de fontes:** parâmetros oficiais, entradas do projeto, intenção do cliente, manifestação EDP e confirmação técnica não podem ser gravados como se fossem a mesma decisão.
3. **Sem override silencioso:** qualquer exceção precisa de justificativa, ator responsável, timestamp e motivo de negócio/técnico.
4. **Sem publicação por operador comum:** alterações de catálogo, parâmetros normativos ou regras oficiais não podem ser feitas por papel operacional ordinário.
5. **Reversibilidade rastreada:** correções e rollbacks precisam preservar histórico, não sobrescrever a origem da decisão.
6. **CLI First:** fluxos críticos devem existir via CLI/serviço antes de qualquer UI de apoio.

---

## 3. Matriz de autoridade de produto

| Ação governada | Regra PO | Status técnico |
| --- | --- | --- |
| Consultar parâmetros oficiais | Permitido para usuários do projeto com acesso ao projeto | Requer validação de acesso/RLS |
| Registrar evidência de topologia | Permitido ao operador como entrada de projeto | Confirmação técnica ainda governada por perfis |
| Registrar intenção de categoria superior | Permitido como registro de intenção/fonte | Não torna categoria definitiva |
| Registrar manifestação EDP | Permitido apenas como evidência formal rastreável | Enforcement técnico pendente |
| Confirmar categoria definitiva | Requer perfil autorizado e evidência prévia | Coaprovação arquitetural pendente |
| Publicar catálogo oficial | Ação privilegiada, não operacional comum | Coaprovação arquitetural pendente |
| Alterar parâmetro normativo | Ação privilegiada com justificativa e auditoria | Coaprovação arquitetural pendente |
| Executar override | Exceção controlada, nunca padrão | Coaprovação arquitetural e QA pendentes |
| Migrar/remover legado | Só após gates operacionais e dados aprovados | Bloqueado por GO-01A/GO-01B |
| Reverter migração | Deve ter plano, evidência e auditoria | Bloqueado por GO-01B |

---

## 4. Requisitos mínimos para coaprovação arquitetural

Para liberar DP-07 globalmente, @architect deve validar pelo menos:

1. perfis técnicos e escopos reais de autorização;
2. política de RLS/acesso por projeto, tenant ou organização;
3. trilha de auditoria para leitura crítica, alteração, override, publicação, migração e rollback;
4. tratamento de break-glass/suporte sem abrir privilégio permanente;
5. bloqueios para alteração direta de parâmetros oficiais por papel não autorizado;
6. compatibilidade com DP-04 para intenção, solicitação e confirmação de categoria superior;
7. cenários de não regressão para contextos fora da EDP São Paulo.

---

## 5. Critérios de aceite para stories

Stories que dependam de DP-07 devem conter:

1. ator, permissão e escopo de cada ação privilegiada;
2. evento auditável gerado por cada transição relevante;
3. comportamento de bloqueio quando o usuário não tem autoridade;
4. justificativa obrigatória para override;
5. separação entre dado oficial, dado informado, decisão externa e decisão confirmada;
6. testes de autorização positiva e negativa;
7. evidência de que a UI, se existir, apenas observa/aciona capacidades já disponíveis no fluxo CLI/API.

---

## 6. Impacto na liberação de pacotes

| Pacote | Resultado |
| --- | --- |
| Pacote 4 | Ainda não liberado por DP-07 global; falta @architect |
| Pacote 5 | Ainda não liberado por DP-07 global |
| Pacote 6 | Ainda bloqueado por GP-01 e DP-07 |
| Pacote 7 | Ainda bloqueado se depender de override/auditoria final |
| Pacote 8 | Ainda bloqueado por GO-01B/DP-09 |

---

## 7. Encaminhamento

Encaminhar para @architect a coaprovação de enforcement técnico. Enquanto isso, esta decisão pode ser usada pelo @sm como referência de produto, mas não como liberação global do gate DP-07.
