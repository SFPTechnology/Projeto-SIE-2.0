# SIE 2.0 — F01 | Plano automático de desbloqueio YOLO v2.0
**Data:** 15/10/2026 · **Executor-alvo:** `scripts/f01_yolo_runner.py` + `scripts/f01_cell_evidence_gate.py` · **Status inicial:** `F00=DONE`, `F01=BLOCKED`, `F02=NOT_RELEASED`.

## 1. Contrato de execução
**Objetivo:** eliminar as lacunas técnicas verificáveis da F01 por desenvolvimento autônomo sem confirmações rotineiras, promover comprovação rastreável de **G01–G06** e **AC-01.01–AC-01.10**, preservar F00 como referência imutável de regressão e **não começar F02**.

**YOLO controlado** permite: consultar fontes públicas e arquivos autorizados, elaborar matrizes, criar testes e código, corrigir regressões, executar três contextos Copilot CLI isolados, registrar commits nas branches `qa/f01-*` e `feat/f01-governanca-normativa` e documentar impasses. **Não** permite presumir licença ou origem primária, marcar valores ABNT/EDP como verificados sem a dupla leitura independente, inventar assinaturas profissionais, modificar `main`, migrar Supabase/produção, liberar F02 ou eliminar testes/golden de F00.

**Condição inicial única de infraestrutura:** VM/container descartável **realmente isolado** com Git, Python, Node, dependências de testes e Copilot CLI instalado e autenticado previamente; token de privilégio mínimo, sem secrets de produção. `--sandbox-confirmed` apenas declara a preparação, **não cria isolamento**. O CLI YOLO pode executar comandos arbitrários: jamais confiar apenas no prompt para segurança. Se não houver CLI, execução autônoma independente = `BLOCKED_ENVIRONMENT`, mas tarefas que não exigem CLI podem continuar por meios compatíveis.

**Sem prometer sucesso artificial:** os seis gates dependem de documentos originais, uso permitido, valores legíveis, cálculos independentes e verificações externas genuínas. A ausência de dados resulta em `BLOCKED_EVIDENCE` com diagnóstico específico. A automação pode completar implementação técnica sem atingir `DONE`.

## 2. Linha de base factual

| Item | Situação confirmada na retomada |
|---|---|
| `main` | SHA `2eee08d126d7bab0a0fe7b7d96b25004ac545447`; não alterar |
| F00 | `DONE`; executar somente `scripts/f00_golden.py --verify` |
| F01 | Branch `feat/f01-governanca-normativa`; PR #3 draft; último código inclui histórico completo **de novas revisões locais** e trilhas de algoritmos, **não** de células normativas verificadas |
| QA-01/02/03 | Perfis e seis skills prontos; branches `qa/f01-arquiteto`, `qa/f01-engenheiro-eletrico`, `qa/f01-dados-ux-llm` ainda apontam para SHA antigo `8aec14ac...`; **sem primeira execução independente comprovada** |
| G01–G06 | **0/6 aceitos** no `QA3_MANIFEST.json` |
| AC-01.* | Critérios controlados em `ORCHESTRATOR_STATE.json`, F01 ainda `BLOCKED` |
| Fontes | ABNT 5410, EDP PT.DT.PDN.00068 v09, NR-10 (e NBR 5419 quando aplicável) identificadas parcialmente; **0 células Iz/Rca/XL/EDP homologadas** |

