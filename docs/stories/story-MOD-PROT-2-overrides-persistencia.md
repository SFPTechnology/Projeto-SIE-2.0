---
executor: "@data-engineer"
quality_gate: "@dev"
quality_gate_tools: [contract_validation, integration_test, security_scan]
---

# Story MOD-PROT-2: Overrides por Circuito e Persistência

## Status

**Done**

## Story

**As a** engenheiro eletricista,
**I want** customizar os parâmetros de proteção (In, curva, fonte do catálogo) por circuito individualmente, com justificativa obrigatória e trilha auditável,
**so that** eu possa tratar exceções normativas sem perder rastreabilidade, do mesmo jeito que já faço no MOD-DC.

## Acceptance Criteria

1. Override por circuito segue o padrão `useGlobal` / `customParams` / `justificativa obrigatória`, análogo a `CircuitoOverride` do MOD-DC-HYBRID.
2. Override sem justificativa é rejeitado com erro explícito (mesmo padrão de `OverrideCircuitoInvalido`).
3. Resultado por circuito registra `baseadoEm: "GLOBAL" | "CUSTOMIZADO"` e `parametrosUsados` (mesmo shape de retorno de `resolverParametrosCircuito` do MOD-DC).
4. Overrides são persistidos em tabela Supabase própria, com política RLS `anon_all_<tabela>` para o modo SPA.
5. Migration própria criada em `supabase/migrations/`, seguindo o padrão de `20260730_001_create_queda_tensao_config.sql`.
6. Nenhuma tabela existente (`dependencia_*`, `parametros_edp_overrides`, `queda_tensao_config`) tem schema alterado.

## 🤖 CodeRabbit Integration

**Story Type Analysis**
**Primary Type**: Database (schema novo, migration, RLS)
**Secondary Type(s)**: Architecture (reaplica o padrão de override já validado no MOD-DC-HYBRID)
**Complexity**: Medium — schema novo isolado, mas replica um padrão já testado em produção

**Specialized Agent Assignment**
**Primary Agents**:
- @data-engineer (schema, migration, RLS)
- @dev (repositório TypeScript, integração com `Repository<T>`)

**Supporting Agents**:
- @architect (validação de que o padrão `CircuitoOverride` foi replicado fielmente, não reinterpretado)

**Quality Gate Tasks**
- [ ] Pre-Commit (@dev): `coderabbit --prompt-only -t uncommitted`
- [ ] Pre-PR (@github-devops): `coderabbit --prompt-only --base main`

**Self-Healing Configuration**
**Expected Self-Healing**:
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL

**Predicted Behavior**:
- CRITICAL issues: auto_fix (até 2 iterações)
- HIGH issues: document_only

**CodeRabbit Focus Areas**
**Primary Focus**:
- RLS: política `anon_all_<tabela>` presente e testada (modo SPA depende disso)
- Schema compliance: FKs, índices, constraints coerentes com `queda_tensao_config`

**Secondary Focus**:
- Validação de override (justificativa obrigatória, customParams não vazio) espelhando `OverrideCircuitoInvalido`

## Tasks / Subtasks

- [x] Definir migration `docs/supabase/0014_dimensionamento_disjuntores_overrides.sql` (AC: 4, 5, 6)
  - [x] **Correção de grounding aplicada durante a implementação:** a pasta real de migrations do submódulo é `docs/supabase/NNNN_*.sql` (numeração sequencial), não `supabase/migrations/` como o Dev Notes original sugeria — `supabase/migrations/20260730_001_create_queda_tensao_config.sql` citado no PRD/ADR está no repositório PAI, fora do submódulo. Migration criada no local correto, próximo número sequencial (`0014`, seguinte ao `0013_secoes_otimizadas.sql`).
  - [x] **Correção de schema aplicada:** em vez de uma linha por override (`id`, `circuito_id` como coluna), segui o padrão REAL já em produção de `dimensionamento_condutores_overrides` (`docs/supabase/0010_dimensionamento_condutores_overrides.sql`): uma linha por **projeto**, coluna `overrides` (jsonb) com o mapa `circuitoId → DisjuntorOverride` serializado inteiro. Reutiliza um padrão já comprovado em produção em vez de inventar um schema por-linha (IDS: REUSE > ADAPT > CREATE).
  - [x] Índice por `projeto_id`; `projeto_id` é PK com FK para `projetos(id) ON DELETE CASCADE`
  - [x] Políticas RLS `dimensionamento_disjuntores_overrides_all_anon` / `..._all_authenticated` (mesmo padrão de `0012_queda_tensao_config.sql`, que é mais completo que o `0010` original)
