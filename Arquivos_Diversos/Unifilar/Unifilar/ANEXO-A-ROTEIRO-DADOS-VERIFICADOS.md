# ANEXO A — ROTEIRO-CAMADA-B · Dados Verificados do proj-1 e Conflitos Pendentes
**Fonte:** SIE-REFERENCIA-COMPLETA.md (dados extraídos de gravações reais de tela — tratados como verificados)
**Uso:** colocar este arquivo ao lado do ROTEIRO-CAMADA-B.md na raiz do repositório. A LLM de terminal
DEVE ler este anexo durante E0 e usar os valores da Seção A2 como alvos de aceite nas etapas E1–E5.

---

## A1 — RELATÓRIO E0 PRELIMINAR (executado em chat, parcial)

```
=== RELATÓRIO E0 (PARCIAL — executado via documento de referência, sem acesso ao repositório) ===
Coberto pela referência:
  - Mapeamento campo observado em tela → campo PontoCarga (Seção A3)
  - Alvos numéricos de aceite E1/E5 (Seção A2)
  - Dados reais das Tabelas 001/002 para o E5 (Seção A4)
Pendente de repositório (a LLM de terminal completa no E0 real):
  - Local de registro dos routers FastAPI
  - Nomes reais de tabelas/colunas SQLAlchemy (a Seção A3 mapeia CONCEITOS de tela,
    não colunas — validar nomes com grep antes do E1)
  - Estrutura de pastas do frontend + versão do Carbon + padrão de fetch
  - Existência de infra Node para E4 (PDF)
Critérios: E0-A1 pendente (rodar pytest no repo) · E0-A2 PARCIAL (Seção A3) · E0-A3 n/a
[VERIFICAR] novos: nenhum — CONF-01/02/03 decididos pelo operador em 08/07/2026 (Seção A5)
```

---

## A2 — ALVOS NUMÉRICOS DE ACEITE (proj-1, verificados contra tela)

| Alvo | Valor verificado | Onde é usado no roteiro |
|---|---|---|
| Total de circuitos (adaptador 1:1) | **44** | E1-A1, E2-A1, UF-01 |
| Total de dependências | 14 | sanidade do loader |
| Soma de va_total do payload | **≈ 57.677 VA** (20.223 + 18.702 + 18.752; tela mostra 57,68 kVA) | **E1-A2** |
| Corrente de demanda ID | 94,41 A | Trifilar E5 (contexto T4) |
| Categoria/Subcategoria | T / **T4** — teto 100 A, condutor 25 mm² | E5 |
| Sistema | Trifásico estrela 220/127 V | loader (tensões válidas: 127/220) |
| Maior IB individual | 34,65 A (ADD-Banheiro-2-Chuveiro-2, 4.400 VA / 127 V) | sanidade E1 |
| Balanceamento por fase | A: 20.223 VA · B: 18.702 VA · C: 18.752 VA · deseq. 0,08% | sanidade E1 (Camada A futura) |
| Demanda D_A / D_B / D_T | 30.475 / 5.500 / 35.975 VA | Trifilar E5 (rótulos de contexto) |
| Diagnóstico global vigente | ERR-DIMENSIONAMENTO-PENDENTE (bloqueia P1 — reforça placeholders de E6) | E6 |

**Instrução:** se E1 retornar soma de VA ≠ ~57.677 VA ou ≠ 44 circuitos, é divergência a
INVESTIGAR e reportar — não ajustar o loader para "bater" o número.

---

## A3 — MAPEAMENTO CONCEITUAL: tela/domínio → PontoCarga (validar nomes de coluna no E0 real)

| Campo PontoCarga | Origem observada no sistema real | Nota |
|---|---|---|
| `id` | id do "circuito" 1:1 da tela Correntes (ex.: `ILUM-Dormitorio-1`, `ADD-Banheiro-2-Chuveiro-2`) | ver CONF-02 |
| `descricao` | nome da carga (LED, Chuveiro, Exaustor…) ou rótulo do ponto | |
| `tipo` | `tipo` do card (iluminacao/tug/tue) + categoria de carga adicional (`outra`) | |
| `dependencia_id` | `dep-*` / slug da dependência servida | |
| `va` | `potência_total` (VA) do circuito 1:1 — VA direto (INC-01) | |
| `tensao_v` | `tensão_resolvida` SOMENTE quando declarada/confirmada; automática sem confirmação → **None** | ver CONF-03 |
| `corrente_ib_a` | `IB` persistido pelo módulo IB (rastreio `IB = S / V`) — nunca recalcular no loader | |
| `fases` | `balanceamento` (letra A/B/C) + `ligação` (mono→1, bifásico→2, trifásico→3) | ver CONF-01 |
| `grupo_edp` | grupo (a–i) herdado da carga | tela usa minúsculas; contrato usa A–I — normalizar no loader |
| `zona_molhada` | conformidade da dependência: `zona_banheiro`/`zona_piscina` classificadas → True; "Não se aplica" → False; ausente → **None** (INC-03) | |

---