Fontes públicas de metadados consultáveis: [EDP — Normas e padrões](https://www.edp.com.br/normas-e-padroes-tecnicos/) (identifica PT.DT.PDN.00068 v09 como publicada em 15/04/2026), [MTE — NR-10](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10) (Portaria 737/2026, vigência geral 01/06/2027 e regime de instalações existentes a conferir) e [ABNT Catálogo](https://www.abntcatalogo.com.br/default.aspx?O=1). **Página editorial é evidência de metadado, não de célula normativa.**

## 3. Pipeline autônomo, repetível e auditável

### BL-00 — Preflight/segurança e F00 congelada
- Verificar estado Git limpo, `main` e F00 sem alterações, PR #3 draft, catálogo, checksums e o estado canônico F01.
- Fazer snapshot da própria **branch de origem** `feat/f01-governanca-normativa` como `base_sha` do ciclo, registrá-lo fora dos dados normativos.
- Executar `python scripts/f01_release_gate.py --verify-invariants` e `python scripts/f01_cell_evidence_gate.py`. Sucesso do **modo status** significa apenas que o bloqueio está íntegro.
- Checar acessos externos e licenças sem publicar conteúdo normativo protegido.

### BL-01 — Inventário de células e fontes primárias
- Ler módulos efetivos `engines.py`, `edp.py`, catálogos, chamadas de cálculo e relatórios. Produzir lista exaustiva de **células realmente necessárias para o escopo ativo**, sem reduzir escopo só para atingir 100%.
- Abrir os campos de `MATRIZ_CELULAS_NORMATIVAS_F01.json`: Rca, XL, Iz, fatores e EDP; relacionar cada item a fonte, edição, página, tabela, linha, coluna, unidade, notas, temperaturas/métodos, limites de aplicação e flags de licença. **Rdc20 não substitui Rca nem XL.**
- Reconciliar cópias do projeto com **fonte primária autorizada**: hash do documento, publicação, erratas, vigência, distribuição/território e data de referência. Cópias derivadas, chunks e hashes locais não são prova de autenticidade.
- Se original não acessível: manter `BLOCKED_SOURCE` e avançar tarefas não dependentes; registrar URL/localização/versão faltantes. Não colar tabelas ABNT protegidas em repositório aberto.

### BL-02 — Dupla conferência independente e reconciliação
- **Leitor A** e **Leitor B** inspecionam individualmente o mesmo documento original/edição autorizada, com artefatos e identidades de origem independentes e sem compartilhar resultado até congelar o primeiro registro. Agentes de IA distintos podem conferir extração e discordâncias, mas **não substituem automaticamente atestação técnica profissional**.
- Comparar valor, escala, unidade, precisão, método, temperatura, condição de instalação, página, linha/coluna, observações e critérios de seleção. Registrar divergência e resolvê-la contra o original; nada de votação.
- Atualizar o status por item: `BLOCKED_SOURCE` → `READY_FOR_INDEPENDENT_REVIEW` → `EVIDENCE_RECONCILED`; **não usar VERIFICADO/HOMOLOGADO** sem evidência externa requerida. O validador estrutural analisa consistência, não certifica fisicamente o original.

### BL-03 — Fixtures e cálculos independentes
- Para cada família normativa efetivamente utilizada: entradas completas, fórmula aplicável, unidade, referência de célula/nota, resultado esperado elaborado **fora do SIE**, tolerância, casos de contorno (12/25 kW quando aplicável, Ib/In/Iz, Rca/XL, concessionária, tensões, temperatura, data e transições).
- Separar estritamente `DEMO_SYNTHETIC` (já existe em `test_f01_independent_math_examples.py`) de `NORMATIVE_REVIEWED`. Golden F00 é apenas regressão, jamais expected normativo independente.
- Executar comparação determinística; falhas devem produzir mudanças de código em branches QA, não alterar valores esperados para coincidir com o software.

### BL-04 — Atualização segura de três branches QA
- **Problema de retomada:** as QA branches estão em SHA de origem antigo. O coordenador deve capturar o SHA F01 **no início da execução**; verificar que cada branch QA está limpa, sem commits não integrados, e que seu HEAD é ancestral da F01.
- Fazer `git merge --ff-only <base_sha>` **em cada worktree isolado antes do primeiro prompt**, e push normal (sem force). Se houver divergência, não apagar trabalho: `BLOCKED_BRANCH_DIVERGENCE`, aplicar cherry-pick/integração controlada **somente com prova e sem rebase destrutivo**.
- Todas as QA branches partem do **mesmo `base_sha` atual**, evitando reimplementar funções já concluídas e preservando a independência das **primeiras análises**.

### BL-05 — Três execuções QA realmente distintas
- Agentes: QA-01 (arquiteto), QA-02 (engenheiro eletricista NBR 5410/EDP), QA-03 (dados/UX/LLM). Utilizar `.github/agents/f01-qa-*.agent.md` e respectivas skills, em **três processos/contextos CLI separados**, nunca três personas no mesmo prompt.
- Cada agente deve executar **integralmente** BL-01/02/03 e implementação do software, 5 etapas corretivas anteriores e G01–G06, **sem ler os outros pareceres antes de congelar o seu próprio commit SHA**.
- Pelo menos 3 ciclos de autocorreção **no máximo**, com logs, tempo e custo limitados; error budget finito. Se origem/licença/documentação faltar, classificar impedimento específico e continuar o que for seguro.
- Salvar `qa3-runs/QA-XX/{PLANO_E_EXECUCAO.md,MATRIZ_6_GATES.json,PARECER_QA.md}` e SHAs individuais.

### BL-06 — Revisão cruzada após congelamento
- QA-01 revisa QA-03; QA-02 revisa QA-01; QA-03 revisa QA-02. Cada comparação registra `finding_id`, severidade, arquivo/linha/célula, evidência, testes para reproduzir, solução, status, reviewer, data e SHA.
- Não permitir autoparecer final sem revisão dos pares. Pareceres IA são verificação computacional; exigência de responsabilidade profissional formal permanece requisito externo da aprovação do escopo técnico.

### BL-07 — Correção integrada e atualização UX/dados
- Integrar **somente** correções que resolvam achados com testes em `feat/f01-governanca-normativa`; preservar `main`, F00 e golden.
- Completar o vínculo entre cálculo e **regra/célula realmente carregada pelo servidor**, distinguindo `CATALOG_METADATA`, `CLIENT_DECLARED`, `SERVER_ALGORITHM_TRACE` e `PRIMARY_SOURCE_VERIFIED`. Jamais converter automaticamente os três primeiros no último.
- Ensaiar histórico/restauração de revisões novas, integridade e concorrência SQLite, autenticação e ausência de dados de cliente misturados; aplicar migrations de produção **apenas em fase separada autorizada**.
- Exibir na UX estado pendente, motivo e fonte, sem selo verde indevido; dark/light, teclado, falha offline e navegação rastreável.

### BL-08 — CI final e critérios completos
- Executar `pytest` API, regressão `scripts/f00_golden.py --verify`, testes E2E Chromium, AIOX, lint, segurança, inspeção de fonte e documentação. **Todos os resultados devem apontar para o mesmo SHA final de integração**.
- Executar `python scripts/f01_release_gate.py --verify-invariants`, `python scripts/f01_cell_evidence_gate.py --strict` e revisão de **10 critérios AC-01.***. Um comando de integridade com exit 0 **não libera norma**.
- Validar lacunas críticas ENG-001 (arredondamento Iz) e ENG-002 (modalidades EDP), coerência territorial/temporal e NR-10 transitória; o resultado de F00 continua imutável.

### BL-09 — Decisão fail-closed sem humanos no loop
- Se todos os critérios estruturais/casos e evidências independentes comprovados, reunir **dossiê elegível para homologação externa**, vinculado ao SHA. A autorização formal, se exigida pelo próprio processo, não pode ser fabricada por agente: permanecer `AWAITING_EXTERNAL_SIGNOFF`.
- Se não houver original, licença, valor, segundo conferente genuíno, revisão profissional exigida ou código testado: registrar `BLOCKED_EVIDENCE`, `BLOCKED_SECURITY`, `BLOCKED_ENVIRONMENT` ou `FAILED_TECHNICAL`, com próximos comandos e evidências pendentes.
- **Nunca marcar F01 DONE nem liberar F02** só com três personas, testes verdes, `--yolo`, porcentagens em JSON ou SHA-256 do catálogo.

## 4. Seis gates — condições de verificação
| Gate | Prova indispensável | Consequência da falta |
|---|---|---|
| G01 | Edição, licença/autorização, documento original, vigência, concessão e hash | BLOCKED_SOURCE |
| G02 | 100% das células **necessárias e usadas** Iz/Rca/XL/EDP, notas, unidades e dupla conferência realmente independente | BLOCKED_SOURCE/REVIEW |
| G03 | Casos **normativos** de referência externa para cada cálculo efetivo, tolerância e resultado SIE | BLOCKED_EVIDENCE |
| G04 | Projeto/revisão/circuito/algoritmo, **IDs/células reais consumidos**, histórico íntegro, restore e diff | PARTIAL até linkage normativo |
| G05 | API + F00 golden + Chromium + AIOX + RBAC/segurança/UX (escopo definido), mesmo SHA | PARTIAL até suite final |
| G06 | Três relatórios iniciais com SHAs/contextos independentes, revisão cruzada e aprovação técnica formal quando necessária | BLOCKED_REVIEW |

**Aceite completo exige também AC-01.01–AC-01.10 no orquestrador.** Contagens de arquivos ou checagens de JSON não são aprovações normativas.

## 5. Arquivos e comandos de retomada
- **Plano mestre existente**: `PLANO_EXECUCAO_AUTONOMA_YOLO.md`; este v2 não o substitui: acrescenta a execução de **fontes/células** e a sincronização segura das branches QA.
- **Matriz de lacunas**: `MATRIZ_CELULAS_NORMATIVAS_F01.json`.
- **Guardião de evidências**: `scripts/f01_cell_evidence_gate.py`, modo status vs. `--strict` (exige prova externa).
- **Coordenador de agentes**: `scripts/f01_yolo_runner.py`. Sem parâmetros apresenta prévia. O comando `--execute --sandbox-confirmed` aciona Copilot Autopilot/YOLO em ambiente previamente isolado.
- **Histórico e status**: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`, `NEXT_ACTION.md`, `QA3_MANIFEST.json`.
- **CI**: workflows `.github/workflows/sie-restructuring-api.yml`, `sie-e2e-browser.yml`, `sie-orchestrator-quality.yml`.

```powershell
# Na raiz do clone isolado, com a branch F01 limpa e o Copilot CLI autenticado:
python scripts/f01_cell_evidence_gate.py
python scripts/f01_yolo_runner.py

# Somente dentro da VM/container descartável e autorizada:
python scripts/f01_yolo_runner.py --execute --sandbox-confirmed

# Após integração e evidências externas, avaliar estritamente:
python scripts/f01_cell_evidence_gate.py --strict
python scripts/f01_release_gate.py --check-release
```

## 6. Critério de saída
**SUCESSO DE IMPLEMENTAÇÃO:** código integrado com CI verde, issues QA documentados, erros corrigidos e lacunas normativas explicitadas sem falsear aprovações.

**SUCESSO TOTAL F01:** G01–G06 6/6, AC 10/10, fonte original conferida, cálculos independentes verificáveis, independência real dos revisores e aprovações externas pertinentes comprovadas; somente então tratar conclusão F01 conforme orquestrador. O fluxo deste plano **nunca inicia a F02**.

**Sem comprovação:** emitir relatório de pendências específico e manter `F01=BLOCKED`, `F00=DONE`, `F02=NOT_RELEASED`. Nenhum humano precisará interromper a automação para responder questões de rotina; exceções não comprováveis permanecem bloqueadas.
