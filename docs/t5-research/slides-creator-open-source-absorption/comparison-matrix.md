# Micro Capability Matrix — slides creator open-source absorption

Esta matriz quebra 36 dimensões macro em 108 microdimensões. Cada célula usa escala 0-100 por cinco lentes: cobertura, profundidade, fidelidade, evidência e absorvibilidade.

Última atualização: 2026-05-18 (após Wave 3 spike).

## Ranking consolidado

| Rank | Player | Score |
|---:|---|---:|
| 1 | slide creator skill | 81.07 |
| 2 | ppt-master | 74.79 |
| 3 | Presenton | 74.09 |
| 4 | presentation-ai | 67.52 |
| 5 | PPTAgent | 63.52 |
| 6 | PresentAgent-2 | 62.68 |
| 7 | banana-slides | 60.16 |
| 8 | powerpoint-skill | 55.07 |
| 9 | slide-deck-ai | 53.28 |

## Matriz

| Dimensão micro | Grupo | Peso | slide creator skill | ppt-master | Presenton | presentation-ai | PPTAgent | PresentAgent-2 | banana-slides | powerpoint-skill | slide-deck-ai | Líder |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Captura intenção, público, tese e restrições antes de gerar | Entrada | 0.6667 | 98 | 82 | 96 | 91 | 75 | 88 | 93 | 70 | 84 | slide creator skill |
| Transforma prompt em outline revisável antes do deck | Entrada | 0.6667 | 96 | 80 | 97 | 93 | 75 | 88 | 93 | 70 | 85 | Presenton |
| Gera deck completo a partir de ideia curta | Entrada | 0.6667 | 92 | 82 | 98 | 92 | 75 | 88 | 95 | 64 | 85 | Presenton |
| Cobertura de tipos PDF/DOCX/PPTX/MD | Entrada | 0.6667 | 77 | 94 | 93 | 55 | 70 | 80 | 65 | 55 | 90 | ppt-master |
| Extração semântica de claims, seções, tabelas e evidências | Entrada | 0.6667 | 82 | 90 | 90 | 55 | 72 | 83 | 65 | 55 | 87 | ppt-master |
| Ingestão/reaproveitamento de PPTX existente | Entrada | 0.6667 | 75 | 95 | 90 | 57 | 70 | 80 | 69 | 55 | 88 | ppt-master |
| Ingestão de URL/site/documento remoto | Entrada | 0.6667 | 59 | 85 | 61 | 35 | 45 | 96 | 40 | 25 | 45 | PresentAgent-2 |
| YouTube/vídeo como fonte de narrativa | Entrada | 0.6667 | 57 | 82 | 60 | 35 | 45 | 97 | 42 | 20 | 45 | PresentAgent-2 |
| Mapeia mídia para momentos/trechos do deck | Entrada | 0.6667 | 56 | 83 | 60 | 35 | 45 | 98 | 40 | 25 | 45 | PresentAgent-2 |
| Roteia fonte por tipo: web, scholar, local, vídeo ou benchmark | Entrada | 1 | 93 | 55 | 49 | 45 | 80 | 98 | 35 | 40 | 55 | PresentAgent-2 |
| Liga claim a evidência e confiança | Entrada | 1 | 93 | 55 | 50 | 43 | 80 | 98 | 35 | 40 | 55 | PresentAgent-2 |
| Verifica frescor e risco factual | Entrada | 1 | 92 | 55 | 50 | 45 | 79 | 97 | 32 | 40 | 55 | PresentAgent-2 |
| Outline editável antes da geração | Planejamento | 0.6667 | 100 | 60 | 91 | 98 | 82 | 78 | 78 | 55 | 65 | slide creator skill |
| Hierarquia seções > slides > beats | Planejamento | 0.6667 | 100 | 62 | 88 | 94 | 85 | 80 | 78 | 55 | 65 | slide creator skill |
| Rastreio outline -> slide final | Planejamento | 0.6667 | 100 | 63 | 88 | 94 | 84 | 78 | 76 | 55 | 65 | slide creator skill |
| Define mudança de crença da audiência | Planejamento | 1.3333 | 100 | 60 | 61 | 58 | 81 | 72 | 43 | 55 | 52 | slide creator skill |
| Usa lógica SCQA/Pyramid/action-title | Planejamento | 1.3333 | 100 | 60 | 62 | 58 | 82 | 73 | 45 | 55 | 52 | slide creator skill |
| Conecta história ao CTA ou decisão final | Planejamento | 1.3333 | 100 | 60 | 63 | 59 | 80 | 72 | 45 | 55 | 50 | slide creator skill |
| Mapa de função por slide | Planejamento | 1 | 100 | 76 | 80 | 78 | 95 | 88 | 60 | 72 | 68 | slide creator skill |
| Critica slides decisivos antes da produção total | Planejamento | 1 | 100 | 76 | 80 | 78 | 94 | 90 | 60 | 70 | 68 | slide creator skill |
| Fluxo de fala/transição entre slides | Planejamento | 1 | 100 | 78 | 80 | 78 | 92 | 88 | 60 | 73 | 68 | slide creator skill |
| Variedade de layout sem virar colagem | Design | 0.6667 | 99 | 88 | 82 | 89 | 80 | 76 | 92 | 78 | 62 | slide creator skill |
| Controle de densidade e legibilidade | Design | 0.6667 | 99 | 88 | 82 | 86 | 80 | 76 | 88 | 81 | 62 | slide creator skill |
| Qualidade visual observada no render final | Design | 0.6667 | 99 | 89 | 82 | 90 | 80 | 76 | 93 | 78 | 62 | slide creator skill |
| Manifesta templates importados | Design | 0.6667 | 100 | 100 | 65 | 90 | 72 | 45 | 42 | 45 | 40 | slide creator skill |
| Replica linguagem visual de template/brand deck | Design | 0.6667 | 100 | 100 | 67 | 91 | 72 | 45 | 42 | 45 | 40 | slide creator skill |
| Seleciona template por função do slide | Design | 0.6667 | 100 | 95 | 65 | 88 | 74 | 45 | 42 | 47 | 40 | slide creator skill |
| Tokens de cor, fonte, espaçamento e grid | Design | 0.6667 | 99 | 78 | 91 | 96 | 65 | 55 | 84 | 54 | 45 | slide creator skill |
| Runtime aplica tema consistentemente | Design | 0.6667 | 99 | 78 | 91 | 97 | 65 | 55 | 88 | 52 | 45 | slide creator skill |
| Guardrails de marca e anti-padrões | Design | 0.6667 | 100 | 78 | 88 | 94 | 65 | 55 | 84 | 55 | 45 | slide creator skill |
| Gera shapes/textos nativos DrawingML | Renderização | 1.6667 | 84 | 100 | 75 | 70 | 82 | 68 | 70 | 92 | 65 | ppt-master |
| Evita transformar tudo em imagem | Renderização | 1.6667 | 88 | 100 | 75 | 70 | 80 | 68 | 67 | 92 | 65 | ppt-master |
| Reabre no PowerPoint sem quebrar layout | Renderização | 1.6667 | 58 | 100 | 76 | 70 | 80 | 68 | 70 | 91 | 65 | ppt-master |
| Charts nativos e editáveis | Renderização | 1 | 77 | 97 | 72 | 60 | 70 | 62 | 55 | 91 | 58 | ppt-master |
| Reconstrói tabelas com hierarquia e destaques | Renderização | 1 | 78 | 96 | 72 | 60 | 70 | 62 | 55 | 91 | 58 | ppt-master |
| Contrato de dados para charts/tabelas | Renderização | 1 | 90 | 92 | 74 | 62 | 70 | 62 | 53 | 86 | 58 | ppt-master |
| LaTeX/OMML para matemática editável ou nítida | Renderização | 1 | 83 | 80 | 45 | 30 | 55 | 35 | 25 | 100 | 42 | powerpoint-skill |
| Mermaid/Graphviz/TikZ/diagram engines | Renderização | 1 | 84 | 78 | 48 | 30 | 55 | 35 | 25 | 100 | 42 | powerpoint-skill |
| QA técnico de overflow, tema e legibilidade | Renderização | 1 | 86 | 80 | 45 | 30 | 55 | 35 | 25 | 100 | 42 | powerpoint-skill |
| Animações/transições padrão | Renderização | 0.6667 | 32 | 98 | 35 | 25 | 40 | 30 | 25 | 46 | 25 | ppt-master |
| Controle por objeto/ordem/timing | Renderização | 0.6667 | 31 | 98 | 35 | 25 | 40 | 30 | 25 | 45 | 25 | ppt-master |
| Valida configuração de animações | Renderização | 0.6667 | 32 | 97 | 35 | 25 | 40 | 30 | 25 | 45 | 25 | ppt-master |
| Speaker notes estruturadas | Multimídia | 0.6667 | 92 | 92 | 30 | 35 | 35 | 82 | 55 | 43 | 25 | slide creator skill |
| TTS/narração automática | Multimídia | 0.6667 | 42 | 95 | 30 | 35 | 35 | 85 | 56 | 40 | 25 | ppt-master |
| Sincroniza áudio com slide/trecho | Multimídia | 0.6667 | 72 | 93 | 30 | 35 | 35 | 87 | 55 | 40 | 25 | ppt-master |
| Exporta deck para vídeo/MP4 | Multimídia | 0.6667 | 36 | 91 | 35 | 40 | 35 | 100 | 96 | 35 | 20 | PresentAgent-2 |
| Q&A ou navegação sobre vídeo | Multimídia | 0.6667 | 36 | 88 | 35 | 40 | 35 | 100 | 93 | 35 | 20 | PresentAgent-2 |
| Pipeline de assets multimídia | Multimídia | 0.6667 | 72 | 90 | 35 | 40 | 35 | 99 | 96 | 35 | 20 | PresentAgent-2 |
| Preview vivo local/web | Editor | 1 | 51 | 100 | 57 | 71 | 60 | 45 | 70 | 35 | 25 | ppt-master |
| Anotações visuais viram correções | Editor | 1 | 52 | 100 | 55 | 68 | 60 | 45 | 73 | 35 | 25 | ppt-master |
| Revisão por screenshot/thumbnail | Editor | 1 | 57 | 99 | 55 | 68 | 60 | 45 | 70 | 39 | 25 | ppt-master |
| Edição por linguagem natural | Editor | 1.3333 | 80 | 78 | 68 | 85 | 52 | 55 | 100 | 35 | 30 | banana-slides |
| Diff antes de aplicar edição | Editor | 1.3333 | 85 | 80 | 68 | 82 | 52 | 55 | 97 | 35 | 30 | banana-slides |
| Histórico reversível de edição | Editor | 1.3333 | 59 | 78 | 69 | 84 | 52 | 55 | 96 | 35 | 30 | banana-slides |
| Target por slide, região ou elemento | Editor | 1 | 76 | 86 | 60 | 80 | 48 | 50 | 100 | 28 | 25 | banana-slides |
| Identidade estável de objetos | Editor | 1 | 78 | 86 | 60 | 80 | 48 | 50 | 96 | 28 | 25 | banana-slides |
| Regenera só a área necessária | Editor | 1 | 72 | 85 | 60 | 78 | 48 | 50 | 100 | 28 | 25 | banana-slides |
| Canvas/editor web para slides | Editor | 1.3333 | 48 | 52 | 88 | 99 | 38 | 50 | 97 | 20 | 30 | presentation-ai |
| Blocos ricos: texto, mídia, charts, componentes | Editor | 1.3333 | 52 | 52 | 88 | 99 | 38 | 50 | 96 | 20 | 30 | presentation-ai |
| Estado, undo/redo e persistência | Editor | 1.3333 | 49 | 52 | 89 | 98 | 38 | 50 | 94 | 20 | 30 | presentation-ai |
| Comentários/revisão assíncrona | Editor | 0.6667 | 28 | 40 | 47 | 91 | 25 | 25 | 55 | 15 | 15 | presentation-ai |
| Colaboração multiusuário em tempo real | Editor | 0.6667 | 26 | 40 | 46 | 90 | 25 | 25 | 55 | 15 | 15 | presentation-ai |
| Workflow de aprovação/versões | Editor | 0.6667 | 32 | 40 | 46 | 89 | 25 | 25 | 55 | 15 | 15 | presentation-ai |
| Link público/privado para apresentar | Distribuição | 1 | 72 | 35 | 78 | 97 | 25 | 35 | 72 | 15 | 20 | presentation-ai |
| Export PDF/PPTX/imagens | Distribuição | 1 | 76 | 39 | 79 | 92 | 25 | 35 | 74 | 15 | 20 | presentation-ai |
| Permissões e controle de acesso | Distribuição | 1 | 78 | 35 | 77 | 95 | 25 | 35 | 70 | 15 | 20 | presentation-ai |
| Eventos de visualização por deck/slide | Distribuição | 0.6667 | 78 | 20 | 36 | 43 | 20 | 20 | 25 | 10 | 10 | slide creator skill |
| Insights de engajamento acionáveis | Distribuição | 0.6667 | 76 | 20 | 36 | 42 | 20 | 20 | 25 | 10 | 10 | slide creator skill |
| Sinal para follow-up comercial | Distribuição | 0.6667 | 78 | 20 | 35 | 41 | 20 | 20 | 25 | 10 | 10 | slide creator skill |
| Endpoint REST para gerar deck | Automação | 1.3333 | 96 | 50 | 100 | 72 | 50 | 81 | 68 | 35 | 80 | Presenton |
| Job assíncrono com status e artefatos | Automação | 1.3333 | 92 | 50 | 100 | 72 | 50 | 78 | 71 | 35 | 78 | Presenton |
| Contrato estável de input/output | Automação | 1.3333 | 96 | 50 | 100 | 72 | 50 | 78 | 68 | 35 | 79 | Presenton |
| MCP/tools para geração e edição | Automação | 1.3333 | 95 | 40 | 100 | 55 | 75 | 70 | 45 | 26 | 60 | Presenton |
| Orquestra etapas por agente/workflow | Automação | 1.3333 | 92 | 40 | 95 | 55 | 80 | 73 | 45 | 25 | 60 | Presenton |
| Limites de ferramenta e segurança operacional | Automação | 1.3333 | 95 | 42 | 97 | 55 | 75 | 70 | 45 | 25 | 60 | Presenton |
| Batch/headless para múltiplos decks | Automação | 1 | 94 | 72 | 88 | 55 | 78 | 70 | 49 | 60 | 97 | slide-deck-ai |
| CLI clara para gerar/exportar/revisar | Automação | 1 | 97 | 75 | 85 | 55 | 78 | 70 | 49 | 64 | 92 | slide creator skill |
| Cabe em CI ou pipeline automatizado | Automação | 1 | 96 | 72 | 88 | 55 | 78 | 70 | 44 | 60 | 95 | slide creator skill |
| Troca de provedores LLM | IA | 0.6667 | 89 | 80 | 99 | 87 | 55 | 78 | 72 | 55 | 96 | Presenton |
| Troca de provedores de imagem/stock | IA | 0.6667 | 88 | 80 | 100 | 85 | 55 | 78 | 75 | 55 | 92 | Presenton |
| Política de custo, privacidade e fallback | IA | 0.6667 | 91 | 80 | 98 | 87 | 55 | 78 | 72 | 55 | 92 | Presenton |
| BYOK explícito | IA | 1.3333 | 96 | 90 | 100 | 89 | 70 | 78 | 75 | 90 | 95 | Presenton |
| Ollama/LM Studio/modelos locais | IA | 1.3333 | 95 | 90 | 100 | 89 | 70 | 78 | 75 | 90 | 96 | Presenton |
| Modo privacidade sem SaaS obrigatório | IA | 1.3333 | 96 | 90 | 100 | 85 | 70 | 78 | 70 | 90 | 96 | Presenton |
| Docker Compose/local deploy | Infra | 1 | 53 | 65 | 100 | 75 | 70 | 71 | 70 | 45 | 82 | Presenton |
| Topologia serviços app/API/storage | Infra | 1 | 82 | 65 | 100 | 75 | 70 | 72 | 70 | 45 | 80 | Presenton |
| Operação: env, storage, logs, upgrade | Infra | 1 | 56 | 65 | 99 | 76 | 70 | 70 | 70 | 45 | 80 | Presenton |
| App desktop empacotado | Infra | 0.6667 | 16 | 35 | 96 | 15 | 20 | 15 | 15 | 10 | 15 | Presenton |
| Uso local/offline prático | Infra | 0.6667 | 20 | 35 | 95 | 15 | 20 | 15 | 11 | 13 | 18 | Presenton |
| Instalador e atualização | Infra | 0.6667 | 17 | 35 | 94 | 15 | 20 | 15 | 15 | 10 | 15 | Presenton |
| QA de narrativa, tese e CTA | Qualidade | 1.3333 | 100 | 78 | 50 | 50 | 95 | 88 | 45 | 92 | 45 | slide creator skill |
| QA visual/rendered key slides | Qualidade | 1.3333 | 100 | 81 | 50 | 50 | 92 | 88 | 45 | 94 | 45 | slide creator skill |
| Itens bloqueantes de release | Qualidade | 1.3333 | 100 | 80 | 50 | 50 | 92 | 88 | 45 | 93 | 45 | slide creator skill |
| Inspeciona objetos editáveis no PPTX | Qualidade | 1.3333 | 98 | 100 | 65 | 55 | 72 | 55 | 45 | 93 | 45 | ppt-master |
| Verifica placeholders/resíduos técnicos | Qualidade | 1.3333 | 92 | 98 | 65 | 55 | 72 | 55 | 45 | 93 | 45 | ppt-master |
| Roundtrip PowerPoint/LibreOffice/PDF | Qualidade | 1.3333 | 93 | 99 | 65 | 55 | 72 | 55 | 45 | 92 | 45 | ppt-master |
| Testes unitários/integração | Qualidade | 0.3333 | 97 | 70 | 58 | 45 | 60 | 55 | 44 | 65 | 55 | slide creator skill |
| Fixtures/golden decks | Qualidade | 0.3333 | 99 | 73 | 55 | 45 | 60 | 50 | 45 | 67 | 55 | slide creator skill |
| Quality gate executável em CI | Qualidade | 0.3333 | 99 | 71 | 57 | 45 | 60 | 50 | 45 | 65 | 55 | slide creator skill |
| Docs operacionais para usuário/agente | Maturidade | 0.3333 | 100 | 74 | 89 | 72 | 75 | 62 | 58 | 82 | 65 | slide creator skill |
| Docs de arquitetura/extensão | Maturidade | 0.3333 | 100 | 73 | 89 | 72 | 75 | 62 | 58 | 78 | 65 | slide creator skill |
| Exemplos e templates documentados | Maturidade | 0.3333 | 100 | 74 | 86 | 72 | 75 | 62 | 58 | 82 | 67 | slide creator skill |
| Licença clara no repositório | Risco | 1 | 100 | 95 | 98 | 95 | 95 | 0 | 0 | 95 | 95 | slide creator skill |
| Segurança para copiar/adaptar código | Risco | 1 | 100 | 95 | 96 | 95 | 95 | 0 | 0 | 95 | 95 | slide creator skill |
| Segurança para absorver padrão/comportamento | Risco | 1 | 100 | 95 | 98 | 95 | 95 | 40 | 45 | 95 | 95 | slide creator skill |
| Tamanho/atividade/sinais de manutenção | Maturidade | 1 | 87 | 92 | 96 | 78 | 72 | 58 | 65 | 62 | 60 | Presenton |
| Coesão arquitetural | Maturidade | 1 | 89 | 91 | 96 | 76 | 72 | 58 | 63 | 62 | 60 | Presenton |
| Custo de absorção para SINKRA | Maturidade | 0.9995 | 91 | 90 | 92 | 76 | 72 | 56 | 62 | 65 | 60 | Presenton |

