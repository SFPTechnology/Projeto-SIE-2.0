# F11 — relatório de execução

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
