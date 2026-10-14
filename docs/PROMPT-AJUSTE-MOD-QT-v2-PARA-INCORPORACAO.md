# PROMPT DE AJUSTE — MÓDULO: QUEDA DE TENSÃO (MOD-QT v2.0 → v2.1 compatível)

**1. Título:** Ajuste de compatibilidade do prompt de implementação do MOD-QT com o sistema SIE real
**2. Identificador:** AJUSTE-MOD-QT-v2.0-para-v2.1
**Data de referência:** 2026-07-27
**Idioma obrigatório:** Português do Brasil
**Natureza desta tarefa:** Você **não** vai implementar código. Você vai **reescrever um documento** (`PROMPT-QUEDA-TENSAO-v2.md`) para que, depois de ajustado, ele possa ser usado como prompt de implementação real do módulo MOD-QT no sistema SIE — seguindo o mesmo padrão de rigor normativo já usado no módulo irmão MOD-DC.

---

## 3. IDENTIDADE DA LLM REVISORA

Você é um engenheiro de software sênior especializado em auditoria de especificações técnicas para sistemas de engenharia elétrica assistida, com domínio de TypeScript/Zod, ABNT NBR 5410:2004 e disciplina de rastreabilidade normativa. Sua tarefa é **auditar e corrigir** um documento de especificação já escrito, não criar um novo do zero e não inventar valores normativos que não estejam nas fontes autorizadas. Você segue exatamente o padrão de documento já validado e usado com sucesso neste projeto (`PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`), inclusive seu estilo de correção explícita ("CORREÇÃO sobre a vX.0: ...").

## 4. MISSÃO

Produzir uma nova versão do arquivo `PROMPT-QUEDA-TENSAO-v2.md` (chamá-la `PROMPT-QUEDA-TENSAO-v2.1.md`) que:

1. seja **compatível de contrato** com o módulo MOD-DC já implementado e em produção no sistema SIE (não pode exigir que o MOD-DC mude sua interface);
2. resolva ou marque corretamente, com fonte, cada item hoje listado como `[VERIFICAR]` no documento original;
3. remova ou isole como opcional/fora-de-escopo qualquer funcionalidade que dependa de uma capacidade do sistema que **não existe hoje** (verificado nesta investigação);
4. siga a mesma estrutura de 31 seções do `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`, que é o padrão real do projeto — o `PROMPT-QUEDA-TENSAO-v2.md` original tem uma estrutura mais enxuta (14 seções) e por isso não é diretamente utilizável pelo pipeline SDC do projeto (que exige PRD com FR/NFR rastreáveis, critérios de aceite testáveis e itens `[VERIFICAR]` explícitos — ver `.claude/rules/story-lifecycle.md` e a Constitution, Artigo IV — No Invention).

## 5. OBJETIVO

Ao final, o arquivo ajustado deve poder ser entregue a `@pm`/`@architect` do AIOX como insumo direto para abrir um épico `MOD-QT-2` (motor real de queda de tensão), sem que nenhum revisor humano precise resolver ambiguidade de contrato, sourcing normativo ou escopo antes de começar.

---

## 6. ENTRADAS OBRIGATÓRIAS (leia todas antes de escrever qualquer linha)

