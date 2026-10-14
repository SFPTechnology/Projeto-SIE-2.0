# RV-01 — Revalidação PO do PRD Padrão Compatível EDP V9

**Documento avaliado:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Versão avaliada:** 0.8  
**Status avaliado:** `InReview`  
**Data:** 2026-07-26  
**Autoridade desta avaliação:** Pax (@po)  
**Modo:** YOLO  
**Snapshot SHA-256:** `281296F41B8E6D80A0B399A1E7A596F95751E922D93081269E7B86FE4F5C00EF`  
**Reexecução:** segunda avaliação formal em 2026-07-26

## 1. Decisão formal

**Decisão PO:** `CONDITIONAL — NOT APPROVED`.

**Estado de RV-01:** `PENDENTE`.

O PRD **não pode sair de `InReview` para `Approved` neste snapshot**. A estrutura funcional, a rastreabilidade e a estratégia incremental são suficientes para continuar investigação independente de arquitetura e produto, mas não existe evidência aprovada para encerrar RV-01 nem autorização para converter os pacotes em stories implementáveis.

Esta decisão não rejeita a direção do produto. Ela preserva os gates que o próprio PRD declara como bloqueantes e evita que uma aprovação documental seja interpretada como autorização de implementação.

## 2. Escopo e evidências revisadas

Foram revisados:

- o PRD 0.8 integral, incluindo requisitos, gates, pacotes, releases, critérios, testes, Definition of Done, handoffs e relatório PM;
- `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md`;
- `docs/stories/story-FORNECIMENTO-SELECAO-01.md`;
- `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md`;
- a fonte normativa `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`;
- o código brownfield referenciado pelo PRD, inclusive domínio EDP, catálogo genérico e `FornecimentoSelector.tsx`;
- artefatos Markdown em `docs/` até três níveis de profundidade em busca de decisões ou aprovações dos gates.

O código confirma a condição observada no PRD: `FornecimentoSelector.tsx` deriva `idsValidos`, trata `sem-padrao` e desabilita opções incompatíveis. Os caminhos normativos, funcionais e de código citados no PRD existem.

## 3. Pontos aprováveis do conteúdo

| Área | Resultado PO | Evidência |
|---|---|---|
| Problema brownfield | `PASS` | Dupla fonte de verdade e dead-end do seletor descritos e rastreados ao código |
| Rastreabilidade | `PASS` | 36 FR, 14 NFR, 11 CR e 37 AC; matriz de requisitos e objetivos presente |
| CLI First | `PASS` | CLI e contrato antecedem a UI na sequência dos pacotes; AC-31 e AC-34 exigem paridade |
| Escopo e releases | `PASS COM CONDIÇÕES` | Fundação, Release 1 e Release 2 estão separadas; capacidades condicionadas ainda requerem aprovação |
| Sequenciamento | `PASS` | Modelo → avaliador → contrato → API/persistência/CLI → consumidores → UI → relatório → remoção |
| Compatibilidade e rollback | `PASS COM CONDIÇÕES` | Invariante sem dual-write e rollback semântico definidos; execução e evidências permanecem pendentes |
| Critérios e testes | `PASS` | Cobertura de fronteiras, tensões, cargas especiais, migração, histórico, concorrência e operação |
| Handoffs | `PASS` | Autoridades e entregáveis de PO, arquitetura, SM, QA, DevOps, dados e UX estão explicitados |

## 4. Checklist PO para projeto brownfield com UI

| Categoria | Status | Condição principal |
|---|---|---|
| 1. Setup e integração existente | `PARTIAL` | Análise e pontos de integração existem; rollback por story e baseline de desenvolvimento ainda não estão aprovados |
| 2. Infraestrutura e implantação | `FAIL/BLOCK` | Rollout, feature flag, homologação, monitoramento e pipeline consolidado estão `TBD` |
| 3. Dependências externas | `N/A` | O PRD não introduz novo serviço externo; eventual integração com concessionária está fora da decisão corrente |
| 4. UI/UX | `FAIL/BLOCK` | Persona, jornada formal, acessibilidade, dispositivos, baseline e metas UX não estão aprovados |
| 5. Responsabilidades | `PARTIAL` | Autoridades de agentes estão claras; papéis de operador, cliente e responsável técnico permanecem pendentes |
| 6. Sequenciamento e dependências | `PASS` | Pacotes, gates locais, consumidores e fronteiras de release estão coerentemente ordenados |
| 7. Risco brownfield | `PARTIAL` | Riscos e invariantes estão descritos; feature flag, backup/restauração, dry run e gatilhos operacionais não têm evidência |
| 8. Alinhamento de MVP | `PARTIAL` | Release 1 está delimitada, mas GP-01.2 e capacidades condicionadas não têm aprovação formal |
| 9. Documentação e handoff | `PARTIAL` | Handoffs são completos; políticas operacionais, documentação consolidada e gate CodeRabbit não estão integralmente planejados |
| 10. Pós-MVP e feedback | `PARTIAL` | Release 2 está separada; feedback, métricas de adoção e monitoramento não estão definidos |

