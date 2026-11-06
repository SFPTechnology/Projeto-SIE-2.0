> **SUSPENSO POR DECISÃO DO RESPONSÁVEL — 04/11/2026.** O usuário declarou que **não deseja realizar o backup remoto recuperável do SIE 2.0**. Este documento é mantido apenas como referência histórica, não como autorização de execução. Não iniciar atividades C17 de backup ou restauração, não criar runners privilegiados/segredos/cofres nem tentar a operação por outro meio sem nova decisão explícita. Como não há recuperação real comprovada, migrations remotas e importação real seguem bloqueadas; código, testes e análises somente de leitura podem continuar.

# C17 — Plano Executivo: Backup Remoto Recuperável do Supabase SIE 2.0

**Versão:** 1.0 — **Data:** 04/11/2026  
**Programa:** SIE 2.0 / Bloco C / Gate GC  
**Destino:** Supabase `fozrymsidnaxmuvxxfhh` — `SIE_2.0`, PostgreSQL 17.11, sa-east-1, pré-produção, organização Supabase no plano Free.  
**Repositório:** `SFPTechnology/Projeto-SIE-2.0` (**PÚBLICO**).  
**Branch exclusiva de desenvolvimento:** `feat/v201-bloco-c-dominio-eletrico`.  
**Fonte legada:** `hlbksclcandbsyqrsbmx` (**SOMENTE LEITURA**, não é o destino do backup desta fase).  
**Contrato de autorização:** `C08_CONTRATO_ENTREGA_C_V201.json`; os itens 1 e 2 já foram autorizados PARA EXECUÇÃO em 04/11/2026, **sem aprovação técnica antecipada**.  
**Classificação:** PLANO DE IMPLEMENTAÇÃO, NÃO EVIDÊNCIA DE BACKUP REAL, RESTAURAÇÃO OU LIBERAÇÃO DE GC.

> **Missão operacional:** arquitetar, implementar, testar e comprovar uma cadeia de backup REAL do banco de pré-produção SIE 2.0 e restauração isolada/independente, **sem testes no computador do usuário, sem Docker Desktop e sem custos adicionais**, preservando os dados em custódia privada recuperável fora do GitHub e do próprio Supabase. Somente depois dos gates de proteção e segurança poderá ser considerada a aplicação das migrations A03/A04/B04/C03 e a migração dos cinco projetos, em procedimento separado.

## 0. Premissas verificadas versus pendências

| Item | Evidência disponível em 04/11/2026 | Impacto |
|---|---|---|
| Destino | `fozrymsidnaxmuvxxfhh` ativo; PostgreSQL 17.11; não é produção | Host certo, mas confirmar novamente na execução |
| Plano da organização Supabase | **Free** | Não presumir backups diários gerenciados; não contratar PITR/add-ons |
| Baseline remoto | GF02 `20261027195557` aplicada; A03/A04/B04/C03 não aplicadas | Fazer backup **antes** de DDL |
| Tabelas e políticas | 9 tabelas/63 colunas públicas, 16 políticas RLS | Recuperação precisa preservar estrutura e políticas |
| Dados do destino | 1 conta Auth; 0 projetos e 0 revisões; 0 buckets e 0 objetos em Storage | Proteger também Auth e metadados; zeros não significam ausência de configurações externas |
| Repositório GitHub | **PÚBLICO**; branch C e PR #11 não integradas à main | Logs e artefatos podem vazar dados; trabalho privilegiado **não** roda em PR não confiável |
| Onda C15 | Scripts para Windows/CI sintético e guardas já implementados | **Não** são backup real; C17 é o caminho remoto separado |
| Fonte original | 5 projetos, 41 ambientes, 52 cargas, 1805 auditorias, 1934 registros operacionais/15 tabelas | **Não** exportar nesta fase; fonte exige plano de corte próprio |
| Recuperação real | Arquivos de backup reais, teste de restore em outra execução e custódia privada: **NÃO COMPROVADOS** | `GC=BLOCKED`; nenhuma migration autorizada para execução imediata |
| Segurança | Advisor Auth: proteção contra senhas vazadas desabilitada (WARN) | Registrar mitigação/limitação, sem assumir que recurso pago está disponível |

