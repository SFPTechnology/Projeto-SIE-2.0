# Regras, versões e matriz de conferência — F01

**Status: BLOQUEADO PARA CÁLCULO NORMATIVO.** Não confundir metadados editoriais confirmados com valores de tabela confirmados. Versionamento em catálogo não muda resultados de projetos históricos: a persistência de snapshots é tarefa ainda pendente.

## Registro controlado de candidatos

| Rule ID estável | Revisão | Edição informada | Contexto | Data/Transição | Proveniência | Aprovação |
|---|---:|---|---|---|---|---|
| ABNT-NBR-5410 | 1 | 2004, corrigida 2008 | BT; tipo/uso a confirmar | Vigência da norma/cópia a conferir | ABNT Catálogo + NBR derivada no repo | NÃO VERIFICADA |
| ABNT-NBR-5419-1 | 1 | 2026, corrigida 2026 | SPDA, parte 1 | Data aplicável a conferir | ABNT Catálogo | NÃO VERIFICADA |
| ABNT-NBR-5419-2 | 1 | 2026, corrigida 2026 | SPDA, parte 2, gestão de risco | Data aplicável a conferir | ABNT Catálogo | NÃO VERIFICADA |
| ABNT-NBR-5419-3 | 1 | 2026, corrigida 2026 | SPDA, parte 3 | Data aplicável a conferir | ABNT Catálogo | NÃO VERIFICADA |
| ABNT-NBR-5419-4 | 1 | 2026, corrigida 2026 | SPDA, parte 4 | Data aplicável a conferir | ABNT Catálogo | NÃO VERIFICADA |
| NR-10-ATE-2027 | 1 | redação anterior | Segurança em eletricidade | Regra geral até 31/05/2027; verificar regra transitória | MTE oficial | NÃO VERIFICADA |
| NR-10-A-PARTIR-2027 | 1 | Portaria 737/2026 | Segurança em eletricidade | Vigência geral a partir de 01/06/2027; exceções | MTE oficial | NÃO VERIFICADA |
| EDP-SP-PTDT00068-V09 | 1 | v09 local candidata | Padrão de entrada | Localidade/município, concessão, data | PDF SHA-256 F00 | NÃO VERIFICADA |

## Matriz auditável de valores/regras

| ID célula | Fonte documento | Tabela/cláusula | Página | Linha | Coluna | Unidade | Valor | Conferência A | Conferência B | Resultado |
|---|---|---|---|---|---|---|---|---|---|---|
| QT-RCA-* | PDF fonte primária a recuperar | Tabelas 29–35 conforme análise histórica a confirmar | PENDENTE | PENDENTE | PENDENTE | Ω/km | **NÃO IMPORTADO** | — | — | BLOQUEADO |
| QT-XL-* | PDF fonte primária a recuperar | Tabelas 29–35 a conferir | PENDENTE | PENDENTE | PENDENTE | Ω/km | **NÃO IMPORTADO** | — | — | BLOQUEADO |
| COND-IZ-* | NBR 5410 fonte ABNT autorizada | Tabela/coluna/método a estabelecer | PENDENTE | PENDENTE | PENDENTE | A | **NÃO IMPORTADO** | — | — | BLOQUEADO |
| EDP-GRUPOS-* | PT.DT.PDN.00068 v09 oficial/vigência a confirmar | Grupos e tabelas por modalidade | PENDENTE | PENDENTE | PENDENTE | Conforme caso | **NÃO IMPORTADO** | — | — | BLOQUEADO |

**Critério de dupla conferência:** dois registros independentes com identidade funcional/credencial, data, arquivo original, edição, tabela, linha, coluna, notas, unidade, valores e justificativa. Identificador pessoal não é exigido nesta fase sem autorização; registrar papéis dos revisores. Ninguém deve inferir valores de `Rdc20` em lugar de `Rca` ou `XL`.

## Precedência, conflito e histórico

1. Não estabelecer precedência automática entre norma geral, regulamento trabalhista e padrão territorial: escopos distintos podem coexistir.
2. `NAO_APLICAVEL` só reflete triagem de produto contextual e data geral conhecida, não dispensa legal profissional.
3. Se faltar data, localidade, parte normativa, edição, aprovação ou hipótese de utilização, `PENDENTE`/`BLOQUEADO`.
4. Regra incompatível, deprecada ou conflitante não concede aprovação. Alterar revisão cria snapshot novo; resultados anteriores não são recalculados silenciosamente.
5. `ELEGIVEL_PARA_CALCULO` do antigo protótipo isolado **não** era parecer normativo e será substituído pelo gate central da API, que nunca libera normas não homologadas.

## Documentos de proveniência

- Catálogo oficial de normas ABNT: https://www.abntcatalogo.com.br/default.aspx?O=1
- NR-10 oficial (MTE, situação/transição 2026): https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10
- F00: `docs/implantacao-sie-2-0/F00/evidencias/fontes-sha256.json`.
