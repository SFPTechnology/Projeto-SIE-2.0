# PRD — Reestruturação do Padrão Compatível EDP São Paulo V9

**Produto:** SIE — Sistema de Instalações Elétricas  
**Módulo:** Padrão de entrada EDP São Paulo  
**Tipo:** PRD Brownfield — modificação estrutural de funcionalidade existente  
**Autor:** Morgan (@pm) — AIOX  
**Data:** 2026-07-26  
**Versão:** 0.8  
**Status:** Approved — RV-01 aprovado como baseline de produto; criação de stories aguarda QA preflight e cada pacote permanece condicionado aos próprios gates  
**Documento-base:** `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md`  
**Fonte oficial de consulta normativa para DP-01 e DP-05:** `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`

---

## 1. Análise e Contexto do Projeto Existente

### 1.1 Fonte da análise

- Plano técnico-funcional produzido por @analyst em 2026-07-26.
- Análise direta do código existente no aplicativo `sistema-de-instala-es-el-tricas-sie-main/`.
- Artefatos de produto, domínio, API, persistência e testes referenciados pelo documento-base.
- Story histórica `docs/stories/story-FORNECIMENTO-SELECAO-01.md`, preservada sem alteração retroativa.
- Parecer técnico aprovado para GN-01/DP-03 e consolidação dos gates arquiteturais produzidos em 2026-07-26.
- `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`, fonte oficial de consulta normativa para DP-01 e DP-05.

Não foi localizado um documento único produzido pelo workflow `document-project`. A análise utiliza os artefatos existentes e evidências diretas do código, sem completar lacunas por suposição.

### 1.2 Estado atual do projeto

O SIE é uma aplicação brownfield para apoio à elaboração de projetos de instalações elétricas. O aplicativo em escopo utiliza TanStack Start, TypeScript, React, IBM Carbon Design System, Supabase/PostgreSQL e Vitest. A funcionalidade de padrão de entrada possui dois fluxos paralelos:

```text
Dependências e cargas
        |
        +--> motor e catálogo genéricos --> seletor, Correntes,
        |                                  Dimensionamento e Unifilar
        |
        +--> motor e catálogo EDP-SP ----> cards EDP,
                                           Divisão de circuitos e relatório
```

Essa duplicidade permite que a mesma unidade consumidora seja apresentada com um resultado EDP e processada por módulos posteriores com tensões ou contratos genéricos diferentes.

O defeito visível no campo “Padrão compatível” ocorre quando o motor genérico retorna `sem-padrao`: `FornecimentoSelector` forma um conjunto vazio de IDs válidos e desabilita todas as opções. O problema, porém, é estrutural e inclui catálogo inadequado à EDP V9, modelo de tensão incompleto, regras de categoria simplificadas, perda de atributos da subcategoria, divergências de demanda e persistência sem proveniência suficiente.

### 1.3 Documentação disponível

- [x] Plano técnico-funcional detalhado
- [x] Fonte normativa EDP V9 em blocos rastreáveis
- [x] PRD brownfield de módulo relacionado como referência de padrão documental
- [x] Story histórica do seletor de fornecimento
- [x] Código e testes do domínio, API, serviços e interface
- [x] Documentação arquitetural de módulo relacionado
- [ ] Documento consolidado de arquitetura do projeto
- [ ] Padrões de codificação em `docs/framework/coding-standards.md`
- [ ] Stack consolidada em `docs/framework/tech-stack.md`
- [ ] Diretrizes UX/UI consolidadas

As ausências documentais não impedem este PRD, mas devem ser consideradas pelo @architect ao ratificar contratos, fronteiras e estratégia de migração.

### 1.4 Definição do aprimoramento

**Tipos de aprimoramento:**

- [x] Modificação significativa de funcionalidade existente
- [x] Correção de defeito e estabilidade
- [x] Reestruturação de domínio e contratos
- [x] Evolução de API, persistência e migração
- [x] Reestruturação de UI/UX
- [ ] Integração com novo sistema externo
- [ ] Atualização da stack tecnológica

**Avaliação de impacto:** impacto maior, com alterações arquiteturais e coordenação de múltiplos incrementos.

O aprimoramento substituirá, na rota EDP-SP, o uso do padrão genérico por uma decisão canônica, normativa, explicável e rastreável. Categoria, topologia/tensões, solicitação superior, subcategoria física e estado regulatório deixarão de ser tratados como um único item genérico.

### 1.5 Problema

O usuário da tela de Padrão de entrada pode ficar sem qualquer opção acionável e, mesmo quando há seleção, diferentes módulos podem calcular o mesmo projeto usando fontes, tensões e padrões divergentes. Isso compromete a coerência entre Padrão de entrada, Divisão de circuitos, Correntes, Dimensionamento, Unifilar e Relatório.

Correções isoladas no `Select`, nos pisos de potência ou no catálogo genérico não resolvem a causa e podem manter dimensionamentos eletricamente incoerentes.

**Persona primária:** `TBD — validação @po`. Os artefatos distinguem operador da tela, cliente solicitante e responsável técnico, mas não definem se esses papéis pertencem à mesma pessoa. Este PRD não atribui autoridade técnica ao operador nem presume que ele represente o cliente. Persona, papéis e responsabilidades devem ser aprovados em GP-01 antes das stories do pacote 6.

### 1.6 Objetivos

- Estabelecer um único resultado canônico de padrão de entrada para projetos EDP-SP.
- Representar separadamente rede, topologia, tensões, categoria mínima, categoria solicitada, subcategoria e especificação física.
- Avaliar todas as alternativas com estado e motivo, evitando listas vazias sem orientação.
- Garantir que todos os consumidores downstream utilizem o mesmo contrato efetivo.
- Preservar norma, versão, proveniência, decisões do usuário e histórico de migração.
- Impedir que o catálogo genérico 127/220/380 seja apresentado como catálogo EDP V9.
- Migrar projetos existentes sem reinterpretação ou conversão silenciosa.
- Respeitar a ordem `CLI/domínio → contratos/observabilidade → API/persistência → UI`.

#### 1.6.1 Matriz de alinhamento dos objetivos

| Objetivo | Resultado verificável | FR/NFR/CR relacionados | AC relacionados | Métrica | Gate |
|---|---|---|---|---|---|
| O-01 — decisão canônica única | Cada projeto EDP possui um único padrão efetivo | FR20–FR23; NFR2 | AC-16–AC-21, AC-34 | Consumidores EDP no contrato genérico = 0; divergências entre módulos = 0 | DP-10; GO-01B para remoção |
| O-02 — dimensões normativas separadas | Rede, topologia, tensões, categorias e especificação não são reduzidas a um item genérico | FR2–FR9, FR14–FR19; NFR1 | AC-03, AC-08–AC-10, AC-15, AC-27–AC-30 | AC aplicáveis aprovados = 100%; ocorrências de 380 V = 0 | GN-01; DP-01–DP-03 |
| O-03 — alternativas acionáveis | Toda alternativa apresenta estado, motivo e próxima ação, sem dead-end silencioso | FR4, FR15, FR26–FR27 | AC-01–AC-07, AC-36 | Candidatos sem estado/motivo = 0; metas UX aprovadas | GP-01 |
| O-04 — consumidores convergentes | Divisão, Correntes, Balanceamento, Dimensionamento, Unifilar e Relatório usam o mesmo contrato | FR21–FR25, FR34; NFR2, NFR12 | AC-16–AC-21, AC-34 | Divergências de tensão/categoria na mesma fixture = 0 | DP-10 |
| O-05 — histórico normativo reconstruível | Decisão e relatório permanecem auditáveis após atualização da norma | FR28–FR30; NFR1, NFR5, NFR7 | AC-22, AC-25–AC-26, AC-32 | Reinterpretações silenciosas = 0; reconstruções históricas aprovadas = 100% | DP-07; GO-01B |
| O-06 — isolamento do catálogo genérico | A rota EDP não produz resultados genéricos; outros contextos permanecem preservados | FR20, FR22, FR33; CR1–CR2, CR11 | AC-02, AC-18, AC-35 | Consumidores genéricos na rota EDP = 0; regressões fora da EDP = 0 | DP-09; DP-10; GO-01B |
| O-07 — migração segura | Legado é migrado sem dual-write, perda ou conversão silenciosa | FR31, FR33; NFR6; CR3–CR6 | AC-24, AC-33, AC-35 | Execuções idempotentes divergentes = 0; rollback semântico aprovado | GO-01B |
| O-08 — CLI First e paridade | Operação essencial existe por CLI antes da UI e compartilha estados com API/UI | FR32; NFR12 | AC-31, AC-34, AC-36–AC-37 | Paridade contratual aprovada = 100% | GP-01 antes da UI; GO-01A antes da ativação; GO-01B antes da remoção |

### 1.7 Limites e autoridades

Este PRD define resultados de produto, requisitos, compatibilidade, critérios e direcionamento de entrega. Ele não:

- realiza validação jurídica da norma;
- substitui análise ou aprovação do responsável técnico;
- define atendimento subterrâneo;
- decide a arquitetura final ou o formato concreto do contrato canônico;
- cria stories formais;
- emite decisão final de qualidade;
- autoriza implementação.

Decisões arquiteturais pertencem ao @architect; criação e refinamento de stories pertencem a @po/@sm; parecer final de qualidade pertence ao @qa.

### 1.8 Premissas refinadas

- Os caminhos `src/...` do documento-base referem-se ao aplicativo `sistema-de-instala-es-el-tricas-sie-main/`.
- O trabalho será organizado como um épico brownfield coeso, com oito pacotes incrementais sugeridos para posterior desdobramento por @po/@sm.
- Requisitos obrigatórios serão separados de sugestões de implementação e do mapa provável de arquivos.
- O domínio e o contrato deverão ser capazes de representar estrela 220/127 V e delta 240/120 V; o momento de ativação integral do fluxo delta permanece decisão de escopo.
- Métricas de negócio, prazo e adoção não presentes nos artefatos permanecerão `TBD — validação @po`.
- O PRD pode seguir para validação de produto e investigação arquitetural, mas não para implementação enquanto os gates aplicáveis permanecerem abertos.

### 1.9 Change Log

