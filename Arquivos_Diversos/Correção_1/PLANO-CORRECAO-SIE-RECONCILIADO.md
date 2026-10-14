# Plano de Correção do Sistema SIE — Reconciliado com o Código-Fonte

> **Autor:** Atlas (Analyst / AIOX) — análise de discovery brownfield
> **Data:** 2026-06-20
> **Sistema analisado:** `sistema-de-instala-es-el-tricas-sie-main`
> **Documentos-base de correção:** `Correção_1/plano_correcao_obrigatoria_modulos.md` e `Correção_1/Plano_Correcao_Obrigatoria_NBR5410_EDP.md`
> **Natureza deste documento:** descritivo e prescritivo. **Nenhuma alteração de código foi feita.** Este plano apenas reconcilia os planos de correção recebidos com o que realmente existe no repositório e detalha as ações.

---

## 0. Sumário executivo

Os dois planos em `Correção_1` foram escritos a partir da **observação do comportamento em execução** ("gravações"), não da leitura do código atual. Ao cruzar item a item com o repositório, encontrei três situações distintas:

| Situação | O que significa | Quantidade aproximada |
|---|---|---|
| ✅ **Já implementado** | A correção pedida já existe no código (premissa do plano desatualizada) | ~30% dos itens |
| 🟡 **Parcial / refatoração** | A estrutura existe, mas como *opcional*, *provisória* ou *advisory*; falta torná-la *obrigatória / definitiva / bloqueante* | ~35% dos itens |
| 🔴 **Greenfield real** | Não existe no código; precisa ser construído | ~35% dos itens |

**Conclusão central:** o sistema está **mais maduro** do que os planos presumem na *primeira metade* (classificação de carga, demanda, balanceamento, diagnósticos) e **confirmadamente incompleto** na *segunda metade* (divisão real de circuitos NBR, dimensionamento de condutores, queda de tensão, proteção por circuito, DR/DPS/aterramento, artefatos finais).

**O defeito de segurança mais importante não é a classificação — é a ausência de _fail-closed_:** o sistema calcula e avança mesmo com pendências críticas (carga sem `tipoAparelho`, tabela 001/002 vazia), porque os diagnósticos são **advisory**, não **bloqueantes**. Essa é a correção de maior alavancagem e menor esforço.

---

## 1. Metodologia e evidências

### 1.1 Stack real (lida de `package.json`, `tsconfig.json`, `vite.config.ts`)

- **Frontend/SSR:** TanStack Start + TanStack Router + React 19 + React Query.
- **Linguagem:** TypeScript 5.8 (ESM, `"type": "module"`).
- **UI:** Carbon Design System + Radix UI + Tailwind 4.
- **Validação:** Zod 3.
- **Persistência:** Supabase (`@supabase/supabase-js`), migrations em `docs/supabase/`.
- **Testes:** Vitest 4 (há 11 suítes só no módulo EDP-SP).
- **Build/runtime:** Vite 8 + Nitro.

### 1.2 Arquitetura real (camadas)

```
src/domain/        ← núcleo (puro, testável)
  calculo/         ← motores de cálculo (iluminação, tomadas, corrente, balanceamento, derivar-circuitos...)
  distribuidora/edp-sp/  ← regras EDP-SP + tabelas .data.json + 11 suítes de teste
  nbr/             ← catálogo NBR (tipos, fatores de demanda, fornecimento)
  modelo/          ← entidades (Projeto, Dependencia, Circuito, PadraoEntrada)
  estado/          ← máquina de estados (estados, eventos, transicoes)
  servicos/        ← casos de uso (cálculo, validação, edição, recálculo, auditoria...)
src/infra/         ← repositórios Supabase + contexto
src/routes/api/v1/ ← endpoints HTTP
src/components/    ← UI (Carbon)
```

A arquitetura **já segue** a separação por camadas que o `plano_correcao_obrigatoria_modulos.md` pede (regras versionáveis em `.data.json`, cálculo isolado de UI). Isso reduz o esforço de várias fases.

### 1.3 Arquivos-chave inspecionados (evidência direta)

