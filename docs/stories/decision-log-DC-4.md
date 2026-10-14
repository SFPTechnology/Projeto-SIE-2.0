# Decision Log — DC-4 Motores C2 e C6 + Seleção Final

**Agente:** @dev (Dex) — YOLO mode
**Data:** 2026-07-12
**Branch:** feature/nbr5410-conformidade-closeout

---

## IDS — SEARCH / DECIDE / LOG

| Artefato | Decisão | Justificativa |
|----------|---------|---------------|
| `motores/motor-sobrecarga.ts` (`verificarSobrecargaC2`) | **REUSE** | C2 (5.3.4.1: IB≤In, In≤Iz, I2≤1,45·Iz) já existia no submódulo (landed com DC-4 commit). Cobre AC-DC-12 e AC-DC-18 integralmente, incl. `regime_sobrecarga_severo` → limite 1,0·Iz. Nenhuma alteração de código necessária. |
| `motores/motor-secao-minima.ts` (`calcularSecaoMinimaC6`) | **REUSE** | C6 (Tabela 47: ILU=1,5; TUG/TUE=2,5; Al=16) já existia. Cobre AC-DC-01. Sem alteração. |
| `servico-dimensionamento-condutores.ts` (seleção final) | **REUSE** | Orquestração `dimensionarCircuito` já faz seção_final = max(C1, C2ajustada, C6, C5), valida série `SERIE_SECOES` e sugere seção superior via `proximaSecao` quando In>Iz. Cobre AC-DC-06 e o `SeletorSecaoNormalizada` conceitual da story. Sem alteração. |
| `tests/domain/dimensionamento-condutores/motor-c2-c6.test.ts` | **CREATE** | Cobertura focada de C2/C6/seleção rastreável por AC (01/06/12/18) não existia; `mod-dc.test.ts` cobria apenas o caso chuveiro agregado. Capacidade de verificação nova legítima. |
| `MotorSobrecarga.ts` / `SeletorSecaoNormalizada.ts` (nomes sugeridos pela story) | **REJEITADO (CREATE)** | Nomes eram placeholders; duplicariam motores já existentes (`motor-sobrecarga.ts`, orquestração no serviço). Viola IDS (REUSE > CREATE) e Constitution Art. IV (No Invention). Caminhos reais do submódulo prevalecem. |

---

## [AUTO-DECISION] Escopo da story vs. prompt de spawn

- **Q:** O prompt de spawn descreveu C2 como "seleção de dispositivo de proteção via Tabela 41 (fusível/disjuntor/diferencial)" e C6 como "alternativas F=1/√n / isenção ≤30%", com nomes de arquivo `motor-protecao-dispositivo.ts`, `motor-alternativas-c6.ts`, `seletor-condutor-protecao-final.ts`. O arquivo da story DC-4 define C2 = sobrecarga (5.3.4.1), C6 = seção mínima (Tabela 47) e seleção = max normalizada.
- **Decisão:** Seguir **o arquivo da story** (fonte de verdade de AC, Constitution Art. III/IV). Não inventei motor de seleção de dispositivo nem "alternativas C6" — esses conceitos não constam dos AC da story. F=1/√n (grupo não semelhante) e isenção ≤30% já foram entregues em **DC-3** (AC-DC-24), não são escopo DC-4.
- **Razão:** Constitution Art. IV (No Invention): toda implementação rastreia a AC. Os AC reais da story são AC-DC-01, 06, 12, 18.

## [AUTO-DECISION] "C6 decisivo" (AC-DC-01) e o rótulo `criterio_decisivo`

- **Q:** AC-DC-01 diz "seção 1,5 mm² (C6 decisivo)". O seletor rotula `criterio_decisivo` pela regra "maior seção, primeiro na ordem C1→C2→C5→C6".
- **Descoberta:** `secaoC2Ajustada = max(C1, C6)` — C2 sempre absorve o piso C6, então C6 nunca é **estritamente** o rótulo `criterio_decisivo` (empate resolve para C2/C1, que vêm antes). Com ILU 1,5 mm², C1 também aterrissa em 1,5 (piso da série), empatando com C6.
- **Decisão:** Não forçar `criterio_decisivo === "C6"` (inalcançável no design atual). Testar o **efeito material**: C6 impõe o piso e `secao_fase` o respeita (`secao_fase >= secao_c6_minima`; e no TUE leve `secao_fase(2,5) > secao_c1(1,5)`, provando que C6 é o critério vinculante). Não alterei a lógica de rótulo para evitar mudança de comportamento sem AC que a exija.
- **Razão:** Preserva o invariante "nenhuma seção subdimensionada" (objetivo da story) sem invenção nem regressão.