| Alteração | Data | Versão | Descrição | Autor |
|---|---|---:|---|---|
| Criação | 2026-07-26 | 0.1 | Contexto brownfield consolidado a partir do plano EDP V9 e evidências do código | Morgan (@pm) |
| Validação PM | 2026-07-26 | 0.2 | Requisitos refinados, sequência aprovada e checklist PM consolidado | Morgan (@pm) |
| Refinamento lógico | 2026-07-26 | 0.3 | Escopo, fluxo delta, gates e consumidores obrigatórios reconciliados | Morgan (@pm) |
| Alinhamento estratégico | 2026-07-26 | 0.4 | CLI First, observabilidade, fachada legada e métricas de usuário reforçados | Morgan (@pm) |
| Controles de risco | 2026-07-26 | 0.5 | Histórico normativo, concorrência, migração, rollback e gate operacional reforçados | Morgan (@pm) |
| Revisão analítica | 2026-07-26 | 0.6 | Rastreabilidade de metadados normativos, cobertura de Balanceamento e handoffs dos gates reconciliados | Atlas (@analyst) |
| Alinhamento de objetivos | 2026-07-26 | 0.7 | Objetivos rastreados, releases delimitados e gates de produto, acesso, retenção e operação vinculados | Atlas (@analyst) |
| Fortalecimento adversarial | 2026-07-26 | 0.8 | Gates de ativação/remoção separados, evidências explícitas, rollback invariável e revalidação PM/PO bloqueante | Atlas (@analyst) |
| Entrada em revisão | 2026-07-26 | 0.8 | Status alterado de Draft para InReview para execução formal de RV-01 em modo YOLO | Morgan (@pm) |
| Revalidação condicional | 2026-07-26 | 0.8 | RV-01 executado com decisão `CONDITIONAL — NOT APPROVED`; DP-02, DP-06, DP-08 e DP-10 aprovados, demais gates bloqueantes registrados | Morgan (@pm) e Pax (@po) |
| Reexecução de RV-01 | 2026-07-26 | 0.8 | Evidências reavaliadas após solicitação de continuidade; ausência de novos pareceres normativos, aprovações UX e provas operacionais mantém o PRD em `InReview` e a implementação não autorizada | Morgan (@pm) e Pax (@po) |
| Simplificação do parecer técnico | 2026-07-26 | 0.8 | Removida a obrigatoriedade de nome, registro profissional, organização, data, bloco bibliográfico e assinatura no parecer GN-01/DP-03; preservadas decisões, fundamentação normativa e rastreabilidade do artefato | Atlas (@analyst) |
| Incorporação do parecer técnico | 2026-07-26 | 0.8 | GN-01 e DP-03 atualizados para `APROVADO`; regras de fronteira, estado bloqueante e snapshot dos gates arquiteturais consolidados sem alterar o `NO-GO` global | Aria (@architect) |
| Revalidação PO e evidências dos gates | 2026-07-27 | 0.8 | DP-01 mantido bloqueado por ausência de fonte por ponto de conexão; contribuição PO de DP-05 aprovada com fontes oficiais e pendente de coaprovação arquitetural; GP-01.2 aprovado | Pax (@po) |
| Definição da fonte de DP-01 | 2026-07-27 | 0.8 | Consulta do usuário à EDP definida como fonte por ponto de conexão, com registro de protocolo/documento e confirmação do responsável técnico; contribuição PO aprovada e gate global pendente de coaprovação | Pax (@po) |
| Coaprovação arquitetural de DP-01 e DP-05 | 2026-07-27 | 0.8 | Fonte de topologia por consulta à EDP e catálogo oficial versionado da área de concessão coaprovados; controles permanecem fail-closed e não autorizam implementação sem os demais gates | Aria (@architect) |
| Aprovação de RV-01 | 2026-07-27 | 0.8 | PRD aprovado como baseline para desdobramento incremental; pacote 1 preliminarmente elegível, sujeito ao QA preflight; gates de pacotes posteriores, ativação e remoção permanecem vigentes | Morgan (@pm) |
| Formalização da fonte oficial de DP-01 e DP-05 | 2026-07-27 | 0.8 | `PT.DT.PDN.00068_V9_chunks.json` formalizado como fonte oficial de consulta normativa dos dois gates; DP-01 e DP-05 permanecem aprovados e deixam de bloquear a criação das stories dos pacotes dependentes, sem dispensar controles por projeto ou outros gates | Atlas (@analyst) |

---

## 2. Requisitos

### 2.1 Requisitos Funcionais

#### Elegibilidade e contexto normativo

- **FR1:** Aplicar a avaliação EDP V9 somente quando distribuidora, área de concessão, unidade individual e tipo de rede estiverem dentro do escopo normativo conhecido.
- **FR2:** Representar explicitamente rede aérea/subterrânea, topologia estrela/delta e tensões nominais 220/127 V ou 240/120 V. A topologia do ponto de conexão deve ser obtida pelo usuário mediante consulta à EDP e registrada com canal, protocolo/documento, data, autoria e confirmação do responsável técnico; município ou endereço não podem determinar automaticamente estrela/delta.
- **FR3:** Tornar o domínio e o contrato capazes de representar 120/240 V, independentemente da decisão DP-02 sobre o momento de ativação operacional integral do fluxo delta. Se a entrega for faseada, CLI, API, UI e relatório devem declarar o ramo delta como bloqueado ou pendente e não afirmar compatibilidade integral EDP V9.
- **FR4:** Produzir pendência acionável quando rede, topologia, localização ou outra entrada obrigatória estiver ausente. Enquanto a EDP não responder à consulta de topologia, o produto deve orientar o usuário e manter `PENDENTE_CONSULTA_CONCESSIONARIA`; rede subterrânea e fornecimento acima de 75 kW devem receber estados próprios, não uma lista vazia ou atendimento BT automático.

#### Categoria, demanda e avaliação

- **FR5:** Determinar a categoria mínima U/D/T considerando carga instalada ativa, topologia, demanda, fases e condições especiais aplicáveis.
- **FR6:** Representar D delta e T delta como condições distintas e não como faixas lineares mutuamente exclusivas.
- **FR7:** Impedir que a fase de força da rede delta seja usada para alimentar carga que não seja trifásica.
- **FR8:** Aplicar a interpretação ratificada em GN-01: exatamente 12 kW, sem equipamento trifásico ou outra condição impeditiva, pertence a U em estrela e delta; exatamente 25 kW sem equipamento trifásico pertence a D em estrela e delta; em delta, exatamente 25 kW com equipamento trifásico pertence a T; exatamente 12 kW com equipamento trifásico em qualquer topologia e exatamente 25 kW com equipamento trifásico em estrela retornam `REQUER_ANALISE_DA_CONCESSIONARIA`.
- **FR9:** Distinguir categoria mínima, categoria superior elegível, intenção do cliente, categoria solicitada e confirmação da concessionária; uma categoria dependente da Nota 03 nunca pode ser selecionada automaticamente nem apresentada como aprovada antes da confirmação correspondente.
- **FR10:** Avaliar a compatibilidade de tensão e número de fases de todas as cargas sem alterar os valores fixos cadastrados.
- **FR11:** Avaliar separadamente motores, raio X, solda e bomba de incêndio, aplicando bloqueio, proteção específica ou estudo conforme as condições autorizadas; carga potencialmente especial sem classificação suficiente deve permanecer pendente e não passar como TUE genérica.
- **FR12:** Usar carga ativa em kW para selecionar o fator do grupo A e reconciliar a demanda total com a soma dos grupos a–i.
- **FR13:** Calcular a corrente de demanda conforme o sistema e registrar fórmula, entradas, unidades e resultado.
- **FR14:** Determinar a subcategoria aplicável pelo conjunto correto das Tabelas 001/002, sem equiparar implicitamente o limite da linha à ampacidade `Iz`.
- **FR15:** Quando equipamento trifásico estiver fora das faixas textuais de T, produzir `REQUER_ANALISE_DA_CONCESSIONARIA` como estado bloqueante, sem categoria automática ou definitiva. Quando limites de cargas especiais, corrente ou outras condições de atendimento forem excedidos, produzir `REQUER_ESTUDO_TECNICO` ou estado equivalente e nunca rotular o caso como compatível.

#### Especificação física do padrão

- **FR16:** Preservar e expor proteção, fusível/chave, medição, condutores PVC e EPR/XLPE, caixa, eletroduto, poste/PCI, aterramento, limites de motor e alertas da subcategoria.
- **FR17:** Aplicar medição indireta acima de 150 A e registrar a pendência documental de responsabilidade técnica correspondente.
- **FR18:** Exibir as responsabilidades diferenciadas pelo ramal para U, D2 e T2.
- **FR19:** Manter o limite EDP entre ponto de conexão e medição separado dos limites NBR 5410 aplicáveis aos circuitos internos.

#### Decisão canônica e consumidores

- **FR20:** Expor um único resultado canônico de padrão de entrada para cada projeto EDP-SP. A fachada de compatibilidade pode ler e diagnosticar dados legados, mas nunca produzir novos resultados pelo contrato genérico.
- **FR21:** Fazer Divisão, Correntes, Balanceamento, Dimensionamento, Unifilar e Relatório consumirem a mesma decisão canônica e as mesmas tensões nomeadas.
- **FR22:** Impedir a oferta ou publicação de 380 V em contexto EDP V9.
- **FR23:** Bloquear consumidores downstream quando o padrão estiver pendente, obsoleto, em estudo ou fora de escopo, sem fallback genérico oculto.
- **FR24:** Invalidar os resultados dependentes quando cargas, rede, topologia, categoria, subcategoria ou seleção efetiva mudarem, preservando somente dados manuais ainda válidos; antes de recálculo em massa, produzir relatório de impacto e executar comparação sem sobrescrita.
- **FR25:** Oferecer nas Dependências somente tensões disponíveis no fornecimento efetivo e nunca reescrever silenciosamente a tensão fixa de uma carga.

#### Seleção, persistência e migração

- **FR26:** Retornar e apresentar todas as alternativas avaliadas, cada uma com estado, motivo, topologia, tensões, categoria e subcategoria disponível.
- **FR27:** Rejeitar no cliente e no servidor candidato incompatível, obsoleto ou calculado sobre entradas que mudaram desde a avaliação.
- **FR28:** Persistir a decisão do usuário, sua natureza mínima ou solicitada, norma, versão e referência ao catálogo oficial, sem copiar o catálogo como configuração editável por projeto; todas as versões oficiais referenciadas devem permanecer imutáveis e disponíveis para reconstrução histórica.
- **FR29:** Registrar seleção, override, migração, recálculo e invalidação com autoria, data, valor anterior, novo valor, justificativa e entradas relevantes.
- **FR30:** Manter fonte oficial e override com proveniências distintas; override do usuário não pode receber automaticamente status normativo verificado.
- **FR31:** Migrar configurações legadas de maneira não destrutiva, reversível e idempotente, classificando casos mapeáveis, pendentes, incompatíveis, customizados ou sem seleção; criar snapshot pré-migração e plano de rollback semântico, mantendo uma única escrita canônica.
- **FR32:** Disponibilizar por CLI, antes da UI equivalente, avaliação de candidatos, consulta da decisão canônica, diagnósticos, inventário e migração, usando os mesmos estados e contrato expostos pela API.
- **FR33:** Remover o contrato genérico da rota EDP apenas após o inventário confirmar que não existem consumidores EDP dependentes dele, exceto casos explicitamente aprovados e isolados, e após aprovação do gate operacional GO-01B.
- **FR34:** Publicar no relatório e no unifilar um único padrão efetivo, com norma, versão, topologia, categoria, subcategoria, especificação e pendências.
- **FR35:** Quando houver MMGD conhecida sem entradas suficientes, registrar pendência explícita e não declarar a proteção completamente verificada.
- **FR36:** Manter a avaliação do atendimento EDP separada da conformidade NBR 5410 da instalação interna.

### 2.2 Requisitos Não Funcionais

