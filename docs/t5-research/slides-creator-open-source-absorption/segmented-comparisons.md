# Comparações Segmentadas — Apps, Skills e Engines

Data: 2026-05-18

Um ranking único entre app completo, skill técnica, renderer e agente acadêmico não é justo. A leitura correta deste bench tem três comparações por classe, e o consolidado deve ser usado apenas como mapa de absorção.

**Atualização:** o segmento `Skills, agentes e workflows` foi recalculado depois da melhoria da `slide-creator` autocontida.

## Apps e produto final

Compara produtos com UI/app, tema, sharing, edição visual e operação self-hosted.

### Ranking justo

| Rank | Player | Score |
|---:|---|---:|
| 1 | Presenton | 80.77 |
| 2 | presentation-ai | 76.91 |
| 3 | banana-slides | 69.91 |

### Matriz profunda

| Dimensão | Peso | Presenton | banana-slides | presentation-ai |
|---|---:|---:|---:|---:|
| Prompt para deck no app | 5.00 | 95 | 92 | 90 |
| Editor de outline | 4.00 | 88 | 78 | 94 |
| Canvas/editor web | 7.00 | 84 | 91 | 91 |
| Loop prompt-to-edit | 7.00 | 68 | 96 | 82 |
| Edição por bloco/região | 5.00 | 60 | 96 | 78 |
| Temas/templates prontos | 5.00 | 81 | 71 | 91 |
| Sistema de marca/tokens | 4.00 | 88 | 84 | 92 |
| Importação de documentos | 4.00 | 90 | 65 | 55 |
| Export PPTX/PDF | 5.00 | 74 | 66 | 67 |
| Editabilidade pós-export | 5.00 | 71 | 60 | 64 |
| Imagens AI/stock | 3.00 | 91 | 77 | 85 |
| Charts/tabelas no app | 3.00 | 72 | 55 | 60 |
| Sharing/publicação | 5.00 | 75 | 70 | 92 |
| Colaboração/revisão | 4.00 | 45 | 55 | 88 |
| Analytics do deck | 3.00 | 35 | 25 | 40 |
| Self-hosted produto | 5.00 | 96 | 69 | 74 |
| Desktop app/package | 3.00 | 90 | 15 | 15 |
| BYOK/providers/local | 4.00 | 97 | 74 | 85 |
| API exposta pelo app | 4.00 | 98 | 68 | 72 |
| MCP/automação do app | 3.00 | 95 | 45 | 55 |
| Polimento visual | 3.00 | 82 | 88 | 86 |
| Docs de instalação/operação | 2.00 | 86 | 58 | 72 |
| Licença segura | 3.00 | 98 | 25 | 95 |
| Maturidade de produto | 4.00 | 92 | 65 | 76 |

## Skills, agentes e workflows

Compara capacidades de raciocínio, orquestração, QA, skill-runtime, validação e geração governada. Atualizado após a skill slide-creator se tornar autocontida.

### Ranking justo

| Rank | Player | Score |
|---:|---|---:|
| 1 | slide creator skill | 88.79 |
| 2 | PPTAgent | 77.01 |
| 3 | PresentAgent-2 | 73.84 |
| 4 | powerpoint-skill | 68.46 |

### Matriz profunda

| Dimensão | Peso | slide creator skill | PPTAgent | powerpoint-skill | PresentAgent-2 |
|---|---:|---:|---:|---:|---:|
| Briefing e elicitação | 4.76 | 96 | 78 | 63 | 80 |
| Governança story/task | 4.76 | 99 | 84 | 66 | 77 |
| Estratégia narrativa | 6.67 | 99 | 80 | 55 | 72 |
| Planejamento de outline | 4.76 | 96 | 87 | 63 | 83 |
| Raciocínio slide-a-slide | 5.71 | 98 | 92 | 70 | 88 |
| Reflexão/revisão agentic | 5.71 | 96 | 92 | 82 | 88 |
| Research/source grounding | 5.71 | 88 | 78 | 40 | 95 |
| Rastreabilidade de evidências | 4.76 | 92 | 77 | 55 | 82 |
| Rubrica QA | 5.71 | 98 | 92 | 90 | 88 |
| Revisão de editabilidade | 4.76 | 92 | 72 | 88 | 55 |
| Diagramas técnicos | 3.81 | 82 | 55 | 98 | 35 |
| Objetos PPTX nativos | 4.76 | 60 | 78 | 88 | 67 |
| Raciocínio de charts/tabelas | 3.81 | 78 | 74 | 87 | 67 |
| Workflow multimodal | 2.86 | 52 | 40 | 30 | 94 |
| Contratos de ferramentas | 3.81 | 85 | 63 | 30 | 74 |
| Execução CLI/headless | 3.81 | 82 | 78 | 60 | 70 |
| Controle de providers | 2.86 | 87 | 63 | 73 | 78 |
| Privacidade/local | 3.81 | 88 | 70 | 90 | 78 |
| Fixtures/eval automatizado | 2.86 | 94 | 76 | 78 | 69 |
| Docs da skill/workflow | 1.90 | 96 | 75 | 78 | 62 |
| Absorvibilidade no SINKRA | 3.81 | 98 | 87 | 88 | 37 |
| Superfície de integração | 2.86 | 72 | 66 | 36 | 73 |
| Maturidade operacional | 2.86 | 86 | 67 | 63 | 55 |
| Fit para revisão humana | 2.87 | 86 | 76 | 63 | 67 |

