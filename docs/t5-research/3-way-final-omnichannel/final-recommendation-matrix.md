# Final Recommendation Matrix — 3-Way Final Omnichannel

**Bench:** 3-way-final-omnichannel
**Fase:** A (artefato 6 de 10)
**Data:** 2026-05-06
**Insumo:** `consolidated-scorecard.md` (matriz 4×9 + 4 personas recalibradas)
**Players cobertos:** Chatwoot, Zendesk, Intercom, Octadesk
**Audiencia:** decisores tecnicos (CTO/Head of CX/Tech Ops) — slide-ready

> **Disclaimer constitucional:** este artefato e RESEARCH agregado, nao recomendacao vinculante para nenhum negocio especifico do Sinkra Hub. Cenarios "estilo Hub" sao perfis genericos, nao mapping 1:1 a AllFluence/AIOX/Academia Lendaria/Bilhon. Decisao final exige due diligence comercial + POC + validacao com BSP local.

---

## 1. Tabela sintese — slide-ready

| Persona | Recomendacao primaria | Alternativa | Nao recomendado | Criterio decisor |
|---|---|---|---|---|
| **SMB BR e-commerce** (5-10 agents, <=1k conv/mes) | **Chatwoot self-host** | Octadesk (zero-DevOps) | Zendesk (TCO inviavel), Intercom (D8 fraco) | TCO + DevOps capacity |
| **Mid-market BR** (50-100 agents, compliance baixo) | **Chatwoot self-host** | Octadesk | Zendesk (over-spec), Intercom | DevOps + WhatsApp volume |
| **Mid-market BR** (50-100 agents, compliance alto / SSO mandatory) | **Zendesk Suite Pro** | Chatwoot Cloud Business | Octadesk (gap enterprise), Intercom | SSO/SAML + audit posture |
| **Enterprise BR multinacional** (100+ agents, regulado, multi-region) | **Zendesk Enterprise** | Chatwoot self-host EU + paid support | Octadesk (out-of-segment), Intercom (D7=0) | HIPAA/FedRAMP/BCR + multi-region |
| **Global SaaS B2B** (in-app heavy, EN-first) | **Intercom** (apesar do score 3o) | Zendesk Suite + in-app addon | Octadesk (BR-only), Chatwoot (in-app modesto) | In-app polish e decisor |
| **Global SaaS B2B GDPR strict** (EU-residency mandatory) | **Chatwoot self-host EU** | Zendesk (Dublin BCR) | Intercom (data sovereignty fraco), Octadesk | Data sovereignty |

---

## 2. Decision tree completo

