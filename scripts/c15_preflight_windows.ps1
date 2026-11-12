<#
 C15 preflight - native PostgreSQL 17 on Windows. No Docker Desktop.
 No remote SQL or DB writes. Safe diagnostic summary only.
#>
[CmdletBinding()]
param(
 [ValidateRange(1025,65535)][int]$LocalPort=55432,
 [string]$BackupRoot=[IO.Path]::Combine($env:LOCALAPPDATA,'SIE2_BACKUPS_PRIVADOS'),
 [string]$ReportPath=''
)
. (Join-Path $PSScriptRoot 'c15_native_common.ps1')
Assert-C15Tools
$root=Assert-C15PrivateFolder $BackupRoot
$localOnline=$false
$prior=$env:PGSSLMODE
try {
 $env:PGSSLMODE='disable'
 & pg_isready -h 127.0.0.1 -p "$LocalPort" | Out-Null
 $localOnline=($LASTEXITCODE -eq 0)
} finally { $env:PGSSLMODE=$prior }
$report=[ordered]@{
 schema_version='C15-PREFLIGHT-1'
 expected_project_ref=$script:C15Destination
 native_postgresql_tools='PASS'
 docker_desktop_required=$false
 local_postgresql_online=$localOnline
 local_host='127.0.0.1'
 local_port=$LocalPort
 private_backup_root=$root
 remote_database_not_touched=$true
 remote_migrations_applied=$false
 gate=if ($localOnline) {'ENV_READY_CHECK_CREDENTIALS_SEPARATELY'} else {'BLOCKED_LOCAL_POSTGRESQL_NOT_RUNNING'}
 utc=(Get-Date).ToUniversalTime().ToString('o')
}
if ($ReportPath) {
 $file=[IO.Path]::GetFullPath($ReportPath)
 [void](Assert-C15PrivateFolder (Split-Path -Parent $file))
 $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $file -Encoding UTF8
}
$report | ConvertTo-Json -Depth 5
