# Native PostgreSQL 17 helpers, no Docker Desktop and no remote writes.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:C15Destination = 'fozrymsidnaxmuvxxfhh'

function Assert-C15Tools {
  foreach ($name in @('pg_dump','pg_restore','psql','pg_isready','createdb','python')) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) { throw "$name ausente no PATH." }
  }
  foreach ($name in @('pg_dump','pg_restore','psql')) {
    $version=(& $name --version | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $version -notmatch 'PostgreSQL\)?\s+(\d+)(?:\.\d+)?') {
      throw "Versao PostgreSQL nao identificada para $name."
    }
    if ([int]$Matches[1] -lt 17) { throw "$name precisa ser versao 17 ou superior." }
  }
}
function Assert-C15PrivateFolder([string]$folder) {
  if ([string]::IsNullOrWhiteSpace($folder)) { throw 'Diretorio privado obrigatorio.' }
  $full=[IO.Path]::GetFullPath($folder)
  if ($full -match '(?i)[\/\\]OneDrive(?:[\/\\]|$)') { throw 'Pasta OneDrive recusada.' }
  $current=[IO.DirectoryInfo]::new($full)
  while ($null -ne $current) {
    if (Test-Path -LiteralPath (Join-Path $current.FullName '.git')) { throw 'Pasta Git recusada.' }
    $current=$current.Parent
  }
  if (Test-Path -LiteralPath $full) {
    $item=Get-Item -LiteralPath $full -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
      throw 'Diretorio junction/reparse recusado.'
    }
  }
  return $full
}
function Assert-C15Remote([string]$hostName,[string]$userName,[int]$port) {
  $ref=$script:C15Destination
  $direct=($hostName -ceq "db.$ref.supabase.co" -and $userName -ceq 'postgres' -and $port -eq 5432)
  $pooler=($hostName -match '^[a-z0-9.-]+\.pooler\.supabase\.com$' -and
      $userName -ceq "postgres.$ref" -and $port -eq 5432)
  if (-not ($direct -or $pooler)) { throw 'Endpoint difere do SIE2 preproducao.' }
  if ($env:PGSSLMODE -cne 'verify-full') { throw 'PGSSLMODE=verify-full exigido.' }
  if (-not $env:PGSSLROOTCERT -or -not (Test-Path -LiteralPath $env:PGSSLROOTCERT -PathType Leaf)) {
    throw 'PGSSLROOTCERT oficial obrigatorio.'
  }
  if (-not $env:PGPASSFILE -or -not (Test-Path -LiteralPath $env:PGPASSFILE -PathType Leaf)) {
    throw 'PGPASSFILE privado obrigatorio.'
  }
  [void](Assert-C15PrivateFolder (Split-Path -Parent $env:PGPASSFILE))
}
function Assert-C15Local([string]$hostName,[int]$port,[string]$database) {
  if ($hostName -cne '127.0.0.1' -or $port -lt 1025 -or $port -gt 65535) {
    throw 'Restore permitido somente localhost/porta nao privilegiada.'
  }
  if ($database -cnotmatch '^c15_[a-z0-9_]{3,48}$') {
    throw 'Nome de banco local descartavel c15_* obrigatorio.'
  }
}
function Get-C15Counts([string]$hostName,[int]$port,[string]$userName,[string]$database) {
  $query="SELECT (SELECT count(*) FROM auth.users), (SELECT count(*) FROM public.sie_projects), (SELECT count(*) FROM public.sie_project_revisions), (SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'), (SELECT count(*) FROM information_schema.columns WHERE table_schema='public'), (SELECT count(*) FROM pg_policies WHERE schemaname='public');"
  $out=@(& psql -X -A -t -w -v ON_ERROR_STOP=1 -h $hostName -p "$port" -U $userName -d $database -c $query)
  if ($LASTEXITCODE -ne 0 -or $out.Count -ne 1 -or $out[0] -notmatch '^\d+\|\d+\|\d+\|\d+\|\d+\|\d+$') {
    throw 'Falha em validar contagens anonimizadas de schema/Auth.'
  }
  return ,([int[]]($out[0].Split('|')))
}
