# Brainstorming Session: Alternativas para implementação de novos módulos no sistema

**Data:** 2026-07-07
**Facilitador:** Atlas (@analyst)
**Objetivo da sessão:** Ideação ampla (divergente)
**Escopo:** Dimensionamento elétrico e proteção
**Perspectivas simuladas:** Arquitetura, Implementação, Dados, QA, Produto

## Contexto

- Dimensionamento de condutores, proteção por circuito e laudo **não existem** no SIE — bloqueio explícito via `ERR-DIMENSIONAMENTO-PENDENTE` em `servico-corrente.ts`; `derivar-circuitos.ts` é autodeclarado "mapeador provisório".
- Auditoria de efetividade/eficácia (2026-07-07): notas 6,5/7,0 no escopo implementado; roadmap acordado P0 (divisão de circuitos definitiva + certificação NBR) → P1 (dimensionamento de condutores) → P1.5 (proteção) → P2 (laudo + hardening Supabase).
- Stack real: TypeScript full-stack (TanStack Start + React 19 + Supabase + Carbon).
- Regras NBR F-03…F-09 e tabelas T-* com `status_verificacao: "VERIFICAR"`; catálogo EDP é a parte mais madura (`VERIFICADO`).
- 1 teste falhando: `carga_automatica_va` contaminada por override manual (`tomadas.ts:136`) — defeito de rastreabilidade na base da cadeia.

Relatório de auditoria: `docs/audits/2026-07-07-auditoria-efetividade-eficacia-roadmap/AUDITORIA-EFETIVIDADE-EFICACIA-ROADMAP.md`

## Ideias Geradas

**Total:** 21

### 🏗️ Arquitetura

1. **Motor de dimensionamento como pipeline puro em `src/domain/`** — funções puras TS, entrada = circuito derivado, saída = condutor + proteção + justificativa normativa. Zero dependência de UI/DB, testável isoladamente.
2. **Módulo "resolvedor de tabelas NBR" genérico** — camada única que resolve Tabelas 36/37/38/39/40 (capacidade de condução, agrupamento, temperatura) como dados versionados `.data.json`, no padrão do catálogo EDP.
3. **Arquitetura de "cadeia com elos plugáveis"** — formalizar carga → demanda → circuitos → dimensionamento → proteção → laudo como pipeline com contratos explícitos entre elos; cada elo vira story independente.
4. **Feature flags por elo** — substituir `ERR-DIMENSIONAMENTO-PENDENTE` por mecanismo de capacidade declarada, permitindo lançamento incremental sem quebrar o fluxo.

### 💻 Implementação

5. **Começar por queda de tensão + capacidade de corrente** — dos 4 critérios NBR de dimensionamento de condutor, implementar primeiro os 2 determinísticos.
6. **Divisão de circuitos definitiva (P0) como módulo separado do provisório** — reescrever `derivar-circuitos.ts` com regras NBR 4.2.5.5, mantendo o antigo como fallback até paridade.
7. **Coordenação de proteção como validador, não gerador** — validar escolhas (IB ≤ In ≤ IZ) antes de gerar automaticamente. Reduz risco normativo.
8. **Corrigir o defeito de rastreabilidade antes de construir em cima** — o teste falhando (`tomadas.ts:136`) está na base da cadeia que o dimensionamento consumirá.

### 🗄️ Dados

9. **Tabelas NBR como dados verificáveis com `status_verificacao`** — replicar o processo de certificação do catálogo EDP, com fonte normativa citada por linha.
10. **Persistir o "memorial de cálculo" desde o dia 1** — cada decisão grava entrada, tabela usada, linha e resultado. Torna o laudo (P2) quase gratuito.
11. **Hardening Supabase junto com o módulo novo** — módulo nasce já no padrão correto (migrations versionadas, CHECK constraints, transação no agregado).

### 🧪 QA

12. **Suíte de casos dourados de dimensionamento** — 20-30 casos resolvidos manualmente como testes de aceitação antes de implementar; módulo só é "PASS" quando bate todos.
13. **Validação cruzada com software de referência** — comparar resultados com ferramentas estabelecidas como teste de regressão normativa.
14. **Certificar as regras F-03…F-09 pendentes** — resolver os `status_verificacao: "VERIFICAR"` antes que o dimensionamento dependa delas.

### 📊 Produto