`tipos-aparelho.ts`, `grupos-demanda.ts`, `cargas-adicionais.ts`, `modelo/dependencia.ts`, `modelo/circuito.ts`, `calculo/derivar-circuitos.ts`, `calculo/balanceamento-fases.ts`, `distribuidora/edp-sp/seletor-subcategoria.ts`, `distribuidora/edp-sp/validacao.ts`, `distribuidora/edp-sp/adaptador-projeto.ts`, `estado/transicoes.ts`, `servicos/servico-validacao.ts`, `subcategorias-fornecimento.data.json`.

---

## 2. Reconciliação crítica — premissas dos planos vs. código real

> Esta é a seção de maior valor. Cada linha corrige uma premissa dos documentos originais com evidência do repositório.

| Item do plano original | Premissa do plano | **Estado real no código** | Veredito |
|---|---|---|---|
| **NBR §0.2 / Módulos §17** — "corrigir roteamento motor→g, forno→d, ar→f" | Mapeamento errado | `tipos-aparelho.ts` (l.54–78): motor→**g**, forno_eletrico→**d**, ar_condicionado→**f**, hidromassagem→**i** — **já corretos** | ✅ Já feito |
| **NBR §0.3** — "forno_eletrico FP 1,0; iluminacao_descarga FP 0,55" | FP errados | `tipos-aparelho.ts`: `iluminacao_descarga` FP **0,55** (✅), mas `forno_eletrico` FP **0,8** (≠ 1,0 do plano) | 🟡 Divergência a confirmar com fonte EDP |
| **NBR §0.1 / Módulos V01** — "`tipo_aparelho` obrigatório + bloqueio" | Campo pode ficar vazio; erro só advisory | `dependencia.ts` (l.41): `tipoAparelho?` é **opcional**; `adaptador-projeto.ts` (l.66, 77–83) roteia ao grupo "a" e só **empurra pendência** `TIPO_APARELHO_AUSENTE`; cálculo prossegue | 🟡 Refatorar (opcional→obrigatório + bloqueio) |
| **NBR §0.4 / Módulos 4.3** — "capturar tensão de placa por carga" | Tensão não capturada (assume 220 V) | `dependencia.ts` (l.37): `tensaoFixa?` **já existe** (opcional); `derivar-circuitos.ts` (l.81) usa `ca.tensaoFixa ?? default` | 🟡 Refatorar (existe, mas opcional/com default) |
| **NBR §1.2 / Módulos 7.3** — "corrigir Tabela 001/002; nunca 150 A com 25 mm²" | Sistema gera par disjuntor/condutor inválido | `subcategorias-fornecimento.data.json`: `"subcategorias": []`, `status_verificacao: "VERIFICAR"`; `seletor-subcategoria.ts` (l.50, 59–61) retorna `verificar/tabelas_001_002_ausentes` e **"nunca inventa disjuntor"** | 🟡 **Não é bug de lógica — é dado ausente.** O par 150 A+25 mm² era de runtime antigo. Falta **popular dados** + tornar VERIFICAR bloqueante |
| **NBR §4.1 / Módulos 9** — "substituir 'tudo na Fase A' provisório" | Balanceamento não existe / tudo na fase A | `balanceamento-fases.ts` (l.35–64): **LPT real** (Longest Processing Time) distribui A/B/C pela fase menos carregada, trata mono/bi/tri | ✅ Já implementado (algoritmo correto) |
| **Módulos V04/V05 / 7.2** — "trifásico não usa U/D; mono não usa T" | Combinações cruzadas aceitas | `validacao.ts` (l.194–219) já emite `ATN-TRIFASICA-FORCOU-CATEGORIA-T`; `seletor-categoria.ts` decide por sistema | 🟡 Diagnóstico existe; falta **bloqueio duro** das combinações cruzadas |
| **NBR Fase 2 / Módulos 8** — "criar entidade Circuito + divisão NBR 9.5.3" | Não existe entidade Circuito | `modelo/circuito.ts` **existe** (entidade rica), mas `derivar-circuitos.ts` (l.13–20) é **mapeador provisório** (1 circuito por carga; não separa ILUM de TUG; não cria exclusivos >10 A; não marca DR) | 🟡 Entidade existe / 🔴 Divisão real é greenfield |
| **NBR Fase 3 / Módulos 10–11** — "condutores, queda de tensão, proteção por circuito" | Não existe | `modelo/circuito.ts` (l.25–38): **sem** campos de método, comprimento, temperatura, agrupamento, condutor fase/neutro/PE, disjuntor, queda | 🔴 Greenfield confirmado |
| **NBR Fase 4 / Módulos 13** — "DR, DPS, aterramento, equipotencialização" | Não existe | Nenhum campo `requer_DR`, `DPS`, `PE`, esquema de aterramento em `circuito.ts`/`projeto.ts` | 🔴 Greenfield confirmado |
| **NBR Fase 5 / Módulos 14** — "memorial, quadro de cargas, unifilar" | Não existe | Há `servico-auditoria.ts` + `ValorRastreavel.tsx` (rastreabilidade parcial), mas **sem** quadro de cargas por circuito nem unifilar | 🟡 Base de rastreio existe / 🔴 artefatos finais greenfield |
| **Módulos 3 / V15** — "fail-closed: alteração invalida cálculos dependentes" | Botão concluir sempre liberado | `transicoes.ts`: estado `EXIGE_VALIDACAO_TECNICA` após recálculo já existe; `servico-validacao.ts` exige ART quando há pendências | 🟡 Máquina de estado existe; falta **gate de CALCULAR** com pendência crítica |

