# C15 — PLANO EXECUTIVO DE IMPLEMENTAÇÃO DO SIE 2.0 SEM DOCKER DESKTOP

**Versão:** 1.0 | **Diagnóstico:** 2026-11-02 | **Projeto:** SIE 2.0 / Bloco C / GC  
**Repositório e branch:** `SFPTechnology/Projeto-SIE-2.0` / `feat/v201-bloco-c-dominio-eletrico`  
**Baseline verificada:** `f2c2db9dec1804ed3ccb1b79424018d376363256` (pré-plano)  
**Destino pré-produção:** Supabase `fozrymsidnaxmuvxxfhh` / PostgreSQL 17.11  
**Origem, exclusivamente leitura:** Supabase `hlbksclcandbsyqrsbmx` / repositório original `SFPTechnology/Projeto-SIE`.  
**Restrições inegociáveis:** nenhuma instalação do Docker Desktop no Windows; nenhum custo adicional; sem alterações em `main`, F12, SIE original, dados da origem, Hostinger ou produção; sem merge/deploy; sem comprometer credenciais/dumps no GitHub ou no chat. O **GC permanece BLOCKED** até evidências efetivas.

> **Escopo:** este documento é um plano pronto para implementação, **não é execução de backup, restore, DDL remoto ou ETL real**. A autorização do titular, em 2026-11-02, é CONDICIONAL: A03/A04/B04/C03 e cópias dos cinco projetos somente após backup REAL do destino, restauração validada e revisão de segurança; a importação exige adicionalmente corte e backup da origem e identidade Auth comprovada. Não solicitar novamente a mesma autorização quando as condições se materializarem; documentar cada gate e interromper diante de falhas.

## 1 — Análise técnica do sistema existente

| Camada | Evidência concreta observada | Implicação |
|---|---|---|
| API | `restructuring/apps/api/sie_api/main.py`, Python/FastAPI; autenticação e persistência desenvolvidas parcialmente | Não depende de Docker Desktop |
| Cálculos | `v201_c_calculation.py`, `v201_c_explicit_checks.py` e testes E01–E11 | Matemática/guardas verificadas; norma e parecer continuam pendentes |
| Dados locais | `v201_dev_store.py` (SQLite) e `v201_pg_dev_adapter.py` (PG17 descartável CI-only) | Adaptador descartável não deve ser redirecionado ao Supabase remoto |
| ETL | `v201_c_etl.py` rejeita `REAL_LEGACY` e aceita somente `SYNTHETIC_TEST` | Importador real, com mapeamento governado, ainda precisa ser desenvolvido |
| Migrations | `20261028102000` (A03), `20261028102100` (A04), `20261028153000` (B04), `20261028203000` (C03) | Arquivos prontos e testados em PG17 isolado; aplicação remota ainda não ocorreu |
| Destino real | Leitura de 2026-11-02: 9 tabelas públicas, 63 colunas públicas, 16 políticas RLS; 1 `auth.users`, 0 `auth.sessions`, 0 projetos/revisões | Somente GF02 `20261027195557` remotamente aplicada; falta verificação de sessão real |
| Fonte real | Último inventário: 5 projetos, 41 ambientes, 52 cargas adicionais, 1.805 eventos, 1.934 registros no conjunto de 15 tabelas | Contagens são históricas; a consulta mais recente à origem falhou por timeout |
| Semântica | 99 colunas inventariadas; 45 campos adicionais classificados, sete aguardando parecer elétrico e um mapeamento de apresentação pendente | Preservar bruto, nunca completar informações faltantes com suposições |
| QA | Cinco workflows PASS em SHA `f2c2db9d...` antes da integração real; C03 já prova backup/restore de PG17 **sintético** | CI descartável não substitui backup/restauração real do Supabase |
| Backup antigo | `scripts/c14_backup_preprod_sie2.ps1` usa `supabase db dump` e `docker`; `C14_PREVOO_BACKUP_RESTORE_PREPROD_20261102.md` prescreve stack Docker | **Não executar C14 no fluxo sem Docker Desktop**. Criar C15 nativo |
| Autorização | `C08_CONTRATO_ENTREGA_C_V201.json`: autorização condicional registrada | Manter `migration_application_permitted_now=false` até prova de restauração |

