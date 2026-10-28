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
