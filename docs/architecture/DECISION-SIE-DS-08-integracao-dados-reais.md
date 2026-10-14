# DECISION SIE-DS-08 — Integração do SIE Command Center a dados/funcionalidades reais

**Insumo:** `docs/analysis/GAP-ANALISE-SIE-COMMAND-CENTER-INTEGRACAO-REAL.md` (Atlas, `@analyst`, 2026-08-01)
**Ratificado por:** Aria (`@architect`) — 2026-08-01
**Decisões de produto confirmadas pelo usuário:** rota vira `/projetos/$projetoId/command-center`; os 4 pontos sem equivalente real são **adaptados** ao vocabulário real, não removidos nem deixados ilustrativos.
**Restrição de partida (inegociável):** zero alteração de design visual — mesmos organisms, mesmas classes CSS, mesma estrutura de `EngineeringShell`. Toda mudança abaixo é de **fonte de dados**, não de **layout**.

> Este documento não implementa nada (Artigo II — Agent Authority: implementação é `@dev`). É o mapeamento técnico definitivo que a(s) story(ies) seguintes devem seguir.

---

## 1. Contexto de projeto (decisão estrutural)

**Decisão:** a rota migra de `src/routes/sie-command-center-preview.tsx` para `src/routes/projetos.$projetoId_.command-center.tsx`, seguindo exatamente a convenção de nomenclatura já usada por `projetos.$projetoId_.queda-tensao.tsx`, `projetos.$projetoId_.circuitos.tsx`, etc.

- `$projetoId` chega via `Route.useParams()` (mesmo padrão de todas as outras rotas de projeto).
- O botão `sie-cc-project-switcher` em `EngineeringShell.tsx:65-78` — hoje decorativo, com `aria-label="Trocar projeto (ilustrativo)"` e nome hardcoded `"Residência Sabiá"` — passa a exibir `projetoQuery(projetoId)` (já existe em `src/hooks/queries.ts:11-16`) e navega para `/projetos/{outroId}/command-center` ao trocar. Isso é troca de dado/handler, não de marcação — a estrutura visual do botão não muda.
- A feature flag `VITE_FEATURE_SIE_COMMAND_CENTER` continua controlando acesso à rota inteira (mesmo mecanismo de `SIE-DS-00`, AC3), agora aplicada à rota com parâmetro.
- **A rota antiga `/sie-command-center-preview` é removida** nesta migração (não mantida em paralelo) — evita dois lugares de verdade para o mesmo shell.

## 2. Mapeamento de wiring por bloco

Nenhuma linha desta tabela cria backend novo — todos os hooks/endpoints já existem. Trabalho de `@dev` é: import do hook real no lugar do `*-data.ts` ilustrativo, e adaptação do `props` de cada organism ao shape real (mudança de tipo, não de estrutura visual).

| Bloco / organism | Fonte mock (a remover) | Fonte real (a usar) |
|---|---|---|
| `MetricCardGrid` (métricas) | `overview-data.ts` → `metricas` | `quedaTensaoResumoQuery(projetoId)` (`hooks/queries.ts:84-88`) para conformidade/pior queda; `parametrosEDPQuery(projetoId)` (linha 90-94) para demanda (`ResultadoDemanda.DT_VA`) |
| `WorkflowStepper` (jornada) | `overview-data.ts` → `etapasJornada` | **Sem fonte real 1:1** — ver §3, item "fluxo %". As 4 etapas em si (Levantamento/Entrada/Dimensionamento/Documentação) podem continuar como rótulos fixos de navegação; o que muda é o cálculo de qual etapa está `ativo`/`completo` (ver §3) |
| `EngineeringPanel` (tabela circuitos) + `ContextInspector` | `overview-data.ts` → `circuitosIlustrativos` | `divisaoCircuitosQuery(projetoId)` (`hooks/queries.ts:42-46`) para lista; `quedaTensaoLoteQuery(projetoId)` (linha 76-81) para `delta_v_percentual`/status por circuito |
| `ParameterPanel` (parâmetros queda de tensão) | `parameters-results-data.ts` → `parametrosQuedaTensao` | Campos de `RequisicaoQuedaTensao`/`ContextoQuedaTensao` (`src/domain/queda-tensao/contratos.ts`) já retornados dentro de `quedaTensaoLoteQuery`/`quedaTensaoResumoQuery` — `@dev` confirma se é necessário um novo `queryOptions` por item de lote ou se o lote já basta |
| `ResultSummary` | `parameters-results-data.ts` → `resultadosQuedaTensao` | `ResultadoInternoQuedaTensao` (mesmo lote acima) — já tem `alertas`/`sugestoes`, mapeáveis 1:1 para os campos opcionais `motivo`/`proximaAcao` que `ResultSummary` já espera |
| `DecisionPanel` | `decision-data.ts` → `contextoDecisao`/`opcoesDecisao` | `simularCenarios()` (`src/domain/queda-tensao/motores/simulador-cenarios.ts`) para as opções; API real `projetos.$projetoId.circuitos.$circuitoId.simular-queda.ts` e `...aplicar-cenario.ts` (já existem em `api/v1/`) para simular/confirmar. **Novidade em relação ao mock:** `aplicarCenario()` exige `justificativa` não vazia — `DecisionPanel` precisa ganhar um campo de justificativa que o mock não tinha (única mudança de estrutura de UI justificada por comportamento real mais rigoroso, não por preferência estética) |
| `ModuleNavigation` | `module-navigation-data.ts` (estático) | Continua estático nos rótulos/ícones, mas os `href` de cada item passam a apontar para as rotas reais já mapeadas em `GAP-ANALISE-SIE-COMMAND-CENTER-INTEGRACAO-REAL.md §5` (ex.: item "Circuitos" → `/projetos/$projetoId/circuitos`) — **exceto** "Diagnóstico", ver §3 |
| `UnifilarPreviewSection` | — | Já real desde `SIE-DS-06`. Zero trabalho. Só precisa receber `projetoId` real em vez do fixture hardcoded, se o fixture ainda estiver fixo — `@dev` confirma no código atual |

