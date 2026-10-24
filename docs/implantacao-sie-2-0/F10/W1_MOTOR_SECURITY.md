# W1 — revisão independente de segurança da execução do motor

Responsável: agente separado `w1_motor_security`. Data: 24/10/2026. Branch `feat/f09-concessionarias-especializadas`, HEAD `52b74702d4e55258b287fc8211240ff6e00dffaa`, diff local de implementação. Esta evidência não representa CI nem revisão de commit final.

## Escopo e resultado

Inspecionados `storage.executar_calculo_f10`, `consultar_calculo_f10`, `_fonte_calculo_f10`, tabela/triggers `execucoes_motor_f10`, adaptador e CLI em `persisted_source_f10.py`, contrato de motor e validadores `InstallationSnapshot`/`CalculationRecord`.

A geração exige evidência persistida; run apenas declarado VALID não atende. A execução usa entrada carregada da revisão histórica, verifica digest do snapshot, executa `analyze_legacy`, compara hashes e versões e grava evidência append-only em transação SQLite. A leitura verifica identidade externa/interna, versões, hashes e resultado canônico. Não se identificou bloqueante reproduzível nesse recorte e trust boundary.

## Evidências executadas

- Comando: `python -m pytest -q tests/test_storage.py tests/test_persisted_source_f10.py tests/test_persisted_source_f10_sqlite.py`.
- Diretório: `restructuring/apps/api`.
- Resultado: 39 passed, 1 warning, 2.67s, exit 0. Aviso de depreciação Starlette/httpx.
- Adversarial adicional em SQLite temporário: executar motor real usando fixture `test_storage.motor_revision`, remover trigger de UPDATE somente no banco de teste e alterar evidência recomputando digest; consultar pelo vínculo original.
- Campos alterados individualmente: `project_id`, `run_id`, `source_sha256`, `revision`, `schema_version`.
- Resultado: cinco alterações rejeitadas com ValueError; script exit 0. Não alterou fixture ou banco produtivo.

## Limites

Hashes e triggers são controles de integridade dentro de armazenamento local confiável. Não são assinatura e não protegem contra administrador/processo com capacidade arbitrária de reescrever simultaneamente banco, histórico, código e filesystem. Locks de publicação são cooperativos; troca maliciosa de ancestrais/symlinks por ator local externo não é comprovadamente eliminada. Manter diretório e DB privados ao proprietário local; não alegar ACL multiusuário.

Não houve concessão de homologação normativa ou profissional. QA independente final, regressão completa, SHA candidato e CI aplicável continuam sendo decisões separadas. Qualquer alteração posterior exige rever a evidência afetada.