**Conclusão arquitetural:** conservar o Supabase atual (Free) como pré-produção; utilizar **PostgreSQL 17 nativo** e PowerShell no Windows para exportar, restaurar e ensaiar; utilizar Supabase MCP para consultar/aplicar migrations remotamente **somente depois do GO**. Nada exige executar o backend elétrico em Docker.

## 2 — Arquitetura-alvo sem Docker Desktop

```text
Supabase LEGADO (somente SELECT / dump nativo)
  hlbksclcandbsyqrsbmx
        |
        | TLS, pg_dump nativo PostgreSQL 17, cópia privada cifrada
        v
Windows + PostgreSQL 17 NATIVO (localhost, porta local dedicada)
  c15_source_restore     c15_target_restore
  ensaio ETL e hashes    prova de backup e rollback
        |                     ^
        |                     | TLS, pg_dump nativo (não usar supabase db dump)
        |                     |
        +---------------- Supabase SIE 2.0 PRÉ-PRODUÇÃO
                             fozrymsidnaxmuvxxfhh
                             A03 -> A04 -> B04 -> C03
                             somente após GO de backup/restore
                             ETL real somente após GO de identidade/corte
```

**Não instalar ou invocar:** `Docker Desktop`, `docker`, `supabase start`, `supabase db dump`, `supabase db reset`, `supabase db pull` nem `supabase db push` no caminho C15 nativo. Os workflows atuais do GitHub podem usar serviços descartáveis no **runner remoto**, o que não instala Docker Desktop no Windows; se a exigência for *zero containers inclusive no CI*, abrir tarefa própria de substituir o serviço PG17 por PostgreSQL instalado nativamente no runner, sem relaxar seus gates.

### Requisitos e segurança do computador Windows

- **PostgreSQL 17 nativo para Windows**: executáveis `pg_dump`, `pg_restore`, `psql`, `pg_isready`, `createdb`, servidor local e pgAdmin opcional. Link: https://www.postgresql.org/download/windows/ .
- Python 3.12 para as ferramentas de validação e ETL, com dependências do projeto fixadas. PowerShell 5.1+ ou PowerShell 7; preferir PowerShell 7 para scripts robustos.
- PostgreSQL local em interface loopback, porta não conflitante (ex. `55432`), autenticação forte, firewall sem exposição à rede, cluster/local `c15_homologacao` isolado de outras bases.
- Destino Supabase com conexão **TLS validada** (`sslmode=verify-full` e certificado CA confiável). Usar conexão direta para comandos PostgreSQL nativos quando IPv6 estiver disponível; em rede somente IPv4 avaliar o **session pooler**, nunca adivinhar hostname/região ou usar transaction pooler para o fluxo sem verificar compatibilidade.
- Credenciais: `PGPASSFILE` em pasta privada protegida pelo Windows, controle estrito de ACL e remoção depois do teste; **não** usar senhas em linha de comando, URLs coladas em logs ou commits; preferir cofre de segredos já disponível.
- Backups em disco local criptografado, fora de Git, OneDrive sincronizado, pastas web e artefatos públicos do CI. **Nunca enviar `auth.users` ou dumps ao GitHub/chat**.

Fontes: https://www.postgresql.org/docs/17/app-pgdump.html ; https://www.postgresql.org/docs/17/app-pgrestore.html ; https://supabase.com/docs/guides/database/connecting-to-postgres ; https://supabase.com/docs/guides/database/psql .

## 3 — Agentes especializados (funções lógicas)

