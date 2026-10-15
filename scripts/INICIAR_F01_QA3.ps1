<#
.SYNOPSIS
Ativa três perfis Copilot em worktrees Git independentes, em sessões SEQUENCIAIS isoladas.
.DESCRIPTION
Execute manualmente em Windows PowerShell com Git e Copilot CLI instalados/autenticados.
Não funde branches nem publica produção. Não altera estado de F01/F02.
O script APENAS inicia agentes quando -Executar for fornecido.
#>
param(
  [string]$Repositorio = (Get-Location).Path,
  [switch]$Executar
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = (Resolve-Path -LiteralPath $Repositorio).Path
if (-not (Test-Path (Join-Path $Repo '.git'))) {
  throw "Informe a pasta raiz do clone Git. Nao foi encontrado .git em $Repo"
}
$agents = @(
  @{ Id='QA-01'; Agent='f01-qa-arquiteto'; Branch='qa/f01-arquiteto'; Dir='QA-01' },
  @{ Id='QA-02'; Agent='f01-qa-engenheiro-eletrico'; Branch='qa/f01-engenheiro-eletrico'; Dir='QA-02' },
  @{ Id='QA-03'; Agent='f01-qa-dados-ux-llm'; Branch='qa/f01-dados-ux-llm'; Dir='QA-03' }
)
$Root = Join-Path (Split-Path -Parent $Repo) 'SIE_F01_QA3_WORKTREES'
$Logs = Join-Path $Root 'logs'

Write-Host "Repo: $Repo"
Write-Host "Pasta de worktrees: $Root"
Write-Host "Modo: $(if($Executar){'EXECUTAR'}else{'SOMENTE PLANO'})"
if (-not $Executar) {
  foreach ($a in $agents) {
    Write-Host "Planejado: $($a.Id) -> $($a.Branch) / $($a.Agent)"
  }
  Write-Host "Para iniciar, execute novamente com -Executar. Todos os bloqueios F01 permanecem fechados."
  exit 0
}
foreach ($command in @('git', 'copilot')) {
  if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
    throw "Comando '$command' indisponivel. Instale/autentique Git e GitHub Copilot CLI antes de iniciar."
  }
}
# Não modifica os arquivos do checkout principal; só atualiza refs remotas.
& git -C $Repo fetch origin
if ($LASTEXITCODE -ne 0) { throw 'Falha no git fetch; sem execucao dos agentes' }
New-Item -ItemType Directory -Force -Path $Root, $Logs | Out-Null

foreach ($a in $agents) {
  $worktree = Join-Path $Root $a.Dir
  if (-not (Test-Path $worktree)) {
    & git -C $Repo show-ref --verify --quiet "refs/heads/$($a.Branch)"
    if ($LASTEXITCODE -eq 0) {
      & git -C $Repo worktree add $worktree $a.Branch
    } else {
      & git -C $Repo worktree add -b $a.Branch $worktree "origin/$($a.Branch)"
    }
    if ($LASTEXITCODE -ne 0) { throw "Nao foi possivel criar worktree de $($a.Id)" }
  }
  $dirty = & git -C $worktree status --porcelain
  if ($LASTEXITCODE -ne 0 -or $dirty) {
    throw "Worktree $($a.Id) com arquivos pendentes; para evitar sobrescrita, corriga antes de continuar"
  }
  $profile = Join-Path $worktree ".github/agents/$($a.Agent).agent.md"
  if (-not (Test-Path $profile)) { throw "Perfil nao encontrado: $profile" }
  $prompt = @"
Execute a F01 inteira como $($a.Id). Leia:
docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md,
docs/sie-orchestrator/NEXT_ACTION.md,
.github/agents/$($a.Agent).agent.md.
Execute INDEPENDENTEMENTE as etapas E01, E02, E03, E04, E05 e todos os gates G01..G06 na SUA branch.
Implemente e teste o que for verificavel, com fontes oficiais autorizadas, dados numericos
somente apos dupla conferencia independente, preservando golden F00 e mantendo F01 BLOCKED
e F02 nao liberada enquanto faltarem provas.
Produza PLANO_E_EXECUCAO.md, MATRIZ_6_GATES.json, PARECER_QA.md e registre SHA/CI
em docs/implantacao-sie-2-0/F01/qa3-runs/$($a.Id)/.
NAO leia rascunhos de outros QA antes de congelar seu primeiro parecer.
Nao modifique producao, Supabase remoto ou main. Registre bloqueios com honestidade.
"@
  $log = Join-Path $Logs "$($a.Id)-console.log"
  Write-Host "INICIANDO $($a.Id) no worktree $worktree. Log: $log"
  Push-Location $worktree
  try {
    & copilot --agent $a.Agent --prompt $prompt 2>&1 | Tee-Object -FilePath $log
    if ($LASTEXITCODE -ne 0) {
      throw "O CLI retornou erro para $($a.Id); veja o log $log"
    }
    $after = & git rev-parse HEAD
    Write-Host "$($a.Id): final de sessao. HEAD=$after"
  } finally {
    Pop-Location
  }
}
Write-Host 'Tres sessoes solicitadas. Inspecione commits e resultados. NENHUM gate foi aprovado por este script.'
Write-Host 'Depois, realize revisao cruzada em sessoes independentes; nao mescle sem gate tecnico e autorizacao.'