**Fontes de referência verificáveis:**  
- https://supabase.com/docs/guides/platform/backups  
- https://supabase.com/docs/guides/database/psql  
- https://www.postgresql.org/docs/17/app-pgdump.html  
- https://www.postgresql.org/docs/17/app-pgrestore.html  
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners  
- https://docs.github.com/en/actions/reference/security/secure-use  

## 1. Limites e decisões de arquitetura

1. **Sem PC do titular:** todo ensaio ocorre em infraestrutura remota temporária de execução controlada, com PostgreSQL 17 nativo em ambiente Linux; nenhum `pg_dump`, `pg_restore`, Docker Desktop ou instalação no Windows do usuário.
2. **Sem custos adicionais:** a consulta ao GitHub confirmou repositório **público**. Os runners hospedados **padrão** são gratuitos nesse cenário, conforme a documentação; NÃO utilizar runner maior ou serviços pagos. Verificar limites, espaço e eventual cobrança de **armazenamento externo** separadamente. A ausência de custo de CPU não prova a existência de local de guarda de backup.
3. **Sem usar GitHub como cofre de dados:** proibir envio de dumps, arquivos SQL, objetos Storage, tokens, segredos, `auth.users`, informações pessoais e dumps cifrados sem aprovação específica para GitHub `artifacts`, `cache`, `releases`, `commits` ou logs. No repositório público, publicar SOMENTE código, listas de verificação e **evidências agregadas sanitizadas**.
4. **Custódia segura é pré-requisito**: identificar e homologar um destino de armazenamento privado **já existente**, com acesso controlado, criptografia robusta, versionamento/imutabilidade e retenção suficiente para o rollback. Precisa ser **independente** do Supabase a ser alterado e de runner efêmero. **Não presumir** que a Hostinger, o GitHub, outro Supabase, um disco temporário ou alguma nuvem tenha armazenamento autorizado. Sem cofre privado comprovado e sem custo adicional: `BLOCKED_SECURE_ESCROW`, e NÃO iniciar dump real.
5. **Gatilho manual e ambiente protegido:** ao tratar banco real, não usar workflow disparado por `pull_request`, `pull_request_target` ou código de fork. Exigir aprovação de execução privilegiada, verificação de SHA fixo, conta de serviço mínima, `GITHUB_TOKEN` somente leitura, ações/dependências fixadas por SHA e segredo disponível **apenas** na etapa protegida. Se os recursos de proteção não forem viáveis no workflow atual, usar executor remoto confiável preexistente (não inventar novo serviço).
6. **Limitação operacional do GitHub:** workflows com `workflow_dispatch` normalmente devem existir na branch padrão para serem disparáveis pela interface/API. **Não** violar a proibição de alterar `main` para facilitar a execução. O agente SRE deve verificar uma modalidade de execução já autorizada em workflow existente que não exponha segredos a push/PR, ou declarar `BLOCKED_EXECUTOR_TRUST`. O plano **não presume** que apenas publicar YAML na branch C torna o disparo seguro/possível.
7. **Restauração sem backdoors:** criar banco PostgreSQL 17 temporário em **segunda execução/runner isolado**, sem conexão com o Supabase de produção. Não restaurar em `fozrymsidnaxmuvxxfhh`, não fazer `db reset`, não criar novo projeto Supabase. Antes de executar conteúdo do dump, inspecionar TOC/DDL e restringir rede/privilégios porque restauros SQL podem executar código do banco de origem.
8. **Sem prematuridade:** a autorização anterior vale para execução dos itens 1 e 2, **não** dispensa dump real, restore funcional, prova de custódia, segurança, vinculação Auth, origem read-only e teste ETL. Documento com status `PASS` não é substituto dessas evidências.

### Arquitetura lógica escolhida

