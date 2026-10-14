# Consolidação dos Gates Arquiteturais — PRD EDP V9

**Documento avaliado:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Parecer incorporado:** `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md`  
**Data do snapshot inicial:** 2026-07-26  
**Último adendo:** 2026-07-27 — coaprovação de DP-01 e DP-05  
**Autoridade:** Aria (@architect)  
**Resultado arquitetural:** `NO-GO PARA IMPLEMENTAÇÃO GLOBAL`  

## 1. Objetivo e limite de autoridade

Este documento incorpora ao desenho do PRD as decisões técnicas de `GN-01` e
`DP-03` e consolida o estado dos gates que possuem decisão, validação ou
dependência arquitetural.

A consolidação:

- encerra `GN-01` e `DP-03` porque o parecer contém decisão final,
  fundamentação normativa e regras testáveis;
- reconhece as decisões já aprovadas de `DP-02`, `DP-06`, `DP-08` e `DP-10`;
- registra separadamente contribuições arquiteturais concluídas e estados
  globais ainda pendentes;
- não substitui coaprovação de @po, validação de @pm, parecer de @qa, evidência
  operacional de @devops nem evidência física de dados de @data-engineer;
- não altera `RV-01` para aprovado e não autoriza criação de stories ou
  implementação.

## 2. Decisões GN-01 e DP-03 incorporadas

### 2.1 GN-01 — `APROVADO`

O contrato arquitetural passa a considerar como regra ratificada:

| Topologia | Carga instalada | Equipamento trifásico | Resultado |
|---|---:|---|---|
| estrela ou delta | exatamente 12 kW | não | `U` |
| estrela | exatamente 25 kW | não | `D` |
| delta | exatamente 25 kW | não | `D` |
| delta | exatamente 25 kW | sim | `T` |
| estrela ou delta | exatamente 12 kW | sim | `REQUER_ANALISE_DA_CONCESSIONARIA` |
| estrela | exatamente 25 kW | sim | `REQUER_ANALISE_DA_CONCESSIONARIA` |

A comparação deve usar carga instalada total em watts inteiros. Tensão,
quantidade de fases ou natureza do equipamento não podem ser alteradas para
forçar enquadramento.

### 2.2 DP-03 — `APROVADO`

`REQUER_ANALISE_DA_CONCESSIONARIA` é incorporado como estado bloqueante do
domínio, e não como categoria de fornecimento.

O contrato canônico deve manter, no mínimo, as seguintes distinções:

- categoria mínima calculada;
- categoria superior pretendida ou solicitada;
- categoria definitiva, nula enquanto não houver manifestação documentada da
  EDP;
- motivo do bloqueio;
- dados faltantes e próxima ação;
- referência posterior a protocolo, documento, condicionantes e decisão da
  concessionária.

Invariantes:

1. T somente é atribuída automaticamente quando todas as condições textuais,
   de fases e de tensão forem satisfeitas.
2. Caso sem enquadramento direto não recebe fallback U, D, T ou genérico.
3. A Nota-03 registra uma solicitação; não confirma categoria superior.
4. Consumidores downstream permanecem bloqueados enquanto a categoria
   definitiva for nula.
5. O resultado preliminar não libera relatório, memorial ou projeto como
   aprovado pela EDP.

## 3. Snapshot consolidado dos gates

| Gate | Estado global | Contribuição arquitetural | Evidência ou bloqueio remanescente |
|---|---|---|---|
| GN-01 | `APROVADO` | Regra normativa incorporada ao domínio e aos testes de fronteira | Parecer técnico §§7, 10–13 |
| DP-01 | `PENDENTE` | Contrato exige fonte, autoria, confiança e confirmação da topologia | Faltam fonte e jornada aprovadas por @po/@architect e responsável técnico |
| DP-02 | `APROVADO` | Delta 240/120 V representável desde o modelo; ativação faseada por consumidor | Decisão PO e ADR; capacidade operacional continua condicionada a testes |
| DP-03 | `APROVADO` | Estado bloqueante e fluxo de manifestação da EDP incorporados | Parecer técnico §§8–13 |
| DP-04 | `PENDENTE` | Contrato separa intenção, solicitação e confirmação | Jornada e autoridades dependem de decisão @po |
| DP-05 | `PENDENTE` | Avaliação deve falhar de modo seguro quando a área não estiver comprovada | Falta mecanismo e evidência de comprovação coaprovados por @po/@architect |
| DP-06 | `APROVADO` | Rede subterrânea retorna fora de escopo acionável e não usa regra aérea | Decisão PO e ADR |
| DP-07 | `PENDENTE` | Default-deny para ações privilegiadas; fonte oficial e override permanecem separados | Faltam matriz de perfis, política de autorização e coaprovação @po/@architect |
| DP-08 | `APROVADO` | MMGD sem entradas suficientes retorna pendência bloqueante | Decisão PO e ADR |
| DP-09 | `PENDENTE` | **Direção arquitetural aprovada:** preservar catálogo genérico fora da EDP e removê-lo apenas da rota EDP | Faltam inventário real, GO-01B aprovado e coaprovação @po |
| DP-10 | `APROVADO` | Contrato canônico e fachada de compatibilidade definidos | ADR DP-10 |
| GP-01.1 | `PENDENTE` | Sem contribuição conclusiva de arquitetura | Persona, papéis e jornada dependem de @ux/@po |
| GP-01.2 | `PENDENTE` | **Dependências técnicas validadas:** fundação, Release 1 e Release 2 respeitam contrato, gates e remoção controlada | Falta aprovação da fronteira e das capacidades condicionadas por @po |
| GP-01.3 | `PENDENTE` | Requer segregação e default-deny coerentes com DP-04/DP-07 | Falta matriz de perfis coaprovada |
| GP-01.4 | `PENDENTE` | Sem contribuição conclusiva de arquitetura | Faltam baseline e metas aprovados por @ux/@po |
| GP-01 | `PENDENTE` | Validação parcial: somente dependências técnicas de GP-01.2 | Todos os quatro itens precisam de aprovação |
| GO-01A | `REPROVADO` | Arquitetura confirma ausência de baseline ativável, rollout reversível e observabilidade comprovada | Exige evidências e aprovações de @devops/@architect/@qa |
| GO-01B | `NÃO APROVADO` | Arquitetura aceita somente evolução aditiva; remoção permanece proibida | GO-01A inválido, dados parciais, inventário, restauração, rollback e dry run ausentes |
| RV-01 | `PENDENTE` | Fora da autoridade arquitetural | Reexecução @pm/@po deve incorporar o novo parecer e este snapshot |