| Agente | Especialidade | Entrega obrigatória e independência |
|---|---|---|
| A-C15-01 — Arquiteto/Orquestrador | arquitetura, contratos, gates, custo zero | checklist G0–G7, congelamento do SHA, C08/C15 sincronizados, nenhum GO fictício |
| A-C15-02 — DBA Backup | PostgreSQL 17 Windows, SSL, pg_dump, pg_restore | backup real destino+origem, SHA256, restauração local, prova sem erros e rollback |
| A-C15-03 — SecOps/Auth | Supabase Auth, RLS, ACL, isolamento A/B, segredos | sessão real, vínculo 5/5, testes negativos, secrets nunca expostos |
| A-C15-04 — Engenheiro de Migração | modelos/ETL, 15 tabelas/99 colunas, provenance, idempotência | importador real fail-closed, 1.934 registros reconciliados, nenhum campo perdido |
| A-C15-05 — Engenheiro Elétrico | NBR/EDP, P03/P06, E01–E11, cálculos independentes | contraprovas normativas e lista para parecer do responsável CREA-SP; sem assinatura fictícia |
| A-C15-06 — QA e Confiabilidade | pytest, PG17, CI, backup/restore, rollback | log de execuções e testes, falhas injetadas, cinco workflows PASS mesmo SHA |
| A-C15-07 — Auditor Independente | verificação de evidências, normas, hashes, controles de autorização | GO/NO-GO fundamentado; rejeita qualquer aprovação com evidência incompleta |

Agentes são papéis de execução e revisão; nenhum substitui a manifestação de aceite profissional nem cria acesso ao computador Windows por si só.

## 4 — Plano técnico de implementação e critérios de aceite

### Fase C15-00 — Inventário e congelamento (gate G0)

**Tarefas:** conferir PR #11/branch/SHA; inventariar scripts, modelos, migradores, schemas, versões das ferramentas, privilégios do conector e estado do Auth; reproduzir SELECTs no destino e comparar com baseline: 9 tabelas, 63 colunas, 16 RLS, 1 usuário, 0 projetos/revisões. Conferir advisor de segurança (proteção de senhas vazadas atualmente WARN). Verificar que nenhuma aplicação ou terceiro já usa o projeto em produção. **Não alterar banco.**

**Entrega:** `C15_G0_BASELINE.json` sem dados privados, hash SHA256 de schema/migrations e matriz de riscos. **GO:** fonte correta, destino correto, baseline reconciliado, custo zero, Auth e RLS sem bloqueio conhecido. Se houver deriva, revisar antes de prosseguir.

### Fase C15-01 — Instalador e ferramentas Windows nativas (gate G1)

**Implementar:** `scripts/c15_preflight_windows.ps1` que faça:
1. `Get-Command pg_dump,pg_restore,psql,pg_isready,createdb,python` e `--version`; exigir cliente PostgreSQL 17 ou superior compatível com servidor 17.
2. Validar diretório privado/ACL/criptografia/armazenamento; recusar Git e caminhos sincronizados.
3. Validar serviço PostgreSQL local e conexão **somente loopback** na porta dedicada; identificar banco local antes de qualquer restore.
4. Validar endereço/usuário/conexão do destino com o Dashboard Supabase via `psql` read-only, SSL `verify-full`; não aceitar mudança silenciosa entre origem e destino.
5. Exibir apenas status e metadados; **nunca exibir credenciais, conexões com senha, dados de usuário ou SQL bruto**.

**Entrega:** `C15_PREFLIGHT_WINDOWS.json` (somente status/sumários); sem Docker nem Supabase CLI obrigatório. **GO:** ferramentas funcionais, TLS validado, base local inequívoca e segredos protegidos.

### Fase C15-02 — BACKUP REAL do Supabase SIE 2.0 (gate G2A)

**Implementar:** `scripts/c15_backup_native.ps1`, com destino pré-produção **hard-coded como referência validada**, sem host/credenciais hard-coded. Usar **`pg_dump` nativo em formato custom `-Fc`** para exportação consistente; exportar no mínimo `public` e o inventário/dependências dos esquemas gerenciados relevantes `auth` e `storage`. **Preferir dump integral do banco quando os privilégios permitirem**, preservando um arquivo original completo; os dumps parciais são **complementares** e não devem ser apresentados como backup completo.

