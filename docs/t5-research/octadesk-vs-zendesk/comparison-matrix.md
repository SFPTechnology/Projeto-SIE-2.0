# Comparison Matrix - Octadesk vs Zendesk

**Data:** 2026-05-06
**Cambio assumido:** USD 1 = BRL 5,05

---

## Tabela mestre dimensao por dimensao

| Dimensao | Octadesk | Zendesk | Veredito |
|---|---|---|---|
| **WhatsApp Cloud API** | Cloud API oficial Meta DIRETO (Octadesk como BSP integrador). Tier lock 2.000-5.000 conv/mes. PT-BR. [H] | Cloud API oficial via Sunshine Conversations BSP layer. Translation layer adiciona pricing variable + complexidade. [H] | **Octadesk: integracao mais direta e transparente.** Zendesk: ecossistema multichannel maior mas Sunshine fee. |
| **Brasil-fit** | BR-native end-to-end: PT-BR, BRL, integracoes BR, ecossistema LWSA, time local, 2.500+ empresas BR [H] | Localizacao BRL no pricing; produto traduzido. Add-ons em USD. Integracoes BR via PARCEIROS. Sem time local de produto. [H] | **Octadesk vence claramente.** |
| **Pricing transparency** | Site /precos: R$1.542 (Conversas), R$2.205 (Helpdesk). G2 mirror: Sea+AI R$2.972 (30 users + 2k conv). Suite gated. WOZ gated. [H/M] | 4 tiers BRL (R$135-R$1.105). Add-ons USD listados. AI per-resolution $1.50/$2.00. Contract terms agressivos. [H] | **Empate complexo.** Zendesk mais granular publico; Octadesk mais simples e Suite gated. |
| **TCO 10 agents 1 ano (sem AI)** | R$ 35.664 (Sea+AI bundle, sub-utilizado) [M] | R$ 90.600 (Suite Pro x 10 x 12) [H] | **Octadesk ~2,5x mais barato em mid-market BR.** |
| **TCO 10 agents 1 ano (com AI agressiva)** | R$ 35.664+ + WOZ gated (proj. R$50-80k) [L] | R$ 281.790 (eesel.ai math) [H] | **Octadesk tende a 3-4x mais barato.** Confidence baixo no WOZ. |
| **Channels nativos** | WhatsApp + Insta + FB + Email + Webchat (5 BR-relevantes) [H] | Email + Chat + Voice + WhatsApp + Insta + FB + Twitter + Apple BC + LINE + SMS (10+) [H] | **Zendesk mais canais; Octadesk os BR-relevantes.** |
| **AI capability** | WOZ Agent (ChatGPT-based). Autonomous + copilot + audio transcribe. Deflection nao benchmarked [M] | Zendesk AI Agents Essential (Suite) + Advanced (paid) + Copilot $50. Deflection 40-80% benchmarked Fin Labs [H] | **Zendesk com AI mais maduro/transparente.** WOZ tem PT-BR nativo mas dados limitados. |
| **Marketplace e ecosystem** | 20-30 integracoes + ecossistema LWSA (Bling, Vindi, Melhor Envio, Yapay) [M] | 1.500+ apps + Sunshine + ZAF + SDK em 4 linguagens [H] | **Zendesk em volume; Octadesk em depth BR.** |
| **Enterprise security e compliance** | LGPD declarada via LWSA + WOZ data isolation. SOC2/ISO27001 NAO publicos [M] | ISO 27001:2022 + 27017 + 27018 + 27701 + 42001 + CSA STAR AI + GDPR BCR + HIPAA + PCI-DSS + FedRAMP + LGPD + SOC 2 Type II [H] | **Zendesk vence sem comparacao.** |
| **Custom roles + sandbox + audit logs** | Nao publicos [L] | Custom agent roles + audit logs + sandbox 2 incluso em Enterprise (R$1.105) [H] | **Zendesk vence claramente.** Para enterprise regulado BR, Octadesk fica fora. |
| **HIPAA / PCI-DSS / FedRAMP** | Nao oferecidos [H gap] | HIPAA via BAA + Advanced Compliance + PCI-DSS redaction + FedRAMP LI-SaaS [H] | **Zendesk unico viavel para healthcare US ou gov.** |
| **Maturidade e marca** | 12 anos BR / 2.500+ empresas / parte LWSA [H] | 19 anos global / 14,8% market share / lider categoria [H] | **Zendesk global; Octadesk no BR mid-market empate.** |
| **Comunidade reviews** | G2: 55 reviews \| Capterra BR: 6 reviews 4,0/5 [M] | G2: 6.000+ reviews 4,3/5 \| Capterra 4,5/5 \| TrustRadius 8,7/10 [H] | **Zendesk vence em volume/credibilidade.** Octadesk sample BR concordante (good value, instabilidade). |

