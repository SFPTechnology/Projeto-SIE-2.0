# F10 — Plano de implementação executável

**Branch de trabalho:** feat/f09-concessionarias-especializadas  
**Limites:** preservar main; sem merge, deploy, migração de produção ou homologação normativa. As extensões F09 já excluídas permanecem fora do escopo.

## Estado inicial confirmado

- O handoff F09 registra a integração essencial como concluída e libera desenvolvimento F10.
- O código F10 existente é uma camada inicial em restructuring/apps/api/sie_api/representation_f10.py, ainda sem editor/importador de planta, armazenamento imutável, PDF ou integração de interface.
- A última suíte API observada no SHA 4f1e27971339c4cae702a3f8353be5162675f70b teve 1.039 aprovações e uma falha em test_svg_escapes_untrusted_labels. A falha está no cenário que muda o ID do quadro sem atualizar as referências dos circuitos; a validação do grafo interrompe corretamente.
- O AIOX passou nesse SHA. A execução de navegador registrada ainda não havia concluído na consulta inicial. O SHA atual da branch é a588224d30877d63d25349160e2168546bce5f5b; a API de checks não apresentou execuções associadas a esse SHA na inspeção.

## Sequência de trabalho

1. **Consertar e confirmar a base de testes**
   - Ajustar o teste de escape SVG para usar rótulo hostil em circuito mantendo ID do quadro e referências válidas.
   - Rodar o teste focal, a suíte API e os três workflows remotos no SHA resultante.
   - Não alterar expectativas funcionais para obter resultado verde.

2. **Consolidar o contrato de artefato**
   - Ampliar o contrato para project_id, revision_id, calculation_run_id, versão da regra e template em todos os artefatos.
   - Garantir que snapshot inválido, referência inexistente, valor não finito ou revisão divergente bloqueiem geração/exportação.
   - Preservar estados de estudo/pendência; nunca inferir aprovação normativa.

3. **Representação gráfica derivada do modelo**
   - Usar IDs do domínio e topologia existente para desenhar unifilar por quadro e legenda rastreável.
   - Implementar geometria de planta somente sobre estruturas/unidades existentes; não inventar escala ou comprimentos. Se o repositório não oferecer contrato geométrico, registrar a dependência e restringir a entrega ao unifilar.

4. **Quadro, quantitativos e relatório**
   - Produzir quadro de circuitos com carga/fase/dispositivo/condutor da mesma revisão e execução.
   - Derivar quantitativos somente de itens e comprimentos efetivamente registrados; estimativas devem ser identificadas separadamente.
   - Gerar saída documental do escopo suportado com IDs, premissas, pendências, status, fontes e referências. PDF só após verificar dependências já suportadas; caso contrário, documentar formato não implementado.

5. **Exportação e validador cruzado**
   - Implementar formatos sustentados pelo projeto e testes de round-trip em seus campos/IDs.
   - Comparar revisão, cálculo, topologia, cargas, fases, proteção e condutor entre quadro/diagrama/relatório; divergência bloqueia pacote.

6. **Prévia, acessibilidade e QA**
   - Exercitar SVG/HTML em viewport pequeno e desktop, foco/semântica, escape de conteúdo e impressão, conforme UI disponível.
   - Produzir pareceres separados QA-01 (arquitetura/testes), QA-02 (escopo de engenharia; sem homologação humana) e QA-03 (integração/segurança/UX).
   - Corrigir achados impeditivos e repetir os testes afetados.

7. **Fechamento**
   - Atualizar relatório F10 e a fonte de estado canônica com SHAs, comandos, resultados e arquivos.
   - Marcar DONE somente se critérios essenciais e três revisões aplicáveis estiverem comprovados. Caso contrário, manter IMPLEMENTED/VALIDATING/BLOCKED com pendências concretas.

## Evidências mínimas de conclusão

- API e regressões relevantes passam no SHA final.
- Três workflows remotos de API, AIOX e Chromium concluídos com sucesso no mesmo SHA.
- Artefatos da mesma revisão têm identidade e dados coerentes; diferenças são bloqueadoras.
- Exportação suportada é reproduzível; QA visual/acessibilidade foi executado quando houver interface.
- QA-01/02/03 e relatório F10 citam provas reais; não há declaração de conformidade profissional/normativa sem parecer e fonte apropriados.

## Plano integral adaptativo — 24/10/2026 (supera sequência parcial histórica)

Baseline: W1 concluída em `7d8edda79019fed91396d53e99bd897191d69ba3`. Arquivo untracked preexistente fora F10 será preservado. O contrato/story foi ampliado antes do código. Modo B+C autorizado pelo responsável: implementação local, publicação na branch e CI por DevOps; sem main/merge/deploy/produção.