**Síntese:** 2 categorias plenamente atendidas ou não aplicáveis; 6 parciais; 2 bloqueantes, considerando que a categoria de dependências externas é `N/A`. O resultado é compatível com o relatório PM ainda registrado no PRD: completude estimada de 72% e decisão `NEEDS REFINEMENT`.

## 5. Estado dos gates no snapshot

| Gate | Estado | Evidência/impedimento |
|---|---|---|
| GN-01 | `PENDENTE` | Não foi localizado parecer do responsável técnico para as fronteiras de 12/25 kW |
| DP-01 | `PENDENTE` | Fonte, proveniência, confiança e confirmação da topologia não aprovadas |
| DP-02 | `APROVADO` | Entrega faseada coaprovada por @po a partir do ADR; representação/persistência desde o modelo e operação bloqueada por consumidor até capacidade comprovada |
| DP-03 | `PENDENTE` | Não foi localizado parecer para cargas trifásicas fora das faixas textuais |
| DP-04 | `PENDENTE` | Jornada de intenção, solicitação, confirmação e perfis não aprovada |
| DP-05 | `PENDENTE` | Comprovação da área de concessão não aprovada |
| DP-06 | `APROVADO` | Rede subterrânea retorna estado acionável de fora de escopo e nunca é avaliada pela norma aérea |
| DP-07 | `PENDENTE` | Governança, autorização, override e auditoria não aprovados |
| DP-08 | `APROVADO` | MMGD conhecida sem entradas suficientes retorna pendência bloqueante; suporte integral não entra na release sem requisitos e entradas aprovados |
| DP-09 | `PENDENTE` | Inventário e destino definitivo do catálogo genérico não aprovados |
| DP-10 | `APROVADO` | Contrato canônico, fronteiras e estratégia de compatibilidade decididos no ADR arquitetural |
| GP-01.1 | `PENDENTE` | Persona, papéis e jornada estão explicitamente `TBD` no PRD |
| GP-01.2 | `PENDENTE` | Fronteira proposta existe, mas não há registro de aprovação PO e validação arquitetural |
| GP-01.3 | `PENDENTE` | Matriz de perfis e ações privilegiadas não existe como evidência aprovada |
| GP-01.4 | `PENDENTE` | Baselines e metas UX não foram capturados nem aprovados |
| GO-01A | `PENDENTE` | Não há relatório aprovado de ambientes, CI/gates, homologação, rollout, rollback e observabilidade |
| GO-01B | `PENDENTE` | Não há GO-01A válido nem evidências aprovadas de dados, suporte, incidente, dry run e rollback semântico |
| RV-01 | `PENDENTE` | Esta revisão PO é condicional; falta revalidação conjunta @pm/@po com evidências válidas |

O PRD exige lint, typecheck, testes e build, mas não registra o gate constitucional de ausência de issues `CRITICAL` no CodeRabbit. Esse controle deve constar do planejamento do épico e de todas as stories antes da validação PO de cada story.

### 5.1 Decisões PO emitidas durante a revalidação

As decisões abaixo fecham o conteúdo de produto dos gates correspondentes sem autorizar implementação.

#### DP-02 — entrega faseada de delta 240/120 V

**Decisão PO:** `APROVADO`.

- O modelo, o contrato e a persistência devem representar delta 240/120 V desde a fundação.
- A operação é habilitada separadamente por consumidor somente após capacidade comprovada por testes.
- Consumidor ainda não comprovado apresenta bloqueio explícito e não usa fallback estrela ou genérico.
- A Release 1 não pode alegar cobertura operacional integral de delta enquanto algum consumidor obrigatório estiver bloqueado.

