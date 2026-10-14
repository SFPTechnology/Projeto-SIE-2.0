# Create Thank You Page Task

## Purpose

Criar páginas de obrigado estratégicas que confirmam a ação, eliminam buyer's remorse, maximizam revenue com OTOs, ativam referrals, e iniciam o relacionamento de forma positiva usando psicologia pós-compra avançada.

## When to Use

- Após finalização de compra (qualquer ticket)
- Após captura de lead (lead magnet, quiz, assessment)
- Após inscrição em webinar/evento
- Após registro em trial/freemium
- Qualquer conversão que merece confirmação e próximos passos

## Theoretical Foundation

### The Critical Moment Theory

Thank you pages representam um dos momentos mais subutilizados do marketing digital. Neste momento, o cliente está:

1. **Fully Committed** - Já tomou a ação (pagamento, cadastro)
2. **Highest Attention** - Ativamente esperando confirmação
3. **Lowest Resistance** - Defesas cognitivas reduzidas pós-decisão
4. **Peak Engagement** - Emocionalmente investido no resultado
5. **Action-Primed** - Momentum da ação anterior carrega adiante

### Buyer's Remorse Psychology

**Teoria da Dissonância Cognitiva:**
Após uma compra, clientes frequentemente experimentam desconforto psicológico:

- O dinheiro foi embora (loss aversion ativado)
- O produto ainda não entregou (incerteza)
- Opções alternativas não foram escolhidas (custo de oportunidade)
- Medos de julgamento social (o que outros vão pensar?)

**Timeline do Arrependimento:**
```
Compra → 0-5 min: Excitação/alívio
       → 5-60 min: Dúvida começa
       → 1-24 horas: Pico de arrependimento
       → 24-72 horas: Resolução (positiva ou negativa)
```

### The Commitment-Consistency Principle (Cialdini)

Uma vez que alguém se compromete com uma ação, são psicologicamente direcionados a permanecer consistentes. Thank you pages alavancam isso através de:

- **Foot-in-the-Door** - Pequeno compromisso leva a maiores
- **Identity Reinforcement** - "Como cliente de [produto], você é o tipo de pessoa que..."
- **Behavioral Momentum** - Mantê-los tomando ações
- **Self-Perception Theory** - Ações moldam auto-imagem

---

## Inputs

```yaml
required:
  conversion_type: "O tipo de conversão (purchase, lead, registration, trial)"
  product_name: "Nome do produto/oferta principal"
  price_paid: "Valor pago (se compra) ou 'free' se lead"
  next_steps: "O que acontece agora após a conversão"
  access_info: "Como/quando terá acesso ao prometido"

optional:
  oto_offer: "Oferta de upsell (One-Time Offer) - produto, preço, benefícios"
  upsell_stack: "Múltiplos upsells em sequência"
  community_link: "Link para comunidade/grupo exclusivo"
  referral_program: "Estrutura do programa de indicação (recompensas)"
  social_sharing: "Se quer incentivar compartilhamento social"
  onboarding_video: "URL do vídeo de boas-vindas"
  quick_win: "Ação rápida para resultado imediato"
  support_channels: "Canais de suporte disponíveis"
  guarantee_details: "Detalhes da garantia para reforçar"
  copywriter_preference: "Copywriter específico desejado"
```

---

## Workflow

### Step 1: Thank You Page Type Selection

```yaml
page_types:

  type_1_simple_confirmation:
    name: "Confirmação Simples"
    description: "Apenas confirma a ação com próximos passos claros"
    use_when:
      - Leads simples (newsletter, download básico)
      - Inscrições de baixo compromisso
      - Quando não há oferta adicional estratégica
    elements:
      - Confirmação de sucesso
      - Próximos passos claros (1-3)
      - Expectativa de entrega
      - Soft CTA (conteúdo gratuito)
    avoid: Upsells agressivos neste contexto

  type_2_confirmation_plus_oto:
    name: "Confirmação + OTO (One-Time Offer)"
    description: "Confirma e apresenta upsell exclusivo"
    use_when:
      - Após qualquer compra
      - Após leads qualificados
      - Quando há produto complementar
    elements:
      - Confirmação clara
      - Validação da decisão
      - OTO com urgência real
      - Fácil de recusar
    conversion_benchmark: "10-25% OTO conversion"

  type_3_onboarding_focused:
    name: "Confirmação + Onboarding"
    description: "Confirma com foco em começar a usar"
    use_when:
      - Produtos complexos (cursos, software)
      - Memberships com múltiplos recursos
      - Quando consumo rápido é crítico para retenção
    elements:
      - Confirmação celebratória
      - Vídeo de boas-vindas
      - Checklist de início
      - Quick win imediato
      - Acesso à comunidade
    goal: "First value in first 24 hours"

  type_4_community_centric:
    name: "Confirmação + Comunidade"
    description: "Confirma com foco em integração ao grupo"
    use_when:
      - Programas com comunidade ativa
      - Memberships baseados em networking
      - Quando peer support é diferencial
    elements:
      - Confirmação acolhedora
      - Convite para comunidade
      - Como se apresentar
      - Expectativas do grupo
      - Primeiras conexões

  type_5_referral_focused:
    name: "Confirmação + Programa de Indicação"
    description: "Confirma e ativa word-of-mouth imediatamente"
    use_when:
      - Produtos com alto NPS
      - Quando viralidade é estratégica
      - Clientes em momento de pico entusiasmo
    elements:
      - Confirmação com celebração
      - Link de referência único
      - Recompensas claras (two-sided)
      - Múltiplos canais de compartilhamento
      - Tracking visível

  type_6_high_ticket_premium:
    name: "Confirmação Premium (High-Ticket)"
    description: "Experiência de confirmação white-glove"
    use_when:
      - Compras de alto valor ($1000+)
      - Quando relacionamento é fundamental
      - Produtos com entrega personalizada
    elements:
      - Mensagem pessoal (vídeo do founder)
      - Validação extensiva da decisão
      - Onboarding concierge
      - Linha direta de suporte
      - Garantia em destaque
```

