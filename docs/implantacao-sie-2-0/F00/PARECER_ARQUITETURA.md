# Parecer de arquitetura — roteiro técnico da F00

**Decisão arquitetural: APROVADO, exclusivamente para a classificação e o roteiro de migração da tarefa 00.07.** Não foram executadas alterações de arquitetura de produto, migrations, troca de motores ou integração nova por este parecer. A aprovação não encerra a F00: o julgamento dos gates e os três vereditos QA pertencem ao fechamento próprio da fase.

| Identificação | Evidência |
|---|---|
| Data | 2026-10-15 |
| Papel responsável | @architect — Aria; revisão por IA, sem representar assinatura profissional ou revisão humana independente |
| Autoridade | `AGENTS.md`; `.aiox-core/constitution.md`, princípio II; definição integral em `.aiox-core/development/agents/architect.md` |
| Requisito | Anexo `F00_EXECUTAR(1).md`, tarefa 00.07; story `docs/stories/story-SIE-F00-BASELINE-PRESERVACAO.md`, RF-F00-07/AC-07 |
| Repositório | `SFPTechnology/Projeto-SIE-2.0` |
| Branch inspecionada | `audit/f00-baseline-2026-10-15` |
| Baseline | `8d86db26f5e8675eaced4638af14bd84019e15e7` |
| Documentos submetidos | `ESTRATEGIA_MIGRACAO.md`, `MATRIZ_PRESERVACAO_FUNCIONAL.csv`, `MAPA_DEPENDENCIAS.md`, inventário e matriz de motores da pasta F00 |

## 1. Base observada e limite da aprovação

A estratégia foi lida integralmente e confrontada com os contratos reais em `restructuring/apps/api/sie_api/`, a UI estática, os artefatos TypeScript incompletos e os ADRs/bloqueios em `docs/sie-orchestrator/`. A revisão não supôs que documentação de implementação histórica corresponda a runtime integrado nesta baseline.

Versões dos documentos efetivamente revisados, fixadas por SHA-256 após a atualização da matriz com os golden:

| Documento nesta pasta | SHA-256 |
|---|---|
| `ESTRATEGIA_MIGRACAO.md` | `d8786615c33d13b4584de4216546c57c7737524b82211def68ee33eb3baaf6a8` |
| `MATRIZ_PRESERVACAO_FUNCIONAL.csv` | `11747f07e58f469cf46e60a14f0c76718a91ebbf3b5be820f07fca0135d47187` |
| `MAPA_DEPENDENCIAS.md` | `447d21443267fa4e56638a9e5d8dec8129b21c9f3f74585feb4b413187de26c2` |

Mudança posterior que altere classificação, contrato, dependência, equivalência ou rollback exige confrontar novamente o trecho afetado antes de reutilizar esta decisão. Atualizar apenas o texto de status para referenciar este parecer não muda a decisão arquitetural.

A matriz contém 37 LEGACY-IDs distintos e contíguos. Uma conferência local por `csv.DictReader`, com separador `;` e UTF-8 BOM, confirmou decisões do conjunto permitido e preenchimento de equivalência, teste/lacuna, evidência e exceção. Os destinos ainda não executáveis são identificados como `LACUNA_FORMAL`; `RETIDO_BASELINE` significa retenção do comportamento atual, sem comprovar portabilidade ou equivalência de implementação futura. Esta verificação estrutural do CSV não substitui os três QA.

As classificações e os procedimentos descritos são suficientes para a tarefa 00.07 porque conservam os contratos identificados, delimitam as lacunas e exigem evidência antes da troca. Não estabelecem um destino implementado para motor ausente nem concedem licença para aplicar as migrations arquivadas.

## 2. Decisões aprovadas

