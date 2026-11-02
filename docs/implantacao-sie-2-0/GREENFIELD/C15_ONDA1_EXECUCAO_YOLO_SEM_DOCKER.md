# C15 — Onda 1 YOLO implementada: execução Windows sem Docker Desktop

**Projeto:** SIE 2.0; **branch:** `feat/v201-bloco-c-dominio-eletrico`; **data:** 2026-11-02.

## Agentes especializados e entregas

| Agente (função de execução) | Entrega realizada nesta rodada | Observações |
|---|---|---|
| C15-ARQ | arquitetura nativa e gates GO/NO-GO | `C15_PLANO_IMPLEMENTACAO_SEM_DOCKER_DESKTOP_V201.md` |
| C15-DBA | pré-voo, dump e restore PostgreSQL nativo | `scripts/c15_native_common.ps1`, `c15_preflight_windows.ps1`, `c15_backup_native.ps1`, `c15_restore_native.ps1` |
| C15-SECOPS | endpoint de destino obrigatório, TLS validado e sigilo das credenciais | `Assert-C15Remote`, `Assert-C15Local`; nenhuma escrita remota |
| C15-INTEGRIDADE | SHA256, verificação de manifestos e prova documental de restauração | `scripts/c15_integrity.py` |
| C15-QA | cenários positivos/negativos com fixtures sintéticas, CI e parser PowerShell | `test_c15_native_backup_restore_v201.py` e workflow de API |
| C15-AUDITOR | rejeitar PASS artificial e evidência incompleta | checks obrigatórios, modo sintético sempre `NO_GO` |

**Limite de agência:** papéis especializados desempenhados nesta implementação por análise, código e testes; não foram iniciadas instâncias humanas autônomas, nem foi acessado o computador Windows do titular.

## Pacote entregue

- `scripts/c15_native_common.ps1`: valida versão 17+ dos executáveis, recusa outra referência Supabase, recusa caminhos OneDrive/Git, exige `PGSSLMODE=verify-full`/CA/PGPASSFILE, e limita restauração a `127.0.0.1`.
- `scripts/c15_preflight_windows.ps1`: identifica ferramentas e PostgreSQL local, sem conectar ao banco remoto.
- `scripts/c15_backup_native.ps1`: `pg_dump --format=custom` do projeto real de pré-produção, inventário sintético de contagens, SHA256 e `manifest.json` privado. **Não executado contra Supabase real nesta rodada**.
- `scripts/c15_restore_native.ps1`: verifica SHA/identidade, exige banco **novo** `c15_*` em loopback, executa `createdb`/`pg_restore --exit-on-error --single-transaction`, compara seis contagens. Ainda exige revisão independente de roles, ACL, extensões e serviços Supabase; não libera DDL automaticamente.
- `scripts/c15_integrity.py`: gera fixture sintética offline, simula tentativa de “GO” indevido, rejeita hash/tamanho divergentes e exporta resultado de prova.
- `restructuring/apps/api/tests/test_c15_native_backup_restore_v201.py`: testes negativos de integridade, identidade, adulteração e bloqueio de gate, executados via `pytest` do projeto.

**O CI da API executa o verificador sintético, os testes unitários e analisa a sintaxe de todos os scripts PowerShell.** A execução offline é determinística e deliberadamente não produz backup real nem equivalência completa de Supabase.

## Como executar no Windows nativo — somente após revisar os scripts

1. Instalar PostgreSQL 17 nativo (cliente `psql`, `pg_dump`, `pg_restore`, `createdb`, serviço PostgreSQL **local**), Python 3.12 e PowerShell 7. Não instalar Docker Desktop.
2. Configurar PostgreSQL local para conexão em `127.0.0.1` e uma porta definida (padrão C15: 55432; é possível escolher 5432 informando a porta).
3. Baixar **apenas os scripts** da branch C do GitHub e conferir os arquivos antes de executar; mantê-los fora da pasta que contém dumps.
4. Rodar pré-voo:
   ```powershell
   pwsh -File .\scripts\c15_preflight_windows.ps1 -LocalPort 5432
   ```
5. No Supabase Dashboard do SIE 2.0, abrir **Connect**, copiar o host do banco direto, se houver IPv6 disponível, ou o **Session pooler (porta 5432)** para rede IPv4. Copiar o nome de usuário correspondente e obter o certificado CA de validação TLS. Não adivinhar host, região, usuário ou senha.
6. Configurar **localmente** `PGSSLMODE=verify-full`, `PGSSLROOTCERT` apontando ao CA e `PGPASSFILE` apontando a arquivo confidencial com ACL restritiva. Não registrar senha em histórico do PowerShell, URL de conexão ou script.
7. Executar exportação apenas do destino SIE 2.0 (substituir os parâmetros por valores exatos do Dashboard):
   ```powershell
   pwsh -File .\scripts\c15_backup_native.ps1 -RemoteHost "HOST_OFICIAL_DASHBOARD" -RemoteUser "USUARIO_OFICIAL_DASHBOARD"
   ```
8. Verificar o `manifest.json` e o dump `sie2_full_database.backup` guardados na pasta privada. **Não publicar nem enviar o dump**, TOC, segredos ou registro Auth.
9. Executar a prova de restauração em PostgreSQL **local descartável**, com usuário e autenticação próprios, após verificar que o banco `c15_target_restore` **NÃO existe**:
   ```powershell
   pwsh -File .\scripts\c15_restore_native.ps1 -ManifestPath "CAMINHO_PRIVADO\manifest.json" -BackupPath "CAMINHO_PRIVADO\sie2_full_database.backup" -LocalPort 5432
   ```
10. Se a restauração exigir roles internas, extensões ou privilégios inexistentes, **não forçar** `--no-owner` nem `--no-acl` para fabricar equivalência. Registrar erros de forma sanitizada e manter o gate bloqueado até preparar clone/roles locais equivalentes e demonstrar os serviços críticos.
11. Encaminhar somente o `manifest.json` saneado e o **resultado agregado** de restauração, sem dados pessoais.

## Restrições e gates ativos

- O dump `pg_dump` nativo completo pode incluir tabelas `auth`/`storage`, mas não leva, por si só, senhas globais de roles nem objetos binários de Storage e não recria serviços de Auth/Edge. Toda capacidade de recuperação essencial precisa de prova; sucesso parcial **não autoriza migrations**.
- O CI usa PostgreSQL descartável no runner remoto GitHub; **não** exige Docker Desktop instalado na máquina Windows do usuário. Caso se proíba qualquer contêiner também no CI, isso exigirá alterar especificamente os workflows existentes.
- O backup do **destino** é um gate próprio; o backup somente leitura da **origem** é outro. O ETL atual `v201_c_etl.py` permanece deliberadamente `SYNTHETIC_TEST`; não tratar os cinco projetos como migrados.
- Orquestração após evidência real: restaurar e auditar dados → revisar segurança e schema → aplicar migrations A03/A04/B04/C03 no SIE2 → validar identidade Auth, origem, ETL real e cópias 5/5 → contraprovas elétricas E01–E11 → decisão C13 → `GC=PASS` somente com todos os requisitos demonstrados.
- `main`, F12, SIE original, fonte legada, produção, dados pessoais e custos adicionais permanecem protegidos.