- **NFR1 — Rastreabilidade:** toda decisão normativa deve identificar documento, versão, fonte, entradas, regra aplicada e proveniência; catálogo, contrato, documentação e relatório devem declarar metadados normativos consistentes.
- **NFR2 — Integridade:** o sistema não pode produzir resultados downstream com contratos, topologias ou tensões divergentes para o mesmo projeto.
- **NFR3 — Sem invenção:** lacunas normativas ou de produto devem gerar pendência, estudo ou decisão aberta, nunca regra presumida.
- **NFR4 — Determinismo:** as mesmas entradas e a mesma versão normativa devem produzir a mesma avaliação de candidatos.
- **NFR5 — Auditabilidade:** o histórico deve permitir reconstruir o estado efetivo e sua origem em qualquer decisão persistida.
- **NFR6 — Idempotência e recuperação:** repetir migração ou recálculo sem mudança de entrada não pode corromper ou duplicar estado. O rollback semântico deve restaurar no contrato canônico o último estado de negócio comprovadamente válido, ou bloquear novas escritas quando essa restauração não for segura; nunca pode reativar escrita legada, cálculo genérico na rota EDP ou dual-write. Eventos posteriores ao snapshot permanecem auditáveis e resultados downstream incompatíveis são invalidados.
- **NFR7 — Concorrência e obsolescência:** resultados calculados sobre entradas, catálogo ou versões anteriores não podem sobrescrever uma decisão atual; avaliação e salvamento devem validar a mesma versão/hash.
- **NFR8 — Testabilidade:** o produto deve cobrir os 37 critérios de aceite do PRD, incluindo os 30 critérios do documento-base e os sete critérios adicionais de CLI, histórico, migração, paridade contratual, remoção, prontidão de produto e ativação operacional, além da matriz de fronteiras, tensões, cargas especiais, subcategorias, integração e migração.
- **NFR9 — Qualidade:** `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` devem passar antes da conclusão.
- **NFR10 — Desempenho:** capturar baseline do fluxo atual antes da implementação e aprovar com @po/@architect um limite mensurável antes das stories que alterem o recálculo.
- **NFR11 — Manutenibilidade:** regras normativas, contratos, persistência, serviços e apresentação devem permanecer separáveis e verificáveis.
- **NFR12 — Observabilidade:** estados pendentes, obsoletos, de estudo e fora de escopo devem ser identificáveis de forma consistente em CLI, API e UI; fluxos faseados devem expor a capacidade real de cada consumidor e impedir avanço quando ele ainda não suportar o estado selecionado.
- **NFR13 — Autorização e segregação de responsabilidades:** solicitação e confirmação de categoria superior, overrides, parâmetros EDP, migração e rollback devem respeitar a matriz de perfis aprovada em DP-04, DP-07 e GP-01; todas as ações privilegiadas devem ser auditáveis.
- **NFR14 — Retenção e resiliência operacional:** retenção, acesso, backup, restauração, suporte e resposta a incidentes para decisões e auditoria devem possuir políticas e evidências aprovadas em GO-01B antes da remoção do legado.

### 2.3 Requisitos de Compatibilidade

- **CR1:** O catálogo genérico deve permanecer isolado da rota EDP enquanto existir requisito explícito para outro fornecedor ou modo.
- **CR2:** `TRI-220-380` nunca pode ser convertido automaticamente para um padrão EDP V9.
- **CR3:** `BI-127-220` legado não pode ser reinterpretado automaticamente como categoria mínima D.
- **CR4:** Configurações customizadas devem ser preservadas para auditoria e encaminhadas para revisão.
- **CR5:** Seleções e schemas anteriores devem continuar legíveis durante a transição somente para compatibilidade, diagnóstico e migração; nenhum novo cálculo EDP pode ser produzido pelo contrato genérico.
- **CR6:** Divisões manuais ainda compatíveis devem ser preservadas; as incompatíveis devem ser invalidadas com motivo.
- **CR7:** A escolha do padrão não pode reescrever a tensão fixa cadastrada em uma carga.
- **CR8:** A especificação do ramal de entrada não pode ser confundida com o dimensionamento dos circuitos terminais.
- **CR9:** A story histórica `docs/stories/story-FORNECIMENTO-SELECAO-01.md` deve permanecer como registro e não ser reescrita retroativamente.
- **CR10:** A experiência visual deve permanecer coerente com o IBM Carbon Design System já utilizado pelo aplicativo, sem fixar a versão atual da biblioteca como requisito permanente.
- **CR11:** Consumidores fora do contexto EDP não podem sofrer regressão por causa da separação do catálogo genérico.

### 2.4 Gates de Decisão, Produto e Operação

Para DP-01 e DP-05, a fonte oficial de consulta normativa deste PRD é
`Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`, correspondente à
PT.DT.PDN.00068 V9. O artefato deve ser consultado e referenciado com
proveniência e versão nas stories e evidências desses gates. O snapshot
formalizado nesta revisão possui SHA-256
`C2C3AC7C0A890FE369E0A357D03F0B162A5905ACBEE1610D717454A01CA8D542`.

Em DP-01, a fonte oficial delimita os sistemas, as tensões e as regras
normativas, mas não identifica automaticamente a topologia disponível em um
ponto de conexão concreto; a manifestação da EDP e a confirmação do
responsável técnico por projeto permanecem obrigatórias. Em DP-05, ela é a
referência normativa oficial do escopo do padrão e deve ser usada em conjunto
com o catálogo versionado e as evidências oficiais da área de concessão. Essa
formalização complementa as fontes específicas já coaprovadas, não altera o
comportamento fail-closed e não reabre DP-01 ou DP-05.

| ID | Decisão | Autoridade/validação |
|---|---|---|
| GN-01 | Ratificação das fronteiras exatas de 12 e 25 kW | responsável técnico |
| DP-01 | Fonte oficial de consulta normativa e confirmação da topologia da rede por ponto de conexão | @po/@architect e responsável técnico |
| DP-02 | Entrega integral imediata ou faseada do fluxo delta 240/120 V | @po/@architect |
| DP-03 | Tratamento de carga trifásica abaixo das faixas T textuais | responsável técnico/@architect |
| DP-04 | Registro de intenção versus confirmação da concessionária para categoria superior | @po |
| DP-05 | Fonte oficial de consulta normativa e forma de comprovação da área de concessão | @po/@architect |
| DP-06 | Tratamento de rede subterrânea | @po/@architect |
| DP-07 | Governança e autorização dos parâmetros EDP | @po/@architect |
| DP-08 | Entrada imediata de MMGD ou pendência explícita | @po/@architect |
| DP-09 | Destino definitivo do catálogo genérico | @po/@architect |
| DP-10 | Forma e estratégia de compatibilidade do contrato canônico | @architect |
| GP-01 | Prontidão de produto para o pacote 6 e a Release 1, comprovada pelos itens GP-01.1–GP-01.4 | @po/@ux, com validação técnica de dependências por @architect |
| GO-01A | Prontidão operacional para ativar a Release 1: ambientes, CI/gates, homologação, rollout, rollback operacional e observabilidade aprovados | @architect/@devops/@qa |
| GO-01B | Prontidão operacional para remover o legado da rota EDP: GO-01A válido e retenção/acesso, backup/restauração, rollback semântico, suporte/resposta a incidentes e dry run aprovados | @architect/@devops/@qa, com evidências de dados por @data-engineer |
| RV-01 | Revalidação formal do PRD 0.8, incluindo completude, adequação da Release 1, critérios, gates e parecer de prontidão | @pm/@po |

#### 2.4.1 Checklist de GP-01

| Item | Evidência bloqueante | Responsável | Aprovação |
|---|---|---|---|
| GP-01.1 | Persona primária, papéis de operador/cliente/responsável técnico e jornada afetada documentados | @ux/@po | @po |
| GP-01.2 | Fronteira da Release 1 e capacidades condicionadas aprovadas | @po | @po, com dependências validadas por @architect |
| GP-01.3 | Matriz de perfis e ações privilegiadas coerente com DP-04 e DP-07 | @po/@architect | @po/@architect dentro de suas autoridades |
| GP-01.4 | Baselines e metas UX da seção 8.4 aprovados | @ux/@po | @po |

GP-01 somente assume estado `APROVADO` quando os quatro itens estiverem aprovados. O estado deve listar individualmente itens `PENDENTE`, `REPROVADO`, `OBSOLETO` ou `APROVADO`; uma aprovação parcial nunca libera o pacote 6 nem a Release 1.

#### 2.4.2 Matriz de evidências e validade dos gates

| Gate | Evidência mínima | Responsável pela evidência | Aprovador | Revalidação obrigatória |
|---|---|---|---|---|
| GN-01 | Parecer técnico com fonte normativa e interpretação das fronteiras | responsável técnico | responsável técnico | Mudança normativa ou nova evidência técnica |
| DP-01 | Referência ao JSON oficial, registro da manifestação EDP por ponto de conexão, proveniência, confiança e confirmação técnica | @po/@architect | Autoridades da seção 2.4 e responsável técnico | Mudança da fonte normativa ou da jornada de captura |
| DP-02 | Decisão de escopo delta e matriz de capacidade por consumidor | @po/@architect | @po/@architect | Mudança de release ou capacidade |
| DP-03 | Parecer para cargas trifásicas não enquadradas diretamente | responsável técnico/@architect | responsável técnico dentro de sua autoridade | Mudança normativa ou do modelo |
| DP-04 | Fluxo de intenção, solicitação, confirmação e perfis associados | @po | @po | Mudança da jornada ou dos papéis |
| DP-05 | Referência ao JSON oficial, catálogo versionado e evidência de comprovação da área de concessão | @po/@architect | @po/@architect | Mudança da fonte normativa ou da fonte de comprovação |
| DP-06 | Estado e tratamento aprovado para rede subterrânea | @po/@architect | @po/@architect | Mudança de escopo ou fonte normativa |
| DP-07 | Política de governança, autorização, override e auditoria | @po/@architect | @po/@architect | Mudança de perfil, parâmetro ou política |
| DP-08 | Decisão de escopo MMGD e entradas mínimas | @po/@architect | @po/@architect | Mudança de release ou entrada disponível |
| DP-09 | Inventário dos contextos genéricos e decisão de destino | @po/@architect | @po/@architect | Novo consumidor ou contexto identificado |
| DP-10 | Decisão arquitetural do contrato e estratégia de compatibilidade | @architect | @architect | Mudança de contrato, schema ou consumidor |
| GP-01 | Checklist GP-01.1–GP-01.4 com links para as evidências | @po/@ux/@architect | Conforme checklist | Mudança de persona, perfil, release ou meta |
| GO-01A | Relatório de CI/gates, homologação, rollout, rollback operacional e observabilidade | @devops/@architect/@qa | @devops/@architect/@qa dentro de suas autoridades | Mudança de build, ambiente, rollout ou risco operacional |
| GO-01B | GO-01A válido, inventário final, políticas/evidências de dados, rollback semântico e dry run | @devops/@architect/@qa/@data-engineer | @devops/@architect/@qa dentro de suas autoridades | Mudança de dados, migração, contrato ou inventário |
| RV-01 | Relatório formal de revalidação da versão 0.8 e Change Log atualizado | @pm/@po | @pm/@po | Toda alteração material posterior do PRD |

Para GN-01 e DP-03, o parecer não precisa incluir nome, registro profissional,
organização, data, bloco `documento_normativo_analisado`/`versao` ou assinatura.
A evidência mínima permanece composta pela decisão técnica de cada gate, pelo
tratamento aplicável, pela fundamentação normativa no corpo das conclusões e
pela referência ao artefato versionado.

#### 2.4.3 Snapshot consolidado após o parecer GN-01/DP-03

Este snapshot incorpora
`docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md` e
`docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md`. Ele é posterior
à reexecução histórica de RV-01. A contribuição @po foi reexecutada em
2026-07-27 e a coaprovação @pm foi concluída no adendo mais recente de RV-01.

