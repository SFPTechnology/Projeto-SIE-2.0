# Matriz de prontidão para GC=PASS

Preparação documental; não autoriza operações remotas. Estado desta rodada: `GC=BLOCKED`.

| ID | Requisito | Fonte | Estado | Evidência | Pendência/bloqueio | Dependência | Responsável | Autorização | Aceite objetivo | Preparação |
|---|---|---|---|---|---|---|---|---|---|---|
| GC-01 | Recuperação independente do destino | C14/C15/C17 | PENDING_EXTERNAL_AUTHORIZATION | procedimento sintético e guardrails C20 | recuperação operacional | mecanismo aprovado | DBA/SRE | autorização operacional | restauração/readback | checklist local |
| GC-02 | A03/A04/B04/C03 no destino | C08/C20 | PENDING_EXTERNAL_AUTHORIZATION | PG17 descartável | DDL remoto proibido | recuperação aprovada | DBA | DDL remoto explícito | migrations/readback | testes descartáveis |
| GC-03 | Auth real A/B e RLS | C08/C20 | PENDING_EXTERNAL_AUTHORIZATION | cenários `SYNTHETIC_ONLY` | Auth/RLS real não executado | ambiente autorizado | Backend/Security | Auth remoto | isolamento A/B | cenários sintéticos |
| GC-04 | E01–E09/E11 com fontes | C08/C12 | PENDING_PROFESSIONAL_ACCEPTANCE | rastreabilidade C22/D2 | fontes/células e parecer | documentação normativa | Eng. eletricista | aceite profissional | regra+fonte+parecer | matriz/testes |
| GC-05 | E10 legado | C19 | DEFERRED | decisão Greenfield | importação fora do escopo | mudança de escopo | Product Owner | nova decisão | não bloquear Greenfield | preservar/diferir |
| GC-06 | C13 homologação | C11/C12/C13 | PENDING_PROFESSIONAL_ACCEPTANCE | C13 preparado, `NOT_SIGNED` | assinatura autêntica | revisão E01–E11 | profissional habilitado | aceite profissional | termo rastreável | pacote de revisão |
| GC-07 | Cinco workflows no SHA final | C08/C20 | PENDING_EVIDENCE | workflows anteriores verdes | revalidar SHA desta entrega | publicação | DevOps | permissão CI | cinco `success` mesmo SHA | monitoramento |
| GC-08 | Preservação original/legado | C19 | VERIFIED | escopo e guardrails | nenhuma | nenhuma | Orchestrator | nenhuma | nenhum artefato original alterado | auditoria |
