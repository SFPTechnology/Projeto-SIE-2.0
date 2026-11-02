<#
.SYNOPSIS
 SIE 2.0 C14 - only exports a real, private Supabase logical backup; NEVER modifies a remote database.
.DESCRIPTION
 Requires the official Supabase CLI, Docker Desktop and prior Supabase CLI login.
 Creates a fresh private output folder under the current user's Documents directory.
 Runs exactly three official 'supabase db dump' read-only operations using 'supabase link'.
 Produces hash manifest and an explicit RESTORE_NOT_VERIFIED state.
 DO NOT put the backup folder, auth data or DB passwords in GitHub.
#>
[CmdletBinding()]
param(
  [string]$OutputRoot = [System.IO.Path]::Combine(
    [Environment]::GetFolderPath('MyDocuments'), 'SIE2_BACKUPS_PRIVADOS')
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$expectedRef = 'fozrymsidnaxmuvxxfhh'

if (-not (Get-Command supabase -ErrorAction SilentlyContinue)) {
  throw 'Supabase CLI nao encontrado. Instale e autentique: supabase login.'
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  throw 'Docker Desktop nao encontrado. Supabase db dump exige Docker.'
}
& docker info --format '{{.ServerVersion}}' *> $null
if ($LASTEXITCODE -ne 0) { throw 'Docker Desktop nao esta em execucao.' }

$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$root = Join-Path $OutputRoot ('SIE2_C14_' + $stamp)
if (Test-Path -LiteralPath $root) { throw 'Diretorio de backup ja existente; recuso sobrescrever.' }
New-Item -ItemType Directory -Path $root -Force | Out-Null
$workspace = Join-Path $root 'supabase_cli_context'
New-Item -ItemType Directory -Path $workspace | Out-Null
$files = @(
  @{ Name='roles.sql'; Args=@('--role-only') },
  @{ Name='schema.sql'; Args=@() },
  @{ Name='data.sql'; Args=@('--use-copy','--data-only','-x','storage.buckets_vectors','-x','storage.vector_indexes') }
)
$started = (Get-Date).ToUniversalTime().ToString('o')
try {
  Push-Location $workspace
  try {
    Write-Host 'Inicializando contexto CLI local (sem escrita remota)...'
    & supabase init
    if ($LASTEXITCODE -ne 0) { throw 'supabase init falhou.' }
    Write-Host 'Vinculando SOMENTE para exportacao. A CLI pode solicitar a senha do banco; nao a compartilhe aqui.'
    & supabase link --project-ref $expectedRef
    if ($LASTEXITCODE -ne 0) { throw 'supabase link falhou.' }
    foreach ($item in $files) {
      $full = Join-Path $root $item.Name
      Write-Host ("Exportando " + $item.Name + "...")
      & supabase db dump -f $full @($item.Args)
      if ($LASTEXITCODE -ne 0) { throw ('Dump falhou: ' + $item.Name) }
      if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        throw ('Arquivo ausente: ' + $item.Name)
      }
      # roles.sql may have no custom role declarations; schema and data must not be empty.
      if ($item.Name -ne 'roles.sql' -and (Get-Item -LiteralPath $full).Length -eq 0) {
        throw ('Dump vazio: ' + $item.Name)
      }
    }
  } finally { Pop-Location }
  $records = foreach ($item in $files) {
    $full = Join-Path $root $item.Name
    $f = Get-Item -LiteralPath $full
    [ordered]@{
      name = $item.Name
      bytes = $f.Length
      sha256 = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant()
    }
  }
  $manifest = [ordered]@{
    schema_version = 1
    project_ref = $expectedRef
    utc_started_at = $started
    utc_finished_at = (Get-Date).ToUniversalTime().ToString('o')
    operation = 'READ_ONLY_SUPABASE_CLI_DB_DUMP'
    source_kind = 'REAL_REMOTE_DATABASE'
    restore_state = 'NOT_VERIFIED'
    migration_go = $false
    files = @($records)
    handling = 'PRIVATE_CONFIDENTIAL_CONTAINS_AUTH_DATA'
  }
  ($manifest | ConvertTo-Json -Depth 5) | Set-Content -LiteralPath (Join-Path $root 'manifest.json') -Encoding UTF8
  Write-Host 'EXPORTACAO COMPLETA: hashes SHA256 gerados.'
  Write-Host ('Local: ' + $root)
  Write-Host 'BLOQUEIO: restauracao independente ainda nao testada; nenhuma migration remota autorizada por este script.'
  Write-Host 'Envie ao responsavel somente manifest.json (apos revisar metadados), NUNCA roles/schema/data.sql.'
} finally {
  # Sensitive tokens, if any, are not needed in the backup folder.
  if (Test-Path -LiteralPath $workspace) {
    Remove-Item -LiteralPath $workspace -Recurse -Force -ErrorAction SilentlyContinue
  }
}
