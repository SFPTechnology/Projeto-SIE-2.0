# Comparison Matrix — Chatwoot vs Zendesk

**Bench:** chatwoot-vs-zendesk
**Data:** 2026-05-06
**Tipo:** product comparison

## Legenda — Niveis de equivalencia

| Score | Significado |
|------:|-------------|
| 5 | Forte — funcionalidade equivalente, mesma profundidade |
| 4 | Parcial alta — equivalente forte, pequenas diferencas escopo |
| 3 | Parcial — equivalente parcial, diferencas significativas |
| 2 | Fraco — equivalente fraco, gap substancial |
| 1 | Sem equivalente — sem correspondencia direta |

---

## Matriz consolidada por dimensao

| Dim | Nome | Peso | Chatwoot snapshot | Zendesk snapshot | Equiv | Vencedor da dim |
|-----|------|-----:|-------------------|------------------|------:|------------------|
| C1 | Canais nativos | 15% | 10 nativos + voice add-on; Telegram/TikTok native; X removido | 10 nativos + voice first-class; Apple BC native; X native; Telegram/TikTok via marketplace | 4 | Empate (perfis diferentes) |
| C2 | AI capability | 20% | Captain (auto-resolve, copilot, smart FAQs, memories, multilingual); credits; deflection nao publicada | AI Agents + Copilot + QA AI + WFM; per-seat $50 + per-resolution opaca; deflection 39-92% customer outcomes | 3 | Zendesk (publicado real) |
| C3 | Pricing transparency / TCO | 15% | $0/$19/$39/$99; ratio sticker-to-real 1.0-1.2x; self-host = $0 | $19/$55/$89/$115/$169 + add-ons; ratio 2.0-3.0x; Vendr median $47.772/yr | 2 | Chatwoot (clear) |
| C4 | Governance/Compliance | 10% | DPA GDPR; SOC2/ISO/FedRAMP nao publicas; HIPAA BAA nao oferecido; self-host = escape valve | SOC2 + ISO 27001/27018/27701 + FedRAMP + HIPAA BAA + GDPR BCR + EU/US/AU/JP residency | 2 | Zendesk (clear) |
| C5 | Ecosystem/Marketplace | 10% | Tens of integrations; API + DB access self-host | **1.977 apps**, 1.136 vendors, 75% ARR marketplace-impacted, AI 21.54% | 2 | Zendesk (clear) |
| C6 | Comunidade/Maturidade | 10% | 29.1k GitHub, G2 4.4 (~200-400 reviews), 9 anos, monthly releases | 6.000+ G2, 14.8% market share, 19 anos, 88% ease-of-use cite | 3 | Zendesk (enterprise scale) / Chatwoot (open dev) |
| C7 | Flexibilidade | 10% | MIT self-host + 3 BSP BYOC + zero lock-in + source modifiable | Cloud-only proprietary + sandbox Enterprise | 1 | Chatwoot (sem equivalente) |
| C8 | Brasil-fit | 10% | BYOC wrap BR BSP; PT-BR UI; sem BRL pricing; sem BR team | BRL pricing publico; suporte BR; sales BR; marketplace BR apps | 3 | Zendesk (mais turnkey) / Chatwoot (mais flexivel) |

**Average equivalence:** 2.625/5 — confirma que **no-clear-winner overall** (filosofias opostas).

---

## Side-by-side detalhado

### C1 — Canais nativos

```yaml
chatwoot_channels:
  native: [live_chat, email, whatsapp_3bsp, fb_messenger, instagram_dm,
           telegram, line, sms, tiktok, api_custom]
  whatsapp_bsp_options: [meta_cloud_direct, twilio, dialog360]
  removed: [twitter_x]
  voice: addon_enterprise_only

zendesk_channels:
  native: [email, live_chat, whatsapp_meta_cloud, fb_messenger, instagram_dm,
          twitter_x, apple_business_chat, line, sms, voice_talk]
  whatsapp_bsp_options: [meta_cloud_only]
  via_marketplace: [telegram, tiktok]
  voice: first_class_native
```

**Delta objetivo:**
- Chatwoot vence: Telegram nativo, TikTok nativo, WhatsApp 3 BSP options BYOC
- Zendesk vence: Voice/Talk first-class, Apple Business Chat nativo, Twitter/X ainda nativo
- Empate em quantidade total de canais nativos (10 cada)

### C2 — AI capability