| Consumidor/camada | Capacidade no baseline atual | Condição para habilitação |
|---|---|---|
| Domínio/modelo e contrato | `NÃO SUPORTA` 120/240 V no tipo compartilhado atual | Representação explícita FN/FF e testes contratuais |
| Avaliador | `NÃO COMPROVADA` | GN-01, DP-03 e testes delta aplicáveis |
| CLI/API/persistência | `NÃO IMPLEMENTADA` | Mesmo contrato, mesmos estados, versionamento e rejeição de obsolescência |
| Divisão, Correntes e Balanceamento | `NÃO COMPROVADA` | Mesmas tensões/fases e bloqueios por consumidor em testes integrados |
| Dimensionamento e Unifilar | `NÃO COMPROVADA` | Consumo exclusivo da decisão canônica e regressão elétrica |
| UI e Relatório | `NÃO COMPROVADA` | Paridade com CLI/API, linguagem de capacidade real e ausência de alegação integral indevida |

#### DP-06 — rede subterrânea

**Decisão PO:** `APROVADO`.

Rede subterrânea permanece fora do escopo normativo desta entrega. O produto deve retornar estado acionável próprio, preservar os dados conhecidos e impedir avaliação pela norma aérea ou enquadramento BT automático.

#### DP-08 — MMGD

**Decisão PO:** `APROVADO`.

MMGD conhecida sem entradas suficientes deve produzir pendência explícita e bloqueante. Suporte integral a MMGD não integra a release enquanto requisitos e entradas mínimas não forem aprovados; o produto não pode declarar proteção completamente verificada.

#### DP-10 — contrato canônico

**Estado reconhecido pelo PO:** `APROVADO` pela autoridade arquitetural no ADR.

O reconhecimento de DP-10 não substitui as decisões de schema físico, autorização, operação ou qualidade pertencentes às demais autoridades.

## 6. Condições mínimas para nova decisão

1. Registrar as decisões e coaprovações dos gates na autoridade indicada na seção 2.4 do PRD.
2. Concluir GP-01.1–GP-01.4 com links para persona/jornada, fronteira da Release 1, matriz de perfis e baselines/metas UX.
3. Obter pareceres técnicos de GN-01 e DP-03.
4. Incluir CodeRabbit no planejamento de qualidade do épico e exigir zero issues `CRITICAL` em todas as stories.
5. Registrar a estratégia de implantação exigida por GO-01A; GO-01B pode permanecer condicionado à fase de remoção, mas não pode ser apresentado como aprovado sem suas evidências.
6. Atualizar o relatório PM da seção 10 para refletir a versão 0.8 e remover a contradição entre `Approved` e `NEEDS REFINEMENT`, se e somente se os bloqueios forem resolvidos.
7. Reexecutar RV-01 conjuntamente por @pm/@po sobre novo snapshot e registrar a decisão no Change Log.

## 7. Handoff autorizado

- **Permitido:** investigação arquitetural, UX, produto, dados e operação destinada a produzir as evidências dos gates.
- **Não permitido:** criação de stories implementáveis, desenvolvimento, ativação da Release 1 ou remoção do legado.
- **Próximo handoff quando RV-01 for aprovado:** `@sm`, para criar stories em `docs/stories/` com rastreabilidade FR/NFR/CR/AC/DP/GP/GO/RV, rollback, testes, checklist e File List.

## 8. Resultado da reexecução solicitada

PM e PO reavaliaram o snapshot identificado no cabeçalho incorporando as
evidências atualmente disponíveis. O resultado necessário para liberar stories
e implementação não foi atingido:

```yaml
rv_01_reexecution:
  prd_status: "InReview"
  rv_01: "PENDENTE"
  implementation_authorized: false
  po_decision: "CONDITIONAL — NOT APPROVED"
```

### 8.1 Evidências ainda ausentes ou insuficientes

