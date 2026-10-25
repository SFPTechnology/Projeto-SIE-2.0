# F12 — plano operacional de implantação e rollback (não executado)

## Pré-condições e segregação
**Somente para execução futura após G01–G08 GO documentado**; não aplicar os comandos abaixo em produção sem inventário e responsável. DEV/TEST locais não são homologação externa. Congelar SHA, versão Python/JS, banco, raízes de artefatos, políticas, DNS/TLS, migrações e permissões. Não levar fixtures, `.env` de teste, dados demonstrativos, tokens locais ou logs com dados pessoais para produção.

## Procedimento mínimo, com responsáveis designados no registro de mudança
1. **Pré-janela — DevOps/DBA:** inventariar domínio, runtime e rede; aprovar capacidade, disponibilidade, RPO/RTO, custo e acesso; obter teste completo do restore em cópia isolada; documentar formato e hash do backup.
2. **T-30 — operador:** suspender ou drenar gravações; impedir novas sessões; iniciar registro cronológico de execução e obter snapshot consistente. O módulo `local_bundle_backup_f11` exige escritores parados; não é backup transacional online conjunto SQLite+filesystem.
3. **T-20 — DBA:** copiar SQLite e TODAS as raízes F05/F10 pelo procedimento `python -m sie_api.local_bundle_backup_f11 backup --db <caminho_DB> --bundle <destino_NOVO>` em máquina de teste (substituir marcadores pelos caminhos aprovados, não executar no host real sem autorização). Verificar `bundle.json`, hash de banco/arquivos, cobertura das raízes e integridade referencial. Proteger backup com ACL e retenção definida.
4. **T-10 — DBA:** executar ensaio de migração upgrade/downgrade em clone offline; usar `data_lifecycle.migrate` apenas no contexto SQLite validado; migrations Supabase requerem plano distinto, nunca misturar bancos sem contrato de dados. Capturar `integrity_check`, `foreign_key_check`, contagem de registros e hashes antes/depois. Se downgrade perderia exclusões lógicas, interromper.
5. **T0 — DevOps:** promover somente artefato SHA/tag+checksum aprovados por estratégia canário/blue-green onde implementada. Não há estratégia de infraestrutura aprovada nesta fase; não improvisar rollout.
6. **T+5 — QA/operador:** smoke HTTPS/autenticação/ACL, leitura/escrita controlada, API, UX, documento F10 com hash verificado, stale após revisão, bloqueios normativos e ausência de dados de demonstração. Usar dados sintéticos.
7. **T+15 — SRE:** verificar latência/erro/recursos, logs sem segredos, backups, alarmes, disponibilidade e integridade; só avançar após aceite de cada janela.
8. **T+30 — change manager:** registrar decisão de manter/abortar; assegurar suporte, handover, runbooks e monitoramento reforçado. Horários são rótulos de ordem sugerida, não SLA aprovado.

## Abortar e reverter
Acionar rollback imediatamente para erro crítico de autenticação/isolamento, perda de dados, divergência de manifesto/hash, falha de migração, integridade SQLite/raízes, indisponibilidade acima do limite aprovado ou cálculo silenciosamente divergente. **Fail closed:** interromper escrita, preservar logs e snapshot forense (redigidos), comunicar responsável, desabilitar rota da versão nova, restaurar versão anterior junto com esquema compatível e conjunto completo de dados/raízes em ambiente limpo. Executar smoke, integridade referencial e reconciliação de contagens; nunca sobrescrever fonte original no teste. A API F11 de restore retorna `root_mapping`; aplicar ao serviço restaurado, incluindo `SIE_F10_ARTIFACT_ROOT`. Testar artefatos F05 e F10 antes de reabrir.

## Dependências críticas ainda não aprovadas
- Plano de identidade/ACL/RLS multiusuário e TLS/domínio: pendente.
- RPO, RTO, SLO e escala reais: pendentes.
- Backup consistente online, runbook de produção e mapeamento de dados externos: pendentes.
- Infraestrutura de canário/blue-green e rollback de migrações externas: não comprovadas.
- Responsável, janela, comunicação, custo e autorização formal: HUMAN_REQUIRED.

A existência deste arquivo não significa que houve ensaio nem implantação.