```text
Supabase SIE 2.0 (PostgreSQL 17.11, SEM ALTERAÇÃO)
        |  TLS com CA oficial + credencial protegida; SQL/pg_dump read-only
        v
Executora remota CONFIÁVEL A (PostgreSQL 17 nativo, sem Docker Desktop)
        |  pg_dump -Fc -> fluxo criptografado antes da persistência
        |  checksum, TOC, inventários e status segregados
        v
Cofre privado EXTERNO e JÁ EXISTENTE, criptografado e recuperável
        |  imutável / verificação de retenção / prova de leitura independente
        v
Executora remota CONFIÁVEL B (nova instância, sem acesso de escrita ao Supabase)
        |  download autenticado, decriptação apenas em armazenamento temporário
        |  pg_restore -> Postgres 17 LOCAL e DESCARTÁVEL do runner B
        v
Comparação independente de dados, schemas, RLS, Auth, roles, extensões
        |
        +-- GC-RECOVERY=GO     => somente autorização para iniciar a fase de migrations
        +-- GC-RECOVERY=NO_GO  => STOP, manter DB remoto preservado
```

**Cofre:** armazenamento externo privado e já contratado/disponível, com criptografia ponta a ponta. A especificação não pressupõe que haja acesso atual a esse cofre; comprovar a disponibilidade antes de integrar qualquer segredo. O identificador do objeto pode ser armazenado apenas em relatório restrito; o GitHub público deve conter somente uma referência opaca não reversível se necessária.

## 2. Agentes especializados — separação de funções

| Perfil | Responsabilidade executiva | Critério de independência |
|---|---|---|
| **C17-DBA** — DBA PostgreSQL sênior | Examinar integridade da base, pg_dump nativo, matrizes schema/roles/Auth, TOC, validar compatibilidade e restauração PostgreSQL 17 | Não aprova o próprio dump sem ensaio conduzido pelo SRE/QA |
| **C17-SRE** — engenheiro de confiabilidade | Identificar executor remoto seguro e cofre já existente, implementar pipeline de duas execuções independentes, reter backup e ensaiar RTO/RPO/rollback | Não acessa dados pessoais em logs; prova extração do cofre |
| **C17-SEC** — engenheiro de segurança | Revisar threat model, identidade do endpoint, CA/TLS, segredos, proteção de ambientes, acesso mínimo, supply chain e LGPD | Pode vetar GO; não altera o parecer do DBA |
| **C17-QA** — revisor de recuperação | Criar casos de sucesso e falha, comparar inventários e hashes, injetar falhas com dados sintéticos | Executa em novo runner; não aceita apenas testes de parser |
| **C17-AUD** — auditor de gates | Confrontar evidência real, assinatura de revisão, contrato C08 e decisões de NO-GO | Somente decide elegibilidade; não cria provas ou declara profissional C13 |
| **C17-ORQ** — orquestrador | Coordenar dependências, SHA imutável, ações de correção e CI | Não se autodeclara auditor independente ou profissional humano |

Os perfis são agentes de revisão de IA em áreas com **rigor esperado de especialistas com 20 anos de experiência**; não representam funcionários/DBAs humanos efetivamente designados. Qualquer atestação institucional/humana continua sob responsabilidade do titular.

## 3. Ondas de implementação — backlog técnico, evidências e gates

### C17-00 / G0 — Pré-voo e decisão de viabilidade de custo/segurança

**Responsáveis:** SRE + Segurança; auditor valida.  
**Ações:** reconfirmar projeto e plano Supabase Free; verificar que backup diário gerenciado não está disponível no plano; confirmar GitHub público/runner padrão; verificar se existe **cofre privado prévio de retenção**, capacidade, ACL, criptografia, acesso futuro e ausência de cobrança. Conferir que não há recursos de produção/Hostinger envolvidos. Verificar mecanismo de workflow protegido viável sem alterar main, sem PR não confiável e sem disparo automático de secrets. Identificar executor A/B e demonstrar que pode armazenar dados temporariamente e apagar todo residual.  
**Implementar:** `scripts/c17_remote_preflight.py` e `C17_EVIDENCIA_PREVOO.json`, com esquema `cost_zero`, `executor_trust`, `escrow_separate`, `secret_provisioning`, `no_remote_writes`; somente status, sem host completo/credenciais.  
**Saída G0:** `PASS` SOMENTE com cofre e executor **realmente comprovados**; caso contrário `NO_GO_SECURE_STORAGE_OR_EXECUTOR`. Não iniciar dump real.

### C17-01 / G1 — Implementação controlada do workflow remoto