| Gate | Estado consolidado | Efeito e evidência vigente |
|---|---|---|
| GN-01 | `APROVADO` | Fronteiras, topologias e compatibilidade de fases ratificadas no parecer técnico |
| DP-01 | `APROVADO — NÃO BLOQUEIA STORIES` | JSON formalizado como fonte oficial de consulta normativa e consulta do usuário à EDP coaprovada para o ponto de conexão; por projeto, somente manifestação registrada e confirmação técnica permitem `TOPOLOGIA_CONFIRMADA` |
| DP-02 | `APROVADO` | Delta representável desde o modelo e ativado de forma faseada por consumidor |
| DP-03 | `APROVADO` | `REQUER_ANALISE_DA_CONCESSIONARIA` e bloqueios ratificados no parecer técnico |
| DP-04 | `PENDENTE` | Jornada e autoridades para intenção, solicitação e confirmação não aprovadas |
| DP-05 | `APROVADO — NÃO BLOQUEIA STORIES` | JSON formalizado como fonte oficial de consulta normativa, com catálogo oficial versionado de 28 municípios, proveniência auditável e comportamento fail-closed coaprovados |
| DP-06 | `APROVADO` | Rede subterrânea permanece fora do escopo com estado acionável |
| DP-07 | `PENDENTE` | Matriz de perfis, autorização, override e auditoria não aprovada |
| DP-08 | `APROVADO` | MMGD sem entradas suficientes produz pendência bloqueante |
| DP-09 | `PENDENTE` | Direção arquitetural aprovada; faltam inventário, GO-01B e coaprovação @po |
| DP-10 | `APROVADO` | Contrato canônico e estratégia de compatibilidade definidos no ADR |
| GP-01.1 | `PENDENTE` | Persona, papéis e jornada dependem de @ux/@po |
| GP-01.2 | `APROVADO` | Fronteira e capacidades condicionadas aprovadas em `docs/prd/GP-01.2-DECISAO-FRONTEIRA-RELEASE-EDP-V9.md` |
| GP-01.3 | `PENDENTE` | Depende de DP-04/DP-07 e de matriz de perfis coaprovada |
| GP-01.4 | `PENDENTE` | Baseline e metas UX dependem de @ux/@po |
| GP-01 | `PENDENTE` | Aprovação parcial não libera pacote 6 ou Release 1 |
| GO-01A | `REPROVADO` | Release 1 não possui evidência operacional suficiente para ativação |
| GO-01B | `NÃO APROVADO` | GO-01A inválido e evidências de dados/operação ainda incompletas |
| RV-01 | `APROVADO` | Condições da decisão PO foram satisfeitas por DP-01/DP-05 coaprovados; reexecução e coaprovação @pm registradas no adendo mais recente |

O fechamento de RV-01 aprova o baseline de produto e permite que o QA
reavalie a entrada do primeiro pacote no SDC. A criação de stories ainda
aguarda o QA preflight. Implementação, ativação da Release 1 e remoção do
legado continuam condicionadas, respectivamente, à story válida e aos gates
aplicáveis de pacote e marco.

DP-01 e DP-05 estão desbloqueados especificamente para a criação das stories
dos pacotes que os referenciam. Eles não devem ser tratados como bloqueadores
de desdobramento enquanto a fonte, a jornada, a norma, o modelo e as
evidências coaprovadas permanecerem válidos. O QA preflight e os demais gates
aplicáveis continuam independentes e podem bloquear a criação ou a execução de
uma story.

### 2.5 Matriz de Rastreabilidade dos Requisitos

| Requisitos | Origem normativa/análise | Critérios relacionados |
|---|---|---|
| FR1–FR4 | EDP-PE-001–007; plano §§2, 7.1–7.4 | AC-07, AC-08, AC-11 |
| FR5–FR15 | EDP-PE-005–017 e EDP-PE-025–028; plano §§4, 5, 7 | AC-09–AC-15 |
| FR16–FR19 | EDP-PE-018–024; plano §§7.1, 9.5–9.11 | AC-27–AC-30 |
| FR20–FR25 | Findings F-01, F-04 e F-09; plano §§6.11, 7.6, 9.7–9.13 | AC-16–AC-21, AC-34 |
| FR26–FR30 | EDP-PE-029; plano §§8, 9.4, 9.14, 9.17 | AC-01–AC-07, AC-22, AC-25, AC-26, AC-32 |
| FR31–FR33 | Findings F-08, F-10 e F-11; Constitution Art. I; plano §§10.5, 10.8, 14 | AC-23–AC-25, AC-31, AC-33, AC-35 |
| FR34–FR36 | Plano §§9.10–9.16 | AC-18, AC-21, AC-22 |
| NFR1–NFR14 | Constitution Arts. I, IV e V; plano §§10–15 e 18; bloqueadores do relatório PM §§10.2–10.5 | AC-06, AC-26, AC-31–AC-37, Definition of Done e matriz de testes |
| CR1–CR11 | Plano §§5.4, 6.4, 13–17 | AC-02, AC-16–AC-25 |
| GP-01, GO-01A, GO-01B e RV-01 | Bloqueadores de produto, autorização, retenção, operação e revalidação do relatório PM §§10.2–10.6 | AC-31, AC-34–AC-37, Definition of Done e matriz de testes |

---

## 3. Objetivos da Reestruturação da Interface

### 3.1 Integração com a UI existente

A reestruturação deve permanecer na jornada atual do projeto e utilizar os padrões do aplicativo: rotas file-based do TanStack Start, componentes IBM Carbon e gerenciamento de estado remoto pelo TanStack Query. A interface apresenta o resultado do domínio; ela não recalcula compatibilidade, categoria ou subcategoria.

O campo deixa de funcionar como um filtro binário de IDs genéricos e passa a representar a avaliação produzida pelo domínio EDP. Estados sem determinação automática devem oferecer diagnóstico e próxima ação, nunca um controle integralmente desabilitado sem resolução.

### 3.2 Telas e visualizações modificadas

- Padrão de entrada, especialmente “Fornecimento elétrico do projeto” e “Padrão compatível”.
- Cards EDP de demanda, categoria/subcategoria, condutor/isolação, diagnósticos e contratos.
- Modais de criação e edição de Dependências, para tensões disponíveis e cargas especiais.
- Estados de prontidão e navegação do projeto.
- Divisão de circuitos, Correntes e Balanceamento, quando bloqueados ou invalidados pelo padrão.
- Dimensionamento de condutores, para obsolescência e recálculo decorrentes do fornecimento.
- Unifilar e suas exportações.
- Relatório técnico e seus diagnósticos.
- Editor de parâmetros EDP, conforme a decisão de governança DP-07.

### 3.3 Requisitos de consistência da interface

- Usar componentes e padrões de interação do IBM Carbon já presentes no aplicativo.
- Exibir categoria mínima e categoria solicitada como informações distintas.
- Exibir topologia, tensões, categoria, subcategoria e estado em cada alternativa.
- Apresentar razões concretas para incompatibilidade, estudo, pendência ou fora de escopo.
- Exigir confirmação e justificativa para categoria superior.
- Nunca rotular “requer estudo” como “compatível”.
- Não oferecer 380 V no contexto EDP V9.
- Exibir norma e versão que sustentam a avaliação.
- Informar configuração obsoleta e exigir novo cálculo antes do salvamento.
- Manter estados de carregamento, falha, ausência de dados e conflito de versão acionáveis.
- Invalidar e atualizar explicitamente todas as consultas dependentes após uma decisão válida.

---

## 4. Restrições Técnicas e Requisitos de Integração

### 4.1 Stack existente observada

| Camada | Tecnologia observada | Restrição relevante |
|---|---|---|
| Linguagem | TypeScript 5.8, modo `strict` | Manter tipos explícitos para estados e tensões |
| Runtime web | TanStack Start / Vite | Preservar rotas file-based e build existente |
| Interface | React 19 e IBM Carbon | Reutilizar componentes e padrões atuais |
| Estado remoto | TanStack Query | Invalidar todas as chaves dependentes |
| Validação | Zod | Manter validação também no servidor |
| Persistência | Supabase/PostgreSQL | Evolução versionada e não destrutiva |
| Testes | Vitest | Integrar aos testes de domínio, serviços, API e UI existentes |
| Imports | Alias `@/*` para `src/*` | Preferir imports absolutos conforme a Constitution |

As versões registram o estado analisado, não uma obrigação de congelamento tecnológico. Mudança de stack ou criação de runtime paralelo exige decisão do @architect e não faz parte deste PRD.

### 4.2 Estratégia de integração

**Banco de dados:** evolução aditiva e versionada dos dados de configuração; preservação do legado e do histórico; separação entre referência oficial, decisão do projeto e override. DDL e políticas finais pertencem a @data-engineer/@architect.

**API:** retornar candidatos avaliados e razões; validar seleção contra entradas e versão atuais; rejeitar salvamento obsoleto; expor um único resultado efetivo aos consumidores EDP.

**Frontend:** substituir a dependência do catálogo genérico na rota EDP; consumir estados estruturados do domínio; manter regras elétricas fora dos componentes visuais; invalidar queries downstream após alteração.

**Testes:** adicionar testes unitários puros do avaliador, testes de contrato, API, persistência/migração, integração ponta a ponta, regressão do cenário visual e cobertura dos módulos consumidores.

### 4.3 Organização de código e padrões

**Estrutura:** manter regras de distribuidora no domínio EDP-SP, modelos compartilhados em domínio/modelo, orquestração em serviços, validação de payloads em schemas, persistência em infraestrutura e apresentação em rotas/componentes.

**Convenções:** TypeScript estrito, estados discriminados, propriedades nomeadas para tensões FN/FF, unidades explícitas e imports pelo alias `@/`.

**Documentação:** toda regra normativa deve manter fonte e versão; decisões arquiteturais e técnicas pendentes devem ser registradas antes das stories afetadas; checklist e File List devem ser atualizados em cada story.

**Restrições:** não inferir FN/FF pela posição em arrays; não duplicar regra normativa na UI; não transformar override em fonte verificada; não reutilizar a especificação do ramal como dimensionamento dos circuitos internos.

### 4.4 Build, implantação e operação

**Build:** integrar ao processo Vite/TanStack Start existente e validar `lint`, `typecheck`, testes e build.

**Implantação:** existem artefatos de publicação para Hostinger, mas o pipeline de produção consolidado não está documentado nos artefatos analisados. Estratégia de rollout, feature flag, rollback e ambiente de homologação permanecem `TBD — @architect/@devops`.

**Observabilidade:** expor inventário de legado, divergências entre contratos, pendências de rede, decisões obsoletas, estudos técnicos e resultados de migração antes da remoção do fluxo antigo.

**Configuração:** catálogo oficial versionado e imutável em runtime; decisões e overrides armazenados separadamente; atualização normativa deve marcar resultados afetados como obsoletos.

### 4.5 Riscos técnicos e mitigação