| task_id | owner | objective / acceptance_criteria | dependencies | write_scope | required_tests / evidence_required | status |
|---|---|---|---|---|---|---|
| F10-ARCH | architect | Inventário AC10.01–10, contrato e DAG sem perder W1 | baseline | plano/story F10 | inspeção símbolos/caminhos e matriz | DONE estática |
| F10-B | graphics | Importar base JSON autorizada por referência, validar escala/calibração/unidade/IDs e renderizar planta; catálogo/legenda versionados | F10-ARCH | floorplan_f10.py, symbols_f10.py, testes novos | CLI import/render, escala inválida, geometria cruzada, escape e legendas | READY |
| F10-C | documents | Quadro e equipamentos/percursos rastreáveis; memorial de resultados reais; reconciliação e PDF válido | F10-ARCH | documents_f10.py, test_documents_f10.py, pyproject | motor real, não inventar fórmula/quantidade, PDF extração/render, adulteração | READY |
| F10-I | integration | Owner único dos módulos oficiais: adicionar diagramas derivados do grafo, snapshot de cálculo, planta/documentos/PDF ao manifesto e serviço CLI; compatibilidade W1 | F10-B,F10-C para hooks finais | representation/store/persisted_source + testes existentes | bundles reais, round-trip JSON/CSV, hashes/PDF, mismatch bloqueado, recovery regressão | READY preparação |
| F10-D | UX/API | Preview oficial autenticado, zoom/navegação/print/download com desktop/mobile e sem fonte remota ativa | F10-I CLI antes ativação UI | artifacts_api_f10.py, main.py, artefatos.html/js, navegação/E2E | token ausente/inválido, traversal, mídia segura, teclado, viewport e browser real | READY preparação |
| F10-QA1 | QA arquitetura | Revisar contratos/código/testes e integridade da integração real | F10-I,F10-D | QA-01.md | testes reais, negativos, regressão; parecer independente | TODO |
| F10-QA2 | QA domínio | Revisar origem das grandezas, geometria/escala, diagrama/quantidades/memorial e limites normativos | F10-I,F10-D | QA-02.md | comparar modelo/execução/exportações; sem assinatura profissional | TODO |
| F10-QA3 | QA segurança/UX | Revisar autorização, arquivos/HTML/SVG/PDF e interação/acessibilidade | F10-I,F10-D | QA-03.md | negativos auth/traversal/XSS e E2E específico F10 | TODO |
| F10-CI | DevOps | Congelar candidato, publicar sem force, três workflows verdes no SHA final | QA1/2/3 e correções | workflows/evidências se necessário | pytest completo/npm4gates/Chromium no SHA candidato | TODO |
| F10-CLOSE | orchestrator | Atualizar matriz/registros/relatório; DONE só com todos critérios aplicáveis provados | F10-CI | docs F10/story/estado canônico | requisito→arquivo→teste→run→SHA e decisão | TODO |

### Contrato gráfico e documental

1. `floorplan_f10.import_floor_plan(raw, snapshot, contract)` valida base JSON, autorização declarada com referência, hash canônico, escala/calibração positiva, unidades m/cm/mm, dimensões, walls/paths/placements e IDs/revisão; rejeita conteúdo ativo/links externos e não presume licença externamente comprovada. Medidas de paths vinculados a trecho devem reconciliar com comprimento salvo em metros usando tolerância explícita; desenho não altera comprimento de ledger silenciosamente.
2. `symbols_f10` fornece catálogo SIE esquemático versionado de símbolos internos, origem e legenda apenas dos usados. Não atribuir convenção normativa sem fonte verificada.
3. Snapshot W1 poderá incluir `verified_calculation_f10` (registro real, entradas persistidas e vínculo hashes), dados explícitos de equipamentos/condutores e base de planta persistida. Integração valida origem e congelamento; record.result_sha256 deve coincidir com run.output_sha256.
4. `documents_f10` consome snapshot/contrato; produz quadro, quantitativo, memorial e PDF. Fórmulas/intermediários só aparecem se rastreáveis ao motor; resultado PENDENTE/BLOQUEADO não vira aprovação.
5. Exportação adicional participa do mesmo manifesto/hash/recovery; PDF real testado, sem substituir por HTML renomeado. Não prometer CAD/BIM sem requisito e contrato de interoperabilidade aprovados.
6. UI é observadora do caminho oficial CLI/serviço; nenhum desenho cliente é origem autoritativa de cálculo. Preview/prints e downloads exigem autenticação local e artefato/projeto/revisão compatíveis; token global não é ACL multiusuário.

