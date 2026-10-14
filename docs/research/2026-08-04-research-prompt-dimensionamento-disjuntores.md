# Research Prompt — Dimensionamento de Disjuntores

**Criado por:** Atlas (Analyst) — `*research-prompt`
**Data:** 2026-08-04
**Tipo de foco:** Customizado (Tecnologia & Integração)
**Status:** Draft — aguardando revisão do usuário

---

## Research Objective

Definir os requisitos normativos, técnicos e de integração para elevar o dimensionamento de disjuntores — hoje uma heurística provisória embutida no MOD-DC (`sugerirProtecaoCircuito`) — a uma **seção de primeira classe** no sistema SIE (rota própria, motor normativo completo, persistência, UI, tutorial), substituindo/absorvendo a lógica atual sem quebrar o MOD-DC e o MOD-SEC que já a consomem.

## Background Context

- **MOD-DC (Dimensionamento de Condutores)** já é seção completa: rota `projetos.$projetoId_.dimensionamento-condutores.tsx`, domínio em `src/domain/dimensionamento-condutores/`, repo Supabase, overrides por circuito (épico `MOD-DC-HYBRID`, `docs/stories/EPIC-MOD-DC-HYBRID.md`).
- **MOD-QT (Queda de Tensão)** segue o mesmo padrão: rota, `servico-queda-tensao.ts`, catálogo de impedâncias versionado por fabricante (`impedancias-prysmian-rev10.ts`), config Supabase própria (`20260730_001_create_queda_tensao_config.sql`).
- **MOD-SEC (Seccionamento Automático, C4)** é um serviço/endpoint (`POST /api/v1/modulos/mod-sec/validar`, `docs/stories/MOD-SEC-1-refined.md`, Done) que valida tempo de seccionamento, mas **recebe `tempo_atuacao_s` como input externo** — hoje não há fonte real desse dado vinda de um disjuntor selecionado por catálogo.
- Toda seção nova precisa seguir a regra de tutorial obrigatório (par `.md`/`.html` + entrada em manifesto de hashes, enforced por pre-commit hook e CI) e o padrão de camadas `domain → infra/repositorios → infra/supabase → hooks/queries → routes`.
- Estado atual da heurística provisória:

```
src/domain/dimensionamento-condutores/motores/motor-protecao.ts
  sugerirProtecaoCircuito() → escolhe In numa série fixa [6,10,16,20,25,32,40,50,63]A
                             → I2 = 1,45 × In (fórmula genérica, sem catálogo real)
```

  Isso alimenta os campos `in_a`/`i2_a`/`fonte_i2` já expostos pelo `ParametrosDimensionamento` do MOD-DC. Não há: catálogo de disjuntores por fabricante, seleção de curva (B/C/D), verificação de poder de interrupção (Icu/Ics) contra corrente de curto-circuito, rota própria, tabela Supabase própria, nem tutorial. Isso bate com o gap "proteção" apontado como inexistente na auditoria de efetividade de 2026-07-07.

- **Cuidado de nomenclatura:** já existe um módulo chamado "MOD-CC" no projeto, mas com o significado de **Command Center** (`projetos.$projetoId_.command-center.tsx`), não "curto-circuito". Evitar essa colisão de sigla ao nomear a nova seção/módulo.

## Research Questions

### Primary Questions (Must Answer)