```yaml
chatwoot_ai:
  product: Captain
  features: [auto_resolve, copilot, smart_faqs, memories_summarization, multilingual]
  pricing: credits_per_tier_300_500_800 + $20_per_1k_overage
  deflection_rate_published: null
  customer_outcomes: not_published
  transparency: credit_consumption_rules_NOT_public

zendesk_ai:
  products: [ai_agents_post_ultimate, copilot, qa_ai, wfm]
  features:
    - autonomous_agentic_cross_channel
    - agent_assistant_with_action_execution
    - auto_qa_scoring
    - workforce_management
  pricing:
    copilot: $50_per_seat
    qa: $35_per_seat
    wfm: $25_per_seat
    ai_agents: per_resolution_NOT_PUBLIC
  deflection_published_customer_outcomes:
    - freedom_furniture: 66pct_first_contact
    - next: 92pct_email_handling_reduction
    - urbanstems: 39pct_automated_$100k_savings_3mo
    - lush: 60pct_first_contact_$434k_annual_savings
  productivity_gain: ~20pct_via_copilot
  transparency: per_seat_clear_per_resolution_opaque
  maturity: post_acquisition_ultimate_2024_still_integrating
```

**Delta objetivo:**
- Zendesk vence em outcomes publicados (4 customers cited 39-92%) e em produtos AI especializados (QA, WFM dedicated)
- Chatwoot vence em simplicidade conceitual (single Captain product, built-in nao add-on)
- Concern compartilhado: ambos tem pricing layer opaco (Chatwoot credits / Zendesk per-resolution)

### C3 — Pricing transparency e TCO real

#### Chatwoot — TCO 5 agentes / 12 meses

```
Cenario A — Cloud Startups
  $19 × 5 agents × 12 = $1.140/year
  Captain credits 300/mo (15.000 credits ano) — overage estimada $60-200/year
  Total ano: ~$1.200-1.340

Cenario B — Cloud Business
  $39 × 5 × 12 = $2.340/year
  Captain credits 500/mo + Teams + Automation + SLA
  Total ano: ~$2.400-2.500

Cenario C — Self-host
  $0 license
  Infra ~$50-200/mo VPS = $600-2.400/year
  DevOps time ~0.05-0.1 FTE
  Total ano: ~$600-2.400 + DevOps

Cenario D — Cloud Enterprise + Voice
  $99 × 5 × 12 = $5.940/year
  + Voice/Video addon (preco sob consulta) ~$1.500-3.000
  + Captain 800 credits + audit + SSO
  Total ano: ~$6.000-9.000
```

#### Zendesk — TCO 5 agentes / 12 meses

```
Cenario A — Suite Team
  $55 × 5 × 12 = $3.300/year (sticker)
  Real (2x): ~$6.600/year com setup + onboarding

Cenario B — Suite Pro + Copilot bundle
  $155 × 5 × 12 = $9.300/year (bundle pricing)
  Real (~1.5x bundle, 2x sem bundle): $9.300-13.000

Cenario C — Suite Enterprise + Copilot
  $209 × 5 × 12 = $12.540/year (bundle)
  + Add-ons (QA $35, WFM $25, ADPP $50) = +$110/agent/mo opcional
  Total ano: $12.540-25.000

Cenario D — AI Agents (per-resolution)
  Pricing nao publico
  Estimated $0.85-1.20 per resolution baseado em peers (Fin $0.99, Help Scout $0.75, Gorgias $0.90-1.00)
  Para 1.000 resolucoes/mo = $850-1.200/mo additional

Vendr median deal: $47.772/year per customer (15% negotiated discount tipico)
```

**Delta sticker-to-real ratio:**
- Chatwoot: **1.0-1.2x** (BYOC reduz markup; credit overage minor)
- Zendesk: **2.0-3.0x** (add-ons necessarios pra parity de feature; AI Agents extra)

### C4 — Governance/Compliance

| Cert/Posture | Chatwoot Cloud | Zendesk Suite |
|--------------|:--------------:|:-------------:|
| SOC 2 Type II | Implicit (nao explicit publica) | ✅ Explicit + audited |
| ISO 27001 | ❌ Nao listado | ✅ |
| ISO 27018 (cloud privacy) | ❌ | ✅ |
| ISO 27701 (privacy info mgmt) | ❌ | ✅ |
| FedRAMP | ❌ | ✅ |
| GDPR DPA | ✅ | ✅ |
| GDPR BCR (Binding Corporate Rules) | ❌ | ✅ Aprovado 2017 (segunda empresa Irish DPC) |
| HIPAA BAA | ❌ Nao oferecido | ✅ Requer Advanced Compliance addon |
| EU Dublin DC | ❌ Cloud nao user-selectable | ✅ (mas requer activation manual) |
| Multi-region (US/EU/AU/JP) | ❌ | ✅ |
| Audit logs | Enterprise tier ($99) | Enterprise tier |
| SSO/SAML | Enterprise tier ($99) | Suite tiers |

**Self-host escape valve:** Chatwoot **MIT self-host** = cliente roda em sua propria regiao com seu proprio compliance posture. Para regulated industries, isso e o backstop quando Cloud nao tem certs.

