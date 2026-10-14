# Inventario - Octadesk

**Data:** 2026-05-06
**Bench:** octadesk-vs-zendesk
**Tipo:** product
**Confidence global:** medium-high

---

## Identidade

| Campo | Valor |
|---|---|
| Nome | Octadesk |
| Empresa | LWSA (Locaweb group) |
| Categoria | Customer service / helpdesk SaaS para PME e e-commerce BR |
| Lancamento | ~2014 (~12 anos) |
| Pais origem | Brasil |
| Target | PMEs brasileiras, e-commerces, equipes marketing+sales+aftersales |
| Tagline | "Resolva 8 a cada 10 atendimentos automaticamente, 24h por dia" |
| URL | https://www.octadesk.com |
| Customer base claim | "+2.500 empresas" (logos: Locaweb, Pfizer, QuintoAndar) |
| Grupo controlador | LWSA: Locaweb, Bling, Tray, Vindi, Octadesk, Melhor Envio, Etus, Yapay |

---

## Features

### Categorias

**Conversas omnichannel (deep)**
- WhatsApp Business API oficial Meta
- Instagram Direct
- Facebook Messenger
- Email
- Webchat (site)

**Helpdesk ticketing (moderate)**
- SLA configuravel por grupo e tipo de demanda
- Help center / base de conhecimento
- Tickets unificados de email + chat + WhatsApp

**Automacao (moderate)**
- Chatbots configuraveis
- Integracoes via tarefas automatizadas
- Bot creation declarado intuitivo (Capterra reviews)

**WOZ Agent - AI nativa (moderate)**
- Atendimento autonomo IA generativa 24/7
- Sugestao de respostas em tempo real (copilot)
- Transcricao automatica de audios em texto
- Baseado em ChatGPT (G2 product description)
- Identifica lacunas e melhora respostas continuamente
- Isolamento de dados entre clientes (declarado)

**Octa Suite (deep, gated)**
- Operacoes multi-time/multi-departamento
- Automacao avancada
- Branch management (filiais)
- Integracoes ERP e CRM profundas
- CSM dedicado

### Diferenciais unicos
- WhatsApp Business API oficial Meta declarado no site (sem intermediario BSP cinza)
- Tracao com e-commerce BR (logos Pfizer, Locaweb, QuintoAndar)
- Pacote LWSA group: ecossistema BR de e-commerce (Bling ERP, Tray e-com, Vindi, Melhor Envio, Yapay)
- WOZ AI generativa nativa em PT-BR
- UX em portugues nativo end-to-end (sem traducao de SaaS gringo)

**Total features estimado:** ~35
**Confidence:** H em features publicas; M em Suite (gated atras de contato comercial)

---

## Pricing

### Site oficial (octadesk.com/precos, 2026-05-06)

| Plano | Entry mensal BRL | Escopo | Agentes |
|---|---:|---|---|
| Octa Conversas | R$ 1.542 | WhatsApp + Insta + FB + chat site | nao detalhado |
| Octadesk Helpdesk | R$ 2.205 | Email + chat + help center + WhatsApp | nao detalhado |
| Octa Suite | contato comercial | Multi-time + branch + ERP/CRM + CSM | nao publico |

### G2 pricing scrape (last update 2025-10-28)

| Plano | Entry mensal BRL | Users | WA conversations/mes | WA numbers |
|---|---:|---:|---:|---:|
| Sea + AI Plan | R$ 2.972 | 30 | 2.000 oficial | 1 |
| Higher Tier | nao publico | 50 | 5.000 oficial | 1 |

### Add-on
- **WOZ Agent**: pricing nao publico (contato comercial), modelo AI agent autonomo + copilot, separado do plano base

### Free tier
- Free tier: nao
- Trial: nao publico explicito (provavel demo agendada)

### **Discrepancia critica versus tech-research**

Tech-research listou "a partir de R$79/mes". Site oficial em 2026-05-06 mostra entry **R$1.542/mes** (Conversas). Desvio de ~20x. **Atualizar tech-research e curiosity_queue.**

