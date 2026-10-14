# SIE 2.0 — Persistência local de projetos (modo iniciante)

## O que foi implementado

A API possui armazenamento SQLite para **testes locais**. As operações disponíveis são criar/atualizar projeto, buscar projeto e consultar histórico de revisões. O acesso é bloqueado por padrão e exige um token local configurado no servidor. Não é serviço de produção, não integra Supabase/PostgreSQL e não é autenticação por usuário final.

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
- A interface ainda não possui uma seção integrada para carregar e salvar projetos.
- Não há contas, perfis ou permissões de produção; o token protege apenas este ambiente local de desenvolvimento.
- Não há assinatura de evidência normativa nem aprovação automática de projetos.
- O banco local e o log de eventos requerem política de backups, migrações e autorização por identidade antes de uso profissional.
