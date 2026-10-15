# Story SIE-F00-BASELINE-PRESERVACAO — Diagnóstico e preservação do legado

## Status

**Ready for Review** — auditoria, instrumentos e QA3 concluídos; fechamento do commit/estado em andamento.

| Campo | Valor |
|---|---|
| Fase | F00; primeira de treze fases, prioridade P0 |
| Épicos de referência | EP12, EP13; interface com EP11, conforme anexo |
| Responsável pela preparação | @sm — River |
| Fonte de requisitos | Anexo `F00_EXECUTAR(1).md`, seções 0–11 |
| Autorização | Solicitação do usuário: “Execute a fase anexada.” |
| Repositório | `SFPTechnology/Projeto-SIE-2.0` |
| Branch de trabalho observada | `audit/f00-baseline-2026-10-15` |
| Commit original observado | `8d86db26f5e8675eaced4638af14bd84019e15e7` |
| Estado da fase | VALIDATING; QA3 aprovados, versionamento final em fechamento |

O anexo é a especificação operacional desta story. Seu nome de origem é `F00_EXECUTAR.md`; a cópia enviada nesta sessão é `/workspace/scratch/34018a10e5db/upload/F00_EXECUTAR(1).md`. Esta referência identifica a entrada, sem presumir que esse caminho transitório existirá em outra sessão. A implementação deve registrar o hash do anexo junto às evidências da fase.

## Story

Como responsável pela reestruturação do SIE 2.0, quero congelar a baseline observada, inventariar contratos e motores e caracterizar o comportamento legado com testes reproduzíveis, para preservar funcionalidades e resultados rastreáveis e planejar uma migração reversível sem alterar a versão publicada.

## Contexto e limites

- Esta é a primeira fase: não exige handoff de uma F00 anterior nem pressupõe inventário completo.
- `docs/sie-orchestrator/PROJECT_STATE.md` e `NEXT_ACTION.md` existem e registram entregas anteriores e bloqueios normativos. Seu conteúdo deve ser reconciliado com o SHA acessado e a evidência atual; afirmações históricas de CI não equivalem a execução nesta sessão.
- `docs/sie-orchestrator/` permanece fonte canônica do estado existente. Os documentos de F00 devem referenciá-la e registrar a fase sem substituir silenciosamente a fila anterior.
- O trabalho inclui auditoria, documentação, scripts de evidência e golden tests. Não inclui implementar motores novos, mudar contratos de produto, alterar `main`, fazer merge ou deploy, migrar dados reais, assumir custos externos ou declarar aprovação normativa/concessionária.
- Um golden test caracteriza o comportamento do código original. Não homologa um cálculo. Comparação técnica independente e memória de cálculo devem permanecer distintas da saída congelada do legado.
- Lacunas de fonte normativa e revisão profissional permanecem explícitas. Nenhum valor técnico ausente será inventado.

## Requisitos rastreáveis

| ID | Requisito | Fonte |
|---|---|---|
| RF-F00-01 | Registrar URL, branch, SHA, árvore, hashes/versões de dependências, PR e CI observáveis. | Anexo §3, 00.01 |
| RF-F00-02 | Inventariar função, arquivo, entradas, saídas, persistência, consumidores, telas e manuais com estados explícitos. | Anexo §3, 00.02 |
| RF-F00-03 | Mapear cargas, demanda, condutores, queda de tensão, proteções e EDP, incluindo regras embutidas, unidades, fontes e riscos. | Anexo §3, 00.03; §9, QA-02 |
| RF-F00-04 | Criar golden tests executáveis vinculados ao SHA original e cobrir comportamentos críticos ou explicitar lacunas. | Anexo §3, 00.04; §5 |
| RF-F00-05 | Auditar segurança e dependências, distinguindo vulnerabilidade comprovada, risco, hipótese e não verificado. | Anexo §3, 00.05 |
| RF-F00-06 | Relacionar cada LEGACY-ID a destino, contrato de entrada/saída, teste/evidência, exceção e status. | Anexo §3, 00.06 |
| RF-F00-07 | Propor manter, encapsular, refatorar, substituir ou aposentar, com reversibilidade, rollback e aprovação técnica documentada. | Anexo §3, 00.07 |
| RF-F00-08 | Publicar relatório, riscos, entregáveis, três pareceres QA e estado reconciliado, sem avanço indevido. | Anexo §3, 00.08; §§9–11 |
| CON-F00-01 | Preservar main, produção, dados e credenciais; não mascarar falhas nem alterar resultados esperados para obter aprovação. | Anexo §0, itens 4/8; §§5/7/9 |
| CON-F00-02 | Diferenciar confirmado, parcial, não identificado e não verificado; DONE apenas com todos os gates essenciais comprovados. | Anexo §§3/6/9/10 |

