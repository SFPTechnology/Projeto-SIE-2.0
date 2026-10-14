# Inventory — Chatwoot

**Snapshot:** 2026-05-06
**Versao avaliada:** v4.13.0 (release 2026-04-17)
**Categoria:** OSS omnichannel customer support + Cloud SaaS gerenciado
**License core:** MIT (mais permissiva da categoria)
**HQ:** Bangalore, India
**Fundado:** 2017 (~9 anos de maturidade)

## TL;DR

Chatwoot e o player OSS mais maduro de helpdesk omnichannel, com a unica licenca MIT do segmento, 29.1k stars no GitHub e Cloud SaaS oficial gerenciado. Stack Ruby on Rails + Vue.js. Pricing Cloud transparente ($0 → $99/agent/mo). Self-hosted gratis (so paga infra). WhatsApp via Meta Cloud API direct, Twilio ou 360Dialog. Captain AI nativo (auto-resolve, copilot, summarization). Trade-offs: marketplace menor, certificacoes compliance publicas ausentes, voice e add-on.

---

## 1. Vendor & Licensing

| Campo | Valor | Confidence |
|-------|-------|-----------|
| Empresa | Chatwoot Inc. | H |
| Pais | India | H |
| Fundacao | 2017 | H |
| Maturidade | ~9 anos | H |
| Licenca core | **MIT** | H |
| Modelo de negocio | OSS (MIT) + Cloud SaaS + Enterprise self-hosted (paid support) | H |

## 2. Canais nativos

| Canal | Suportado | Tier minimo | Notas |
|-------|-----------|-------------|-------|
| Live Chat (web widget) | ✅ | Hacker | Widget customizavel |
| Email | ✅ | Startups | IMAP/SMTP |
| **WhatsApp** | ✅ | Startups | 3 BSP options: Meta Cloud, Twilio, 360Dialog |
| Facebook Messenger | ✅ | Startups | OAuth + page subscription |
| Instagram DM | ✅ | Startups | Via Meta Business |
| Telegram | ✅ | Startups | Bot API |
| Line | ✅ | Startups | Native |
| SMS | ✅ | Startups | Via Twilio/Bandwidth |
| TikTok | ✅ | Startups | Native channel |
| API channel custom | ✅ | Startups | Build seu canal |
| Voice/Phone | ⚠️ | Enterprise (20+ agents) | Optional add-on |
| Apple Business Chat | ❌ | — | Nao suportado |
| Twitter/X | ❌ | — | Removido (X API pricing change) |

**Total nativos:** 10 canais nativos + voice opcional. Cobertura: a mais completa do segmento OSS.

### WhatsApp BSP options (diferencial)

Chatwoot tem arquitetura provider-pattern: `Channel::Whatsapp` model + service classes herdando de `Whatsapp::Providers::BaseService`. Isso permite:

| Provider | Setup | Templates | Embedded signup | Brasil-fit |
|----------|-------|-----------|-----------------|------------|
| Meta Cloud API (direct) | Embedded signup | ✅ sync_templates | ✅ | Disponivel BR |
| Twilio | Manual (SID + token) | ❌ NAO suportado | ❌ | Twilio BR available |
| 360Dialog | Manual API key | ✅ | ❌ | Conexao Germany |

[Source: deepwiki.com/chatwoot/chatwoot/7.4-whatsapp-channel, 2026-05-06]

**Significado pratico:** cliente escolhe seu BSP. Em BR, possivel conectar Take Blip/Zenvia via Cloud API ou custom wrap.

## 3. AI capabilities — Captain

| Feature | Descricao | Pricing |
|---------|-----------|---------|
| **Auto-resolve** | "Automate first-response conversations with AI that learns from your help center and FAQs" | Credits |
| **Co-Pilot** | "Draft, improve, or translate responses in one click" | Credits |
| **Smart FAQs** | Content gap analysis — automatically identifies common unanswered questions | Credits |
| **Memories** | Auto-summarizes key conversation details, tracks recurring issues per customer | Credits |
| **Multilingual** | Translates messages to any language instantly | Credits |

