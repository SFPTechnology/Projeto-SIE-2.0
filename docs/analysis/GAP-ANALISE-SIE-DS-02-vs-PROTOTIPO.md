# Gap Analysis (atualizada) — `/sie-command-center-preview` vs. Protótipo do SIE Command Center

**Autor:** Atlas (`@analyst`)
**Data:** 2026-07-31
**Análise anterior:** `docs/analysis/GAP-ANALISE-SIE-DS-LOCAL-01-vs-PROTOTIPO.md` (feita antes de `SIE-DS-02`)

## Resumo executivo

Desde a última análise, `SIE-DS-02` foi implementada (nav lateral, cabeçalho global, paleta de comandos). **Os dois maiores gaps identificados antes (Gap 1 e Gap 4) estão substancialmente resolvidos.** O que resta é, na sua maior parte, **conteúdo real de página** — não estrutura de shell — e continua fora do escopo desta avaliação até uma decisão explícita de investir em `SIE-DS-03`+.

## O que mudou desde a última análise

| Item | Antes (`SIE-DS-LOCAL-01`) | Agora (`SIE-DS-02`) |
|---|---|---|
| Navegação | Lista horizontal simples, sem agrupamento | ✅ Nav lateral 256px, 4 grupos/9 itens, item ativo, colapso para drawer < 992px |
| Cabeçalho | Título estático + selo | ✅ Seletor de projeto, sync-state, busca, densidade, autor |
| Paleta de comandos | Ausente | ✅ `Ctrl/Cmd+K`, filtro, navegação por seta, `Esc` |
| Densidade | Ausente | ✅ `comfortable`/`compact` alternável, tokens portados |
| Estilos inline | Presentes (corrigido em correção pontual anterior) | ✅ 100% classes CSS em todos os 3 organisms |

## O que ainda falta (gaps reais, mapeados ao backlog)

### 1. Cabeçalho contextual — `SIE-DS-03`

O protótipo tem um segundo cabeçalho, **dentro do `<main>`**: breadcrumb (`Projetos / Residência Sabiá / Visão geral`), título + descrição do módulo, badge de status ("Em dimensionamento"), ações primárias (Inspetor, Validar projeto). A implementação atual não tem isso — o `<main>` vai direto para o conteúdo ilustrativo de `SIE-DS-LOCAL-01`. Isso é explicitamente OUT scope de `SIE-DS-02` (documentado na própria story) e IN scope de `SIE-DS-03`.

### 2. Conteúdo real do Overview — `SIE-DS-03`

O protótipo tem: grid de métricas (4 `metric-card`s com progresso/tendência), painel de jornada técnica (`WorkflowStepper` com 4 etapas), painel de engenharia com tabela+diagrama lado a lado e um `segmented-control` para alternar entre eles. A implementação atual mantém a tabela simples de 3 projetos ilustrativos de `SIE-DS-LOCAL-01`, sem nenhum desses elementos.

### 3. Inspector panel — `SIE-DS-04`+

O protótipo tem um painel lateral direito com propriedades do item selecionado, rastreabilidade e ações contextuais. Totalmente ausente — depende de haver algo selecionável primeiro (List+Inspector é `SIE-DS-04`).

### 4. Detalhes menores do protótipo não replicados (pequenos, não bloqueiam nada)

- Botão "Ajuda e atalhos" no rodapé da nav lateral (o protótipo tem; a implementação atual só tem o rótulo "Conceito v1 · isolado").
- Atalho `?` para abrir a paleta (só `Ctrl/Cmd+K` foi implementado).
- Overlay de fundo + fechamento por `Esc`/clique-fora no drawer de navegação mobile (já registrado como Should-Fix no QA Gate de `SIE-DS-02`, `ARCH-001`).
- Sistema de toast para feedback de ações demonstrativas.

Nenhum desses 4 itens estava em nenhuma AC de `SIE-DS-02` — não são bugs, são detalhes do protótipo que ninguém pediu para replicar ainda.

## Resposta direta

**A estrutura do shell (nav, cabeçalho, paleta) já está alinhada com o protótipo.** A diferença visual que resta ao abrir as duas páginas lado a lado é, essencialmente: **o protótipo mostra uma página cheia de conteúdo (Overview completo); a implementação real ainda mostra o placeholder ilustrativo mínimo de `SIE-DS-LOCAL-01` dentro desse shell agora completo.**

Para fechar essa diferença, o próximo passo real é `SIE-DS-03` (cabeçalho contextual + conteúdo real de Overview) — não uma correção, uma implementação nova.

---

— Atlas, investigando a verdade 🔎