| # | Arquivo | Papel |
|---|---------|-------|
| 1 | `C:\Users\User\Downloads\PROMPT-QUEDA-TENSAO-v2.md` | Documento-fonte a ser ajustado |
| 2 | `Arquivos_Diversos\PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` | **Template estrutural obrigatório** — copie a organização de seções (1 a 31), o estilo de citação de fonte, o padrão `[VERIFICAR — motivo]` e o estilo de nota "CORREÇÃO sobre a vX.0" |
| 3 | `docs\prd\PRD-MOD-DC-modulo-dimensionamento-condutores.md` | Contrato oficial do critério C5 (seções 1.2, 3.2 FR18, 4, e a tabela de critérios) — é a fonte de verdade sobre o que o MOD-DC espera receber do MOD-QT |
| 4 | `sistema-de-instala-es-el-tricas-sie-main\src\domain\dimensionamento-condutores\contratos.ts` | Interface TypeScript real `RetornoMODQT` (linhas 50-56) — contrato que **não pode ser quebrado** |
| 5 | `sistema-de-instala-es-el-tricas-sie-main\src\api\schemas\otimizar-condutor.schema.ts` | Schema Zod real `RetornoMODQTSchema` (linhas 74-93) — validação de runtime já em produção |
| 6 | `sistema-de-instala-es-el-tricas-sie-main\src\routes\api\v1\modulos.mod-qt.validar.ts` | Endpoint de integração já existente, hoje servido por um **mock** (`validarModQTMock`, linha 102) que será substituído pelo motor real |
| 7 | `docs\stories\MOD-QT-1-refined.md` | Story já concluída (Done) que implementou apenas o contrato/endpoint/mock — mostra o que **já está pronto** e não deve ser duplicado |
| 8 | `Arquivos_Diversos\NBR_5410_original\NBR-5410.md` | Texto integral da NBR 5410:2004 — fonte primária para resolver os itens `[VERIFICAR]` de limite normativo (seção 6.2.7, linhas ~10144-10178) |
| 9 | `Arquivos_Diversos\NBR_5410_comentada\markdown_limpo_16_pdfs\06_dimensionamento_markdown_limpo.md` | Fonte explicativa (Guia EM) — **use com a mesma cautela do `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` §8, item 3**: numeração de tabelas da edição 1997, não copiar números de tabela sem converter para a edição 2004 |
| 10 | `sistema-de-instala-es-el-tricas-sie-main\src\domain\calculo\geometria.ts` (ou equivalente) e `sistema-de-instala-es-el-tricas-sie-main\src\domain\unifilar\unifilar-graph.ts` | Prova de que **não existe** hoje nenhum campo de coordenadas espaciais (x, y) de cômodo/quadro no sistema — usado para decidir o tratamento da seção 5.2 do documento-fonte |

---

## 7. ACHADOS QUE MOTIVAM ESTE AJUSTE (não reabra a investigação — use estes achados como ponto de partida)

### 7.1 Divergência de nomes de campo (bloqueante, resolver na seção 14 do novo documento)

O documento-fonte define `ResultadoQuedaTensao` com campos como `delta_v_circuito_pct`, `conforme_circuito`, `limite_circuito_pct`. O contrato real já implementado e consumido pelo MOD-DC é `RetornoMODQT`:

```typescript
interface RetornoMODQT {
  readonly atende: boolean;
  readonly queda_percentual: number;
  readonly limite_aplicado: number;
  readonly secao_requerida_mm2?: number | null;
  readonly fonte: string;
}
```

e o request esperado pelo endpoint `/api/v1/modulos/mod-qt/validar` é:

```typescript
{ dependencia_id: string (uuid), corrente_a: number, comprimento_m: number,
  secao_mm2: number, limite_percentual: number, origem: string }
```

O novo documento deve **adotar esses nomes como contrato externo obrigatório** do endpoint público, e pode manter os nomes mais descritivos do documento-fonte (`delta_v_circuito_pct` etc.) apenas como **modelo interno** do motor, com uma camada de mapeamento explícita e documentada entre os dois.

### 7.2 Dependência de um "Motor de Geometria" que não existe (bloqueante, resolver na seção 5.2/13 do novo documento)

A seção 5.2 do documento-fonte (`estimar_comprimento_circuito`) pressupõe `posicao_quadro: tuple[float, float]` e `posicao_ponto: tuple[float, float]` — coordenadas espaciais de cômodos. Nenhum módulo do SIE hoje (nem o cálculo de geometria de iluminação, nem o grafo do diagrama unifilar) armazena ou expõe coordenadas x/y de cômodo ou quadro. Implementar essa função como está especificada exigiria um módulo upstream novo, inexistente e fora do escopo de queda de tensão.