**Modelo de pricing:** credits inclusos no tier (300 / 500 / 800/mo) + $20 por 1.000 credits adicionais.

**Concern:** consumo exato de credits por feature (e.g., quantos credits = 1 auto-resolve vs 1 copilot suggestion) **nao publicado** no site oficial. Buyer assume cap soft sem visibilidade — risco para forecast TCO.

[Source: chatwoot.com/captain + chatwoot.com/pricing, 2026-05-06]

## 4. Pricing — Cloud SaaS

| Tier | Preco | Agents | Conversas/mo | Canais | Captain Credits | Retencao | SSO/SAML | Audit Logs | Teams/Automation/SLA |
|------|------:|--------|--------------|--------|----------------:|----------|:--------:|:----------:|:--------------------:|
| **Hacker** | $0/agent/mo | ate 2 | 500 | live chat only | 0 | 30 dias | ❌ | ❌ | ❌ |
| **Startups** | $19/agent/mo | unlimited | unlimited | **all** | 300 | 1 ano | ❌ | ❌ | ❌ (so help center) |
| **Business** | $39/agent/mo ⭐ | unlimited | unlimited | all | 500 | 2 anos | ❌ | ❌ | ✅ Teams + Automation + SLA |
| **Enterprise** | $99/agent/mo | unlimited | unlimited | all | 800 | 3 anos | ✅ | ✅ | ✅ + Agent Capacity |

**Add-ons:**
- Captain credits overage: $20 / 1.000 credits
- Voice/Video: Enterprise (20+ agents) optional

**Billing:** annual (mensal disponivel com markup nao publicado)