## [AUTO-DECISION] AC-DC-12 "In > Iz → C2 reprovado; sugestão de seção superior"

- **Q:** O design auto-remedia (sobe para `proximaSecao`) em vez de rotular REPROVADO quando In>Iz.
- **Decisão:** Cobrir os dois ramos como o código os distingue: (a) **In > Iz** (proteção excede Iz da seção candidata) → sobe seção (chuveiro: In=40 > Iz=39,9 da seção 10 → sobe para 16, C2 torna-se decisivo); (b) **IB > In** (proteção subdimensionada para a carga) → `criterios.C2 = REPROVADO`. Ambos atendem à intenção do AC (não aceitar seção/proteção subdimensionada + sugerir seção superior).
- **Razão:** A "sugestão de seção superior" do AC = `proximaSecao`. O rótulo REPROVADO é reservado ao caso genuinamente inviável (IB>In / I2>limite), evitando marcar como falha um cenário auto-corrigível.

---

## Exemplos numéricos validados (worked examples)

| AC | Cenário | Resultado esperado | Verificado |
|----|---------|--------------------|-----------|
| AC-DC-01 | ILU Cu PVC B1 30 °C, IB 2,36 A | C6=1,5; C1≤1,5; **seção fase 1,5 mm²** | ✅ |
| AC-DC-01 | TUE leve, IB 3 A, In 10 A | C1=1,5; C6=2,5; **fase 2,5** (C6 eleva acima de C1) | ✅ |
| AC-DC-06 | ILU e chuveiro | seção fase ∈ série IEC 60228 | ✅ |
| AC-DC-12 | Chuveiro, In 40 > Iz 39,9 (10 mm²) | C2 sobe p/ **16 mm²**, decisivo=C2 | ✅ |
| AC-DC-12 | Chuveiro, IB 34,65 > In 20 | **criterios.C2 = REPROVADO** | ✅ |
| AC-DC-18 | I2 ausente | pendência `PENDENTE-I2`, limite não avaliado | ✅ |
| AC-DC-18 | I2=58 ≤ 1,45·45 | condição b) aprovada | ✅ |
| AC-DC-18 | I2=50, regime severo (limite 1,0·Iz=45) | **reprovado** (50 > 45) | ✅ |

---

## Quality Gates

| Gate | Comando | Resultado |
|------|---------|-----------|
| Testes focados | `npx vitest run tests/domain/dimensionamento-condutores/motor-c2-c6.test.ts` | 11/11 PASS |
| Suíte de domínio | `npx vitest run tests/domain/dimensionamento-condutores` | 42/42 PASS (sem regressões; era 31) |
| Testes API (contrato) | `npx vitest run tests/api` | 54/54 PASS (sem regressões) |
| Typecheck | `npx tsc --noEmit` | limpo (exit 0) |
| Lint | `npx eslint tests/.../motor-c2-c6.test.ts` | limpo (exit 0) |

**Self-healing:** 1 iteração (ajuste de teste TUE leve: `in_a` inadequado disparava bump de C2 para 4; corrigido para `in_a=10` + asserção de piso vinculante). Sem escalonamento. Zero mudanças no código de produção.

---

## Handoff → @qa (Quinn)

- Story `story-DC-4-motores-c2-c6.md` → **InReview**.
- Sem `git push` (delegado a @devops).
- **Escopo real DC-4:** C2 (sobrecarga 5.3.4.1) + C6 (seção mínima Tab. 47) + seleção final normalizada — **tudo pré-existente** (REUSE); entrega DC-4 = cobertura de teste rastreável + validação dos AC.
- Atenção QA: (1) `criterio_decisivo` nunca reporta "C6" por design (C2 absorve piso C6) — ver AUTO-DECISION; (2) In>Iz auto-remedia (sobe seção) em vez de REPROVAR; REPROVADO reservado a IB>In / I2>limite.
