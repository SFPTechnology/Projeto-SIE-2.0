# Copy Anti-Slop Checklist

Cross-skill gate to refuse AI-generated copy patterns. Mirror of `design-absolute-bans.md §5` (Jane Doe Effect), adapted for copy outputs.

**Authority:** `.claude/rules/design-absolute-bans.md §5`
**Canonical data:** `squads/copy/data/copy-anti-slop-bans.yaml`
**Absorbed from:** tasteskill.dev v2 + impeccable.style v3.1.1

---

## When to run

- **Before delivering any copy artifact** (sales letter, VSL, email, ad, headline, body)
- **In `copy-chief` review** before approving handoff
- **In `copy-ops-worker` generation** as guardrail during draft

---

## 1. Filler words check 🪓

**Banned (refuse + rewrite):**

Elevate · Unlock · Unleash · Empower · Streamline · Seamless · Next-Gen · Next-Generation · Best-in-Class · World-Class · Industry-Leading · Revolutionary · Disruptive · Cutting-Edge · State-of-the-Art · Game-Changing · Game-Changer · Innovative

- [ ] Scan headline + lead + body. Any of the above appear?
- [ ] If yes: replace with concrete verb + number OR observable consequence
- [ ] Exception: termo aceitável se contexto adiciona substância imediata (ex: "Streamline 3 manual approvals into 1 click")
- [ ] Exception: dentro de quote real de cliente

**Example fixes:**
| ❌ Banned | ✅ Replacement |
|---|---|
| "Unleash your team's potential" | "Reduza handoffs em 40% no primeiro sprint" |
| "Seamless integration" | "Integração em 12 minutos, sem API key" |
| "Next-gen workflow" | "Aprovação em 1 clique (3 etapas a menos)" |
| "Revolutionary AI platform" | "Resposta em <8s com 92% de precisão" |

---

## 2. Generic names check 👤

**Banned:**

John Doe · Jane Doe · Sarah Chen · Sarah Chan · Jack Su · Test User · Demo User · Lorem User · Example Person

- [ ] Toda referência a pessoa em testimonial / case / exemplo é um nome REAL ou placeholder explícito `[TESTIMONIAL_PENDING — collect from {source}]`?
- [ ] Para PT-BR, usar nomes regionais realistas (Camila Ferreira, Bruno Rocha, Priya Iyer)
- [ ] Para US, usar nomes culturalmente diversos com sobrenomes reais

**Example fixes:**
| ❌ Banned | ✅ Replacement |
|---|---|
| "Sarah Chen, VP of Marketing" | "Camila Ferreira, Head de Growth na Magalu" |
| "John Doe testou o produto" | "[TESTIMONIAL_PENDING — collect from beta-cohort-3]" |

---

## 3. Startup-slop names check 🏢

**Banned:**

Acme · Acme Corp · Nexus · SmartFlow · FlowSync · DataSync · ExampleCo · TestCo · StartupCo · TechFlow · CloudSync · AISync · TechCorp · GenericCo

- [ ] Toda menção a empresa em case study / social proof é uma empresa REAL (com permissão) ou placeholder explícito?
- [ ] Se for cliente real cujo nome bate por acaso (raro), comentar `# verified real customer`
- [ ] Para PT-BR, citar empresas reconhecíveis: Magazine Luiza, Stone, iFood, Localiza, Natura

**Example fixes:**
| ❌ Banned | ✅ Replacement |
|---|---|
| "Empresas como Acme e Nexus usam" | "Magalu, Stone e iFood já usam" |
| "Case study: Acme Corp dobrou conversão" | "[CASE_STUDY_PENDING — beta-cohort-3 results]" |

---

## 4. Fake numbers check 🔢

**Banned patterns:**

- Round percentages: 99.99%, 100%, 50%, 10x, 100x (sem contexto verificável)
- Lazy phones: 555-1234, 555-555-5555, 1234567
- Round money: $1,000,000, $99.99, $9.99

- [ ] Toda estatística usa número orgânico (2-3 dígitos, não round)?
- [ ] Toda métrica de resultado tem fonte verificável (período, baseline)?
- [ ] Phone numbers são reais OU `[PHONE_PENDING — collect]`?
- [ ] Money values são específicos (não $100K, $1M sem decimal)?

**Example fixes:**
| ❌ Banned | ✅ Replacement |
|---|---|
| "Aumento de 50% nas vendas" | "Aumento de 47.2% nas vendas (jan-mar 2026)" |
| "10x faster" | "7.3x mais rápido (vs baseline em 2026Q1)" |
| "$1,000,000 MRR" | "$1.247M MRR em mar/2026" |