| Risco | Severidade | Mitigação requerida |
|---|---|---|
| Corrente calculada com tensão errada | Crítica | Contrato único, propriedades FN/FF nomeadas e teste ponta a ponta |
| Conversão silenciosa de 380 V | Crítica | Bloqueio explícito na migração e testes negativos |
| Categoria incorreta nas fronteiras | Alta | Gate GN-01 e testes exatos de 12/25/75 kW |
| Solicitação superior tratada como enquadramento | Alta | Estados e campos separados, confirmação explícita |
| Perda de configuração existente | Alta | Migração não destrutiva, reversibilidade e auditoria |
| Override tratado como norma verificada | Alta | Proveniência e status separados |
| Subcategoria estrutural incompleta | Alta | Contrato que preserve todos os atributos oficiais |
| Resultado downstream não invalidado | Alta | Matriz de dependências e testes de invalidação |
| Rede subterrânea avaliada pela norma aérea | Alta | Gate de escopo e estado próprio |
| MMGD ignorada | Alta quando aplicável | Pendência explícita até haver entrada suficiente |
| Regressão em outros fornecedores | Média | Isolar o módulo EDP do catálogo genérico |
| Alterações concorrentes no app brownfield | Alta | Baseline reproduzível e coordenação por stories antes da implementação |
| Versão normativa antiga indisponível para auditoria | Crítica | Repositório central imutável de versões oficiais |
| Metadados conflitantes entre EDP v06 e V9 | Crítica | Validação automática de versão em catálogo, contrato, documentação e relatório |
| Correção de demanda alterar projetos em massa | Alta | Relatório de impacto e recálculo em modo comparação |
| Dual-write criar fontes divergentes durante a transição | Crítica | Uma escrita canônica; legado estritamente somente leitura |
| Catálogo mudar entre avaliação e salvamento | Alta | Validar versão/hash nas duas operações |
| Topologia manual incorreta | Alta | Proveniência, autoria, confiança e confirmação do dado |
| Carga especial não classificada passar como TUE | Crítica | Classificação obrigatória ou pendência bloqueante |
| Divisão manual violar semântica delta | Alta | Revalidação por topologia, fases e finalidade da carga |
| Tempestade de recálculos após invalidação | Média/Alta | Grafo de dependências e controle arquitetural de disparos |
| CLI, API e UI divergirem nos estados | Alta | Contrato compartilhado e testes contratuais |
| Rollback restaurar schema sem restaurar significado | Crítica | Snapshot e rollback semântico testado |
| Solicitação superior parecer aprovação | Alta | Estados e linguagem distintos para intenção, solicitação e confirmação |
| Delta faseado avançar para consumidor incompatível | Alta | Matriz de capacidade e bloqueio por consumidor |
| Fixture divergir da interpretação normativa aprovada | Alta | Testes rastreados ao parecer GN-01/DP-03 e revalidação em caso de mudança normativa |
| Relatório antigo perder sua base normativa | Crítica | Referência permanente à versão oficial utilizada |
| Ativação da Release 1 sem prontidão operacional | Alta | Gate GO-01A antes da ativação |
| Remoção do legado sem prontidão operacional completa | Alta | Gate GO-01B antes do pacote 8 |

---

## 5. Estrutura do Épico

### 5.1 Decisão de estrutura

**Épico único:** Padrão de Entrada EDP V9 Canônico e Rastreável.

**Objetivo:** eliminar a dupla fonte de verdade e garantir que avaliação, seleção, persistência, circuitos, correntes, dimensionamento, unifilar e relatório utilizem o mesmo fornecimento EDP, com rastreabilidade normativa e migração segura.

Um único épico preserva o resultado sistêmico e impede que uma camada seja declarada concluída enquanto o produto ainda usa contratos concorrentes. A execução permanece incremental por meio dos oito pacotes abaixo.

Os pacotes são briefings para planejamento. Não constituem stories formais; @po/@sm devem dimensioná-los, criar as stories e distribuir seus critérios.

### 5.2 Gates por pacote

| Gate | Pacotes bloqueados |
|---|---|
| GN-01 — fronteiras de 12/25 kW | Casos de fronteira dos pacotes 2 e 8 |
| DP-01 — fonte da topologia | 1, 2, 4 e 6 |
| DP-02 — ativação do fluxo delta | Ramos operacionais delta dos pacotes 2, 6 e 8; não bloqueia representação nem persistência |
| DP-03 — cargas trifásicas abaixo das faixas T | Casos correspondentes dos pacotes 2 e 8 |
| DP-04 — categoria superior | 4, 6 e 7 |
| DP-05 — área de concessão | 2, 4 e 6 |
| DP-06 — rede subterrânea | 2, 4 e 6 |
| DP-07 — governança de parâmetros | 4, 6 e 7 |
| DP-08 — MMGD | 2, 4 e 7 |
| DP-09 — destino do catálogo genérico | 8 |
| DP-10 — contrato canônico | 3, 4, 5, 6, 7 e 8 |
| GP-01 — prontidão de produto | Pacote 6 e ativação da primeira release para usuários |
| GO-01A — prontidão de ativação | Ativação da Release 1 |
| GO-01B — prontidão de remoção | Remoção do legado no pacote 8 |
| RV-01 — revalidação do PRD 0.8 | Conversão dos pacotes em stories implementáveis; investigação independente pode prosseguir |

Uma decisão bloqueia somente o pacote indicado. Trabalho independente pode prosseguir quando possuir entradas e critérios aprovados.

### 5.3 Sequência dos pacotes

```text
Modelo → Avaliador → Contrato
                         ├─→ API/Persistência/CLI
                         │              ↓
                         └─→ Consumidores downstream
                                        ↓
                                       UI
                                        ↓
                           Relatório e auditoria
                                        ↓
                         Regressão + remoção legado
```

| Pacote | Resultado esperado | Dependências | Evidência de saída |
|---|---|---|---|
| 1. Modelo normativo e catálogo estrutural | Domínio representa escopo, rede, topologia, tensões, categorias, subcategorias, estados e especificação física completa | DP-01; representação delta independe de DP-02 | Matriz estrela/delta representável; catálogo validado e versionado |
| 2. Demanda e avaliador de candidatos | Função pura calcula demanda, categoria, corrente, subcategoria e alternativas com motivos | Pacote 1; GN-01, DP-01, DP-03, DP-05, DP-06 e DP-08; DP-02 somente para o ramo delta operacional | Testes de fronteira, cargas especiais, demanda e estados |
| 3. Contrato canônico e fachada | Um contrato tipado expõe a decisão efetiva e uma fachada mantém a transição | Pacotes 1–2; DP-10 | Testes de contrato e compatibilidade sem uso de posição em arrays |
| 4. API, persistência, versionamento, CLI e observabilidade | Seleção validada no servidor, configuração versionada, migração auditável, operação CLI e diagnósticos observáveis | Pacote 3; DP-01, DP-04–08, DP-10 | Avaliação/consulta/diagnóstico via CLI, migração reversível/idempotente, rejeição de estado obsoleto e indicadores operacionais |
| 5. Convergência dos consumidores | Divisão, Correntes, Balanceamento, Dimensionamento e Unifilar usam a mesma decisão | Pacotes 3–4 | Testes integrados confirmam as mesmas tensões, fases e categoria |
| 6. Reestruturação da UI | Padrão e Dependências exibem alternativas, pendências, confirmação e motivos sem dead-end | Pacotes 4–5; DP-01, DP-04–07, DP-10 e GP-01; DP-02 somente para ativação do ramo delta | Fluxos UI e regressão da captura aprovados; persona, perfis e metas UX ratificados |
| 7. Relatório técnico e auditoria consolidada | Relatório e auditoria exibem uma fonte, especificação, proveniência e pendências | Pacotes 4–6; DP-04, DP-07, DP-08 e DP-10 | Relatório/unifilar coerentes e histórico reconstruível |
| 8. Regressão ponta a ponta e remoção do legado | Suíte completa verde; fluxo genérico removido somente da rota EDP sem dependências remanescentes | Pacotes 1–7; GN-01, DP-03, DP-09, DP-10 e GO-01B; DP-02 define o conjunto de testes delta | Inventário final, testes E2E, rollback validado, ausência de dupla fonte na EDP e não regressão dos contextos externos |

### 5.4 Fronteiras de release

| Marco | Pacotes | Uso permitido | Condições de saída | Legado |
|---|---|---|---|---|
| Fundação interna | 1–4 | Desenvolvimento, testes e investigação; sem ativação da nova UI para usuários | Gates aplicáveis dos pacotes resolvidos; CLI, contrato, persistência e migração demonstráveis | Preservado para leitura, diagnóstico e rollback; nenhuma nova escrita EDP |
| Release 1 — convergência EDP | 1–7 | Primeira entrega ativável para usuários da rota EDP | RV-01, GP-01 e GO-01A aprovados; consumidores convergentes; regressão do dead-end, relatório e auditoria aprovados | Adaptador legado permanece somente leitura para auditoria e rollback |
| Release 2 — remoção controlada EDP | 8 | Remoção do contrato genérico exclusivamente da rota EDP | DP-09, DP-10 e GO-01B aprovados; inventário sem dependências EDP; dry run e rollback semântico comprovados | Removido da rota EDP; preservado fora dela quando houver requisito explícito |

- A correção estrutural somente pode ser declarada entregue na Release 1; a fundação interna isolada não resolve o resultado do usuário.
- A Release 1 não autoriza remover o legado e deve operar sem dual-write.
- A Release 2 não autoriza descontinuar o catálogo genérico para outras distribuidoras ou modos. Qualquer remoção fora da rota EDP exige requisito, análise de impacto e story próprios.
- Delta 240/120 V, MMGD, editor avançado de parâmetros e integração externa seguem as decisões condicionantes já registradas. Quando não integrarem a release, o produto deve expor bloqueio ou pendência explícita, sem alegar cobertura integral.

### 5.5 Requisitos de integração e rollback

- Contratos novos entram antes da remoção dos antigos.
- A configuração legada original permanece preservada para auditoria.
- A fachada pode ler o legado para diagnóstico e migração, mas novos resultados EDP são produzidos somente pelo contrato canônico.
- Consumidores migram por etapas, mas nenhum resultado novo pode combinar as duas fontes.
- A UI só persiste decisões pelo contrato novo e validado no servidor.
- Catálogo, schema e decisão possuem versões identificáveis.
- Cada story deve definir rollback compatível com sua alteração.
- O pacote 8 só remove adaptadores temporários da rota EDP depois de o inventário confirmar ausência de dependências EDP não aprovadas.
- Catálogo e consumidores genéricos fora da rota EDP permanecem inalterados até existir requisito e story específicos para seu destino.
- Testes de regressão devem acompanhar cada pacote, não apenas o fechamento do épico.

**Invariante de rollback semântico:**

1. O legado permanece somente leitura e nunca volta a produzir novos resultados EDP.
2. O rollback restaura o último estado canônico comprovadamente válido ou bloqueia novas escritas quando a restauração segura não for possível.
3. Nenhuma estratégia de rollback pode criar dual-write ou copiar alterações canônicas para uma configuração legada editável.
4. Eventos posteriores ao snapshot permanecem no histórico; resultados downstream incompatíveis são invalidados antes da retomada.
5. Repetir rollback ou restauração sobre o mesmo snapshot não pode produzir estado diferente sem nova entrada autorizada.

---

## 6. Critérios de Aceite do Épico

### 6.1 Campo e candidatos

- **AC-01:** em estado sem candidato automaticamente compatível, o campo não fica com todas as opções mudas; mostra alternativas avaliadas e motivos.
- **AC-02:** nenhuma opção da tela EDP é carregada do catálogo genérico 127/220/380.
- **AC-03:** toda opção exibe topologia, tensões, categoria e subcategoria quando disponível.
- **AC-04:** opção incompatível não pode ser salva no cliente nem na API.
- **AC-05:** opção que requer estudo não é rotulada como compatível.
- **AC-06:** categoria superior exige ação explícita e registra que decorre da Nota 03.
- **AC-07:** ausência de dados de rede gera pendência acionável.

### 6.2 Norma e cálculo

- **AC-08:** estrela 220/127 V e delta 240/120 V são representáveis pelo domínio e pelo contrato.
- **AC-09:** exatamente 12 e 25 kW seguem a interpretação ratificada em GN-01, distinguindo topologia e presença de equipamento trifásico; casos sem enquadramento direto retornam `REQUER_ANALISE_DA_CONCESSIONARIA`.
- **AC-10:** D delta e T delta seguem condições distintas.
- **AC-11:** carga acima de 75 kW não recebe padrão BT automático.
- **AC-12:** cargas especiais produzem bloqueio ou estudo conforme limites.
- **AC-13:** Tabela 005 é indexada por kW ativo.
- **AC-14:** DT reconcilia com a soma dos grupos a–i.
- **AC-15:** corrente e subcategoria registram fórmula e entradas.

