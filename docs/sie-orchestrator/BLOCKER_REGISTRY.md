# BLOCKER_REGISTRY — bloqueios atuais e estratégias

| Código | Classificação | Evidência e causa | Estratégia comprovada / próxima ação | Estado |
|---|---|---|---|---|
| NOR-01 | REQUIREMENT_GAP / DATA_INCONSISTENCY | A API recebe tabela de condutor do usuário; não há versão normativa integrada e aprovada | Inventário offline executado: 6 arquivos, SHA-256; prosseguir conferência dos valores, versões e casos primários | BLOCKED |
| SIE-AUTO-003 | REQUIREMENT_GAP | Extrações EDP/NBR presentes, mas o hash não garante transcrição/edição/aplicabilidade | Story de proveniência publicada; matriz `NORMATIVE-SOURCES-RECOVERY.md`; falta revisão de cláusulas e dados | BLOCKED |
| NOR-02 | CALCULATION_FAILURE (risco de aceitação) | Somente Ib≤In≤Iz e queda resistiva não atendem às verificações normativas completas | Exigir proteção, curto-circuito, impedância, reatância e casos independentes após NOR-01 | BLOCKED |
| EDP-01 | REQUIREMENT_GAP | Seleção de categoria por corrente ainda não valida todos os critérios da distribuidora | Manter `liberado_para_padrao_entrada=false` | BLOCKED |
| SEC-01 | EXTERNAL_AUTHORIZATION | Token local sem perfis/identidade de produção e migração autorizada | Preservar localhost; não publicar nem migrar dados | HUMAN_REQUIRED |
| UX-01 | TEST_FAILURE — resolvido para escopo local | Testes de navegador inexistentes até esta etapa | Chromium real 3 passed (38612351246) + API 90 passed; sem supor homologação de produção | DONE para fluxo local |
| ENG-004-01 | TEST_FAILURE — resolvido | Regressão rejeitava comprimento zero trifásico, 1 failed / 85 passed no run 38605924113 | Corrigida função; 90 passed em 38612351333 | DONE |
| CLI-01 | ARCHITECTURE_CONFLICT — resolvido | CLI faltante em fluxo UI-first | CLI publicada e testada na story 001 | DONE |

## Progresso sem aprovação normativa

O run 38613344311 registrou 99 testes Python passando, presença dos seis artefatos e manifesto SHA256 como artifact 11917953248. O próprio manifesto conserva `normative_conformity_verified=false`. Não é permitido considerar NOR-01 ou SIE-AUTO-003 resolvidos com base apenas neste inventário.


### Checkpoint final F05 — 21/10/2026
HUMAN_REQUIRED somente para publicação: auto-review rejeitou git push sem autorização explícita do payload F05 neste destino. Código fb5e3e382db973a989fb499a07a62404d83d80eb e QA3/testes locais aprovados; branch remota inexistente,CI não executado. Retomar publicação e CI após autorização específica, sem repetir implementação nem reabrir aceites anteriores.


### Encerramento F05 — 21/10/2026 — estado vigente
F05 DONE. Bloqueio de publicação RESOLVIDO por autorização explícita do usuário. Branch publicada com árvores idênticas às locais. API39662901530,AIOX39662901277,Chromium39662901273 completed/success no SHA7c5547af06e6b569f493473ceb61cd6d224603da;604 API,34 F00,25 Chromium,18 AIOX e QA3 aprovados. Passagem F06 liberada,próximo arquivo F06_EXECUTAR.md;sem merge/deploy. O checkpoint HUMAN_REQUIRED acima é histórico e não representa impedimento atual.
