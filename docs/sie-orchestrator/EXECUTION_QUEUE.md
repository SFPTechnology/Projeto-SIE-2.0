## Decisão vigente — 20/10/2026

**F01 DONE por aceite expresso do titular. F02 liberada para desenvolvimento.** A decisão está em `docs/implantacao-sie-2-0/F01/ACEITE_TITULAR_ENCERRAMENTO_F01.json`, vinculada por SHA-256 ao manifesto e orquestrador. As pendências técnicas anteriores permanecem registradas como limites de uso, sem bloquear o avanço autorizado do desenvolvimento. Aceites do lote 01 e F00 preservados; nenhuma nova homologação normativa ou liberação de produção é atribuída. Os registros abaixo são históricos quando conflitarem com esta decisão.

# EXECUTION_QUEUE — fila reconciliada

Critério: `READY` só com dependências DONE e requisitos definidos; `DONE` exige todos os critérios documentados e evidência verificada. A fonte canônica dos estados é `ORCHESTRATOR_STATE.json`.

| ID | Atividade | Dependências | Estado | Evidência / próxima ação |
|---|---|---|---|---|
| F00 | Diagnóstico e preservação da baseline | Nenhuma; fase inicial | DONE | 37 IDs, replay 34, 134 pytest, 3 Chromium, 18 AIOX, QA3; pacote remoto ab12904, passagem sequencial liberada |
| F01 | Engenharia de requisitos e governança normativa | F00 DONE + aceite do titular | DONE | Encerrada em20/10/2026 por decisão expressa; F02 liberada para desenvolvimento; resultado técnico e limites de produção preservados |
| SIE-AUTO-001 | CLI de projetos | Nenhuma | DONE | Testes CLI e documentação anteriores |
| SIE-AUTO-002 | Gates AIOX | Nenhuma | DONE | lint/typecheck/test/build na CI |
| SIE-AUTO-011 | Escalonador determinístico | 001, 002 | DONE | 67 testes e qualidade AIOX anteriores |
| SIE-AUTO-004 | Contratos de engenharia | 011 | DONE | 90 pytest, 38612351333; AIOX 38612351441 |
| SIE-AUTO-005 | E2E real de navegador | 011 | DONE | 3 Chromium, 38612351246 |
| SIE-AUTO-003 | Evidência normativa e rastreabilidade de tabelas | Documentos fonte | BLOCKED | Inventário SHA256 6/6 (38613344311), conteúdo normativo ainda não validado |
| NOR-01 | Fontes/catálogos normativos confiáveis | Fonte primária e casos | BLOCKED | Matrizes e versões independentes pendentes |
| SIE-AUTO-006 | Identidade de produção / migração DB | Ambiente autorizado | HUMAN_REQUIRED | Sem credenciais nem escopo de produção autorizados |
| SIE-AUTO-007 | Motores normativos completos | NOR-01, 004 | PENDING | Bloqueado pelos dados normativos |
| SIE-AUTO-008 | Diagramas e memoriais | 007, 006 | PENDING | Aguardar domínio validado e isolamento |
| SIE-AUTO-009 | QA final/UX/documentação | 005, 008 | PENDING | Aguardar sistema completo |
| SIE-AUTO-010 | Liberação controlada | 009, 006, NOR-01 | PENDING | Testes independentes e aprovação técnica |

A referência histórica de SIE-AUTO-003 foi reconciliada no JSON, mas **não** foi marcada DONE pela simples criação do manifesto. Não há atividade READY nesta revisão. Um bloqueio de norma não deve fazer o orquestrador inventar valores de tabelas.

| F02 | Arquitetura e modelagem do domínio elétrico | F01 DONE por aceite titular | VALIDATING |539API/F0034/AIOX,QA3 aprovado; conferir CI de publicação |