| Decisão | IDs | Aprovação e motivo |
|---|---|---|
| Manter | 001–002, 007, 010–020, 031 | Reter os 15 comportamentos/ferramentas existentes sem reescrita nesta fase. Preservar os limites de integração e segurança documentados. |
| Encapsular | 003–006, 008–009 | Isolar os seis contratos de cálculo/análise/EDP em futura story, preservando unidades, erros, precisão e gate. Não criar equivalência entre modelo simplificado e dimensionamento completo. |
| Encapsular após recuperar dependências | 021–022 | Preservar otimizador/schema TypeScript como artefatos parciais. Imports `../modelo/tipos` e `./validadores` ausentes em `src/domain/calculo/otimizador.ts:6–20` impedem execução/equivalência C1–C6. |
| Encapsular como legado inativo | 024–028 | Reter cinco grupos de SQL/pacotes gráficos. Adapters futuros dependem de cadeia de schema, consumidores, bibliotecas e teste isolado; arquivo preservado não significa função operacional. |
| Substituir após projeto e recuperação de contrato | 023, 029–030, 032–037 | Nove grupos sem equivalência demonstrada. A decisão registra a direção proposta, não um substituto já aprovado. Recuperação do original ou aceitação expressa da ausência deve anteceder especificação e comparação do candidato. |
| Refatorar | Nenhum nesta F00 | Não há alteração de runtime necessária para o diagnóstico. Reavaliar somente por story e evidência de benefício/compatibilidade. |
| Aposentar | Nenhum nesta F00 | Não há prova suficiente de desuso ou cobertura equivalente. Preservar código, dados de referência, SQL, ZIPs e documentos históricos. |

As cinco opções de decisão foram consideradas. A ausência de candidatos a refatorar/aposentar é uma decisão explícita, não uma lacuna de classificação. O total é consistente com o CSV: 15 manter, 13 encapsular e 9 substituir.

## 3. Interfaces e invariantes obrigatórios

| Fronteira | Contrato confirmado | Condição para mudança futura |
|---|---|---|
| Cálculo e análise | `engines.py:34–43,54–69,80–128`; `application.py:9–26`: Decimal interno, unidades explícitas, apresentação arredondada e erros definidos | Comparar entrada, resultado, erros e precisão no SHA antigo e no candidato. Diferença elétrica não pode ser removida por normalização. |
| HTTP | `main.py:48–99`; `storage_api.py:12–60`: rotas, campos JSON e respostas 401/404/409/422/503 | Versionar ou adaptar qualquer quebra; preservar consumidores existentes e TestClient/E2E pertinentes. |
| CLI | `cli.py:36–85`: salvar/carregar/historico, UUID, JSON stdout, códigos 0/2/3/4; `scheduler_cli.py:15–69`: operações de estado | Biblioteca/CLI funcional antes de expandir UI, conforme Constitution I. A CLI atual de projetos não comprova CLI de todos os motores futuros. |
| Persistência local | `storage.py:49–103`: revisão esperada, conflito sem sobrescrita, limite JSON, transação e eventos de ação/revisão | Não converter histórico de ações em promessa de restauração de versões; preservar UUID, revisão e dados em comparação/restauração. |
| Liberação de engenharia | `domain/gates.py:21–32`: ausência de evidência bloqueia; referência declarada mantém PENDENTE; flags do cliente não aprovam | Conservar o fechamento preventivo. Um novo mecanismo de aprovação exige requisitos, identidade, fonte, revisão e testes próprios. |
| EDP | `domain/edp.py:49–65`: sugestão por corrente, alertas e `liberado_para_padrao_entrada=False` | Não tratar catálogo, candidato ou metadado herdado VERIFICADO como elegibilidade da instalação. |
| Estado operacional | `scheduler.py`; ADR-SIE-008/011: JSON canônico e fila, sem bridge de execução | Manter um escritor por workspace enquanto não houver lock; uma transição de estado não prova ação externa executada. |
| UI e gráficos | `apps/web/app.js`; pacotes históricos de unifilar/DXF sem integração comprovada | Integrar a contratos já estabilizados e verificar E2E/arquivo exportado; não presumir cobertura por protótipo ou ZIP. |

Os gates AIOX raiz não compilam nem comprovam o produto TypeScript incompleto; `package.json` chama `scripts/validate-sdc-auto-1.js`. A estratégia separa corretamente tooling, testes Python e navegador real.

