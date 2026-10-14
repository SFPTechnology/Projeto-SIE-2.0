# Princípios Invioláveis — Slides Creator v9.0.0

Fonte canônica: `outputs/sinkra-squad/criacao-slides-ia/architecture.yaml#invariants`
Absorvido em: 2026-04-19 (ADR-021 / EPIC-SC-NARR)

Estes 7 princípios são invariantes da geração de decks McKinsey-grade. Cada um é enforçado em layer específica (code | schema | validator) e falha bloqueia a release.

---

## P1 — Fidelidade aos dados
- **enforcement_level:** `code`
- **enforcement layer:** tasks narrativas + QA sampling
- **failure_mode:** Qualquer número/citação não rastreável à fonte = QA FAIL.
- **validator:** `tasks/validate-fontes-apa.md` (orphan check) + `tasks/p1-fidelity-sampling.md` (10% humano opcional).
- **NUNCA:**
  - Modificar números, datas, nomes ou fatos recebidos
  - Inferir dados que não foram fornecidos
  - Arredondar valores sem permissão explícita
  - Reescrever citações ou interpretações de terceiros
  - Preencher gaps de dados com estimativas não solicitadas
  - Alterar ordem cronológica ou causal de eventos
- **SEMPRE:**
  - Usar dados EXATAMENTE como recebidos
  - Explicitar cálculos derivados ("Análise da equipe baseada em [fonte]")
  - Documentar gaps como "Dados não disponíveis" em vez de inventar
  - Preservar contexto original de citações com aspas
  - Citar fonte primária quando usar dados secundários
  - Sinalizar ambiguidades com marker `[VALIDAR COM CLIENTE: ...]`
- **teste_de_validação:** Um analista júnior deve conseguir rastrear cada número, fato ou citação de volta ao material fonte original sem ambiguidade.
- **edge_cases:** ver `data/edge-case-decisions.yaml` (EC-01 ambíguo, EC-02 insuficiente, EC-05 negativo)

## P2 — Especificação obsessiva
- **enforcement_level:** `schema`
- **enforcement layer:** `data/slide-spec-schema.yaml` (10 componentes obrigatórios) + `deck-spec.schema.json` sobre o output de `emit-deck-spec`.
- **failure_mode:** SlideSpec sem hex/grid_coord/pt_size OR sem qualquer dos 10 componentes = schema validation FAIL.
- **validator:** `tasks/emit-deck-spec.md` (schema gate — consome slide-spec-schema).
- **absorbed_detail:** Wave A (2026-04-20) — 10 componentes mandatórios: metadata, action_title, layout_grid, visual_elements (1-4), support_elements, footer_sources, ai_prompts, speaker_notes, transition_flow, quality_checklist.
- **anti-pattern:** "Adicione um gráfico de barras mostrando crescimento" (vago).
- **target-pattern:** "Gráfico de barras verticais agrupadas, posicionado em grid colunas 2-9 linhas 3-6, dimensões 14cm × 8cm, barras 0.8cm cada, cores [#003B5C, #00A86B], eixo Y 0-100 incrementos 20, data labels 12pt Bold #000000..."

## P3 — Pyramid Principle + MECE
- **enforcement_level:** `validator`
- **enforcement layer:** validators narrativos rodados em `SESSION-QA` fresh.
- **failure_mode:** Vertical test falha OU MECE violado = QA FAIL.
- **validators:** `tasks/validate-pyramid.md` + `tasks/validate-vertical-flow.md` + `tasks/run-vertical-test.md` (cross-instance).
- **regras_de_ouro (Barbara Minto):**
  1. Ideias em qualquer nível sempre resumem as ideias agrupadas abaixo
  2. Ideias em cada agrupamento são mutuamente exclusivas (MECE)
  3. Ideias em cada agrupamento seguem ordem lógica (dedutiva, cronológica, estrutural ou comparativa)
- **aplicação_slide (vertical flow):** Título = conclusão/insight principal · Visual = argumentos de suporte (max 3-4) · Fonte = evidências
- **aplicação_deck (horizontal flow):** Executive Summary = topo da pirâmide · Body = argumentos detalhados · Appendix = dados brutos
- **rule_of_three:** max 3 mensagens por nível hierárquico
- **teste_de_validação:** Cada slide-título sintetiza os visuals abaixo? Cada seção-título sintetiza os slides abaixo?