[Source: https://www.chatwoot.com/pricing, fetched 2026-05-06]

## 5. Pricing — Self-hosted

| Item | Custo |
|------|-------|
| License (MIT) | **$0 forever** |
| Infra minima (Docker Compose VPS) | ~$20-50/mo |
| Production-grade (PG managed + Redis + LB + S3) | ~$150-400/mo dependendo do scale |
| DevOps human time | Variavel — tipicamente 0.1-0.3 FTE no scale up |
| Captain AI self-hosted | Documentado configuravel; OpenAI API key cliente-fornecida (custos LLM separados) |
| Enterprise self-hosted edition (paid support) | Sob contato comercial direto |

**Self-hosted = MIT puro, todas as features sao do core open-source** (sem feature gating no source code). Diferenca vs Cloud: cliente assume ops + sem managed Captain.

## 6. Stack tecnico

| Camada | Tech | Confidence |
|--------|------|-----------|
| Backend | Ruby 46.1% (Rails) | H |
| Frontend | Vue.js 28.1% | H |
| JavaScript | 22.8% | H |
| Database | PostgreSQL | H |
| Cache/Queue | Redis + Sidekiq | H |
| Deploy | Docker / Heroku / Kubernetes | H |
| Telemetry | Built-in metrics + Sentry optional | H |

**Maturidade do codigo:**
- 6.119 commits no develop branch
- 266 PRs abertos
- 140+ contributors documented em releases
- Cadencia: minor releases mensais

[Source: github.com/chatwoot/chatwoot fetched 2026-05-06]

## 7. Comunidade & Reviews

| Metrica | Valor | Confidence |
|---------|-------|-----------|
| GitHub stars | **29.100** | H |
| GitHub forks | 7.200 | H |
| Open PRs | 266 | H |
| G2 rating | 4.4 / 5 | M |
| G2 review count | Nao disclosed em snapshots; estimado 200-400 | L |

**G2 top pros (review themes):**
- Cost-effectiveness (OSS pricing)
- Privacy via self-hosting
- Customization flexibility
- Easy integrations (Slack, email)
- Transparent pricing

**G2 top cons:**
- UI could improve
- Reporting less customizable
- AI automation pre-Captain era was thin (reviews podem ser dated)
- Connectivity issues no self-host (config errors)

## 8. Governance & Compliance

| Area | Status | Confidence |
|------|--------|-----------|
| SOC2 | Cloud: implicito (nao explicito em pagina publica) | M |
| ISO 27001 | Nao publicamente listado | M |
| GDPR DPA | Yes (Cloud + self-hosted EU residency = customer-controlled) | H |
| HIPAA BAA | **Nao oferecido publicamente** | H |
| EU hosting Cloud | **Regiao de hosting nao user-selectable em standard tiers** | M |
| Audit logs | Enterprise tier only ($99/mo) | H |
| SSO/SAML | Enterprise tier only ($99/mo) | H |

**Concern para regulated industries:** sem HIPAA BAA publico, sem ISO 27001 publica, sem regiao EU explicit Cloud. **Self-hosted e o escape valve** — cliente roda em sua propria regiao com seu proprio compliance posture.

## 9. Marketplace & Integracoes

Chatwoot **nao tem marketplace curado** (vs Zendesk 1.977 apps). Integracoes distribuidas:

| Tipo | Exemplos |
|------|----------|
| Native | Slack, Shopify, Dialogflow, Microsoft Teams, WordPress |
| Migration tools | Help Scout, Intercom |
| API | REST + webhooks universal |
| Plugins/apps | Apps/dashboard apps via SDK custom |

**API openness:** REST + webhooks abertos; self-host = arbitrary DB read.

**Trade-off:** ecosystem menor mas API e openness compensam para teams tecnicos. Para teams non-technical, marketplace gigante e diferencial real do Zendesk.

## 10. Support & SLA

| Tier | Support level |
|------|--------------|
| Community | GitHub Discussions, Discord, forum |
| Cloud Hacker/Startups | Email/chat best effort |
| Cloud Business+ | Email/chat com SLA publicado |
| Cloud Enterprise | CSM dedicado |
| Self-hosted Enterprise | Contrato paid support (preco sob consulta) |

## 11. Brasil-fit

| Dim | Status |
|-----|--------|
| WhatsApp BSP BR | ✅ via Cloud API (Meta) ou Twilio BR ou 360Dialog (BSP-Direct EU) |
| PT-BR UI | ✅ Community translation madura |
| Pricing BRL | ❌ (pricing $USD) |
| VTEX nativa | ❌ |
| Shopify nativa | ✅ |
| RD Station nativa | ❌ |
| Pix nativa | ❌ |
| Local support BR team | ❌ Community-driven |
| BYOC BR BSP | ✅ Cliente conecta Take Blip/Zenvia via Cloud API |

**Veredito BR:** estrutura permite operacao BR mas sem amenities BR-first (sem BRL pricing, sem VTEX, sem dedicated BR team).

## 12. Diferenciais unicos

1. **MIT license** — unica do segmento omnichannel maduro
2. **Self-hosted real** sem feature-gating no codigo
3. **Dual deployment** (Cloud + Self-hosted) com mesma feature set
4. **BYOC WhatsApp** (3 BSP options)
5. **Captain AI built-in** (nao add-on a la carte como Zendesk Copilot)
6. **Pricing transparente** sem hidden fees ($0/$19/$39/$99)

## 13. Weaknesses conhecidas

1. Captain AI credit consumption nao publicado (forecast opaco)
2. Marketplace muito menor que Zendesk (~tens vs ~1.977)
3. G2 review count visibilmente menor (cred com buyers enterprise)
4. Voice e add-on, nao first-class
5. Compliance certs publicas (ISO/FedRAMP) ausentes
6. Self-hosted exige Docker/DevOps competence
7. Twitter/X channel removido

## 14. Sources cited

- https://www.chatwoot.com/pricing (2026-05-06)
- https://www.chatwoot.com/captain (2026-05-06)
- https://github.com/chatwoot/chatwoot (2026-05-06)
- https://deepwiki.com/chatwoot/chatwoot/7.4-whatsapp-channel
- https://www.chatwoot.com/docs/product/channels/whatsapp/360dialog
- Tech-research report 02-research-report.md (2026-05-06)