15. **"Modo assistido" como MVP** — sistema sugere dimensionamento com justificativa, engenheiro confirma/ajusta. Menor risco de responsabilidade técnica.
16. **Módulo de proteção contra choque (DR) como diferencial rápido** — regras de obrigatoriedade de DR são determinísticas e simples; alto valor percebido, baixo custo.
17. **Priorizar o que desbloqueia o laudo** — ordenar os módulos pela dependência do laudo (entregável que o cliente paga), não pela ordem "natural" da cadeia elétrica.

### 🔀 Combinações e Wild Cards

18. **(5+10) Dimensionamento com memorial embutido** — cada função retorna `{ resultado, memorial }`; junta critério técnico e rastreabilidade num único contrato.
19. **(12+13) Banco público de casos de teste NBR5410** — publicar casos dourados como dataset open-source; ativo de marketing técnico e validação comunitária.
20. **🃏 "Explicador normativo"** — cada resultado clicável abre a citação exata da NBR5410 (seção, tabela, linha). Transforma o SIE em ferramenta de defesa técnica perante fiscalização.
21. **🃏 Simulação de cenários** — "e se eu trocar cobre por alumínio / embutido por bandeja?" — o motor puro (ideia 1) torna isso quase gratuito.

## Categorização

| Categoria | Ideias | Tema |
|---|---|---|
| **Fundação primeiro** | 6, 8, 9, 11, 14 | Corrigir base antes de construir (P0) |
| **Motor de dimensionamento** | 1, 2, 5, 18 | Núcleo técnico dos condutores (P1) |
| **Proteção** | 7, 16 | Validação e DR (P1.5) |
| **Rastreabilidade → Laudo** | 10, 17, 20 | Caminho para o entregável final (P2) |
| **Arquitetura evolutiva** | 3, 4 | Como os módulos convivem |
| **Qualidade normativa** | 12, 13, 19 | Confiança nos resultados |
| **UX/Diferencial** | 15, 21 | Valor percebido |

## Top 5 Recomendações Priorizadas

| # | Ideia | Valor | Esforço | ROI | Racional |
|---|---|---|---|---|---|
| 1 | **Cadeia com elos plugáveis + contratos (3)** | 9 | 4 | 2,25 | Destrava a implementação incremental de todo o roadmap P0-P2; decisão de arquitetura, não código |
| 2 | **Casos dourados antes do código (12)** | 9 | 3 | 3,00 | Define "correto" antes de implementar; converte risco normativo em suíte de testes |
| 3 | **Memorial embutido no contrato (18)** | 8 | 3 | 2,67 | Custo marginal agora, laudo quase gratuito no P2 |
| 4 | **Divisão de circuitos definitiva (6)** | 8 | 6 | 1,33 | É o P0 acordado; pré-requisito real de tudo |
| 5 | **Modo assistido como MVP (15)** | 7 | 4 | 1,75 | Reduz responsabilidade técnica e antecipa entrega de valor |

### Próximos passos por recomendação

1. **Cadeia plugável:** handoff para @architect — desenhar contratos entre elos (tipos TS de entrada/saída de cada estágio) antes de qualquer implementação.
2. **Casos dourados:** levantar 20-30 casos resolvidos por engenheiro (planilhas reais), formalizar como fixtures de teste de aceitação.
3. **Memorial embutido:** incluir `{ resultado, memorial }` no contrato desenhado em (1) — decisão de design, custo marginal.
4. **Divisão de circuitos:** criar epic/stories com @pm a partir do roadmap P0.
5. **Modo assistido:** validar com usuários-alvo (engenheiros) se sugestão+confirmação atende antes de investir em geração totalmente automática.

## Key Insights

- As alternativas **não competem entre si** — a decisão real é *arquitetural* (ideias 3+18 definem o contrato) e *sequencial* (fundação P0 antes do motor P1).
- O maior risco do projeto não é técnico, é **normativo**: por isso os casos dourados (12) devem preceder qualquer linha do motor de dimensionamento.
- O memorial de cálculo (10/18) é a ponte barata entre P1 e P2 — decidir agora, colher no laudo.
- O padrão de certificação do catálogo EDP (única área `VERIFICADO`) é o modelo a replicar para as tabelas NBR.

## Metadados da Sessão

- **Ideias geradas:** 21
- **Categorias identificadas:** 7
- **Perspectivas:** 5 (Arquitetura, Implementação, Dados, QA, Produto)
- **Duração:** ~30 min
- **Insumos:** Auditoria de efetividade 2026-07-07, auditoria NBR5410/EDP 2026-06-21

---

**Handoffs sugeridos:**
- @architect → design dos contratos da cadeia plugável (recomendação 1)
- @pm → conversão das top 5 em epic/stories (recomendações 2-5)