```
PERGUNTA-RAIZ: Qual o footprint geografico e o perfil regulatorio?

1. Operacao e exclusivamente Brasil?
   ├── SIM (BR-only):
   │   │
   │   ├── 1.1 ≤10 agents + e-commerce / DTC / PME?
   │   │   ├── Tem DevOps interno (1+ pessoa familiarizada com Docker/K8s)?
   │   │   │   ├── SIM → CHATWOOT self-host community ($0 license + ~R$300-800/mes infra)
   │   │   │   └── NAO → OCTADESK (zero-DevOps + bundle Bling/Tray/Vindi via LWSA)
   │   │   └── Volume WhatsApp >5k conv/mes?
   │   │       ├── SIM → privilegiar BSP-direct (Chatwoot via Twilio/Gupshup ou Octadesk Smarters)
   │   │       └── NAO → ambos servem; decidir por DevOps capacity
   │   │
   │   ├── 1.2 50-100 agents (mid-market BR)?
   │   │   ├── SSO/SAML mandatory por compliance interna ou auditoria?
   │   │   │   ├── SIM → ZENDESK Suite Professional/Enterprise (SSO nativo + audit logs)
   │   │   │   └── NAO ↓
   │   │   ├── BR-only + bundle Bling/Tray/Vindi/integracoes LWSA dominam stack?
   │   │   │   ├── SIM → OCTADESK (BR-fit categorical + ecossistema LWSA)
   │   │   │   └── NAO ↓
   │   │   └── DevOps maduro + cost-conscious + customizacao alta?
   │   │       ├── SIM → CHATWOOT self-host Enterprise (TCO ~3-5x menor que Zendesk)
   │   │       └── NAO → ZENDESK Suite Team/Pro (default seguro)
   │   │
   │   └── 1.3 100+ agents enterprise BR regulado (healthcare/fintech/governo)?
   │       ├── HIPAA / FedRAMP / SOC2 Type II mandatory?
   │       │   ├── SIM → ZENDESK Enterprise (categorical em D4=95)
   │       │   └── NAO ↓
   │       └── Buyer aceita customer-controlled compliance (self-host EU)?
   │           ├── SIM → CHATWOOT self-host EU + paid support partner
   │           └── NAO → ZENDESK Enterprise
   │
   └── NAO (global / multi-region / EN-first):
       │
       ├── 2.1 In-app messaging (web SDK + mobile SDK + product tours) e DECISIVO?
       │   ├── SIM + budget enterprise → INTERCOM (D9=95 categorical)
       │   └── NAO ↓
       │
       ├── 2.2 GDPR strict + EU data residency mandatory?
       │   ├── SIM + tem DevOps EU → CHATWOOT self-host (data sovereignty 100%)
       │   ├── SIM + sem DevOps EU → ZENDESK (Dublin region + BCR)
       │   └── NAO ↓
       │
       ├── 2.3 Compliance enterprise (SOC2 + ISO 27001 + HIPAA) + multi-region?
       │   └── SIM → ZENDESK Enterprise (default global)
       │
       └── 2.4 Cost-conscious + flexibilidade alta + DevOps maduro?
           └── SIM → CHATWOOT self-host (categorical em D7=100)
```

**Atalho mental (3 perguntas):**

1. BR-only? Sim → Chatwoot/Octadesk/Zendesk (descartar Intercom).
2. Tem DevOps maduro? Sim → Chatwoot competitivo. Nao → SaaS (Zendesk/Octadesk/Intercom).
3. Compliance enterprise mandatory? Sim → Zendesk default. Nao → abrir leque.

---

## 3. Casos especiais — cenarios estilo Sinkra Hub (perfis genericos)

> Perfis ilustrativos, NAO recomendacao vinculante para qualquer negocio especifico do Hub. Apenas mostra como o decision tree se aplica em arquetipos comuns no portfolio.

### Perfil A — E-commerce DTC BR (mass-market, BR-only)

| Item | Valor |
|---|---|
| Volume tipico | 30-80 agents, 5-20k conv/mes, WhatsApp >70% do mix |
| Player primario | **Chatwoot self-host** (caso tenha DevOps) ou **Octadesk** (caso nao tenha) |
| Alternativa | Zendesk Suite Team apenas se compliance/SSO entrar como hard requirement |
| Razao (2-3 linhas) | BR-fit + WhatsApp depth + TCO BRL dominam. Compliance enterprise e secundario. Octadesk vence quando o time nao quer operar infra; Chatwoot vence quando a equipe valoriza customizacao + zero per-seat e ja roda Docker. |

### Perfil B — SaaS B2B global (EN-first, EU+US)

| Item | Valor |
|---|---|
| Volume tipico | 20-40 agents, 3-10k conv/mes, in-app + email dominantes |
| Player primario | **Intercom** se in-app + AI premium sao parte do produto; senao **Zendesk** |
| Alternativa | Chatwoot self-host EU para GDPR strict + cost-conscious |
| Razao (2-3 linhas) | In-app messenger + product tours + AI sao decisivos para SaaS B2B mid-market global. BR-fit irrelevante. Custo per-resolution Intercom explode em volume — fazer modelagem antes. |

### Perfil C — Educacao BR mass-market (high-volume, BR-only)

| Item | Valor |
|---|---|
| Volume tipico | 15-50 agents, 10-50k conv/mes (alto volume sazonal), WhatsApp dominante |
| Player primario | **Chatwoot self-host** (TCO previsivel em alto volume) |
| Alternativa | Octadesk se time prefere SaaS BR + bundle integracoes (gateways, CRMs BR) |
| Razao (2-3 linhas) | Volume alto WhatsApp inviabiliza per-seat USD (Zendesk/Intercom). Chatwoot self-host elimina custo per-conv ao escalar; Octadesk e SaaS BR pragmatico. Intercom descartado por D8 baixo + per-resolution. |

