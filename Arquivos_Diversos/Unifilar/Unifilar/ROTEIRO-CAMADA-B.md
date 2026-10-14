# ROTEIRO-CAMADA-B.md
## SIE — Implementação Integral da Camada B (Renderizador SVG Próprio)
### Roteiro de procedimentos para execução por LLM em terminal (ex.: Claude Code)

**Versão:** 2.0 · Julho 2026 (substitui a versão anterior — agora ancorado nos artefatos entregues)
**Base normativa:** ABNT NBR 5410:2004 · EDP-SP PT.DT.PDN.00068 v09 · PT.DT.PDN.03.14.020 v06 · IEC 60617 · IEC 60228
**Documento de referência:** PRD — Camada de Visualização v1.0 (Seções 4, 5, 6)
**Artefatos de entrada (obrigatórios, já produzidos e testados 6/6):**
- `sie-camada-visualizacao-fase0-1b.zip` — contrato canônico, adaptador 1:1, router, export_dxf, simbolos_iec.tsx, UnifilarHero.tsx, testes T1–T6
- `demo-unifilar-hero.jsx` — referência visual de comportamento esperado (NÃO integrar ao produto)
- `unifilar-proj-1-exemplo.dxf` — referência de validação do formato DXF

**Uso prático:** extraia o zip na raiz do repositório do SIE, abra a LLM de terminal
nessa raiz e cole este roteiro inteiro como primeira mensagem. A LLM executa E0 e para.

---

## §0 — REGRAS GERAIS (VALEM PARA TODAS AS ETAPAS — RELEIA ANTES DE CADA UMA)

**RG-01 — Uma etapa por vez.** Execute exclusivamente a etapa corrente (E0→E7, em ordem).
Ao concluir, apresente o RELATÓRIO DE ETAPA (formato no §9) e **PARE**. Não inicie a
próxima etapa sem confirmação explícita do operador ("prossiga para E<n>").

**RG-02 — Projeção, não recálculo.** Nenhum componente da Camada B calcula, converte
ou interpreta valores elétricos. Todo valor exibido vem do contrato canônico
(`CircuitoCanonico`) servido pelo backend. Se um valor necessário não existe no
contrato, exiba `[VERIFICAR]` — jamais derive.

**RG-03 — Disciplinas normativas invioláveis:**
- INC-01: `va_total` é VA direto. Proibido dividir por fator de potência em qualquer ponto.
- INC-04: tensão ausente = `null`. Proibido fallback para 127 V (ou qualquer default).
- INC-03: zona molhada não classificada = `null`. Proibido assumir `false`.
- INC-07: seção de condutor só existe se pertencer à série IEC 60228 (validador já no contrato).

**RG-04 — Determinismo (RNF-03).** Mesma entrada JSON → mesmo SVG, byte-identical.
Proibido em qualquer componente de renderização: `Math.random`, `Date.now`,
`new Date`, `crypto.randomUUID`, iteração sobre objetos sem ordenação explícita,
ids gerados por contador global. Ordenação sempre vinda do backend.

**RG-05 — Valores normativos são dados, não código.** Tabelas EDP (001/002),
limites e parâmetros vão em arquivos de configuração com campos `fonte`,
`referencia` e `status_verificacao`. Valor não confirmado contra a norma =
`status_verificacao: "VERIFICAR"`. Proibido hardcode de valor normativo em componente.

**RG-06 — Definição canônica única de símbolo.** Qualquer alteração de geometria em
`simbolos_iec.tsx` exige alteração espelhada no bloco `BLK_*` correspondente em
`export_dxf.py`, e vice-versa. Registre o par de arquivos alterados no relatório.

**RG-07 — NÃO TOCAR (global, todas as etapas):**
- Módulos de cálculo existentes do SIE (demanda, IB, categoria, padrão de entrada).
- Schemas/tabelas do banco (apenas leitura via loader).
- `contrato_circuito.py` — o contrato é congelado; extensões só com aprovação do operador.
- Camada A / Fable 5 (fora deste roteiro).
- Motor de geometria.
- `demo-unifilar-hero.jsx` — é referência, não código de produto.