Hipoteses para a discrepancia:
1. R$79/mes era um plano antigo descontinuado (2023-2024)
2. R$79 era ad spend do tech-research aplicado a outro player
3. Promo temporaria nao mais ativa

**Sources:**
- https://www.octadesk.com/precos (oficial)
- https://www.g2.com/products/octadesk/pricing (mirror G2)

**Confidence:** H site (Conversas/Helpdesk); M Sea+AI G2 (mirror que pode estar levemente desatualizado mas ordem de grandeza coerente); L Octa Suite

---

## Integrations

### API
- REST disponivel
- Webhooks: SIM
- Documentacao: developers.octadesk.com (provavel; nao verificado fonte primaria)

### Marketplace
- Pagina /integracoes ativa
- Estimativa: 20-30 integracoes catalogadas

### Integracoes nativas declaradas

| Categoria | Integrations |
|---|---|
| E-commerce BR | VTEX, Tray, NuvemShop, Shopify, Magento |
| CRM | Salesforce, HubSpot, Pipedrive, RD Station |
| Marketing | ActiveCampaign, RD Station |
| Ecossistema LWSA | Bling (ERP, mesmo grupo), Vindi (assinaturas), Melhor Envio (logistica), Tray (e-com) |

### Gaps verificacao
- **VTEX native oficial Octadesk:** mencionado em /integracoes mas profundidade nao auditada
- **Conta Azul native:** nao confirmado em fonte primaria
- **Bling native oficial:** esperado (mesmo grupo LWSA) mas nao auditado em pagina dedicada

**SDK languages:** nao publico (provavel REST direto)
**Plugin system:** nao
**Source:** https://www.octadesk.com/integracoes
**Confidence:** H lista nominal; M profundidade

---

## User Experience

| Dimensao | Valor |
|---|---|
| Onboarding | good (Capterra: "super facil de utilizar", implementacao rapida) |
| UI quality | modern (interface assemelha-se a WhatsApp; PT-BR nativa) |
| Learning curve | low-moderate |
| Mobile app | sim |
| Offline support | nao publico |
| Acessibilidade | nao publico |
| Idioma nativo PT-BR | SIM (vantagem clara vs incumbents traduzidos) |

**Source:** Capterra Brazil + G2
**Confidence:** M (sample size pequeno: 6 reviews Capterra BR)

---

## Reviews

### G2

- **Reviews:** 55 (G2 product page; rating exato bloqueado por 403)
- **Top praises:** Ease of Use, Features, Easy Integrations, Easy Implementation
- **Top complaints:** Limited Features, Feature Issues, Limited Customization, Chatbot Issues, Instabilidades/outages

### Capterra Brasil

- **Rating:** 4.0/5
- **Reviews:** 6
- **Value score:** 4.3/5
- **Support score:** 3.7/5
- **Recommendation rate:** 80%

**Top praises:**
- Multi-channel unification ("unite numerous types of chat in one place")
- Ease of use ("super facil de utilizar")
- Pricing better than Freshdesk/Zendesk (visao operador BR)
- Bot creation intuitive

**Top complaints:**
- Stability issues / disconnections / slowdowns reportados (long-term user 4+ anos)
- Limited native integrations (some require API config)
- Weak audio alerts for notifications
- Outages com frequencia aumentada no ultimo ano

**Source:** https://www.capterra.com.br/software/192993/octadesk + G2
**Confidence:** M (sample BR muito pequeno; sinal de instabilidade recorrente em multiplas reviews merece atencao)

---

## Scalability & Enterprise

### Limites publicos

| Plano | Users | WA conversations/mo | Numeros WA |
|---|---:|---:|---:|
| Sea + AI | 30 | 2.000 | 1 |
| Higher | 50 | 5.000 | 1 |
| Suite | nao publico | nao publico | nao publico |

### Enterprise features declaradas
- Branch management (filiais) - Octa Suite
- ERP/CRM integracoes profundas - Octa Suite
- CSM dedicado - Octa Suite

### Gaps enterprise versus Zendesk (CRITICOS)