## Acceptance Criteria

- [x] **AC-01 — Baseline reproduzível:** URL, branch, SHA original, árvore rastreável, versões/hashes, PR e execuções de CI possuem referência verificável ou estado explícito de indisponibilidade. `main` e produção foram preservadas. (RF-F00-01, CON-F00-01)
- [x] **AC-02 — Inventário completo no escopo:** todos os módulos da baseline selecionada são mapeados com arquivos, funções, contratos, persistência, consumidores e interfaces/manuais; nenhum status é inferido pela mera existência de arquivo. A delimitação do escopo é expressa e não oculta partes não inspecionadas. (RF-F00-02)
- [x] **AC-03 — Motores e fontes rastreados:** matriz motor × regra × fonte × risco inclui as seis famílias indicadas, entradas, grandezas/unidades, saídas, parâmetros embutidos e fontes incertas marcadas NÃO VERIFICADO. (RF-F00-03)
- [x] **AC-04 — Caracterização executável:** pelo menos um caso por comportamento crítico identificado ou lacuna explícita; entradas e saídas fixadas por execução do SHA original, hashes e comando reproduzível, sem atualizar expectativas para mascarar falha. Comparações independentes são identificadas separadamente. (RF-F00-04)
- [x] **AC-05 — Riscos evidenciados:** análise de segredos sem divulgar valores, CORS, bibliotecas, permissões, licenças, rotas, migrações e código descontinuado; cada risco tem prioridade, localização/prova, alcance, estado e ação. Limitações de auditoria de dependências são documentadas. (RF-F00-05)
- [x] **AC-06 — Preservação sem equivalência falsa:** CSV relaciona LEGACY-ID, origem, entrada, saída, destino, decisão, teste, evidência, exceção e status. Destinos futuros permanecem planejados/não implementados. Nenhum módulo é chamado preservado sem prova de equivalência ou exceção formal registrada. (RF-F00-06)
- [x] **AC-07 — Migração reversível:** estratégia classifica módulos nas cinco decisões previstas, explicita ordem/dependências, critérios, rollback e aprovação técnica dentro do escopo; sem executar migração de produto nesta fase. (RF-F00-07)
- [ ] **AC-08 — Relatório e estado reais:** entregáveis obrigatórios versionáveis, cobertura, gaps, falhas, riscos, testes/comandos/resultados, alterações e próximos passos registrados; estado canônico reconciliado. F00 só é DONE se tasks essenciais e QA aplicáveis estiverem aprovados; senão BLOCKED/PENDENTE/HUMAN_REQUIRED conforme causa. (RF-F00-08, CON-F00-02)
- [x] **AC-09 — QA3 concluído:** três pareceres separados QA-01/02/03 com requisito, severidade, evidência, reprodução, correção, revalidação e veredito; achados impeditivos resolvidos ou fase retida. Nenhuma aprovação computacional é apresentada como homologação normativa. (Anexo §§6/9)

## Tasks / Subtasks

- [x] **00.01 — Congelar baseline** (AC-01)
  - [x] Registrar URL, branch, SHA, estado de trabalho, árvore e hashes do fonte e dos manifests/lockfiles.
  - [x] Identificar runtimes e dependências, PR e CI oficiais; separar observação atual de registro histórico.
  - [x] Documentar o procedimento para reproduzir o checkout e os testes sem tocar em main/produção.
