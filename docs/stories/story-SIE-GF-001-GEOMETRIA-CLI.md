# Story SIE-GF-001 — Núcleo geométrico greenfield, CLI-first

**Contexto:** engenharia reversa do SIE original e reconstrução independente SIE 2.0.
**Base:** commit F11 `11643cf3ad7da2e6182183c6071148f924bfe741`; branch isolada `feat/gf01-geometria-core-f11` para desenvolvimento, sem modificar `feat/f12-liberacao-controlada`.
**Escopo:** geometria retangular de ambientes, identidade de projeto/revisão, hash canônico; sem validação elétrica e sem dados remotos.

## Proveniência verificável
- Legado **somente leitura**: `SFPTechnology/sistema-de-instala-es-el-tricas-sie`, `src/domain/calculo/geometria.ts` (`main`). Área L×C; perímetro útil `2(L+C)-exclusões`, assumindo ambiente retangular.
- `REFERENCIA-INTEGRAL-SISTEMA.md`: requisitos F-01/F-02; dado normativo F-03 em diante ainda requer verificação independente.
- Novo destino obrigatório: `fozrymsidnaxmuvxxfhh`. No checkpoint 27/10/2026, conta MCP indisponível: `link_id must identify an eligible linked account`. Não executar migrations nem presumir schema.

## Critérios de aceite
- [x] GF01-01: CLI com entrada JSON vinculada a `project_id` e `revision_id` (UUID).
- [x] GF01-02: cálculo geométrico em `Decimal`, sem arredondar prematuramente.
- [x] GF01-03: rejeitar dimensões inválidas, NaN/infinito, exclusão >= perímetro, campos não documentados e IDs duplicados.
- [x] GF01-04: manifesto determinístico SHA-256 dos dados de entrada canonizados.
- [x] GF01-05: saída indica `rectangular_only` e `NOT_EVALUATED`; nenhum cálculo de conformidade presumido.
- [x] GF01-06: suíte local focada com 22 testes e verificação de erros CLI, sem banco real.
- [ ] GF01-07: CI completo no SHA final da branch.
- [ ] GF01-08: testes de persistência/RLS e migração em ambiente de homologação (bloqueados pela conexão).

## File list
- `docs/stories/story-SIE-GF-001-GEOMETRIA-CLI.md`
- `docs/implantacao-sie-2-0/GREENFIELD/GEOMETRIA-CLI.md`
- `restructuring/apps/api/sie_api/nextgen_geometry.py`
- `restructuring/apps/api/sie_api/nextgen_geometry_cli.py`
- `restructuring/apps/api/tests/test_nextgen_geometry.py`

## Validação e restrições
`PYTHONPATH=restructuring/apps/api python -m pytest restructuring/apps/api/tests/test_nextgen_geometry.py -q`

**Resultado em execução isolada:** 22 PASS (Python 3.13). CI da branch de desenvolvimento a conferir; gate F12 preservado e nao aplicado a novas features.

Nenhuma alteração no SIE original, `main`, banco Supabase ou hospedagem Hostinger. O módulo não possui autorização normativa, autenticação, tenant sharing, importação de planta irregular, persistência nem UI.