- [x] Criar `src/domain/dimensionamento-disjuntores/overrides.ts` (AC: 1, 2, 3)
  - [x] Interface `DisjuntorOverride` (`useGlobal`, `customParams`, `justificativa`) — espelha `CircuitoOverride`; `customParams` restrito a `Partial<Pick<ResultadoProtecaoCircuito, "in_a"|"norma_dispositivo"|"capacidade_interrupcao">>` (não o objeto genérico de `ParametrosDimensionamento`, já que o domínio de MOD-PROT customiza o *resultado*, não um objeto de parâmetros de entrada rico como o MOD-DC tem)
  - [x] Função `resolverParametrosProtecaoCircuito({ circuito, tipoInstalacao, override })` retornando `{ baseadoEm, resultado, justificativaOverride? }`
  - [x] Classe de erro `OverrideProtecaoInvalido` (mesmo padrão de `OverrideCircuitoInvalido`)
- [x] Criar repositório (AC: 4)
  - [x] `src/infra/repositorios/repositorio-dimensionamento-disjuntores-overrides.ts` (nome alinhado à convenção real do projeto — `repositorio-dimensionamento-condutores-overrides.ts` — em vez do nome curto sugerido originalmente)
  - [x] `src/infra/supabase/repo-dimensionamento-disjuntores-overrides.supabase.ts`
  - [x] Registrado em `src/infra/contexto.ts` (`ContextoApp.repoDisjOverrides`)
- [x] Testes (AC: 1–6)
  - [x] `src/domain/dimensionamento-disjuntores/overrides.test.ts`: GLOBAL, CUSTOMIZADO válido, CUSTOMIZADO sem justificativa (erro), CUSTOMIZADO sem customParams (erro)
  - [x] Teste de repositório dedicado (`src/infra/supabase/__tests__/...`) **não foi criado** — não há instância Supabase disponível neste ambiente para testar contra ela; a lógica de persistência é exercitada indiretamente via `tests/api/dimensionamento-disjuntores-flow.test.ts` usando `novoContextoApp(..., "memory")`, mesmo padrão de isolamento usado em todo o resto da suíte do projeto
  - [x] Nenhuma tabela existente teve schema alterado — confirmado por revisão do diff da migration (apenas `CREATE TABLE IF NOT EXISTS` nova)

## Dev Notes

### Padrão de referência — copiar, não reinterpretar

