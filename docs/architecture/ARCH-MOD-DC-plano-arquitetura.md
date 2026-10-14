# Plano de Arquitetura - MOD-DC v3.0

**Produto:** SIE - Sistema de Instalacoes Eletricas  
**Modulo:** MOD-DC - Dimensionamento de Condutores  
**Origem:** `docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md`  
**Decisao arquitetural:** AD-DC-01  
**Autor:** Aria (@architect) - AIOX  
**Data:** 2026-07-12  
**Status:** Aprovado para desdobramento tecnico por stories, condicionado a `@sm` criar as stories DC-1...DC-10.

---

## 1. Sumario Executivo

O MOD-DC v3.0 deve ser implementado como **modulo TypeScript nativo dentro do TanStack Start existente**, no subapp:

`sistema-de-instala-es-el-tricas-sie-main/`

Esta decisao fecha a AD-DC-01 para as stories DC-1 e DC-7:

- **DC-1:** base normativa versionada no proprio app, com dados normativos persistidos via Supabase/PostgreSQL e repositorios TypeScript.
- **DC-7:** API e rotas server implementadas como rotas TanStack Start em `src/routes/api/v1/...`, usando contratos Zod/TypeScript.

Nao sera criado servico Python/FastAPI separado nesta fase. A stack Python/Pydantic do documento-base fica tratada como referencia de formato contratual, nao como decisao de runtime, porque o brownfield real ja opera com TanStack Start, TypeScript, Zod, Vitest, Supabase e rotas server internas.

---

## 2. AD-DC-01 - Runtime/API do MOD-DC

### 2.1 Decisao

**Escolha:** opcao 1 do PRD - **modulo TypeScript dentro do TanStack Start existente**.

**Forma final:**

- Dominio puro em `src/domain/dimensionamento-condutores/`.
- Contratos formais em TypeScript e Zod.
- Persistencia normativa via `src/infra/...` e Supabase/PostgreSQL.
- API interna via TanStack Start server routes em `src/routes/api/v1/...`.
- UI Carbon integrada as rotas existentes de projeto.
- Testes com Vitest, incluindo unitarios, integracao, regressao normativa e performance.

### 2.2 Justificativa

Esta opcao preserva a arquitetura brownfield e evita duplicar backend, deploy, autenticacao, observabilidade e camada de dados. O repositorio ja possui:

- `src/domain/` com dominio puro e testavel.
- `src/api/schemas/` com validacao Zod.
- `src/routes/api/v1/` com rotas server REST internas.
- `src/infra/contexto.ts` com injecao manual de repositorios `memory | supabase`.
- `src/infra/supabase/` com adaptadores reais de persistencia.
- `tests/` e `src/**/__tests__` com Vitest.

### 2.3 Alternativas rejeitadas

| Alternativa | Decisao | Motivo |
|---|---|---|
| Servico Python/FastAPI separado | Rejeitada para DC-1/DC-7 | Criaria segundo runtime, segundo deploy, duplicacao de contratos e maior custo operacional sem necessidade demonstrada. |
| Modelo hibrido TypeScript + Python | Rejeitado nesta fase | So deve ser reavaliado se houver requisito futuro de motor numerico externo, laudo batch pesado ou integracao regulatoria fora do app. |
| Reescrever modulos existentes | Proibido | PRD marca Cargas, Demanda EDP, IB, Categoria de Entrada, MOD-QT e guardas INC-01/INC-04/INC-07 como intocaveis. |

### 2.4 Condicoes da decisao

1. O motor de calculo do MOD-DC fica independente de React, Supabase e HTTP.
2. A camada visual nunca recalcula resultado; ela renderiza o objeto `rastreio`.
3. Valores normativos nunca ficam hardcoded no motor quando pertencem a base normativa versionada.
4. Lacunas `[VERIFICAR]` bloqueiam o criterio afetado com erro explicito.
5. Comparacoes normativas usam adaptador decimal testado, nao `number` solto em trechos criticos.
6. DC-1 deve entregar persistencia normativa antes de DC-3/DC-4 consumirem tabelas completas.
7. DC-7 deve apenas expor contratos e orquestrar servico; regra normativa continua no dominio.

---

## 3. Tecnologias Utilizadas

### 3.1 Stack principal