## 3. Resolução dos 4 pontos sem equivalente real (adaptar, por decisão do usuário)

| Ponto | Resolução determinada |
|---|---|
| "Fluxo concluído: 72%" | **Remover o percentual.** Não inventar um cálculo de progresso que não existe no domínio (violaria Artigo IV mesmo depois de "adaptado"). `WorkflowStepper` mantém as 4 etapas como navegação fixa; o estado `ativo`/`completo` de cada etapa passa a ser inferido de sinais reais já existentes (ex.: etapa "Dimensionamento" = `ativo` se `quedaTensaoResumoQuery` retornar `PENDENTE`/`ACIMA` em algum circuito, `completo` se todos `OK`) — regra exata de inferência fica para `@dev` propor e `@po` validar na story, não fechada aqui |
| "Método de instalação B1" | **Substituir pelo vocabulário real:** exibir `familia_id`/`topologia_coluna_id` (ou a descrição textual associada no catálogo `impedancias-prysmian-rev10.ts`) em vez do texto fixo "B1 · eletroduto embutido" |
| Estado binário conforme/revisar | **Expor o 3º estado.** `EngineeringPanel`/badges passam a ter 3 variantes (`OK`→`success`, `ACIMA`→`danger`, `PENDENTE`→`neutral`/`warning`, a definir o mapeamento exato de cor na story) em vez de só 2. Isso é mudança de dado exibido, a paleta de badges (`success/info/warning/danger/neutral`) já suporta 5 estados — nenhum token novo necessário |
| "Diagnóstico" no menu | **Renomear ou remover o item até existir rota real equivalente.** Não apontar para `diagnostico.tsx` (health-check de Supabase) fingindo que é diagnóstico de conformidade do projeto — isso seria pior que deixar mockado, seria ativamente enganoso. Decisão final de texto (remover vs. renomear para algo como "Status da conexão") cabe a `@po` na validação da story |

## 4. Fora de escopo desta decisão

- Criar a rota real de "diagnóstico de conformidade NBR 5410" — não existe hoje, e inventá-la está fora do que este documento cobre (seria uma feature nova, não uma integração).
- Qualquer alteração em `src/domain/**` — toda a integração consome serviços/hooks já existentes; nenhuma lógica de domínio nova é necessária.
- Gate de CodeRabbit (`§15.4`) — segue indisponível, condição já conhecida desde `SIE-DS-07`; a story que implementar esta decisão herda a mesma limitação e deve declará-la, não escondê-la.

## 5. Próximo passo

Story-Driven Development (Artigo III) exige que isto vire story(ies) antes de qualquer código. Sugestão de particionamento (não vinculante — `@sm` decide o corte real no `*draft`):

- **SIE-DS-08:** migração de rota (`$projetoId`) + wiring de `MetricCardGrid`/`EngineeringPanel`/`ContextInspector` (circuitos, métricas, demanda).
- **SIE-DS-09:** wiring de `ParameterPanel`/`ResultSummary`/`DecisionPanel` (queda de tensão, incl. campo de justificativa) + os 4 ajustes semânticos do §3 + `ModuleNavigation` real.

Handoff para `@sm` (`*draft`) usando este documento como fonte de arquitetura ratificada.

---

— Aria, arquitetando o futuro 🏗️
