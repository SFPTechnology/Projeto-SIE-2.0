# ADR EDP V9 — DP-10: Contrato Canônico e Estratégia de Compatibilidade

**Produto:** SIE — Sistema de Instalações Elétricas  
**Módulo:** Padrão de entrada EDP São Paulo V9  
**Autoridade:** Aria (@architect)  
**Data:** 2026-07-26  
**PRD:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md` v0.8  
**Status do ADR:** `DECIDIDO`  
**Gate encerrado por este ADR:** `DP-10`  
**Autorização de implementação:** `NÃO` — permanece condicionada a RV-01, às stories formais e aos gates de cada pacote

---

## 1. Escopo da decisão

Este ADR fixa somente:

1. a forma lógica do resultado canônico EDP V9;
2. as fronteiras entre domínio, aplicação, persistência, API/CLI e apresentação;
3. a estratégia de coexistência e retirada do contrato genérico na rota EDP;
4. as dependências arquiteturais dos gates de release.

O ADR não ratifica interpretação normativa, não define DDL/RLS finais, não aprova perfis de usuário, não cria stories e não autoriza ativação ou remoção de legado.

## 2. Evidências do brownfield

1. O tipo compartilhado `Tensao` aceita somente `127 | 220 | 380`, portanto não representa 120/240 V (`sistema-de-instala-es-el-tricas-sie-main/src/domain/modelo/padrao-fornecimento.ts:7`).
2. O serviço atual publica simultaneamente `contratos?: ContratosPadraoEntrada` e `edpSp?.contratos?: ContratosEDP` (`src/domain/servicos/servico-padrao-entrada.ts:43-51`).
3. Divisão de circuitos lê `edpSp?.contratos`, enquanto Correntes lê `tela.contratos`, comprovando duas fontes no mesmo projeto (`src/domain/servicos/servico-divisao-circuitos.ts:25-36`; `src/domain/servicos/servico-corrente.ts:271-275`).
4. O relatório atual admite e publica os dois contratos (`src/domain/servicos/servico-relatorio-projeto.ts:654-663`).
5. O contrato genérico usa array de tensões e o contrato EDP usa propriedades FN/FF nomeadas; adaptadores atuais ainda conciliam as duas formas (`src/domain/calculo/contratos-padrao-entrada.ts:9-19`; `src/domain/distribuidora/edp-sp/contratos.ts:19-45`).
6. A configuração genérica é persistida como JSON do projeto e os parâmetros EDP em persistência separada; não existe ainda um registro canônico versionado da decisão (`src/infra/supabase/mapeadores.ts:107-116`; `src/infra/supabase/repo-parametros-edp.supabase.ts:6`).
7. A API recebe `autor` como texto do payload e o acesso Supabase server-side usa `service_role`; não há matriz de perfis implementada para as ações privilegiadas do PRD (`src/api/schemas/padrao-entrada.ts:70`; `src/infra/supabase/client.ts:23-36`).
8. O `package.json` possui lint, typecheck, test e build, mas não possui comandos EDP de avaliação, inventário ou migração. Também não há workflow de CI no subaplicativo.

Essas evidências confirmam F-01, F-04, F-09 e F-11 do documento-base e impedem tratar qualquer contrato atual como o contrato final requerido pelo PRD.

## 3. DP-10 — decisão

### 3.1 Fonte canônica

Para todo projeto identificado como EDP-SP, haverá um único **Resultado Canônico de Padrão EDP** produzido pelo domínio EDP V9 e exposto por um único ponto do serviço de Padrão de entrada.

- O motor e o contrato permanecem TypeScript nativo no runtime TanStack Start existente.
- O domínio normativo permanece em `src/domain/distribuidora/edp-sp/`.
- React, rotas HTTP, Supabase e componentes visuais não calculam categoria, compatibilidade, corrente ou subcategoria.
- O motor genérico não pode produzir novo resultado para um projeto no contexto EDP.

### 3.2 Forma lógica obrigatória

O contrato será um agregado discriminado, sem inferência pela posição de arrays, contendo no mínimo os grupos abaixo.

| Grupo | Conteúdo obrigatório | Origem |
|---|---|---|
| Identidade normativa | distribuidora, documento, versão normativa, referência imutável do catálogo e versão do schema do resultado | FR28, NFR1, AC-22, AC-32 |
| Escopo e rede | área de concessão comprovada ou pendente, rede aérea/subterrânea, topologia e tensões nominais FN/FF nomeadas | FR1-FR4, AC-07, AC-08 |
| Snapshot de entradas | carga instalada kW/kVA, demanda VA, cargas/fases relevantes e identificador/hash ou versão das entradas | FR10-FR13, FR27, NFR7 |
| Avaliação | todos os candidatos, cada um com estado, motivos estruturados, categoria, topologia, tensões e subcategoria disponível | FR15, FR26, AC-01-AC-05 |
| Decisão efetiva | categoria mínima, categoria solicitada, confirmação quando aplicável, subcategoria e fundamento da decisão | FR5-FR9, AC-06 |
| Especificação física | proteção, fusível/chave, medição, condutores PVC e EPR/XLPE, caixa, eletroduto, poste/PCI, aterramento, limites e alertas | FR16-FR19, AC-27-AC-30 |
| Controle e proveniência | estado atual, obsolescência, autoria, datas, justificativa, origem oficial/override e versão/hash validada no salvamento | FR24, FR27-FR30, NFR5-NFR7 |
| Capacidade downstream | estado suportado ou bloqueado por consumidor, sempre com motivo explícito | FR21-FR23, NFR12 |

Os significados dos estados definidos no PRD são obrigatórios. Os nomes concretos dos enums podem ser definidos nas stories, desde que exista uma correspondência total e testada com:

- determinado;
- elegível por solicitação;
- incompatível;
- requer estudo técnico;
- dados de rede pendentes;
- fora de escopo subterrâneo;
- fora de escopo de média tensão;
- catálogo/decisão obsoleta.

Uma lista de candidatos não é a decisão efetiva. A decisão efetiva é opcional enquanto houver pendência, estudo, obsolescência ou fora de escopo; consumidores downstream devem permanecer bloqueados nesses estados.

### 3.3 Tensões e topologia

O contexto EDP deve possuir um tipo de tensão capaz de representar 120, 127, 220 e 240 V sem adicionar 120/240 ao catálogo genérico de outras distribuidoras por efeito colateral.

O contrato canônico usa propriedades nomeadas:

- `fase_neutro`;
- `fase_fase`, quando aplicável;
- topologia explícita.

É proibido inferir FN/FF pela ordenação de arrays ou considerar 127/220 equivalente a 120/240.

### 3.4 Ponto único de leitura

`servicoPadraoEntrada` será a fachada de aplicação para obter:

1. avaliação atual;
2. decisão efetiva;
3. diagnósticos;
4. versão/obsolescência;
5. capacidade dos consumidores.

Divisão, Correntes, Balanceamento, Dimensionamento, Unifilar e Relatório devem ler esse mesmo resultado. Nenhum consumidor EDP pode escolher entre `tela.contratos` e `tela.edpSp.contratos`.

### 3.5 Persistência lógica

A evolução será aditiva e versionada. O desenho físico final pertence a @data-engineer, mas deve respeitar estas separações:

1. catálogo oficial versionado e imutável;
2. contexto de rede e entradas do projeto;
3. decisão canônica corrente;
4. eventos append-only de seleção, confirmação, override, invalidação, migração, recálculo e rollback;
5. snapshot pré-migração e referência permanente à versão normativa utilizada.

O projeto persiste referência ao catálogo oficial, não uma cópia mutável. Fonte oficial e override permanecem registros distintos. Avaliação e salvamento validam a mesma versão/hash.

### 3.6 Compatibilidade e migração

Será usado um **adaptador de estrangulamento somente leitura**:

- lê o legado para inventário, diagnóstico, comparação, migração e rollback semântico;
- nunca calcula nem grava um novo resultado EDP pelo contrato genérico;
- classifica o legado segundo a matriz do PRD, sem equivalência por nome;
- nunca converte `TRI-220-380`;
- nunca presume que `BI-127-220` seja categoria mínima D;
- preserva customizações e casos ambíguos para revisão.

Cada operação nova possui uma única escrita canônica. Dual-write é proibido.

Os consumidores podem migrar incrementalmente, mas um resultado downstream individual não pode combinar fontes. Enquanto um consumidor ainda não suportar o estado canônico selecionado, ele retorna bloqueio explícito; não usa fallback genérico.

O catálogo genérico permanece preservado fora da rota EDP. Sua remoção da rota EDP só ocorre no pacote 8, após inventário sem dependências remanescentes e aprovação de GO-01B.

### 3.7 Ordem de entrega

A ordem arquitetural obrigatória é:

```text
domínio/modelo EDP
  -> avaliador puro
  -> contrato canônico + fachada somente leitura
  -> CLI e observabilidade
  -> API e persistência
  -> consumidores downstream
  -> UI
  -> relatório/auditoria
  -> inventário final e remoção controlada