**RG-08 — Guardas automáticas (execute ao final de TODA etapa que altera código):**
```bash
# G1 — fallback de tensão proibido (INC-04)
grep -rnE "(\?\?|\|\|)\s*127|tensao\w*\s*(=|:)\s*127|voltage\w*\s*(=|:)\s*127" --include="*.py" --include="*.tsx" --include="*.ts" <dirs_da_camada_b> && echo "VIOLAÇÃO INC-04" || echo "G1 OK"
# G2 — divisão por FP proibida (INC-01)
grep -rniE "/\s*(fp|fator_potencia|power_factor|pf)\b" --include="*.py" --include="*.tsx" --include="*.ts" <dirs_da_camada_b> && echo "VIOLAÇÃO INC-01" || echo "G2 OK"
# G3 — não-determinismo proibido (RNF-03)
grep -rnE "Math\.random|Date\.now|new Date\(|randomUUID" --include="*.tsx" --include="*.ts" <dirs_de_renderizacao_svg> && echo "VIOLAÇÃO RNF-03" || echo "G3 OK"
# G4 — zona molhada / DR assumidos (INC-03)
grep -rnE "(zona_molhada|requisito_dr)\s*(=|:)\s*(False|false)" --include="*.py" <dirs_da_camada_b> | grep -viE "test|fixture" && echo "VIOLAÇÃO INC-03 — inspecionar" || echo "G4 OK"
```
Substitua `<dirs_da_camada_b>` pelos diretórios reais identificados em E0.
Qualquer "VIOLAÇÃO" = etapa reprovada; corrija antes de reportar.

**RG-09 — Não-regressão obrigatória.** Toda etapa termina com:
```bash
pytest sie_visualizacao/tests/ -v
```
mais os testes criados nas etapas anteriores. Falha de teste antigo = regressão;
corrija sem alterar o teste (salvo aprovação explícita do operador).

**RG-10 — Idioma e rastreabilidade.** Código, comentários, mensagens e relatórios
em português brasileiro. Todo elemento visual novo carrega `fonte_linha` /
`status_linha` propagados do contrato.

**RG-11 — Commits.** Um commit por etapa concluída e aprovada, mensagem
`camada-b(E<n>): <título da etapa>`. Nada de commit parcial entre etapas.

---

## E0 — PREPARAÇÃO E INVENTÁRIO (somente leitura + setup)

**Objetivo:** ambiente pronto, artefatos íntegros, mapa do repositório real.

**Procedimento:**
1. Confirme que `sie_visualizacao/` existe na raiz com a estrutura do zip
   (`backend/`, `frontend/`, `tests/`, `README.md`). Se não, extraia o zip.
2. Instale dependências backend respeitando o gerenciador do projeto
   (poetry/uv/pip — detecte antes): `pydantic fastapi ezdxf pytest httpx`.
3. Rode a suíte base: `pytest sie_visualizacao/tests/ -v` → **exigido 6/6**.
4. Inventário (somente leitura, sem alterar nada):
   - Onde o app FastAPI registra routers (`main.py`/`app.py`)?
   - Quais modelos SQLAlchemy contêm pontos de carga, tensão, VA, IB, fases,
     grupo EDP, classificação de zona molhada? Monte a tabela
     `tabela.coluna → campo PontoCarga`, lacunas marcadas `[VERIFICAR]`
     (ex.: "não há coluna de zona molhada → `zona_molhada=None` sempre").
   - Estrutura do frontend React: pasta de componentes, roteamento, versão do
     Carbon, padrão de chamada à API (fetch/axios/react-query).
   - Existe infra Node no servidor (para Puppeteer/Playwright em E4)? Sim/Não.

**Critérios de aceite:**
- E0-A1: pytest 6/6 verde no ambiente do projeto.
- E0-A2: tabela de mapeamento SQLAlchemy → `PontoCarga` apresentada, com lacunas explícitas.
- E0-A3: nenhum arquivo do repositório original alterado (`git status` limpo, exceto `sie_visualizacao/`).

**PARE. Aguarde confirmação.**

---

## E1 — INTEGRAÇÃO BACKEND (loader real + endpoint vivo)

**Objetivo:** `GET /api/v1/projetos/{id}/visualizacao` respondendo com dados reais
do banco (proj-1, 44 circuitos via adaptador 1:1).

**Procedimento:**
1. Crie `sie_visualizacao/backend/loader_pontos.py`:
   `carregar_pontos_do_projeto(projeto_id: str) -> list[PontoCarga]`, usando a
   sessão SQLAlchemy do projeto e o mapeamento de E0.
   - Coluna de tensão vazia/ausente → `tensao_v=None` (INC-04). Nunca preencher.
   - IB lido da coluna persistida pelo módulo IB. Se não existir persistido,
     `corrente_ib_a=None` + reporte `[VERIFICAR]` (não calcule no loader).
   - Sem classificação de zona molhada → `zona_molhada=None` (INC-03).