- [x] **00.02 — Inventariar módulos e contratos** (AC-02)
  - [x] Mapear funções/arquivos, entradas, saídas, armazenamento, consumidores, telas e manuais.
  - [x] Conferir imports e caminhos de execução; classificar confirmado/parcial/não identificado/não verificado.
  - [x] Produzir `INVENTARIO_LEGADO.md` com cobertura e escopo verificáveis.
- [x] **00.03 — Mapear motores e fontes** (AC-03)
  - [x] Inspecionar cargas, demanda, condutores, queda de tensão, proteções e EDP na baseline.
  - [x] Documentar grandezas, unidades, premissas, regras embutidas, tabelas, edição/proveniência e risco.
  - [x] Marcar dados técnicos sem rastreabilidade como NÃO VERIFICADO, sem substituição inventada.
- [x] **00.04 — Produzir golden tests** (AC-04)
  - [x] Identificar comportamentos críticos e executar casos fixos no código do SHA original.
  - [x] Persistir entradas/saídas, hashes, referência ao código e comandos reproduzíveis.
  - [x] Executar testes, registrar falhas legítimas e distinguir caracterização de verificação matemática independente.
- [x] **00.05 — Auditar segurança e dependências** (AC-05)
  - [x] Verificar segredos, CORS, permissões, licenças, rotas, migrações e código descontinuado sem expor credenciais.
  - [x] Inventariar dependências, indisponibilidades de runtime e imports quebrados.
  - [x] Produzir `REGISTRO_RISCOS_INICIAIS.md` e mapa de dependências com severidade/evidência.
- [x] **00.06 — Construir matriz de preservação** (AC-06)
  - [x] Atribuir LEGACY-ID e vincular origem/contrato, destino, decisão, teste e evidência.
  - [x] Registrar explicitamente equivalência não comprovada, destino futuro e exceções formais.
  - [x] Produzir `MATRIZ_PRESERVACAO_FUNCIONAL.csv` coerente com o inventário e os testes.
- [x] **00.07 — Definir estratégia de migração** (AC-07)
  - [x] Classificar manter/encapsular/refatorar/substituir/aposentar com justificativa e dependências.
  - [x] Definir alterações reversíveis, critério de parada e procedimento de rollback.
  - [x] Obter parecer técnico da autoridade @architect, sem executar mudanças de produto nesta fase.
- [ ] **00.08 — Publicar relatório de baseline** (AC-08, AC-09)
  - [x] Produzir `BASELINE_CI.md` e `RELATORIO_EXECUCAO.md` com comandos, resultados e limitações reais.
  - [x] Executar QA-01, QA-02 e QA-03; corrigir inconformidades permitidas e revalidar o que foi afetado.
  - [x] Reconciliar estado em `docs/sie-orchestrator/`, checklist e File List desta story.
  - [x] Julgar os gates e registrar a retomada de F00 ou a passagem condicionada à próxima fase.

## Dev Notes e caminhos

Os entregáveis de auditoria devem ficar em `docs/implantacao-sie-2-0/F00/`, incluindo `INVENTARIO_LEGADO.md`, `MATRIZ_PRESERVACAO_FUNCIONAL.csv`, `BASELINE_CI.md`, `REGISTRO_RISCOS_INICIAIS.md`, mapa de dependências, estratégia de migração e `RELATORIO_EXECUCAO.md`. Scripts/fixtures e testes devem respeitar os runners e camadas encontrados no repositório. O desenvolvedor registrará seus caminhos reais na File List; os nomes de artefatos auxiliares não representam implementação existente.

O `package.json` raiz observado define `lint`, `typecheck`, `test` e `build` via `scripts/validate-sdc-auto-1.js`. Isso é uma fronteira de quality gates e não prova cobertura de todos os motores. Identificar e executar também os runners de produto pertinentes antes de julgar cobertura. (Fonte: `package.json#scripts`.)

Os arquivos `docs/framework/tech-stack.md`, `source-tree.md` e `coding-standards.md` configurados em `.aiox-core/core-config.yaml` não foram encontrados na preparação; os fallbacks `docs/pt/framework/` também não existem. Registrar essa lacuna sem inventar stack ou tratar referência ausente como evidência. Requisitos desta story vêm diretamente do anexo e das regras observadas em `AGENTS.md` e `.aiox-core/constitution.md`.