**Importante:** `pg_dump` sozinho não exporta roles globais nem todos os recursos externos. Verificar permissões e possibilidade de coletar metadados das roles sem escalar privilégios (`pg_dumpall --globals-only` pode falhar no Supabase gerenciado). Inventariar Storage *objetos físicos*, Edge Functions, Auth settings, extensões e secrets como itens externos ao backup PostgreSQL; se houver conteúdo indispensável fora do banco, criar exportação/recuperação protegida específica. **Não alterar roles `supabase_auth_admin` ou `supabase_storage_admin` no remoto.**

**Padrão de operação ilustrativo (após configurar PGHOST, PGPORT, PGUSER, PGDATABASE, PGSSLMODE, PGSSLROOTCERT e PGPASSFILE em sessão segura):**
```powershell
pg_dump --format=custom --file="$env:LOCALAPPDATA\SIE2_BACKUPS_PRIVADOS\sie2_preprod.backup" --dbname=postgres
pg_restore --list "$env:LOCALAPPDATA\SIE2_BACKUPS_PRIVADOS\sie2_preprod.backup"
Get-FileHash "$env:LOCALAPPDATA\SIE2_BACKUPS_PRIVADOS\sie2_preprod.backup" -Algorithm SHA256
```
*Este exemplo é **referência de comando**, não script liberado: a implementação deve exigir pasta privada existente, arquivo não sobrescrito, identidade do endpoint, código de saída zero, TLS validado e logs seguros. Nunca executar `pg_dump` apontando para origem quando a intenção é destino.*

**Entrega:** dump original cifrado + `C15_TARGET_BACKUP_MANIFEST.json` com SHA256, timestamps UTC, cobertura por schema/tabela, status das roles/objetos externos, sem conteúdo de linhas. **NO-GO:** `pg_dump` falha, tabela imprescindível ausente, dump parcial confundido com integral, extensão/objeto obrigatório sem rota de recuperação, qualquer credencial em log.

### Fase C15-03 — Restauração nativa e prova de recuperação (gate G2B)

**Implementar:** `scripts/c15_restore_native.ps1` e `scripts/c15_verify_restore.py`.

1. Criar banco **local descartável e vazio** (`c15_target_restore`) no PostgreSQL 17 Windows; host explicitamente `127.0.0.1`, porta dedicada; recusar host remoto, host proxy ou alvo já existente.
2. Validar hash SHA256 dos arquivos antes de restaurar e ler sumário com `pg_restore --list`.
3. Restaurar com `pg_restore --exit-on-error --single-transaction` (quando compatível), capturar código de saída real; no clone local, preparar apenas roles/extensões estritamente necessárias e registrar diferenças de proprietários/ACL. Usar `--no-owner`/`--no-acl` **somente com justificativa** e verificar separadamente que políticas RLS/GRANT originais estão preservadas pela evidência.
4. Confrontar inventário de esquemas/tabelas/colunas/FKs/índices/funções/triggers, 16 políticas RLS, 1 usuário Auth (sem imprimir credenciais), 0 projetos/revisões e checksums compatíveis com backup original. Inspecionar erros específicos de `auth`, `storage`, extensões e permissões.
5. Ensaiar restauração novamente em **segundo banco local vazio** ou reconstrução controlada; nunca rodar `DROP` no remoto.
6. Deixar claro que restore em PostgreSQL puro **não é restauração end-to-end de todos os serviços Supabase**. A cobertura exigida para rollback deve ser comprovada; se Auth/Storage/serviço crítico não puder ser reproduzido fielmente, `G2B=BLOCKED`, sem DDL no destino.

**Entrega:** `C15_TARGET_RESTORE_EVIDENCE.json` com `restore_status`, SHA de backup, versão, matriz de cobertura, contagens e divergências; referência a execução local, nenhuma credencial. **GO:** recuperação de todas as estruturas/dados críticos do escopo e RLS comprovada sem erros impeditivos; caso contrário BLOCKED e replanejar sem burlar a autorização.

### Fase C15-04 — Backup e corte consistente da ORIGEM (gate G3)

