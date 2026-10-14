# Metodologia de Pesos por Persona

Data: 2026-05-18

Esta camada existe para responder se as personas usam as características certas. Cada persona declara o trabalho real, must-haves, anti-goals e microdimensões decisivas antes do cálculo.

## Contrato

- Escala: 0-100 por player.
- Pesos: cada persona soma 100.
- Base: toda microdimensão herda uma fração do peso neutro para não apagar capacidades secundárias.
- Foco: must-haves recebem peso adicional.
- Anti-goals: explicam baixo peso ou uso como benchmark comportamental, sem inventar penalidade fora da matriz.
- Base de cálculo: 108 microdimensões derivadas das 36 dimensões macro.

## Personas Auditáveis

### Founder/consultoria B2B

- **Job:** Transformar briefing estratégico em apresentação comercial consultiva, editável em PowerPoint e defensável em reunião.
- **Must-have:** Narrativa consultiva; PPTX editável; QA de editabilidade; Fontes rastreáveis; Entrega rápida.
- **Anti-goals:** Editor bonito sem saída PPTX robusta; Deck sem prova/fonte; Vídeo ou web-only como entrega principal.
- **Top microdimensões:** Define mudança de crença da audiência (5.35); Usa lógica SCQA/Pyramid/action-title (5.35); Conecta história ao CTA ou decisão final (5.35); Gera shapes/textos nativos DrawingML (4.43); Evita transformar tudo em imagem (4.43); Reabre no PowerPoint sem quebrar layout (4.43); Inspeciona objetos editáveis no PPTX (3.76); Verifica placeholders/resíduos técnicos (3.76); Roundtrip PowerPoint/LibreOffice/PDF (3.76); QA de narrativa, tese e CTA (3.23); QA visual/rendered key slides (3.23); Itens bloqueantes de release (3.23).
- **Vencedor calculado:** slide creator skill contra ppt-master, gap 3.09.

### Produto self-hosted/API

- **Job:** Disponibilizar geração de apresentações como produto interno/API governada e executável localmente.
- **Must-have:** API de geração; MCP/tools; Docker/self-hosting; BYOK/Ollama; Provider registry; Workspace por execução.
- **Anti-goals:** Fluxo apenas UI; Dependência de SaaS fechado; Sem isolamento de dados por run.
- **Top microdimensões:** Endpoint REST para gerar deck (5.54); Job assíncrono com status e artefatos (5.54); Contrato estável de input/output (5.54); MCP/tools para geração e edição (5.02); Orquestra etapas por agente/workflow (5.02); Limites de ferramenta e segurança operacional (5.02); Docker Compose/local deploy (3.4); Topologia serviços app/API/storage (3.4); Operação: env, storage, logs, upgrade (3.4); BYOK explícito (3.03); Ollama/LM Studio/modelos locais (3.03); Modo privacidade sem SaaS obrigatório (3.03).
- **Vencedor calculado:** Presenton contra slide creator skill, gap 17.

### Engenheiro de renderer PPTX

- **Job:** Converter IR/DeckSpec em PPTX nativo, editável e verificável sem rasterizar o deck inteiro.
- **Must-have:** PPTX nativo; Charts/tabelas nativos; OOXML; QA de editabilidade; Template import.
- **Anti-goals:** HTML screenshot como slide; PDF como saída principal; Sem relatório por objeto.
- **Top microdimensões:** Gera shapes/textos nativos DrawingML (7.77); Evita transformar tudo em imagem (7.77); Reabre no PowerPoint sem quebrar layout (7.77); Charts nativos e editáveis (3.7); Reconstrói tabelas com hierarquia e destaques (3.7); Contrato de dados para charts/tabelas (3.7); Inspeciona objetos editáveis no PPTX (3.08); Verifica placeholders/resíduos técnicos (3.08); Roundtrip PowerPoint/LibreOffice/PDF (3.08); LaTeX/OMML para matemática editável ou nítida (2.44); Mermaid/Graphviz/TikZ/diagram engines (2.44); QA técnico de overflow, tema e legibilidade (2.44).
- **Vencedor calculado:** ppt-master contra powerpoint-skill, gap 13.86.

### Autor técnico/acadêmico