Paralelismo: B e C independentes em módulos novos; I é owner único dos três módulos oficiais; UX prepara leitura enquanto CLI não está pronto. Nenhum agente modifica arquivo de outro sem serialização. Cada achado QA volta ao owner, com reteste e invalidação da evidência afetada. Evidências locais não substituem CI; três workflows devem corresponder ao SHA final. Status operacional permitido TODO/READY/IN_PROGRESS/READY_FOR_REVIEW/DONE/BLOCKED, com blocking_reason e output_reference registrados no relatório ao surgir resultado ou bloqueio.

### Contrato complementar da especificação integral (prevalece sobre importação JSON isolada)

Fonte principal adicional: `ESPECIFICACAO_ENGENHARIA_CAMADA_GRAFICA_F10.md`, conteúdo consultado pelo orquestrador. F10-B deve importar arquivo real PNG/JPEG ou SVG seguro, guardar original, MIME/tamanho/hash e referência declarada de autorização. Uma implementação do formato SVG seguro satisfaz a alternativa de formato; não anunciar PNG/JPEG sem implementá-los/testá-los. Asset SVG usa subset estrito sem DTD/entidades/scripts/handlers/style ativo/URLs externas; original preservado para auditoria não pode ser servido como conteúdo ativo sem sanitização. Planta guarda `asset`, calibração com `confirmed_by` e `confirmed_at`, geometria revisionada; JSON é somente metadado geométrico, não substitui asset.

F10-D deve oferecer pan/zoom, seleção apenas de elementos do modelo, camadas, undo/redo local, salvar explicitamente e avisar alterações não salvas. Salvamento deve usar versão esperada e conflito otimista, persistindo revisão nova e sem sobrescrever histórico. Editor não deve alterar cálculos/comprimentos silenciosamente. API aplica autenticação local em import/calibrate/geometry/generate/query/history/download e não recebe caminho filesystem arbitrário.

Para compatibilidade W1, o modo integral é explícito (`full_f10=True` / CLI `--full`); exige base persistida válida e `verified_calculation_f10`, e acrescenta documentos/PDF/UI sem alterar o contrato do pacote W1 legado. Falta de dados para multifilar/prumada gera estado indisponível e motivo rastreável, sem criar ligações. CAD/BIM são opcionais. Símbolos mantêm versão, origem e licença explícitas.

### Contrato full multicircuito — correção obrigatória QA-02

- `dados.calculation_runs_f10: {circuit_uuid: run_uuid}` é obrigatório em modo full; cobertura exata de circuitos do agregado, sem run reaproveitado para circuitos diferentes. Todos os runs devem pertencer à mesma revisão autoritativa e possuir evidência real verificável. `calculation_run_id` escalar do contrato/CLI é âncora de compatibilidade, incluída no mapa, não atestação global.
- Snapshot declara `calculation_scope_f10: PER_CIRCUIT_RUN_MAP_V1`; `calculation_dependencies_f10` contém circuito/run e hashes de entrada, resultado, execução, snapshot e versões de regra/algoritmo individuais. `verified_calculations_f10` contém `{circuit_id, run_id, record, parameters, execution_sha256}` por circuito. Quadros/diagramas/memorial/PDF devem cobrir o mesmo conjunto e não repetir resultado de uma execução única para circuitos distintos.
- Memorial reconcilia cada record com sua dependência e linha do circuito. Regra/algoritmo escalares da âncora não substituem versões individuais quando houver diferenças. Regeração/verificação consulta todas as evidências. Falta/alteração de qualquer dependência torna o pacote stale/invalid conforme contrato existente.
- Quadros são derivados de `board_id`; unifilar multicircuito/multiquadro mostra somente arestas efetivas. Alimentadores podem usar o motor real somente quando seu contrato explícito for compatível e testado. Carga de alimentador, quando exibida, é soma exata das cargas aparentes descendentes declaradas do grafo, identificada como `SUM_DECLARED_DOWNSTREAM_NOT_DEMAND`; não é demanda calculada nem conversão de corrente para potência. Fonte incapaz de comprovar um circuito bloqueia geração integral, com razão explícita.
- `phases_count` é contagem. Identificação de condutores de fase deve vir de `dados.phase_assignments_f10`, nunca do número de fases. Sem identificação explícita, a saída é `UNSPECIFIED`; multifilar indisponível com motivo. Valores explícitos devem ser validados contra conexão FN/FF/trifásica; N/PE não são presumidos de uma contagem.
- CLI/API executam cada run mapeado; modo full só publica após cobertura completa. W1 legado continua byte-compatible e intencionalmente escalar.