**Responsáveis:** SRE escreve, Segurança revisa, QA testa.  
**Entregas propostas:**
- `scripts/c17_backup_remote.sh`: shell POSIX/Bash com `set -Eeuo pipefail`, tratamento de sinais e remoção de temporários.
- `scripts/c17_restore_remote.sh`: leitura do cofre externo e restauração em runner isolado B.
- `scripts/c17_backup_manifest.py`: manifesto sem PII, bytes, SHA256, PostgreSQL major, SHA exato do código, instante, cobertura de schema, referências internas de evidência.
- `scripts/c17_verify_recovery.py`: validação de cobertura e reconciliação.
- `.github/workflows/sie-c17-recovery-secure.yml`: definição de pipeline **somente preparatória na branch C**, não adicionar gatilhos privilegiados indiscriminados; ativação protegida demanda G0 aprovado e solução compatível com branch/main.
- `restructuring/apps/api/tests/test_c17_*.py`: positivos/negativos offline e integração PG17 sintética.
- `docs/implantacao-sie-2-0/GREENFIELD/C17_*.json`: manifests sanitizados, provas e decisões.

**Controles técnicos:** 
- runner padrão `ubuntu-24.04` (VM), `postgresql-client-17` e `postgresql-17` nativos, instalados/pinados por fonte de pacotes autenticada; **sem Docker Desktop**. Testar versão cliente exata e espaço em disco.
- workflow protegido com `permissions: {contents: read}`, `concurrency` não concorrente, SHA integral fixado do checkout, `persist-credentials: false`, `timeout-minutes` conservador, `environment` aprovado e secrets escopados.
- nunca usar `pull_request_target`, `workflow_run` com artefato de PR como script, forks, releases ou caches não confiáveis para a etapa com acesso ao banco real.
- apenas imagem/ações oficiais ou cuidadosamente auditadas, pinadas por **SHA completo**; dependências Python/CLI bloqueadas com hashes.
- `set +x`, mascaramento de variáveis sensíveis, sem URIs completas/SQL/TOC nos logs; artefatos do GitHub contendo **somente evidências agregadas**.
- impedir upload e print de qualquer dump em caso de erro; eliminar arquivo temporário e tentar higienizar, sem prometer limpeza forense de discos de terceiros.
- todos os segredos residem em *GitHub Environment Secrets* ou gestor de segredos já disponibilizado, com revisão de acesso. **Nenhum segredo é criado, lido ou armazenado por este plano.**

**G1:** executar pipeline completamente sintético, incluindo falhas de autenticação, host inesperado, segredo ausente, dump corrompido, cofre inacessível, checksum incorreto, restore incompleto, storage sem retenção e PR malicioso. Tudo deve resultar em `NO_GO` sem exposição.

### C17-02 / G2 — Levantamento pré-backup do Supabase (somente leitura)

**Responsáveis:** DBA + Segurança.  
**Ações:** conectar ao **endpoint exato de destino**, confirmado no Dashboard; impor `sslmode=verify-full` e CA correto; preferir conexão direta ou session pooler 5432 somente quando suportado; nunca transacionar dados via pooler de transação sem validação. Inventariar schema `public`, `auth`, `storage`, extensões, roles/GRANTs, RLS, migrações e storage externo; conferir expected GF02 e detectar deriva. Validar permissões suficientes para ler `auth.users` sem reproduzir dados.  
**Baseline indicativa:** `auth.users=1`, `auth.sessions=0`, projetos/revisões zero, policies `public=16`, buckets/objects zero; reconferir em execução, não impor números antigos se houver mudança legítima.  
**G2:** `PASS` se identidade, TLS, cobertura de leitura, capacidade e política de acesso confirmadas; zero DDL e zero DML no remoto.

### C17-03 / G3 — Backup REAL e custódia criptografada

