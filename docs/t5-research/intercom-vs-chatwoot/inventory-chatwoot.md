# Inventario — Chatwoot

**Data:** 2026-05-06
**Tipo:** Product
**Confidence:** High (estrutura) / Medium (AI performance comparativa)

## Identidade

| Dim | Valor |
|---|---|
| Nome | Chatwoot |
| Empresa | Chatwoot Inc. |
| Categoria | OSS + Cloud — Omnichannel customer engagement |
| Fundacao | 2017 (~9 anos) |
| Sede | India |
| Licenca | **MIT** (cloud + self-hosted) |
| Tagline | "AI-powered, open-source customer support platform" |
| URL | https://www.chatwoot.com |

## Pricing (2026-05-06, USD)

| Plano | $/agent/mo | Agents | Conversations | Captain credits | Retention |
|---|---:|---|---|---:|---|
| **Hacker (Free)** | $0 | Up to 2 | 500/mo | 0 (Captain NAO incluida) | 30 dias |
| **Startups** | $19 | Unlimited | Unlimited (fair use) | 300/mo | 1 ano |
| **Business** | $39 | Unlimited | Unlimited (fair use) | 500/mo | 2 anos |
| **Enterprise** | $99 | Unlimited | Unlimited (fair use) | 800/mo | 3 anos |
| **Self-hosted** | **$0** | Unlimited | Unlimited | **N/A — Captain NAO disponivel self-hosted** | Voce controla |

**Captain extras:** $20/1.000 credits.

**1 credit ~ 1 AI action** (resposta automatica, suggestion, summarization). Documentacao oficial nao detalha custo por tipo de acao.

**Self-hosted infra cost estimado:** $20-50/mo VPS (Docker/Heroku).

**Cobranca anual** para preco listado em Cloud.

## Feature Inventory (resumo)

### AI / Automation [MODERATE — em rapida evolucao 2026]
- Captain AI Agent (auto-resposta first-line)
- Captain Co-Pilot (agent-side draft/improve/translate)
- Smart FAQs (knowledge gap detection)
- Memories (auto-summarize)
- Query (Ask Co-Pilot)
- Automation rules (Business+)
- Auto-assignment, business hours, auto-responder

### Channels [DEEP — todos nativos]
- Live chat widget customizavel
- Email
- **WhatsApp Business Cloud API** (BYOC — cliente conecta WABA via BSP)
- Facebook Messenger
- Instagram DM
- **Telegram nativo** (Intercom nao tem)
- Line
- SMS (via Twilio)
- **TikTok nativo**
- API Channels custom

### Help Center / Knowledge [MODERATE]
- Help center (Startups+)
- Multilingual
- Captain reads como RAG source

### Ticketing / Inbox [DEEP]
- Conversations unificadas
- Private notes, mentions, labels, shortcuts
- Canned responses, command bar
- Teams (Business+)
- SLA support (Business+)
- Custom views/filters (Startups+)

### Campaigns [MODERATE]
- Campaigns (Startups+)
- Advanced campaigns (Business+)
- Pre-chat forms (Business+)
- WhatsApp outbound

### Reporting & Analytics [BASIC-MODERATE]
- Live reporting (Hacker)
- CSAT reviews (Business+)
- Conversation reports
- **G2 reviewers citam reporting como ponto fraco**

### Enterprise / Compliance [DEEP em self-hosted]
- SSO + SAML (Enterprise Cloud)
- Audit logs (Enterprise)
- Agent capacity management (Enterprise)
- **Self-hosted = data sovereignty completa**

### Voice / Video [BASIC]
- Video/voice support (Enterprise)

## Captain AI — deep specs

