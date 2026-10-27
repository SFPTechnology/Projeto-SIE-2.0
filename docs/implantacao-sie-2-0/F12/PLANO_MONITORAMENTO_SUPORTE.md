# F12 — plano de monitoramento, alarmes, suporte e incidentes

**Estado:** PLAYBOOK PREPARADO; nenhuma plataforma externa, dashboard, alarme de produção ou pós-deploy foi configurado/testado nesta execução.

## Medições obrigatórias para um ambiente futuro
| Sinal | Coleta/alerta a ensaiar | Reação |
|---|---|---|
| Disponibilidade e TLS | health endpoint, certificado, DNS, erro de handshake, status 5xx | interromper rollout, abrir incidente |
| Latência | p50/p95/p99 por rota sem parâmetros pessoais; definir alvo pela capacidade aprovada | investigar saturação e filas |
| Erros e segurança | taxa 4xx/5xx, 401/403, acessos negados, tentativas de login | verificar autenticação e evento de segurança |
| Persistência | integridade SQLite ou DB homologado, tamanho, filas, migrações, estados não publicados | suspender escrita e executar diagnóstico |
| Artefatos e regras | download com SHA inválido, documentos `STALE` apresentados como correntes, edição de regra inesperada | bloquear entrega e preservar proveniência |
| Backup | atraso/ausência, checksum, teste de restore periódico, últimas cópias válidas | escalonamento e teste em cópia isolada |
| Infraestrutura | CPU, memória, disco, conexões, TLS, backups, alarmes, disponibilidade | ampliar ou reverter conforme change |

Os valores de SLO local na F11 são **provisórios e não representativos de produção**; não inventar limiar numérico. A equipe de operação deve fixar limiares/volume de carga, RPO/RTO, contatos e ferramentas ANTES do GO.

## Playbook do incidente (P0/P1/P2)
1. Identificar horário, versão/SHA, ambiente e sintoma; atribuir responsável de plantão.
2. Preservar registros com dados pessoais e tokens redigidos; assegurar correlação sem revelar payloads.
3. P0 (integridade, acesso indevido, cálculo que gera documento incorreto ou indisponibilidade crítica): **congelar rollout e escrita**, acionar responsável, avaliar rollback.
4. P1 (degradação, falha de backup) e P2 (UX/funcionalidade recuperável): abrir ticket com impacto, contorno e prazo designado; sem reduzir gates de segurança.
5. Verificar hashes, `CURRENT/STALE`, consistência de banco/arquivos e último restore comprovado.
6. Executar correção em TEST, replay do caso, regressão e aprovação antes de reintroduzir; evitar mutações diretas em produção.
7. Fechar somente com evidência de saúde e pós-mortem: causa raiz, impacto, linha do tempo, ação corretiva e teste de não regressão.

## Suporte e feedback
Canal, SLA, plantonista, plataforma de tickets e usuários piloto: **a definir pelo titular**. Registrar tickets com ID, gravidade, ambiente, SHA, versão de regra, evidências sanitizadas, ações e aceite. Sondar UX do primeiro acesso e erro; nunca coletar tokens de usuários.

## Relatório de pós-implantação
`RELATORIO_POS_IMPLANTACAO.md` inicia como **NÃO EXECUTADO**, pois não houve deploy. Atualizar por responsável após mudança autorizada: janela, commit/tag, checksums, banco/schema, smoke, indicadores e eventos, rollback, aceites, pendências e decisão de operação.