---

## 5. Filler phrases check 📋

**Banned openers / clichés:**

- "In today's fast-paced world..." / "In today's digital age..." / "In the modern era..."
- "Are you tired of..." / "Look no further!"
- "Take it to the next level"
- "Push the envelope" / "Think outside the box"
- "Move the needle" / "Synergy" / "Leverage" (como verbo)
- "Holistic" / "At the end of the day"

- [ ] Copy começa com o ponto (sem warm-up)?
- [ ] Sem qualquer das frases banidas acima?
- [ ] Sem buzzwords corporativos diluídos?

**Example fixes:**
| ❌ Banned | ✅ Replacement |
|---|---|
| "In today's fast-paced world, productivity is key..." | "Você gasta 3h/dia em status meetings." |
| "Are you tired of slow workflows? Look no further!" | "Aprovações de orçamento que demoram 9 dias agora levam 2 horas." |

---

## 6. Em-dash ban check 〰️

**Banned characters:** `—` (em-dash U+2014) · `–` (en-dash quando usado como em-dash) · `--` (double-hyphen)

> **Reflexa ban_07 do design** — em-dashes são tell de AI writing. Use vírgula, dois-pontos, ponto-vírgula, ponto ou parênteses.

- [ ] Sem `—` no body copy?
- [ ] Sem `--` no body copy?
- [ ] Exceções permitidas:
  - Dentro de quote direta de fonte externa (preservar fonte)
  - Em Markdown frontmatter (`---`)
  - Em URL ou string técnica

**Example fixes:**
| ❌ Banned | ✅ Replacement |
|---|---|
| "O produto faz X — sem fricção, sem onboarding" | "O produto faz X. Sem fricção. Sem onboarding." |
| "Você quer crescer — mas não sabe por onde começar" | "Você quer crescer, mas não sabe por onde começar." |

---

## 7. Lorem ipsum check 🚫

- [ ] Zero Lorem ipsum no output final
- [ ] Se copy não estiver pronto, usar marcador explícito: `[TODO: real headline from brief Section 3]`
- [ ] Templates do squad NÃO devem deixar Lorem ipsum default — só placeholder marcado `[TODO: ...]`

---

## 8. Aggregate AI-Slop Score

Após rodar checks 1-7, computar score:

| Score | Status | Ação |
|---|---|---|
| 0-20 | pass | Deliverable OK |
| 21-40 | warn | Avisar copy-chief, sugerir revisão antes de release |
| 41-60 | review | Manual gate — copy-chief lê e decide |
| 61-80 | block | Rebrief required — copy-ops-worker re-roda |
| 81-100 | hard-block | Full rebrief — retomar do brief original |

Fórmula: `P0_hits × 15 + P1_hits × 8 + P2_hits × 3` (capped at 100)

---

## Output schema

Após scan, emit `qa/copy-anti-slop-report.yaml`:

```yaml
copy_anti_slop_report:
  asset: "{file_path or asset_id}"
  scan_date: "2026-05-19T..."
  total_hits: 7
  p0_count: 2
  p1_count: 4
  p2_count: 1
  ai_slop_score: 53
  status: review
  hits:
    - category: filler_words
      term: "Seamless"
      location: "headline:s01"
      severity: P1
      replacement_suggested: "Integração em 12 minutos"
    - category: fake_numbers
      term: "99.99%"
      location: "body:p3"
      severity: P0
      replacement_suggested: "97.4% (dados Q1/2026)"
  top_fixes:
    - "Replace 3 filler words with concrete verbs (lift score by -24)"
    - "Replace 2 fake percentages with sourced numbers (lift score by -30)"
```

---

## Anti-Patterns desse checklist

- **Aplicar mecanicamente sem ler contexto** — sempre considerar exception_pattern
- **Banir termo legítimo dentro de quote real** — quotes externas preservam fonte
- **Sair regex-hunting sem rewrite suggestion** — score sem fix = sem valor
- **Block em P0 sem oferecer placeholder** — sempre dar caminho de saída (`[TODO: ...]`)

---

## Reference

- Canonical data: [`squads/copy/data/copy-anti-slop-bans.yaml`](../data/copy-anti-slop-bans.yaml)
- Cross-skill rule: `.claude/rules/design-absolute-bans.md §5`
- Bench source: `docs/bench/2026-05-18-impeccable-vs-sinkra-design-stack/`
- Cross-fit pair: `.claude/skills/slide-creator/templates/qa/copy-gates.yaml#jane_doe_effect_gate`