### 6.3 Consistência sistêmica

- **AC-16:** Padrão de entrada, Divisão, Correntes, Balanceamento, Dimensionamento, Unifilar e Relatório usam o mesmo contrato.
- **AC-17:** uma troca de padrão invalida todos os resultados dependentes.
- **AC-18:** não aparece 380 V em projeto EDP V9.
- **AC-19:** tensão fixa de carga nunca é alterada pela seleção.
- **AC-20:** circuitos incompatíveis ficam bloqueados com razão, sem fallback.
- **AC-21:** relatório não publica dois padrões concorrentes.

### 6.4 Persistência e auditoria

- **AC-22:** seleção persiste norma, versão, decisão e proveniência.
- **AC-23:** catálogo oficial não é duplicado como configuração editável em cada projeto.
- **AC-24:** configuração legada não é reinterpretada silenciosamente.
- **AC-25:** atualização normativa marca decisões obsoletas.
- **AC-26:** histórico registra autor, data, valor anterior, novo valor e justificativa.

### 6.5 Especificação física

- **AC-27:** subcategoria expõe medição, proteção, condutores, caixa, eletroduto, poste e aterramento.
- **AC-28:** PVC e EPR/XLPE usam as colunas corretas.
- **AC-29:** acima de 150 A gera medição indireta e pendência documental.
- **AC-30:** U, D2 e T2 exibem a responsabilidade diferenciada do ramal.

### 6.6 CLI e observabilidade

- **AC-31:** antes da disponibilização da nova UI, a CLI permite avaliar candidatos, consultar a decisão canônica, inspecionar diagnósticos e executar inventário/migração com os mesmos estados e contrato da API.

### 6.7 Controles de histórico, migração e operação

- **AC-32:** uma decisão e um relatório históricos podem ser reconstruídos usando a versão oficial imutável referenciada, mesmo após atualização normativa; catálogo, contrato, documentação e relatório rejeitam metadados normativos divergentes.
- **AC-33:** a migração cria snapshot prévio, mantém o legado somente leitura, realiza uma única escrita canônica e comprova rollback semântico e idempotência; o rollback restaura o último estado canônico válido ou bloqueia novas escritas, sem reativar escrita legada, cálculo genérico EDP ou dual-write, e preserva a auditoria dos eventos posteriores.
- **AC-34:** para a mesma fixture e versão, CLI, API e UI apresentam os mesmos estados, motivos e decisão canônica.
- **AC-35:** o contrato genérico não pode ser removido da rota EDP enquanto GO-01B não comprovar GO-01A válido, retenção e acesso, backup/restauração, rollback semântico, suporte/resposta a incidentes e dry run aprovados.

### 6.8 Prontidão de produto e ativação

- **AC-36:** o pacote 6 e a Release 1 permanecem bloqueados enquanto qualquer item GP-01.1–GP-01.4 estiver pendente, reprovado ou obsoleto; a evidência deve identificar separadamente o estado de cada item.
- **AC-37:** a Release 1 não pode ser ativada enquanto GO-01A não comprovar ambientes, CI/gates, homologação, rollout, rollback operacional e observabilidade aprovados pelas autoridades correspondentes.

---

## 7. Estratégia Mínima de Testes

### 7.1 Fronteiras de categoria

| Caso | Topologia | Carga | Resultado de referência |
|---|---|---:|---|
| B01 | estrela | 0 kW | U |
| B02 | estrela | 11,999 kW | U |
| B03 | estrela | 12,000 kW sem carga trifásica | U |
| B04 | estrela | 12,001 kW sem carga trifásica | D |
| B05 | estrela | 25,000 kW sem carga trifásica | D |
| B06 | estrela | 25,001 kW | T |
| B07 | estrela | 75,000 kW | T |
| B08 | qualquer | 75,001 kW | fora de escopo/estudo |
| B09 | delta | 12,001 kW sem carga trifásica | D; operação condicionada à capacidade do consumidor conforme DP-02 |
| B10 | delta | 25–75 kW sem carga trifásica | D; operação condicionada à capacidade do consumidor conforme DP-02 |
| B11 | delta | 12,001–75 kW com carga trifásica | T; operação condicionada à capacidade do consumidor conforme DP-02 |
| B12 | estrela | 12,000 kW com carga trifásica | `REQUER_ANALISE_DA_CONCESSIONARIA` |
| B13 | delta | 12,000 kW com carga trifásica | `REQUER_ANALISE_DA_CONCESSIONARIA` |
| B14 | estrela | 25,000 kW com carga trifásica | `REQUER_ANALISE_DA_CONCESSIONARIA` |
| B15 | delta | 25,000 kW com carga trifásica | T; operação condicionada à capacidade do consumidor conforme DP-02 |
| B16 | delta | 11,999 kW com carga trifásica | `REQUER_ANALISE_DA_CONCESSIONARIA` |
| B17 | estrela | 24,999 kW com carga trifásica | `REQUER_ANALISE_DA_CONCESSIONARIA` |

GN-01 e DP-03 estão aprovados. Os resultados
`REQUER_ANALISE_DA_CONCESSIONARIA` continuam bloqueantes por regra operacional:
categoria automática e definitiva permanecem nulas até manifestação
documentada da EDP.

Como DP-02 aprovou a entrega faseada, B09–B11 e B15 devem validar a
representação integral no domínio e o bloqueio explícito em cada consumidor
cuja capacidade operacional delta ainda não tenha sido comprovada.

### 7.2 Tensões e topologia

- U estrela oferece FN 127 V.
- D/T estrela oferecem FN 127 V e FF 220 V.
- U delta oferece FN 120 V.
- D/T delta oferecem as tensões aplicáveis 120/240 V.
- 127/220 V não é tratado como equivalente a 120/240 V.
- 380 V não é candidato EDP.
- A fase de força delta não alimenta carga não trifásica.
- Consulta à EDP ainda não iniciada produz `CONSULTA_CONCESSIONARIA_NAO_INICIADA`.
- Consulta sem resposta produz `PENDENTE_CONSULTA_CONCESSIONARIA`.
- Resposta sem protocolo ou confirmação técnica produz `TOPOLOGIA_NAO_CONFIRMADA`.
- Somente manifestação da EDP registrada e confirmada pelo responsável técnico libera a topologia.

### 7.3 Categoria superior

- Projeto U sem necessidade FF: U determinado e D elegível.
- Projeto U com carga 220 V em estrela: U incompatível e D elegível por solicitação.
- Projeto D: T elegível por solicitação.
- Alternativa superior não é selecionada automaticamente.
- Seleção grava aceite e justificativa.
- Recálculo preserva a distinção entre categoria mínima e solicitada.

### 7.4 Cargas especiais e demanda

- Casos de raio X, solda, motores e bomba de incêndio nos limites e acima deles.
- Caso superior ao limite gera estudo, não candidato compatível.
- Tabela 005 muda de faixa pelo kW ativo, não por kVA.
- Fator de potência altera kW sem corromper kVA.
- Grupos a–i usam quantidade, maior/restantes e fatores corretos.
- `D1 + D3 = DT`.
- Unidades VA, W e kW permanecem explícitas.

### 7.5 Subcategorias

Cobrir U2; D2, D4, D6, D7, D9 e D10; T2, T4, T6, T7, T9 e T10.

Para cada linha, validar limite de corrente, proteção, medição, condutor PVC, condutor EPR/XLPE, caixa, eletroduto, poste/PCI, aterramento, motor e alertas. Incluir 150 A, imediatamente acima de 150 A, 350 A e acima de 350 A.

### 7.6 Integração ponta a ponta

Para a mesma fixture:

1. cadastrar dependências e cargas;
2. calcular demanda;
3. avaliar candidatos;
4. selecionar ou solicitar categoria;
5. dividir circuitos;
6. calcular correntes;
7. dimensionar;
8. montar unifilar;
9. gerar relatório.

Asserções obrigatórias: mesmo sistema, mesmas tensões, mesma categoria/subcategoria, nenhum consumidor EDP usando catálogo genérico, nenhuma tensão reinterpretada e todos os resultados dependentes invalidados após mudança.

### 7.7 Regressão do defeito observado

Fixture: cargas em 127 e 220 V, demanda compatível com categoria mínima U e rede estrela EDP.

Resultado esperado:

- U incompatível com a necessidade FF 220 V;
- D elegível por solicitação superior;
- seleção de D mediante confirmação;
- subcategoria D calculada pela corrente;
- Correntes, Dimensionamento e Unifilar usando 127/220 V;
- nenhuma opção silenciosamente desabilitada.

### 7.8 Migração

Cobrir configuração sem versão, catálogos com piso BI 8 e 0, `MONO-127`, `MONO-220`, `BI-127-220`, `TRI-220-380`, catálogo customizado, override EDP antigo, projeto sem topologia e repetição idempotente da migração.

### 7.9 Histórico, concorrência e rollback

- reconstruir decisão e relatório com versão normativa anterior;
- alterar catálogo ou carga entre avaliação e salvamento e rejeitar a decisão obsoleta;
- executar migração com snapshot, repetir sem mudança e realizar rollback semântico;
- comprovar que o legado permanece somente leitura durante a transição;
- comparar CLI, API e UI para a mesma fixture;
- rejeitar catálogo, contrato ou relatório com metadados normativos divergentes;
- validar carga especial desconhecida como pendência bloqueante;
- revalidar divisão manual em topologia delta;
- verificar bloqueio por consumidor quando delta estiver faseado;
- executar dry run do pacote 8 e impedir remoção quando GO-01B estiver incompleto.

### 7.10 Produto, autorização e operação

- comprovar que cada item GP-01.1–GP-01.4 possui estado independente e que qualquer item não aprovado bloqueia o pacote 6 e a Release 1;
- validar permissões positivas e negativas para solicitação/confirmação de categoria superior, overrides, parâmetros EDP, migração e rollback conforme a matriz aprovada;
- comprovar auditoria de toda ação privilegiada com autoria, data, justificativa e resultado;
- restaurar snapshot de decisão e auditoria conforme a política de backup aprovada e reconstruir seu significado;
- executar rollback sobre o mesmo snapshot mais de uma vez e comprovar a invariante da seção 5.5, sem escrita legada ou dual-write;
- verificar retenção, acesso e descarte segundo a política aprovada, sem eliminar a versão normativa necessária à reconstrução histórica;
- impedir ativação da Release 1 quando qualquer evidência de GO-01A estiver ausente ou obsoleta;
- simular falha operacional e comprovar monitoramento, suporte, escalonamento e resposta a incidente definidos em GO-01B;
- executar regressão em contexto não EDP e comprovar que o catálogo e seus consumidores permanecem funcionais.
- impedir criação de stories implementáveis enquanto RV-01 não contiver revalidação formal da versão corrente.

---

## 8. Escopo e Métricas de Sucesso

### 8.1 Incluído

- Domínio e catálogo EDP-SP V9.
- Carga instalada, demanda, categoria, corrente e subcategoria.
- Avaliação e seleção do padrão de entrada.
- Rede, topologia e tensões 220/127 V e 240/120 V.
- Cargas especiais relevantes ao atendimento.
- Especificação física, proteção e medição do padrão.
- API, persistência, auditoria e migração.
- Dependências, Divisão, Correntes, Balanceamento e Dimensionamento.
- Unifilar, relatório e estados de prontidão.
- CLI de inventário/migração, testes e remoção controlada do legado.