**Decision Tree:**
```
É uma compra ou lead?
├── COMPRA
│   ├── Alto ticket ($500+)?
│   │   └── YES → Type 6: Premium
│   │   └── NO → Tem OTO disponível?
│   │       └── YES → Type 2: Confirmation + OTO
│   │       └── NO → Produto complexo?
│   │           └── YES → Type 3: Onboarding
│   │           └── NO → Tem comunidade?
│   │               └── YES → Type 4: Community
│   │               └── NO → Type 1: Simple
├── LEAD
│   ├── Lead qualificado (quiz, assessment)?
│   │   └── YES → Type 2: Com tripwire OTO
│   │   └── NO → Type 1: Simple + soft CTA
├── REGISTRATION
│   └── Evento/Webinar → Custom event template
```

---

### Step 2: Confirmation Block Development

```yaml
confirmation_elements:

  success_headline:
    purpose: "Comunicar claramente que a ação foi bem-sucedida"
    formulas:
      celebratory: "🎉 Parabéns! [Ação] confirmada!"
      welcoming: "Bem-vindo(a) à [comunidade/produto]!"
      direct: "✅ Pronto! Sua [ação] está completa."
      personal: "[Nome], você está dentro!"

    examples:
      purchase: "🎉 Compra Confirmada! Você agora tem acesso ao [Produto]."
      lead: "✅ Você está dentro! Seu [Lead Magnet] está a caminho."
      registration: "🗓️ Inscrição Confirmada! Nos vemos em [data]."
      trial: "🚀 Trial Ativado! Sua jornada com [Produto] começa agora."

  order_summary:
    purpose: "Dar clareza sobre o que foi adquirido/feito"
    include:
      - Nome do produto/oferta
      - Preço pago (se aplicável)
      - Número do pedido/confirmação
      - Data da transação
      - Método de pagamento (parcial, por segurança)

    format: |
      **Resumo do Pedido:**
      - Produto: [Nome]
      - Investimento: R$[valor]
      - Pedido #: [número]
      - Data: [data]

  delivery_expectations:
    purpose: "Eliminar ansiedade sobre próximos passos"
    elements:
      - O que receberão
      - Quando receberão
      - Como receberão (email, plataforma, etc)
      - O que fazer se não receber

    timeline_templates:
      instant: "Acesso imediato - confira seu email agora mesmo"
      minutes: "Em até [X] minutos você receberá..."
      hours: "Nas próximas [X] horas, espere..."
      physical: "Seu pedido será enviado em [X] dias úteis"
```

---

### Step 3: Buyer's Remorse Prevention Block

```yaml
remorse_prevention:

  decision_validation:
    purpose: "Reforçar que a decisão foi correta"
    psychological_basis: "Cognitive dissonance reduction"

    templates:
      social_proof_validation: |
        "Você se juntou a [X.XXX]+ pessoas que já [alcançaram resultado]
        com [produto]. Você está em excelente companhia."

      authority_validation: |
        "Esta é a mesma [metodologia/ferramenta] usada por [autoridade/empresa]
        para [resultado impressionante]."

      rational_validation: |
        "Você tomou uma decisão inteligente. [Produto] vai te ajudar a
        [economizar/ganhar/evitar] [benefício quantificável]."

      emotional_validation: |
        "Lembra daquela sensação de [dor/frustração] com [problema]?
        Você acabou de dar o passo para deixar isso para trás."

  benefit_reminder:
    purpose: "Relembrar por que compraram/se inscreveram"
    structure: |
      Com [produto], você agora tem:
      ✓ [Benefício 1 - mais impactante]
      ✓ [Benefício 2 - diferenciador]
      ✓ [Benefício 3 - conveniente]

  future_pacing:
    purpose: "Criar antecipação positiva pelo resultado"
    psychological_basis: "Mental rehearsal increases commitment"

    templates:
      timeline_based: |
        "Nas próximas [semanas/meses], você vai:
        → [Marco 1] em [tempo]
        → [Marco 2] em [tempo]
        → [Resultado final] em [tempo]"

      transformation_based: |
        "Imagine [cenário futuro positivo]. Isso é o que está
        à sua espera com [produto]."

      before_after: |
        "Antes: [estado atual ruim]
        Depois: [estado futuro desejado]
        E isso começa HOJE."

  guarantee_visibility:
    purpose: "Remover risco residual"
    elements:
      - Tipo de garantia (devolução, satisfação)
      - Prazo (30, 60, 90 dias)
      - Processo (como acionar)
      - Sem perguntas (se aplicável)

    template: |
      🛡️ **Sua Garantia:** [X] dias de satisfação ou seu dinheiro de volta.
      Zero risco. Zero burocracia. Você está 100% protegido.
```

