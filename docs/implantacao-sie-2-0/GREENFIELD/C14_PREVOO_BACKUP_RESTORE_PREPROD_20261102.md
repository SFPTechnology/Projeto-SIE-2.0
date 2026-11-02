# C14 — Pré-voo da homologação remota do Bloco C (SIE 2.0)

**Data:** 2026-11-02. **Status do gate de execução:** `BLOCKED_BACKUP_RESTORE_REAL_NOT_PROVEN`.
**Ambiente:** `fozrymsidnaxmuvxxfhh` — declarado pelo proprietário como **pré-produção, não produção**.
**Escopo autorizado em 2026-11-02:** aplicar A03/A04/B04/C03 e importar cópias dos cinco projetos **somente após** backup real, restauração comprovada e verificações de segurança. Sem custos adicionais e sem tocar SIE original, `main`, F12 ou produção.
**Não equivale a GO incondicional para DDL.** Nenhuma aplicação remota pode preceder os gates estabelecidos nesta autorização.

## 1. Constatações verificadas por leituras remotas

- Destino ativo PostgreSQL 17.11: 1 `auth.users`, 0 `auth.sessions`, 0 projetos e 0 revisões.
- Schema `public`: 9 tabelas, 63 colunas, 16 políticas RLS. Contagem e estrutura sujeitas a novo readback antes do DDL.
- Hash MD5 determinístico **de inventário de colunas**: `3612115882486c8dfda17b688196a8de`; hash MD5 **de nomes/roles/comandos das políticas**: `c7e7439d0d751f400d7c740762066555`. São apenas *indicadores de deriva*, **não backups e não provas criptográficas de integridade de dados**.
- Histórico remoto: **somente** `20261027195557` (GF02). Pendentes `20261028102000`, `20261028102100`, `20261028153000`, `20261028203000`.
- CI no SHA `007ea24b26b0f7f4b5dcfeb773c86521f7181a15`: cinco workflows `SUCCESS`; C03 testou backup+restore de *PostgreSQL descartável com dados sintéticos*, **não** o Supabase de destino.
- Aviso de segurança de Auth: `auth_leaked_password_protection` desativado, severidade WARN. Avaliar correção/limitações do plano antes do uso real: https://supabase.com/docs/guides/auth/password-security#password-strength-and-leaked-password-protection .
- Projeto de origem `hlbksclcandbsyqrsbmx`: leituras atuais por conector falharam por timeout; as contagens históricas 5 projetos/1.934 registros **não** comprovam o estado atual nem corte transacional.

## 2. Gerar backup REAL do destino (Windows, usuário local)

### Pré-requisitos
1. No computador confiável do titular, instalar **Docker Desktop** e **Supabase CLI**, conforme https://supabase.com/docs/guides/local-development/cli/getting-started .
2. Autenticar na CLI com `supabase login` (**nunca enviar token, conexão, senha nem SQL dump ao chat ou GitHub**).
3. Baixar este repositório/branch ou obter o script `scripts/c14_backup_preprod_sie2.ps1` e revisar seu conteúdo.
4. Guardar backups em disco privado local protegido (BitLocker/criptografia adequada), **fora de OneDrive público, Git, repositório e pastas compartilhadas**.

No Windows PowerShell, executar (ajustar o caminho para o arquivo baixado):
```powershell
supabase --version
docker info
supabase login
& ".\scripts\c14_backup_preprod_sie2.ps1"
```

O script faz `supabase init` num contexto temporário e `supabase link --project-ref fozrymsidnaxmuvxxfhh`, solicitando credencial apenas localmente. Depois usa **somente** os comandos oficiais de leitura:
```bash
supabase db dump -f roles.sql --role-only
supabase db dump -f schema.sql
supabase db dump -f data.sql --use-copy --data-only -x storage.buckets_vectors -x storage.vector_indexes
```
(Executados em contexto da CLI já vinculado ao projeto correto; os caminhos reais são privados e distintos.)

**Artefato gerado:** diretório local `SIE2_BACKUPS_PRIVADOS/SIE2_C14_...` com `roles.sql`, `schema.sql`, `data.sql`, `manifest.json` contendo tamanhos e SHA256. O campo `restore_state=NOT_VERIFIED` é proposital e **não pode ser alterado manualmente para sinalizar aprovação**.

Fonte oficial: https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore e https://supabase.com/docs/guides/platform/backups .

### Critério de autenticidade do dump

