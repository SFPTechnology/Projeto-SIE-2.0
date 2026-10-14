# Decision Log — DC-5 (Neutro, PE e PEN)

**Agent:** @dev (Dex) | **Mode:** YOLO | **Date:** 2026-07-13
**Story:** `docs/stories/story-DC-5-neutro-pe.md` | **Status:** Ready → InProgress → InReview

---

## Contexto

Motores de neutro/PE/PEN já estavam implementados no submódulo
`sistema-de-instala-es-el-tricas-sie-main`, à frente da story (commits DC-1/DC-4).
DC-5 formaliza e cobre por testes o comportamento normativo (6.2.6.2 + Tab. 48 /
Tab. 58 / PEN TN-C). O gap real da story era Task 5 (testes dedicados).

## Decisões (IDS: REUSE > ADAPT > CREATE)

| # | Decisão | Tipo | Justificativa |
|---|---------|------|---------------|
| D1 | `motor-neutro.ts` (`dimensionarNeutro`) para 5 condições + Tab. 48 + bloqueio harmônicas | REUSE | Já implementado e correto; produz exatamente os valores das AC-DC-15 (35→25; sem condições → neutro=fase) |
| D2 | `motor-pe-pen.ts` (`dimensionarPe`) para Tab. 58 | REUSE | Produz AC-DC-16 (50→25, 10→10, 25→16) sem modificação |
| D3 | `motor-pe-pen.ts` (`dimensionarPen`) para PEN TN-C | REUSE | Piso 10 mm² Cu / 16 mm² Al; null fora de TN-C |
| D4 | CREATE `tests/domain/dimensionamento-condutores/motor-neutro-pe.test.ts` (18 testes) | CREATE | Não existia arquivo dedicado; `mod-dc.test.ts` cobria só 1 caso agregado de DC-5. Novo arquivo isola AC-DC-15/16 + Tasks 3/4 em nível de unidade |
| D5 | NÃO criar `validador-neutro-pe.ts` nem validação de cor/função (AC-DC-17) | AUTO-DECISION | AC-DC-17 consta no prompt de missão mas NÃO nas AC da story. Art. IV (No Invention) + Story-Driven Development → implementar apenas AC-DC-15/16 e Tasks 1-5. Reason: story é a fonte autoritativa; File List PascalCase do rascunho é aspiracional e diverge do código real (kebab-case) |
| D6 | Seguir convenção real de testes `tests/domain/dimensionamento-condutores/` | AUTO-DECISION | File List da story aponta `tests/unit/domain/` inexistente; alinho ao diretório real usado por motor-c1/c2-c6/mod-dc |

## Verificação das AC

- **AC-DC-15:** `dimensionarNeutro({3F, neutro, ate_15}, 35, {equilibrado, protegido, Cu})` → 25 ✅; sem as 5 condições (não equilibrado / não protegido / monofásico / seção ≤25) → neutro=fase ✅
- **AC-DC-16:** `dimensionarPe(50)=25`, `dimensionarPe(10)=10`, `dimensionarPe(25)=16` ✅
- **Task 3 (PEN):** TN-C Cu piso 10; TN-C Al piso 16; usa fase quando > piso; null fora de TN-C ✅
- **Task 4 (harmônicas):** `taxa_h3="acima_33"` → neutro=fase + pendência `VERIFICAR-NEUTRO-HARMONICAS` ✅

## Quality Gates

| Gate | Resultado |
|------|-----------|
| Testes focados | 18/18 pass |
| Suíte domínio dimensionamento-condutores | 60/60 pass (6 arquivos, sem regressão vs. 42 anteriores) |
| `tsc --noEmit` | exit 0 |
| `eslint` (arquivo novo) | limpo (após `--fix` prettier) |

## Handoff para @qa

- Verificar traçabilidade AC ↔ testes.
- Confirmar que AC-DC-17 (cor/função) permanece fora de escopo desta story ou requer nova story/AC do @po.