### 8.2 Fora de escopo da entrega

- Validação jurídica da norma.
- Substituição da análise ou aprovação de responsável técnico.
- Especificação do atendimento subterrâneo.
- Suporte integral a MMGD sem entradas e requisitos aprovados.
- Regras para outras distribuidoras não documentadas.

### 8.3 Limites de autoridade deste PRD

- Este documento não define a arquitetura final, que pertence ao @architect.
- Este documento não cria stories formais, autoridade de @po/@sm.
- Este documento não executa nem autoriza implementação; após as aprovações, a implementação é necessária para entregar o épico.
- Este documento não emite parecer final de qualidade, autoridade de @qa.

### 8.4 Métricas verificáveis

| Métrica | Meta |
|---|---:|
| Critérios AC-01–AC-37 aprovados | 100% |
| Consumidores EDP usando contrato genérico após migração | 0 |
| Ocorrências de 380 V em projeto EDP V9 | 0 |
| Candidatos exibidos sem estado e motivo | 0 |
| Reinterpretações automáticas de legado não inequívoco | 0 |
| Divergências de tensão/categoria entre módulos na mesma fixture | 0 |
| Migrações repetidas produzindo estado diferente sem nova entrada | 0 |
| Regressões comprovadas em consumidores fora da rota EDP | 0 |
| Ações privilegiadas executadas sem perfil autorizado | 0 |
| Itens GP-01.1–GP-01.4 aprovados antes do pacote 6 | 100% |
| Evidências obrigatórias de GO-01A aprovadas antes da ativação | 100% |
| Evidências obrigatórias de GO-01B aprovadas antes da remoção | 100% |
| Revalidação RV-01 da versão corrente aprovada antes das stories | 100% |
| Gates locais de qualidade aprovados | 100% |

Baseline de desempenho, tempo-alvo de entrega, adoção e métricas de negócio permanecem `TBD — validação @po/@architect`; devem ser definidos antes das stories afetadas. Os valores UX não são presumidos por este PRD e devem ser aprovados formalmente em GP-01.

Como condição de GP-01 e antes do pacote 6, @po/@ux devem capturar baseline e aprovar metas para:

- taxa de dead-end do seletor;
- tempo para resolver uma pendência de fornecimento;
- compreensão dos estados e motivos apresentados;
- abandono do fluxo;
- solicitações de suporte relacionadas ao padrão de entrada.

### 8.5 Definition of Done

O épico somente pode ser considerado concluído quando:

- decisões pendentes necessárias estiverem registradas;
- RV-01 estiver aprovado para a versão corrente antes da criação de stories implementáveis;
- stories e critérios estiverem aprovados;
- catálogo cobrir a matriz V9 definida para a entrega;
- avaliador de candidatos for determinístico, rastreável e testado;
- existir um único contrato efetivo por projeto EDP;
- todos os consumidores EDP estiverem migrados;
- GP-01.1–GP-01.4 estiverem individualmente aprovados antes do pacote 6 e da ativação da Release 1;
- GO-01A estiver aprovado antes da ativação da Release 1;
- persona, papéis e matriz de perfis estiverem aprovados, com DP-04 e DP-07 resolvidos para as ações afetadas;
- versões normativas referenciadas permanecerem imutáveis e reconstruíveis;
- persistência e migração forem idempotentes, com snapshot e rollback semântico testados;
- relatório de impacto do recálculo massivo estiver aprovado;
- cenário do defeito original estiver coberto;
- testes de estrela e fronteiras passarem; para delta, passarem os testes operacionais integrais ou os testes de representação com bloqueio explícito, conforme DP-02;
- relatório e unifilar refletirem o mesmo padrão;
- inventário confirmar ausência de dependências EDP não aprovadas no contrato genérico;
- a Release 1 tiver sido validada como convergência EDP sem dual-write e com o adaptador legado somente leitura;
- GO-01B estiver aprovado antes de qualquer remoção do legado;
- retenção, acesso, backup/restauração, suporte e resposta a incidentes possuírem políticas e evidências aprovadas em GO-01B;
- o catálogo genérico fora da rota EDP permanecer preservado, salvo requisito e story específicos aprovando destino diferente;
- `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passarem;
- checklist e File List de cada story estiverem atualizados;
- @qa emitir parecer de qualidade;
- documentação técnica e operacional estiver atualizada.

---

## 9. Direcionamento e Handoffs

### 9.1 Decisão PM

**Status:** `APPROVED — RV-01 APROVADO; QA PREFLIGHT PENDENTE; IMPLEMENTAÇÃO NÃO AUTORIZADA`.

O PRD está aprovado como baseline de produto para desdobramento incremental.
DP-01 e DP-05 estão fechados e não bloqueiam a criação das stories dos pacotes
dependentes. O pacote 1 está preliminarmente elegível porque DP-01 e RV-01
foram fechados, mas a criação da primeira story depende do novo parecer do QA
preflight. Cada pacote posterior permanece condicionado aos demais gates que
lhe sejam aplicáveis.

```yaml
latest_revalidation:
  date: "2026-07-27"
  prd_status: "Approved"
  rv_01: "APPROVED"
  story_creation_authorized: false
  implementation_authorized: false
  decision: "APPROVED AS PRODUCT BASELINE"
  po_reexecution: "COMPLETED"
  po_conditional_requirements_satisfied: true
  pm_coapproval: "APPROVED"
  package_1_preliminary_story_eligibility: true
  dp_01_blocks_story_creation: false
  dp_05_blocks_story_creation: false
  qa_preflight: "PENDING_REEXECUTION"
post_revalidation_architecture_evidence:
  GN-01: "APROVADO"
  DP-01: "APROVADO_NAO_BLOQUEIA_STORIES"
  DP-03: "APROVADO"
  DP-05: "APROVADO_NAO_BLOQUEIA_STORIES"
  architecture_consolidation: "CONCLUÍDA"
  rv_01_reexecution_required: false