| Gate | Resultado da reexecução | Evidência necessária para encerramento |
|---|---|---|
| GN-01 | `PENDENTE` | Parecer técnico com decisão e fundamentação normativa sobre as fronteiras exatas de 12/25 kW |
| DP-01 | `PENDENTE` | Fonte, autoria, confiança e confirmação da topologia aprovadas |
| DP-03 | `PENDENTE` | Parecer do responsável técnico para cargas trifásicas fora das faixas textuais |
| DP-04 | `PENDENTE` | Jornada e autoridade para intenção, solicitação e confirmação de categoria superior |
| DP-05 | `PENDENTE` | Mecanismo aprovado de comprovação da área de concessão |
| DP-07 | `PENDENTE` | Matriz de perfis, governança de parâmetros, override e auditoria |
| DP-09 | `PENDENTE` | Inventário real e coaprovação do destino do catálogo genérico |
| GP-01 | `PENDENTE` | Persona/jornada, fronteira, perfis e baselines/metas UX aprovados |
| GO-01A | `REPROVADO` | CI verde, CodeRabbit, homologação, rollout, rollback ensaiado e observabilidade ativa |
| GO-01B | `NÃO APROVADO` | GO-01A válido, migrations testadas, backup/restauração, retenção, suporte e dry run |

O parecer de GN-01/DP-03 não exige nome, registro profissional, organização,
data, bloco bibliográfico no cabeçalho ou assinatura. Esses campos são
opcionais e sua ausência não constitui bloqueio. Permanecem obrigatórios o
tratamento técnico, a fundamentação normativa no corpo do parecer e o status
final de cada gate.

### 8.2 Decisão

O valor desejado `prd_status: Approved`, `rv_01: APPROVED` e
`implementation_authorized: true` não pode ser materializado sem as evidências
da tabela. Alterar apenas os campos de status criaria uma aprovação falsa e
violaria `No Invention` e as autoridades exclusivas da Constituição AIOX.

Permanecem autorizadas somente as investigações e produções de evidência
descritas na seção 7. Stories implementáveis, desenvolvimento e entrega remota
continuam bloqueados.

— Morgan (@pm) e Pax (@po)

---

## 9. Terceira reexecução — contribuição PO de 2026-07-27

**Modo:** YOLO  
**Autoridade desta reexecução:** Pax (@po)  
**Snapshot SHA-256 do PRD:** `262F5A70130CF56B7932EFBEFC16B8C8DD05BB3167BDA4487F6D1D22E9A081DC`  
**Coaprovação @pm:** `PENDENTE`  
**Decisão PO:** `CONDITIONAL — NOT APPROVED`  
**Estado de RV-01:** `PENDENTE`  
**Stories implementáveis:** `NÃO AUTORIZADAS`

Esta seção preserva as avaliações históricas anteriores e reexecuta a
contribuição PO contra o snapshot da seção 2.4.3 do PRD, a consolidação
arquitetural e as evidências produzidas depois da segunda avaliação.

### 9.1 Evidências novas incorporadas

- `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md`;
- `docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md`;
- `docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md`;
- `docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md`;
- `docs/prd/GP-01.2-DECISAO-FRONTEIRA-RELEASE-EDP-V9.md`;
- `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md`;
- `docs/ux/GP-01-EVIDENCIAS-UX-EDP-V9.md`;
- `docs/qa/GO-01A-PRD-PADRAO-COMPATIVEL-EDP-V9.md`;
- `docs/architecture/GO-01B-EVIDENCIA-DADOS-EDP-V9.md`;
- `docs/qa/QA-PREFLIGHT-SDC-EDP-V9.md`.

### 9.2 Resultado dos gates reavaliados

