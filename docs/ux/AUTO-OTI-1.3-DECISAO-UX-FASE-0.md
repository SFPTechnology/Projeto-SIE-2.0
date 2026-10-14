# AUTO-OTI-1.3 — Decisão UX da Fase 0

**Data:** 2026-08-02  
**Responsável:** Uma (`@ux-design-expert`)  
**Story:** `docs/stories/story-AUTO-OTI-1.3-aplicar-secao-auto-otimizada-no-mod-qt.md`  
**Estado da decisão:** `APROVADA POR UX`; a aprovação conjunta de `@po` continua obrigatória para concluir o gate da Fase 0  
**Escopo:** semântica de confirmação individual/lote, estados, contagens e acessibilidade; sem implementação de UI

## 1. Decisão

Fica escolhida a segunda opção permitida pelo plano:

1. **Otimizar todos** calcula os circuitos e apresenta os resultados, sem aplicar nem persistir seções.
2. Depois do cálculo, a ação explícita **Aplicar {n} seções aprovadas** confirma o lote consolidado, em que `{n}` é a quantidade de resultados aprovados que será enviada ao caso de uso comum.

O lote não é aplicado automaticamente ao término de **Otimizar todos**. A segunda ação é o consentimento inequívoco para persistência. Somente resultados **Aprovados** integram o envio, e a aplicação usa uma única operação atômica.

A aplicação individual mantém a semântica existente **Confirmar seção {n} mm²**. Essa ação confirma apenas o circuito aberto e usa o mesmo caso de uso headless utilizado pelo lote.

## 2. Evidência brownfield

A interface atual sustenta a escolha em duas etapas:

- `DimensionamentoCondutoresResumo.tsx` já apresenta **Otimizar todos ({total})**, calcula o lote e deixa os resultados disponíveis para consulta, sem confirmação durável.
- `OtimizarCondutorModal.tsx` já separa o cálculo individual da ação **Confirmar seção {n} mm²**.
- O estado atual `secoesConfirmadas` é retido em React/`localStorage`; conforme plano e story, essa retenção não é fonte durável e não pode continuar sendo apresentada como aplicação persistida.

Portanto, a decisão preserva o modelo mental atual — primeiro calcular, depois confirmar — e torna explícito o novo efeito persistente.

## 3. Semântica de estado

| Situação | Representação textual obrigatória | Regra de aplicação |
|---|---|---|
| Motor produziu resultado | **Calculado** | Não é aplicado, persistido nem vigente. |
| Resultado com `status === "APROVADO"` e seção finita e positiva | **Aprovado** | Habilita a confirmação individual e compõe `{n}` no lote. |
| Confirmação enviada e operação ainda sem resultado durável | Operação em andamento, sem rótulo **Aplicado** | Não antecipar sucesso. |
| Resposta `DURAVEL` | **Aplicado**, **Persistido** e, quando compatível, **Vigente** | Só aqui a UI pode apresentar o item como aplicado. |
| Resposta `VOLATIL` | **VOLATIL** e não persistido | Não apresentar como aplicado, persistido ou vigente. |
| Resposta `FALHOU` | **FALHOU** | Nenhum item do lote pode aparecer como aplicado. |
| Registro incompatível com a assinatura ou ciclo de vida | **Obsoleto** | Não é fonte vigente do MOD-QT. |
| Override auditado no MOD-QT | **Manual MOD-QT** | Permanece distinguível e prevalece sobre a seção automática vigente. |

Uma falha transitória com a mesma assinatura não altera visualmente a seção vigente anterior para obsoleta; a tentativa falha deve ser comunicada separadamente. Uma nova entrada aplicada com assinatura diferente segue as regras normativas de invalidação.

## 4. Contagens do lote

A apresentação consolidada deve manter as contagens separadas, sem converter sucesso parcial de cálculo em sucesso parcial de aplicação:

- **Calculados**: resultados produzidos pelo motor.
- **Aprovados**: calculados válidos e elegíveis para aplicação; este valor alimenta `{n}` em **Aplicar {n} seções aprovadas**.
- **Aplicados**: itens confirmados como aplicados somente após `DURAVEL`.
- **Persistidos**: itens cuja gravação durável foi confirmada.
- **Ignorados**: itens não enviados ou não aplicados, com motivo retornado.
- **Conflitos**: itens reportados em conflito.
- **Falhas**: itens/operação reportados como falha.
- **Persistência**: classificação textual `DURAVEL`, `VOLATIL` ou `FALHOU` para a operação.

Quando não houver resultado aprovado, `{n} = 0` e não existe lote elegível para aplicação. Em falha da transação durável, nenhum item recebe estado aplicado.

## 5. Acessibilidade

A implementação desta decisão deve atender ao mínimo WCAG AA definido para a UI do projeto:

- ações são controles semânticos operáveis por teclado, com foco visível e nome acessível que explicita o efeito e a quantidade;
- progresso impede reenvio concorrente e é comunicado por texto; o usuário não depende apenas de botão desabilitado ou alteração visual;
- resultado e contagens são apresentados em texto e anunciados pela região de feedback/notificação existente, sem depender apenas de cor, badge ou ícone;
- `DURAVEL`, `VOLATIL`, `FALHOU`, **Aplicado** e **Obsoleto** permanecem legíveis como texto; cores são apenas reforço;
- ícones permanecem complementares e não substituem rótulos; tabelas preservam cabeçalhos semânticos;
- a ação **Aplicar {n} seções aprovadas** não usa uma quantidade genérica: o nome acessível contém o mesmo `{n}` visível.

## 6. Limites preservados

- A decisão não autoriza aplicação automática após o cálculo.
- `localStorage` não é fonte compartilhada ou durável.
- A UI não calcula a assinatura nem fornece seção autoritativa; usa o caso de uso headless comum.
- O estado aplicado não existe antes de `DURAVEL`.
- A edição manual, a justificativa e a auditoria do MOD-QT permanecem preservadas.
- Nenhuma fórmula, contrato protegido ou regra de precedência é alterada por esta decisão.

## 7. Parecer UX para o gate

**Parecer:** `GO UX` para a semântica **Otimizar todos → Aplicar {n} seções aprovadas**, condicionada à coaprovação de `@po` e aos demais gates da Fase 0. Este parecer não altera o status `Draft` da story e não autoriza início de implementação isoladamente.

---

— Uma, desenhando com empatia 💝
