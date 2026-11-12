<#
 C15 restore of a native PostgreSQL backup into a fresh LOCAL PG17 database.
 Never issues commands to the remote database. Missing roles/extensions block.
 Requires PG17 installed and local PostgreSQL service on a loopback port.
#>
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$ManifestPath,
 [Parameter(Mandatory=$true)][string]$BackupPath,
 [int]$LocalPort=55432,
 [string]$LocalHostName='127.0.0.1',
 [string]$LocalUser='postgres',
 [string]$RestoreDatabase='c15_target_restore'
)
. (Join-Path $PSScriptRoot 'c15_native_common.ps1')
Assert-C15Tools
Assert-C15Local $LocalHostName $LocalPort $RestoreDatabase
$manifest=Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if ($manifest.project_ref -cne $script:C15Destination) { throw 'Projeto de destino incorreto.' }
& python (Join-Path $PSScriptRoot 'c15_integrity.py') verify-backup --manifest $ManifestPath --backup $BackupPath
if ($LASTEXITCODE -ne 0) { throw 'Dump e manifesto nao conferem.' }
$old=$env:PGSSLMODE
$env:PGSSLMODE='disable'
try {
  $exists=@(& psql -X -A -t -w -v ON_ERROR_STOP=1 -h $LocalHostName -p "$LocalPort" -U $LocalUser -d postgres -c "SELECT count(*) FROM pg_database WHERE datname='$RestoreDatabase';")
  if ($LASTEXITCODE -ne 0 -or $exists.Count -ne 1 -or $exists[0] -cne '0') { throw 'Banco local existente ou conexao insegura.' }
  & createdb --no-password -h $LocalHostName -p "$LocalPort" -U $LocalUser $RestoreDatabase
  if ($LASTEXITCODE -ne 0) { throw 'Criacao de base local falhou.' }
  # Do not suppress errors, silently skip objects or claim ACL fidelity.
  & pg_restore --no-password --single-transaction --exit-on-error -h $LocalHostName -p "$LocalPort" -U $LocalUser -d $RestoreDatabase $BackupPath
  if ($LASTEXITCODE -ne 0) { throw 'Restore incompleto; inspecione roles e extensoes. REMOTO INTACTO.' }
  $counts=Get-C15Counts $LocalHostName $LocalPort $LocalUser $RestoreDatabase
  $reference=@($manifest.baseline.auth_users,$manifest.baseline.public_projects,$manifest.baseline.public_revisions,$manifest.baseline.public_tables,$manifest.baseline.public_columns,$manifest.baseline.public_rls_policies)
  $same=$true
  for ($i=0;$i -lt 6;$i++) { if ($counts[$i] -ne [int]$reference[$i]) { $same=$false } }
  $proof=[ordered]@{
    schema_version='C15-RESTORE-1'
    project_ref=$script:C15Destination
    backup_sha256=$manifest.backup.sha256
    restore_target='LOCAL_POSTGRESQL_17_DISPOSABLE'
    utc=(Get-Date).ToUniversalTime().ToString('o')
    checks=[ordered]@{
      dump_exit_zero=$true
      restore_exit_zero=$true
      schema_equivalent=$same
      row_counts_equivalent=$same
      rls_policies_equivalent=$same
      auth_data_equivalent=($counts[0] -eq [int]$manifest.baseline.auth_users)
      roles_acl_equivalent=$false
      extensions_equivalent=$false
      external_services_recovery_reviewed=$false
    }
    note='Pending independent ACL, role, extension, and external service review. Not a migration GO.'
  }
  $private=Split-Path -Parent ([IO.Path]::GetFullPath($ManifestPath))
  [void](Assert-C15PrivateFolder $private)
  $report=Join-Path $private 'restore-proof.json'
  $proof | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $report -Encoding UTF8
  & python (Join-Path $PSScriptRoot 'c15_integrity.py') verify-restore --manifest $ManifestPath --backup $BackupPath --proof $report
  if ($LASTEXITCODE -ne 0) { throw 'Verificador de integridade falhou.' }
  Write-Host 'Restore PG17 executado. Revisao independente de roles/ACL e servicos pendente; GC BLOCKED.'
  Write-Host "Relatorio privado: $report"
} finally { $env:PGSSLMODE=$old }
