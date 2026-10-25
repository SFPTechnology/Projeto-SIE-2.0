# F11 — relatório de execução

## Decisão final de software — 25/10/2026

**F11 DONE para QA do software local suportado, condicionada à confirmação dos três workflows no SHA deste fechamento documental. Liberação técnica/profissional e produção: REPROVADAS.** A implementação de código `51c5e95dca484294418d5db9ca7b05156a86d3fb` tem API [40164100141](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/40164100141) (1202 passed, 1 warning), AIOX [40164100172](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/40164100172) e Chromium [40164100154](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/40164100154) (36 passed), todos completed/success no mesmo SHA. QA-01/02/03 aprovaram separadamente o recorte local; QA-02 não aprovou conformidade normativa/profissional. F00 manteve 34 casos. A captura `pip freeze` nos workflows desta edição permite reconstruir o ambiente resolvido por run; conferir artefatos e três CI no SHA documental final antes de tomar este fechamento como confirmado.

Os AC-11.01–11.10 foram atendidos **como processo de QA e decisão do recorte local**: a matriz lista motores e pendências, o E2E cobre navegador Chromium, o backup exige parada de escritores e a sonda mede SLO provisório local. O parecer técnico rejeita a elegibilidade de release profissional por fontes/casos normativos e inspeções físicas ainda pendentes. F10 legado segue preservado; `f11_require_f09=True` seleciona o fluxo integrado consultivo, sem converter F06–F08 em motor normativamente homologado. Nenhum merge em main ou deploy ocorreu. As seções abaixo são histórico quando conflitarem com esta decisão.

## Continuação de 25/10/2026 — integração implementada, validação de CI pendente

**CI intermediário:** `af11b81856ff2412af60234c929c2f6881eb035c` teve API e AIOX success; Chromium failure em `40163941377` por porta web aleatória fora da lista CORS. Fixture E2E corrigido para origem local 5173; repetir os três workflows no novo SHA antes de decidir o gate.

O plano em `PLANO_FECHAMENTO_INTEGRAL.md` foi executado na branch F11. A ponte F09→F10 exige F09 quando `f11_require_f09=True`, reconcilia projeto, revisão, topologia, IDs e hashes F06–F08 e avaliação consultiva, e grava a proveniência no snapshot, manifesto, HTML e PDF. O modo F10 legado permanece explícito e sem alegação F09. Um teste altera carga, observa `STALE`, refaz F06/F07/F08/F09 e CalculationRun F10 e obtém `CURRENT`; seis adulterações de metadados/IDs foram recusadas após correção QA-01.

O backup offline `sie_api/local_bundle_backup_f11.py` inventaria as duas raízes F05/F10 registradas, verifica hashes e estado, restaura banco e raízes em destinos novos e devolve mapeamento para configurar o serviço. Corrupção, symlink, estado incompleto, overwrite e destino dentro da fonte são recusados. Escritores devem ser parados; não há snapshot transacional online entre SQLite e filesystem. `EVIDENCIAS_RESILIENCIA.md` contém as seis medições locais, SLO provisório e limites. O E2E F11 está em `restructuring/e2e/test_f11_browser.py` para execução no CI Chromium.

**Verificações locais atuais:** API `1202 passed, 1 warning`; F00 `34` casos históricos; npm lint/typecheck/test (18)/build exit 0; QA-01 aprovou o contrato local, QA-02 aprovou a rastreabilidade consultiva e manteve homologação normativa/profissional pendente, QA-03 aprovou recuperação/resiliência local e aguarda Chromium. Chromium local não iniciou por binário ausente; execução remota no SHA final é obrigatória. As seções abaixo descrevem o checkpoint anterior e são históricas quando conflitantes.

**Estado: BLOCKED.** F10 permanece DONE. A base `540f2c8e7e61a1efb6bf71abcedc8768d7086914` corresponde à branch `feat/f09-concessionarias-especializadas` e tem três workflows success: API `40142136768`, AIOX `40142136778`, Chromium `40142136788`. F11 usa branch isolada `feat/f11-qa-integrado`; nenhuma alteração em main ou produção.