---

## 3. Matriz de prontidão por módulo

| # | Módulo (ordem de engenharia) | Prontidão | Esforço dominante |
|---:|---|---|---|
| 1 | Base normativa / tabelas versionadas | 🟢 Alta (estrutura `.data.json` + `parametros.ts`) | Popular dados faltantes |
| 2 | Modelo de dados técnico | 🟡 Média (faltam campos de circuito físico) | Refatorar `circuito.ts`/`projeto.ts` |
| 3 | Validação impeditiva (fail-closed) | 🔴 Baixa (diagnósticos são advisory) | Gates na máquina de estados/serviços |
| 4 | Previsão de cargas (ilum/TUG/TUE) | 🟢 Alta (`iluminacao.ts`, `tomadas.ts`, `cargas-adicionais.ts`) | Ajustes pontuais + obrigatoriedade |
| 5 | Enquadramento EDP (demanda/categoria) | 🟢 Alta (`motor-demanda.ts`, seletores, validacao) | Popular Tabela 001/002 + bloqueio |
| 6 | Divisão final de circuitos (NBR 9.5.3) | 🔴 Baixa (só mapeador provisório) | **Greenfield** |
| 7 | IB + balanceamento | 🟢 Alta (`corrente-circuitos.ts`, `balanceamento-fases.ts`) | Reusar após Fase 6 |
| 8 | Dimensionamento de condutores | 🔴 Inexistente | **Greenfield** + tabelas ampacidade |
| 9 | Queda de tensão | 🔴 Inexistente | **Greenfield** |
| 10 | Proteção sobrecorrente/curto | 🔴 Inexistente | **Greenfield** |
| 11 | DR / DPS / aterramento / equipot. | 🔴 Inexistente | **Greenfield** |
| 12 | Artefatos finais (quadro/unifilar/memorial) | 🟡 Parcial (rastreio existe) | Greenfield de saída |
| 13 | Rastreabilidade de fórmulas | 🟡 Parcial (`ValorRastreavel`, `servico-auditoria`) | Estender cobertura |
| 14 | Auditoria/testes/homologação | 🟡 Parcial (11 suítes EDP) | Ampliar p/ casos CT01–CT12 |

---

## 4. Plano de correção faseado (detalhado)

> Regime **phase-gated**: uma fase só inicia quando a anterior fecha o gate. Ordenação por **fluxo de dados** (não por severidade), conforme `Plano_Correcao_Obrigatoria_NBR5410_EDP.md`. Cada passo indica: **tipo** (✅/🟡/🔴), **arquivos-alvo**, **ação**, **critério de aceite**.

### FASE 0 — Saneamento da entrada e da classificação *(fundação)*