**Responsáveis:** DBA executa, SRE custodia, Segurança monitora.  
**Procedimento:** 
1. Garantir G0/G1/G2 e autorização C08 verificados, congelar SHA e janela de snapshot.
2. Executar `pg_dump` nativo do banco de destino em **formato custom `-Fc`** com snapshot MVCC consistente, saída **transmitida para criptografia autenticada** (ex.: `age` com chave pública de custódia previamente homologada) antes de persistência externa. **Sempre `pipefail` e validação de todos os exit codes**, não inferir sucesso apenas pela existência de arquivo.
3. Usar credenciais do serviço protegidas e restrição lógica de leitura; se o papel necessário ao dump tiver privilégios administrativos por limitações da plataforma, reforçar a barreira de comandos/método e revisão SecOps — não criar novos papéis por DDL antes do backup.
4. Inventariar TOC `pg_restore --list`, verificar cobertura real `public` e dados necessários de `auth` e `storage`; se `pg_dump` não exportar completamente algum objeto essencial, registrar `PARTIAL` e `NO_GO`.
5. Inventariar *recursos externos* ao dump: objetos de Storage (0 confirmados previamente, reconferir), configurações Auth/identidade, credenciais gerenciadas e Edge Functions. Se essenciais para rollback, preparar inventário e procedimento independente **sem colocar segredos em backup/relatório público**.
6. Depositar o backup já cifrado no cofre privado **externo ao Supabase**. Confirmar que objeto existe, é legível por entidade independente, tem checksum verificável, retenção e chave de decriptação recuperável. O manifesto público contém no máximo identificador opaco e estado verificado, sem dados de conexão.
7. Remover resíduos temporários do runner, invalidar credenciais efêmeras quando possível, auditar acessos e política de retenção.

**Observação de engenharia:** `pg_dump` cobre um banco, **não** faz dump de roles globais, senhas ou dos binários do Storage API; restauração plena de uma plataforma Supabase pode demandar camadas adicionais. Uma prova de cópia PostgreSQL **não** autoriza declarar prontidão geral de todos os serviços. 
**G3:** `PASS` com arquivo REAL custodiado e inventário completo do escopo. Backups vazios, corrompidos, não criptografados, não persistentes, no próprio Supabase ou somente em runner/GitHub = `NO_GO`.

### C17-04 / G4 — Prova de restauração em SEGUNDA execução independente

**Responsáveis:** SRE executa, QA reconcilia, DBA observa.  
**Ações:**
1. Criar nova VM/runner padrão e banco PostgreSQL 17 **descartável** no próprio runner B, acessível **somente em loopback**; sem usar Docker Desktop, novo projeto Supabase, main ou infraestrutura de produção.
2. Baixar o backup **do cofre externo**, provar que ele não depende do runner A e validar checksum do ciphertext antes da decriptação.
3. Decriptar **apenas na máquina isolada**, validar formato e integridade do dump, listar TOC e revisar DDL potencialmente executável antes do restore.
4. Preparar roles/extensões da instância de prova segundo receita local mínima auditada; não inferir que reproduz `supabase_auth_admin`/ACL/segredos gerenciados; registrar diferenças.
5. Usar `pg_restore --exit-on-error`, com transação única quando viável, em banco **novo e vazio**. Recusar `--clean` ou `DROP DATABASE` fora da VM B, host remoto, socket externo e bancos preexistentes. Recusar opção `--no-owner`/`--no-acl` como atalho para declarar equivalência.
6. Executar verificações SQL de contagens, FKs, índices, constraints, triggers, schema, sequências, Auth/Storage, 16 políticas RLS, grants e extensões; inspeção de dados sensíveis **agregada** apenas. Quando roles/serviços Supabase não forem reproduzíveis no PostgreSQL puro, emitir `PARTIAL` e propor procedimento de restauração credível para o **escopo específico das migrations**, sem alegar recuperação integral da plataforma.
7. Repetir ensaio em outra VM/novo banco, ou teste independente equivalente com rastreabilidade; reconfirmar acesso futuro à chave e objeto do cofre.
8. Confirmar que a instância real de destino ficou intocada.

**G4:** `PASS` só se a restauração atender a cobertura de recuperação exigida para a próxima mudança, suas limitações estiverem explicitadas/aceitas por DBA + SecOps + SRE, e a capacidade de recuperar a cópia do cofre permanecer comprovada. Se dependências críticas do Supabase não forem recuperáveis: `NO_GO`.

### C17-05 / G5 — Auditoria de segurança e continuidade