---

### Step 4: One-Time Offer (OTO) Development

```yaml
oto_framework:

  psychology:
    primary_drivers:
      - FOMO: "Medo de perder oferta exclusiva"
      - Momentum: "Acabou de comprar, mais fácil comprar de novo"
      - Reduced_friction: "Dados de pagamento já inseridos"
      - Exclusivity: "Só para quem acabou de comprar"
      - Consistency: "Já se identificou como comprador"

    stat: "81% dos americanos dizem que encontrar uma boa oferta
          está em suas mentes durante toda a jornada de compra"

  oto_types:

    type_1_accelerator:
      name: "Acelerador"
      description: "Ajuda a obter resultados mais rápido"
      pricing: "30-50% do produto principal"
      examples:
        - "Implementação guiada"
        - "Templates prontos"
        - "Coaching adicional"
        - "Fast-track module"

      copy_angle: "Chegue ao resultado em metade do tempo"

    type_2_complement:
      name: "Complemento"
      description: "Produto que aumenta o valor do principal"
      pricing: "20-40% do produto principal"
      examples:
        - "Workbook físico para curso digital"
        - "Plugin adicional para software"
        - "Recurso avançado"

      copy_angle: "O par perfeito para [produto principal]"

    type_3_upgrade:
      name: "Upgrade"
      description: "Versão superior do que compraram"
      pricing: "Diferença + pequeno desconto"
      examples:
        - "Básico → Pro"
        - "Anual → Lifetime"
        - "Individual → Equipe"

      copy_angle: "Desbloqueie todo o potencial"

    type_4_bundle:
      name: "Bundle Exclusivo"
      description: "Pacote disponível só neste momento"
      pricing: "40-60% off do valor total separado"
      examples:
        - "Todos os bônus em um pacote"
        - "Biblioteca completa"
        - "Acesso a tudo"

      copy_angle: "Leve tudo por uma fração do preço"

    type_5_support:
      name: "Suporte Premium"
      description: "Acesso privilegiado a ajuda"
      pricing: "15-30% do produto principal"
      examples:
        - "Grupo VIP de suporte"
        - "Calls de Q&A"
        - "Revisão personalizada"

      copy_angle: "Nunca fique travado"

    type_6_done_for_you:
      name: "Feito Por Você"
      description: "Serviço que implementa pelo cliente"
      pricing: "100-300% do produto principal"
      examples:
        - "Setup completo"
        - "Configuração personalizada"
        - "Implementação full"

      copy_angle: "Sente e veja acontecer"

  oto_pricing_strategy:
    golden_rule: "OTO deve custar 30-60% do produto principal"

    price_anchoring:
      show_original: true
      show_savings: true
      show_percentage_off: true

      format: |
        De ~~R$[preço original]~~
        Por apenas **R$[preço OTO]**
        Você economiza R$[economia] ([X]% off)

    payment_options:
      low_oto: "Pagamento único"
      high_oto: "Opção de parcelamento"
      subscription: "Trial ou primeiro mês reduzido"

  oto_timing:
    golden_window:
      peak: "0-60 segundos após compra"
      high: "1-5 minutos"
      moderate: "5-15 minutos"
      declining: "15+ minutos"

    best_practice: "Apresentar OTO IMEDIATAMENTE após confirmação,
                   antes de entregar instruções de acesso"

  oto_copy_framework:

    four_part_formula:
      pattern_interrupt: "ESPERA! Antes de acessar [produto]..."
      value_bridge: "Já que você está investindo em [meta], você vai querer isso..."
      exclusive_offer: "Apenas para novos clientes de [produto]"
      urgency_close: "Esta oferta desaparece quando você sair desta página"

    headline_templates:
      - "Espera! Sua experiência pode ser ainda melhor..."
      - "⚡ Oferta Exclusiva Para Novos Membros"
      - "Antes de acessar, considere isso..."
      - "Uma última coisa que vai [benefício]..."
      - "PARE! Você vai querer ver isso..."

    body_structure: |
      [PATTERN INTERRUPT HEADLINE]

      Parabéns por investir em [produto]! Isso mostra que você
      está comprometido com [meta].

      E já que você está nessa jornada, quero te apresentar algo
      que vai [benefício principal do OTO]:

      **[NOME DO OTO]**

      [2-3 frases explicando o que é e por que importa AGORA]

      Com [OTO], você vai:
      ✓ [Benefício 1]
      ✓ [Benefício 2]
      ✓ [Benefício 3]

      **Preço normal:** ~~R$[original]~~
      **Seu preço exclusivo:** R$[OTO] (economize [X]%)

      ⏰ Esta oferta expira quando você sair desta página.

      [BOTÃO: SIM! Adicionar por R$[preço]]

      [Link discreto: Não, obrigado. Quero só meu acesso ao [produto].]

    decline_copy:
      soft: "Não, obrigado. Quero acessar minha compra agora."
      neutral: "Pular esta oferta →"
      avoid: "Não, eu não quero [benefício]" # Muito manipulativo
```