### 7.3 Itens `[VERIFICAR]` do documento-fonte — situação real de cada um

| ID original | Item | Situação real após checagem nas fontes locais |
|---|---|---|
| VER-QT-01 | Limites de queda de tensão (4%/7%) | **Já resolvido.** `NBR-5410.md`, seção 6.2.7.1/6.2.7.2 (linhas ~10144-10178): 7% a partir de transformador próprio ou da distribuidora; 5% a partir do ponto de entrega em tensão secundária nos demais casos; 7% a partir de gerador próprio; **circuitos terminais nunca acima de 4%**; nota 3 permite +0,005%/m além de 100 m, limitado a +0,5%. Isto é idêntico ao que o PRD-MOD-DC §12.6 já usa — **não há divergência a verificar**, apenas transcrever com a citação correta. |
| VER-QT-02 | Resistência por seção (Cu/Al, 70 °C/90 °C) | Permanece `[VERIFICAR]` — não consta na NBR 5410 nem nos anexos locais do projeto. **Corrigir a fonte citada:** o documento-fonte cita "NBR 5410 Anexo G", mas o Anexo G da NBR 5410:2004 trata de **equipotencialização principal**, não de impedância de condutores — essa citação está errada e deve ser removida. Fonte real a buscar: catálogos de fabricante (Prysmian/Nexans) ou IEC 60364-5-52, explicitamente fora dos anexos disponíveis ao projeto hoje. |
| VER-QT-03 | Reatância indutiva por seção | Mesma situação de VER-QT-02: `[VERIFICAR]`, mesma correção de fonte (não é Anexo G). |
| VER-QT-04 | Fórmula bifásico (fator 2 vs √3) | Permanece `[VERIFICAR]` — não há trecho localizado nos anexos que resolva isso; manter como pendência explícita, sem assumir. |
| VER-QT-05 | Temperatura de referência (70 °C PVC / 90 °C EPR-XLPE) | Estas temperaturas **coincidem** com a Tabela 35 já transcrita e confirmada em `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` §12.3 (chunk 117): PVC ≤ 300 mm² → 70/100/160 °C; EPR/XLPE → 90/130/250 °C (a primeira coluna é a temperatura de serviço contínuo). Pode ser citado como **CONFIRMADO por reaproveitamento** do MOD-DC, com a mesma fonte. |
| VER-QT-06 | Alturas padronizadas de tomada (0,30/1,10/2,00 m) | Permanece `[VERIFICAR]` — são valores de prática de projeto, não localizados como obrigação normativa nos anexos disponíveis; manter como parâmetro configurável, não normativo. |

### 7.4 O mock atual já em produção é menos completo que o motor v2 do documento-fonte

O mock hoje aceita apenas monofásico, cobre, 220 V fixo, sem reatância (`RHO_COBRE = 0.0172`, `TENSAO_REF_V = 220` hardcoded em `modulos.mod-qt.validar.ts`). O motor completo do documento-fonte (trifásico, Cu/Al, método completo com reatância) é estritamente uma evolução — não há conflito aqui, apenas a necessidade de o novo documento deixar explícito que ele **substitui** `validarModQTMock` mantendo o mesmo endpoint e V.

---

## 8. FONTES E LIMITES DE CONHECIMENTO (aplicar a mesma disciplina do §8/§9 do `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`)

1. Hierarquia de fontes, da mais para a menos autoritativa:
   1. `NBR-5410.md` / `NBR_5410_chunks.json` — ABNT NBR 5410:2004 (texto integral local).
   2. `contratos.ts` / `otimizar-condutor.schema.ts` / `modulos.mod-qt.validar.ts` — contrato **já em produção**, tratado como requisito não negociável de compatibilidade (não é fonte normativa, é restrição de engenharia).
   3. `PRD-MOD-DC-modulo-dimensionamento-condutores.md` — fonte da regra de negócio de integração C5.
   4. `06_dimensionamento_markdown_limpo.md` (Guia EM) — fonte explicativa; **proibido copiar numeração de tabela da edição 1997 sem converter**.
   5. `PROMPT-QUEDA-TENSAO-v2.md` (documento-fonte original) — **não é fonte normativa**; suas fórmulas e valores só valem quando confirmados pelas fontes acima.