### Perfil D — Healthcare/fintech BR regulado (compliance high)

| Item | Valor |
|---|---|
| Volume tipico | 80-200 agents, 5-15k conv/mes, multicanal regulado, audit trail mandatory |
| Player primario | **Zendesk Suite Enterprise** (compliance categorical) |
| Alternativa | Chatwoot self-host on-prem BR caso buyer aceite customer-controlled compliance posture |
| Razao (2-3 linhas) | SOC2 Type II + ISO 27001 + audit logs nativos + SSO/SAML + RBAC granular sao hard requirements. Octadesk fora do segmento. Intercom D7=0 inviabiliza data sovereignty exigida em fintech regulada. |

---

## 4. Quando NAO escolher cada player

### Nao escolher CHATWOOT quando

- Time NAO tem DevOps interno e nao quer pagar partner para gerenciar infra (TCO oculto vira o de SaaS).
- Compliance HIPAA / FedRAMP / SOC2 Type II e mandatory e o buyer nao aceita customer-controlled posture (D4=55).
- Captain AI ainda imaturo e o caso de uso depende criticamente de AI deflection com benchmark publicado (D2=65 + Captain confidence M).
- Necessidade de marketplace amplo de plugins enterprise (Salesforce, NetSuite, Workday) — D5=65 vs Zendesk D5=95.
- Decisor exige SLA contratual de uptime + suporte vendor 24/7 incluido sem custo separado.

### Nao escolher ZENDESK quando

- Operacao SMB BR com TCO BRL como restricao dura: R$359/agent/mes Suite Team x 10 agents = R$3.6k/mes vs Octadesk ~R$700/mes (delta 5x).
- Setup cost + custom dev + AI add-ons explodem o budget (Zendesk AI agents tipicamente add-on separado).
- Buyer quer self-host real / data sovereignty 100% — Zendesk SaaS-only (D7=35 com BYOK parcial).
- Caso de uso e in-app messenger + product tours + AI proativa como produto central — Intercom polish > Zendesk addon.
- Customizacao de fluxos exige source code access ou modificacao deep — Zendesk e closed-source.

### Nao escolher INTERCOM quando

- Operacao majoritariamente Brasil — D8=35 (sem BSP-direct local, BRL ausente, suporte PT-BR limitado).
- Volume alto de conversas (>10k/mes) com pricing per-resolution — TCO explode previsivelmente.
- Data sovereignty / on-prem / self-host sao hard requirements — D7=0 categorical loser.
- WhatsApp e canal dominante (>50% do mix) — D1=60 e o pior do quarteto, BSP fica via Twilio addon.
- Compliance regulado BR (LGPD strict + DPO local + auditoria CVM/BACEN) — posture inferida M, sem certificacoes BR-friendly.

### Nao escolher OCTADESK quando

- Operacao multinacional / multi-region — gap enterprise + ausencia de regions EU/US (D4=45).
- Compliance HIPAA / FedRAMP / SOC2 Type II mandatory — categorical out (D4=45).
- Caso de uso enterprise com 100+ agents + integracoes globais (Salesforce, Workday, etc.) — D5=60.
- AI sofisticada com benchmark publicado e parte do RFP — D2=70 atras de Zendesk e Intercom.
- Time precisa de comunidade global ativa + extenso material em ingles — D6=55 (mercado BR-only).

---

## 5. Tiebreakers operacionais — checklist

Quando dois players empatam tecnicamente (delta <2 pts no scorecard de persona), use esta checklist objetiva. Cada criterio e binario / quantificavel.