**Passo 0.1 — `tipoAparelho` obrigatório + bloqueio de cálculo** 🟡 `[CRÍTICO]`
- **Arquivos:** `modelo/dependencia.ts` (tornar `tipoAparelho` não-opcional na carga adicional ou exigir no schema de entrada), `api/schemas/dependencia.ts` (Zod: campo obrigatório), `adaptador-projeto.ts` (l.77–83: deixar de rotear ao grupo "a"; promover a pendência a **erro bloqueante**), gate em `servico-calculo.ts` / `estado/transicoes.ts`.
- **Ação:** impedir transição `PENDENTE→CALCULAR` (ou produzir estado `ERRO`) enquanto houver carga sem `tipoAparelho`. Converter `ERR-CARGA-SEM-TIPO-APARELHO` de *advisory* para *blocker*.
- **Aceite:** salvar/calcular carga sem tipo é impossível; o ar-condicionado de 3.516 VA passa a ter tipo e some o erro.

**Passo 0.2 — Revisão do mapa tipo→grupo** ✅ `[verificação]`
- **Estado:** já correto em `tipos-aparelho.ts`. **Ação reduzida:** apenas validar a tabela completa (a–i) item a item com a fonte EDP v06 e congelar com teste de regressão (`__tests__/classificacao.test.ts`).
- **Aceite:** teste cobrindo os 23 tipos → grupo esperado, verde.

**Passo 0.3 — Fatores de potência por tipo** 🟡 `[MÉDIO]`
- **Arquivos:** `tipos-aparelho.ts`, `fatores-potencia.data.json`, `__tests__/fatores-potencia.test.ts`.
- **Ação:** reconciliar com a fonte EDP. **Divergência aberta:** plano pede `forno_eletrico` FP 1,0; código tem 0,8. **Confirmar com a norma antes de mudar** (ver §6). `iluminacao_descarga` 0,55 já confere.
- **Aceite:** FP por tipo batem com a EDP v06 documentada e versionada.

**Passo 0.4 — Tensão de placa por carga** 🟡 `[deriva de F-05]`
- **Arquivos:** `dependencia.ts` (`tensaoFixa` já existe — promover de "fallback silencioso" para "default editável e explícito por carga"), UI de cadastro (`NovaDependenciaModal.tsx`/`EditarDependenciaModal.tsx`), `api/schemas/dependencia.ts`.
- **Ação:** capturar tensão nominal por carga; default por tipo, editável; **não** assumir 220 V para todo TUE.
- **Aceite:** micro-ondas declarado 127 V não é tratado como 220 V bifásico.

**🚪 Gate Fase 0:** toda carga classificada (tipo + tensão); nenhuma pendência de tipo; cálculo bloqueado se houver.

---

### FASE 1 — Demanda e entrada *(consome Fase 0)*

**Passo 1.1 — Revalidação da demanda por grupo** 🟢
- **Arquivos:** `motor-demanda.ts`, `motor-edp-sp.ts`, `fatores-demanda.ts`/`.data.json`, `__tests__/motor-demanda.test.ts`.
- **Ação:** reexecutar a demanda com a classificação obrigatória; confirmar grupos f e g e a entrada do AC.
- **Aceite:** DT recalculado e completo; demanda reproduzível a partir das tabelas.

**Passo 1.2 — Tabela 001/002 + entrada** 🟡 `[CRÍTICO — dado]`
- **Arquivos:** `subcategorias-fornecimento.data.json` (hoje `[]`), `seletor-subcategoria.ts`, `validacao.ts` (`ATN-TABELA-NAO-VERIFICADA`).
- **Ação:** **popular** a escada completa da Categoria T (T2…T10) com pares disjuntor↔seção válidos e rótulos coerentes; **tornar bloqueante** o estado `verificar/tabelas_001_002_ausentes` e `status_verificacao=VERIFICAR` (hoje é só ATENÇÃO). Validar `IB ≤ In ≤ Iz` na saída.
- **Aceite:** para a corrente de demanda correta, a entrada resolve sub-categoria coerente (ex.: T2 p/ ~58–67 A); **nunca** 150 A com 25 mm²; sem dados, o sistema **bloqueia** em vez de avisar.
- **Pendência de dado:** valores oficiais T2…T10 (ver §6).