## 4. Gates arquiteturais ainda pendentes

### 4.1 DP-01 — fonte da topologia

Critério de fechamento:

- fonte da topologia identificada;
- proveniência, autoria e confiança registradas;
- regra de confirmação definida;
- comportamento para divergência ou ausência aprovado;
- validação conjunta de @po/@architect e responsável técnico.

Até o fechamento, topologia ausente ou não confiável produz pendência
bloqueante; o sistema não pode inferir estrela ou delta.

### 4.2 DP-05 — área de concessão

Critério de fechamento:

- mecanismo de comprovação identificado;
- evidência persistida e auditável;
- tratamento de indisponibilidade ou conflito definido;
- coaprovação @po/@architect.

Até o fechamento, área não comprovada impede aplicar automaticamente a regra
EDP V9.

### 4.3 DP-07 e GP-01.3 — governança e perfis

Critério de fechamento:

- papéis reais e vínculo usuário–projeto definidos;
- matriz de solicitar, confirmar, publicar, sobrescrever, migrar e reverter;
- trilha de auditoria e política de break-glass;
- alinhamento com DP-04;
- coaprovação @po/@architect.

Até o fechamento, ações privilegiadas permanecem em default-deny. Policies
universais ou autoria informada apenas pelo cliente não são evidência válida.

### 4.4 DP-09 — destino do catálogo genérico

A decisão arquitetural está fixada: o catálogo genérico é preservado fora do
contexto EDP e removido somente da rota EDP. O estado global continua
`PENDENTE` até:

- inventário real demonstrar os consumidores e contextos existentes;
- dependências EDP serem migradas para o contrato canônico;
- contextos externos terem não regressão comprovada;
- GO-01B estar aprovado;
- @po coaprovar o destino com base no inventário.

### 4.5 GP-01.2 — fronteira de release

A arquitetura valida a sequência e as dependências técnicas já descritas no
PRD:

```text
fundação interna (pacotes 1–4)
        -> Release 1 / convergência EDP (pacotes 1–7)
        -> Release 2 / remoção controlada (pacote 8)
```

A validação não aprova `GP-01.2`: @po ainda deve aprovar a fronteira e declarar
as capacidades condicionadas. Delta operacional continua faseado por
consumidor; fundação interna não pode ser ativada isoladamente; remoção do
legado pertence somente à Release 2.

### 4.6 GO-01A e GO-01B

O parecer arquitetural acompanha os estados `REPROVADO` e `NÃO APROVADO`.
Fechamento exige evidência operacional e de qualidade, não apenas desenho:

- candidato identificável com gates verdes e CodeRabbit sem `CRITICAL`;
- homologação equivalente à produção;
- rollout reversível, kill switch e rollback ensaiados;
- observabilidade e resposta a incidente ativas;
- para GO-01B, GO-01A válido, inventário final, migrations testadas,
  backup/restauração do significado, rollback semântico e dry run.

## 5. Impacto nos pacotes

| Escopo | Efeito desta consolidação |
|---|---|
| Regras GN-01/DP-03 | Especificação normativa liberada para futuro desdobramento em story |
| Pacote 2 — avaliador | Mantém dependência de DP-01 e DP-05; já pode usar as regras ratificadas de fronteira e exceção |
| Pacote 4 — API/persistência/CLI | Mantém dependência de DP-04/DP-07 e da autorização formal de stories |
| Pacote 6 — UI | Bloqueado por GP-01 |
| Release 1 | Bloqueada por RV-01, GP-01 e GO-01A |
| Pacote 8 / Release 2 | Bloqueado por DP-09 e GO-01B |

## 6. Parecer de arquitetura do snapshot inicial