---

### Step 5: Next Steps Block Development

```yaml
next_steps_framework:

  structure:
    format: "Numbered list (1, 2, 3)"
    max_steps: 4
    clarity: "Específico e acionável"
    timeline: "Incluir quando possível"

  templates:

    digital_product:
      step_1:
        action: "Confira seu email"
        detail: "Você receberá seus dados de acesso em [X] minutos"
        fallback: "Não encontrou? Verifique spam/promoções"
      step_2:
        action: "Faça login na área de membros"
        detail: "[Link] - Use o email [email] e senha enviada"
      step_3:
        action: "Comece pelo [módulo/recurso específico]"
        detail: "É o melhor ponto de partida para [resultado rápido]"
      step_4:
        action: "Entre na comunidade"
        detail: "[Link] - Se apresente e conheça outros membros"

    lead_magnet:
      step_1:
        action: "Abra seu email"
        detail: "Seu [lead magnet] chega em até 2 minutos"
      step_2:
        action: "Adicione nosso email aos contatos"
        detail: "Garanta que nada importante se perca"
      step_3:
        action: "Baixe e [ação específica]"
        detail: "O [section X] é onde a mágica acontece"

    webinar_registration:
      step_1:
        action: "Adicione ao calendário"
        detail: "[Botões: Google, Outlook, Apple]"
      step_2:
        action: "Baixe o workbook"
        detail: "Você vai precisar dele durante a aula"
      step_3:
        action: "Chegue 5 minutos antes"
        detail: "[Data] às [hora] - não perca o início"
      step_4:
        action: "Prepare suas perguntas"
        detail: "Teremos Q&A ao vivo no final"

    physical_product:
      step_1:
        action: "Você receberá email de confirmação"
        detail: "Com número de rastreamento em até [X] horas"
      step_2:
        action: "Acompanhe a entrega"
        detail: "Link de tracking no email"
      step_3:
        action: "Ao receber, [ação específica]"
        detail: "Comece por [primeiro uso recomendado]"

  quick_win_integration:
    purpose: "Dar resultado imediato para criar momentum"
    criteria:
      - Achievable em <5 minutos
      - Esforço mínimo requerido
      - Produz resultado visível
      - Constrói em direção a meta maior

    examples:
      course: "Assista o vídeo de 3 min e identifique seu primeiro insight"
      software: "Configure [feature básica] em 2 minutos"
      ebook: "Leia a introdução e anote seu #1 takeaway"
      membership: "Se apresente na comunidade (2 min)"

    template: |
      💡 **Enquanto você espera, faça isso:**
      [Ação específica que leva 2-5 minutos e gera resultado/insight]
```

---

### Step 6: Referral Program Integration

```yaml
referral_framework:

  psychology:
    core_stat: "92% das pessoas confiam em recomendações de amigos e família"

    four_principles:

      social_currency:
        definition: "Pessoas compartilham o que as faz parecer bem"
        application:
          - Programa transparente sem termos escondidos
          - Faça o compartilhamento parecer premium
          - Mostre trust signals

      instant_gratification:
        definition: "Pessoas querem recompensas imediatas"
        application:
          - Recompensa instantânea ou muito rápida
          - Processo simples de compartilhamento
          - Múltiplos canais disponíveis
          - Código fácil de lembrar

      social_proof:
        definition: "Pessoas acreditam no que outros fazem"
        application:
          - Mostre números de participação
          - Destaque resultados de outros referrers
          - Crie senso de comunidade

      timing:
        definition: "Melhor momento é logo após experiência positiva"
        application:
          - Pedir no thank you page (pico de entusiasmo)
          - Follow-up após uso positivo
          - Triggers baseados em comportamento

  reward_structure:

    two_sided_model:
      description: "Ambos os lados ganham = 3x maior participação"
      example:
        referrer: "R$50 de crédito"
        referred: "20% off primeira compra"

    tiered_rewards:
      description: "Gamificação com múltiplos níveis"
      structure:
        tier_1:
          requirement: "1-2 indicações"
          reward: "10% desconto"
        tier_2:
          requirement: "3-5 indicações"
          reward: "Produto grátis"
        tier_3:
          requirement: "6+ indicações"
          reward: "Status VIP + acesso exclusivo"

  copy_templates:

    invitation_formula: |
      **Conhece alguém que se beneficiaria de [resultado]?**

      Dê a eles [benefício para amigo] no primeiro [produto].
      Você ganha [benefício para você] quando eles [ação].

      Seu link exclusivo: [LINK]

      [Botão: Copiar Link] [Botão: WhatsApp] [Botão: Email]

    stats_display: |
      📊 **Suas Indicações:**
      - Links compartilhados: [X]
      - Amigos que entraram: [X]
      - Créditos ganhos: R$[X]

  sharing_channels:
    priority_order:
      - WhatsApp (Brasil: principal)
      - Email
      - Telegram
      - Facebook
      - Twitter/X
      - Copiar link

    pre_written_messages:
      whatsapp: |
        Ei! Acabei de entrar no [Produto] e achei que você ia gostar.
        Eles estão dando [desconto] pra quem entra pelo meu link: [LINK]

      email:
        subject: "Achei isso e lembrei de você"
        body: |
          Oi [nome],

          Acabei de investir no [Produto] e é exatamente o que
          [você/a gente] estava procurando para [meta].

          Eles me deram um link especial que dá [desconto]
          pra quem eu indicar: [LINK]

          Dá uma olhada!
```