**Passo 1.3 — Arredondamento de exibição** 🟡 `[MÉDIO]`
- **Arquivos:** `lib/utils/round.ts`, `lib/formatters.ts`, `ValorRastreavel.tsx`.
- **Ação:** exibir corrente com casas decimais adequadas (ex.: 58,3 A).
- **Aceite:** sem dízimas na interface.

**🚪 Gate Fase 1:** entrada dimensionada de forma segura e completa; remove o "Bloqueio A".

---

### FASE 2 — Divisão de Circuitos *(keystone — consome Fase 1)* 🔴 `[ALTO]`

> A entidade `Circuito` existe (`modelo/circuito.ts`), mas a **divisão real NBR 9.5.3 não existe** — `derivar-circuitos.ts` é mapeador provisório (1 circuito por carga). Esta fase **substitui** esse mapeador por um motor de divisão real.

**Passo 2.1 — Motor de divisão de circuitos** 🔴
- **Arquivos:** novo `calculo/divisao-circuitos.ts` (substitui o uso provisório de `derivar-circuitos.ts`); estender `modelo/circuito.ts` com `tipo` granular (iluminação / TUG seca / TUG molhada / TUE dedicado / carga fixa) e vínculo carga↔ambiente.
- **Ação:** alocar cargas conforme NBR 5410 9.5.3: iluminação separada de TUG; circuito exclusivo para cada TUE e equipamento > 10 A; agrupar respeitando limites; tipar cada circuito.
- **Aceite:** nenhum circuito mistura iluminação e TUG; chuveiro/motor/AC em circuitos próprios; cada carga em exatamente um circuito.

**Passo 2.2 — Marcação de DR por circuito** 🔴
- **Arquivos:** `modelo/circuito.ts` (novo campo `requer_DR`/`corrente_diferencial_mA`), modelo de ambiente (`dependencia.ts`: flags molhado/externo já presumidas — verificar e adicionar).
- **Ação:** marcar `requer_DR` (≤ 30 mA) em circuito que sirva área molhada/externa (NBR 5410 5.1.3.2).
- **Aceite:** banheiros, cozinha e área externa saem com DR obrigatório marcado.

**Passo 2.3 — Tensão por circuito e IB definitivo** 🟡
- **Arquivos:** `corrente-circuitos.ts`, `resolver-ligacao.ts` (já existem), consumindo a tensão por carga da Fase 0.4.
- **Ação:** selecionar tensão de cada circuito e recalcular IB com ligação correta (mono/bi/tri).
- **Aceite:** IB por circuito reflete a tensão real; pronto para dimensionamento.

**🚪 Gate Fase 2:** circuitos terminais reais, tipados, com DR e IB corretos.

---

### FASE 3 — Dimensionamento elétrico por circuito *(consome Fase 2)* 🔴 `[ALTO]`

**Passo 3.1 — Captura de dados de instalação** 🔴
- **Arquivos:** `modelo/circuito.ts` (novos campos: `metodo_instalacao`, `temperatura_ambiente_C`, `circuitos_agrupados`, `comprimento_m`), UI e schemas correspondentes, nova tabela `tabela-metodos-instalacao.data.json`.
- **Aceite:** todo circuito tem os quatro dados; sem eles, o dimensionamento não roda (fail-closed).

**Passo 3.2 — Dimensionamento de condutores** 🔴
- **Arquivos:** novo `calculo/dimensionar-condutores.ts`; novas tabelas `ampacidade.data.json` e `fatores-correcao.data.json` (NBR 5410 Tab. 36–39 e 47).
- **Ação:** seção mínima (1,5 mm² ilum / 2,5 mm² força) + ampacidade com correção de temperatura/agrupamento; garantir `IB ≤ Iz`.
- **Aceite:** seção de cada circuito satisfaz ampacidade corrigida e piso mínimo.
- **Pendência de dado:** tabelas de ampacidade e fatores (§6).

**Passo 3.3 — Queda de tensão** 🔴
- **Arquivos:** novo `calculo/queda-tensao.ts`; critérios em `tabela-queda-tensao.data.json`.
- **Ação:** queda acumulada por circuito; reiterar seção quando a queda governar (NBR 5410 6.2.7).
- **Aceite:** queda dentro do limite; seção ajustada onde necessário.