2. No app principal: `app.include_router(router)` +
   `registrar_repositorio(carregar_pontos_do_projeto)` — únicas linhas tocando
   arquivo pré-existente nesta etapa.
3. Teste de integração `sie_visualizacao/tests/test_e1_endpoint.py` (TestClient):
   - 200 para proj-1; `total_circuitos == 44`; `provisorio is True`;
   - todo circuito com `tensao_v == null` tem `corrente_projeto_a == null` e status `ATENÇÃO`;
   - duas chamadas consecutivas retornam corpo JSON idêntico (byte a byte).
4. Guardas RG-08 + suíte completa RG-09.

**NÃO TOCAR nesta etapa:** frontend; `export_dxf.py`; qualquer módulo de cálculo.

**Critérios de aceite:**
- E1-A1: chamada real ao endpoint retorna os 44 circuitos do proj-1.
- E1-A2: soma de `va_total` do payload == carga instalada exibida hoje na tela
  Correntes/IB do SIE (informe o número; divergência = investigar e reportar, não ajustar).
- E1-A3: teste de identidade de payload (determinismo) verde.

**PARE. Aguarde confirmação.**

---

## E2 — INTEGRAÇÃO FRONTEND (página Unifilar Hero + memorial)

**Objetivo:** página real no app React/Carbon renderizando o unifilar do backend,
com click-to-trace abrindo memorial (UF-03) e faixa "Árvore provisória" (R-04).

**Procedimento:**
1. Copie `simbolos_iec.tsx` e `UnifilarHero.tsx` para a pasta de componentes do
   projeto (ex.: `src/components/unifilar/`). Ajuste apenas imports/paths — não
   altere geometria nem layout (RG-06).
2. Crie a página/rota `Unifilar` que consome o endpoint de E1 (padrão de fetch
   detectado em E0) e renderiza `<UnifilarHero>`.
3. Memorial: `SidePanel` (ou `Modal`) Carbon recebendo o circuito de `onTrace`,
   exibindo `derivacao` (regra, referência normativa, fórmula, entradas),
   `fonte_linha`, `status_linha`, pendências, e campos P1 como
   `[VERIFICAR] — aguarda P1`. Use `demo-unifilar-hero.jsx` como referência de
   conteúdo/comportamento do painel — não copie estilos inline para o produto;
   use componentes e tokens Carbon do projeto.
4. Estados de carregamento (skeleton Carbon) e erro (InlineNotification) — sem
   inventar dados em caso de erro.
5. Acessibilidade: Tab percorre os 44 circuitos, Enter/Espaço abre memorial,
   foco visível (UF-06). Rode axe/lighthouse se disponível.

**NÃO TOCAR:** backend (congelado após E1); geometria dos símbolos.

**Critérios de aceite:**
- E2-A1: página exibe 44 circuitos sem sobreposição (UF-01) e faixa provisória visível.
- E2-A2: circuito com tensão `null` renderiza tracejado + badge ATENÇÃO (UF-02).
- E2-A3: clique e Tab+Enter abrem o memorial com fórmula `IB = S / V` e referência NBR (UF-03, UF-06).
- E2-A4: nenhum valor exibido difere do payload (amostragem de 3 circuitos, incluindo 1 pendente).

**PARE. Aguarde confirmação.**

---

## E3 — DETERMINISMO E NÃO-REGRESSÃO VISUAL (RNF-03 / UF-04)

**Objetivo:** prova automatizada de que mesma entrada → mesmo SVG, byte-identical.

**Procedimento:**
1. Crie renderização isolada do SVG para teste: função/script que, dado o JSON do
   contrato, serializa o SVG do `UnifilarHero` (`renderToStaticMarkup` de
   react-dom/server, ou vitest+jsdom — conforme ferramental do projeto).
2. Congele a fixture `sie_visualizacao/tests/fixtures/proj1_visualizacao.json`
   (payload real capturado de E1).
3. Teste byte-identical: renderizar a fixture duas vezes → strings idênticas
   (igualdade estrita, não snapshot "aproximado").
4. Teste de sensibilidade: alterar 1 campo da fixture (ex.: `va_total` de um
   circuito) → o SVG DEVE mudar (evita teste vazio).