---

### Step 7: Community & Social Integration

```yaml
community_block:

  community_invitation:
    elements:
      - Nome da comunidade
      - Link de acesso
      - O que encontrará lá
      - Como se apresentar
      - Regras básicas

    template: |
      ## 👥 Junte-se à Nossa Comunidade

      Você agora faz parte de um grupo exclusivo de [X]+ [avatares]
      que estão [meta comum].

      **Entre no grupo:** [LINK/BOTÃO]

      **Ao entrar:**
      1. Se apresente usando: Nome, cidade, sua meta principal
      2. Leia as regras fixadas
      3. Diga "Oi!" no canal de boas-vindas

      Nos vemos lá! 👋

  social_sharing:
    purpose: "Ativar word-of-mouth no pico de entusiasmo"

    elements:
      - Mensagem pré-escrita
      - Botões por plataforma
      - Visual share card (se possível)
      - Incentivo opcional

    templates:
      purchase_celebration: |
        "Acabei de investir no meu [área] com [Produto]! 🚀
        Animado(a) para [resultado esperado]."

      event_registration: |
        "Vou participar do [Evento] em [data]!
        Quem mais vai? 🙋"

      achievement: |
        "Completei [marco] no [Produto]!
        [X] dias de trabalho valendo a pena. 💪"

    share_buttons:
      - LinkedIn (B2B, profissional)
      - Instagram Stories (visual, lifestyle)
      - Twitter/X (tech, opiniões)
      - Facebook (comunidade geral)
```

---

### Step 8: Onboarding Elements

```yaml
onboarding_framework:

  welcome_video:
    purpose: "Criar conexão pessoal e orientar início"

    best_practices:
      length: "30-90 segundos (ideal: 60s)"
      content:
        - Parabéns pessoal
        - O que esperar
        - Por onde começar
        - Promessa de suporte
      tone: "Acolhedor, animado, confiante"
      autoplay: false
      thumbnail: "Rosto amigável + botão play"
      transcript: "Disponível para quem prefere ler"

    script_template: |
      "Ei [Nome ou 'você aí']!

      Parabéns por entrar no [Produto]. Você tomou uma decisão
      que vai [resultado principal].

      Aqui está o que vai acontecer agora:
      [Passo 1, 2, 3 em 15 segundos]

      Minha recomendação? Comece por [primeiro módulo/ação].
      É onde você vai ter seu primeiro [quick win].

      Se precisar de qualquer coisa, estamos aqui.

      Bem-vindo(a) e vamos nessa!"

  progress_checklist:
    purpose: "Visualizar jornada e criar compromisso"

    psychological_basis:
      - Zeigarnik Effect: Tarefas incompletas ficam na mente
      - Goal Gradient: Aceleração perto da conclusão
      - Loss Aversion: Não perder progresso feito

    format: |
      ## ✅ Seu Checklist de Início

      □ Acessar área de membros
      □ Assistir vídeo de boas-vindas (3 min)
      □ Completar [Módulo/Ação 1]
      □ Entrar na comunidade
      □ [Quick win específico]

      **Dica:** Complete pelo menos 3 itens hoje!

  quick_start_resource:
    purpose: "Recurso imediato para começar"

    types:
      - PDF de início rápido
      - Primeiro módulo desbloqueado
      - Template inicial
      - Guia de configuração
      - Video tutorial curto

    positioning: "Disponível imediatamente, sem esperar email"
```

---

### Step 9: Support & Trust Elements

```yaml
support_trust_block:

  support_access:
    purpose: "Garantir que ajuda está disponível"

    elements:
      - Email de suporte
      - Chat (se disponível)
      - FAQ link
      - Horário de atendimento
      - Tempo de resposta esperado

    template: |
      ## 🤝 Precisa de Ajuda?

      📧 **Email:** [suporte@empresa.com]
      💬 **Chat:** [link] (seg-sex, 9h-18h)
      📚 **FAQ:** [link]

      Respondemos em até [X] horas úteis.

  guarantee_reinforcement:
    purpose: "Eliminar risco residual pós-compra"

    template: |
      🛡️ **Lembre-se:** Você tem [X] dias de garantia incondicional.

      Se por qualquer motivo não ficar satisfeito(a),
      basta enviar um email para [suporte] e devolvemos
      100% do seu investimento. Sem perguntas, sem burocracia.

      Zero risco. Você está protegido(a).

  trust_badges:
    elements:
      - Selo de compra segura
      - Certificações
      - Logos de parceiros/mídia
      - Número de clientes
```

---

### Step 10: Page Structure Assembly

