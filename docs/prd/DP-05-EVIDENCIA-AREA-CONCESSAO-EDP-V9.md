# DP-05 — Evidência da Área de Concessão EDP São Paulo

**PRD:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Data da verificação:** 2026-07-27  
**Autoridade desta decisão:** Pax (@po)  
**Contribuição PO:** `APROVADA`  
**Estado global vigente de DP-05:** `APROVADO`  
**Implementação autorizada por este documento:** `NÃO`

## 1. Decisão de produto

A área de concessão da EDP São Paulo deve ser comprovada por catálogo
versionado de municípios derivado de fonte oficial. Declaração livre de
distribuidora, texto digitado pelo usuário ou inferência por proximidade não
constituem comprovação.

O catálogo deve registrar:

- identificador e versão da fonte;
- data de obtenção e verificação;
- UF e nome canônico do município;
- hash do conteúdo publicado para uso pelo SIE;
- estado de validade do catálogo.

## 2. Fontes oficiais verificadas

1. EDP — Área de concessão SP:  
   `https://www.edp.com.br/area-de-concessao-sp/`
2. ANEEL — Sexto Termo Aditivo, Anexo I — Área de Concessão:  
   `https://www2.aneel.gov.br/cedoc/adsp20251584_2.pdf`

As duas fontes listam os mesmos 28 municípios. O termo aditivo da ANEEL é a
fonte regulatória primária; a página da EDP é a fonte operacional de
conferência.

## 3. Catálogo de referência

| # | Município | UF |
|---:|---|---|
| 1 | Aparecida | SP |
| 2 | Biritiba Mirim | SP |
| 3 | Caçapava | SP |
| 4 | Cachoeira Paulista | SP |
| 5 | Canas | SP |
| 6 | Caraguatatuba | SP |
| 7 | Cruzeiro | SP |
| 8 | Ferraz de Vasconcelos | SP |
| 9 | Guararema | SP |
| 10 | Guaratinguetá | SP |
| 11 | Guarulhos | SP |
| 12 | Itaquaquecetuba | SP |
| 13 | Jacareí | SP |
| 14 | Jambeiro | SP |
| 15 | Lorena | SP |
| 16 | Mogi das Cruzes | SP |
| 17 | Monteiro Lobato | SP |
| 18 | Pindamonhangaba | SP |
| 19 | Poá | SP |
| 20 | Potim | SP |
| 21 | Roseira | SP |
| 22 | Salesópolis | SP |
| 23 | Santa Branca | SP |
| 24 | São José dos Campos | SP |
| 25 | São Sebastião | SP |
| 26 | Suzano | SP |
| 27 | Taubaté | SP |
| 28 | Tremembé | SP |

## 4. Regra de comprovação

| Entrada | Resultado | Efeito |
|---|---|---|
| UF `SP` e município canônico presente no catálogo oficial válido | `AREA_CONCESSAO_COMPROVADA` | Permite continuar para os demais gates |
| UF diferente de `SP` ou município ausente do catálogo | `FORA_AREA_CONCESSAO_EDP_SP` | Impede aplicar a avaliação EDP V9 |
| UF/município ausente, ambíguo ou sem normalização inequívoca | `PENDENTE_COMPROVACAO_AREA` | Bloqueia avaliação automática |
| Catálogo sem fonte, versão, data ou hash | `FONTE_AREA_CONCESSAO_INVALIDA` | Bloqueia publicação/uso do catálogo |

Regras adicionais:

1. Normalização pode tratar caixa, espaços e acentuação apenas quando o
   resultado for inequívoco.
2. Correspondência aproximada não pode incluir automaticamente um município.
3. A comprovação da área não determina a topologia da rede; `DP-01` permanece
   independente.
4. Uma atualização da concessão exige nova versão do catálogo e revalidação de
   DP-05.
5. Decisões históricas preservam a versão do catálogo usada na avaliação.

## 5. Critérios de fechamento

- [x] Fonte oficial regulatória identificada.
- [x] Fonte operacional da concessionária identificada.
- [x] Municípios reconciliados entre as fontes.
- [x] Regra fail-closed definida.
- [x] Proveniência e versionamento exigidos.
- [x] Contribuição @po aprovada.
- [x] Coaprovação @architect.
- [ ] Catálogo físico implementado e testado em story autorizada.

## 6. Decisão PO anterior à coaprovação arquitetural

```yaml
DP-05:
  po_decision: APROVADO
  global_status: PENDENTE_DE_COAPROVACAO_ARCHITECT
  source_of_truth: ANEEL_SIXTH_ADDITIVE_ANNEX_I
  operational_cross_check: EDP_AREA_DE_CONCESSAO_SP
  municipality_count: 28
  fail_closed: true
  story_creation_authorized: false
```

— Pax, equilibrando prioridades

O bloco acima preserva o snapshot da decisão PO. Seu estado global foi
substituído pelo adendo arquitetural a seguir.

## 7. Adendo arquitetural — coaprovação em 2026-07-27

**Autoridade:** Aria (@architect)  
**Decisão arquitetural:** `COAPROVADO`  
**SHA-256 da evidência PO avaliada:**  
`2032989615F945B6BFCBAFB6645ACEDECDBB569616239F9D259B0AF3E2A4DACD`

DP-05 está arquiteturalmente completo com base nas fontes já registradas: o
Anexo I do Sexto Termo Aditivo da ANEEL como fonte regulatória primária e a
página da EDP como conferência operacional. O catálogo reconciliado contém 28
municípios distintos.

O desenho exige fonte, versão, data e hash; preserva a versão usada em decisões
históricas; rejeita correspondência aproximada; e bloqueia o uso quando os
dados de localização forem ausentes, ambíguos ou quando a fonte for inválida.
A área comprovada apenas habilita a continuação dos demais gates e não
determina a topologia de DP-01.

A criação do catálogo físico e seus testes pertencem à execução de story
futura. Sua ausência atual não invalida a decisão de arquitetura e tampouco
autoriza implementação sem os demais gates.

```yaml
DP-05_architect_coapproval_2026_07_27:
  status_final: APROVADO
  po_contribution: APROVADA
  architect_coapproval: APROVADA
  source_of_truth: ANEEL_SIXTH_ADDITIVE_ANNEX_I
  operational_cross_check: EDP_AREA_DE_CONCESSAO_SP
  municipality_count: 28
  municipality_count_unique: 28
  versioned_and_auditable: true
  fail_closed: true
  package_2_blocked_by_DP_05: false
  story_creation_authorized_by_this_document: false
  implementation_authorized_by_this_document: false
```

— Aria, arquitetando o futuro