5. Registre o hash SHA-256 do SVG canônico do proj-1 no relatório — baseline
   para auditoria diff-based.
6. Guardas RG-08 (G3 em especial) + suíte completa.

**Critérios de aceite:**
- E3-A1: teste byte-identical verde em 2 execuções consecutivas.
- E3-A2: teste de sensibilidade verde.
- E3-A3: hash baseline registrado.

**PARE. Aguarde confirmação.**

---

## E4 — ENDPOINTS DE EXPORTAÇÃO (DXF e PDF — UF-05 / RNF-08)

**Objetivo:** download real de DXF e PDF do unifilar a partir do app.

**Procedimento:**
1. `GET /api/v1/projetos/{id}/unifilar.dxf`: reutiliza o payload de E1 e
   `exportar_unifilar_dxf` (não duplicar lógica de layout). `media_type`
   `image/vnd.dxf`, nome de arquivo com id do projeto.
2. Teste: baixar o DXF do proj-1 via TestClient, abrir com `ezdxf.readfile`,
   assert versão AC1024, layers `SIE_*`, blocos `BLK_*`, nº de INSERTs ≥ 44 + cabeçalho
   (mesmos asserts do T6, agora ponta a ponta). Compare visualmente com
   `unifilar-proj-1-exemplo.dxf` de referência.
3. PDF (SVG → PDF vetorial):
   - Com infra Node (confirmada em E0): Puppeteer/Playwright headless imprime o
     SVG serializado de E3 (HTML mínimo) em A3 paisagem, vetorial, margens para carimbo.
   - Sem infra Node: implemente `GET .../unifilar.svg` (SVG já determinístico) e
     registre o PDF como `[VERIFICAR] — pendente de infra`, sem fallback raster.
4. Botões de exportação na página de E2 (Carbon `Button` + ícone Download).

**NÃO TOCAR:** layout do DXF/SVG (congelados por E3 — mudar layout invalida o baseline).

**Critérios de aceite:**
- E4-A1: DXF baixado do app validado por script ezdxf.
- E4-A2: PDF vetorial gerado (texto selecionável) OU pendência declarada com causa.
- E4-A3: hash do SVG servido == baseline de E3 (nenhum drift).

**PARE. Aguarde confirmação.**

---

## E5 — TRIFILAR DO PADRÃO DE ENTRADA (PRD 4.2)

**Objetivo:** diagrama trifilar parametrizado por categoria/subcategoria EDP,
com dados das Tabelas 001/002 externalizados.

**Procedimento:**
1. Crie `sie_visualizacao/config/tabelas_edp_padrao_entrada.json`: uma linha por
   subcategoria relevante (mínimo T4, T6, D4) com os campos que o diagrama usa
   (disjuntor geral, seção do ramal, tipo de medição, características do quadro)
   e, por linha, `fonte` (ex.: "PT.DT.PDN.03.14.020 v06 — Tabela 001, linha X"),
   `referencia` e `status_verificacao`. **Preencha apenas valores que constem de
   documentos/configs presentes no repositório; todo o resto entra `null` +
   `status_verificacao: "VERIFICAR"`. Proibido estimar (RG-05).**
2. Backend: `GET /api/v1/projetos/{id}/padrao-entrada` → categoria/subcategoria
   do projeto (lida do módulo já existente, sem recalcular) + a linha da tabela.
3. Componente `TrifilarPadraoEntrada.tsx`: 3 fases + neutro (+ PE), medição,
   dispositivo geral, reutilizando `simbolos_iec.tsx`; rótulos vindos do
   endpoint; campos `VERIFICAR` renderizam badge ATENÇÃO.
4. Testes: trocar subcategoria na fixture (T4→T6→D4) altera rótulos de
   disjuntor/condutor conforme a linha correspondente (PE-01, PE-02); snapshot
   byte-identical por subcategoria (estende E3).

**Critérios de aceite:**
- E5-A1: nenhum valor normativo hardcoded em componente (inspeção + grep por
  valores de ampacidade/seção nos .tsx).
- E5-A2: PE-01 e PE-02 verdes; toda lacuna listada com `status_verificacao: VERIFICAR`.
- E5-A3: determinismo por subcategoria verde.

**PARE. Aguarde confirmação.**

---

## E6 — MULTIFILAR / FUNCIONAL POR CIRCUITO (PRD 4.3, com placeholders P1)