```yaml
page_structure:

  layout_hierarchy:
    above_fold:
      - Confirmation headline (celebratório)
      - Order/action summary
      - Delivery expectations

    section_2:
      - Decision validation
      - Benefit reminder
      - Social proof snippet

    section_3_optional:
      - OTO offer (se aplicável)
      - Urgência e countdown
      - Accept/decline buttons

    section_4:
      - Next steps (numbered)
      - Quick win prompt
      - Timeline expectations

    section_5:
      - Community invitation
      - Referral program
      - Social sharing

    section_6:
      - Support access
      - Guarantee reminder
      - Footer

  visual_layout: |
    ┌─────────────────────────────────────────────────┐
    │ [1] CONFIRMAÇÃO                                 │
    │     🎉 Headline de sucesso                      │
    │     Resumo do pedido/ação                       │
    │     Expectativa de entrega                      │
    ├─────────────────────────────────────────────────┤
    │ [2] VALIDAÇÃO                                   │
    │     Reforço da decisão                          │
    │     Prova social                                │
    │     Future pacing                               │
    ├─────────────────────────────────────────────────┤
    │ [3] OTO (Opcional)                              │
    │     Pattern interrupt headline                  │
    │     Oferta exclusiva                            │
    │     Urgência + countdown                        │
    │     [SIM] [Não, obrigado]                       │
    ├─────────────────────────────────────────────────┤
    │ [4] PRÓXIMOS PASSOS                             │
    │     1. Primeiro passo                           │
    │     2. Segundo passo                            │
    │     3. Terceiro passo                           │
    │     💡 Quick win                                │
    ├─────────────────────────────────────────────────┤
    │ [5] ENGAJAMENTO                                 │
    │     👥 Comunidade                               │
    │     🎁 Programa de indicação                    │
    │     📢 Compartilhe                              │
    ├─────────────────────────────────────────────────┤
    │ [6] SUPORTE                                     │
    │     Contatos                                    │
    │     🛡️ Garantia                                │
    └─────────────────────────────────────────────────┘

  mobile_optimization:
    principles:
      - Single column layout
      - Large tap targets (44px mínimo)
      - Key info acima da dobra
      - Click-to-call para suporte
      - Formulários simplificados

    above_fold_priority:
      - Confirmação
      - Acesso/entrega info
      - CTA principal (se OTO)
```

---

## Complete Page Templates

### Template 1: Simple Lead Confirmation

```markdown
# ✅ Você está dentro!

Parabéns, [Nome]! Seu acesso ao **[Lead Magnet]** foi confirmado.

---

## O que acontece agora:

1. **Confira seu email** — Você receberá o [material] em até 5 minutos
2. **Verifique spam** — Se não encontrar, olhe na pasta de spam/promoções
3. **Adicione nosso email** — [email] aos seus contatos para não perder nada

---

## 💡 Enquanto espera:

[Link para conteúdo gratuito relevante ou introdução ao tema]

---

**Dúvidas?** [suporte@empresa.com]

Bem-vindo(a)! 🎉
```

### Template 2: Purchase Confirmation + OTO

```markdown
# 🎉 Compra Confirmada!

Parabéns, [Nome]! Você agora tem acesso ao **[Produto]**.

**Resumo do Pedido:**
- Produto: [Nome do Produto]
- Investimento: R$[valor]
- Pedido #: [número]

---

## Você fez a escolha certa

Assim como [X.XXX]+ pessoas que já [resultado alcançado] com [Produto],
você está no caminho para [transformação principal].

Nos próximos [tempo], você vai [benefício 1], [benefício 2] e [benefício 3].

---

## ⚡ ESPERA! Oferta Exclusiva Para Novos Membros

Já que você está investindo em [meta], tenho algo que vai acelerar seus resultados:

### [Nome do Upsell]

[Produto] é incrível, mas com [OTO] você vai [benefício principal do OTO]
em metade do tempo.

✓ [Benefício 1]
✓ [Benefício 2]
✓ [Benefício 3]

**De:** ~~R$[preço original]~~
**Seu preço exclusivo:** R$[preço OTO] (economia de [X]%)

⏰ **Esta oferta expira quando você sair desta página**

[🟢 SIM! Adicionar por R$[preço]]

[Não, obrigado. Quero só acessar minha compra →]

---

## Seus Próximos Passos:

1. **Confira seu email** para dados de acesso (em até 5 minutos)
2. **Faça login** na área de membros: [LINK]
3. **Comece pelo** [Módulo/Recurso específico]
4. **Entre na comunidade:** [LINK]

💡 **Dica:** Complete o [primeiro módulo] hoje — é onde você terá seu primeiro resultado.

---

## 🛡️ Sua Garantia

Você tem [X] dias para testar. Se não amar, devolvemos 100%.

**Precisa de ajuda?** [suporte@empresa.com]

Bem-vindo(a) à família [Produto]! 🚀
```

### Template 3: Course/Membership Onboarding

