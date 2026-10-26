# F12 — checklist de autorização GO/NO-GO

**Decisão corrente: NO-GO para produção.** Preenchimento somente com observações; campos sem evidência = `PENDENTE`. Nem o CI nem o modo autônomo aprovam mudança real.

| Gate | Evidência exigida | Estado |
|---|---|---|
| G01 — código | SHA fixado, diff autorizado, API/AIOX/Chromium atuais no mesmo SHA, manifesto e checksums | PARCIAL: F11 verificado, F12 a verificar |
| G02 — engenharia | fontes normativas válidas, casos independentes, responsável técnico e limites claros para projeto real | BLOQUEADO para uso profissional |
| G03 — identidade/segurança | autenticação e ACL de produção, HTTPS, segregação DEV/TEST/PROD, revisão de logs/secrets e acessos mínimos | PENDENTE |
| G04 — backup/restore | backup íntegro, RPO/RTO aprovados e ensaio com todas as raízes e SQLite no ambiente representativo | PENDENTE (F11 demonstrou local offline) |
| G05 — banco/migração | inventário de schema, upgrade/downgrade, reconciliar dados com hash/contagens em cópia representativa | PENDENTE |
| G06 — observabilidade | logs redigidos, métricas reais, alertas disparados, rota de incidente e ensaio de indisponibilidade | PENDENTE |
| G07 — produto | instalador/build reprodutível, hash e suporte, smoke/E2E, acessibilidade/compatibilidade acordadas | PENDENTE |
| G08 — mudança | responsável, ambiente, custo, impacto, data/janela, comunicação e autorização rastreada | HUMAN_REQUIRED |
| G09 — rollout | backup imediatamente anterior, implantação progressiva, smoke e reversão testada | NÃO EXECUTADO |
| G10 — pós-implantação | monitoramento da janela, resposta a falhas, integridade e aceite formal | NÃO EXECUTADO |

## Regra determinística
`GO` somente se G01–G08 estiverem comprovadamente aprovados no SHA/ambiente corretos **antes** de G09. `DONE` F12 somente após G09 e G10 também comprovados e QA3 aplicável aprovado. Qualquer `PENDENTE`, `HUMAN_REQUIRED` ou falha crítica implica `NO-GO`. Corrigir o defeito e repetir validação, não reclassificar.
O validador `scripts/f12_release_gate.py` confere apenas invariantes de preparação; `--require-production` recusa liberação mesmo que `--check` passe.

## Registro formal de decisão (não preenchido)
- ID de mudança:
- Responsável aprovador / função:
- Ambiente, URL, inventário de dependências, dados envolvidos:
- Janela (fuso horário), custo autorizado e plano de comunicação:
- SHA/tag, pacote/checksum, backups verificados, evidências de G01–G08:
- Resultado de risco, prazo de rollback e gatilhos de abortar:
- Parecer QA-01 / QA-02 / QA-03 e responsabilidade técnica aplicável:
- Decisão GO ou NO-GO / data / assinatura:
Sem esse registro, autorização permanece **AUSENTE**.

## Evidência incremental W1–W4
Código F12 `d7b55a7` validado por API 1210/Chromium36/AIOX/F12 safety8+19; builds determinísticos e recusa de adulteração; HTTPS em loopback sem domínio real. **G01 parcialmente validado para distribuição LOCAL_QA; G03/G04/G05/G06/G07 NÃO validados em produção**. G02/G08 HUMAN_REQUIRED, G09/G10 NÃO EXECUTADOS. Não promover estas medições sintéticas a `GO`.