**Tarefas:** acesso apenas de leitura ao `hlbksclcandbsyqrsbmx` via PostgreSQL nativo; resolver timeout de conectividade com conexões/certificados oficiais antes de tentar dump. Fazer dump privado consistente das **15 tabelas** e histórico; verificar novamente 5 projetos, 41 ambientes, 52 cargas adicionais, 1.805 eventos e total de 1.934 registros **somente se os valores atuais confirmarem**. Restaurar em `c15_source_restore` local para validar integridade e calcular hashes e somatórios por tabela e projeto. Documentar momento de corte e deriva. Se fonte mudou, conservar as contagens atuais e abrir reconciliação, não ajustar artificialmente dados.

**Entrega:** `C15_SOURCE_CUTOFF_MANIFEST.json`, `C15_SOURCE_RESTORE_EVIDENCE.json`, dumps privados protegidos. **GO:** todos os registros legados incluídos, exportação consistente, sem perda/alteração da origem, 10 referências históricas órfãs preservadas.

### Fase C15-05 — Identidade Auth, campos e ETL real (gate G4)

**Implementar componentes NOVOS, isolados do importador sintético:** `v201_c_etl_real.py`, `v201_c_real_mapping.py`, `v201_c_remote_adapter.py` (nomes propostos); contratos de provenance e ledger por `source_project_id/source_row_id/source_hash`.

1. Provar **login efetivo no SIE 2.0**, sujeito JWT Supabase verificado pelo backend e vinculado à conta Auth existente. O simples cadastro em `auth.users` não basta. Conferir titularidade independente dos cinco IDs selecionados; proibir derivar autorização de `autor` legado ou `user_metadata`.
2. Revisar 99 colunas e a disposição de 45 campos; sete elétricos e um mapeamento de exibição aguardam decisão. Preservar integralmente a versão bruta dos itens sem transformação aprovada, com hash e referência; não gerar valores elétricos inexistentes.
3. Suportar nulos de tensão em quatro cargas, dois registros trifásicos com topologia não validada, 41 alturas zeradas e dez eventos de auditoria órfãos **sem perdas ou correções automáticas**.
4. Transformar dados da restauração local de origem com UUID determinístico/remap auditável, transações curtas, ledger de idempotência, staging lógico e regra `NOT_EVALUATED` para resultados elétricos antigos; preservar todas as 15 tabelas via modelo canônico ou arquivo bruto governado.
5. Executar ensaio inteiramente local: normal → retry → falha injetada → rollback → reprocessamento idempotente → comparação de contagens/hashes. O adaptador CI-only existente continua proibido para remoto.
6. Suportar destino remoto **apenas após G2A/G2B/G3/G4**, com configuração de conexão permitida explicitamente, autenticação confiável e tokens de servidor jamais enviados ao browser.

**Entrega:** `C15_REAL_ETL_DRYRUN.json`, matriz 99/99, 5/5 IDs de origem ligados a UID Auth verificado, e evidência de atomicidade. **NO-GO:** qualquer campo perdido, usuário não comprovado, dados eletricamente inferidos ou discrepância de hash sem explicação.

### Fase C15-06 — Aplicar migrations no Supabase EXISTENTE (gate G5)

**Dependências cumulativas:** G0/G1/G2A/G2B, revisão SecOps/RLS, registro de SHA das quatro SQL, correspondência exata com manifesto, confirmações de condição pré-produção e custo zero. O usuário **já autorizou condicionalmente**, não pedir autorização genérica novamente; registrar evidência do cumprimento das condições.

**Execução remota:** ferramenta Supabase `apply_migration`, **uma por vez**, sem Supabase CLI e sem Docker. Ordem:
1. `20261028102000_sie_a03_indexes_v201.sql`;
2. `20261028102100_sie_a04_revision_lifecycle_v201.sql`;
3. `20261028153000_sie_b04_idempotency_backend_grants_v201.sql`;
4. `20261028203000_sie_c03_electrical_domain_v201.sql`.