## Engines, renderer e runtime

Compara bibliotecas/runtimes para gerar, exportar, rodar localmente e integrar por API/CLI.

### Ranking justo

| Rank | Player | Score |
|---:|---|---:|
| 1 | ppt-master | 82.13 |
| 2 | Presenton | 74.11 |
| 3 | powerpoint-skill | 64.40 |
| 4 | slide-deck-ai | 59.97 |

### Matriz profunda

| Dimensão | Peso | ppt-master | Presenton | slide-deck-ai | powerpoint-skill |
|---|---:|---:|---:|---:|---:|
| Fidelidade de shapes PPTX | 7.92 | 98 | 75 | 65 | 88 |
| Texto editável real | 5.94 | 97 | 72 | 59 | 88 |
| Charts nativos | 4.95 | 92 | 72 | 58 | 86 |
| Tabelas nativas | 3.96 | 92 | 72 | 58 | 86 |
| Replicação de tema/template | 4.95 | 90 | 72 | 42 | 47 |
| Profundidade OOXML | 5.94 | 95 | 55 | 45 | 67 |
| Animações/transições | 2.97 | 92 | 35 | 25 | 45 |
| Math/OMML | 3.96 | 78 | 45 | 42 | 98 |
| Render de diagramas | 3.96 | 80 | 52 | 46 | 94 |
| Motor de layout | 3.96 | 90 | 75 | 53 | 65 |
| Preview/anotações | 3.96 | 95 | 55 | 25 | 35 |
| Parsing de documentos | 3.96 | 90 | 90 | 88 | 55 |
| Parsing URL/mídia | 1.98 | 82 | 60 | 45 | 25 |
| API runtime | 4.95 | 50 | 98 | 78 | 35 |
| MCP/runtime agentic | 4.95 | 40 | 95 | 60 | 25 |
| CLI/headless | 4.95 | 72 | 85 | 92 | 60 |
| Docker/self-hosted | 4.95 | 65 | 95 | 80 | 45 |
| Distribuição desktop | 1.98 | 35 | 90 | 15 | 10 |
| Abstração de providers | 3.96 | 80 | 95 | 92 | 55 |
| Modelos locais/BYOK | 3.96 | 90 | 98 | 92 | 90 |
| Áudio/vídeo | 2.97 | 89 | 33 | 23 | 38 |
| Harness QA técnico | 3.96 | 83 | 60 | 50 | 77 |
| Docs runtime | 1.98 | 70 | 86 | 65 | 78 |
| Licença/runtime seguro | 2.98 | 95 | 98 | 95 | 95 |

## Mapa de Absorção Composto

- **App layer:** Presenton como base de produto/API/self-hosting, com padrões de UX de banana-slides e presentation-ai.
- **Skill/agentic layer:** slide creator skill agora lidera narrativa, QA, contratos, playbooks, validação de pacote e independência; PPTAgent/PresentAgent-2 seguem como inspiração de planning/research.
- **Engine/runtime layer:** ppt-master para PPTX nativo editável, Presenton para runtime/API/MCP, slide-deck-ai para fluxo Python/headless e powerpoint-skill para matemática/diagramas/QA técnico.

## Decisão

Não existe vencedor absoluto entre classes diferentes. O benchmark mede três campeões por classe e uma composição alvo.