## P4 — Action titles obrigatórios
- **enforcement_level:** `validator`
- **enforcement layer:** regex + componentes semânticos por slide.
- **failure_mode:** Título descritivo (ex: "Análise de market share") = QA FAIL.
- **validator:** `tasks/validate-action-title.md`.
- **absorbed formula (Wave A):** `[O QUE ACONTECEU] + [MAGNITUDE/POR QUE IMPORTA] + [AÇÃO IMPLÍCITA]`
- **anti-patterns:** "Análise de mercado" · "Resultados financeiros" · "Conclusões"
- **target-patterns:**
    - "Mercado brasileiro crescerá 45% ao ano até 2027, 1.7× mais rápido que média global"
    - "EBITDA expandiu 23% YoY impulsionado por mix premium (+340bps margem)"
    - "Revenue cresceu 34% em Q4 via enterprise segment, superando guidance de 28% e validando upmarket strategy"
- **vertical-test:** Ler só os títulos de um deck deve contar a história completa sem abrir nenhum slide.

## P5 — Enumeração universal
- **enforcement_level:** `validator`
- **enforcement layer:** schema check de DeckSpec + varredura cross-slide.
- **failure_mode:** Qualquer visual sem ID (Gráfico N, Tabela N.M) = QA FAIL.
- **validator:** `tasks/validate-enumeration-universal.md`.
- **nomenclatura_obrigatória:**
  - `Gráfico {N}` — charts (bar, line, waterfall, scatter, pie)
  - `Tabela {N}.{M}` — tables (N = seção, M = índice dentro da seção)
  - `Figura {N}` — ilustrações, imagens, ícones decorativos
  - `Diagrama {N}` — fluxos, 2x2, value chains
- **formato_referência_cruzada:** "Conforme Gráfico 3.2, ..." em speaker notes e appendix
- **teste_de_validação:** Grep cross-deck: cada visual_id aparece ≥2x (definição + ≥1 referência)?

## P6 — Citação completa APA
- **enforcement_level:** `schema`
- **enforcement layer:** schema de fonte em DeckSpec.
- **failure_mode:** Citação sem `{org, title, date, url, access_date}` = schema FAIL.
- **validator:** `tasks/validate-fontes-apa.md`.
- **5_componentes_obrigatórios:**
  - `org` — organização emissora (ex: "McKinsey & Company")
  - `title` — título do documento (ex: "Global AI Survey 2024")
  - `date` — data de publicação (formato depende do idioma, ver `data/context-adaptations.yaml`)
  - `url` — URL completa (ou DOI)
  - `access_date` — data de acesso (obrigatória para web sources)
- **formato_footer_default:** `Fonte: {org} {title}, {date}, p. {página}. Acesso em: {access_date}` em Helvetica Neue italic 9pt #6E6E6E
- **teste_de_validação:** Schema AJV: todas 5 chaves presentes + url parseável + dates válidas
- **edge_case:** Fontes em outro idioma seguem APA variant — ver `data/context-adaptations.yaml#language`

## P7 — Prompts de IA completos (10 componentes)
- **enforcement_level:** `schema`
- **enforcement layer:** schema do `image_prompt` embutido em SlideSpec.
- **failure_mode:** Prompt IA com <10 componentes = schema FAIL.
- **validator:** `tasks/validate-action-title.md` (P7 sub-check) + `emit-deck-spec.md` (schema gate).
- **10_componentes_obrigatórios:**
  1. `subject_specification` — o quê exatamente
  2. `style_references` — corporate photography, Annual Report 2024 style, painter reference
  3. `composition` — framing, POV, focal point, rule of thirds
  4. `lighting` — direção, intensidade, mood, time of day
  5. `color_palette` — MUST match slide palette (reference `active-palette.yaml`)
  6. `environment` — setting, context, background
  7. `technical_params` — resolution, aspect ratio, film/digital, lens
  8. `mood_and_emotion` — target feeling in viewer
  9. `negative_prompts` — what to avoid (no watermarks, no text, no fingers, etc.)
  10. `reference_images` — if any (URLs ou descrições)
- **teste_de_validação:** Schema AJV: todas 10 chaves com valor não-vazio; `color_palette` conforma com brand resolution
- **KB_de_referência:** `data/kbs/KB_08_ai_generation.md` — protocolos ultra-detalhados

---

## Gate D01/D02/D03 — Human-in-the-loop

Os princípios são observados em três checkpoints humanos durante o workflow `generate-presentation` v2:

- **D01** (post-narrative analysis) — valida P1/P3/P6.
- **D02** (post-structure) — valida P3/P4 + vertical test precondition.
- **D03** (post-design) — valida P2/P5/P7 + STK-10 co-sign quando há brand override.

Ver: `data/checkpoint-schema.yaml`.
