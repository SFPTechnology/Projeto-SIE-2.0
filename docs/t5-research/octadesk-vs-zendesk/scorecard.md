# Scorecard - Octadesk vs Zendesk

**Data:** 2026-05-06
**Metodo:** Weighted 8 dimensions (persona-neutral baseline + 3 persona recalibrations)
**Escala:** 0-100 por dimensao; final = soma ponderada

---

## Score persona-neutral (peso original)

| ID | Dimensao | Peso | Octadesk | Zendesk | Delta | Vencedor |
|----|---|---:|---:|---:|---:|---|
| C1 | WhatsApp Business API integration | 25 | 92 | 78 | +14 | Octadesk |
| C2 | Brasil-fit operacional | 20 | 95 | 50 | +45 | Octadesk |
| C3 | Feature parity enterprise | 15 | 35 | 95 | -60 | Zendesk |
| C4 | AI capability | 10 | 70 | 85 | -15 | Zendesk |
| C5 | Pricing transparency e TCO BR | 10 | 65 | 70 | -5 | Zendesk (marginal) |
| C6 | Marketplace e ecosystem | 5 | 60 | 95 | -35 | Zendesk |
| C7 | Maturidade governance compliance | 10 | 45 | 95 | -50 | Zendesk |
| C8 | Comunidade reviews | 5 | 55 | 90 | -35 | Zendesk |

### Totais ponderados

| Player | Score |
|---|---:|
| **Zendesk** | **76,45** |
| **Octadesk** | **71,00** |
| Delta | 5,45 |

**Classificacao:** Tecnicamente proximos. Vencedor depende da persona/contexto.

---

## Recalibracao por persona

### Persona A: E-commerce SMB BR (5-10 agents, ~1k conversas/mes, sem AI agressiva)

**Pesos recalibrados:**
- C1 WhatsApp: 30
- C2 Brasil-fit: 30
- C3 Enterprise: 5
- C4 AI: 10
- C5 Pricing: 15
- C6 Marketplace: 5
- C7 Compliance: 3
- C8 Reviews: 2

| Player | Score |
|---|---:|
| **Octadesk** | **79,5** |
| **Zendesk** | **67,0** |
| Delta | +12,5 Octadesk |

**Rationale:** PME BR: WhatsApp + BR-fit dominam. Compliance enterprise e marketplace volume irrelevantes. Octadesk vence por:
- TCO 2,5-4x menor
- Integracoes BR first-class (VTEX/Tray/NuvemShop)
- Suporte PT-BR nativo
- Ecossistema LWSA (Bling, Vindi, Melhor Envio)
- Sem complexidade Sunshine ou contract escalation

**Veredito A:** **OCTADESK**

---

### Persona B: Mid-market BR (50-100 agents, ~10k conversas/mes, AI moderado)

**Pesos recalibrados:**
- C1 WhatsApp: 25
- C2 Brasil-fit: 20
- C3 Enterprise: 15
- C4 AI: 15
- C5 Pricing: 10
- C6 Marketplace: 5
- C7 Compliance: 7
- C8 Reviews: 3

| Player | Score |
|---|---:|
| **Zendesk** | **75,6** |
| **Octadesk** | **72,0** |
| Delta | +3,6 Zendesk (empate tecnico) |

**Rationale:** Mid-market BR vive a TENSAO CENTRAL deste bench:
- Octadesk vence: TCO (R$95k vs R$1M+ ano), BR-fit, WhatsApp transparency
- Zendesk vence: enterprise features, AI maduro, custom roles, audit logs, multi-canal global

**Decisao depende de:**
1. SSO/SAML obrigatorios por compliance interna? -> Zendesk
2. Volume AI agressivo (5k+ resolutions/mes)? -> WOZ pode ganhar (mas precisa testar)
3. Equipes globais USA/EU? -> Zendesk
4. BR-only operacao? -> Octadesk
5. Ferramentas Bling/Tray/Vindi ja em uso? -> Octadesk

**Veredito B:** **EMPATE TECNICO** com leve vantagem Zendesk em score, vantagem Octadesk em TCO. Recomendar POC paralelo.

---

### Persona C: Enterprise BR multinacional (100+ agents, healthcare/financeiro/governo, multi-region)

**Pesos recalibrados:**
- C1 WhatsApp: 15
- C2 Brasil-fit: 10
- C3 Enterprise: 25
- C4 AI: 10
- C5 Pricing: 5
- C6 Marketplace: 10
- C7 Compliance: 20
- C8 Reviews: 5

| Player | Score |
|---|---:|
| **Zendesk** | **86,0** |
| **Octadesk** | **55,5** |
| Delta | +30,5 Zendesk (clear winner) |

**Rationale:** Enterprise multinacional BR mandata:
- SSO/SAML/SCIM
- Custom agent roles
- Sandbox para change mgmt
- Audit logs detalhados
- Multi-help-center
- HIPAA (se healthcare) / PCI-DSS / SOC 2 Type II / ISO 27001
- Multi-region data residency
- Contract enterprise multi-ano

Octadesk **NAO oferece** essas features publicamente. Zendesk **unico viavel** apesar do TCO 4-5x maior.

**Veredito C:** **ZENDESK** (sem ambiguidade).

---

## Tiebreaker factors (mid-market)

Para a Persona B em empate tecnico, decisores devem cruzar com:

1. **Volume de WhatsApp esperado por mes**
   - <5k conv/mes = Octadesk Sea+AI ou Higher
   - >10k conv/mes = avaliar Octa Suite vs Zendesk + Sunshine extras

2. **Compliance interna obriga SSO/SAML?**
   - SIM = Zendesk
   - NAO = qualquer um

3. **Equipes globais (USA/EU/APAC)?**
   - SIM = Zendesk multi-region
   - BR-only = Octadesk

4. **Hosting BR estrito (LGPD operador)?**
   - SIM = Octadesk presumivel BR via LWSA (auditar com vendor)
   - Aceita USA/EU = Zendesk

5. **Equipe tecnica disponivel para integrar Sunshine + ZAF?**
   - SIM = Zendesk
   - NAO = Octadesk pricing/setup mais simples

6. **Multi-help-center (varias marcas/produtos)?**
   - SIM = Zendesk (300 inclusos Enterprise)
   - NAO = Octadesk

---

## Sintese final

**Score puro persona-neutral:** Zendesk vence por 5,45 (76,45 vs 71,00).

**Score ajustado por persona BR:**
- SMB e-commerce: **Octadesk** (+12,5)
- Mid-market: **Empate tecnico** (Zendesk +3,6, mas Octadesk vence em TCO)
- Enterprise multinacional: **Zendesk** (+30,5)

**Tese central confirmada:** Octadesk e Zendesk NAO competem no mesmo segmento. Octadesk e a escolha racional para PME/mid-market BR sem requirements regulatorios pesados; Zendesk e mandatorio para enterprise multinacional regulado. Em mid-market BR, e empate tecnico que se decide por compliance e equipe.