---

## Sumario

### Octadesk vence em
- Brasil-fit operacional
- TCO BR mid-market (2,5x-4x mais barato)
- WhatsApp setup transparency
- BR ecosystem (LWSA group)
- PT-BR nativo end-to-end

### Zendesk vence em
- Channels nativos (10+ vs 5)
- AI capability transparency e benchmarks publicos
- Marketplace volume (1.500+ apps)
- Enterprise security e compliance auditados
- Custom roles + sandbox + audit logs
- HIPAA + PCI-DSS + FedRAMP
- Maturidade e share global
- Comunidade reviews volume

### Empates
- AI capability funcional (vantagem Zendesk em transparencia/benchmark)
- Maturidade no contexto BR mid-market

### Octadesk gaps criticos
- SOC 2 / ISO 27001 ausentes
- SSO/SAML/SCIM nao publicos
- Custom roles / audit logs / sandbox nao publicos
- Data residency BR nao auditada
- Marketplace ~50x menor
- WOZ deflection nao benchmarked
- Sample reviews limitado

### Zendesk gaps criticos para BR
- Add-ons em USD (FX risk)
- Sunshine pricing complexity (variavel)
- BR connectors via PARCEIROS nao first-class
- Sem time local de produto BR
- Data residency BR nao garantida
- Contract terms agressivos (no downgrade, 5-7% escalation, overages auto-billed)
- Setup steep learning curve
- Custos add-ons stack rapido (Copilot + WFM + QA + ADPP = +$160/agent/mo)

---

## TCO Side-by-Side - Cenarios BR

### Cenario A: E-commerce SMB BR (5 agents, ~1k conversas/mes, sem AI)

| Linha | Octadesk | Zendesk |
|---|---:|---:|
| Plataforma base | R$ 1.542/mo (Conversas tier publico) | R$ 1.795/mo (Suite Team R$359 x 5) |
| AI add-on | nao | nao |
| Sunshine extra | n/a | provavel zero (incluso) |
| **Total mensal** | **R$ 1.542** | **R$ 1.795** |
| **Total anual** | **R$ 18.504** | **R$ 21.540** |

**Diferenca:** Octadesk ~14% mais barato. Mas Octadesk Conversas pode estar sobredimensionado vs 5 agents (fonte sugere tier multi-canal generoso).

### Cenario B: Mid-market BR (50 agents, ~10k conversas/mes, AI moderado)

| Linha | Octadesk | Zendesk |
|---|---:|---:|
| Plataforma base | R$ 2.972/mo (Sea+AI 30 users, escalar Higher 50) | R$ 37.750/mo (Suite Pro R$755 x 50) |
| AI add-on | WOZ (gated, proj. R$5-10k/mo) | Copilot $50 x 50 = $2.500 = R$ 12.625/mo |
| AI per-res | n/a (incluso WOZ) | 5.000 res x $1,50 = $7.500 = R$ 37.875/mo |
| Sunshine | n/a | extra variavel ($495+ + per-MAU + per-notification) |
| **Total mensal min** | **R$ 7.972 - R$ 12.972** | **R$ 88.250+** |
| **Total anual** | **R$ 95.664 - R$ 155.664** | **R$ 1.059.000+** |

**Diferenca:** Octadesk **6,8x-11x mais barato** em mid-market BR com AI moderado.

### Cenario C: Enterprise BR multinacional regulada (100 agents, BAA, SSO, audit)

| Linha | Octadesk | Zendesk |
|---|---:|---:|
| Plataforma base | Octa Suite contato sales (gated) | R$ 110.500/mo (Suite Enterprise R$1.105 x 100) |
| AI add-on | WOZ gated | Copilot $50 x 100 = $5.000 = R$ 25.250/mo |
| Compliance/security | LGPD declarada apenas | ADPP $50 x 100 = $25.250/mo + Advanced Compliance |
| HIPAA / SSO / sandbox | NAO disponivel | incluso Enterprise + ADPP |
| WFM/QA | nao publico | $25 + $35 = $60 x 100 = R$ 30.300/mo (opcional) |
| Sunshine | n/a | extra $495+/mo + variavel |
| **Total mensal estimado** | **gated** | **R$ 161.000 - R$ 205.000** |

**Veredito:** Octadesk neste cenario provavelmente nao qualifica (nao oferece HIPAA/sandbox/SSO publicos). Zendesk vence por **disponibilidade**, nao por preco.

---

## Sources

- inventory-octadesk.json
- inventory-zendesk.json
- docs/research/2026-05-06-omnichannel-helpdesk-landscape/02-research-report.md
