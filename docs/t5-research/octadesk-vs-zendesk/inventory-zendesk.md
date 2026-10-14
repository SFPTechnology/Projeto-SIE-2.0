# Inventario - Zendesk

**Data:** 2026-05-06
**Bench:** octadesk-vs-zendesk
**Tipo:** product
**Confidence global:** high

---

## Identidade

| Campo | Valor |
|---|---|
| Nome | Zendesk for Customer Service (Suite) |
| Empresa | Zendesk Inc. (private equity-owned post-2022 take-private) |
| Categoria | Customer service / helpdesk SaaS enterprise global |
| Lancamento | 2007 (~19 anos) |
| Pais origem | USA |
| Target | SMB to enterprise; mid-market e enterprise referenciam mais |
| Tagline | "Customer service made effortless" |
| URL | https://www.zendesk.com |
| Market share | 14.80% categoria customer experience (lider global, 6sense data) |

---

## Features

### Categorias

**Suporte multicanal Suite (deep)**
- Email, chat, voice (Talk), WhatsApp via Sunshine Conversations
- Instagram, Facebook, Twitter, Apple Business Chat, Line, SMS
- Help Center / Guide multi-help-center (ate 300 em Enterprise)
- Communities / Gather

**Agent Workspace (deep)**
- Unified inbox cross-channel
- Triggers, automations, views, workflows
- Macros e templates
- Side conversations (loop interno)

**AI Agents post-Ultimate.ai (deep mas fragmentada)**
- AI Agents Essential (incluso em Suite)
- AI Agents Advanced (add-on)
- Copilot $50/agent/mo - reply suggest + summarize
- Resolucao 40-50% baseline ate 80% maduro (declarado)

**Reporting & Analytics (deep)**
- Explore (built-in BI)
- Custom dashboards
- Forecasting (ADPP+)

**Voice Talk (moderate)**
- Inbound/outbound voice nativo
- IVR, recording, voicemail
- Contact Center add-on $50/agent/mo

**Workforce Management (moderate)**
- WFM add-on $25/agent/mo
- Schedule + adherence + forecasting

**Quality Assurance (moderate)**
- QA add-on $35/agent/mo
- Conversation review + scorecards

### Diferenciais unicos
- Maior marketplace de apps da categoria (1.500+ apps)
- Suite plans modulares (Team -> Enterprise) com upgrades graduais
- Sunshine Conversations BSP nativo (WhatsApp + WeChat + LINE + Apple Business Chat)
- Multi-help-center (ate 300 em Enterprise) - unico no segmento
- Sandbox 2 inclusos em Enterprise
- Custom agent roles em Enterprise
- Audit logs em Enterprise
- BYOK encryption via ADPP add-on
- FedRAMP LI-SaaS (gov USA)
- ISO 27001:2022, 27017, 27018, 27701, 42001, CSA STAR AI L1+L2

**Total features estimado:** ~200
**Confidence:** H em features publicas; M em add-ons gated

---

## Pricing

### Site oficial Brasil (zendesk.com.br/pricing, 2026-05-06, em BRL)

| Plano | Preco BRL/agent/mes | Billing | Escopo |
|---|---:|---|---|
| Support Team | R$ 135 | anual | Ticketing-only baseline |
| Suite Team | R$ 359 | anual | Omnichannel basico (email + chat + voice + WhatsApp via Sunshine) |
| Suite Professional | R$ 755 | anual | Advanced workflows + custom roles parcial |
| Suite Enterprise | R$ 1.105 | anual | Full enterprise: multi-help-center, sandbox, audit log, custom roles |

### Tiers USD referencia global

| Plano | Preco USD/agent/mes |
|---|---:|
| Suite Team | $55 |
| Suite Growth | $89 |
| Suite Professional | $115 |
| Suite Enterprise | $169 |

### Add-ons listados na pagina Brasil

| Add-on | Preco USD | Unidade | Notes |
|---|---:|---|---|
| Copilot (AI) | $50 | agent/mo annual | reply suggest + summarize |
| Quality Assurance | $35 | agent/mo annual | conversation review + scorecards |
| Workforce Management | $25 | agent/mo annual | schedule + adherence |
| Advanced Data Privacy & Protection (ADPP) | $50 | agent/mo annual | BYOK + advanced audit |
| Contact Center (Voice) | $50 | agent/mo annual | full voice + IVR |

### AI Agents pricing (per-resolution)

| Modalidade | Preco USD/resolucao |
|---|---:|
| Committed plan | $1.50 |
| Pay-as-you-go | $2.00 |

**Definicao:** "Automated resolution" = bot fully handled sem human; verificado 72h sem follow-up + LLM check
**Source:** eesel.ai 2026 guide

### Free tier
- Free tier: nao
- Trial: 14 dias

### Contract terms criticos
- Annual billing only para preco listado (monthly +15-25%)
- Downgrades blocked mid-contract
- 30 dias notice via revops@zendesk.com para nao-renovacao
- Sem refund early cancellation
- 5-7% price escalation clauses anuais
- Overages auto-billed sem grace period (Jan 2026 update)