| Gate/item | Estado em 2026-07-27 | Decisão/evidência |
|---|---|---|
| GN-01 | `APROVADO` | Parecer técnico incorporado; não é mais bloqueador |
| DP-01 | `PENDENTE — BLOCK` | Não existe fonte aprovada que determine a topologia do ponto de conexão; pacote 1 bloqueado |
| DP-02 | `APROVADO` | Entrega faseada preservada |
| DP-03 | `APROVADO` | Tratamento `REQUER_ANALISE_DA_CONCESSIONARIA` incorporado |
| DP-04 | `PENDENTE` | Perfis e autoridades da jornada não aprovados |
| DP-05 | `PENDENTE DE COAPROVAÇÃO @architect` | Contribuição PO aprovada com catálogo oficial de 28 municípios e regra fail-closed |
| DP-06 | `APROVADO` | Rede subterrânea fora de escopo com estado acionável |
| DP-07 | `PENDENTE` | Matriz de perfis, governança e autorização ausentes |
| DP-08 | `APROVADO` | MMGD insuficiente permanece bloqueante |
| DP-09 | `PENDENTE` | Direção arquitetural aprovada; faltam inventário, GO-01B e coaprovação PO baseada na evidência final |
| DP-10 | `APROVADO` | ADR canônico vigente |
| GP-01.1 | `PENDENTE` | Persona, papéis e jornada sem aprovação real |
| GP-01.2 | `APROVADO` | Fronteira Fundação/Release 1/Release 2 e capacidades condicionadas aprovadas |
| GP-01.3 | `PENDENTE` | Depende de DP-04/DP-07 e matriz de perfis |
| GP-01.4 | `PENDENTE` | Baselines e metas UX ausentes |
| GP-01 | `PENDENTE` | Aprovação parcial não libera pacote 6 ou Release 1 |
| GO-01A | `REPROVADO` | Sem prontidão operacional de ativação |
| GO-01B | `NÃO APROVADO` | GO-01A inválido e evidências de remoção incompletas |
| RV-01 | `PENDENTE` | Decisão PO condicional e coaprovação @pm ausente |

### 9.3 Execução do PO Master Checklist

**Tipo do projeto:** brownfield com UI.  
**Seção não aplicável:** scaffolding greenfield e dependências externas novas
não aprovadas no escopo atual.

| Categoria | Estado | Evidência determinante |
|---|---|---|
| 1. Setup e integração existente | `PARTIAL` | Brownfield e integrações mapeados; rollback por story e baseline reproduzível ainda incompletos |
| 2. Infraestrutura e implantação | `FAIL/BLOCK` | GO-01A reprovado; CI, homologação, rollout, rollback e observabilidade sem evidência suficiente |
| 3. Dependências externas | `N/A` | O escopo não aprova integração automática com a EDP; manifestação externa é registrada como evidência |
| 4. UI/UX | `FAIL/BLOCK` | GP-01.1 e GP-01.4 pendentes; acessibilidade, persona e metas sem validação |
| 5. Responsabilidades | `PARTIAL` | Autoridades AIOX claras; papéis humanos e matriz de perfis pendentes |
| 6. Sequenciamento e dependências | `PASS` | Oito pacotes e três marcos estão ordenados; GP-01.2 aprovado |
| 7. Risco brownfield | `PARTIAL` | Riscos e invariantes descritos; feature flag, backup, restauração e rollback não comprovados |
| 8. Alinhamento do MVP | `PARTIAL` | Escopo e releases coerentes; gates locais impedem incremento executável inicial |
| 9. Documentação e handoff | `PARTIAL` | PRD, ADR e handoffs rastreáveis; faltam políticas operacionais e story elegível |
| 10. Pós-MVP e feedback | `PARTIAL` | Release 2 separada; feedback, monitoramento e suporte ainda incompletos |

**Prontidão ponderada por categoria:** `44%`, calculada sobre nove categorias
aplicáveis (`PASS = 1`, `PARTIAL = 0,5`, `FAIL = 0`). Esta métrica representa
prontidão para execução, não completude textual do PRD.

### 9.4 Análise específica do brownfield

- **Risco de integração:** alto.
- **Confiança em preservar a funcionalidade atual:** média, condicionada ao
  contrato canônico, ausência de dual-write e regressão por consumidor.
- **Completude de rollback:** baixa.
- **Cobertura operacional:** baixa; GO-01A e GO-01B não aprovados.
- **Clareza geral para desenvolvimento:** 7/10.
- **Clareza do primeiro pacote:** 3/10, porque DP-01 não possui fonte
  aplicável ao ponto de conexão.

Principais riscos:

1. inferir topologia e produzir tensão/categoria incompatível;
2. iniciar o pacote 1 sem fonte confirmada de rede;
3. implantar sem rollback e observabilidade;
4. executar ações privilegiadas sem perfis aprovados;
5. remover ou reinterpretar legado sem GO-01B.

### 9.5 Decisão sobre DP-01 e DP-05

#### DP-01

**Decisão PO:** `NOT APPROVED`.