1. Quais critérios normativos da NBR 5410 (5.3.4 — proteção contra sobrecargas; 5.3.5 — proteção contra curto-circuito; 5.3.6 — seletividade/discriminação) a seção deve implementar como regras verificáveis (não apenas a série fixa de In hoje usada)?
2. Que dado de corrente de curto-circuito presumida (Icc) no ponto de instalação é necessário para validar poder de interrupção (Icu/Ics), e onde/como ele deveria ser calculado no sistema — hoje não há esse cálculo em nenhum módulo existente?
3. Qual fonte de catálogo de disjuntores (fabricante/norma — WEG, Siemens, ABB, Schneider, ou tabela normativa genérica) adotar para curvas de disparo (B/C/D) e poder de interrupção, seguindo o mesmo padrão de catálogo versionado usado em `impedancias-prysmian-rev10.ts`?
4. A nova seção **substitui** `sugerirProtecaoCircuito()` (`motor-protecao.ts`) ou esse heurístico vira apenas uma sugestão inicial, com override manual auditável — replicando o padrão `CircuitoOverride` já usado no MOD-DC-HYBRID?
5. Como validar seletividade/discriminação entre o disjuntor do circuito terminal e o disjuntor geral (padrão de entrada, `padrao-entrada.tsx`)?
6. A nova seção se torna a fonte real de `tempo_atuacao_s` que o MOD-SEC hoje recebe como input externo — e se sim, qual o contrato de integração entre as duas?
7. Que forma de persistência Supabase é necessária — nova tabela dedicada (padrão `dependencia_*`) ou extensão das tabelas de configuração já existentes por circuito?

### Secondary Questions (Nice to Have)

- Nome definitivo do módulo/rota (evitando colisão com "MOD-CC" já usado para Command Center).
- Estrutura de nav/command-center: novo item de menu, novo card de KPI no command-center?
- Quais arquivos-fonte entrariam na unidade de documentação do tutorial (manifest) desta seção?
- Como versionar futuras revisões de catálogo de disjuntores sem quebrar cálculos históricos já persistidos (mesmo problema de rastreabilidade que MOD-QT resolveu com `impedancias-prysmian-rev10`)?

## Research Methodology

### Information Sources
- NBR 5410 (seções 5.3.4, 5.3.5, 5.3.6) como fonte normativa primária
- Catálogos técnicos de fabricantes de disjuntores (curvas de disparo, Icu/Ics) — priorizar fabricantes já usados no projeto (Prysmian aparece para cabos; verificar se há preferência declarada para disjuntores)
- Código-fonte já mapeado: `motor-protecao.ts`, `servico-dimensionamento-condutores.ts`, `contratos.ts` (MOD-SEC), stories `EPIC-MOD-DC-HYBRID`

### Analysis Frameworks
- Matriz "existe vs. falta" por critério normativo (sobrecarga / curto-circuito / seletividade)
- Comparação de padrões de integração já usados no sistema (MOD-QT↔MOD-DC, MOD-SEC↔MOD-DC) como modelo para MOD-DISJ↔MOD-DC/MOD-SEC

### Data Requirements
- Priorizar fontes normativas oficiais e catálogos de fabricante atuais (não dados genéricos/estimados)

## Expected Deliverables

### Executive Summary
- Lacunas normativas cobertas hoje só parcialmente (heurística) vs. as que faltam por completo
- Recomendação de arquitetura de integração (substituir vs. compor com `motor-protecao.ts`)

### Detailed Analysis
- Especificação de critérios normativos verificáveis (equivalente ao que MOD-SEC fez para C4)
- Modelo de dados proposto (schema de tabela, contrato de API)
- Plano de integração com MOD-DC e MOD-SEC (pontos de chamada, contratos)

### Supporting Materials
- Matriz de comparação de fabricantes/catálogos de disjuntores
- Diagrama de fluxo de dados entre MOD-DC → nova seção → MOD-SEC

## Success Criteria

O output deve ser suficiente para `@architect *analyze-impact` avaliar complexidade e `@pm *write-spec` escrever a spec formal sem precisar reabrir pesquisa normativa básica.

## Timeline and Priority

Sem prazo formal declarado; sugerido tratar como pré-requisito de spec antes de qualquer story de implementação, dado o gap identificado na auditoria de 2026-07-07.

---

## Handoff

- **next_agent:** `@pm`
- **next_command:** `*write-spec`
- **condition:** Pesquisa concluída (research.json/relatório de pesquisa criado a partir deste prompt)
- **alternative:** `@architect *analyze-impact` — se a pesquisa revelar complexidade maior que a esperada