| Aspecto | Detalhe |
|---|---|
| Modelo | **NAO disclosed** (vendor nao publica se OpenAI, Anthropic, ou proprio) |
| RAG sources | Help center, past chats, FAQs |
| RAG pipeline detalhado | NAO publicado |
| Deflection rate | **NAO publicado oficialmente** |
| Capacidades | Auto-resposta + Co-Pilot + Smart FAQs + Memories + Query |
| Linguagens | 8+ marketing-demonstradas (incluindo **Portuguese**) + Malayalam |
| Treinamento | Help center + chats + FAQs |
| Hallucination control | Nao endereado publicamente |
| Escalation | Hands off basico to human |
| Credits system | 300/500/800 por tier; $20/1.000 extras |
| Playground | Sim; **falta simulation mode** robusto contra past questions |
| Self-hosted | **NAO disponivel** — exclusivo Cloud |
| Weaknesses (third-party) | Sem autonomous workflows, sem custom actions, advanced routing limitado, sem forecast deflection antes go-live |

## Reviews

| Fonte | Rating | Reviews/Stars |
|---|---|---|
| G2 | 4.4/5 | 200+ |
| Capterra | 4.6/5 | 100+ |
| GitHub | N/A | **29.100 stars, 7.200 forks, 6.119 commits, v4.13.0 (Apr 17 2026)** |

**Trusted by claim:** 15.000+ businesses.

**Top praise (G2):**
- Open source flexibility
- Self-hosting option
- WhatsApp/Telegram nativos
- Cost effectiveness
- Easy Slack/email integration

**Top complaints (G2):**
- UI not as polished as Intercom
- Reporting/Analytics weak
- Portal disconnects occasionally
- Account manager only com 20+ agents

## Integracoes

- **API:** REST
- **Webhooks:** Sim
- **Marketplace:** **NAO existe formal** — integracoes via API/webhooks
- **Key:** Slack, DialogFlow, Twilio, custom via API, WABA via BSP escolhido pelo cliente
- **SDKs:** JavaScript core; Ruby/Python/PHP community
- **In-app SDK:** Widget chat only (sem messenger SDK profundo)

## Stack tecnica

- **Linguagens:** Ruby (46%), Vue (28%), JavaScript (23%)
- **DB:** PostgreSQL + Redis
- **Deploy:** Docker, Heroku, Kubernetes (community)

## Compliance / Enterprise

- GDPR claims (Cloud + self-hosted)
- LGPD/HIPAA/PCI possivel via self-hosted (depende da infra)
- Sem certificacao SOC2/ISO publica do Cloud
- **Self-hosted = total controle** (advantage absolute)

## Diferenciais vs Intercom

1. **Self-hosted MIT** — data sovereignty + $0 license
2. Free tier permanente + free self-hosted unlimited
3. **Telegram nativo** (Intercom NAO tem)
4. TikTok channel nativo
5. **BYOC WhatsApp** — conecta WABA propria sem markup
6. Source code modificavel — custom UI/integrations sem limite
7. Pricing tier 50-65% mais barato para mesmo headcount
8. **5x menor cost para SMB (5 agents)**
9. API Channels para canais custom
10. Comunidade open-source contribuindo

## Fraquezas vs Intercom

1. **Captain AI sem modelo publicado** nem deflection rate (Fin tem ambos)
2. Captain sem autonomous workflows nem custom actions
3. **Captain NAO disponivel em self-hosted** — quebra promessa OSS pura
4. Reporting/Analytics fraco
5. Sem marketplace formal
6. In-app Messenger SDK menos polido
7. Sem HIPAA out-of-box, sem multibrand (Cloud)
8. Pre-built reports menos polished
9. Setup self-hosted exige Docker/DevOps
10. Sem simulation mode para forecast deflection
11. Sem case studies enterprise visiveis (Intercom tem Lightspeed publico)

## Sources

- https://www.chatwoot.com/pricing (consultado 2026-05-06)
- https://www.chatwoot.com/captain/ (consultado 2026-05-06)
- https://github.com/chatwoot/chatwoot
- https://www.g2.com/products/chatwoot/reviews
- https://www.eesel.ai/blog/chatwoot-captain (third-party overview)
- docs/research/2026-05-06-omnichannel-helpdesk-landscape/02-research-report.md (secao 2.4)