### C5 — Ecosystem / Marketplace

| Metrica | Chatwoot | Zendesk |
|---------|---------:|--------:|
| Apps marketplace curado | Tens (community-distributed) | **1.977** |
| Vendors | Open (sem lista oficial) | 1.136 |
| Free apps | N/A | 1.176 |
| AI-powered apps | Via custom integration | 21.54% (~425 apps) |
| Customer install rate | N/A | 58% tem 1+ |
| Marketplace ARR impact | N/A | 75% |
| API openness | REST + webhooks + DB access self-host | REST + webhooks + sandbox Enterprise |

### C6 — Comunidade / Maturidade

| Sinal | Chatwoot | Zendesk |
|-------|---------:|--------:|
| GitHub stars | 29.100 | N/A (proprietary) |
| GitHub forks | 7.200 | N/A |
| Open PRs | 266 | N/A |
| G2 rating | 4.4 | 4.3 |
| G2 reviews count | ~200-400 (estimate) | **6.000+** |
| Maturidade (anos) | 9 | **19** |
| Market share categoria CX | N/A (OSS) | **14.80%** |
| Competitors in category | — | 252 |
| Estimated payback (months) | N/A | 17 |
| Ease of use (G2 mention) | N/A | 88% |
| Release cadence | Monthly minor | Continuous deployment SaaS |
| BR sales/support team | ❌ | ✅ |

### C7 — Flexibilidade (sem equivalencia)

```yaml
chatwoot_flexibility:
  self_hosted: MIT_full_source_no_feature_gating
  deployment: [docker_compose, kubernetes, heroku, cloud_saas]
  byoc_whatsapp: 3_bsp_options
  api: REST_webhooks_DB_access_self_host
  customization_ceiling: forks_plugins_dashboard_apps
  vendor_lock_in: minimal_can_migrate_to_self_host_anytime

zendesk_flexibility:
  self_hosted: IMPOSSIBLE
  deployment: cloud_saas_only
  byoc_whatsapp: meta_cloud_only
  api: REST_webhooks_sandbox_enterprise
  customization_ceiling: apps_via_zendesk_apps_framework
  vendor_lock_in: MAXIMUM_proprietary
```

**Score 1 (sem equivalente):** Zendesk **nao tem equivalente** ao self-host MIT do Chatwoot. Chatwoot **nao tem equivalente** ao sandbox dedicated do Zendesk Enterprise.

### C8 — Brasil-fit

| Dim | Chatwoot | Zendesk |
|-----|:--------:|:-------:|
| WhatsApp BSP BR | ✅ BYOC (Meta direct, Twilio BR, 360Dialog) | ✅ Meta Cloud API direct |
| PT-BR UI | ✅ Community translation madura | ✅ Mature |
| Pricing BRL publicado | ❌ | ✅ R$135/R$359/R$755/R$1.105 |
| VTEX nativa | ❌ | ❌ |
| Shopify nativa | ✅ | ✅ via marketplace |
| RD Station nativa | ❌ | ✅ via marketplace community |
| Pix nativa | ❌ | ❌ |
| Local support team | ❌ | ✅ |
| BR sales team | ❌ | ✅ |

**Delta objetivo:**
- Zendesk vence em turnkey BR (BRL pricing + suporte BR + sales BR)
- Chatwoot vence em flexibilidade BR (cliente wrap qualquer BSP BR via Cloud API)
- Ambos perdem para Octadesk/Take Blip/Zenvia em integracoes BR-specific (VTEX, Pix, RD Marketing nativo)

---

## Sintese da matriz

```yaml
verdict_overall:
  no_clear_winner: true
  reason: filosofias_opostas — OSS_flexibility vs Enterprise_compliance_ecosystem
  
chatwoot_dominant:
  - C7_flexibilidade (sem equivalente)
  - C3_pricing_transparency (clear)
  
zendesk_dominant:
  - C4_governance_compliance (clear)
  - C5_ecosystem_marketplace (clear)
  - C6_maturidade_enterprise_scale
  
balanced_or_perfil_diferente:
  - C1_canais
  - C2_ai
  - C8_brasil_fit
  
selection_criteria_question:
  - "Voce precisa de SOC2/HIPAA/FedRAMP cert publica?" -> Zendesk
  - "Voce precisa de marketplace 1.977 apps?" -> Zendesk
  - "Voce precisa de self-host por compliance/cost/control?" -> Chatwoot
  - "Voce tem time tecnico DevOps?" -> Chatwoot viable
  - "Voce e PME com budget restritivo?" -> Chatwoot
  - "Voce e enterprise BR com need de BR-team?" -> Zendesk (mas considerar Octadesk/Take Blip)
```