## A4 — DADOS PARA O E5 (Trifilar): Sub-categorias 001/002 verificadas em tela

Status de todas as linhas: **VERIFICADO** · Fonte: "EDP-SP PT.DT.PDN.00068 v09 (anexo local, carregado no sistema)"

| Sub-cat | Categoria | I máx (A) | Disjuntor (A) | Seção (mm²) |
|---|---|---|---|---|
| U2 | U | 70 | 70 | distribuidora |
| D2 | D | 63 | 63 | distribuidora |
| D4 | D | 100 | 100 | 25 |
| D6 | D | 150 | 150 | 50 |
| D7 | D | 200 | 200 | 70 |
| D9 | D | 300 | 300 | 120 |
| D10 | D | 350 | 350 | 185 |
| T2 | T | 63 | 63 | distribuidora |
| T4 | T | 100 | 100 | 25 |
| T6 | T | 150 | 150 | 50 |
| T7 | T | 200 | 200 | 70 |
| T9 | T | 300 | 300 | 120 |
| T10 | T | 350 | 350 | 185 |

**Instrução para E5:** o sistema JÁ possui essas tabelas carregadas e editáveis
(aba "Sub-categorias 001/002" dos Parâmetros EDP). O endpoint de E5 deve LER a
tabela persistida do projeto (respeitando edições do projetista, badge "Modificado"),
não duplicar este anexo em novo JSON. Este anexo serve como fixture de teste e
verificação cruzada. Teto de categoria: DT > 75.000 VA **ou** ID > 350 A (correção
já incorporada — não reabrir).

---

## A5 — CONFLITOS — **DECIDIDOS PELO OPERADOR EM 08/07/2026** (registro; não reabrir sem justificativa nova)

### CONF-01 — Convenção de fases: A/B/C (sistema real) vs. R/S/T (PRD + contrato entregue)
As telas de Correntes/IB usam fases **A/B/C** (`N+A`, `A+B`); o PRD e o enum `Fase`
do contrato entregue usam **R/S/T**. Alternativas:
- **(a)** Adotar A/B/C como convenção oficial: alterar enum do contrato + rótulo do
  `SymBarramento` + bloco DXF (RG-06) ANTES do E1. Prós: coerência com o sistema em
  produção, loader trivial. Contras: diverge do texto do PRD (atualizar PRD).
- **(b)** Manter R/S/T no contrato e mapear A→R, B→S, C→T no loader. Prós: PRD intacto.
  Contras: duas convenções vivas no produto; equivalência A=R não confirmada em norma.
**DECIDIDO: alternativa (b) — R/S/T é a convenção oficial do contrato/PRD; o loader converte A→R, B→S, C→T via `mapear_fase_abc_para_rst` (adaptador_1x1.py). Teste T7 cobre o mapeamento.**

### CONF-02 — Prefixos de id: sistema usa ILUM-/TUG-/ADD-; adaptador entregue gera ILUM-/TUG-/TUE-/OUTRA-
No sistema real, cargas adicionais viram `ADD-<dep>-<carga>`. Alternativas:
- **(a)** Loader preserva o id REAL do circuito 1:1 vindo do banco (recomendado: o
  adaptador só usa seu gerador de id quando o ponto não traz id) — nenhum id inventado,
  rastreabilidade direta com a tela.
- **(b)** Re-rotular tudo no padrão do adaptador. Contras: quebra rastreio visual
  usuário↔tela↔diagrama.
**DECIDIDO: alternativa (a) — o id do circuito é o id real do banco; adaptador atualizado (não gera mais ids). Teste T8 cobre a preservação.**

### CONF-03 — Semântica de `tensão_resolvida` "Automática" vs. INC-04
A tela Saída A admite default 127 V para ILU/TUG (com aviso de que TUE deve declarar).
O contrato trata `tensao_v=None` como pendência. Questão: para ILU/TUG com tensão
"Automática" (127 V do contrato de integração), o loader deve (a) passar 127 V com
`fonte_linha` apontando a Saída A (tensão é resolvida por contrato de integração,
não fallback silencioso — INC-04 preservada), ou (b) passar None e marcar tudo
ATENÇÃO (44 circuitos quase todos pendentes — ruído)? Recomendação técnica: (a) para
ILU/TUG, (b) permanece obrigatório para TUE sem tensaoFixa.
**DECIDIDO: sugestão aceita — ILU/TUG com tensão da Saída A entram com 127 V + fonte_linha rastreável (status INFO); TUE/outra sem tensaoFixa => None + ATENÇÃO, e o adaptador REJEITA TUE marcada como resolvida por contrato (guarda INC-04). Campo novo `tensao_resolvida_por_contrato` em PontoCarga. Testes T9/T10.**

---

## A6 — DECISÕES FECHADAS (Seção 15 da referência — a LLM de terminal NÃO reabre)
Não modificar o IB · jusante contra o contrato antes da Divisão · SVG próprio (sem
React Flow/GoJS) · IEC 60617 (NBR 5444 cancelada) · arquitetura híbrida Fable + SVG.
