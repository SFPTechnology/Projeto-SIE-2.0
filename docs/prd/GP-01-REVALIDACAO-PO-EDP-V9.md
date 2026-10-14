# GP-01 — Revalidação PO de persona, papéis, UX, perfis e metas — EDP V9

**Data:** 2026-07-27  
**Agente responsável:** @po / Pax  
**PRD base:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Evidência UX:** `docs/ux/GP-01-EVIDENCIAS-UX-EDP-V9.md`  
**Gate:** GP-01  
**Status global:** PENDENTE  

---

## 1. Decisão

GP-01 permanece pendente. O @po confirma apenas o que já estava aprovado e registra as condições de produto para avanço, sem liberar Pacote 6 ou Release 1.

---

## 2. Status por subitem

| Subitem | Status PO | Justificativa |
| --- | --- | --- |
| GP-01.1 — Persona, papéis e jornada | PENDENTE | A evidência UX informa ausência de validação real de persona primária e responsabilidades finais |
| GP-01.2 — Fronteira de Release 1 | APROVADO | Decisão já formalizada em `docs/prd/GP-01.2-DECISAO-FRONTEIRA-RELEASE-EDP-V9.md` |
| GP-01.3 — Perfis/permissões | CONTRIBUIÇÃO PO PRONTA; PENDENTE @architect | Depende de enforcement técnico, matriz final de permissões e alinhamento com DP-07 |
| GP-01.4 — Metas/UX/operacionais | PENDENTE | Falta baseline, métrica aprovada, instrumentação e critério de sucesso verificável |
| GP-01 global | PENDENTE | Aprovação parcial não libera o gate global |

---

## 3. Modelo de papéis aceito como referência de produto

O @po aceita o seguinte modelo de papéis como taxonomia de produto para refinamento, sem convertê-lo em persona validada nem em autorização técnica final:

| Papel de produto | Responsabilidade esperada | Limite |
| --- | --- | --- |
| Operador do projeto | Inserir dados, registrar evidências e acompanhar pendências | Não confirma categoria superior sozinho; não publica catálogo |
| Responsável técnico/autorizado | Ratificar decisões técnicas e confirmações finais | Precisa de enforcement técnico aprovado |
| Administrador normativo/catálogo | Manter parâmetros oficiais quando autorizado | Ação privilegiada, auditável e fora do papel operacional comum |
| Suporte/break-glass | Atuar em exceções controladas | Não pode virar permissão permanente ou silenciosa |
| Cliente/solicitante | Origem da intenção de categoria superior | Não executa confirmação técnica no sistema por padrão |

---

## 4. Condições para liberar GP-01

GP-01 só pode ser liberado quando houver:

1. persona primária e jornada validadas ou decisão PO explícita aceitando a ausência de pesquisa com risco documentado;
2. papéis e responsabilidades aprovados por @po;
3. matriz de permissões coaprovada por @po/@architect;
4. UX ou fluxo operacional mínimo para explicar estados pendentes, bloqueios e confirmação;
5. metas de sucesso e baseline definidos;
6. plano de medição ou instrumentação mínima;
7. validação QA de que as stories refletem papéis, permissões, metas e critérios de aceite.

---

## 5. Impacto na liberação de pacotes

| Item | Resultado |
| --- | --- |
| Pacote 6 | BLOQUEADO |
| Release 1 | NÃO AUTORIZADO |
| Stories do Pacote 6 | Não devem ser criadas como prontas para desenvolvimento enquanto GP-01 global estiver pendente |
| Stories exploratórias/documentais | Podem ser preparadas se declararem dependências e não forem tratadas como implementação liberada |

---

## 6. Encaminhamento

1. @ux-design-expert deve completar GP-01.1 e GP-01.4.
2. @architect deve coaprovar GP-01.3 em conjunto com DP-07.
3. @qa deve validar a cobertura dos critérios de aceite antes de qualquer liberação de Pacote 6.
