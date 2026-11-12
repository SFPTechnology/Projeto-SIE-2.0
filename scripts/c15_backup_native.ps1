<#
 Native read-only PostgreSQL 17 SIE 2.0 pre-production backup.
 Requires PGSSLMODE=verify-full, PGSSLROOTCERT and PGPASSFILE.
 Storage objects, auth service config, Edge Functions remain outside dump.
#>
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$RemoteHost,
 [Parameter(Mandatory=$true)][string]$RemoteUser,
 [int]$RemotePort=5432,
 [string]$OutputRoot=[IO.Path]::Combine($env:LOCALAPPDATA,'SIE2_BACKUPS_PRIVADOS')
)
. (Join-Path $PSScriptRoot 'c15_native_common.ps1')
Assert-C15Tools
Assert-C15Remote $RemoteHost $RemoteUser $RemotePort
$root=Assert-C15PrivateFolder $OutputRoot
$folder=Join-Path $root ("C15_DEST_"+(Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ'))
if (Test-Path -LiteralPath $folder) { throw 'Recuso sobrescrever backup.' }
New-Item -ItemType Directory -Path $folder -Force | Out-Null
$backup=Join-Path $folder 'sie2_full_database.backup'
$toc=Join-Path $folder 'toc_private.txt'
& pg_dump --no-password --format=custom --file=$backup --host=$RemoteHost --port="$RemotePort" --username=$RemoteUser --dbname=postgres
if ($LASTEXITCODE -ne 0) { throw 'pg_dump falhou. Nenhum GO.' }
if (-not (Test-Path -LiteralPath $backup) -or (Get-Item -LiteralPath $backup).Length -le 5) { throw 'Backup invalido.' }
& pg_restore --list $backup | Set-Content -LiteralPath $toc -Encoding UTF8
if ($LASTEXITCODE -ne 0) { throw 'TOC do dump invalido.' }
$counts=Get-C15Counts $RemoteHost $RemotePort $RemoteUser 'postgres'
$file=Get-Item -LiteralPath $backup
$manifest=[ordered]@{
 schema_version='C15-1'
 project_ref=$script:C15Destination
 mode='REAL_REMOTE_READ_ONLY'
 source_kind='SUPABASE_SIE2_PREPRODUCTION'
 dump_format='custom'
 utc_created_at=(Get-Date).ToUniversalTime().ToString('o')
 remote_write_performed=$false
 migration_go=$false
 restore_state='NOT_VERIFIED'
 backup=[ordered]@{
   name=$file.Name
   bytes=$file.Length
   sha256=(Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash.ToLowerInvariant()
 }
 baseline=[ordered]@{
  auth_users=$counts[0]
  public_projects=$counts[1]
  public_revisions=$counts[2]
  public_tables=$counts[3]
  public_columns=$counts[4]
  public_rls_policies=$counts[5]
 }
 coverage=[ordered]@{
  full_pg_dump_attempted=$true
  roles_globally_dumped=$false
  storage_binary_objects_exported=$false
  auth_and_storage_service_recovery='NOT_VERIFIED'
  roles_acl_equivalent='NOT_VERIFIED'
  external_configuration_exported=$false
 }
}
$manifestPath=Join-Path $folder 'manifest.json'
$manifest | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
& python (Join-Path $PSScriptRoot 'c15_integrity.py') verify-backup --manifest $manifestPath --backup $backup
if ($LASTEXITCODE -ne 0) { throw 'Hash de backup inconsistente.' }
Write-Host 'Dump PostgreSQL concluido, integridade SHA256 PASS, RESTORE PENDENTE.'
Write-Host "Pasta privada: $folder"