## 4. Reversibilidade e dados

O plano distingue corretamente reversão de código de restauração de banco. Aceito o procedimento proposto: SHA e branch isolados; adapter opt-in; conservação do formato compatível; backup consistente e ensaio de restauração antes de qualquer futura alteração de schema/dados; comparação de dados, UUID, revisão, conflitos e histórico na cópia restaurada. Não se deve executar `reset` destrutivo no trabalho compartilhado.

Para SQLite, parar escritores ou usar seu mecanismo de backup consistente; copiar somente o arquivo principal durante escrita não é procedimento aprovado. `RepositorioProjetos.historico()` guarda ação/revisão/instante, sem snapshots dos conteúdos anteriores, conforme `storage.py:78–103`.

Para Postgres/Supabase, a F00 apenas conserva os arquivos. Cadeia completa de schema, backup e restauração testados, constraints e políticas por identidade são pré-requisitos da story futura. Reverter um commit SQL não desfaz DDL nem recupera dados. Políticas arquivadas amplas e FKs não resolvidas não podem ser carregadas em produção como etapa de preservação.

Para o JSON do scheduler, preservar snapshot/histórico antes de mutação autorizada e validar a cópia restaurada; `replace` atômico com revisão otimista não oferece exclusão mútua entre processos. Restaurar o arquivo não desfaz efeitos externos. Normas e extrações permanecem versionadas por hash/edição/proveniência; troca do dado exige trilha de revisão.

Esses procedimentos são **plano avaliado**, não ensaios de migração/restauração já executados nesta revisão.

## 5. Pendências preservadas e critérios de parada

| Pendência | Evidência | Efeito sobre a decisão |
|---|---|---|
| Iz arredondada influencia seleção de proteção | `engines.py:104` → `application.py:17`; golden `ANALISE-IZ-ARREDONDADO`: Iz bruta 19,995 A versus In 20 A | Anomalia conhecida deve continuar caracterizada. Correção futura necessita teste matemático separado e diferença versionada; não editar a fixture antiga para ocultá-la. |
| Modalidade EDP e carga trifásica incompatíveis podem retornar candidato | `edp.py:49–65`; cenário U com carga trifásica e liberação false | Não homologar. Regra corrigida depende de aplicabilidade confirmada e regressão própria, mantendo o caso legado. |
| Motores completos e contratos históricos ausentes/parciais | LEGACY-021–030 e 032–037; mapa de dependências | Não declarar equivalência nem aposentar legado. Recuperar código/casos ou formalizar a ausência antes da implementação futura. |
| Fontes e dados técnicos ainda não liberados | NOR-01, NOR-02 e EDP-01 no registro canônico; matriz de motores/fontes | Conservar bloqueios. Hash, cópia local, golden e rótulo documental não são homologação normativa. |
| Identidade e ambiente de produção não definidos | SEC-01; API local opt-in/token em `storage_api.py:23–34` | Manter localhost/escopo local; sem migração real, publicação ou abertura multiusuário. |

Qualquer quebra de contrato sem tratamento explícito, divergência elétrica sem análise, perda de revisão/dados, bypass do gate, falta de fonte exigida ou restauração não demonstrada interrompe a etapa futura afetada. Tarefas independentes e seguras podem continuar, sem presumir resolução dessas dependências.

## 6. Encaminhamento

`ESTRATEGIA_MIGRACAO.md` está **aprovada tecnicamente no escopo F00**, em conjunto com as delimitações deste parecer. O documento pode conservar a identificação de proposta preparada pelo inventário e referenciar esta decisão para seu status de revisão.

Cabe ao @qa confrontar inventário, golden, riscos e relatório e emitir QA-01/02/03; cabe ao fechamento conferir todos os gates antes de decidir DONE ou passagem. Este parecer não autoriza F01 automaticamente, merge, push, deploy, custos, migração de dados ou uso profissional normativamente aprovado. Nenhuma dessas operações foi realizada por @architect.