```markdown
# 🚀 Bem-vindo(a) ao [Curso/Membership]!

[Nome], sua jornada começa agora. Você fez uma escolha que vai mudar [área da vida].

---

## 🎬 Comece Aqui (2 minutos):

[VIDEO EMBED - Boas-vindas do instrutor]

---

## ✅ Seu Checklist de Início

□ **Acessar** a área de membros → [BOTÃO: Entrar]
□ **Assistir** vídeo de orientação (3 min)
□ **Completar** [Módulo 1: Nome]
□ **Entrar** na comunidade → [BOTÃO: Participar]
□ **Fazer** seu primeiro [quick win específico]

**Meta:** Complete pelo menos 3 itens hoje!

---

## 📚 Sua Jornada

**Semana 1:** [Tema] — Você vai aprender [outcome]
**Semana 2:** [Tema] — Você será capaz de [outcome]
**Semana 3:** [Tema] — Você terá [outcome]
**Semana 4:** [Tema] — Você estará [estado final]

---

## 👥 Sua Comunidade

Você agora faz parte de um grupo de [X]+ [avatares] comprometidos com [meta].

**Entre no grupo:** [LINK]

**Ao entrar:**
1. Se apresente: Nome, cidade, sua meta #1
2. Leia as regras no topo
3. Encontre seu "accountability partner"

---

## 🎁 Convide um Amigo

Conhece alguém que se beneficiaria deste [curso/programa]?

**Dê 25% off** para eles e **ganhe R$50 de crédito**.

Seu link: `[referral-link]`

[Copiar] [WhatsApp] [Email]

---

## 🤝 Suporte

- **Dúvidas de conteúdo:** Comunidade
- **Problemas técnicos:** [suporte@empresa.com]
- **Chat ao vivo:** [LINK] (seg-sex, 9h-18h)

Respondemos em até 24 horas úteis.

---

🛡️ **Lembre-se:** [X] dias de garantia. Zero risco.

Estamos animados para ver sua transformação! 💪
```

### Template 4: Webinar/Event Registration

```markdown
# ✅ Inscrição Confirmada!

**[Nome do Evento]**

📅 [Data completa]
⏰ [Horário] ([Timezone])
📍 [Online via Zoom/Local]

[Adicionar ao Google Calendar] [Adicionar ao Outlook] [Adicionar ao Apple Calendar]

---

## 📋 Antes do Evento:

1. **Baixe o workbook** — Você vai precisar durante a aula
   [BOTÃO: Baixar Workbook]

2. **Bloqueie sua agenda** — Chegue 5 minutos antes

3. **Prepare suas perguntas** — Teremos Q&A ao vivo

4. **Teste seu áudio/vídeo** — Verifique que tudo funciona

---

## O Que Você Vai Aprender:

✓ [Tópico/Benefício 1]
✓ [Tópico/Benefício 2]
✓ [Tópico/Benefício 3]
✓ [Bônus/Surpresa se houver]

---

## 📢 Convide Alguém

Conhece alguém que se beneficiaria deste evento?

Compartilhe o link de inscrição:
`[link-do-evento]`

[WhatsApp] [Email] [Copiar Link]

---

## ⚠️ Importante

- **Não poderá participar ao vivo?** Responda ao email de confirmação e enviaremos a gravação.
- **Dúvidas?** [suporte@empresa.com]

Nos vemos em [data]! 🎯
```

### Template 5: Referral-Focused Thank You