- **Job:** Gerar aulas, relatórios técnicos e apresentações acadêmicas com notação e diagramas corretos.
- **Must-have:** Math/OMML; Diagramas; Tabelas; QA técnico; Fixtures determinísticas.
- **Anti-goals:** Visual premium sem rigor técnico; Fórmula rasterizada sem editabilidade; Sem validação de layout.
- **Top microdimensões:** LaTeX/OMML para matemática editável ou nítida (12.01); Mermaid/Graphviz/TikZ/diagram engines (12.01); QA técnico de overflow, tema e legibilidade (12.01); QA de narrativa, tese e CTA (5.17); QA visual/rendered key slides (5.17); Itens bloqueantes de release (5.17); Testes unitários/integração (2.23); Fixtures/golden decks (2.23); Quality gate executável em CI (2.23); Docs operacionais para usuário/agente (1.69); Docs de arquitetura/extensão (1.69); Exemplos e templates documentados (1.69).
- **Vencedor calculado:** slide creator skill contra powerpoint-skill, gap 3.69.

### Designer/brand editor

- **Job:** Criar e ajustar decks com identidade visual, preview rápido, tema reaplicável e colaboração com stakeholders.
- **Must-have:** Editor web; Temas/tokens; Template import; Preview vivo; Sharing; Colaboração.
- **Anti-goals:** CLI-only; Sem runtime visual; Sem aplicação consistente de marca.
- **Top microdimensões:** Canvas/editor web para slides (5.11); Blocos ricos: texto, mídia, charts, componentes (5.11); Estado, undo/redo e persistência (5.11); Tokens de cor, fonte, espaçamento e grid (3.31); Runtime aplica tema consistentemente (3.31); Guardrails de marca e anti-padrões (3.31); Manifesta templates importados (2.8); Replica linguagem visual de template/brand deck (2.8); Seleciona template por função do slide (2.8); Variedade de layout sem virar colagem (2.3); Controle de densidade e legibilidade (2.3); Qualidade visual observada no render final (2.3).
- **Vencedor calculado:** presentation-ai contra Presenton, gap 5.97.

### Operador prompt-to-edit

- **Job:** Iterar em cima de um deck existente com comandos naturais e diffs por elemento ou região.
- **Must-have:** Prompt-to-edit; Edição regional; Preview; Diff de alteração; Undo/reroute.
- **Anti-goals:** Regenerar deck inteiro para cada ajuste; Edição textual sem contexto visual; Cópia de código AGPL sem decisão jurídica.
- **Top microdimensões:** Edição por linguagem natural (7.12); Diff antes de aplicar edição (7.12); Histórico reversível de edição (7.12); Target por slide, região ou elemento (4.71); Identidade estável de objetos (4.71); Regenera só a área necessária (4.71); Canvas/editor web para slides (3.84); Blocos ricos: texto, mídia, charts, componentes (3.84); Estado, undo/redo e persistência (3.84); Preview vivo local/web (2.69); Anotações visuais viram correções (2.69); Revisão por screenshot/thumbnail (2.69).
- **Vencedor calculado:** presentation-ai contra banana-slides, gap 0.03.

### Enterprise/compliance

- **Job:** Rodar geração de slides com dados sensíveis, auditoria, licença segura e opção sem envio para SaaS externo.
- **Must-have:** Licença segura; BYOK/local; Self-hosting; Grounding; QA; Logs auditáveis.
- **Anti-goals:** Licença copyleft sem ADR; SaaS-only; Sem trilha de fontes ou decisões.
- **Top microdimensões:** Licença clara no repositório (5.91); Segurança para copiar/adaptar código (5.91); Segurança para absorver padrão/comportamento (5.91); BYOK explícito (3.56); Ollama/LM Studio/modelos locais (3.56); Modo privacidade sem SaaS obrigatório (3.56); Docker Compose/local deploy (2.67); Topologia serviços app/API/storage (2.67); Operação: env, storage, logs, upgrade (2.67); Roteia fonte por tipo: web, scholar, local, vídeo ou benchmark (2.17); Liga claim a evidência e confiança (2.17); Verifica frescor e risco factual (2.17).
- **Vencedor calculado:** Presenton contra slide creator skill, gap 0.88.

### Research multimodal/vídeo

- **Job:** Transformar fontes multimodais em deck narrado com pesquisa, evidências, export vídeo e Q&A sobre o conteúdo.
- **Must-have:** URL/YouTube; Grounding; Narração; Vídeo; Q&A; Planejamento.
- **Anti-goals:** Deck sem fontes; Vídeo sem PPTX; Pipeline multimodal sem governança.
- **Top microdimensões:** Roteia fonte por tipo: web, scholar, local, vídeo ou benchmark (4.59); Liga claim a evidência e confiança (4.59); Verifica frescor e risco factual (4.59); Exporta deck para vídeo/MP4 (3.93); Q&A ou navegação sobre vídeo (3.93); Pipeline de assets multimídia (3.93); Speaker notes estruturadas (3.41); TTS/narração automática (3.41); Sincroniza áudio com slide/trecho (3.41); Ingestão de URL/site/documento remoto (2.89); YouTube/vídeo como fonte de narrativa (2.89); Mapeia mídia para momentos/trechos do deck (2.89).
- **Vencedor calculado:** PresentAgent-2 contra ppt-master, gap 2.11.

