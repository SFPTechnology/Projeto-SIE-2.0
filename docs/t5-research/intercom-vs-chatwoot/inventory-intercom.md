# Inventario — Intercom

**Data:** 2026-05-06
**Tipo:** Product
**Confidence:** High

## Identidade

| Dim | Valor |
|---|---|
| Nome | Intercom |
| Empresa | Intercom Inc. |
| Categoria | SaaS — AI-first customer messaging & support |
| Fundacao | 2011 (~15 anos) |
| Sede | EUA |
| Licenca | Proprietary |
| Tagline | "The complete AI-first customer service solution" |
| URL | https://www.intercom.com |

## Pricing (2026-05-06, USD)

| Plano | $/seat/mo | Conteudo destaque |
|---|---:|---|
| Essential | $29 | Messenger + shared inbox + ticketing + help center + Fin AI included (cobrado per resolution) |
| Advanced | $85 | + multiple inboxes + workflows + round-robin + multilingual help center + 20 lite seats free |
| Expert | $132 | + SSO + HIPAA + SLAs + multibrand + 50 lite seats free |

**Fin AI Agent:** **$0.99 por resolucao** (cobrado quando customer confirma resolucao OU nao pede ajuda em 24h OU Fin completa workflow). All tiers.

**Add-ons:**
- Copilot: $29/agent/mo (10 conv/mo free) — agent-side AI assistant
- Pro Analytics: $99/mo (1.000 conv conversation analytics)
- Proactive Support Plus: $99/mo (500 in-app messages, Product Tours, Surveys, Checklists) — **necessario para outbound WhatsApp**

**Sem free tier permanente.** 14-day trial only.

**Custos reais G2 reportam 60-80% acima do sticker** — combinacao Fin per-resolution + Copilot + Proactive Support Plus + WhatsApp Meta fees.

## Feature Inventory (resumo)

### AI / Automation [DEEP]
- **Fin AI Agent** — Fin Apex 1.0 model proprietary
- Fin Copilot (agent-side AI)
- AI workflows (Advanced+)
- Smart suggestions / autotranslate

### Channels [DEEP em-app, MODERATE omnichannel]
- **In-app Messenger** (best-in-class — sem rival)
- Web chat
- Email shared inbox
- WhatsApp Business Cloud API (oficial Meta direct)
- Instagram DM
- Facebook Messenger
- SMS
- **Telegram NAO suportado nativamente**

### Help Center / Knowledge [DEEP]
- Help center publico
- Multilingual help center (Advanced+)
- Articles + collections
- Fin reads from help center as RAG source

### Ticketing [MODERATE]
- Shared inbox (Essential)
- Multiple inboxes (Advanced+)
- SLAs (Expert)
- Round-robin assignment (Advanced+)

### Proactive Support [DEEP]
- Outbound messages (banners, tooltips, in-app)
- Product Tours, Surveys, Checklists (add-on)
- Outbound WhatsApp campaigns (requer add-on)

### Reporting & Analytics [DEEP]
- Pre-built reports
- Custom reports (Pro add-on)
- Conversation insights, agent dashboards, SLA tracking, trends

### Enterprise / Compliance [DEEP em Expert]
- SSO + identity (Expert)
- HIPAA, SLAs, multibrand (Expert)
- ISO 27001/27018/27701, GDPR, CCPA, SOC2 Type II

## Fin AI — deep specs

| Aspecto | Detalhe |
|---|---|
| Modelo | **Fin Apex 1.0** (proprietary, patented) |
| Engine | Fin AI Engine — patented retrieval/reranker |
| RAG pipeline | 6 steps — query refinement, retrieval (fin-cx-retrieval), reranking (fin-cx-reranker), generation (Fin Apex 1.0), accuracy validation, optimization |
| Deflection rate publicado | **51% medio** (research aggregators); ate 67% maduro; testimonial Lightspeed cita 65% end-to-end |
| Improvement claim | +1% resolution rate / mes |
| Linguagens | Multiple (lista oficial nao publicada); pt-BR vs pt-PT requer tooling adicional |
| Treinamento | Fin Flywheel — RAG sobre help center + procedures + policies |
| Hallucination control | Step 5 (validate accuracy) — sem detalhes publicos |
| Escalation | Hands off ao agent inbox; honra assignment rules |
| Standalone mode | Disponivel em Zendesk/Salesforce/HubSpot/Freshdesk via integracao |
| Setup time | "Under 1 hour" (fin.ai) |

## Reviews

| Fonte | Rating | Reviews |
|---|---|---|
| G2 | 4.5/5 | 5.000+ |
| Capterra | 4.5/5 | 1.000+ |

**Top praise (G2):**
- Fin feels human-like, not typical AI
- Beautiful, modern interface
- Quick escalation
- Polished workflows

**Top complaints (G2):**
- Setup complexity vs alternatives
- Pricing surprises (real bill 60-80% acima sticker)
- Per-resolution AI imprevisivel sem volume
- Hidden costs em add-ons

## Integracoes

- **API:** REST + GraphQL
- **Webhooks:** Sim
- **App Store:** 300+ apps
- **Key:** Salesforce, HubSpot, Slack, Stripe, GitHub, Jira, Zapier, Segment, Mixpanel
- **SDKs:** JavaScript, iOS, Android, React Native, Flutter
- **In-app SDK:** Best-in-class — Messenger SDK roda em qualquer SaaS

## Compliance / Enterprise

- SOC2 Type II, GDPR, HIPAA, ISO 27001/27018/27701, CCPA
- SSO, SAML, audit logs (Expert)
- Data residency: EU + US options (Expert)

## Diferenciais vs Chatwoot

1. In-app Messenger SDK best-in-class
2. Fin AI Apex 1.0 com modelo proprietary publicado + RAG patentes
3. Deflection rate publicado (51-67%)
4. Pre-built reports + Pro analytics
5. Multibrand support (Expert)
6. Marketplace 300+ apps polished
7. HIPAA + SOC2 + ISO certs em pacote enterprise

## Fraquezas vs Chatwoot

1. Sem free tier permanente
2. Sem self-hosted / OSS option — total vendor lock-in
3. Sem licenca aberta
4. Per-resolution AI imprevisivel
5. Telegram NAO suportado nativamente
6. Sem comunidade open-source

## Sources

- https://www.intercom.com/pricing (consultado 2026-05-06)
- https://fin.ai/ (consultado 2026-05-06)
- https://www.g2.com/compare/chatwoot-vs-fin-by-intercom
- docs/research/2026-05-06-omnichannel-helpdesk-landscape/02-research-report.md (secao 2.1)