```markdown
# 🎉 Parabéns! Você está dentro!

[Nome], sua [compra/inscrição] está confirmada.

Confira seu email para [detalhes de acesso/próximos passos].

---

## 🎁 Compartilhe e Ganhe

Gostou do [Produto]? Seus amigos vão gostar também!

**Seu amigo ganha:** 25% off na primeira compra
**Você ganha:** R$25 de crédito para cada amigo

### Seu Link Exclusivo:
```
[https://empresa.com/ref/SEU-CODIGO]
```

[📋 Copiar Link]

---

## Compartilhe em 1 Clique:

[📱 WhatsApp] [✉️ Email] [📘 Facebook] [🐦 Twitter]

**Mensagem pronta:**
> "Acabei de entrar no [Produto] e estou amando!
> Se você está querendo [resultado], usa meu link que você ganha desconto: [LINK]"

---

## 📊 Seu Painel de Indicações

| Métrica | Valor |
|---------|-------|
| Links compartilhados | 0 |
| Amigos cadastrados | 0 |
| Créditos ganhos | R$0 |

*Atualiza em tempo real*

---

## 🏆 Desbloqueie Recompensas

| Indicações | Recompensa |
|------------|------------|
| 1-2 | R$25 crédito cada |
| 3-5 | + Acesso ao [bônus] |
| 6+ | + Status VIP |

---

## Seus Próximos Passos:

1. Confira o email com seus dados de acesso
2. Compartilhe seu link com 3 amigos
3. Acompanhe suas indicações aqui

**Suporte:** [suporte@empresa.com]

Bem-vindo(a)! 🚀
```

### Template 6: High-Ticket Premium Confirmation

```markdown
# 🏆 Bem-vindo(a) ao [Programa Premium]

[Nome], você fez um investimento significativo em si mesmo(a).
Isso demonstra compromisso real com [transformação].

---

## 🎬 Mensagem Pessoal do [Founder/Instrutor]

[VIDEO EMBED - Mensagem pessoal de boas-vindas, 60-90 segundos]

---

## Sua Jornada Premium

Você agora tem acesso a:

✓ **[Benefício 1]** — [descrição breve]
✓ **[Benefício 2]** — [descrição breve]
✓ **[Benefício 3]** — [descrição breve]
✓ **[Benefício 4]** — [descrição breve]
✓ **Suporte VIP** — Resposta prioritária em até [X] horas

---

## 📞 Sua Onboarding Call

Como membro [Tier/Programa], você tem direito a uma call de onboarding
personalizada com [pessoa].

[BOTÃO: Agendar Minha Call]

---

## 🔐 Seus Acessos

**Área de Membros:** [LINK]
**Comunidade VIP:** [LINK]
**Suporte Direto:** [whatsapp/email VIP]

Seus dados de login foram enviados para [email].

---

## 🛡️ Sua Garantia Premium

Você tem [X] dias de garantia incondicional. Se por qualquer motivo
não ficar 100% satisfeito(a), devolvemos cada centavo investido.

Acreditamos tanto no [Programa] que assumimos todo o risco.

---

## 📱 Linha Direta

Como membro premium, você tem acesso direto:

**WhatsApp VIP:** [número]
**Email prioritário:** [email-vip]

Respondemos em até [X] horas.

---

Estamos honrados em fazer parte da sua jornada.

Com gratidão,
[Nome do Founder]
[Assinatura/Foto]
```

---

## Quality Checklist

```yaml
confirmation_check:
  - [ ] Headline confirma claramente a ação realizada
  - [ ] Resumo do pedido/ação está presente e preciso
  - [ ] Próximos passos estão claros e específicos
  - [ ] Timeline de entrega está comunicada

remorse_prevention_check:
  - [ ] Validação da decisão presente
  - [ ] Benefícios relembrados
  - [ ] Prova social incluída
  - [ ] Garantia visível (se aplicável)

oto_check (se aplicável):
  - [ ] Complementa a compra original
  - [ ] NÃO bloqueia acesso ao produto
  - [ ] Fácil de recusar sem culpa
  - [ ] Urgência é genuína (não fake)
  - [ ] Preço ancora corretamente

engagement_check:
  - [ ] Quick win identificado
  - [ ] Comunidade convidada (se houver)
  - [ ] Referral program apresentado
  - [ ] Social sharing facilitado

support_check:
  - [ ] Canais de suporte visíveis
  - [ ] FAQ acessível
  - [ ] Tempo de resposta comunicado

mobile_check:
  - [ ] Layout funciona em mobile
  - [ ] Botões são grandes o suficiente
  - [ ] Info crítica acima da dobra
  - [ ] Carregamento rápido
```

---

## Metrics to Track

```yaml
thank_you_page_metrics:

  primary_kpis:
    oto_conversion_rate:
      formula: "OTO accepts / Thank you page views"
      benchmark: "10-25%"

    secondary_action_rate:
      formula: "Secondary CTAs clicked / Page views"
      benchmark: "30-50%"

    referral_initiation_rate:
      formula: "Referral links generated / Page views"
      benchmark: "5-15%"

  secondary_metrics:
    community_join_rate:
      benchmark: "15-30%"
    quick_win_completion:
      benchmark: "40-60%"
    feedback_response_rate:
      benchmark: "10-20%"
    social_share_rate:
      benchmark: "2-8%"
    support_ticket_reduction:
      benchmark: "20-40% reduction vs. no thank you page"

  revenue_tracking:
    oto_revenue_monthly: "OTO conversions × OTO price"
    referral_revenue_monthly: "Referred conversions × Average order value"
    ltv_impact: "Compare LTV of customers who engaged vs. didn't"
```

---

## Copywriter Recommendations

| Contexto | Copywriter | Por quê |
|----------|------------|---------|
| OTO agressivo com urgência | Dan Kennedy | Master de urgência e escassez |
| Thank you elegante/premium | David Ogilvy | Tom sofisticado, brand-building |
| Thank you com storytelling | Gary Halbert | Conexão emocional profunda |
| Thank you de curso/digital | Frank Kern | Casual, acolhedor, coach energy |
| Thank you high-ticket | Alex Hormozi | Value reinforcement, lógica |
| Referral e viralidade | Ryan Deiss | Otimização de funnel |
| Onboarding de SaaS | Joanna Wiebe | Clareza, UX writing |

---

## Output

```yaml
deliverables:
  - confirmation_block: "Bloco de confirmação completo"
  - validation_copy: "Copy de validação da decisão"
  - oto_section: "Seção de OTO (se aplicável)"
  - next_steps_block: "Bloco de próximos passos"
  - referral_section: "Seção de programa de indicação"
  - community_block: "Bloco de comunidade (se aplicável)"
  - support_section: "Seção de suporte"
  - complete_page: "Página completa montada"
  - quality_checklist: "Checklist de qualidade preenchido"
  - metrics_setup: "Configuração de métricas recomendadas"

format: markdown
```

---

*Task Version: 2.0*
*Methodology: Post-Purchase Psychology + OTO Conversion + Referral Activation*
*Based on: CXL, TheGood, ConvertCart, Campaign Monitor, WPFunnels Research*
*Lines: 1200+*
