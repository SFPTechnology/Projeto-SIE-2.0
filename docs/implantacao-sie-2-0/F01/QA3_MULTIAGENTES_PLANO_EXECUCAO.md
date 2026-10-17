# SIE 2.0 — Programa QA3 de implementação independente da F01
**Objetivo do programa:** alcançar, com provas auditáveis, **100% dos seis critérios F01**, sem forçar aprovação nem avançar para F02 enquanto houver bloqueios. Data: 2026-10-15. Documento de execução para outros LLMs/agentes especializados.

## Estado de partida, imutável como evidência
- Branch de integração `feat/f01-governanca-normativa`, PR #3 em draft, baseada em F00 DONE; manter `main` intacta.
- A API e a interface passaram por testes, mas o `ORCHESTRATOR_STATE.json` registra `F01=BLOCKED`, 0 células normativas homologadas e 0 fixtures numéricas normativas independentes.
- O catálogo de fontes (8 registros) e snapshots do **catálogo** no SQLite local não provam que a tabela foi realmente usada no cálculo; ainda não há histórico completo do cálculo por circuito/revisão.
- Os três novos arquivos `.agent.md` são **definições executáveis por plataforma compatível**, e seis `SKILL.md` são guias reutilizáveis. Sua criação **não** instancia agentes independentes, não executa suas correções e não constitui parecer profissional.

## Matriz de papéis, skills e responsabilidade integral
| Agente / ID | Principal diferenciação | Skills próprias | Responsabilidade |
|---|---|---|---|
| QA-01 Arquiteto | Python/FastAPI, segurança, motor, CI, snapshots, engenharia de sistemas | `f01-arquitetura-integridade`, `f01-verificacao-multigates` | **Executar E01–E05 integralmente e produzir seis provas G01–G06**, do código à conformidade técnica; parecer individual e revisão cruzada |
| QA-02 Engenheiro Eletricista | BT, ABNT NBR 5410, EDP e outras distribuidoras por concessão, NR-10, cálculo | `f01-engenharia-fontes`, `f01-calculo-independente` | **Executar E01–E05 integralmente e produzir seis provas G01–G06**; foco em célula, cálculo independente e regimes transitórios |
| QA-03 Dados/UX/LLM | banco relacional, rastreabilidade, interface técnica, acessibilidade e prompt evaluation | `f01-dados-evidencias`, `f01-ux-llm-seguranca` | **Executar E01–E05 integralmente e produzir seis provas G01–G06**; foco em histórico, UX, ataques e alucinação |

**Tarefas E01–E05 em cada um dos três planos individuais:**
- **E01:** fontes normativas, edições, licenças, concessões, vigências e original autorizado.
- **E02:** tabelas/células de Rca, XL, Iz, fatores, demanda/EDP, com unidade, notas e duas conferências **realmente independentes**.
- **E03:** cálculos independentes, expected, tolerâncias, limites e comparação SIE (golden F00 é só caracterização).
- **E04:** implementações Python/JS/SQL e dados por projeto/circuito/revisão, UX, hashes, rastreabilidade e testes de backup/rollback.
- **E05:** conflitos normativos, segurança, revisão adversarial, regressões, E2E, QA final e relatório.

## Checklist obrigatório G01–G06
| Gate | Evidência de aceite | Situação inicial |
|---|---|---|
| G01 Fontes | PDF/documento original autorizado, edição, vigência, jurisdição e licença; hash e citação | PARCIAL |
| G02 Tabelas | **100% das células efetivamente necessárias e usadas** verificadas por duas conferências separadas, valores/unidades/condições | BLOCKED |
| G03 Casos numéricos | Cálculos independentes de referência por motor e limites; original rastreável | BLOCKED |
| G04 Rastreabilidade | Cada resultado por circuito aponta para regras/células realmente usadas, revisão e memória; restore histórico e diff | PARCIAL |
| G05 Testes/segurança/UX | Suite CI verde sobre **mesmo SHA**, replay F00, Chromium, fuzz de entrada, autorização, backup e verificação UX | PARCIAL |
| G06 QA3 | Parecer inicial isolado de QA-01/02/03, revisão cruzada e resolução das divergências, atestação independente | BLOCKED |

**100% significa 6/6 aceitos com provas objetivas, não marcar caixas manualmente.** Se E01/E02 não possuírem material original ou autorizações, os agentes avançam em engenharia de software e registram bloqueio específico. Apenas a ausência de erro na CI **não** prova ABNT/EDP.

