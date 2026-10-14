# PEDIDO DE COMPLEMENTO — EXTRAÇÃO LITERAL DE Rca E XL (VER-QT-02 / VER-QT-03)

**Identificador:** MOD-QT-2-COMPLEMENTO-EXTRACAO-v1.0
**Destinatário:** LLM externa com acesso web (mesma que produziu a resolução de 2026-07-28, ou sessão nova)
**Antecedente:** `RESOLUCAO-VER-QT-MOD-QT-2` de 2026-07-28
**Data:** 2026-07-28
**Natureza:** tarefa única de extração de dados. **Não é** pedido de análise, arquitetura ou recomendação.

---

## 1. O QUE JÁ FOI ACEITO — NÃO REFAZER

Sua entrega anterior foi auditada. Os seguintes pontos foram **verificados de forma independente e aceitos**; não os revisite:

| Item | Situação |
|---|---|
| VER-QT-04 — fator 2 no circuito bifásico, tensão fase-fase no percentual | **ACEITO.** Fonte: Guia Prysmian Rev. 9, §6.2, p. 20 |
| VER-QT-06 — alturas de tomada não são prescrição normativa | **ACEITO.** Fonte: NBR 5410:2004 §9.5.2.2.1 |
| VER-QT-07 — alínea c → limite total 5 % para EDP-SP | **ACEITO.** Cadeia reconfirmada por leitura direta dos textos literais |
| Identificação da fonte de impedância (Prysmian Rev. 9, tabelas 29–35, 60 Hz, `Rca`/`XL` pareados) | **ACEITO** como localização correta |
| Transcrição da tabela 18 (`Rdc20`, classe 2, Cu e Al) | **ACEITO.** Aprovada em quatro testes de coerência relacional |

**Sua recusa em declarar antecipadamente a nova razão do gate de não-regressão foi considerada correta.** Não a declare agora tampouco.

---

## 2. O QUE FALTA — E POR QUE ESTA TAREFA EXISTE

Sua entrega classificou VER-QT-02 e VER-QT-03 como RESOLVIDO. A auditoria os **rebaixou a PARCIAL** pelo seguinte motivo, que não é uma discordância de mérito:

> A entrega identificou a fonte, qualificou a chave de seleção e definiu regras de importação — mas **não contém uma única célula de `Rca` ou `XL`**. A tabela 18 transcrita é `Rdc20` (corrente contínua, 20 °C), que a própria entrega declara, corretamente, não ser substituta de `Rca`. Os valores que o motor de cálculo efetivamente consome continuam ausentes.

Você resolveu o **método**. Falta o **dado**.

**Esta tarefa tem um único objetivo:** transcrever literalmente as tabelas 29 a 35 do Guia Prysmian Rev. 9 (pp. 34–41), produzindo os pares `Rca` / `XL` com toda a qualificação necessária para que cada célula seja rastreável e não ambígua.

---

## 3. ESCOPO — O QUE ESTÁ FORA

Não inclua nesta entrega:

- ❌ Proposta de arquitetura, modelo de dados ou fluxo de validação. A proposta de "Ficha Técnica de Linha" da entrega anterior foi **escalada para decisão de arquitetura do projeto** e está fora do seu escopo. Não a desenvolva, não a defenda, não a assuma como decidida.
- ❌ Plano de correção de código. Já existe.
- ❌ Reanálise de VER-QT-04, VER-QT-06 ou VER-QT-07.
- ❌ Recomendações sobre bloquear ou não cálculos sem dados.
- ❌ Qualquer valor que não venha literalmente de uma célula publicada.

Se você identificar algo relevante fora deste escopo, registre em uma seção final de observações, em no máximo cinco linhas. Não deixe isso ocupar a entrega.

---

## 4. DOCUMENTO-ALVO

| Campo | Valor |
|---|---|
| Título | Guia de Dimensionamento de Cabos para Baixa Tensão |
| Editor | Prysmian Brasil |
| Revisão | Rev. 9 |
| URL declarada na entrega anterior | `https://br.prysmian.com/sites/default/files/atoms/files/Guia_de_Dimensionamento-Baixa_Tensao_Rev9.pdf` |
| Alvo | **Tabelas 29 a 35, pp. 34–41** |
| Âncoras já validadas | §6.2 p. 20 (fórmulas); §6.3 e tabela 18 p. 21 (`Rdc20` e correção térmica); §6.4 p. 22 |

Se a URL não responder, busque o documento por título + revisão no site oficial da Prysmian Brasil. **Se você não conseguir abrir o PDF, vá direto para a §9 deste pedido.** Não reconstrua as tabelas de memória, de outra revisão, de outro fabricante ou de fonte secundária.

---

## 5. O QUE EXTRAIR — UMA LINHA POR CÉLULA PUBLICADA

Para **cada** célula publicada nas tabelas 29–35, produza um registro com os campos abaixo. Campos que a tabela não publicar recebem `null` — nunca um valor inferido.