### TCO examples 2026

**5-person startup:**
- Suite Growth $89 x 5 = $445/mo
- AI Agents 500 res x $1.50 = $750/mo
- **Total: $1.195/mo / $14.340/year**

**10-person mid-market:**
- Suite Professional $115 x 10 = $1.150/mo
- Advanced AI $50 x 10 = $500/mo
- AI resolutions 2.000 x $1.50 = $3.000/mo
- **Total: $4.650/mo / $55.800/year**

### Vendr median deal
- $47.772/year por cliente (15% desconto negociado tipico)

**Source:** zendesk.com.br/pricing + eesel.ai 2026 + helpjuice + supportbench
**Confidence:** H para tier publico site BRL; H para add-ons; H para AI per-resolution; M para tier USD historico

---

## Integrations

### API
- REST + GraphQL parcial
- Webhooks: SIM
- Documentacao: developer.zendesk.com (extensivo)

### Marketplace
- **1.500+ apps** (zendesk.com/marketplace/)

### Integracoes nativas globais
- Slack, GitHub, Jira, Salesforce, HubSpot, Shopify, Stripe, Microsoft 365
- Talk nativo (voice)
- Sunshine Conversations BSP nativo

### Integracoes BR via parceiros (NAO first-class)
- VTEX by BCR.CX (parceiro)
- VTEX by Aktie Now (parceiro)
- Tray, NuvemShop: nao confirmado app dedicado
- RD Station, Bling, Conta Azul: nao first-class

**Gap critico BR:** falta de connectors NATIVOS first-class para Tray, NuvemShop, RD Station, Bling, Conta Azul. Conectores VTEX existem mas via parceiros (BCR.CX, Aktie Now). Profundidade depende do parceiro.

### SDK languages
- JavaScript, Python, Ruby, PHP

### Plugin system
- Zendesk Apps Framework (ZAF)

### Sunshine Conversations pricing
- Model: fixed monthly fee + variable per MAU + per notification
- Starter price from: $0.15/notification (custom channels/WhatsApp/in-app)
- Monthly fee from: $495/mo (via GetApp)
- Editions: Starter, Premium, Enterprise

**Source:** zendesk.com/marketplace/ + zendesk.com.br/marketplace/apps/support
**Confidence:** H para apps count global; M para BR-specific connector depth

---

## User Experience

| Dimensao | Valor |
|---|---|
| Onboarding | moderate-complex (G2: "configuration takes longer than expected, requires technical expertise") |
| UI quality | modern but feature-dense |
| Learning curve | moderate-steep (G2 mention multiplas vezes) |
| Mobile app | sim |
| Offline support | limited |
| Acessibilidade | WCAG 2.1 AA (declarado) |
| Idioma PT-BR | tradus PT-BR (nao nativo) |

**Source:** G2 reviews summary 6.000+ + Trust Center
**Confidence:** H

---

## Reviews

### G2

- **Rating:** 4.3/5
- **Reviews:** 6.000+
- **Payback period:** 17 meses

**Top praises:**
- Ease of Use (532 mentions)
- Features (402)
- Customer Support (286)
- Helpful (280)
- Ticket Management (257)
- Strong automation, robust reporting, multi-channel unified

**Top complaints:**
- Cost / pricing escalation (66 mentions: "expensive for smaller teams")
- Limited Features customization (123)
- Ticketing complexity (94)
- Customer support slow / unhelpful (73)
- Integration issues at scale (55)
- Steep learning curve
- Configuration complexity
- Add-ons stack ($50 Copilot + $25 WFM + $35 QA + $50 ADPP)

### Capterra
- **Rating:** 4.5/5
- **Reviews:** extenso (milhares)

### TrustRadius
- **Rating:** 8.7/10

**Source:** https://www.g2.com/products/zendesk-support-suite/reviews + learn.g2.com/zendesk-review
**Confidence:** H

---

## Scalability & Enterprise

### Tier limits

| Plano | Capacidade |
|---|---|
| Suite Team | single help center, agent workspace basic |
| Suite Professional | 5 help centers + side conversations + custom views |
| Suite Enterprise | 300 help centers + sandbox 2 inclusos + custom agent roles + audit logs |
| Suite Enterprise Plus | additional sandbox + 99.9% SLA + premium support |

### Enterprise features
- SSO/SAML (2 configs) + JWT (2) + OIDC
- SCIM provisioning
- Custom agent roles (Enterprise)
- Audit logs (Enterprise)
- Sandbox environments (Enterprise = 2; Plus = +)
- Multi-help-center (300 em Enterprise)
- BYOK via AWS KMS + Azure Key Vault + Google Cloud (ADPP add-on $50/agent)
- RBAC granular
- 2FA
- DDoS via Cloudflare + AWS
- IDPS, SIEM real-time
- AES-256 at rest, TLS 1.2+ in transit