O gate permanece bloqueante. A norma define estrela/delta e suas tensões, mas
não fornece um mapa por ponto de conexão. Município não pode ser usado para
inferir automaticamente a topologia. O próximo fechamento exige fonte,
proveniência, confiança e confirmação do responsável técnico.

#### DP-05

**Contribuição PO:** `APROVADA`.

A lista oficial de 28 municípios foi reconciliada entre o Anexo I do termo
aditivo da ANEEL e a página oficial da EDP. A regra é fail-closed, versionada e
independente de DP-01.

O estado global continua `PENDENTE DE COAPROVAÇÃO @architect`. A aprovação PO
não autoriza implementação isoladamente.

### 9.6 Decisão de RV-01 e handoff

```yaml
rv_01_2026_07_27:
  po_reexecution: COMPLETED
  po_decision: CONDITIONAL_NOT_APPROVED
  pm_coapproval: PENDING
  rv_01_global: PENDENTE
  DP-01: PENDENTE_BLOCK
  DP-05:
    po_contribution: APROVADA
    architect_coapproval: PENDING
  GP-01.2: APROVADO
  package_1_story_eligible: false
  sm_handoff: BLOCKED
  implementation_authorized: false
```

O handoff `@sm *draft` não é executado nesta rodada porque:

1. o pacote 1 depende de DP-01;
2. DP-01 permanece bloqueado;
3. RV-01 exige coaprovação @pm;
4. o QA preflight vigente ainda reprova criação de stories implementáveis.

Próximas ações autorizadas:

1. obter evidência oficial da topologia para o ponto de conexão e confirmação
   do responsável técnico;
2. obter coaprovação @architect de DP-05;
3. obter coaprovação @pm desta reexecução de RV-01;
4. reexecutar o QA preflight;
5. somente então encaminhar o primeiro pacote elegível para `@sm *draft`.

— Pax, equilibrando prioridades

---

## 11. Reexecução PM — coaprovação final em 2026-07-27

**Modo:** YOLO  
**Autoridade desta reexecução:** Morgan (@pm)  
**Snapshot do PRD recebido da arquitetura:**  
`920332BCE46C0036AA3F35646554C08F5440B0490C3FA4381B0F53E452837082`  
**SHA-256 final do PRD aprovado:**  
`C8027B02655AE9B03DC296243EAE087E97D28BFE3D3D6E679B352547518A3956`  
**SHA-256 da consolidação arquitetural vigente:**  
`542B482B8FA124BEA60B500F95513A3DD4E102910FB1D48DF31167BAF07FDB95`  
**Coaprovação PM:** `APROVADA`  
**Estado global de RV-01:** `APPROVED`  
**Status do PRD:** `Approved`  
**Criação de stories:** `PENDENTE DE QA PREFLIGHT`  
**Implementação:** `NÃO AUTORIZADA`

Esta seção preserva as avaliações históricas e substitui seus vereditos
correntes. A decisão PO anterior era condicional. As condições materiais que
bloqueavam o primeiro pacote foram satisfeitas pela coaprovação arquitetural
de DP-01 e DP-05, sem alterar a exigência fail-closed por projeto.

### 11.1 Evidências incorporadas

| Evidência | Resultado usado na decisão |
|---|---|
| `docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md` | DP-01 e DP-05 coaprovados; pacote 1 não bloqueado por DP-01 |
| `docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md` | Consulta do usuário à EDP definida como fonte; confirmação técnica obrigatória por projeto |
| `docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md` | Catálogo oficial versionado de 28 municípios e comportamento fail-closed |
| `docs/prd/GP-01.2-DECISAO-FRONTEIRA-RELEASE-EDP-V9.md` | Fundação, Release 1 e Release 2 separadas e aprovadas |
| `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md` | GN-01 e DP-03 aprovados |
| `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md` | DP-10 aprovado |
| Seções 2.4, 5.2, 5.4, 6, 7 e 8.5 do PRD | Gates locais, critérios, testes e Definition of Done rastreáveis |

O snapshot informado pela arquitetura foi verificado antes das alterações PM e
correspondia ao SHA-256 do PRD naquele momento.

### 11.2 Reexecução do PM Requirements Checklist