| Campo | Tipo | Regra |
|---|---|---|
| `tabela` | inteiro | 29 a 35 |
| `pagina` | inteiro | página impressa onde a célula aparece |
| `familia_cabo` | string | **rótulo literal** do título da tabela (nome comercial do produto) |
| `material` | `"CU"` \| `"AL"` | conforme publicado |
| `classe_condutor` | string \| null | classe de encordoamento, se a tabela declarar |
| `isolacao` | string | rótulo literal (ex.: PVC, EPR, XLPE, HEPR) |
| `temperatura_servico_c` | número | temperatura de operação declarada pela tabela (tipicamente 70 ou 90) |
| `formacao` | string | unipolar, multipolar, ou o rótulo literal publicado |
| `arranjo_publicado` | string | rótulo literal da coluna/desenho (ex.: trifólio, justaposto, multicondutor) |
| `espacamento_publicado` | string \| null | rótulo literal (ex.: `s = 2D`, `13 cm`, `20 cm`) |
| `secao_mm2` | número | linha literal da tabela |
| `r_ca_ohm_km` | número \| null | `Rca` na temperatura de operação, conforme publicado |
| `x_l_ohm_km` | número \| null | `XL` a 60 Hz, conforme publicado |
| `frequencia_hz` | número | confirme que é 60; se a tabela declarar outra, registre a real |
| `rotulo_coluna_origem` | string | texto literal do cabeçalho da coluna de onde o número foi lido |
| `observacoes_da_tabela` | string \| null | notas de rodapé, exclusões, condições de validade |

**Regra de precisão numérica:** transcreva o número exatamente como impresso, incluindo todas as casas decimais. Não arredonde, não normalize separador decimal para "melhorar" a leitura, não converta unidade.

**Regra de cobertura:** extraia **todas** as linhas e **todas** as colunas geométricas de cada tabela. Não selecione "as mais usadas". Se uma tabela tiver 4 colunas de arranjo × 15 seções, isso são 60 registros, não 15.

---

## 6. ÂNCORA DE VERIFICAÇÃO — CONFIRME QUE ESTÁ NO MESMO DOCUMENTO

Antes de extrair as tabelas 29–35, abra a **tabela 18, p. 21**, e confirme que os valores abaixo (transcritos por você anteriormente e já auditados) conferem com o que você está lendo agora:

| Seção mm² | Cu classe 2 `Rdc20` | Al classe 2 `Rdc20` |
|---:|---:|---:|
| 1,5 | 12,1000 | não publicado |
| 2,5 | 7,4100 | não publicado |
| 4 | 4,6100 | não publicado |
| 6 | 3,0800 | não publicado |
| 10 | 1,8300 | não publicado |
| 16 | 1,1500 | 1,9100 |
| 25 | 0,7270 | 1,2000 |
| 35 | 0,5240 | 0,8680 |
| 50 | 0,3870 | 0,6410 |
| 70 | 0,2680 | 0,4430 |
| 95 | 0,1930 | 0,3200 |
| 120 | 0,1530 | 0,2530 |
| 150 | 0,1240 | 0,2060 |
| 185 | 0,0991 | 0,1640 |
| 240 | 0,0754 | 0,1250 |
| 300 | 0,0601 | 0,1000 |
| 400 | 0,0470 | 0,0778 |
| 500 | 0,0366 | 0,0605 |

**Se algum valor divergir**, pare e reporte: significa que você está em outra revisão do documento, e toda a extração seria de uma edição diferente da que sustenta o restante da resolução. Isso é um resultado válido e importante — reporte-o em vez de prosseguir.

---

## 7. FORMATO DE SAÍDA

Entregue **dois artefatos** na mesma resposta.

### 7.1 Artefato A — dados (obrigatório)

Bloco de código JSON único, nomeado `impedancia-prysmian-bt-rev9.json`:

```json
{
  "fonte": {
    "documento": "Guia de Dimensionamento de Cabos para Baixa Tensão",
    "editor": "Prysmian Brasil",
    "revisao": "Rev. 9",
    "url": "...",
    "data_acesso": "AAAA-MM-DD",
    "paginas_extraidas": [34, 35, 36, 37, 38, 39, 40, 41],
    "frequencia_hz": 60,
    "ancora_tabela_18_conferida": true
  },
  "cobertura": {
    "tabelas_encontradas": [29, 30, 31, 32, 33, 34, 35],
    "tabelas_nao_localizadas": [],
    "celulas_publicadas_contadas": 0,
    "celulas_extraidas": 0,
    "celulas_ilegiveis": 0
  },
  "registros": [
    {
      "tabela": 29,
      "pagina": 34,
      "familia_cabo": "...",
      "material": "CU",
      "classe_condutor": "2",
      "isolacao": "PVC",
      "temperatura_servico_c": 70,
      "formacao": "unipolar",
      "arranjo_publicado": "...",
      "espacamento_publicado": "...",
      "secao_mm2": 2.5,
      "r_ca_ohm_km": null,
      "x_l_ohm_km": null,
      "frequencia_hz": 60,
      "rotulo_coluna_origem": "...",
      "observacoes_da_tabela": null
    }
  ]
}
```

