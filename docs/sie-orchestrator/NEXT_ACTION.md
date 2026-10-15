# NEXT_ACTION — F01 BLOQUEADA (continuar F01, não F02)

**Fonte canônica:** `ORCHESTRATOR_STATE.json`, revisão 10, `F00=DONE`, `F01=BLOCKED`, `NOR-01=BLOCKED`. Branch F01: `feat/f01-governanca-normativa`; PR #3 em rascunho, apontado para branch F00. Main/produção intocadas.

## Prova computacional F01
- GitHub Actions `SIE modular API`: 149 pytest, 1 warning, success na revisão `fa6002d`: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38722630175 .
- `SIE Browser E2E (Chromium)`: 4 testes reais success (inclusive painel normativo), https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38722630269 .
- Gates AIOX root: success, https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38722630211 .
- Esses testes não validam conteúdo nem vigência de tabela normativa.

## Ordem de retomada, sem copiar prompt nem editar CSV manualmente
1. Prosseguir a própria F01: obter fonte primária autorizada/licença e conferir linha, coluna, edição, vigência, unidade e notas de **cada célula realmente usada**, com dupla conferência; não inventar Rca/XL/Iz/EDP.
2. Documentar conflitos territoriais e exceções transitórias NR-10, com fundamentação, e preparar casos numéricos de referência independentes antes da liberação.
3. Implementar snapshots imutáveis por projeto, diffs entre edições e trilha de impacto, com banco de ensaio local/descartável, sem produção.
4. Reexecutar regressão, integração, segurança, UX e três pareceres QA. Só alterar F01 para DONE com gates exigidos satisfeitos.

**Próxima fase F02: BLOQUEADA.** A fase F01 deve ser retomada; não há background automático ou autorização de deploy.