| # | Pergunta | Resposta SIM | Resposta NAO |
|---|---|---|---|
| T1 | Tem DevOps interno (1+ pessoa familiarizada Docker/K8s, 10+ horas/mes disponiveis)? | Chatwoot fica viavel | Descartar Chatwoot self-host; ir para SaaS |
| T2 | Volume WhatsApp esperado >5k conv/mes nos proximos 12 meses? | BSP-direct preferido (Chatwoot via BSP, Octadesk Smarters); evitar Twilio addon caro | Qualquer player serve em D1 |
| T3 | SSO/SAML/SCIM mandatory por compliance interna? | Zendesk (nativo todos os tiers Pro+); Chatwoot Enterprise (Cloud) | Qualquer player |
| T4 | Audit logs imutaveis + retention >1 ano + RBAC granular sao requisitos auditados? | Zendesk default; Chatwoot self-host com customizacao | Octadesk/Intercom/Chatwoot Cloud |
| T5 | Data residency: EU mandatory ou BR mandatory? | EU → Chatwoot self-host EU ou Zendesk Dublin; BR → Octadesk ou Chatwoot self-host BR | Qualquer SaaS region disponivel |
| T6 | TCO BRL: budget <R$1k/agent/mes ou >R$1k/agent/mes? | <R$1k → Chatwoot/Octadesk; >R$1k → leque aberto | — |
| T7 | In-app messenger (web SDK + mobile SDK) e parte CORE do produto/UX? | Intercom (D9=95 categorical) | Qualquer player; in-app modesto suficiente |
| T8 | AI deflection benchmark publicado e RFP requirement? | Zendesk (Resolution Bot publicado) ou Intercom (Fin published) | Qualquer player serve |
| T9 | Ecossistema Bling/Tray/Vindi/iFood/correios sao dependencias hard? | Octadesk (bundle nativo via LWSA) | Qualquer player; integracoes via API/Zapier |
| T10 | Marketplace plugins enterprise (Salesforce/NetSuite/Workday) e requisito? | Zendesk (D5=95); Intercom moderado (D5=85) | Qualquer player |
| T11 | Equipe tem skills internas para customizar UI/fluxos via codigo? | Chatwoot OSS viabiliza fork/custom dev | SaaS configuravel suficiente |
| T12 | Operacao 24/7 com SLA contratual + suporte vendor incluso e mandatory? | Zendesk (Premier Support) ou Octadesk Premium | Self-host exige partner pago separado |
| T13 | Buyer e cost-conscious extremo (CFO-driven)? Per-seat USD inviavel? | Chatwoot ($0 license) ou Octadesk (BRL flat) | Zendesk/Intercom OK |
| T14 | Risco de vendor lock-in e KPI explicito no comite tech? | Chatwoot (OSS, dados em DB proprio) reduz lock-in | Qualquer SaaS expoe lock-in moderado |
| T15 | Multilingual mandatory (PT-BR + EN + ES + DE + FR)? | Zendesk (i18n maduro + ecosystem) ou Intercom | Octadesk PT-BR-first; Chatwoot OK mas custom strings |

**Como usar:** marque SIM/NAO em cada linha → contar quantas linhas favorecem cada player → desempate vai para quem teve mais matches relevantes ao caso especifico. Em caso de empate, voltar ao decision tree (secao 2) e usar perfil de persona como tiebreaker macro.

---

## 6. Resumo executivo (1 paragrafo)

**Nao existe vencedor universal neste mercado.** O scorecard neutro aponta empate tecnico entre Zendesk (74.95) e Chatwoot (74.40), mas a decisao real e persona-driven: **Chatwoot** vence SMB BR e e unico top-2 em todas as personas (flexibilidade + TCO sao categorical); **Zendesk** vence mid-market+/enterprise/global pelo combo compliance + ecosystem + maturidade; **Octadesk** e especialista BR PME com BR-fit categorical (D8=95) mas gap enterprise; **Intercom** e categorical em in-app (D9=95) mas paga D7=0 + D8=35 caro fora de SaaS B2B in-app heavy. Decisores devem (a) classificar a operacao em uma das 4 personas, (b) aplicar o decision tree (secao 2), (c) cruzar com tiebreakers (secao 5) — nessa ordem.

---

## Cross-refs

- Matriz consolidada → `consolidated-scorecard.md`
- Reconciliacoes paired benches → `triangulation-analysis.md`
- Scores por dimensao com citacoes → `cross-bench-matrix.md`
- Dados estruturais → `consolidated-scorecard.json`
- Metadados do bench → `metadata.json`