Após cada migration: consultar `supabase_migrations.schema_migrations`, confirmar invariantes/índices/constraints/funções/GRANT/RLS e verificar operações de criação, revisão, snapshot, imutabilidade e segurança. **Parar na primeira falha**; diagnosticar e planejar restauração/remediação a partir do backup verificável, sem executar `db reset` remoto. `GC` e `C13` permanecem independentes.

**Entrega:** `C15_REMOTE_MIGRATION_READBACK.json` por versão, inventário de schema pós-aplicação, logs com segredo mascarado, sumário dos testes A/B.

### Fase C15-07 — Importar cinco projetos de forma controlada (gate G6)

**Dependências adicionais:** G3 (origem), G4 (Auth/ETL e mapeamento), G5 (schema); backup/restauração real mantidos. Importar **cópias**, nunca mover ou apagar a fonte. Executar uma primeira importação por projeto com batch ledger, owner real validado, transação idempotente e capacidade de reverter inserções controladas. Conferir 5/5 projetos, 41/52/1.805 históricos ou os novos totais validados no cutoff, além do total de 15 tabelas / 99 colunas e referências preservadas; contar *por tabela* para evitar falso positivo em somatório. Auditar resultados antigos como não avaliados.

Executar ataques negativos: identidade B acessando A (403/404); alteração de owner; replay com payload divergente; duplicação; DELETE em revisão selada; interrupção de lote; restart/retry; quebra de hash; downgrade de regra normativa; sessão expirada. Nenhum comando de ETL deve alterar o projeto original.

**Entrega:** `C15_REAL_MIGRATION_RECONCILIATION.json`, tabela de contagens e hashes de cada projeto, catálogo de exceções, prova de rollback, QA Auth/RLS.

### Fase C15-08 — Engenharia elétrica, aceite e encerramento (gate G7)

- Realizar contraprovas normativas E01–E11 com edição/fonte oficial aplicável e testes de fronteira. O relatório sintético C12 atual não homologa mínimos de iluminação/TUG, DR/DPS, aterramento, corrente I2, concessionária etc.
- Validar certidões CREA-SP/atribuições atuais e enquadramento de ART quando cabível; responsável habilitado revisa evidências e **decide** no C13, sem assinatura automática.
- Reexecutar todos os workflows no SHA final e mais QA remoto de integração A/B/restore/ETL; evidência de testes sintéticos não equivale a login real nem homologação técnica.
- Atualizar C08 para `GC=PASS` **somente** quando G0–G7 estiverem PASS com evidência verificável e aceite profissional válido. Handoff e merge para a branch B são atos posteriores e controlados; implantação em produção exige gate próprio.

## 5 — Matriz de execução e bloqueio

| ID | Gate | Dependências | Evidência para PASS | Estado inicial |
|---|---|---|---|---|
| C15-00 | Baseline | — | inventário/CI/SHA/RLS readback | PARCIAL |
| C15-01 | Ferramentas nativas | C15-00 | `pg_dump/pg_restore/psql` 17, TLS e servidor local | NÃO EXECUTADO |
| C15-02 | Dump do destino | C15-01 | arquivo real, SHA, cobertura, sem secrets | BLOQUEADO |
| C15-03 | Restore do destino | C15-02 | restauração local fiel e repetida | BLOQUEADO |
| C15-04 | Backup/corte da origem | C15-01 | dump fonte e reconciliação em restore | BLOQUEADO (timeout) |
| C15-05 | ETL real + Auth | C15-04 | 99/99 e ensaio 5/5 com UID verificável | NÃO IMPLEMENTADO |
| C15-06 | Migrations remotas | C15-03 + segurança | 4 versões aplicadas e comprovadas | AUTORIZAÇÃO CONDICIONAL; NÃO EXECUTADO |
| C15-07 | Importação real | C15-04/05/06 | 5/5 projetos, contagens/hashes, BOLA negado | BLOQUEADO |
| C15-08 | Engenharia + GC | C15-07 + normas | C12/C13, CI, decisões e C08 válidos | BLOQUEADO |

