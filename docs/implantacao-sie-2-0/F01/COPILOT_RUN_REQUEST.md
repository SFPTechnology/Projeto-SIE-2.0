# SIE F01 — Solicitação de execução Copilot QA3

Este arquivo é **somente o gatilho de nova rodada** do workflow
`.github/workflows/f01-copilot-qa-isolated.yml`, sem modificações em F00, F02 ou main.

**Branch permitida:** `feat/f01-governanca-normativa`.  
**Condição obrigatória:** GitHub Actions secret `F01_COPILOT_PAT` com fine-grained PAT pessoal, permissão `Copilot Requests` e assinatura Copilot autorizada.  
**Primeira ativação:** pode-se também reexecutar o último run com falha de autenticação por **Re-run all jobs**, sem editar este arquivo.

Para iniciar uma rodada futura, após configurar o secret, altere APENAS o campo `request_id` abaixo via interface de edição GitHub na branch F01 e salve o commit. Esse `push` dispara três trabalhos independentes e três revisões cruzadas, com artefatos e sem `push` automático.

- request_id: F01-QA3-2026-10-19-04-COPILOT-ACTIVATED
- objetivo: verificar F01 na versão exata do novo commit e registrar relatórios independentes
- classificacao: primeira verificação independente, **NÃO homologação normativa**
- limite: F00 DONE, F01 BLOCKED, F02 não liberada