```yaml
architecture_gate_consolidation_snapshot_2026_07_26:
  GN-01: APROVADO
  DP-03: APROVADO
  architectural_direction_DP-09: APROVADA
  architectural_validation_GP-01.2: APROVADA
  remaining_architectural_gates:
    - DP-01
    - DP-05
    - DP-07
    - DP-09
    - GP-01.3
    - GO-01A
    - GO-01B
  rv_01_reexecution_required: true
  story_creation_authorized: false
  implementation_authorized: false
  release_1_activation_authorized: false
  legacy_removal_authorized: false
```

O parecer técnico elimina os bloqueios normativos de `GN-01` e `DP-03`, mas
não elimina os bloqueios de produto, acesso, operação, dados e revalidação.
O próximo snapshot de `RV-01` deve usar esta consolidação e não repetir
`GN-01` ou `DP-03` como pendentes.

O estado desta seção é histórico. Para DP-01 e DP-05, prevalece o adendo da
seção 7.

## 7. Adendo arquitetural — DP-01 e DP-05 em 2026-07-27

### 7.1 Evidências avaliadas

| Gate | Artefato | SHA-256 antes da coaprovação |
|---|---|---|
| DP-01 | `docs/prd/DP-01-EVIDENCIA-FONTE-TOPOLOGIA-EDP-V9.md` | `3A24CCD1B6F22F45DCC81F4F28F3F2DF7ADC7662C4F93B0F90C4D5A27F8922AC` |
| DP-05 | `docs/prd/DP-05-EVIDENCIA-AREA-CONCESSAO-EDP-V9.md` | `2032989615F945B6BFCBAFB6645ACEDECDBB569616239F9D259B0AF3E2A4DACD` |

Foram usadas somente as fontes e evidências já registradas nesses artefatos.
Não houve promoção de evidência de implementação, teste, operação ou
manifestação da EDP para um projeto concreto.

### 7.2 DP-01 — `APROVADO`

Arquitetura coaprova a consulta do usuário à EDP para o ponto de conexão como
fonte da topologia. A decisão satisfaz o critério do gate porque:

1. a fonte e o responsável pela captura estão definidos;
2. protocolo ou documento, canal, data, autoria e referência verificável
   preservam a proveniência;
3. município e endereço não podem inferir estrela ou delta;
4. ausência, divergência e obsolescência possuem estados bloqueantes;
5. somente manifestação válida da EDP e confirmação do responsável técnico
   produzem `TOPOLOGIA_CONFIRMADA`;
6. todos os consumidores dependentes devem falhar de modo seguro nos demais
   estados.

A confirmação do responsável técnico é um controle por projeto, não uma
coaprovação documental pendente do desenho. Consequentemente, o gate de
decisão DP-01 está encerrado, mas nenhuma unidade concreta recebe topologia
confirmada sem cumprir a jornada.

### 7.3 DP-05 — `APROVADO`

Arquitetura coaprova o catálogo versionado de área de concessão. A evidência
registrada reconcilia 28 municípios distintos entre a fonte regulatória da
ANEEL e a conferência operacional da EDP e define:

- identificador, versão, data e hash da fonte;
- município canônico e UF;
- preservação da versão usada na decisão histórica;
- rejeição de correspondência aproximada;
- estados bloqueantes para localização ausente/ambígua e fonte inválida;
- independência entre comprovação da área e topologia da rede.

A implementação física e os testes do catálogo serão evidência de uma story
futura. Eles não são condição para a coaprovação do desenho e continuam sem
autorização por este documento.

### 7.4 Snapshot vigente após as coaprovações

| Gate | Estado vigente | Efeito |
|---|---|---|
| DP-01 | `APROVADO` | Pacote 1 deixa de estar bloqueado por falta de decisão sobre a fonte; cada projeto continua fail-closed até resposta EDP e confirmação técnica |
| DP-05 | `APROVADO` | Pacotes dependentes podem especificar o catálogo oficial fail-closed; uso efetivo exige implementação e testes futuros |

```yaml
architecture_gate_consolidation_2026_07_27:
  DP-01:
    status_final: APROVADO
    po_contribution: APROVADA
    architect_coapproval: APROVADA
    per_project_technical_confirmation: REQUIRED_FAIL_CLOSED
  DP-05:
    status_final: APROVADO
    po_contribution: APROVADA
    architect_coapproval: APROVADA
    official_catalog: SPECIFIED_NOT_IMPLEMENTED
  remaining_architectural_gates:
    - DP-07
    - DP-09
    - GP-01.3
    - GO-01A
    - GO-01B
  package_1_blocked_by_DP_01: false
  package_2_blocked_by_DP_05: false
  rv_01_reexecution_required: true
  story_creation_authorized: false
  implementation_authorized: false
  release_1_activation_authorized: false
  legacy_removal_authorized: false
```

DP-01 e DP-05 deixam de integrar a lista de gates arquiteturais pendentes. O
resultado global permanece `NO-GO PARA IMPLEMENTAÇÃO GLOBAL`: RV-01, QA
preflight e os demais gates aplicáveis mantêm suas autoridades e bloqueios.

— Aria, arquitetando o futuro
