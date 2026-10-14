# Copy Squad - Arquitetura Atômica

## Overview

Esta squad usa **arquitetura atômica**: agentes são compactos (~300-500 linhas), e frameworks/voice/phrases são carregados sob demanda de arquivos externos.

**24 agentes ativos** organizados em 5 camadas (0-3 + orchestration/tooling), conforme definido em `config.yaml` v4.0.0.

## IMPORTANTE: Loading é Manual

Quando um agente referencia `load: frameworks/kennedy/10-rules.yaml`, você precisa fazer um **Read manual** desse arquivo.

**Não existe carregamento automático.** O `load:` é uma diretiva de documentação que indica qual arquivo usar.

### Exemplo de Uso

```
1. Ativar agente: @dan-kennedy
2. Usar comando: *urgency
3. Agente indica: "load: frameworks/kennedy/urgency-engineering.yaml"
4. VOCÊ faz: Read squads/copy/frameworks/kennedy/urgency-engineering.yaml
5. Agente aplica framework ao seu caso
```

## Estrutura de Arquivos

```
squads/copy/
├── agents/              # Agentes core (300-500 linhas cada)
│   ├── gary-halbert.md
│   ├── eugene-schwartz.md
│   ├── dan-kennedy.md
│   └── ... (24 agentes ativos)
│
├── frameworks/          # Frameworks por copywriter (60 arquivos)
│   ├── kennedy/         # 10 frameworks Dan Kennedy
│   │   ├── 10-rules.yaml
│   │   ├── urgency-engineering.yaml
│   │   ├── guarantee-architecture.yaml
│   │   └── ...
│   ├── schwartz/        # 10 frameworks Eugene Schwartz
│   │   ├── five-levels-of-awareness.yaml
│   │   ├── five-stages-of-sophistication.yaml
│   │   └── ...
│   └── ... (outros copywriters)
│
├── voice/               # DNA de voz (6 arquivos)
│   ├── kennedy.yaml
│   ├── schwartz.yaml
│   └── ...
│
├── phrases/             # Frases signature (6 arquivos)
│   ├── kennedy.yaml
│   └── ...
│
├── authority/           # Provas de autoridade (6 arquivos)
│   ├── kennedy.yaml
│   └── ...
│
├── tasks/               # Tasks específicas de copy
├── workflows/           # Workflows de produção
├── checklists/          # Checklists de qualidade
│
└── archive/             # Agentes arquivados (não usar)
    ├── README.md
    └── agents/
        └── ramit-sethi.md     [ARCHIVED]
```

## Tier System

Source of truth: `config.yaml` v4.0.0

### Tier 0 — Foundation / Diagnóstico

Mestres clássicos que definem os fundamentos da persuasão e consciência de mercado.

| Agente | Especialidade |
|--------|---------------|
| claude-hopkins | Scientific Advertising & Tested Methods |
| eugene-schwartz | Five Levels of Awareness & Sophistication |
| robert-collier | Mental Conversation Analysis |

### Tier 1 — Masters / Direct Response

Mestres do direct response com resultados comprovados em vendas diretas.

| Agente | Especialidade |
|--------|---------------|
| gary-halbert | The Prince of Print & Boron Letters |
| gary-bencivenga | Persuasion Engineering |
| david-ogilvy | Brand Direct Response |
| clayton-makepeace | Visceral Copy & Emotional Amplification |
| parris-lampropoulos | Fascinations & Bullets (700-to-100) |
| john-carlton | Simple Writing System |
| jim-rutz | Magalogs & Direct Mail |
| david-deutsch | Direct Mail & Sales Letters |

### Tier 2 — Systematizers / Frameworks

Copywriters que criaram sistemas e frameworks replicáveis.

| Agente | Especialidade |
|--------|---------------|
| dan-kennedy | Magnetic Marketing & No B.S. |
| todd-brown | E5 Method & Big Idea |
| jeff-walker | Product Launch Formula (PLF) |
| frank-kern | Intent-Based Branding & Mass Control |
| stefan-georgi | RMBC Method |
| russell-brunson | Funnels & Book Launch Systems |

### Tier 3 — Specialists / Digital Era

Especialistas em canais digitais específicos (email, social, content).

| Agente | Especialidade |
|--------|---------------|
| jon-benson | Video Sales Letters (VSL) |
| dan-koe | Digital Writing & One-Person Business |
| andre-chaperon | Soap Opera Sequences |
| ben-settle | Daily Email & Infotainment |
| ry-schwartz | Email Copywriting & Sequences |

### Tool — Quality & Orchestration

| Agente | Função |
|--------|--------|
| copy-chief | Orchestrator / Quality Review |
| joe-sugarman | Triggers & Quality Analysis Tool |

**Total: 24 agentes ativos** (3 Tier 0 + 8 Tier 1 + 6 Tier 2 + 5 Tier 3 + 2 orchestration/tooling = 24)

## Agentes Arquivados

Os seguintes agentes foram movidos para `archive/` e **não devem ser usados**:

| Agente | Razão do Arquivamento |
|--------|----------------------|
| ramit-sethi | Personal finance educator, not copywriter |

Alex Hormozi nao integra o roster ativo atual. Para surfaces de oferta, roteie por Kennedy, Todd Brown, Georgi ou Brunson conforme o formato.

### Reativação

Se precisar de um agente arquivado:
1. Verifique se outro agente ativo cobre o caso de uso
2. Se não cobrir, documente a justificativa
3. Mova de `archive/agents/` para `agents/`
4. Atualize este documento e `config.yaml`

## Benefícios da Arquitetura Atômica

1. **Agentes menores**: Mais fácil de manter e entender
2. **Frameworks reutilizáveis**: Mesmo framework usado por múltiplos agentes
3. **Separação de concerns**: Persona vs. metodologia vs. voz
4. **Evolução independente**: Atualizar framework sem tocar no agente

## Trade-offs

1. **Loading manual**: Requer Read explícito dos frameworks
2. **Mais arquivos**: 60+ arquivos de suporte vs. 24 superfícies runtime
3. **Curva de aprendizado**: Entender a estrutura leva tempo

## Métricas de Redução

| Agente | Antes | Depois | Redução Real* |
|--------|-------|--------|---------------|
| dan-kennedy | 2,796 linhas | 314 linhas + deps | ~73% |
| eugene-schwartz | 2,134 linhas | 350 linhas + deps | ~70% |
| copy-chief | 1,500 linhas | 280 linhas + deps | ~75% |

*Redução real considera agente + frameworks + voice + phrases + authority

---

*Arquitetura v4.0 - Runtime Baseline Alignment*
*Última atualização: 2026-03-10*