**Responsáveis:** Segurança + DBA + Auditor.  
**Testes independentes obrigatórios:**
- ameaça 1: workflow no **repositório público** com `secrets` acessíveis a PR/fork → bloqueio;
- ameaça 2: arquivo/artefato, dump, SQL ou texto em log, commit, cache ou GitHub Actions `artifacts` → bloqueio;
- ameaça 3: endpoint errado, senha em URL, `sslmode` inferior a `verify-full`, CA não validado → bloqueio;
- ameaça 4: vazamento da chave privada da criptografia ou indisponibilidade de recuperação → bloqueio;
- ameaça 5: falha parcial em `pg_dump` ou `pg_restore`, TOC incompleto, hash divergente → bloqueio;
- ameaça 6: roles/Auth/Storage não recuperáveis quando essenciais para rollback → bloqueio;
- ameaça 7: backup expirado, dependência do runner que será destruído, cofre não independente, acesso futuro não comprovado → bloqueio;
- ameaça 8: ferramenta altera origem, `main`, F12, Hostinger, produção, cria projeto pago ou aplica DDL remoto prematuramente → bloqueio.
- ameaça 9: janela de backup ultrapassa baseline de schema e dados antes das migrations → novo backup antes do GO; não reutilizar snapshot desatualizado.

**Saída:** `C17_SECURITY_VERDICT.json` sem segredos; `C17_RECOVERY_EVIDENCE.json` com assinatura técnica de revisão (sem forjar assinatura humana) e evidência de cofre; decisão independente `GO_RECOVERY_READY` / `NO_GO`.

### C17-06 / G6 — Handoff controlado para migrations e GC

**Responsáveis:** AUD + ORQ, com aprovação humana somente se requerida pelo procedimento de mudança.  
**Exigir conjuntamente:**
- [ ] Execução no ambiente confiável, sem custo novo e sem Windows do usuário.
- [ ] Backup REAL do **destino correto** e cópia **persistente, cifrada e recuperável** em cofre externo homologado.
- [ ] Restauração real bem-sucedida com **outro runner** e escopo de recuperação comprovado.
- [ ] Auth/RLS, roles/ACL, extensões e objetos externos classificados e cobertos por plano de recuperação demonstrado.
- [ ] Revisão independente DBA + SRE + Segurança sem bloqueio crítico.
- [ ] Manifesto com SHA do software e snapshot do banco antes de DDL; retenção suficiente para rollback.
- [ ] Confirmação de que GF02 é a única migration aplicada e A03/A04/B04/C03 estão pendentes.
- [ ] Logs e evidências sanitizados; nenhum dado pessoal/segredo publicado.
- [ ] Separação clara entre `RECOVERY_READY`, `MIGRATIONS_READY`, `ETL_READY` e `GC_PASS`.

**Decisão:** caso tudo acima esteja comprovado, registrar `C17=RECOVERY_READY` e liberar o **início da etapa de revisão e aplicação de migrations** na ordem A03→A04→B04→C03, cada qual com leitura pós-aplicação e plano de rollback. **NÃO** alterar `GC=PASS` com base apenas neste C17. O ETL 5/5 e aceite elétrico C13 exigem gates próprios.

## 4. Matriz de produtos entregáveis

| Ordem | Arquivo proposto | Evidência mínima | Gatilho |
|---|---|---|---|
| 01 | `C17_PREVOO_REMOTE.json` | origem/destino, runner gratuito, cofre real e política de retenção, sem segredos | G0 |
| 02 | `scripts/c17_remote_preflight.py` | verificador fail-closed das precondições | G0–G1 |
| 03 | `.github/workflows/sie-c17-recovery-secure.yml` | workflow de execução **protegida**, sem PR/fork e sem atalhos de main | G1, somente ativável após revisão |
| 04 | `scripts/c17_backup_remote.sh` | dump real cifrado antes de custódia e códigos de saída validados | G2–G3 |
| 05 | `scripts/c17_restore_remote.sh` | download do cofre, recuperação em runner B isolado | G4 |
| 06 | `scripts/c17_verify_recovery.py` | schema/Auth/RLS/ACL/extensão e contagens verificados | G4 |
| 07 | `test_c17_*.py` | falhas injetadas e positivos sintéticos, inclusive bloqueio por cofre indisponível | G1/G5 |
| 08 | `C17_BACKUP_MANIFEST_PRIVATE.json` | SHA/horário/escopo/custódia **em meio privado** | G3 |
| 09 | `C17_RECOVERY_EVIDENCE.json` | resultado sanitizado de restore real e divergências | G4 |
| 10 | `C17_SECURITY_VERDICT.json` | auditoria DBA/SRE/SEC e ausência de riscos críticos | G5 |
| 11 | `C17_GATE_HANDOFF.json` | GO/NO-GO fundamentado, referência ao C08 | G6 |