**Passo 3.4 — Proteção contra sobrecorrente** 🔴
- **Arquivos:** novo `calculo/protecao-sobrecorrente.ts`; tabela de dispositivos.
- **Ação:** dimensionar proteção com `IB ≤ In ≤ Iz` **e** `I₂ ≤ 1,45·Iz`; verificar Icu vs. curto presumido.
- **Aceite:** as duas inequações satisfeitas em todos os circuitos; Icu compatível.

**🚪 Gate Fase 3:** condutores e proteções de circuito dimensionados e verificados.

---

### FASE 4 — Sistema *(consome Fase 3)*

**Passo 4.1 — Balanceamento de fases** ✅ `[verificação/integração]`
- **Estado:** `balanceamento-fases.ts` já implementa LPT correto. **Ação reduzida:** integrar com os circuitos **reais** da Fase 2 (hoje opera sobre o andaime provisório) e expor antes/depois na UI (`projetos.$projetoId_.correntes.tsx`).
- **Aceite:** corrente por fase aproximadamente equilibrada sobre circuitos reais.

**Passo 4.2 — Aterramento e equipotencialização** 🔴 `[MÉDIO]`
- **Arquivos:** `modelo/projeto.ts` (esquema de aterramento — tipicamente TN-C-S na entrada EDP `[VERIFICAR]`), `modelo/circuito.ts` (condutor PE), novo `calculo/aterramento.ts`.
- **Ação:** definir esquema; dimensionar PE por circuito; especificar BEP e equipotencialização suplementar em áreas molhadas (NBR 5410 6.4).
- **Aceite:** todo circuito com PE; BEP definido; áreas molhadas com equipotencialização suplementar.

**🚪 Gate Fase 4:** instalação eletricamente completa e equilibrada; proteção contra choque íntegra (DR + PE + equipotencialização).

---

### FASE 5 — Saída auditável *(consome tudo)* 🟡 `[MÉDIO]`

**Passo 5.1 — Memorial, quadro de cargas e unifilar** 🟡/🔴
- **Arquivos:** estender `servico-auditoria.ts` + `ValorRastreavel.tsx` (rastreio já parcial); novos geradores de quadro de cargas por circuito e diagrama unifilar; rota de relatório.
- **Ação:** memorial rastreável (entradas, fórmulas, normas, etapas), quadro de cargas e unifilar.
- **Aceite:** documento auditável suficiente para conferência e base de ART.

---

## 5. Camada transversal — Fail-closed e gates de liberação

> Esta é a correção de **maior alavancagem**. Hoje a máquina de estados (`transicoes.ts`) permite `CALCULAR` sem checar pendências, e os diagnósticos (`validacao.ts`) são informativos.

Implementar os 6 portões do `plano_correcao_obrigatoria_modulos.md` §18 como **guardas reais** na máquina de estados / serviços:

| Gate | Bloqueia avanço se… | Ponto de implementação |
|---|---|---|
| G1 cálculo preliminar | falta tensão/sistema, dimensões, potência/tensão/tipo de carga, regra não versionada | `servico-calculo.ts` + `transicoes.ts` |
| G2 demanda EDP | carga sem grupo/`tipoAparelho`; concessionária indefinida; categoria×sistema incompatível | `adaptador-projeto.ts` + `validacao.ts` (promover ERRO a blocker) |
| G3 circuitos | cargas incompletas; exclusivos não identificados; DR obrigatório não marcado | motor da Fase 2 |
| G4 condutores | falta IB/método/comprimento/temperatura/agrupamento/isolação | motor da Fase 3 |
| G5 proteção | condutores não dimensionados; Iz não calculada; queda não validada; curto não informado | motor da Fase 3.4 |
| G6 relatório | qualquer erro crítico; circuito sem proteção; DR/aterramento ausentes; artefatos faltando; sem ART | `servico-auditoria.ts` + rota de relatório |

**Regra única:** o botão **"Concluir projeto"** permanece bloqueado enquanto houver qualquer pendência crítica (V01–V15 do plano de módulos). As regras V01–V15 devem virar testes (CT04–CT12).

---

## 6. Pendências de dados normativos (bloqueiam fases, não dependem de código)