**Objetivo:** detalhe de circuito individual com todos os condutores, honrando
a pendência estrutural do P1.

**Procedimento:**
1. Componente `MultifilarCircuito.tsx`: recebe UM `CircuitoCanonico`;
   - bifásico (2 fases) → 2 condutores de fase + N + PE; monofásico → F + N + PE (MF-01);
   - fases rotuladas com as letras reais de `fases[]`; `fases=[]` → condutores
     tracejados + `[VERIFICAR]`;
   - `secao_mm2`/`disjuntor_a` `null` → rótulo `[VERIFICAR] — aguarda P1` (MF-02);
     comprimento não existe no contrato → sempre `[VERIFICAR]` (não inventar campo).
2. Acesso: botão "Ver multifilar" dentro do memorial de E2 (não criar rota nova
   sem necessidade).
3. Testes: MF-01 para um circuito 220 V bifásico e um 127 V monofásico da
   fixture; MF-02 (placeholders); snapshot determinístico.

**NÃO TOCAR:** contrato (não adicionar campo `comprimento` — definição pertence
ao P1; registre como pendência de contrato no relatório).

**Critérios de aceite:**
- E6-A1: MF-01 verde nos dois casos.
- E6-A2: MF-02 verde — nenhum valor de seção/disjuntor exibido sem origem no contrato.
- E6-A3: suíte completa (T1–T6 + E1–E6) verde + guardas RG-08 limpas.

**PARE. Aguarde confirmação.**

---

## E7 — RELATÓRIO FINAL E CONSOLIDAÇÃO

**Objetivo:** fechamento auditável da Camada B.

**Procedimento:**
1. Rode a suíte integral + as 4 guardas em todos os diretórios da Camada B.
2. Produza `RELATORIO-CAMADA-B.md` na raiz de `sie_visualizacao/` contendo:
   - matriz de critérios: UF-01..06, PE-01..02, MF-01..02, RNF-02/03/04/08/09
     → estado (ATENDIDO / PARCIAL / VERIFICAR) + evidência (teste/arquivo/hash);
   - RNF-02: medir tempo de renderização do unifilar de 44 circuitos
     (Performance API/profiler) e registrar contra o teto de 500 ms;
   - lista consolidada de TODOS os `[VERIFICAR]` remanescentes, com dono sugerido
     (operador / P1 / Divisão / documento EDP);
   - pares símbolo React ↔ bloco DXF alterados (RG-06) durante o roteiro;
   - hashes SHA-256 baseline: SVG do proj-1 + cada subcategoria do trifilar;
   - fora do escopo, explicitamente: Planta Elétrica 4.4 (aguarda Geometria
     Fase 4), Curvas T×I e Aterramento (Fase 2+), Camada A/Fable (outro roteiro).
3. Nenhuma alteração de código nesta etapa além de correções de regressão.

**Critérios de aceite:**
- E7-A1: suíte 100% verde, guardas limpas.
- E7-A2: relatório entregue com matriz completa e pendências rastreáveis.

**FIM DO ROTEIRO.**

---

## §9 — FORMATO DO RELATÓRIO DE ETAPA (obrigatório ao fim de cada E<n>)

```
=== RELATÓRIO E<n> — <título> ===
Arquivos criados:    <lista>
Arquivos alterados:  <lista + 1 linha de motivo cada>
Testes executados:   <comando> → <X passed / Y failed>
Guardas RG-08:       G1 <OK/VIOLAÇÃO> · G2 <..> · G3 <..> · G4 <..>
Critérios de aceite: E<n>-A1 <ATENDIDO/FALHOU + evidência> ...
[VERIFICAR] novos:   <lista ou "nenhum">
Fora do escopo tocado: NENHUM (obrigatório — se não puder afirmar, explique e pare)
Commit: camada-b(E<n>): <mensagem>
Próxima etapa proposta: E<n+1> — aguardando confirmação do operador.
```

## §10 — PROTOCOLO DE EXCEÇÃO

Se qualquer instrução deste roteiro conflitar com o código real do repositório
(coluna inexistente, versão de Carbon incompatível, rota ocupada):
**não improvise a resolução normativa**. Descreva o conflito, proponha no máximo
2 alternativas com trade-offs, marque `[VERIFICAR]` e aguarde decisão do operador.
Conflitos de engenharia pura (nome de pasta, ferramenta de teste) podem ser
resolvidos autonomamente, registrando a decisão no relatório da etapa.
