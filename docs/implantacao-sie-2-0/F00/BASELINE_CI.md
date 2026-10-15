# F00 — Baseline, ambiente e testes

Data: 2026-10-15. Este documento registra a caracterização do snapshot selecionado; não certifica a engenharia nem a segurança de uma implantação.

## Revisões efetivamente observadas

| Campo | Valor |
|---|---|
| Repositório | https://github.com/SFPTechnology/Projeto-SIE-2.0 |
| Branch de origem | `refactor/sie-2-foundation-2026-10-14` |
| Commit original | `8d86db26f5e8675eaced4638af14bd84019e15e7` |
| Branch isolada F00 | `audit/f00-baseline-2026-10-15` |
| Main observada | `2eee08d126d7bab0a0fe7b7d96b25004ac545447` |
| PR anterior | [#1](https://github.com/SFPTechnology/Projeto-SIE-2.0/pull/1), aberto, draft, base main |
| Árvore completa | `evidencias/arvore-baseline.txt`: 12.127 entradas rastreadas, modos/blobs/tamanhos |
| Hashes | `evidencias/baseline.json`: árvore Git, SHA256 do manifesto, anexo e 55 arquivos operacionais/configurações |

A cópia local anterior estava atrasada e continha dois commits locais; ela foi preservada. A F00 usa worktree nova no head remoto observado, não a revisão antiga. Não há fase anterior exigível: F00 é a primeira fase. A governança existente é mantida em `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`.

O `.gitmodules` aponta para outro repositório sem gitlink no snapshot. A consulta ao repositório legado e à branch nele indicada retornou 404/not found no conector nesta sessão. Isso comprova indisponibilidade de acesso por essa via; não permite concluir se foi removido, renomeado ou tornado privado. Os extratos e pacotes históricos permanecem inventariados como evidência estática.

## CI do SHA original, consultada nesta execução

| Workflow | Run/job | Resultado observado |
|---|---|---|
| API modular | [38614258541](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38614258541), job 116025158079 | success; log confirma **99 passed, 1 warning**, sintaxe JS e 6 fontes hashadas |
| Chromium real | [38614258229](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38614258229), job 116025157702 | success; log confirma **3 passed** |
| AIOX raiz | [38614258449](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38614258449), job 116025158291 | success; steps npm ci, lint, typecheck, test e build |

`get_commit_combined_status` retornou lista de statuses vazia; não foi interpretada como aprovação nem como CI pendente. Os workflows/jobs e dois logs foram consultados separadamente. O wrapper de runs consultado filtra eventos de PR e primeira página; não é uma lista universal de toda a CI. Resumos estruturados: `evidencias/github-ci-baseline.json`.

## Execução local e reprodução limpa

| Verificação | Resultado | Evidência |
|---|---|---|
| Suíte preexistente, excluindo novo arquivo | 99 passed, 1 warning | `evidencias/baseline-api.log` |
| Captura/replay do código original | 34 cenários, igualdade completa | `evidencias/golden-replay.log` |
| Novo pacote golden | 35 passed: 34 cenários + metadados | `evidencias/golden-tests.log` |
| Regressão API/domínio/CLI/SQLite/scheduler | 134 passed, 1 warning | `evidencias/api-regression.log` |
| Regressão em venv criada nesta sessão | 134 passed, 1 warning | `evidencias/clean-api-regression.log` |
| Replay em venv limpa | 34 cenários iguais | `evidencias/clean-golden-replay.log` |
| Dependências da venv limpa | pip check exit 0 | `evidencias/clean-dependency-check.log` |
| Gates raiz | lint/typecheck/test/build exit 0; 18 testes AIOX | logs `lint`, `typecheck`, `aiox-tests`, `build` |
| JavaScript da UI | node --check exit 0 | `evidencias/web-syntax.log` |
| Chromium local em ambiente isolado | 3 passed em 8,24 s, exit 0 | `evidencias/browser-e2e.log` |
| Fontes documentais | 6 presentes, 0 ausentes, conformidade false | `evidencias/fontes-sha256.json` |

O estado/resultado da execução local de Chromium é registrado em `evidencias/browser-e2e.log` e `evidencias/test-results.json`. A evidência de CI acima permanece identificada separadamente. O resumo consolidado de F00 informa o resultado final observado.

O Python padrão inicialmente não possuía pytest. Primeiro foram recuperadas dependências instaladas de trabalho anterior, com `PYTHONPATH` explícito apontando o código desta worktree. Em seguida foi criada venv nova, instaladas as versões exatas de `evidencias/python-installed.txt` e repetida a suíte sem importar o código anterior. `evidencias/runtime.json` distingue esses ambientes. A dependência AIOX local é reutilizada; a instalação limpa por lockfile foi observada na CI do SHA original. Não houve instalação de runtimes históricos arquivados.

Versões locais principais: Python 3.12.14; pytest 9.1.1; FastAPI 0.143.0; Pydantic 2.14.1; httpx 0.28.1; uvicorn 0.54.0; Node 24.19.0; npm 11.9.0. A CI original usou Python 3.12.15/FastAPI 0.143.1, conforme logs oficiais: não foi presumida identidade de ambiente. O warning é a depreciação Starlette TestClient/httpx; não foi suprimido. npm registra aviso de configuração `http-proxy` sem impedir os gates.

## Como reproduzir

Na raiz de checkout da branch F00, com Git, Node e Python 3.12 disponíveis:

```bash
python -m venv .venv-f00
# Ative a venv conforme seu sistema; no Windows: .venv-f00\Scripts\activate
python -m pip install -r docs/implantacao-sie-2-0/F00/evidencias/python-installed.txt
python -m pip install --no-deps -e ./restructuring/apps/api
python -m pytest -q restructuring/apps/api/tests
python scripts/f00_golden.py --verify
npm ci --prefix .aiox-core --ignore-scripts --no-audit --no-fund
npm run lint
npm run typecheck
npm test
npm run build
```

O replay requer que o commit original esteja acessível no histórico Git. A CI foi ajustada com `fetch-depth: 0` e um step explícito de replay; alterações no script também acionam o workflow. Em checkout raso, obter o SHA original é pré-requisito. A instalação `--no-deps -e` pode baixar ferramentas de build, mas não atualiza os pacotes congelados. O snapshot de versões é uma evidência deste teste; não substitui uma política de lock/hashes de distribuição para releases futuras.

Para o navegador, instalar o extra `.[e2e]` da API e Chromium, conforme `restructuring/docs/TESTE-E2E-NAVEGADOR.md`, e executar `python -m pytest -q restructuring/e2e` com portas 8000/5173 livres. A sessão usou Playwright 1.55.0, Chromium Headless Shell build 1187. Todos os serviços de teste usam loopback e SQLite temporário. Nenhuma credencial de produção é necessária.

## O que os golden tests comprovam

`scripts/f00_golden.py --capture <arquivo-novo>` extrai os 14 módulos Python por `git show` no SHA fixo, grava-os em diretório temporário e executa um subprocesso cujo pacote carregado deve estar dentro dessa extração. A captura inicial de 34 entradas/saídas está em `restructuring/apps/api/tests/fixtures/f00_legacy_golden.json`, com SHA original e hashes dos módulos. A operação recusa sobrescrever arquivos. `--verify` compara o documento inteiro com nova execução do mesmo SHA e não modifica expectativas.

Casos: quedas mono/trifásicas e comprimento zero; arredondamento; seleção/limiar/erro de condutor; seleção/erro de disjuntor; gate sem fonte e flags de cliente; análise integrada; 13 categorias EDP e bloqueios; persistência SQLite com revisões, conflito, reabertura e histórico. O relógio é omitido explicitamente no snapshot de SQLite; ids, nomes, dados, revisões e ações são preservados. CLI, API de armazenamento, scheduler e UI têm os testes existentes citados na matriz, não saídas inventadas.

Os casos `ANALISE-IZ-ARREDONDADO` (ENG-001) e `EDP-U-CARGA-TRIFASICA` (ENG-002) fixam anomalias conhecidas. Passar nesses snapshots significa reproduzir o comportamento observado, não aceitá-lo como projeto correto. A desigualdade independente de Iz e os casos aritméticos estão na matriz de motores/QA-02. Casos de engenharia futura devem corrigir a causa com exceção/mudança de contrato deliberada, mantendo intacta a evidência histórica.

## Limites e gates

- Os scripts raiz validam uma fronteira AIOX, sem compilar o TypeScript incompleto de `src/` nem homologar motores.
- Não existe equivalência executável demonstrada entre o legado externo indisponível, snapshots e o novo runtime. Essas lacunas têm exceções na matriz de preservação.
- Catálogos normativos, identidade de produção e módulos completos mantêm os bloqueios anteriores. Nenhum resultado de teste concede aprovação ABNT/EDP/NR-10.
- A auditoria estática de SQL não comprova estado de um banco instalado. Auditoria CVE online abrangente e CodeRabbit não foram executados; disponibilidade/limites estão no registro de riscos.
- O commit de entrega e a decisão dos gates são registrados no relatório e no PR da F00. A baseline original permanece imutável.

## Versionamento e formato das evidências

O pacote foi versionado no commit local real `8797f616f07c3866833db4eb463e050ece76420d` (50 arquivos, incluindo 16 logs adicionados explicitamente). O fechamento DONE e os registros derivados pertencem ao commit seguinte da mesma branch. A checagem staged padrão sinalizou hard breaks da cópia imutável do anexo e finais CRLF do CSV; ambas preservam os formatos intencionais. A conferência configurada com `cr-at-eol` e exclusão somente desse anexo passou. O CSV foi lido como 37 linhas/19 colunas e o anexo conferido por SHA256; não houve alteração da entrada do usuário para silenciar o check.

A primeira instalação do navegador falhou durante download/descompactação e atualização do lock local. A recuperação mudou para o host de download alternativo e instalação `--only-shell` em diretório novo; então Chromium1187/FFmpeg foram instalados e os 3 E2E executados com sucesso. Isso foi falha de preparação do runtime, sem alteração de teste esperado ou aplicação.

### Publicação do checkpoint

O checkpoint local `8797f616f07c3866833db4eb463e050ece76420d` tem equivalente remoto [`ab12904`](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/ab129046716b5bcff62bd5ca2f0cb470b7c0f077), com a mesma árvore `904e4a84de7d772a8915c4d79b5e27aa130959c1`. O push HTTPS pelo terminal falhou por autenticação ausente; a publicação usa o conector GitHub já autorizado. Autoria/data do commit geram SHA diferente e o mapeamento é explícito em `evidencias/publication-map.json`. O snapshot de arquivos, fixture e testes não mudou.