```

CLI, API e UI reutilizam o mesmo contrato e os mesmos estados; não haverá um modelo simplificado exclusivo da UI.

## 4. Fronteiras dos módulos

| Camada | Responsabilidade | Não pode |
|---|---|---|
| Domínio EDP V9 | catálogo oficial, avaliação, estados, decisão e contrato canônico | depender de React, HTTP ou Supabase |
| Serviço de aplicação | carregar entradas, chamar domínio, validar obsolescência, orquestrar persistência e invalidação | selecionar entre fonte genérica e EDP para novo cálculo |
| Persistência | guardar referências, decisão, snapshots e eventos de forma versionada | copiar catálogo oficial como configuração editável ou fazer dual-write |
| CLI | avaliar, consultar, diagnosticar, inventariar, migrar e executar dry run | possuir regras ou estados próprios |
| API | validar payload, autorização e versão; serializar o contrato compartilhado | recalcular regra normativa na rota |
| UI | capturar entradas/decisões e apresentar estados/motivos | inferir compatibilidade ou alterar tensão fixa |
| Consumidores | aceitar a decisão canônica ou bloquear com motivo | fallback genérico oculto |

## 5. Situação dos demais gates

O snapshot abaixo foi atualizado pela incorporação posterior do parecer
GN-01/DP-03. A matriz detalhada e os critérios de fechamento estão em
`docs/architecture/CONSOLIDACAO-GATES-ARQUITETURAIS-EDP-V9.md`.

| Gate | Parecer arquitetural em 2026-07-26 | Estado global |
|---|---|---|
| GN-01 | Parecer técnico incorporado ao contrato e às fixtures de fronteira | `APROVADO` |
| DP-01 | O contrato exige fonte, autoria e confiança da topologia, mas o repositório não contém fonte aprovada | `PENDENTE` — @po/@architect + responsável técnico |
| DP-02 | Entrega faseada: representar/persistir delta desde o modelo e bloquear operação por consumidor até capacidade comprovada | `APROVADO` |
| DP-03 | Parecer técnico incorporado como estado bloqueante `REQUER_ANALISE_DA_CONCESSIONARIA`, sem categoria automática ou definitiva | `APROVADO` |
| DP-04 | Fluxo e perfis de categoria superior não definidos | `PENDENTE` — @po |
| DP-05 | Não há mecanismo de comprovação da área de concessão | `PENDENTE` — @po/@architect |
| DP-06 | Rede subterrânea produz estado acionável de fora de escopo e nunca é avaliada pela norma aérea | `APROVADO` |
| DP-07 | A API aceita autoria declarada pelo cliente e não há matriz de perfis; alterações privilegiadas devem permanecer bloqueadas até política e autorização reais | `PENDENTE` — @po/@architect |
| DP-08 | MMGD conhecida sem entradas suficientes produz pendência bloqueante; suporte completo não integra a release sem requisitos/entradas aprovados | `APROVADO` |
| DP-09 | **Direção arquitetural aprovada:** preservar o catálogo genérico fora da EDP e removê-lo somente da rota EDP após inventário e GO-01B | `PENDENTE` — exige inventário e coaprovação @po |
| DP-10 | Contrato, fronteiras e compatibilidade fixados neste ADR | `APROVADO` |
| GP-01 | Dependências técnicas de GP-01.2 validadas; GP-01.1, coaprovação de GP-01.2, GP-01.3 e GP-01.4 permanecem sem evidência completa | `PENDENTE` |
| RV-01 | Fora da autoridade de @architect e não localizado como aprovado para o PRD 0.8 | `PENDENTE` — @pm/@po |

## 6. GO-01A e GO-01B

### GO-01A — `NÃO APROVADO`

Faltam evidências bloqueantes de:

- CI obrigatório executando lint, typecheck, testes e build;
- ambiente de homologação identificado;
- estratégia de rollout/feature flag para a rota EDP;
- rollback operacional que preserve a invariante sem dual-write;
- observabilidade e limiares para divergência, obsolescência, migração e bloqueios;
- evidência de CLI EDP funcional e paridade com API;
- pareceres de @devops e @qa.

Os artefatos Hostinger existentes não demonstram, por si, prontidão da Release 1.

### GO-01B — `NÃO APROVADO`

Além de GO-01A válido, faltam:

- inventário final sem consumidores EDP no contrato genérico;
- DDL, consistência transacional e evidências de dados aprovados por @data-engineer;
- políticas e testes de retenção, acesso e descarte;
- backup e restauração do significado, não apenas do schema;
- snapshot e rollback semântico idempotente comprovados;
- suporte, escalonamento e resposta a incidentes;
- dry run do pacote 8;
- pareceres de @devops e @qa.

## 7. Dependências e recomendação

### Pode prosseguir

- investigação independente;
- captura de baseline;
- inventário somente leitura;
- elaboração e aprovação dos gates;
- elaboração de fixtures rastreadas ao parecer aprovado de GN-01/DP-03, sem
  converter os pacotes em stories implementáveis.

### Não pode prosseguir

- conversão dos pacotes em stories implementáveis antes de RV-01;
- implementação sem stories formais;
- pacote 6 ou ativação da Release 1 sem GP-01 e GO-01A;
- remoção do legado sem DP-09, inventário e GO-01B;
- qualquer novo cálculo EDP pelo contrato genérico.

**Recomendação arquitetural:** `NO-GO PARA IMPLEMENTAÇÃO E ATIVAÇÃO`.  
`GO` somente para investigação e fechamento dos gates. GN-01, DP-02, DP-03,
DP-06, DP-08 e DP-10 estão encerrados; o bloqueador imediato do workflow SDC é
RV-01, seguido dos gates específicos de cada pacote.

— Aria, arquitetando o futuro
