# C01 — Inventário do legado: evidência atualizada

## Read-back operacional de C01 — 28/10/2026 (corrige o checkpoint anterior)

O banco legado foi localizado no projeto Supabase `Electrical_Project` (organização correspondente à do SIE 2.0). Uma leitura autenticada, sem DDL/DML, confirmou que a estrutura real contém 15 tabelas de domínio, além da tabela de controle de schema. Os registros NÃO estão vazios.

| Tabela | Registros lidos |
|---|---:|
| projetos | 5 |
| dependencias | 41 |
| dependencia_bancadas | 0 |
| dependencia_cargas_adicionais | 52 |
| dependencia_edicoes_manuais | 17 |
| dependencia_validacao | 0 |
| eventos_auditoria | 1805 |
| parametros_edp_overrides | 2 |
| dependencia_retornos_downstream | 0 |
| dimensionamento_condutores_overrides | 2 |
| dimensionamento_condutores_resultado | 3 |
| dimensionamento_disjuntores_overrides | 2 |
| queda_tensao_config | 5 |
| secoes_otimizadas_operacoes | 0 |
| secoes_otimizadas_projeto | 0 |

As verificações SQL de órfãos retornaram 0 para dependências→projetos, cargas→dependências, edições→dependências, auditoria→projetos e overrides EDP→projetos. Na referência histórica auditoria→dependências foram constatados **10 eventos sem ambiente atualmente correspondente**, que devem permanecer preservados/quarentenados até conciliação.

`auth.users` do legado está vazio e `public.projetos` não possui `owner_id`; o destino SIE 2.0 também estava sem usuários Auth no read-back. Portanto o inventário da **origem está comprovado**, mas a **titularidade dos projetos NÃO está comprovada**. Uma matrícula/texto de autor não substitui usuário autenticado. Nenhuma importação ou mapeamento de proprietário real está autorizado automaticamente.

**C01: SOURCE_FOUND_COUNTS_VERIFIED.** **C07 real: HUMAN_REQUIRED (owner mapping + 10 referências históricas + backup, staging e reconciliação).** Nunca adotar `NO_LEGACY_DATA`. Este read-back não constitui exportação, snapshot imutável de corte, verificação de backup ou autorização para escrever no destino.

---

## Levantamento inicial, mantido para rastreabilidade

# C01 — Inventário e decisão da fonte legada (28/10/2026)

## Origem examinada — somente leitura
- `SFPTechnology/sistema-de-instala-es-el-tricas-sie` (private, main): `docs/supabase/0001_init.sql`, `0002_add_trifasica.sql`, `SCHEMA.md`, modelo `src/domain/modelo/dependencia.ts` e `projeto.ts`.
- `SFPTechnology/Projeto-SIE` (private, master): repositório confirmado; nenhuma alteração realizada.
- `SFPTechnology/Projeto-SIE-2.0` (branch B aprovada): fonte nova GF02/B, não base legada de produção.

## Estrutura conhecida — NÃO é volume de dados
| Tabela legada | Papel | Registros reais verificados |
|---|---|---|
| projetos | projeto agregado, id texto, sem owner Auth | **NÃO MEDIDO** |
| dependencias | salas, estado, versões, resultado legado | **NÃO MEDIDO** |
| dependencia_bancadas | bancadas ordenadas | **NÃO MEDIDO** |
| dependencia_cargas_adicionais | cargas e trifásico | **NÃO MEDIDO** |
| dependencia_edicoes_manuais | overrides e autoria textual | **NÃO MEDIDO** |
| dependencia_validacao | validação em esquema legado | **NÃO MEDIDO** |
| eventos_auditoria | eventos com referências texto opcionais | **NÃO MEDIDO** |
| parametros_edp_overrides | parametrização arbitrada em JSON legado | **NÃO MEDIDO** |

## Decisão e condições de acesso
**LEGACY_SOURCE_UNVERIFIED / ETL_REAL_BLOCKED.** O SQL demonstra oito tabelas e o modelo de acesso `service_role` server-only, sem Auth individual de usuário final; **não** comprova que as tabelas foram criadas na instância operacional, contém registros nem qual titular é legítimo. Nenhum dump, credencial, conexão ou recorte identificado neste checkpoint. É proibido declarar `NO_LEGACY_DATA`, fabricar contagens, atribuir owner arbitrário, tratar `autor` textual como UUID de Auth ou realizar cutover.

**Para certificar C01 real:** identificar projeto Supabase legado/backup operacional **sem alterar origem**; autorização de extração; registrar hora de corte, hash dos bytes autorizados, contagens e órfãos por tabela, verificação de titularidade, proteção de PII e responsável. Uma ausência só pode ser certificada após consulta autenticada de origem autoritativa; até lá, caminhos C06/C07 usam exclusivamente fixtures sintéticas locais.

## Riscos conhecidos
- Legado usa IDs texto, enquanto GF02 usa UUID e FKs compostas por projeto/revisão.
- Oito tabelas legadas não têm owner individual; migrar exige identidade reconhecida por procedimento humano.
- Campos `resultado` e `padrao_entrada_config` têm estrutura JSON sem garantia de compatibilidade elétrica.
- Ausência de medição não significa zero. Fonte mantida inalterada.