**Observação:** os arquivos acima, salvo este plano, são **artefatos a implementar**, não existentes/executados apenas por constarem da tabela.

## 5. Casos obrigatórios de teste de aceitação

| Caso | Execução | Resultado obrigatório |
|---|---|---|
| REC-01 | Dump sintético + restore em runner B | PASS sem dados reais |
| REC-02 | Destino Supabase diferente do ref esperado | NO-GO antes de conectar |
| REC-03 | TLS inválido / certificado ausente | NO-GO |
| REC-04 | Falha no dump / exit code ≠ 0 | NO-GO; nenhum arquivo considerado válido |
| REC-05 | Falha no cofre externo / permissão ou custo não aprovado | NO-GO antes da migração |
| REC-06 | Cópia remota corrompida ou SHA diferente | NO-GO |
| REC-07 | Restore parcial / role ou extensão ausente | NO-GO + diagnóstico |
| REC-08 | Auth/RLS ou dados críticos diferentes no restore | NO-GO |
| REC-09 | SQL tenta restaurar em endpoint não local ou sobre banco existente | NO-GO |
| REC-10 | PR/fork tenta acessar secrets do banco | NO-GO |
| REC-11 | Algum log/artefato tenta publicar dump, chave, token ou PII | NO-GO |
| REC-12 | Backup real extraído do cofre e restaurado na VM B, com cobertura aprovada | G4 PASS após revisão independente |
| REC-13 | Repetir recuperação com chave/documento persistentes após encerrar VM A | G5 PASS |
| REC-14 | Migration já aplicada, drift de schema ou snapshot envelhecido | NO-GO e novo pré-voo |

**Limite honesto da evidência:** fixture sintética nunca substitui REC-12/REC-13; checks editáveis em JSON nunca equivalem à execução efetiva.

## 6. Fluxo de orquestração segura e tratamento de falhas

1. Repetir automaticamente apenas testes, lint, simulações de falha, implementação de código, auditoria de manifesto e rechecagem de evidências que **não** modificam dados reais.
2. A cada falha: salvar apenas diagnóstico sanitizado, classificar causa, corrigir na branch C, repetir QA do mesmo SHA; rejeitar loops cegos de credenciais e conexões. Bloqueios por cofre não existente, custo, habilitação/Auth ou assinatura **não** podem ser corrigidos por renomear status.
3. Ao atingir `G0–G5=PASS`, realizar revisão independente; não transformar aprovação administrativa dos itens 1 e 2 em prova técnica.
4. Quando `C17=RECOVERY_READY`, devolver controle ao plano do Bloco C para migrations e ETL, com os quatro migrations e 5 projetos já autorizados condicionalmente. Manter `GC=BLOCKED` até homologação E01–E11 e C13 real.

### Papel do titular neste C17

**Sem instalar software, executar `pg_dump` ou restaurar no Windows.** Se e somente se não houver um cofre privado/execução remota confiável já disponível, a equipe deverá indicar a única dependência externa necessária (habilitar uso de armazenamento já existente e o mecanismo de aprovação de secrets **sem compartilhar credenciais no chat**). Não contratar nem inventar infraestrutura. A autorização de execução já está registrada, não repeti-la.

## 7. Evidências de conclusão do PLANO versus conclusão da EXECUÇÃO

**Plano C17:** elaborado, auditável e pronto para ser implementado em branch C.  
**Executor privilegiado:** não verificado nesta elaboração.  
**Cofre remoto privado e persistente:** não identificado/comprovado nesta elaboração.  
**Backup REAL:** não realizado nesta elaboração.  
**Restauração REAL:** não realizada nesta elaboração.  
**Migrations remotas:** A03/A04/B04/C03 não executadas nesta elaboração.  
**GC:** `BLOCKED`.

**Declaração de saída:** é proibido emitir `C17=PASS` ou `GC=PASS` sem prova documental e operacional do dump real, de sua custódia e da restauração independente, com aceites de segurança e recuperação. Este plano não modifica banco remoto nem autoriza custos novos.