```

O estado `Approved` confirma a suficiência do PRD para planejamento e
desdobramento incremental. Ele não promove gates exclusivos de outros pacotes,
não substitui o parecer do QA e não autoriza ativação ou remoção.

**Evidências vigentes:**

- `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json` — fonte oficial de consulta normativa para DP-01 e DP-05;
- `docs/prd/RV-01-PRD-PADRAO-COMPATIVEL-EDP-V9.md` — histórico da decisão PO condicional e adendo PM de aprovação de RV-01;
- `docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md` — consulta do usuário à EDP coaprovada como fonte de topologia por ponto de conexão;
- `docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md` — catálogo oficial versionado de 28 municípios coaprovado;
- `docs/prd/GP-01.2-DECISAO-FRONTEIRA-RELEASE-EDP-V9.md` — fronteira de release aprovada;
- `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md` — GN-01 e DP-03 aprovados;
- `docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md` — incorporação do parecer e snapshot arquitetural;
- `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md` — DP-10 aprovado;
- `docs/ux/GP-01-EVIDENCIAS-UX-EDP-V9.md` — GP-01.1 e GP-01.4 pendentes;
- `docs/architecture/GO-01B-EVIDENCIA-DADOS-EDP-V9.md` — contribuição de dados parcial; GO-01B não aprovado;
- `docs/qa/GO-01A-PRD-PADRAO-COMPATIVEL-EDP-V9.md` — GO-01A reprovado para ativação;
- `docs/qa/QA-PREFLIGHT-SDC-EDP-V9.md` — QA `FAIL` para criação de stories e implementação.

**Decisões aprovadas no snapshot vigente:** GN-01, DP-01, DP-02, DP-03, DP-05, DP-06, DP-08, DP-10 e GP-01.2. A direção arquitetural de DP-09 está aprovada, mas o gate global permanece `PENDENTE` até inventário, GO-01B e coaprovação @po. Em DP-01, a aprovação do desenho não substitui a manifestação da EDP e a confirmação técnica exigidas por projeto.

**Bloqueador imediato para criação da primeira story:** reexecução do QA
preflight. **Gates ainda abertos, sem reabrir RV-01:** DP-04 e DP-07 para os
pacotes 4, 6 e 7; GP-01 para o pacote 6 e ativação da Release 1; GO-01A para
ativação da Release 1; DP-09 e GO-01B para o pacote 8/Release 2. GN-01, DP-01,
DP-03 e DP-05 não devem voltar a ser listados como pendentes sem mudança da
fonte, da jornada, da norma, do modelo ou nova evidência conflitante.

### 9.2 Handoff para @po

- Validar a persona primária e os papéis de operador, cliente e responsável técnico com @ux.
- Concluído: JSON formalizado como fonte oficial de consulta normativa de DP-01; a jornada por consulta do usuário à EDP permanece coaprovada, a confirmação técnica continua obrigatória por projeto e o gate não bloqueia a criação de stories.
- Concluído: JSON formalizado como fonte oficial de consulta normativa de DP-05; decisão, catálogo e evidência permanecem coaprovados e o gate não bloqueia a criação de stories.
- Aprovar com @ux a matriz de perfis, baseline e metas UX de GP-01, respeitando DP-04 e DP-07.
- Concluído: fronteira da Release 1 e capacidades condicionadas aprovadas em GP-01.2.
- Concluído: coaprovação @pm de RV-01 registrada em 2026-07-27.
- Após o QA preflight favorável, encaminhar o pacote 1 para desdobramento por
  @sm.

### 9.3 Handoff para @architect

- Concluído: incorporar GN-01/DP-03, definir contrato canônico em DP-10, validar as dependências técnicas de GP-01.2 e fixar a direção arquitetural de DP-09.
- Concluído: coaprovar DP-01 e DP-05 com os controles fail-closed registrados nos respectivos artefatos.
- Pendente: coaprovar DP-07, DP-09 e GP-01.3 quando as evidências e decisões das demais autoridades existirem.
- Detalhar a evolução de persistência e a validação de obsolescência com @data-engineer, sem promover GO-01B antes da evidência operacional.
- Participar com @devops e @qa da reavaliação de GO-01A e GO-01B dentro de sua autoridade.

### 9.4 Validação técnica especializada

- Concluído em `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md`: interpretação das fronteiras de 12/25 kW, tratamento de cargas trifásicas sem enquadramento direto e leitura aplicável das Tabelas 001/002.
- O fluxo de categoria superior preserva categoria mínima, solicitada e definitiva separadas; perfis e autoridades permanecem pendentes em DP-04/DP-07/GP-01.3.

### 9.5 Handoff para @sm

Após parecer favorável do QA preflight e resolução dos gates aplicáveis ao
pacote selecionado:

- criar stories em `docs/stories/`;
- manter rastreabilidade para FR/NFR/CR/AC/DP/GP/GO/RV;
- preservar a sequência de dependências aprovada;
- organizar as stories pelos marcos de fundação interna, Release 1 e Release 2 definidos na seção 5.4;
- incluir rollback, testes locais, checklist e File List;
- não iniciar pela story visual.

### 9.6 Handoff para @qa

- Revisar a matriz mínima de testes.
- Definir gates por pacote.
- Validar regressão ponta a ponta e ausência de dupla fonte.
- Validar NFR13, NFR14 e os cenários da seção 7.10.
- Participar com @architect e @devops da definição e aprovação de GO-01A e GO-01B dentro de sua autoridade.
- Emitir o parecer final somente após os gates de qualidade.

### 9.7 Handoff para @devops

- Definir ambientes, CI/gates, estratégia de rollout e rollback operacional, monitoramento, suporte/resposta a incidentes e execução do dry run.
- Participar com @architect e @qa da definição e aprovação de GO-01A e GO-01B dentro de sua autoridade.
- Não ativar a Release 1 enquanto GO-01A estiver incompleto e não remover o legado enquanto GO-01B estiver incompleto.

### 9.8 Handoff para @data-engineer

- Propor schema e políticas de retenção, acesso, backup, restauração e descarte para decisões e auditoria.
- Demonstrar que snapshot e restauração preservam schema, significado e referência normativa.
- Fornecer as evidências de dados requeridas por GO-01B, sem emitir o parecer final de qualidade.

### 9.9 Handoff para @ux

- Validar com @po persona, papéis, jornada, linguagem, acessibilidade e compatibilidade de dispositivos.
- Capturar baseline e propor metas mensuráveis para as métricas UX da seção 8.4.
- Aprovar com @po os itens GP-01.1 e GP-01.4 e contribuir para GP-01.2/GP-01.3 dentro de sua autoridade.

---

## 10. Relatório de Validação PM

### 10.1 Resumo executivo

> **Nota de versionamento:** a pontuação e o veredito abaixo foram produzidos pela validação PM anterior às revisões analíticas 0.7 e 0.8. GN-01 e DP-03 foram aprovados posteriormente e estão incorporados nas seções 2.1, 2.4.3, 7.1 e 9. Somente @pm/@po podem revalidar a completude e atualizar o parecer por meio de RV-01 após as decisões de GP-01 e dos demais gates.

- **Completude estimada:** 72%.
- **Adequação do MVP:** grande; fronteiras de release definidas na seção 5.4, com aprovação de GP-01 ainda pendente.
- **Prontidão para arquitetura:** `NEARLY READY` — a investigação pode prosseguir, mas decisões normativas, de produto e NFRs bloqueiam implementação.
- **Decisão final PM:** `NEEDS REFINEMENT`.

O núcleo funcional está bem definido, rastreável e testável. Persona, fronteira de release, segurança/autorização, retenção, confiabilidade, implantação e operação agora possuem requisitos e gates explícitos, mas suas decisões, valores e evidências permanecem pendentes; por isso a implementação continua bloqueada nos pacotes correspondentes.

### 10.2 Resultado por categoria

| Categoria | Status | Questões críticas |
|---|---|---|
| 1. Definição do Problema e Contexto | PARTIAL | Persona, baseline quantitativo e horizonte de resultado |
| 2. Definição do Escopo MVP | PARTIAL | Fronteiras de release definidas; MoSCoW, aprovação de GP-01 e feedback do usuário pendentes |
| 3. Experiência do Usuário | PARTIAL | Acessibilidade, dispositivos, jornada formal e validação de linguagem |
| 4. Requisitos Funcionais | PASS | Priorização e desdobramento individual ainda pendentes |
| 5. Requisitos Não Funcionais | PARTIAL | NFR13/NFR14 e gates definidos; perfis, políticas, metas e evidências ainda pendentes |
| 6. Estrutura de Épico e Stories | PARTIAL | Stories formais dependem de @po/@sm |
| 7. Orientação Técnica | PARTIAL | Rollout, segurança, desempenho e observabilidade |
| 8. Requisitos Multifuncionais | PARTIAL | Autorização, retenção, ambientes, monitoramento e suporte |
| 9. Clareza e Comunicação | PASS | Cadência e responsáveis nominais pendentes |

### 10.3 Questões por prioridade

#### Bloqueadores

DP-01 e DP-05 estão aprovados, não bloqueiam a criação de stories e não
integram a lista abaixo.

1. Resolver DP-04, DP-07, DP-09, GP-01, GO-01A e GO-01B antes dos pacotes e marcos correspondentes.
2. Preservar a rastreabilidade das decisões aprovadas de GN-01 e DP-03 em contrato, fixtures, stories e implementação futura.
3. Aprovar a fronteira da Release 1 e as capacidades condicionadas definidas na seção 5.4.
4. Aprovar em DP-04, DP-07 e GP-01 os perfis autorizados para categoria superior, overrides, parâmetros EDP, migração e rollback.
5. Aprovar em GO-01B retenção, acesso, backup/restauração, suporte e resposta a incidentes para os dados de decisão e auditoria.

#### Alta prioridade

1. Capturar baseline e aprovar metas mensuráveis de desempenho.
2. Definir comportamento para falhas parciais e concorrência.
3. Definir rollout, homologação, rollback operacional e monitoramento.
4. Completar requisitos de acessibilidade e compatibilidade de dispositivos.
5. Definir persona e responsabilidades de operador, cliente e responsável técnico.

#### Média prioridade

1. Planejar feedback de usuários.
2. Definir horizonte de entrega e capacidade.
3. Definir suporte e resposta a incidentes.
4. Detalhar estados bloqueados na navegação.
5. Decidir se haverá integração externa com a concessionária ou apenas registro.

#### Baixa prioridade

1. Registrar responsáveis nominais e datas-alvo para os DPs.
2. Definir cadência de acompanhamento.
3. Registrar aprovações no Change Log.

### 10.4 Avaliação do MVP

**Fundação interna — pacotes 1–4, não ativável isoladamente para usuários:**

- modelo normativo e catálogo estrutural;
- demanda e avaliador;
- contrato canônico;
- persistência versionada e diagnóstico CLI;

**Release 1 — convergência EDP, primeiro resultado completo para usuários:**

- migração de Divisão, Correntes, Balanceamento, Dimensionamento, Unifilar e Relatório;
- correção do dead-end do campo;
- relatório coerente e regressão ponta a ponta.

**Entregas condicionadas a decisão:**

- ativação operacional integral de delta 240/120 V;
- suporte completo a MMGD;
- editor avançado de parâmetros;
- integração externa com concessionária;
- remoção controlada do legado na rota EDP, exclusiva da Release 2;
- qualquer remoção do catálogo genérico fora do contexto EDP, que exige requisito e story próprios.

Não é aceitável ativar somente a fundação interna nem cortar contrato canônico, validação no servidor ou migração dos consumidores e ainda considerar o defeito estrutural resolvido.

### 10.5 Prontidão técnica

**Pontos prontos:**

- stack e fronteiras atuais analisadas;
- dois fluxos concorrentes identificados;
- requisitos e critérios rastreáveis;
- consumidores, riscos e sequência de migração mapeados;
- matriz mínima de testes definida.

**Investigações necessárias:**

- materialização do contrato canônico conforme o ADR DP-10;
- evolução de schema e consistência transacional;
- estratégia de leitura durante a migração;
- perfis e autorização;
- desempenho e volume de dados;
- rollout, rollback e observabilidade;
- política de retenção e suporte.

### 10.6 Recomendações e próximos passos

1. Concluído: @pm reexecutou e coaprovou RV-01 sobre o snapshot da seção 2.4.3; @po e @ux ainda concluem GP-01 e @po conduz DP-04, DP-07 e DP-09 dentro de sua autoridade.
2. @po/@sm preservam GN-01 e DP-03 como aprovados e exigem rastreabilidade ao parecer nas stories afetadas.
3. @architect mantém DP-01 e DP-05 como coaprovados e coaprova DP-07, DP-09 e GP-01.3 quando as evidências existirem; as dependências técnicas de GP-01.2 já estão validadas.
4. @data-engineer propõe schema, retenção, acesso, backup/restauração e fornece evidências de dados para GO-01B.
5. @ux completa jornada, acessibilidade, validação da linguagem, baseline e metas UX.
6. @devops, @architect e @qa aprovam GO-01A para ativação e GO-01B para remoção, respeitando as evidências específicas de cada gate.
7. @sm cria stories somente após os gates aplicáveis, com rastreabilidade e testes locais.
8. @qa revisa a matriz e define gates por pacote.

### 10.7 Revalidação PM vigente — 2026-07-27

Esta subseção substitui somente o veredito e a prontidão do snapshot histórico
das subseções 10.1–10.3. As lacunas ali descritas permanecem válidas nos
pacotes e marcos aos quais foram vinculadas.

| Categoria do PM Checklist | Estado vigente | Efeito |
|---|---|---|
| 1. Problema e contexto | `PARTIAL` | Problema e usuários afetados estão claros; persona e impacto quantitativo continuam em GP-01.1 |
| 2. Escopo MVP | `PASS` | Fundação, Release 1 e Release 2 possuem fronteiras e condições aprovadas em GP-01.2 |
| 3. Experiência do usuário | `PARTIAL` | Não bloqueia o pacote 1; GP-01.1/GP-01.4 bloqueiam o pacote 6 |
| 4. Requisitos funcionais | `PASS` | Requisitos e critérios são rastreáveis e testáveis |
| 5. Requisitos não funcionais | `PARTIAL` | Autorizações e operação permanecem vinculadas a DP-07, GO-01A e GO-01B |
| 6. Épico e stories | `PARTIAL` | Épico e sequência estão definidos; stories dependem do QA preflight e de @sm |
| 7. Orientação técnica | `PASS` | Contrato, gates, riscos e sequência arquitetural estão documentados |
| 8. Requisitos multifuncionais | `PARTIAL` | Dados, perfis e operação possuem gates explícitos para os pacotes afetados |
| 9. Clareza e comunicação | `PASS` | Autoridades, handoffs, evidências e validade dos gates estão explícitos |

Pela métrica declarada (`PASS = 1`, `PARTIAL = 0,5`, `FAIL = 0`), a prontidão
documental é `72%` (`6,5/9`). O resultado é suficiente para aprovar o PRD como
baseline incremental porque não existe `FAIL` sem gate e pacote de contenção.

**Decisão PM vigente:** `APPROVED AS PRODUCT BASELINE`.

- **RV-01:** `APPROVED`.
- **Pacote 1:** preliminarmente elegível para criação de story.
- **Criação de story:** aguarda reexecução favorável do QA preflight.
- **Implementação:** não autorizada sem story válida e gates de qualidade.
- **Release 1:** não ativável enquanto GP-01 e GO-01A não forem aprovados.
- **Release 2/pacote 8:** bloqueada por DP-09 e GO-01B.

---

## 11. Referências

- `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md` — documento-base integral.
- `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json` — fonte oficial de consulta normativa para DP-01 e DP-05.
- `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md` — decisão técnica aprovada para GN-01 e DP-03.
- `docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md` — snapshot vigente dos gates com dependência arquitetural.
- `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md` — decisão do contrato canônico e da estratégia de compatibilidade.
- `docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md` — decisão PO da consulta do usuário à EDP como fonte de topologia por ponto de conexão.
- `docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md` — decisão PO e fontes oficiais da área de concessão.
- `docs/prd/GP-01.2-DECISAO-FRONTEIRA-RELEASE-EDP-V9.md` — aprovação PO da fronteira de release.
- `docs/stories/story-FORNECIMENTO-SELECAO-01.md` — story histórica.
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/distribuidora/edp-sp/` — domínio EDP existente.
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/nbr/catalogo-fornecimento.data.json` — catálogo genérico existente.
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/FornecimentoSelector.tsx` — comportamento atual do campo.
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/` — consumidores e contratos atuais.

---

*PRD elaborado e validado por Morgan (@pm), com revisão analítica de alinhamento por Atlas (@analyst) e consolidação arquitetural por Aria (@architect). Próximo passo: reexecução do QA preflight para decidir a entrada do pacote 1 no SDC.*
