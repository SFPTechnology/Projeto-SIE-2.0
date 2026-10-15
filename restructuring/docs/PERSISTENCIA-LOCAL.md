# SIE 2.0 — Persistência local de projetos (modo iniciante)

## O que foi implementado

O SIE agora disponibiliza **CLI direta e API opcional** sobre o mesmo armazenamento SQLite para **testes locais**. As operações disponíveis são criar/atualizar projeto, buscar projeto e consultar histórico de revisões. A **API HTTP** é bloqueada por padrão e exige um token local configurado no servidor. A CLI acessa diretamente o SQLite no computador, sem token HTTP. Não é serviço de produção, não integra Supabase/PostgreSQL e não é autenticação por usuário final.

## Modo recomendado: CLI sem servidor nem token

Siga a regra do projeto **CLI First**. Abra o PowerShell dentro de `restructuring\apps\api` com Python instalado e ambiente virtual ativo. A CLI usa somente o arquivo SQLite informado; não se conecta à internet, não inicia a API e não concede aprovação normativa.

**1. Testar que a CLI responde:**

```powershell
python -m sie_api.cli --help
```

**2. Criar um arquivo de dados de exemplo** (`dados.json`), usando PowerShell:

```powershell
'{"circuitos":[{"nome":"TUG 01"}]}' | Set-Content -Encoding utf8 dados.json
```

**3. Salvar um novo projeto:**

```powershell
python -m sie_api.cli --database sie-local.sqlite3 salvar --nome "Casa de teste" --arquivo dados.json
```

O retorno contém `id` (UUID) e `revisao: 1`. Copie o identificador retornado.

**4. Consultar o projeto e as revisões**, substituindo `UUID_COPIADO` pelo valor recebido:

```powershell
python -m sie_api.cli --database sie-local.sqlite3 carregar --id UUID_COPIADO
python -m sie_api.cli --database sie-local.sqlite3 historico --id UUID_COPIADO
```

**5. Atualizar o projeto:** edite `dados.json`, utilize o mesmo ID e forneça `--revisao-esperada 1`. Uma nova gravação bem-sucedida gerará a revisão 2.

```powershell
python -m sie_api.cli --database sie-local.sqlite3 salvar --id UUID_COPIADO --nome "Casa atualizada" --arquivo dados.json --revisao-esperada 1
```

Erros: código 2 = entrada/arquivo inválido; código 3 = projeto inexistente; código 4 = conflito de revisão. O banco tem limite de 1 MiB de JSON por projeto. O arquivo deve ser um **objeto** JSON. UTF-8 com ou sem BOM é aceito para compatibilidade com PowerShell.

A CLI e a API podem usar o mesmo arquivo de banco, mas não modifique arquivos SQLite manualmente enquanto houver gravações em andamento. O token `SIE_LOCAL_API_TOKEN` se aplica somente à API HTTP e não é exigido para a CLI que trabalha com seu próprio acesso local.

---

## Modo opcional: API local com token

## 1. Preparar o ambiente

Abra PowerShell na pasta `restructuring\apps\api` e ative o ambiente virtual, conforme o README.

Gere um token aleatório com PowerShell, sem colar segredos no repositório:

```powershell
$env:SIE_LOCAL_API_TOKEN = ([guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N"))
$env:SIE_LOCAL_DB_PATH = Join-Path (Get-Location) "sie-local.sqlite3"
python -m uvicorn sie_api.main:app --host 127.0.0.1 --port 8000
```

**Importante:** a API de armazenamento somente é habilitada quando ambos os valores existem e o token tem pelo menos 24 caracteres. Não faça push da base `sie-local.sqlite3` ou do token. Para impedir acesso por outros computadores, mantenha `--host 127.0.0.1`.

## 2. Fazer uma gravação

Em outro terminal PowerShell, a API pode ser testada com `Invoke-RestMethod`. Use o mesmo token criado no primeiro terminal, transferindo-o com cuidado para a variável `$token` do terminal de teste (não publique em prints, scripts ou chats).

```powershell
$token = "<TOKEN_LOCAL_GERADO_NO_PRIMEIRO_TERMINAL>"
$headers = @{ Authorization = "Bearer $token" }
$id = [guid]::NewGuid().ToString()
$corpo = @{
  id = $id
  nome = "Teste de projeto residencial"
  dados = @{ circuitos = @() }
  revisao_esperada = 0
} | ConvertTo-Json -Depth 8
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/local/projetos" -Method Put -Headers $headers -ContentType "application/json" -Body $corpo
```

A resposta deve incluir `estado: armazenado_localmente` e `revisao: 1`. Na segunda gravação do mesmo ID, use `revisao_esperada: 1`; a nova revisão será `2`.

## 3. Consultar o projeto e o histórico

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/local/projetos/$id" -Headers $headers
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/local/projetos/$id/historico" -Headers $headers
```

## 4. Entendendo mensagens de erro

| HTTP | Mensagem | Significado |
|---|---|---|
| 503 | Armazenamento local desabilitado | Token ou caminho do banco não configurados |
| 401 | Credencial inválida/ausente | Token incorreto ou não enviado |
| 409 | Conflito de revisão | Outro salvamento alterou o projeto; releia antes de gravar |
| 422 | Dados inválidos | Confira nome, tamanho do JSON, campos e revisão |
| 404 | Projeto não encontrado | ID não existe no banco local |

## 5. Limitações e próximos passos

- Dados ficam no arquivo SQLite local. A gravação não modifica o banco Supabase.
- A interface possui painel experimental **Projetos locais** para salvar e reabrir análises. Requer API e token; a CLI funciona independentemente.
- Não há contas, perfis ou permissões de produção; o token protege apenas este ambiente local de desenvolvimento.
- Não há assinatura de evidência normativa nem aprovação automática de projetos.
- O banco local e o log de eventos requerem política de backups, migrações e autorização por identidade antes de uso profissional.