`celulas_publicadas_contadas` e `celulas_extraidas` **devem ser iguais**. Se não forem, explique a diferença no Artefato B.

### 7.2 Artefato B — relatório de extração (obrigatório)

Markdown curto com:

1. **Inventário das tabelas** — uma linha por tabela: número, página, família, materiais, faixa de seções, colunas geométricas encontradas, nº de registros extraídos.
2. **Resultado dos testes de coerência** (§8) — tabela com o valor apurado e verdito de cada teste.
3. **Anomalias** — células ilegíveis, notas de rodapé restritivas, exclusões declaradas pelo fabricante, colunas ambíguas.
4. **Observações fora de escopo** — máximo cinco linhas.

---

## 8. TESTES DE COERÊNCIA — VOCÊ DEVE RODAR E REPORTAR

Estes testes serão reexecutados na auditoria. Rode-os antes de entregar e reporte os valores apurados, mesmo que algum falhe. **Um teste que falha e é reportado é aceitável; um teste falho e omitido invalida a entrega.**

| # | Teste | Comportamento esperado |
|---|---|---|
| T1 | `Rca × secao_mm2` dentro de uma mesma família/isolação/temperatura | aproximadamente constante ao longo das seções |
| T2 | `Rca(Al) / Rca(Cu)` na mesma seção, mesma condição | aproximadamente constante em toda a faixa |
| T3 | `Rca(70 °C) / Rdc20` da tabela 18, mesma seção e classe | **≥ 1,19** (efeito da temperatura conforme §6.3) e **crescente com a seção** (efeito pelicular). Reporte a razão por seção |
| T4 | `Rca(90 °C) / Rca(70 °C)` mesma seção | aproximadamente constante e > 1 |
| T5 | `XL` ao longo das seções, mesma coluna geométrica | variação suave, sem saltos; valores tipicamente na ordem de centésimos a décimos de Ω/km |
| T6 | `XL` entre colunas geométricas diferentes, mesma seção | deve **diferir** — se for idêntico entre arranjos, a leitura de coluna está errada |
| T7 | Monotonicidade | `Rca` estritamente decrescente com o aumento da seção |

T3 é o teste mais importante: ele amarra as tabelas 29–35 à tabela 18 já auditada. Se T3 falhar, provavelmente há troca de coluna, de classe ou de temperatura na leitura.

---

## 9. SE VOCÊ NÃO CONSEGUIR ACESSAR O DOCUMENTO

Este é um resultado legítimo e deve ser entregue com a mesma seriedade. Nesse caso, entregue **apenas** o seguinte, sem JSON e sem tabelas:

```markdown
## Falha de acesso — extração não realizada

- **O que foi tentado:** {URLs, termos de busca, portais consultados, literalmente}
- **Resultado de cada tentativa:** {404, paywall, exige cadastro, PDF sem camada de texto, etc.}
- **O documento existe e foi localizado?** {sim/não — e onde}
- **Versão localizada:** {revisão encontrada, se diferente da Rev. 9}
- **Caminho recomendado para obtenção:** {ação concreta: solicitar ao representante comercial, formulário do fabricante, biblioteca técnica, etc.}
- **Alternativas equivalentes identificadas:** {outros catálogos primários que publiquem Rca e XL pareados a 60 Hz — apenas identificar, NÃO extrair sem autorização}
```

**Não** compense a falha de acesso com valores de outra fonte, de outra revisão ou de memória. Não produza uma tabela "provisória". O projeto já tem uma tabela provisória e é exatamente dela que está tentando se livrar.

---

## 10. REGRAS INVIOLÁVEIS (mantidas do pedido original)

1. Nenhum valor sem célula publicada correspondente.
2. Nenhuma interpolação, extrapolação, analogia entre materiais, entre classes, entre formações ou entre arranjos.
3. Conhecimento paramétrico próprio não é fonte. Se você "sabe" o valor, isso é hipótese, não dado.
4. Célula não publicada é `null`, nunca preenchida.
5. Se a tabela for de frequência diferente de 60 Hz, declare — não converta silenciosamente.
6. Não altere nada relativo ao contrato público do sistema (fora do seu escopo nesta tarefa de qualquer modo).
7. Reporte todo teste de coerência que falhar.

---

## 11. CHECKLIST ANTES DE ENTREGAR

- [ ] Âncora da tabela 18 conferida e resultado declarado (§6).
- [ ] Todas as tabelas de 29 a 35 percorridas, ou as ausentes declaradas em `tabelas_nao_localizadas`.
- [ ] Todas as colunas geométricas de cada tabela extraídas, não apenas a primeira.
- [ ] `celulas_publicadas_contadas` == `celulas_extraidas`, ou divergência explicada.
- [ ] Sete testes de coerência rodados e reportados com valores apurados.
- [ ] Nenhuma célula preenchida por inferência.
- [ ] Nenhuma proposta de arquitetura incluída (§3).
- [ ] Números transcritos com as casas decimais originais.

---

**Fim do pedido. Uma única tarefa: transcrever o que está publicado, com rastreabilidade completa, ou declarar que não conseguiu.**