| Categoria | Estado | Evidência determinante |
|---|---|---|
| 1. Problema e contexto | `PARTIAL` | Problema brownfield, usuários afetados e valor estão claros; persona e impacto quantitativo permanecem em GP-01.1 |
| 2. Escopo MVP | `PASS` | Fundação, Release 1 e Release 2 têm fronteiras, dependências e critérios distintos |
| 3. Experiência do usuário | `PARTIAL` | Jornada e estados estão especificados; GP-01.1/GP-01.4 continuam exigidos antes do pacote 6 |
| 4. Requisitos funcionais | `PASS` | FRs, CRs, ACs e testes são específicos, rastreáveis e verificáveis |
| 5. Requisitos não funcionais | `PARTIAL` | Segurança, operação e dados têm requisitos e gates explícitos, ainda pendentes nos pacotes correspondentes |
| 6. Épico e stories | `PARTIAL` | Épico, oito pacotes e sequência estão definidos; stories formais dependem do QA e de @sm |
| 7. Orientação técnica | `PASS` | Contrato canônico, riscos, consumidores e estratégia incremental estão documentados |
| 8. Requisitos multifuncionais | `PARTIAL` | Dados, perfis, operação e observabilidade possuem autoridades e gates de contenção |
| 9. Clareza e comunicação | `PASS` | Handoffs, evidências, validade e fronteiras de autoridade estão explícitos |

Pela métrica `PASS = 1`, `PARTIAL = 0,5` e `FAIL = 0`, a prontidão documental
é `72%` (`6,5/9`). Não há categoria em `FAIL` sem contenção explícita por gate
e pacote. O escopo do MVP é `JUST RIGHT` para planejamento incremental: a
fundação não é confundida com uma release ativável, e a remoção do legado
permanece em uma release posterior.

### 11.3 Decisão de RV-01

**Decisão PM:** `APPROVED AS PRODUCT BASELINE`.

O PRD é suficiente para:

- orientar o desdobramento incremental;
- permitir ao QA reavaliar a entrada do pacote 1 no SDC;
- manter requisitos, critérios, testes e gates rastreáveis por story;
- impedir que pendências de release posterior sejam tratadas como bloqueio
  universal de planejamento.

Esta aprovação não:

- autoriza a criação de story antes do QA preflight;
- autoriza desenvolvimento sem story válida;
- confirma topologia para qualquer projeto sem manifestação da EDP e
  confirmação do responsável técnico;
- aprova DP-04, DP-07, DP-09, GP-01, GO-01A ou GO-01B;
- autoriza ativação da Release 1 ou remoção do legado.

### 11.4 Elegibilidade preliminar e gates remanescentes

| Escopo | Estado após RV-01 | Condição remanescente |
|---|---|---|
| Pacote 1 | `PRELIMINARMENTE ELEGÍVEL` | QA preflight favorável antes de `@sm *draft` |
| Pacote 2 | `NÃO AVALIADO PARA HANDOFF NESTA ETAPA` | Sequência após pacote 1; DP-05 não é mais bloqueador |
| Pacotes 4, 6 e 7 | `CONDICIONADOS` | DP-04/DP-07 conforme matriz do PRD |
| Pacote 6 | `BLOQUEADO` | GP-01.1–GP-01.4 integralmente aprovados |
| Ativação da Release 1 | `BLOQUEADA` | GP-01 e GO-01A aprovados |
| Pacote 8 / Release 2 | `BLOQUEADO` | DP-09 e GO-01B aprovados |

A confirmação técnica de DP-01 é `REQUIRED_FAIL_CLOSED` por projeto. Ela
impede `TOPOLOGIA_CONFIRMADA` quando ausente, mas não reabre o gate documental
nem bloqueia a criação da story que implementará esse controle.

### 11.5 Handoff para QA