2. É proibido: consultar internet; inventar valores de resistência/reatância; assumir fórmula do bifásico sem fonte; inventar coordenadas espaciais de cômodo.
3. Toda lacuna normativa vira `[VERIFICAR — fonte necessária: X]`, nunca um valor "razoável" ou "típico" sem marcação.

---

## 9. PASSO A PASSO OBRIGATÓRIO

Execute os passos nesta ordem. Não pule etapas. Não produza o arquivo final antes de completar 9.1–9.8.

### 9.1 — Leia todas as 10 entradas da seção 6 integralmente

Não resuma por amostragem. O contrato de `contratos.ts` e o schema de `otimizar-condutor.schema.ts` devem ser lidos byte a byte — qualquer divergência de nome de campo entre o documento ajustado e esses dois arquivos é um defeito bloqueante da sua entrega.

### 9.2 — Extraia a estrutura de 31 seções do template

Liste, a partir de `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`, os títulos exatos das 31 seções (use `grep "^## "` mentalmente ou releia o índice). Mapeie cada conteúdo do `PROMPT-QUEDA-TENSAO-v2.md` original para a seção correspondente do template. Onde o original não tiver conteúdo equivalente (ex.: não há seção de "Acessibilidade" nem "Segurança e responsabilidade técnica" no original), você deve **criar a seção com conteúdo mínimo aplicável ao MOD-QT** ou marcá-la explicitamente como `HERDADO DO MOD-DC — sem alteração` quando a regra já é genérica do sistema (ex.: R-05 Design System, R-09 Nada aprovado por arredondamento).

### 9.3 — Reescreva a seção 5 (objetivo) e 6/7 (escopo/fora de escopo) removendo a estimativa de comprimento por geometria do caminho crítico

A estimativa automática via `estimar_comprimento_circuito` (documento-fonte, seção 5.2) deve ser movida para uma seção "FORA DE ESCOPO — trabalho futuro, depende de Motor de Geometria (inexistente)", citando explicitamente o achado do item 7.2 deste prompt. O comprimento manual informado pelo projetista (`comprimento_m`, já presente no contrato real) permanece como único caminho suportado nesta versão.

### 9.4 — Reescreva a seção de contratos de entrada/saída (equivalente à seção 14 do template) usando os nomes reais

- O contrato de **request/response do endpoint público** deve usar exatamente os nomes de `ValidarMODQTSchema` e `RetornoMODQTSchema` (seção 6 deste prompt, entradas 4 e 5).
- Modelos internos do motor (com nomes mais descritivos, se desejado) devem ser explicitamente rotulados como "modelo interno — mapeado para o contrato público na camada de API", com uma tabela de correspondência campo a campo.
- Preserve o campo opcional `secao_requerida_mm2`, que hoje já dispara o laço de revalidação C1/C2/C6 no MOD-DC (`servico-dimensionamento-condutores.ts`) — este é o mecanismo mais crítico de acoplamento e não pode ser renomeado nem removido.

### 9.5 — Reescreva a seção normativa (equivalente à seção 12 do template) aplicando a tabela do item 7.3 deste prompt

Para cada item da tabela em 7.3: se "já resolvido", promova para `CONFIRMADO` com a citação exata (arquivo + linha/seção); se "permanece [VERIFICAR]", mantenha a marcação, mas corrija a fonte citada quando estiver errada (caso do "Anexo G").

### 9.6 — Adicione uma seção de "CORREÇÃO SOBRE A v2.0" (siga o estilo do template, ex.: linha 35 e 149 do `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`)