## 6 — Pacote de implementação que a equipe deve entregar

**Scripts a criar (ainda NÃO existem):**
- `scripts/c15_preflight_windows.ps1`: ferramentas, endpoint, TLS, diretório protegido, conexão local.
- `scripts/c15_backup_native.ps1`: `pg_dump` nativo, validação de cobertura e manifesto SHA256 de destino e origem em perfis segregados.
- `scripts/c15_restore_native.ps1`: `pg_restore` nativo, banco local descartável e barreira de host/porta.
- `scripts/c15_verify_restore.py`: teste estruturado da restauração e comparação de schemas, dados, Auth/RLS.
- `restructuring/apps/api/sie_api/v201_c_etl_real.py`: ETL real governado, read-only origem, idempotência/provenance.
- `restructuring/apps/api/tests/test_c15_*.py`: negativos, isolamento A/B, corrupção de hash, backup incompleto, restore interrompido, replay, rollback e 5 projetos.
- `docs/implantacao-sie-2-0/GREENFIELD/C15_*.json`: manifests sanitizados, status GO/NO-GO e evidências assináveis.

**Alterar somente na branch C:** scripts, testes, documentação/contratos e, após os gates, as migrations **no destino pré-produção já autorizado**. **Não modificar** C14 de forma que oculte seu uso de Docker: C15 é o novo caminho selecionado e o anterior passa a ser legado/inaplicável para este cenário.

## 7 — Critérios de rejeição imediata e política de recuperação

- Falha de dump ou impossibilidade de restaurar Auth/Storage/ACL/extensões necessários → `BACKUP_RESTORE_BLOCKED`.
- Falta de certificado TLS verificável, origem com timeout, export sem snapshot consistente ou hash divergente → `SOURCE_CUTOFF_BLOCKED`.
- Tentativa de `pg_restore` em endereço remoto, porta não local ou banco não descartável → abortar **antes de conectar**.
- Credencial, token, dump ou arquivo com dados pessoais em GitHub/CI público → interromper, revogar credenciais comprometidas e excluir artefato por procedimento próprio.
- Auth sem login real/titularidade comprovada → `OWNER_BINDING_BLOCKED`.
- Norma/tabela elétrica sem fonte homologada, DR/DPS/aterramento não implementados ou contraprova falha → `NORMATIVE_REVIEW_REQUIRED`; proibir conformidade fictícia.
- Falha em migration ou importação → parar, capturar diagnóstico, reavaliar backup e realizar reversão **somente contra o destino pré-produção** em procedimento controlado.
- Qualquer custo adicional, criação de projeto/branch paga, alteração em origem, `main`, F12 ou produção → **STOP**.

## 8 — Sequência sugerida de trabalho e primeira frente liberada

**Onda 1 — imediata, sem SQL remoto:** implementar C15-00, C15-01, C15-02 (script), C15-03 (script e testes) e configurar o ambiente Windows nativo; testar com dados sintéticos. Incluir auditoria independente de export/import, error handling e scripts assinados/verificáveis.

**Onda 2 — somente após execução local pelo operador:** realizar dump REAL do destino e restore REAL, comprovar os dois; em paralelo resolver timeout da origem e completar mapeamento/identidade Auth. Não afirmar G2B=PASS por teste sintético.

**Onda 3 — após gates satisfeitos:** aplicar A03/A04/B04/C03 via Supabase MCP, executar readbacks e segurança; migrar as cinco cópias com ETL real e reconciliação.

**Onda 4 — fechamento técnico:** E01–E11 normativos, aceite humano C13, CI final, auditoria e `GC=PASS` quando todos os requisitos forem atendidos.

### Resultado efetivo deste documento

**Somente planejamento e inventário de leitura:** migrations remotas **não aplicadas**, backup real **não realizado**, ETL real **não executado**, GC **BLOCKED**. O uso de PostgreSQL 17 nativo substitui integralmente a necessidade de Docker Desktop para o procedimento Windows; não torna uma restauração incompleta automaticamente aceitável.