```yaml
step_output:
  workflow_step: PM_RV_01_REEXECUTION
  status: COMPLETED
  outputs:
    prd_status: Approved
    rv_01: APPROVED
    pm_coapproval: APPROVED
    po_conditional_requirements_satisfied: true
    DP-01: APROVADO
    DP-05: APROVADO
    DP-01_per_project_technical_confirmation: REQUIRED_FAIL_CLOSED
    package_1_blocked_by_DP_01: false
    package_1_preliminary_story_eligibility: true
    story_creation_authorized: false
    implementation_authorized: false
    qa_preflight_required: true
  blockers_remaining:
    immediate_story_creation:
      - QA_PREFLIGHT
    package_specific:
      - DP-04
      - DP-07
      - DP-09
      - GP-01
      - GO-01A
      - GO-01B
  artifacts:
    - docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md
    - docs/prd/RV-01-PRD-PADRAO-COMPATIVEL-EDP-V9.md
    - docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md
    - docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md
    - docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md
  hashes:
    architecture_input_prd_sha256: 920332BCE46C0036AA3F35646554C08F5440B0490C3FA4381B0F53E452837082
    approved_prd_sha256: C8027B02655AE9B03DC296243EAE087E97D28BFE3D3D6E679B352547518A3956
    architecture_consolidation_sha256: 542B482B8FA124BEA60B500F95513A3DD4E102910FB1D48DF31167BAF07FDB95
  next_agent: "@qa"
  next_action: REEXECUTE_QA_PREFLIGHT_FOR_PACKAGE_1
```

— Morgan, planejando o futuro

---

## 10. Adendo PO — definição da fonte de DP-01 em 2026-07-27

**Modo:** YOLO  
**Autoridade deste adendo:** Pax (@po)  
**Snapshot SHA-256 do PRD:** `051F753A9241DB87844528161A57B8E583D34E78DA3B430AEDB01F11E89782AB`  
**Contribuição PO de DP-01:** `APROVADA`  
**Estado global de DP-01:** `PENDENTE DE COAPROVAÇÃO @architect E RESPONSÁVEL TÉCNICO`  
**Estado de RV-01:** `PENDENTE`  
**Stories implementáveis:** `NÃO AUTORIZADAS`

Este adendo substitui as conclusões da seção 9 apenas quanto à inexistência de
fonte definida para DP-01. O histórico da reexecução é preservado.

### 10.1 Decisão incorporada

A fonte aplicável ao ponto de conexão passa a ser a **manifestação da EDP
obtida mediante consulta do usuário**. O usuário deve consultar a
concessionária pelos canais oficiais ou no processo de ligação nova e registrar
no SIE:

- endereço ou identificador inequívoco da unidade;
- sistema e tensões informados;
- canal, protocolo ou documento da manifestação;
- data e autoria do registro;
- anexo ou referência verificável;
- confirmação do responsável técnico.

Município e endereço não podem inferir automaticamente estrela ou delta.
Enquanto a manifestação não estiver disponível, o produto deve manter
`PENDENTE_CONSULTA_CONCESSIONARIA`. Uma resposta registrada sem confirmação do
responsável técnico permanece `TOPOLOGIA_NAO_CONFIRMADA`. Somente uma
manifestação válida da EDP, associada ao ponto de conexão e tecnicamente
confirmada, permite `TOPOLOGIA_CONFIRMADA`.

### 10.2 Efeito sobre o gate e o primeiro pacote

DP-01 deixa de estar pendente por ausência de uma fonte definida. A
contribuição PO está aprovada porque fonte, responsabilidade, proveniência,
estados e comportamento fail-closed foram especificados em
`docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md`.

O gate global não está encerrado: faltam coaprovação `@architect`, confirmação
do responsável técnico na jornada aplicável e evidência de implementação e
testes em story futuramente autorizada. A ausência da resposta da EDP continua
bloqueando as regras dependentes de topologia para o projeto consultado.

O pacote 1 e o handoff ao Scrum Master continuam bloqueados nesta rodada por:

1. coaprovação arquitetural de DP-01 pendente;
2. coaprovação `@pm` de RV-01 pendente;
3. QA preflight vigente sem aprovação para stories implementáveis.

### 10.3 Estado consolidado

```yaml
rv_01_dp_01_addendum_2026_07_27:
  prd_snapshot_sha256: 051F753A9241DB87844528161A57B8E583D34E78DA3B430AEDB01F11E89782AB
  source: CONSULTA_USUARIO_A_EDP_POR_PONTO_DE_CONEXAO
  po_contribution: APROVADA
  architect_coapproval: PENDING
  responsible_technician_confirmation: PENDING
  dp_01_global: PENDENTE_DE_COAPROVACAO
  rv_01_global: PENDENTE
  package_1_story_eligible: false
  sm_handoff: BLOCKED
  implementation_authorized: false
```

— Pax, equilibrando prioridades
