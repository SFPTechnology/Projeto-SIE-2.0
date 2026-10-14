# Pricing Strategy — Counter-Pricing vs Submagic / Eddie / Descript

**Data:** 2026-05-06
**Princípio central:** **pricing É marca**. As 3 incumbentes têm dor pública de pricing. Nosso pricing precisa ser o oposto delas, **estruturalmente** (não apenas mais barato).

---

## 1. Counter-pricing thesis

### vs Descript — "Sem créditos. Sem surpresa."
Descript pivotou para AI Credits que esgotam em 1 dia (`descript.../audience-truth.md` Pattern #2). Bill shock $30 → "hundreds" no G2 é dor #2.
**Nossa resposta:** **flat pricing** com cap de minutos processados (não AI credits abstratos). Use à vontade dentro do tier.

### vs Eddie AI — "Tier intermediário existe."
Eddie tem abismo $21 → $167 (8× pulo) que abandona freelancer + creator sério (`eddie-ai.../gtm-gaps.md` Gap #1).
**Nossa resposta:** **curva linear** R$29 → R$69 → R$149 → R$299. Cada degrau é 2,4× o anterior, não 8×.

### vs Submagic — "Refund 30d. Aviso 7d. Cancele em 1 clique."
Submagic policy literal "no refunds. Ever." (`submagic.../audience-truth.md` Reclamação #2). Auto-renew sem aviso confirmado em 5+ Trustpilot. Sem proration.
**Nossa resposta:** **commitments públicos contratuais** — refund 30d, aviso 7d, proration honesta, cancelamento self-serve sem fricção.

---

## 2. Estrutura de tiers recomendada (4 tiers)

### Tier Free — "Solo Test"
- **Preço:** R$0
- **Inclui:**
  - 5 vídeos/mês (até 60 segundos cada)
  - 720p export
  - Watermark (apenas na fase 0–6 meses; remover quando produto provar para reduzir fricção)
  - Acesso à comunidade Discord
  - Suporte via Discord (não privado)
- **Wedge strategy:** mostrar capacidade real do produto, não "demo crippled". Limitação por **volume**, não por features.
- **Conversão alvo:** 8–12% Free → Solo nos 90 dias.

### Tier Solo — "Creator Solo"
- **Preço:** **R$29/mo (anual)** ou **R$39/mo (mensal)**
- **Equivalente USD:** ~$5.80/mo (anual) / $7.80/mo (mensal) — significativamente abaixo de Submagic Starter $19, Eddie Plus $21, Descript Hobbyist $24.
- **Inclui:**
  - 20 vídeos/mês (até 5 minutos cada)
  - 1080p export sem watermark
  - Captions em PT-BR (todos os estilos)
  - Suporte humano em PT-BR (resposta <24h)
  - Pix, boleto, cartão (1×–12× sem juros até R$300)
- **Por que esse preço:** PPP-adjusted (R$ × 5 ≈ USD × 1) e abaixo do "psychological floor" de R$30/mo onde se tornar mensalidade decisão familiar.

### Tier Creator — "Creator Pro"
- **Preço:** **R$69/mo (anual)** ou **R$89/mo (mensal)**
- **Equivalente USD:** ~$13.80/mo (anual) — concorre com Submagic Pro $24/mo.
- **Inclui:**
  - 100 vídeos/mês (até 15 minutos cada)
  - 4K export
  - Long-form repurpose (1 vídeo longo → N shorts)
  - Templates de captions BR (estilo Casimiro/Felipe Neto/Whindersson sob licença/genéricos)
  - B-roll AI search (powered by SigLIP 2 — `docs/bench/visual-embedding-models/`)
  - Semantic library search (own o gap "Eddie B-Roll Finder")
  - Mobile companion app (quando lançar)
- **Sweet spot do ICP-1.**

### Tier Pro/Agency — "Pro & Agency"
- **Preço:** **R$149/mo (anual)** ou **R$199/mo (mensal)**
- **Equivalente USD:** ~$30/mo (anual) — preenche o GAP $24 → $167 do Eddie.
- **Inclui:**
  - Vídeos ilimitados (cap em 5000 minutos processados/mês — generoso o suficiente para nunca tocar)
  - 5 sub-accounts (multi-brand kit)
  - White-label preview (preview com logo do cliente)
  - NF-e brasileira + contrato PT-BR + LGPD compliance pack
  - SLA 4h em horário comercial BRT
  - API access (Hotmart/Eduzz/Kiwify integrations)
  - Multicam VLM-decisionado (quando o produto provar — `categorical-gap-map.md` Gap #5)
- **Targeting:** ICP-2 (agência BR) + ICP-3 (course creator) + entry-level ICP-4.

### Tier Enterprise — "Custom"
- **Preço:** A partir de R$1500/mo, custom.
- **Targeting:** ICP-4 a partir do mês 12+.

---

## 3. Free Tier Strategy — wedge

### Princípio
**O free tier é o canal de aquisição #1.** Submagic se queixa que ferramentas "free" geraram tráfego sem conversão (`submagic.../README.md` TL;DR §3 — David Zitoun admitiu YouTube downloader não converteu).

### Decisão de wedge
- **NÃO copiar Submagic free** ("3 vídeos com watermark para sempre" — `submagic.../audience-truth.md` Reclamação #4 confirma frustração).
- **NÃO copiar Descript free** (60min limited, anyway).
- **DAR free tier que cumpre 80% do trabalho** para o creator emergente, mas **fica curto rápido** para creator escalando.

### Free tier deve gerar:
- **Conversão por valor demonstrado** (não por friction crippled).
- **Word-of-mouth** (creator sem dinheiro recomenda a 10 outros que vão pagar).
- **SEO content seed** (creator gera vídeo + posta org "Editado com Sinkra" — UGC marketing).

### Free tools paralelos (estilo Submagic 9M visits/mês mas PT-BR-first)
- `sinkra.com/ferramentas/legendar-video` — caption generator PT-BR free (até 3 min, sem login).
- `sinkra.com/ferramentas/cortar-podcast` — long-to-short generator (1 vídeo, 30s clip free).
- `sinkra.com/ferramentas/transcrever-audio` — Whisper-powered, free até 30min.
- `sinkra.com/ferramentas/hooks-de-reel` — gerador de hook em PT-BR.

**Alvo SEO:** capturar "legendar vídeo automático", "cortar podcast em shorts", "transcrever áudio grátis" em pt-BR (volume = ~50–200k buscas/mês cada keyword segundo SEMrush typical pattern para BR).

---

## 4. Annual vs Monthly Anchoring

### Estratégia
- **Annual default no pricing page** (mostrado primeiro).
- **Toggle Monthly / Annual** logo no topo, não escondido.
- **Saving callout claro**: "Economize 25% no anual."

### Por que annual default
- Aumenta LTV imediatamente (cash flow para reinvestir em distribuição).
- Reduz churn estrutural (anual = trinco mental).
- Pago via Pix anual = R$348 (R$29 × 12) — entra como receita única no mês 1.

### MAS:
- **Sem dark pattern.** Nada de "free trial → cobrança automática anual" sem aviso.
- **Aviso 30 dias antes da renovação anual** com email + dashboard banner.
- **Refund pro-rata** se cancelar dentro de 30 dias do início do anual.

---

## 5. Anti-Dark-Pattern Public Commitments

Estas frases vão na **homepage, pricing page, footer e checkout**:

### Compromissos públicos (literais para landing)
1. **"Refund de 30 dias, sem perguntas."** — diferente de Submagic "we don't refund. ever."
2. **"Aviso por email 7 dias antes de cada renovação."** — diferente de Submagic auto-renew silencioso.
3. **"Cancele em 1 clique. Sem call, sem chat, sem fricção."** — diferente de Descript que requer múltiplos passos.
4. **"Upgrade na hora. Pague apenas a diferença pro-rateada."** — diferente de Submagic sem proration.
5. **"Use à vontade dentro do seu tier. Sem créditos que somem."** — diferente de Descript AI Credits.
6. **"Pague em Pix, boleto ou cartão parcelado em até 12×."** — Submagic/Eddie/Descript = só USD card.
7. **"NF-e brasileira emitida automaticamente."** — Submagic/Eddie/Descript = não emitem.
8. **"Suporte humano em português, BRT 8h–22h, resposta <24h."** — único entre os 4.

### Onde aparecem
- **Hero footer:** banner em horizontal "30 dias refund · Aviso 7d · Cancele 1 clique · Pix/Boleto · NF-e".
- **Pricing page:** seção "Nossos compromissos" antes da tabela de tiers.
- **Checkout:** repete os 8 commitments antes do pagar.
- **Email transacional:** repete em welcome email + 7d-pre-renewal email.
- **Comparison page `vs/submagic`:** tabela honesta com checkmarks vs cruzes.

### Risco e mitigação
**Risco**: cumprir 100% dos commitments exige workflow técnico perfeito. Quebrar = "Submagic 2.0" reputação destruída em 1 review viral.
**Mitigação**:
- Não anunciar publicamente até infra estar pronta (Stripe webhooks + email 7d + proration calc + refund auto).
- Workflow de QA pré-launch: "fazer 5 cancelamentos de teste em produção, verificar cada commitment".
- Founder Alan responde pessoalmente toda reclamação de billing nos primeiros 90 dias.

---

## 6. PPP Adjustment (BR vs USD)

| Tier | BRL (anual) | BRL (mensal) | USD-equiv anual | USD-equiv mensal | Submagic equiv | Eddie equiv | Descript equiv |
|------|-------------|--------------|------------------|-------------------|----------------|--------------|----------------|
| Free | R$0 | R$0 | $0 | $0 | $0 | $0 | $0 |
| Solo | R$29 | R$39 | $5.80 | $7.80 | $19 (Starter) | $21 (Plus) | $24 (Hobbyist) |
| Creator | R$69 | R$89 | $13.80 | $17.80 | $24 (Pro) | — | $35 (Creator) |
| Pro/Agency | R$149 | R$199 | $30 | $40 | $69 (Business) | $167 (Pro) | $65 (Business) |

**Observação importante:** USD-equiv é roughly 5× BRL nos tiers pagos. Significa que para mercado USD futuro, **pricing internacional pode ser 2× o equivalente BRL** ($14 Solo, $29 Creator, $59 Pro/Agency) — ainda sub-precificado vs incumbentes mas com margem para CAC internacional.

**PPP rationale**: salário mediano BR × 5 ≠ salário mediano US, mas **disposição a pagar SaaS** em PT-BR é menor por fator ~2× (cabe nos R$30–80 sweet spot). Detalhar em `docs/bench/finance-pricing-ppp/` se evolução exigir.

---

## 7. Pricing como conteúdo de marketing

### Página de pricing como sales asset
- **Tabela comparativa "Sinkra vs Submagic vs Eddie vs Descript"** logo abaixo dos tiers.
- 8 commitments (item 5) como ícones grandes.
- Calculator ROI: "Em quantos vídeos você economiza R$ vs editor freelancer R$300/vídeo?"
- Testimonials de creator brasileiro reais (não traduzidos).

### Ataques tácticos com pricing
- **"Vindo do Submagic? Reembolsamos sua última fatura ao migrar."** — switching offer.
- **"Pagou anual no Descript? Sinkra te dá os meses restantes grátis."** — competitive switch.
- **"Free para estudantes de cinema BR (com .edu ou cursos parceiros)."** — Eddie não tem (`eddie-ai.../gtm-gaps.md` Gap #7).

---

## 8. Métricas a tracking (D-1)

| Métrica | Alvo mês 3 | Alvo mês 6 |
|---------|-----------|-----------|
| Free signup → trial activation | ≥40% | ≥55% |
| Free → paid conversion | ≥8% | ≥12% |
| ARPU mensal (Solo + Creator) | R$45 | R$55 |
| Annual / Monthly mix | 30% / 70% | 45% / 55% |
| Churn mensal pago | ≤6% | ≤4% |
| Refund rate | ≤2% | ≤1.5% |
| NPS interno | ≥50 | ≥60 |
| Inbound NPS de "anti-dark-pattern" | mencionado em 30%+ NPS comments | mencionado em 50%+ |

---

## Fontes
- `outputs/spy/research/submagic-marketing-deepdive/pricing-psychology.md`
- `outputs/spy/research/eddie-ai-marketing-deepdive/pricing-psychology.md`
- `outputs/spy/research/descript-marketing-deepdive/pricing-psychology.md`
- `outputs/spy/research/competitive-gtm-synthesis/categorical-gap-map.md`
- `outputs/spy/research/competitive-gtm-synthesis/icp-and-segmentation.md`