Nenhuma decisão arquitetural nova é tomada por esta story. @architect aprova o roteiro técnico; @dev implementa instrumentos de auditoria e testes; @qa emite os vereditos. Operações remotas, se cabíveis e autorizadas, pertencem a @devops; não há autorização implícita para merge/deploy.

## Testing e quality gates

1. Capturar checkout/SHA e ambiente antes da caracterização; usar ambiente isolado sem serviços de produção.
2. Executar os testes disponíveis e pertinentes à baseline e os golden tests, preservando stdout/stderr, exit code e comando. Distinguir teste não executado, ignorado, bloqueado e aprovado.
3. Rodar `npm run lint`, `npm run typecheck`, `npm test` e `npm run build`; falhas pré-existentes são registradas e classificadas. Não usar o verde desses wrappers como substituto de testes de produto.
4. Para motores, cobrir entradas/saídas com unidades, casos de fronteira e cálculo independente quando verificável. Fonte normativa ausente permanece lacuna; teste computacional não libera conformidade.
5. Retestar correção específica e regressões afetadas. Não editar saídas esperadas apenas para ocultar defeito.
6. Antes do fechamento, verificar diff, ausência de mudança de produto/main/produção, CSV e Markdown legíveis, referências existentes e estado consistente.

## CodeRabbit Integration

**Configuração observada:** habilitada em `.aiox-core/core-config.yaml`, com degradação permitida se CLI ausente. Disponibilidade e execução ainda NÃO VERIFICADAS; registrar o resultado real, sem simular parecer.

| Aspecto | Planejamento de qualidade |
|---|---|
| Tipo | Auditoria de baseline; secundários: segurança, integração e caracterização |
| Agentes | @dev implementação; @architect estratégia; @qa pareceres; @devops somente operações remotas autorizadas |
| Pre-commit | Runners pertinentes, golden tests, lint/typecheck/test/build, diff e verificação de segredos |
| Pre-PR | Somente se houver PR autorizado; revisão de @qa e @devops |
| Pre-deployment | Não aplicável à F00; deploy fora do escopo |
| Self-healing | @dev light: até 2 iterações/15 minutos para CRITICAL; @qa full: até 3 iterações/30 minutos para CRITICAL/HIGH; limites não autorizam modificar produto fora do escopo |
| Foco | Vínculo ao SHA original, contratos, cobertura, equivalências, fontes, segurança e nenhuma expectativa adulterada |

## QA Results — revisão concluída

Três revisões de IA ou três perspectivas da mesma LLM **não equivalem a três auditores humanos independentes**. Decisão profissional necessária deve permanecer explicitamente pendente. A aprovação de QA nesta fase trata da auditoria, não da conformidade dos cálculos.

| Revisor | Veredito | Critérios confrontados |
|---|---|---|
| QA-01 — Arquitetura, código e testes | APROVADO | Árvore/contratos/imports; origem real dos golden tests; LEGACY-ID → destino → teste → decisão |
| QA-02 — Engenharia elétrica e normas | APROVADO | Grandezas/unidades/premissas/fontes; casos independentes; riscos e ausência de homologação presumida |
| QA-03 — Integração, dados, segurança e UX | APROVADO | Credenciais, rotas, dependências, instruções, perda de dados, rollback e distinção dos estados |

Cada parecer deve registrar requisito, gravidade CRITICA/ALTA/MEDIA/BAIXA, prova por arquivo/linha/teste/log/commit, reprodução, risco, correção e revalidação. Vereditos permitidos: APROVADO/REPROVADO/BLOQUEADO/PENDENTE.

## Checklist de fechamento