| Dado | Onde entra | Bloqueia |
|---|---|---|
| Tabela 001/002 — sub-categorias Categoria T (T2…T10): par disjuntor↔seção | `subcategorias-fornecimento.data.json` | Fase 1.2 |
| FP oficial por tipo (resolver divergência forno 0,8 vs 1,0) | `fatores-potencia.data.json` | Fase 0.3 |
| Tabelas de ampacidade NBR 5410 (Tab. 36–39) | nova `ampacidade.data.json` | Fase 3.2 |
| Fatores de correção (temperatura/agrupamento) | nova `fatores-correcao.data.json` | Fase 3.2 |
| Limites de queda de tensão (6.2.7) e ponto de referência | nova `tabela-queda-tensao.data.json` | Fase 3.3 |
| Esquema de aterramento padrão da entrada EDP (TN-C-S?) | `projeto.ts` | Fase 4.2 |

---

## 7. Riscos e observações

1. **Risco de retrabalho por planos desatualizados:** seguir os documentos `Correção_1` ao pé da letra reimplementaria itens já prontos (classificação, balanceamento). Use a §2 deste documento como filtro.
2. **Divergência FP forno (0,8 × 1,0):** não alterar sem confirmar a fonte EDP v06 — mudança de FP propaga para demanda e corrente.
3. **`derivar-circuitos.ts` é provisório por design** (o próprio código diz). Não "consertar" o mapeador; **substituí-lo** pelo motor da Fase 2 e remover o uso provisório com cuidado (verificar consumidores em rotas/serviços).
4. **Persistência:** novos campos de circuito (Fase 3) exigem migrations Supabase (`docs/supabase/0003_*.sql`) e atualização dos mapeadores (`infra/supabase/mapeadores.ts`).
5. **Classificação atual do produto:** enquanto Fases 2–5 não fecharem, manter o rótulo do plano de módulos §20 — *"Ferramenta de pré-dimensionamento, não liberada para projeto executivo"*. Liberação só após nova validação técnica integral + ART.

---

## 8. Sequência recomendada (roadmap)

```
[Camada transversal: Fail-closed/Gates] ── habilita segurança desde o início
        │
Fase 0 (saneamento) → Fase 1 (demanda+entrada) → 🚪 remove Bloqueio A
        │
Fase 2 (divisão de circuitos — keystone, greenfield)
        │
Fase 3 (condutores, queda, proteção — greenfield)
        │
Fase 4 (balanceamento[reuso] + aterramento) → 🚪 remove Bloqueio B
        │
Fase 5 (memorial, quadro, unifilar) → 🚪 habilita parecer de liberação
        │
Fase de homologação (CT01–CT12 + revisão de eng. eletricista)
```

**Quick wins (baixo esforço, alto valor), na ordem:**
1. Tornar pendências críticas **bloqueantes** (Fase 0.1 + §5) — destrava a segurança "fail-closed".
2. Tornar `VERIFICAR`/tabela vazia **bloqueante** (Fase 1.2) — fecha o risco do par disjuntor/condutor incoerente.
3. Congelar com testes o que já está correto (0.2, 4.1) para evitar regressão durante o greenfield.

---

## 9. Próximos passos sugeridos (handoff)

- **@architect (Aria):** validar o desenho do motor de Divisão de Circuitos (Fase 2) e do modelo estendido de `Circuito` (Fase 3) — são as decisões estruturais.
- **@data-engineer (Dara):** migrations Supabase para os novos campos + carga das tabelas normativas (§6).
- **@pm (Morgan):** transformar este plano em épico + stories, bloco a bloco (§4), com as pendências de dado (§6) como pré-requisitos explícitos.
- **Especialista normativo / eng. eletricista:** fornecer os dados oficiais EDP/NBR da §6 e homologar (CT01–CT12).

> **Nota de integridade (Artigo IV — No Invention):** todos os vereditos da §2 derivam de leitura direta dos arquivos citados. Onde o dado normativo não existe no repositório (T2…T10, ampacidades, FP do forno), o item está marcado como **pendência de dado**, não como decisão — a definição cabe à fonte EDP/NBR e ao responsável técnico.

— Atlas, investigando a verdade 🔎