## Execução observada

| Task | Estado | Evidência e lacuna |
|---|---|---|
| 11.01 | PARCIAL | Candidato, versões, dados e limites em `CANDIDATO_E_COMISSIONAMENTO.md`; versão Python transitiva não travada; registrar SHA final/ambiente CI. |
| 11.02 | PARCIAL | QA-02: 134, 111 e 118 testes focados, conjuntos sobrepostos; casos sintéticos e limites do motor, sem conferência normativa integral. |
| 11.03 | PENDENTE | `MATRIZ_VALIDACAO_INTEGRADA.md` por motor; fontes e casos de engenharia profissionais incompletos. |
| 11.04 | PENDENTE | Teste novo cobre CURRENT → mudança de geometria → STALE → recálculo → CURRENT. F09 persiste F06–F08; F10 usa parser F05 e motor legado. Falta percurso único com mesmas evidências e revisão. |
| 11.05 | PENDENTE | F10 teve Chromium no SHA base; executar F11 no SHA final e conferir jornadas aplicáveis. |
| 11.06 | PENDENTE | Dois testes negativos novos passam. Recuperação SQLite + múltiplas raízes de arquivo não demonstrada. Tentativa experimental falhou em dois testes e foi retirada antes do commit. |
| 11.07 | PENDENTE | Não há SLO aprovado nem medição representativa de concorrência, carga, timeout e indisponibilidade. |
| 11.08 | PARCIAL | Pacote F10 testado para snapshot e revisão; não concilia um fluxo único F06–F10. |
| 11.09 | PARCIAL | Checklist aplicável criado; todos os ensaios físicos NÃO EXECUTADOS, dependem de projeto real. |
| 11.10 | REPROVADO para liberação | Três pareceres separados documentados; gates 11.03–11.07 impedem homologação e F12. |

## Testes e alterações

- API local: `python -m pytest -q` em `restructuring/apps/api`: **1184 passed, 1 warning**, 21,99 s (após retirada de implementação de backup incompleta).
- AIOX local: `npm ci --prefix .aiox-core --ignore-scripts --no-audit --no-fund`; `npm run lint`, `npm run typecheck`, `npm test` (18 testes) e `npm run build`: saída zero.
- Testes novos: `test_f11_integrated_revision.py` e `test_f11_security_recovery.py`. Três workflows foram configurados para reagir a story/evidências F11; CI do SHA final ainda não verificado neste registro.
- QA-01: PENDENTE, integração contínua e CI. QA-02: APROVADO para recortes computacionais, PENDENTE para homologação técnica. QA-03: PENDENTE, recuperação multi-raiz, resiliência e E2E F11.

## Condições concretas de desbloqueio

1. Ligar avaliação persistida F09 (F06 demanda, F07 condutores, F08 proteção) ao cálculo/documento F10 com os mesmos IDs, hashes, projeto e revisão; teste de alteração de carga, recálculo e obsolescência ponta a ponta.
2. Criar backup/restore offline de SQLite e **todas** as raízes registradas, inclusive exportações F05 e artefatos F10, com rejeição de corrupção, ausência e caminho indevido; validar recuperação isolada.
3. Definir alvo de navegadores e SLOs do ambiente local; medir concorrência/carga/falhas e executar E2E e segurança no SHA final.
4. Conferir fontes/casos independentes e aplicabilidade por profissional qualificado para qualquer homologação normativa; completar inspeções de campo quando houver instalação real.
5. Reexecutar API/AIOX/Chromium no SHA final, corrigir achados e obter QA-01/02/03 favoráveis aos gates de F11. Não iniciar F12 enquanto F11 estiver BLOCKED.

Nenhuma contagem de teste concede conformidade ABNT, NR-10 ou concessionária. Os três revisores automatizados fornecem perspectivas técnicas separadas, sem substituir auditoria humana independente.