### Compliance certifications
- ISO 27001:2022, 27017:2015, 27018:2019, 27701:2019, 42001 (AI mgmt)
- CSA STAR AI Levels 1 & 2
- GDPR (BCRs approved by Irish DPC - 2nd company ever)
- CCPA/CPRA
- HIPAA (via BAA + Advanced Compliance add-on)
- PCI-DSS (com redaction tools)
- FedRAMP LI-SaaS (gov USA)
- LGPD (Brazil) declarado
- SOC 2 Type II (sob NDA via Trust Center)

### Data residency
- Multiple regions (USA, EU, APAC). EU hosting via Zendesk Data Center selection
- **Nao garantido data center BR.** Dados podem residir USA/EU. Risco concreto para LGPD operadores que precisam de residencia BR estrita

### SLA
- 99.9% Enterprise Plus
- 99.5% baseline Enterprise

**Source:** zendesk.com/trust-center/ + eesel.ai 2026 + supportbench audit
**Confidence:** H

---

## Support & Community

| Dimensao | Valor |
|---|---|
| Docs quality | excellent (developer.zendesk.com + support.zendesk.com extensos) |
| Channels | Standard support (todos planos), Premium Support (paid add-on), Premier Plus (Enterprise+), Email, Chat (limited), Phone (premium tiers) |
| Language | ingles principal; PT-BR via traducao |
| Community | Zendesk Community + Trailhead-equivalente |
| Knowledge base | sim |
| Status page | sim |
| BR local team | presenca via canal de revenda BR mas nao um time local de produto comparavel a Octadesk |

**Source:** support.zendesk.com
**Confidence:** H

---

## AI nativa - Zendesk AI

| Atributo | Valor |
|---|---|
| Nome | Zendesk AI (Agents + Copilot) |
| Engine declarado | post-Ultimate.ai acquisition + proprio LLM stack |
| Modos | AI Agents Essential (free in Suite), AI Agents Advanced (paid), Copilot $50/agent/mo, Bots automation |
| Language | multi-language including PT-BR |
| Deflection rate publicado | 40-50% baseline ate 80% maduro (declarado + 3rd party Fin Labs) |
| Pricing model | Hybrid: per-seat ($50 Copilot) + per-resolution AI Agents ($1.50 committed / $2.00 PAYG) |
| Automated resolution definition | Bot fully handled sem human; verificado 72h sem follow-up + LLM check |
| Data isolation | declarada |

**Source:** zendesk.com/service/ai/ + eesel.ai 2026 + Trust Center
**Confidence:** H

---

## WhatsApp Integration

| Atributo | Valor |
|---|---|
| Oficial Meta declarado | SIM |
| BSP role | Zendesk BSP via Sunshine Conversations + Cloud API direct |
| Cloud API only | SIM |
| Sunshine Conversations role | Translation layer entre support team e messaging apps (WhatsApp, FB, Insta, Apple BC, LINE, Telegram, Viber) |
| Sunshine pricing | $0.15/notification + fixed monthly fee + variable per MAU + per notification; starter $495/mo |
| Sunshine transparency score | low-medium (multiplas variaveis) |
| Message pricing passthrough | SIM (Meta charges via Sunshine) |
| Free 24h service window | padrao Meta |
| Templates approval | padrao Meta com Sunshine intermediation |
| Multi-agent same number | via agent workspace |
| Tier lock | WhatsApp via Sunshine Conversations (Suite Team em diante) |

**Source:** Trust Center + eesel.ai Sunshine guide + GetApp
**Confidence:** H para oficialidade Cloud API; M para Sunshine pricing exato (gated)

---

## Sources Consulted

1. https://www.zendesk.com
2. https://www.zendesk.com.br/pricing/
3. https://www.zendesk.com/pricing/ (redirects to .com.br)
4. https://www.zendesk.com/marketplace/
5. https://www.zendesk.com/trust-center/
6. https://support.zendesk.com
7. https://developer.zendesk.com
8. https://www.g2.com/products/zendesk-support-suite/reviews
9. https://learn.g2.com/zendesk-review
10. https://www.eesel.ai/blog/zendesk-pricing-2026
11. https://www.eesel.ai/blog/zendesk-sunshine-conversations
12. https://www.eesel.ai/blog/zendesk-whatsapp
13. https://www.eesel.ai/blog/zendesk-security-and-compliance
14. https://www.eesel.ai/blog/zendesk-saas-enterprise
15. https://supp.support/blog/zendesk-pricing-2026-full-breakdown
16. https://www.supportbench.com/zendesk-enterprise-vs-supportbench-enterprise-security-compliance-audit/
17. https://www.zendesk.com.br/marketplace/apps/support/813236/vtex-by-bcrcx/
18. https://www.zendesk.com.br/marketplace/apps/support/147884/vtex-by-aktie-now/
19. docs/research/2026-05-06-omnichannel-helpdesk-landscape/02-research-report.md (sec 2.1)

## Data Quality

- **Features:** verified
- **Pricing:** current (BRL site + USD ref + AI per-resolution + contract terms)
- **Reviews:** recent (G2 6.000+; Capterra extenso)
- **Compliance:** verified (Trust Center publica)
- **Confidence global:** high