**Nao publicos / nao confirmados:**
- SSO/SAML/OIDC
- SCIM provisioning
- Custom agent roles
- Audit logs detalhados
- Sandbox environment
- Multi-help-center
- BYOK encryption
- HIPAA BAA (esperado nao oferecer)
- PCI-DSS
- SOC 2 Type II report
- ISO 27001 (apenas LGPD declarada via LWSA group)

### Compliance publica
- **LGPD:** declarada via parent LWSA + pagina dedicada pt.octadesk.com/lgpd
- **GDPR:** declarada para WOZ
- **SOC 2 / ISO 27001:** nao publicamente confirmado

### Data residency
- Presumivel BR via parent LWSA (Locaweb hosting BR conhecido)
- Nao auditado em fonte primaria

**Source:** https://pt.octadesk.com/lgpd + WebSearch + G2 pricing
**Confidence:** L para enterprise features (gaps prevalecentes); H para LGPD declaration

---

## Support & Community

| Dimensao | Valor |
|---|---|
| Docs quality | good (loop.octadesk.com ativo) |
| Channels | chat, email, central de ajuda, WhatsApp suporte (provavel) |
| Language | PT-BR nativo (vantagem clara vs incumbents) |
| Community | forum/help center; size nao publico |
| Knowledge base | sim |
| Status page | nao confirmado |
| CSM dedicado | apenas tier Octa Suite |

**Source:** https://loop.octadesk.com
**Confidence:** M

---

## AI nativa - WOZ Agent

| Atributo | Valor |
|---|---|
| Nome | WOZ Agent |
| Engine declarado | ChatGPT-based (G2 product description) |
| Modos | Autonomous answer, Copilot suggest, Audio transcription, Continuous learning |
| Language | PT-BR nativo |
| Deflection rate publicado | nao publico (claim 80% marketing geral, nao validado em benchmark independente) |
| Pricing model | add-on separado, contato comercial |
| Data isolation | declarada |
| Performance vs Fin/Captain/Zendesk AI | nao testado em benchmark publico independente |

**Source:** homepage octadesk.com + G2
**Confidence:** H para existencia; M para performance/pricing real

---

## WhatsApp Integration

| Atributo | Valor |
|---|---|
| Oficial Meta declarado | SIM |
| BSP role | Octadesk atua como BSP integrado a Cloud API Meta |
| Cloud API only | SIM (compatibilidade post-Oct-2025 sunset on-premise) |
| Message pricing passthrough | SIM (Meta charges + Octadesk plan) |
| Free 24h service window | padrao Meta |
| Template approval flow | padrao Meta |
| Multi-agent same number | implicito por design |
| Tier lock | Sea+AI 2.000 conv/mes; Higher 5.000 conv/mes (overage) |

**Source:** homepage octadesk.com + G2 + WebSearch confirmacao
**Confidence:** H para oficialidade Cloud API; M para detalhes BSP fee

---

## Sources Consulted

1. https://www.octadesk.com (homepage)
2. https://www.octadesk.com/precos
3. https://www.octadesk.com/integracoes
4. https://pt.octadesk.com/lgpd
5. https://www.octadesk.com/politicas
6. https://www.octadesk.com/termos-uso
7. https://blog.octadesk.com
8. https://loop.octadesk.com
9. https://www.g2.com/products/octadesk/reviews
10. https://www.g2.com/products/octadesk/pricing (last update 2025-10-28)
11. https://www.capterra.com.br/software/192993/octadesk
12. https://www.zohoflow.com/apps/octadesk/integrations/shopify
13. docs/research/2026-05-06-omnichannel-helpdesk-landscape/02-research-report.md (sec 2.3)

## Data Quality

- **Features:** verified
- **Pricing:** current partial (tier publico H, Suite L)
- **Reviews:** recent partial (G2 55; Capterra BR 6)
- **Compliance:** declarative (LGPD declarada; SOC2/ISO27001 nao confirmado)
- **Confidence global:** medium-high para nucleo BR; medium-low para enterprise gaps