| Camada | Tecnologia | Uso no MOD-DC |
|---|---|---|
| Linguagem | TypeScript strict | Dominio, contratos, servicos, rotas e UI. |
| Runtime web | TanStack Start | Server routes e paginas integradas ao app atual. |
| UI | React 19 + IBM Carbon | Jornada, tabela de resultados, detalhe e estados. |
| Validacao de entrada | Zod | Schemas HTTP, payloads de lote, retornos downstream e filtros. |
| Persistencia | Supabase/PostgreSQL | Base normativa versionada, resultados, aprovacoes e auditoria. |
| Testes | Vitest | Unitarios, integracao, regressao normativa, API e performance. |
| Build/qualidade | Vite, TypeScript, ESLint | Gates do projeto. |

### 3.2 Precisao numerica

O PRD exige disciplina equivalente a `Decimal`. Em TypeScript, a arquitetura define:

- criar um wrapper de dominio `DecimalNormativo` em `src/domain/dimensionamento-condutores/precisao/`;
- encapsular a biblioteca escolhida atras desse wrapper;
- usar `DecimalNormativo` em comparacoes normativas de C1/C2/C5/C6, fatores e arredondamentos;
- manter entrada/saida JSON como string ou number conforme contrato, mas converter internamente no limite do dominio;
- adicionar testes proprios da dependencia, conforme NFR8.

Dependencia sugerida para avaliacao em DC-1/DC-2: `decimal.js` ou equivalente. A story deve fixar versao e provar comportamento com testes antes de uso em regra normativa.

---

## 4. Estrutura de Pastas

Estrutura-alvo dentro de `sistema-de-instala-es-el-tricas-sie-main/`:

```text
src/
  api/
    schemas/
      dimensionamento-condutores.ts
      dimensionamento-condutores.test.ts

  domain/
    dimensionamento-condutores/
      contratos.ts
      tipos.ts
      erros.ts
      estados.ts
      rastreio.ts
      precisao/
        decimal-normativo.ts
        decimal-normativo.test.ts
      normativa/
        repositorio-normativo.ts
        consulta-tabelas.ts
        serie-normalizada.ts
        tabela-33-tipos-linha.ts
        tabela-36-39-iz.ts
        tabela-40-temperatura.ts
        tabela-41-resistividade-solo.ts
        tabela-42-45-agrupamento.ts
        tabela-46-condutores-carregados.ts
        tabela-47-secoes-minimas.ts
        tabela-48-neutro.ts
        tabela-58-pe.ts
        tabela-30-k-curto.ts
      validacao/
        validador-entradas.ts
        guardas-inc.ts
        validador-cores.ts
        validador-aluminio.ts
      motores/
        motor-capacidade-corrente.ts
        motor-sobrecarga.ts
        motor-secao-minima.ts
        motor-neutro.ts
        motor-pe-pen.ts
        seletor-secao-final.ts
        verificador-independente.ts
      integracoes/
        contrato-qt.ts
        contrato-cc.ts
        contrato-sec.ts
        contrato-prot.ts
        retorno-downstream.ts
      servico-dimensionamento-condutores.ts
      index.ts

  infra/
    repositorios/
      repositorio-normas-condutores.ts
      repositorio-resultados-dimensionamento.ts
    supabase/
      repo-normas-condutores.supabase.ts
      repo-resultados-dimensionamento.supabase.ts

  routes/
    api/
      v1/
        projetos.$projetoId.dimensionamento-condutores.ts
        projetos.$projetoId.dimensionamento-condutores.lote.ts
        projetos.$projetoId.dimensionamento-condutores.$resultadoId.ts
        projetos.$projetoId.dimensionamento-condutores.retorno-qt.ts
        projetos.$projetoId.dimensionamento-condutores.retorno-cc.ts
        projetos.$projetoId.dimensionamento-condutores.retorno-seccionamento.ts
        tabelas.dimensionamento-condutores.$tabela.ts

  components/
    app/
      dimensionamento-condutores/
        DimensionamentoCondutoresWorkspace.tsx
        DimensionamentoCondutoresTabela.tsx
        DimensionamentoCondutoresDetalhe.tsx
        DimensionamentoCondutoresPendencias.tsx
        DimensionamentoCondutoresResumo.tsx

  routes/
    projetos.$projetoId_.dimensionamento-condutores.tsx
```

Estrutura de testes:

```text
tests/
  api/
    dimensionamento-condutores.test.ts
    dimensionamento-condutores-retornos.test.ts
  domain/
    dimensionamento-condutores/
      base-normativa.test.ts
      validador-entradas.test.ts
      motor-capacidade-corrente.test.ts
      motor-sobrecarga.test.ts
      motor-neutro-pe.test.ts
      maquina-estados.test.ts
      regressao-ca-dc.test.ts
      performance-lote.test.ts
  infra/
    normas-condutores-supabase.test.ts
  ui/
    dimensionamento-condutores.vrt.test.tsx
```