- [x] Tasks 00.01–00.08 possuem evidência verificável.
- [x] Entregáveis obrigatórios existem e correspondem ao SHA auditado.
- [x] Comportamentos críticos possuem caracterização ou lacuna justificada.
- [x] Riscos, falhas e dependências estão classificados sem ocultação.
- [x] QA-01 APROVADO no escopo aplicável.
- [x] QA-02 APROVADO no escopo aplicável, sem concessão normativa indevida.
- [x] QA-03 APROVADO no escopo aplicável.
- [x] File List e estado canônico estão atualizados.
- [x] Branch main, dados e sistema publicado estão preservados.
- [x] Gate de passagem foi decidido com evidências; caso contrário, permanece retomada de F00.

## Dev Agent Record

### Modelo utilizado

Codex; a versão específica do modelo não foi registrada em metadado verificável desta execução.

### Debug Log References

Logs em `docs/implantacao-sie-2-0/F00/evidencias/`:134 pytest, 35 golden incluídos, replay 34, 3 Chromium, 18 tooling; quatro gates raiz e pip check exit 0. O @sm criou a story antes do código.

### Completion Notes

Execução do anexo concluída no escopo de auditoria/testes/documentação, com 37 IDs e exceções formais; QA-01/02/03 e roteiro de arquitetura aprovados. Estado canônico VALIDATING até o fechamento versionado; as 12 atividades anteriores foram preservadas. Produto/main/produção sem alteração.

### File List

| Arquivo | Ação | Estado |
|---|---|---|
| `.github/workflows/sie-restructuring-api.yml` | Modificado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/BASELINE_CI.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/ESTRATEGIA_MIGRACAO.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/F00_EXECUTAR.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/INVENTARIO_LEGADO.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/MAPA_DEPENDENCIAS.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/MATRIZ_MOTORES_FONTES.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/MATRIZ_PRESERVACAO_FUNCIONAL.csv` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/PARECER_ARQUITETURA.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/QA-01.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/QA-02.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/QA-03.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/REGISTRO_RISCOS_INICIAIS.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/RELATORIO_EXECUCAO.md` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/aiox-tests.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/api-regression.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/arvore-baseline.txt` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/baseline-api.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/baseline.json` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/browser-e2e.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/build.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/clean-api-regression.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/clean-dependency-check.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/clean-golden-replay.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/fontes-sha256.json` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/github-ci-baseline.json` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/golden-replay.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/golden-tests.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/lint.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/python-installed.txt` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/runtime.json` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/scheduler-state.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/source-inventory-help.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/test-results.json` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/typecheck.log` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/web-syntax.log` | Criado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/DEPENDENCY_GRAPH.md` | Modificado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/EXECUTION_HISTORY.md` | Modificado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/EXECUTION_QUEUE.md` | Modificado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/NEXT_ACTION.md` | Modificado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` | Modificado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/PROJECT_STATE.md` | Modificado | Validado; fechamento versionado pendente |
| `docs/sie-orchestrator/TECHNICAL_DECISIONS.md` | Modificado | Validado; fechamento versionado pendente |
| `docs/stories/story-SIE-F00-BASELINE-PRESERVACAO.md` | Criado | Validado; fechamento versionado pendente |
| `restructuring/README.md` | Modificado | Validado; fechamento versionado pendente |
| `restructuring/apps/api/tests/fixtures/f00_legacy_golden.json` | Criado | Validado; fechamento versionado pendente |
| `restructuring/apps/api/tests/test_legacy_golden.py` | Criado | Validado; fechamento versionado pendente |
| `restructuring/docs/MANUAL-OPERACIONAL.html` | Modificado | Validado; fechamento versionado pendente |
| `scripts/f00_golden.py` | Criado | Validado; fechamento versionado pendente |
| `docs/implantacao-sie-2-0/F00/evidencias/precommit-consistency.log` | Criado | Validação de coerência exit 0 |

## Change Log

| Data | Versão | Descrição | Autor |
|---|---|---|---|
| 2026-10-15 | 1.0 | Story de auditoria F00, requisitos rastreáveis, AC e tarefas pendentes; execução integral autorizada pelo usuário. | @sm — River |

| 2026-10-15 | 1.1 | Execução F00, instrumentos, evidências, riscos e QA3 concluídos; versionamento em fechamento. | @dev/coordenador |