- A CLI deve informar êxito nas três exportações, sem erros/truncamento.
- Comparar `Get-FileHash -Algorithm SHA256` de cada arquivo com os valores do manifesto.
- Conferir referência de destino correta, data, os 9 objetos públicos e `auth.users` incluído no dump de dados, observadas as filtragens oficiais da CLI.
- **Não colocar `data.sql` em anexos/chats**: pode conter credenciais derivadas e informações pessoais. Sem criptografia/guarda restrita: **BLOCKED**.

## 3. Teste de restauração — obrigatório e separado do Supabase

1. Provisionar stack **local descartável** Supabase/Docker, em diretório novo, conforme CLI oficial (não reutilizar o diretório de projeto conectado ao Supabase remoto).
2. Restaurar **no banco LOCAL** roles, schema e data seguindo o procedimento da documentação da Supabase, usando `psql --single-transaction --variable ON_ERROR_STOP=1`. Confirmar antes da execução que o host é `127.0.0.1` / `localhost`, e não contém `.supabase.co`.
3. Comparar no banco RESTAURADO as contagens de `auth.users`, `public.sie_projects`, `public.sie_project_revisions`, presença das 9 tabelas e 16 políticas RLS, e consultar hashes de estruturas, sem imprimir conteúdo de usuários.
4. Executar rollback de prova: descartar a base local e reexecutar restauração sem erros; registrar versão PostgreSQL/Supabase, horário, testes e hashes dos arquivos.
5. Se versão de Auth/Storage ou extensões impedir restauração válida, **não marcar PASS**; resolver compatibilidade e testar novamente. Backups SQL sem restauração bem-sucedida não satisfazem autorização.
6. Gerar **manifesto separado de validação de restauração** com código `C14_RESTORE_VERIFIED`, executor, data, checks de estrutura/contagens, hash dos arquivos e referência ao banco local descartável.

**Não executar** `db reset` / `db push` / `apply_migration` / `psql` contra o projeto remoto durante esta etapa.

## 4. Backup da origem e corte transacional

Antes da importação REAL, efetuar adicionalmente um dump read-only protegido do projeto **de origem** `hlbksclcandbsyqrsbmx`, com 15 tabelas e trilha histórica; calcular hash e comparar o inventário de corte. O script C14 acima é de **destino**; para a origem, usar comandos oficiais em contexto separado vinculado somente ao projeto de origem. Nunca modificar o banco legado e nunca promover autor textual a identidade Auth.

Como houve timeout em leituras atuais à origem, tratar o `cutoff` como **PENDING** até acesso consistente; não presumir que as contagens históricas continuam atuais.

## 5. Gates para aplicação remota das migrations no destino

**Pré-migration GO = todos verdadeiros:**

- [ ] Dump do **destino real** com roles/schema/data, hashes e guarda privada;
- [ ] **Restauração integral verificável** no banco local descartável, com comparativos;
- [ ] Verificação de ausência de mudanças de schema desde o pré-voo (readback de migration history, 9 tabelas / 63 colunas / 16 políticas, ou diferenças revisadas);
- [ ] Exame das migration SQL versionadas em ordem A03 → A04 → B04 → C03, mesmo SHA aprovado e sem DDL destrutiva inesperada;
- [ ] Verificações de RLS, privilégios e segurança de dados;
- [ ] Confirmação de que `fozrymsidnaxmuvxxfhh` continua sendo o projeto de **pré-produção**, sem serviço real;
- [ ] Plano de reversão usando os arquivos de backup já comprovados e janela de manutenção.

Depois do GO, aplicar **uma** migration por vez por `apply_migration` (sem alterações manuais em produção), verificar sua versão `supabase_migrations.schema_migrations`, invariantes do schema e políticas. Em caso de erro, **interromper** sem testar próximas migrations.

**GO ETL REAL** é separado: requer dump de origem com corte e reconciliação 1.934 (valor histórico a revalidar), comprovação de sessão Auth real do titular, autorização de mapeamento dos cinco projetos, quarentena sem perda dos sete campos elétricos e demais dados não homologados, idempotência e rollback.

**GO GC=PASS** requer adicionalmente decisão técnica do profissional habilitado sobre E01–E11, termo C13 assinado, testes de integração A/B reais e cinco workflows PASS no SHA congelado. É proibido elevar GC apenas com `PASS` sintético.

## 6. Segurança e limites

- Organizaçao `Applicationmanager` Free: **nenhuma criação de projeto/branch paga**; o projeto de destino existente é usado após verificação.
- Não publicar SQL dumps, JWTs, senhas, credenciais, `auth.users`, scripts de conexão com segredos ou documentos CREA com PII no GitHub.
- `main`, F12, SIE original, Hostinger e produção permanecem intactos.
- Esta documentação e o script **não executaram backup remoto, restore real, migrations ou ETL**; são instrumentos de execução e prova.