Documentacao e dados:

```text
docs/
  architecture/
    ARCH-MOD-DC-plano-arquitetura.md
  stories/
    DC-1-...
    DC-2-...

sistema-de-instala-es-el-tricas-sie-main/
  docs/
    supabase/
      0008_mod_dc_base_normativa.sql
      0009_mod_dc_resultados.sql
```

---

## 5. Componentes Principais

### 5.1 Contratos

**Arquivos:** `contratos.ts`, `src/api/schemas/dimensionamento-condutores.ts`

Responsabilidades:

- `CircuitoParaDimensionamento`: entrada funcional do motor.
- `ParametrosDimensionamento`: metodo, temperatura, agrupamento, material, isolacao, protecao e contexto.
- `ResultadoDimensionamento`: secoes de fase, neutro, PE/PEN, status, criterio decisivo, pendencias e verificacoes.
- `Rastreio`: fonte exata de cada valor usado, incluindo tabela, linha, coluna, pagina, chunk_id, versao e status.
- Schemas Zod de API para validar HTTP antes de chamar o dominio.

### 5.2 Repositorio Normativo

**Arquivos:** `normativa/repositorio-normativo.ts`, `infra/.../repo-normas-condutores.supabase.ts`

Responsabilidades:

- Consultar tabelas 33, 36-48, 58 e 30 por chave completa.
- Recusar consulta incompleta com `ERRO-CONSULTA-INCOMPLETA`.
- Recusar linha `[VERIFICAR]` quando usada em criterio obrigatorio com `ERRO-TABELA-INCOMPLETA`.
- Retornar valor + metadados de rastreio em toda consulta.
- Servir tanto o motor quanto o endpoint `GET /api/v1/tabelas/...`.

### 5.3 Validador de Entradas

**Arquivos:** `validacao/validador-entradas.ts`, `guardas-inc.ts`

Responsabilidades:

- Bloquear ausencia de tensao (`ERRO-TENSAO-AUSENTE`).
- Bloquear ausencia de isolacao (`ERRO-ISOLACAO-AUSENTE`).
- Bloquear ausencia de metodo/tipo de linha (`ERRO-METODO-AUSENTE`).
- Aplicar guardas INC-01, INC-04 e INC-07 sem alterar os modulos existentes.
- Validar aluminio, cores, tipo de linha e combinacoes incompatíveis.

### 5.4 Motores de Calculo

**Arquivos:** `motores/*`

Responsabilidades:

- `MotorCapacidadeCorrente`: C1, Tabelas 36-46, fatores de temperatura, solo, agrupamento e F=1/sqrt(n).
- `MotorSobrecarga`: C2, `IB <= In <= Iz`, `I2 <= 1,45*Iz`, `PENDENTE-I2` e regime severo.
- `MotorSecaoMinima`: C6, Tabela 47.
- `MotorNeutro`: neutro, Tabela 48 e harmonicas.
- `MotorPePen`: PE/PEN, Tabela 58 e minimos aplicaveis.
- `SeletorSecaoFinal`: maior secao entre criterios calculados, revalidacao e criterio decisivo.
- `VerificadorIndependente`: segunda passagem para detectar divergencia entre criterio calculado e status final.

### 5.5 Servico de Aplicacao

**Arquivo:** `servico-dimensionamento-condutores.ts`

Responsabilidades:

- Orquestrar validacao, consultas normativas, motores, integracoes e persistencia.
- Dimensionar circuito individual.
- Dimensionar lote.
- Revalidar resultado apos retorno de MOD-QT, MOD-CC ou MOD-SEC.
- Nunca recomputar valores de outros modulos intocaveis; consumir apenas contratos.

### 5.6 API/Rotas Server

**Arquivos:** `src/routes/api/v1/...`

Endpoints planejados:

| Metodo | Rota | Responsabilidade |
|---|---|---|
| `POST` | `/api/v1/projetos/:projetoId/dimensionamento-condutores` | Dimensionar circuito individual. |
| `POST` | `/api/v1/projetos/:projetoId/dimensionamento-condutores/lote` | Dimensionar lote de circuitos. |
| `GET` | `/api/v1/projetos/:projetoId/dimensionamento-condutores` | Consultar resumo por estado/criterio. |
| `GET` | `/api/v1/projetos/:projetoId/dimensionamento-condutores/:resultadoId` | Consultar resultado com rastreio completo. |
| `GET` | `/api/v1/tabelas/dimensionamento-condutores/:tabela` | Consultar base normativa com fonte/status por linha. |
| `POST` | `/api/v1/projetos/:projetoId/dimensionamento-condutores/retorno-qt` | Receber retorno MOD-QT e revalidar. |
| `POST` | `/api/v1/projetos/:projetoId/dimensionamento-condutores/retorno-cc` | Receber retorno MOD-CC futuro e revalidar. |
| `POST` | `/api/v1/projetos/:projetoId/dimensionamento-condutores/retorno-seccionamento` | Receber retorno MOD-SEC futuro e revalidar. |

### 5.7 UI Carbon

**Arquivos:** `components/app/dimensionamento-condutores/*` e rota `projetos.$projetoId_.dimensionamento-condutores.tsx`

Responsabilidades:

- Exibir seis criterios C1...C6.
- Destacar criterio decisivo com rotulo textual.
- Exibir pendencias C3/C4/C5 sem permitir status completo.
- Exibir detalhe "Como este resultado foi obtido" a partir de `rastreio`.
- Permitir lote, filtros, comparacao de cenarios e overrides auditados conforme stories DC-8/DC-9.

---

## 6. Como os Arquivos se Conectam

### 6.1 Fluxo DC-1 - Base Normativa

```text
docs/supabase/0008_mod_dc_base_normativa.sql
  -> Supabase/PostgreSQL
  -> src/infra/supabase/repo-normas-condutores.supabase.ts
  -> src/domain/dimensionamento-condutores/normativa/repositorio-normativo.ts
  -> motores C1/C2/C6/neutro/PE
  -> ResultadoDimensionamento.rastreio
```

DC-1 deve criar a base versionada e carregar valores confirmados. Dados com `[VERIFICAR]` entram na base com status proprio e bloqueiam uso em criterio obrigatorio.

### 6.2 Fluxo DC-7 - API

```text
HTTP request
  -> src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores*.ts
  -> src/api/schemas/dimensionamento-condutores.ts
  -> src/api/http.ts (withZod, ok, erro, mapearErro)
  -> src/api/contexto-singleton.ts (getServicos)
  -> servicoDimensionamentoCondutores(ctx)
  -> dominio + repositorios
  -> HTTP response padronizada
```

As rotas nao contem regra normativa. Elas validam entrada, chamam servico e traduzem erro de dominio para resposta HTTP.

### 6.3 Fluxo a partir dos modulos existentes

```text
Cargas/Demanda/Divisao de Circuitos/IB
  -> servicoCorrente.obterPreparoDimensionamento()
  -> ContratoSaidaDimensionamento atual
  -> adaptador CircuitoParaDimensionamento
  -> servicoDimensionamentoCondutores.dimensionarLote()
```

O MOD-DC deve consumir a saida de corrente existente, mas ampliar o contrato com os campos obrigatorios do PRD: metodo, isolacao, temperatura, agrupamento, comprimento, protecao e contexto de instalacao.

### 6.4 Fluxo de retorno downstream

```text
MOD-QT / MOD-CC / MOD-SEC
  -> POST retorno-qt|retorno-cc|retorno-seccionamento
  -> validar schema Zod
  -> carregar resultado anterior
  -> aplicar retorno ao criterio C5/C3/C4
  -> revalidar todos os criterios
  -> persistir nova versao do resultado
  -> auditar evento
```

Retornos que exigirem secao maior devem disparar revalidacao completa, nao apenas patch visual.

### 6.5 Fluxo UI

```text
Rota React do projeto
  -> api.preparoDimensionamento / api.dimensionamentoCondutores
  -> query hooks
  -> components/app/dimensionamento-condutores/*
  -> renderiza ResultadoDimensionamento + rastreio
```

A UI nao consulta tabelas diretamente para recalcular. Quando precisar exibir fonte normativa, usa o rastreio retornado pela API.

---

## 7. Fronteiras e Dependencias

### 7.1 Modulos intocaveis

Nao alterar regra interna dos modulos abaixo durante MOD-DC:

- Cargas.
- Demanda EDP.
- IB/correntes.
- Categoria de Entrada EDP.
- Tabelas 001/002 EDP.
- Mapeamento R/S/T.
- MOD-QT, exceto consumo de contrato.
- Guardas INC-01, INC-04 e INC-07.