O padrão de override já existe e está em produção no MOD-DC-HYBRID: `src/domain/dimensionamento-condutores/overrides.ts` (`CircuitoOverride`, `resolverParametrosCircuito`, `OverrideCircuitoInvalido`, `dimensionarLoteComOverrides`). Esta story replica exatamente essa estrutura para o domínio de proteção — **não é uma reinterpretação livre**, é uma cópia adaptada. [Source: PRD-MOD-PROT-dimensionamento-disjuntores.md#fr5]

Trecho de referência (`dimensionamento-condutores/overrides.ts`, já implementado):
```ts
export class OverrideCircuitoInvalido extends Error {
  constructor(
    public readonly circuitoId: string,
    message: string,
    public readonly detalhes: ReadonlyArray<string> = [],
  ) { super(message); this.name = "OverrideCircuitoInvalido"; }
}

function hasCustomParams(customParams): customParams is NonNullable<...> {
  return customParams != null && Object.keys(customParams).length > 0;
}
```
Use exatamente essa validação (justificativa `.trim()` obrigatória, `customParams` não vazio) para `DisjuntorOverride`/`OverrideProtecaoInvalido`.

### Persistência — padrão a seguir

`queda_tensao_config` (`supabase/migrations/20260730_001_create_queda_tensao_config.sql`) é a migration de referência mais recente e mais próxima em escopo (config por projeto/circuito do MOD-QT). Siga a mesma estrutura de política RLS (`anon_all_<tabela>` para `anon`, necessário porque o modo SPA usa a anon key e fica sujeito a RLS — ver CLAUDE.md do submódulo, seção "RLS no modo SPA"). [Source: sistema-de-instala-es-el-tricas-sie-main/CLAUDE.md#rls-no-modo-spa]

O **nome de tabela e o DDL concreto (colunas, índices) são autoridade de @data-engineer** — o ADR (`mod-prot-contrato-integracao.md` §3) apenas sugere `dimensionamento_disjuntores_overrides` como ponto de partida, não vinculante. Não travar a story nesse nome se @data-engineer preferir outro.

### Repositório

Interface `Repository<T>` já existe em `src/infra/repositorios/repositorio.ts`, com `InMemoryRepository` usada nos testes de todos os módulos (evita mocks de infraestrutura — ver CLAUDE.md do submódulo: "A `InMemoryRepository`... é usada nos testes para substituir os repos Supabase sem mocks."). Siga o mesmo par de arquivos (`infra/repositorios/*.ts` + `infra/supabase/*.supabase.ts`) já usado por `repositorio-resultado-dimensionamento-condutores.ts` / `repo-resultado-dimensionamento-condutores.supabase.ts`.

### Previous Story Insights

Story MOD-PROT-1 ainda não foi implementada no momento da criação desta story (sequência de draft, não de execução) — nenhum Dev Agent Record disponível ainda. Ao iniciar esta story, revisar a seção "Dev Agent Record" da Story MOD-PROT-1 para confirmar o shape final de `ResultadoProtecaoCircuito`, já que `DisjuntorOverride.customParams` deve aceitar um subconjunto desses campos (In, curva/`norma_dispositivo`, fonte de catálogo).

### Testing

- Framework: Vitest.
- Localização: `src/domain/dimensionamento-disjuntores/overrides.test.ts` (domínio) e `src/infra/supabase/__tests__/repo-disjuntores-overrides.test.ts` (infra).
- Teste de integração de repositório deve usar `InMemoryRepository` como baseline e, se possível, rodar contra Supabase local/staging seguindo o padrão já usado nos testes de infra existentes do projeto.

### Project Structure Notes

Arquivos novos ficam em `src/domain/dimensionamento-disjuntores/` (domínio, já criado na Story MOD-PROT-1), `src/infra/repositorios/` e `src/infra/supabase/` (mesmas pastas usadas por todos os outros módulos — não criar pastas novas de infra).

## Change Log

| Date | Version | Description | Author |
|------|---------|--------------|--------|
| 2026-08-05 | 1.0 | Story criada a partir do PRD-MOD-PROT e do ADR `mod-prot-contrato-integracao.md` | River (@sm) |
| 2026-08-05 | 1.1 | Validated GO (9/10) — Status: Draft → Ready. Nota: nome de tabela permanece não-vinculante, @data-engineer confirma no início da implementação | Pax (@po) |
| 2026-08-05 | 1.2 | Implementado e testado — Status: Ready → Ready for Review. Schema real corrigido para o padrão comprovado (uma linha/projeto, jsonb), local de migration corrigido para `docs/supabase/` | Dex (@dev) |
| 2026-08-08 | 1.3 | QA Gate CONCERNS (REQ-001: AC5 cita caminho inexistente; REL-001: migration 0014 nao aplicada) | Quinn (@qa) |
| 2026-08-08 | 1.4 | Status: Ready for Review -> InReview (normalizacao de ciclo de vida) | Dex (@dev) |

## Dev Agent Record

### Agent Model Used

Claude Sonnet 5 (claude-sonnet-5), modo YOLO (autônomo)

### Debug Log References

Nenhum impasse relevante. Verificação de grounding antes de escrever a migration revelou que a pasta `supabase/migrations/` citada no Dev Notes não existe no submódulo — a real é `docs/supabase/`; corrigido antes de criar o arquivo (ver Completion Notes).

### Completion Notes List

- **Desvio deliberado do Dev Notes original, documentado:** a migration foi criada em `docs/supabase/0014_dimensionamento_disjuntores_overrides.sql` (não `supabase/migrations/`), e o schema segue o padrão real de produção de `dimensionamento_condutores_overrides` (uma linha por projeto com `overrides jsonb`), não o schema por-linha-por-circuito que o Dev Notes original havia esboçado como sugestão inicial. Ambas as correções são fiéis ao princípio "REUSE > ADAPT > CREATE" — reaproveitam um padrão já em produção em vez de inventar um novo.
- `DisjuntorOverride.customParams` é tipado como subconjunto de `ResultadoProtecaoCircuito` (`in_a`, `norma_dispositivo`, `capacidade_interrupcao`), não como um objeto de parâmetros rico — porque o override de MOD-PROT customiza o *resultado* da seleção de disjuntor, não uma lista extensa de parâmetros normativos como o MOD-DC tem.
- Teste de infraestrutura Supabase dedicado não foi criado (sem instância disponível neste ambiente); cobertura de persistência vem da suíte de API (`tests/api/dimensionamento-disjuntores-flow.test.ts`) rodando contra o contexto in-memory — mesmo padrão usado em toda a suíte do projeto.
- Migration não foi aplicada contra um banco real (sem acesso a instância Supabase neste ambiente) — SQL revisado manualmente contra o padrão de `0012_queda_tensao_config.sql`, mas a aplicação real fica pendente para quando o ambiente de deploy estiver disponível.

### File List

**Criados:**
- `src/domain/dimensionamento-disjuntores/overrides.ts`
- `src/domain/dimensionamento-disjuntores/overrides.test.ts`
- `src/domain/dimensionamento-disjuntores/index.ts`
- `src/infra/repositorios/repositorio-dimensionamento-disjuntores-overrides.ts`
- `src/infra/supabase/repo-dimensionamento-disjuntores-overrides.supabase.ts`
- `docs/supabase/0014_dimensionamento_disjuntores_overrides.sql`

**Modificados:**
- `src/infra/contexto.ts` (registro de `repoDisjOverrides`)

## QA Results

### Review Date: 2026-08-08

### Reviewed By: Quinn (Test Architect)

**Traceability:** 5/6 ACs plenamente atendidas; AC5 parcial.

- AC1/AC2/AC3 verificadas em `overrides.ts` (`useGlobal`/`customParams`, `OverrideProtecaoInvalido` em justificativa vazia, `baseadoEm: "GLOBAL"|"CUSTOMIZADO"`), com testes dedicados.
- AC4 verificada: `0014` cria `dimensionamento_disjuntores_overrides_all_anon FOR ALL TO anon`.
- AC6 verificada: o único `ALTER TABLE` do `0014` é `ENABLE ROW LEVEL SECURITY` sobre a tabela **nova**. Nenhuma tabela existente alterada.

**Ressalvas:**
- **REQ-001 (low)** — AC5 exige `supabase/migrations/` e cita `20260730_001_create_queda_tensao_config.sql`. **Nenhum dos dois existe** no repositório. A implementação seguiu a convenção real e vigente (`docs/supabase/00NN_*.sql`). O defeito está no texto da AC, não no código — correção cabe ao @po.
- **REL-001 (medium)** — ponto de atenção do @dev **confirmado**: a aplicação da migration `0014` contra o Supabase permanece não verificada. Sem a tabela, a persistência de overrides falha em runtime. Confirmar antes do release.

### Gate Status

Gate: CONCERNS → docs/qa/gates/MOD-PROT-2-overrides-persistencia.yml

### Re-Review Date: 2026-08-08

Sem mudanca de codigo nesta remediacao. REQ-001 (texto da AC5) e REL-001 (migration 0014 nao aplicada) permanecem abertos como ressalvas nao bloqueantes. Nota: as Tasks da propria story ja documentam a correcao de caminho (`docs/supabase/` e o local real), o que confirma REQ-001 como defasagem do texto da AC, nao defeito.

### Gate Status (mantido)

Gate: CONCERNS -> docs/qa/gates/MOD-PROT-2-overrides-persistencia.yml