### Arquiteto slide creator skill stack

- **Job:** Projetar a stack final combinando narrativa, renderer, runtime, agentes, QA, licenças e roadmap de absorção.
- **Must-have:** Composição modular; PPTX nativo; API/MCP; QA; Licença; Local/BYOK.
- **Anti-goals:** Fork único; Ranking absoluto injusto; Absorção de código com risco jurídico.
- **Top microdimensões:** Gera shapes/textos nativos DrawingML (3.94); Evita transformar tudo em imagem (3.94); Reabre no PowerPoint sem quebrar layout (3.94); Endpoint REST para gerar deck (3.06); Job assíncrono com status e artefatos (3.06); Contrato estável de input/output (3.06); MCP/tools para geração e edição (3.06); Orquestra etapas por agente/workflow (3.06); Limites de ferramenta e segurança operacional (3.06); Define mudança de crença da audiência (2.81); Usa lógica SCQA/Pyramid/action-title (2.81); Conecta história ao CTA ou decisão final (2.81).
- **Vencedor calculado:** Presenton contra slide creator skill, gap 3.79.

### Agência/marketing em escala

- **Job:** Produzir muitas variações de decks para campanhas, propostas e relatórios com marca consistente e ciclos rápidos de revisão.
- **Must-have:** Temas; Prompt-to-edit; Visual/layout; Share; Vídeo; Colaboração; Templates.
- **Anti-goals:** Saída apenas técnica; Sem editor para revisão de marca; Sem publicação/compartilhamento.
- **Top microdimensões:** Edição por linguagem natural (3.31); Diff antes de aplicar edição (3.31); Histórico reversível de edição (3.31); Canvas/editor web para slides (3.06); Blocos ricos: texto, mídia, charts, componentes (3.06); Estado, undo/redo e persistência (3.06); Tokens de cor, fonte, espaçamento e grid (3.03); Runtime aplica tema consistentemente (3.03); Guardrails de marca e anti-padrões (3.03); Variedade de layout sem virar colagem (2.78); Controle de densidade e legibilidade (2.78); Qualidade visual observada no render final (2.78).
- **Vencedor calculado:** presentation-ai contra Presenton, gap 4.81.

### DevOps/batch automation

- **Job:** Rodar geração e validação de decks em pipelines automatizados, sem depender de cliques em UI.
- **Must-have:** CLI/headless; API; MCP; Docker; Fixtures/CI; Logs; Provider registry.
- **Anti-goals:** UI-only; Sem fixture; Sem API estável; Sem isolamento de workspace.
- **Top microdimensões:** Batch/headless para múltiplos decks (4.17); CLI clara para gerar/exportar/revisar (4.17); Cabe em CI ou pipeline automatizado (4.17); Endpoint REST para gerar deck (3.8); Job assíncrono com status e artefatos (3.8); Contrato estável de input/output (3.8); MCP/tools para geração e edição (3.8); Orquestra etapas por agente/workflow (3.8); Limites de ferramenta e segurança operacional (3.8); Docker Compose/local deploy (2.5); Topologia serviços app/API/storage (2.5); Operação: env, storage, logs, upgrade (2.5).
- **Vencedor calculado:** Presenton contra slide creator skill, gap 7.68.

### Revenue enablement/analytics

- **Job:** Criar decks comerciais por segmento e medir leitura, engajamento e evolução das versões.
- **Must-have:** Narrativa; Share/publicação; Analytics; Branding; Prompt completo; Colaboração; PPTX editável.
- **Anti-goals:** Deck sem métrica de consumo; Sem versão por ICP; Sem edição comercial rápida.
- **Top microdimensões:** Link público/privado para apresentar (3.6); Export PDF/PPTX/imagens (3.6); Permissões e controle de acesso (3.6); Define mudança de crença da audiência (3.48); Usa lógica SCQA/Pyramid/action-title (3.48); Conecta história ao CTA ou decisão final (3.48); Eventos de visualização por deck/slide (2.97); Insights de engajamento acionáveis (2.97); Sinal para follow-up comercial (2.97); Canvas/editor web para slides (2.25); Blocos ricos: texto, mídia, charts, componentes (2.25); Estado, undo/redo e persistência (2.25).
- **Vencedor calculado:** presentation-ai contra Presenton, gap 0.57.

## Implicação

Com essa leitura, o bench deixa de perguntar “qual projeto é melhor?” e passa a perguntar “qual projeto é melhor para este trabalho específico e em qual microcapacidade?”.