### 7.2 Pontos de integracao permitidos

- Ler `ContratoSaidaDimensionamento` gerado por `servicoCorrente`.
- Criar adaptador de entrada do MOD-DC sem mudar o calculo de IB.
- Persistir resultados e rastreio em novas tabelas.
- Criar rotas API novas em `/api/v1`.
- Criar tela nova do modulo em rota propria.

### 7.3 Delegacao para @data-engineer

O desenho logico da arquitetura define que a base normativa deve existir, mas o DDL final, indices, constraints, RLS e estrategia de carga devem ser validados por `@data-engineer` antes de DC-1 ser implementada.

---

## 8. Plano por Stories

| Story | Arquitetura necessaria | Saida esperada |
|---|---|---|
| DC-1 | Tabelas normativas, repositorio normativo, carga versionada, migracoes | Base normativa consultavel com status/fonte/rastreio. |
| DC-2 | `ValidadorEntradas`, catalogo de erros, Zod inicial | Entradas bloqueadas corretamente antes de calculo. |
| DC-3 | Motor C1 e consulta normativa | Capacidade de corrente calculada com fatores rastreados. |
| DC-4 | Motores C2/C6 e seletor final | Secao final parcial com criterio decisivo. |
| DC-5 | Neutro, PE/PEN | Condutores complementares dimensionados ou bloqueados. |
| DC-6 | Maquina de estados e contratos downstream | Pendencias C3/C4/C5 explicitas e revalidacao preparada. |
| DC-7 | Rotas server + schemas + servico de aplicacao | API interna funcional para individual, lote, consultas e retornos. |
| DC-8 | UI Carbon principal | Jornada e tabela com seis criterios. |
| DC-9 | UI lote/cenarios/resumo | Operacao em lote e comparacoes auditadas. |
| DC-10 | Testes finais e hardening | CA-DC-01...25 verdes ou `xfail` documentado para lacuna normativa. |

---

## 9. Gates Arquiteturais

1. **Gate DC-1:** nenhuma story de motor pode consumir tabela normativa incompleta sem status e rastreio.
2. **Gate DC-2:** nenhum calculo roda com tensao, isolacao ou metodo ausentes.
3. **Gate DC-3/DC-4:** nenhuma comparacao normativa critica usa `number` diretamente sem passar por wrapper decimal.
4. **Gate DC-6:** `VERIFICADO-COMPLETO` so existe com C1...C6 aprovados ou nao aplicaveis e sem pendencias.
5. **Gate DC-7:** rotas server nao contem regra normativa; apenas validacao, orquestracao e serializacao.
6. **Gate DC-8/DC-9:** UI renderiza rastreio, nao recomputa.
7. **Gate DC-10:** `npm run lint`, `npm run typecheck`, `npm test` e CA-DC-01...25.

---

## 10. Riscos Tecnicos e Mitigacoes

| Risco | Impacto | Mitigacao |
|---|---|---|
| Precisao decimal em TypeScript mal encapsulada | Resultado normativo incorreto | Wrapper `DecimalNormativo` + testes de fronteira antes dos motores. |
| Base normativa incompleta | Bloqueio de varios circuitos reais | Status `[VERIFICAR]` explicito e erro bloqueante; carga incremental rastreada. |
| Motor virar servico acoplado a Supabase | Baixa testabilidade | Dominio recebe repositorio por interface; testes usam memoria/fixtures. |
| UI recalcular valor para exibir detalhe | Divergencia de rastreio | Detalhe renderiza apenas payload `rastreio`. |
| Retorno MOD-QT alterar secao sem revalidar C1/C2/C6 | Resultado inconsistente | `retorno-downstream.ts` sempre chama revalidacao completa. |
| Criar backend Python paralelo por conveniencia | Custo operacional e duplicacao | Decisao AD-DC-01 bloqueia Python nesta fase. |

---

## 11. Decisao Final

AD-DC-01 fica encerrada como:

```text
DECIDIDO: implementar MOD-DC v3.0 como modulo TypeScript nativo
no TanStack Start existente, com dominio puro, contratos Zod/TypeScript,
persistencia Supabase/PostgreSQL, API em rotas server TanStack e UI React
Carbon. Nao criar servico Python/FastAPI em DC-1/DC-7.
```

Com isso, DC-1 e DC-7 estao desbloqueadas do ponto de vista arquitetural, desde que respeitem os gates deste plano e sejam desdobradas em stories antes de qualquer implementacao.