Registre de forma explícita, como nota de rastreabilidade (não apagar a história da decisão):
1. Contrato de saída renomeado para compatibilidade com `RetornoMODQT` já em produção.
2. Estimativa de comprimento via geometria removida do escopo desta versão por dependência inexistente.
3. Citação de fonte de resistência/reatância corrigida (não é Anexo G).
4. Limites 4%/7%/5% promovidos de `[VERIFICAR]` para `CONFIRMADO`.

### 9.7 — Escreva critérios de aceite testáveis (equivalente à seção 25 do template)

Reaproveite os `CA-QT-01` a `CA-QT-16` do documento-fonte, mas:
- ajuste todo nome de campo testado para o contrato real (`atende`, `queda_percentual`, `limite_aplicado`, `secao_requerida_mm2`, `fonte`);
- remova ou marque como `FORA DE ESCOPO` os critérios que dependem da estimativa de geometria (ex.: CA-QT-08);
- adicione um critério de **não regressão do mock**: toda entrada que hoje passa pelo mock (`validarModQTMock`) deve produzir resultado equivalente ou mais preciso com o motor novo, nunca uma reprovação onde antes havia aprovação sem uma causa normativa nova e documentada.

### 9.8 — Preencha a seção final "PENDÊNCIAS [VERIFICAR]" (equivalente à seção 28 do template) com a lista final e definitiva

Deve conter, no mínimo: VER-QT-02, VER-QT-03, VER-QT-04, VER-QT-06 (ver item 7.3), cada um com fonte necessária declarada, igual ao padrão do template (`[VERIFICAR — motivo]`).

---

## 10. FORMATO DE SAÍDA ESPERADO

1. Um único arquivo `PROMPT-QUEDA-TENSAO-v2.1.md`, salvo em `Arquivos_Diversos\` (mesma pasta do documento-fonte original, ao lado de `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`), com a estrutura de 31 seções do template.
2. Não decida por conta própria alterar limites normativos, fórmulas ou nomes de campo além do que este prompt autoriza — qualquer decisão de engenharia não coberta aqui deve virar uma pergunta explícita na seção final do documento, não uma suposição silenciosa.
3. Não implemente código nesta tarefa. A saída é exclusivamente o documento `.md` ajustado.

## 11. CHECKLIST DE ENTREGA (verifique antes de finalizar)

- [ ] Todas as 10 entradas da seção 6 foram lidas por completo
- [ ] O contrato de request/response do endpoint usa exatamente os nomes de `ValidarMODQTSchema`/`RetornoMODQTSchema`
- [ ] Nenhuma seção do documento final depende de coordenadas espaciais de cômodo como caminho obrigatório
- [ ] Todo item `[VERIFICAR]` do original foi resolvido, corrigido de fonte, ou mantido com justificativa — nenhum foi silenciosamente removido
- [ ] A citação "Anexo G" para tabelas de impedância foi removida/corrigida
- [ ] Os limites 4%/7%/5% aparecem como `CONFIRMADO` com citação de `NBR-5410.md`
- [ ] Existe uma seção "CORREÇÃO SOBRE A v2.0" nos moldes do template
- [ ] Os 31 títulos de seção do template estão presentes (mesmo que com conteúdo "não aplicável ao MOD-QT")
- [ ] Nenhum valor normativo novo foi inventado

## 12. CRITÉRIO DE ACEITE DESTE AJUSTE

O ajuste está pronto para ser incorporado ao sistema quando, e somente quando, `@architect` ou `@pm` do AIOX conseguir ler `PROMPT-QUEDA-TENSAO-v2.1.md` e abrir diretamente uma story de épico `MOD-QT-2` sem precisar voltar a este documento nem ao documento-fonte original para esclarecer nome de campo, fonte normativa ou escopo.

## 13. INSTRUÇÕES FINAIS

Trabalhe com rigor e objetividade. Não amplie o escopo do MOD-QT além do que o documento-fonte já propunha, exceto pelas remoções e correções explicitamente autorizadas neste prompt. Cite arquivo e linha (ou seção normativa) para toda afirmação de fato. Quando não tiver certeza, marque `[VERIFICAR]` — nunca complete a lacuna com um valor plausível.
