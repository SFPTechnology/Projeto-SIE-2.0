# DP-01 — Evidência da Fonte de Topologia da Rede EDP V9

**PRD:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Data da verificação:** 2026-07-27  
**Autoridade desta avaliação:** Pax (@po)  
**Contribuição PO:** `APROVADA`  
**Estado global vigente de DP-01:** `APROVADO`  
**Implementação autorizada por este documento:** `NÃO`

## 1. Conclusão

A fonte de topologia definida para DP-01 é a **consulta do usuário à
concessionária EDP São Paulo para o ponto de conexão**.

A PT.DT.PDN.00068 V9 define os sistemas estrela 220/127 V e delta 240/120 V e
afirma que o atendimento depende do tipo de rede e do local da unidade
consumidora. Os exemplos normativos também partem do sistema disponível no
município/local, mas não fornecem uma matriz capaz de determinar a topologia
da ligação concreta.

Por isso, município ou endereço não determinam automaticamente estrela/delta.
O usuário deve solicitar a informação à EDP pelos canais oficiais de
atendimento ou durante o processo de ligação nova e registrar a resposta no
SIE.

A página oficial de ligação nova informa que a distribuidora avalia a rede
elétrica disponível no local da unidade consumidora:

`https://www.edp.com.br/ligacao-nova/`

## 2. Evidências examinadas

- PT.DT.PDN.00068 V9, §§5.3.1 e 5.3.3 e exemplos de cálculo;
- `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`;
- domínio, schemas e rotas atuais em
  `sistema-de-instala-es-el-tricas-sie-main/src/`;
- `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md`;
- documentos públicos da EDP localizados para tensões padronizadas e área de
  concessão;
- página oficial de ligação nova e canais de atendimento da EDP.

As fontes confirmam quais topologias e tensões existem, mas não qual delas está
disponível em cada ligação concreta sem consulta à concessionária.

## 3. Jornada aprovada de consulta

1. O usuário ou seu representante informa o endereço completo e os dados
   solicitados pela EDP.
2. O usuário solicita à EDP a informação do sistema/tensão disponível para o
   ponto de conexão, pelos canais oficiais ou no pedido de ligação nova.
3. Enquanto não houver resposta, o SIE mantém
   `PENDENTE_CONSULTA_CONCESSIONARIA`.
4. O usuário registra no SIE o protocolo e a manifestação recebida.
5. O responsável técnico confirma que topologia, tensão e projeto são
   compatíveis.
6. Somente então a topologia pode assumir estado confirmado e alimentar o
   avaliador EDP V9.

## 4. Evidência mínima da consulta

O registro deve conter:

- endereço ou identificador inequívoco da unidade;
- sistema informado: estrela 220/127 V ou delta 240/120 V;
- concessionária consultada;
- canal utilizado;
- referência a documento, resposta ou protocolo;
- data de emissão/consulta;
- usuário responsável pela captura;
- confirmação do responsável técnico;
- anexo ou referência verificável à manifestação recebida;
- estado de validade e regra de revalidação.

## 5. Estados do fluxo

| Condição | Estado |
|---|---|
| Consulta ainda não solicitada | `CONSULTA_CONCESSIONARIA_NAO_INICIADA` |
| Consulta solicitada sem resposta | `PENDENTE_CONSULTA_CONCESSIONARIA` |
| Resposta registrada sem confirmação técnica | `TOPOLOGIA_NAO_CONFIRMADA` |
| Resposta e confirmação técnica válidas | `TOPOLOGIA_CONFIRMADA` |
| Fontes divergentes | `DIVERGENCIA_TOPOLOGIA_REDE` |
| Documento/protocolo obsoleto | `TOPOLOGIA_OBSOLETA` |

Somente `TOPOLOGIA_CONFIRMADA` permite aplicar as regras dependentes de
DP-01. Os demais estados não podem:

- inferir estrela ou delta pelo município;
- assumir 220/127 V como padrão;
- aplicar fallback genérico;
- liberar pacote dependente de DP-01;
- alterar a tensão nominal das cargas.

## 6. Critérios de fechamento

- [x] Fonte aplicável ao ponto de conexão identificada: consulta à EDP.
- [x] Responsabilidade do usuário definida.
- [x] Jornada de captura e confirmação aprovada por @po.
- [x] Proveniência, protocolo e autoria definidos.
- [x] Tratamento de ausência, divergência e obsolescência definido.
- [x] Contribuição @po aprovada.
- [x] Coaprovação @architect.
- [x] Confirmação do responsável técnico definida como controle obrigatório e
      fail-closed por projeto.
- [ ] Fluxo implementado e testado em story autorizada.

## 7. Decisão PO anterior à coaprovação arquitetural

```yaml
DP-01:
  po_decision: APROVADO
  source: CONSULTA_USUARIO_A_EDP_POR_PONTO_DE_CONEXAO
  global_status: PENDENTE_DE_COAPROVACAO
  architect_coapproval: PENDING
  responsible_technician_confirmation: PENDING
  package_1_blocked: true
  story_creation_for_package_1_authorized: false
```

— Pax, equilibrando prioridades

O bloco acima preserva o snapshot da decisão PO. Seu estado global foi
substituído pelo adendo arquitetural a seguir.

## 8. Adendo arquitetural — coaprovação em 2026-07-27

**Autoridade:** Aria (@architect)  
**Decisão arquitetural:** `COAPROVADO`  
**SHA-256 da evidência PO avaliada:**  
`3A24CCD1B6F22F45DCC81F4F28F3F2DF7ADC7662C4F93B0F90C4D5A27F8922AC`

DP-01 está arquiteturalmente completo porque fonte, proveniência, autoria,
estados, próxima ação e comportamento para ausência, divergência e
obsolescência estão definidos sem inferência automática de topologia.

A confirmação do responsável técnico não é uma coaprovação documental
prévia a esta decisão. Ela é um controle obrigatório da jornada de cada
projeto: enquanto não houver manifestação verificável da EDP associada ao
ponto de conexão e confirmação técnica, a topologia permanece não confirmada
e todos os consumidores dependentes devem falhar de modo seguro.

A aprovação do gate não confirma estrela ou delta para qualquer unidade
concreta, não substitui a EDP ou o responsável técnico e não autoriza
implementação sem story e sem os demais gates aplicáveis.

```yaml
DP-01_architect_coapproval_2026_07_27:
  status_final: APROVADO
  po_contribution: APROVADA
  architect_coapproval: APROVADA
  source: CONSULTA_USUARIO_A_EDP_POR_PONTO_DE_CONEXAO
  municipality_or_address_inference_allowed: false
  responsible_technician_confirmation:
    scope: PER_PROJECT
    required_for: TOPOLOGIA_CONFIRMADA
    absence_behavior: FAIL_CLOSED
  package_1_blocked_by_DP_01: false
  story_creation_authorized_by_this_document: false
  implementation_authorized_by_this_document: false
```

— Aria, arquitetando o futuro
