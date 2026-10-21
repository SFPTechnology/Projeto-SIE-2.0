# F03 — Persistência, segurança e infraestrutura de dados
Data: 21/10/2026. Estado: **DONE — implementação, QA3 e CI do mesmo SHA aprovados**.
Branch: `feat/f03-persistencia-seguranca`; base F02 `3d7780c5107ac217bffb10326fac37a2debf69aa`.
F02 DONE e passagem conferidas em seu relatório e orquestrador. F00, aceites F01, domínio F02 e main preservados.

|Task|Resultado|Evidência|
|---|---|---|
|03.01|Inventário tabelas/índices/triggers/FK e destino aditivo|MATRIZ_DADOS_PERSISTENCIA.md; storage.py|
|03.02|SQLite local, sem novo ORM; PostgreSQL produção projetado|ADR_ARMAZENAMENTO.md|
|03.03|Migração001 transacional, downgrade, recusa perda de tombstones|data_lifecycle.py; MIGRACOES_VERSIONADAS; testes F03|
|03.04|criado_em, atualizado_em, autor local, revisão otimista, histórico imutável, arquivamento interno sem DELETE|storage.py; testes de conflito/lock/arquivo parcial|
|03.05|Token opt-in legado + peer loopback, produção bloqueada, erros sanitizados|main.py; test_storage_api.py; test_lifecycle_f03.py|
|03.06|Contas, organizações, papéis, ownership e cenários negativos projetados|MATRIZ_RBAC_RLS.md; identidade/RLS de produção não implementados|
|03.07|APIs CRUD não destrutivas e snapshot F02 preservados; CLI backup/restore|regressão API/CLI F02; CLI data_lifecycle|
|03.08|Backup online e restore isolado verificados, destino exclusivo0600|PLANO_BACKUP_RESTORE.md; teste restore com revisão e decimal longo|
|03.09|Conflito, banco bloqueado/corrompido, migração parcial, UUID e acesso indevido|test_lifecycle_f03.py e regressão; cross-tenant real não aplicável sem identidade|
|03.10|DEV/TEST, prod bloqueado, sem rollout|GUIA_AMBIENTES.md; teste prod503|

## Correções após revisão crítica
Novo banco agora nasce0600; banco existente mantém modo (requer diretório privado). Eventos antigos permanecem LEGACY_UNKNOWN; novas operações LOCAL_OWNER, sem atribuir autor humano. Erros SQLite retornam503 sanitizado, sem caminhos ou token. Snapshot normativo não é alterado nem promovido por migração/restore. Não houve ajuste de cálculo ou relaxamento de resultado esperado.

## Testes
- F00 golden:34PASS, fixture original intacta.
- npm lint/typecheck/test/build:PASS;18casos da suíte AIOX.
- F03 focados:12PASS; inclui banco bloqueado, arquivo corrompido, novo modo0600, downgrade/reupgrade, restore, autor e bytes normativos.
- `PYTHONPATH=restructuring/apps/api python -m pytest restructuring/apps/api/tests -q`: **551 passed**,1aviso,15,55s;12F03 incluídos na contagem.
- Aviso existente Starlette/TestClient, sem falha.
- Sem novo E2E de interface: esta fase não alterou formulários/UI; integraçãoHTTP/CLI e compatibilidade cobertas por suíte existente. CI de navegador, quando observado, será registrado separadamente.

## QA3
|Parecer|Estado no escopo local/design produção|Registro|
|---|---|---|
|QA-01 arquitetura/código/testes|APROVADO após correções|QA-01.md|
|QA-02 engenharia/normas|APROVADO na preservação de dados/contratos|QA-02.md|
|QA-03 integração/dados/segurança|APROVADO após correções|QA-03.md|
Revisão computacional delegada em três perspectivas; não equivale a três auditorias humanas ou homologação normativa.

## Gates e limites
Leitura/escrita/revisão local, rollback/restore isolados e acessos negativos demonstrados. Produção permanece condicionada e bloqueada: contas, organizações e RLS apenas projetados; não são denominados testes multiusuário. Retenção/cifragem são política proposta, não rotina instalada. Arquivamento preserva histórico e não é eliminação LGPD. Backup valida integridade SQLite/FK; histórico também tem digest na leitura. Não foi examinado banco ativo nem executada migração PostgreSQL/Supabase legada.
F03 concluída no escopo autorizado. Passagem liberada para desenvolvimento da F04. Próximo arquivo: **F04_EXECUTAR.md**. Nenhum merge/deploy ou custo Copilot.


## Publicação e encerramento
Commit de código: `61e65e980960ecbf23cc846a9ac4d7645096fc03`.

|Workflow|Resultado no mesmo SHA|Evidência|
|---|---|---|
|API/F00|SUCCESS;551pytest,1aviso,10,08s;34golden,fixture intacta|https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39595433472|
|AIOX|SUCCESS;lint/typecheck/test18/build|https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39595433149|
|Chromium|SUCCESS;17testes,31,41s|https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39595433124|

Código publicado em https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/61e65e980960ecbf23cc846a9ac4d7645096fc03 . Árvore local conferida idêntica à remota. Estes resultados pertencem ao SHA de código; o encerramento posterior altera somente registros documentais. QA-01/02/03 pertencem ao incremento contido nesse commit. CodeRabbit CLI indisponível; nenhuma execução desse serviço é afirmada. Identidade/RLS de produção permanecem projetados conforme task03.06, sem impedir a entrega local exigida pelo artefato.