## Método de verdadeira separação de trilhas
1. Coordenador fixa a mesma branch base SHA de partida e cria `qa/f01-arquiteto`, `qa/f01-engenheiro-eletrico`, `qa/f01-dados-ux-llm`. Cada agente é convocado em execução/contexto separado com sua `.agent.md`; não recebe parecer ou código em andamento de outro agente, exceto baseline fixa.
2. Cada um cria e testa implementação própria de **todas** as E01–E05 em sua branch; registra na pasta `docs/implantacao-sie-2-0/F01/qa3-runs/QA-XX/` relatório individual com SHA, G01–G06, fontes/células, expected independente, CI e blockers.
3. Congelar o primeiro parecer com commit/hash e data antes de qualquer troca. Uma mesma sessão/LLM usando três personas **não é verificação factual independente**.
4. Rodada cruzada: QA-01 revisa QA-03; QA-02 revisa QA-01; QA-03 revisa QA-02, com objeções registradas. Nenhum agente aprova sua própria contribuição. Controvérsias normativas obrigatórias retornam à fonte primária e, quando requerido, a revisão profissional independente.
5. Coordenador reúne somente alterações validadas na branch F01; conflitos resolvidos com evidência, jamais por votação ou porcentagem de confiança. Executar regressão/QA3 sobre o merge final, mantendo PR draft até DONE legítimo.

## Contratos dos entregáveis individuais
`PLANO_E_EXECUCAO.md`: status E01–E05, tasks e commits, critérios/decisões, operações não realizadas. `MATRIZ_6_GATES.json`: estado de G01–G06, lista de evidências com URLs/SHA, premissas, reviewers. `PARECER_QA.md`: achados P0/P1/P2, correções, testes executados com link CI, impeditivos e recomendação. `FONTES_CONFERIDAS.csv`: coluna fonte/edição/abrangência/célula/unidade/leitor A/leitor B/diferença/resultado, sem redistribuir texto protegido. `CASES_INDEPENDENTES.json`: expected e referências quando a fonte tiver sido conferida.

## Gatilhos FAIL-CLOSED e segurança
- Proibir `verified_data=true` com base em campo cliente, JSON gerado por LLM, screenshot, IA autodeclarada perita, resumo de PDF sem origem ou relatório automático sem documento.
- Original não disponível, licença desconhecida, célula não conferida, discrepância, incerteza de data/distribuidora, QA não independente, pipeline falho, falsificação de evidência ou versão histórica irreproduzível = GXX BLOCKED.
- Não usar banco de produção, GitHub main, secrets, custo externo nem deploy; nunca usar `--force` para zerar erros, apagar golden F00 ou pular gate.
- Cada alteração SQLite deve ser ensaiada em arquivo descartável, testando histórico e restauração. Supabase/produção não autorizado nesta fase.
- Critérios `G01..G06` e `ORCHESTRATOR_STATE.json` permanecem bloqueados até verificação real. O relatório de orquestração não é assinatura normativa nem autoridade profissional.

## Ativação para iniciantes
Em ambiente compatível com os custom agents de GitHub Copilot, abra o repositório/branch contendo os perfis, selecione um perfil `f01-qa-...` no IDE ou execute `copilot --agent f01-qa-arquiteto --prompt "Execute integralmente E01–E05 de F01, registre o pacote individual e preserve os bloqueios não comprovados"` (CLI instalada e configurada). Repita em **sessões separadas**, cada qual na própria branch e partindo do SHA congelado; GitHub/VS Code pode exigir que os perfis sejam publicados na branch padrão para descoberta web, o que **não foi feito** para preservar `main`. Confirme a disponibilidade da ferramenta em sua conta; arquivos no Git por si só **não** agendam execução.

## Aceite e decisão da próxima fase
Use `scripts/f01_release_gate.py --verify-invariants` na CI. Ele verifica integridade do checklist e impede declaração inconsistentes; **não valida autenticidade humana ou técnica das fontes**, que exige revisão documental independente. Só depois de provas de G01..G06 aceitas + revisão humana pertinente o coordenador poderá aprovar F01 DONE; jamais liberar F02 antecipadamente.

## Checklist de ativação — recursos criados, execuções ainda pendentes

- Três branches distintas, mesma baseline `8aec14ac0817ba75ea5e5cee90240368807f1bf7`: `qa/f01-arquiteto`, `qa/f01-engenheiro-eletrico`, `qa/f01-dados-ux-llm`.
- Issues independentes: https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/4, https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/5, https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/6.
- Manual iniciante: `LEIA_PRIMEIRO_QA3.md`. Ativador opcional Windows: `scripts/INICIAR_F01_QA3.ps1` (modo simulação por padrão; requer `-Executar` e Copilot CLI autenticado).
- `scripts/f01_release_gate.py` é guardião estrutural fail-closed: sem revisão documental independente e assinaturas reais, nenhuma porcentagem ou JSON autoriza F01 DONE.
- **Status atual dos 3 agentes:** CONFIGURADOS; **0/3 EXECUTADOS**. Não afirmar paralelismo, revisão independente concluída ou status 6/6 aprovado.
