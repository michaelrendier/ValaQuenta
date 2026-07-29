<#
.SYNOPSIS
    ValaQuenta - installer for Windows (PowerShell 5.1 or PowerShell 7+).

.DESCRIPTION
    Creates a virtual environment in .venv, installs the dependencies from
    requirements.txt, and then verifies the install by recomputing a known
    constant rather than merely checking that imports succeed.

    Nothing here needs an administrator prompt.

.PARAMETER User
    Install into the user site-packages instead of creating a .venv.

.PARAMETER NoJupyter
    Skip JupyterLab. The engines import fine without it; you just cannot open
    the .ipynb files.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\install.ps1

.EXAMPLE
    .\install.ps1 -NoJupyter

.NOTES
    If PowerShell refuses to run this file, Windows is blocking unsigned
    scripts. Either use the -ExecutionPolicy Bypass form above, or allow local
    scripts for your account:

        Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#>

[CmdletBinding()]
param(
    [switch]$User,
    [switch]$NoJupyter
)

$ErrorActionPreference = 'Stop'
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoDir

function Say  { param($m) Write-Host "`n==> $m" -ForegroundColor White }
function Warn { param($m) Write-Host "    $m" -ForegroundColor Yellow }
function Die  { param($m) Write-Host "ERROR: $m" -ForegroundColor Red; exit 1 }

# ── Python ───────────────────────────────────────────────────────────────────
Say 'Locating Python'

$Py = $null
$candidates = @()

# The py launcher is the most reliable way to find a specific version.
if (Get-Command py -ErrorAction SilentlyContinue) {
    foreach ($v in @('3.13', '3.12', '3.11', '3.10')) {
        $candidates += ,@('py', @("-$v"))
    }
}
$candidates += ,@('python', @())
$candidates += ,@('python3', @())

foreach ($c in $candidates) {
    $exe = $c[0]; $pre = $c[1]
    if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
    try {
        $args = $pre + @('-c', 'import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)')
        & $exe @args 2>$null
        if ($LASTEXITCODE -eq 0) { $Py = $exe; $PyPre = $pre; break }
    } catch { }
}

if (-not $Py) {
    Die @"
no Python 3.10+ found.

Install it from https://www.python.org/downloads/ and tick
"Add python.exe to PATH" during setup, or from the Microsoft Store:

    winget install Python.Python.3.12
"@
}

$verText = & $Py @($PyPre + @('--version')) 2>&1
Write-Host "    $Py $PyPre -> $verText"

# ── Environment ──────────────────────────────────────────────────────────────
$PipTarget = @()
if ($User) {
    Say 'Installing into the user site-packages'
    $PipTarget = @('--user')
    $PyExe = $Py; $PyArgs = $PyPre
}
else {
    Say 'Creating virtual environment (.venv)'
    if (-not (Test-Path '.venv')) {
        & $Py @($PyPre + @('-m', 'venv', '.venv'))
        if ($LASTEXITCODE -ne 0) { Die 'could not create the virtual environment' }
    }
    else {
        Write-Host '    .venv already exists, reusing it'
    }
    $PyExe = Join-Path $RepoDir '.venv\Scripts\python.exe'
    $PyArgs = @()
    if (-not (Test-Path $PyExe)) { Die "venv python not found at $PyExe" }
}

# ── Dependencies ─────────────────────────────────────────────────────────────
Say 'Installing dependencies'
& $PyExe @($PyArgs + @('-m', 'pip', 'install', '--upgrade', 'pip')) 2>$null | Out-Null

$Req = 'requirements.txt'
if ($NoJupyter) {
    $Req = [System.IO.Path]::GetTempFileName()
    Get-Content 'requirements.txt' |
        Where-Object { $_ -notmatch '^(jupyterlab|ipykernel)' } |
        Set-Content $Req
    Write-Host '    (skipping JupyterLab)'
}

& $PyExe @($PyArgs + @('-m', 'pip', 'install') + $PipTarget + @('-r', $Req))
if ($LASTEXITCODE -ne 0) {
    Warn 'pip install failed.'
    Warn 'If a package tried to build from source, install the Microsoft C++'
    Warn 'Build Tools, or use a Python version that has prebuilt wheels'
    Warn '(3.10-3.13 are safest).'
    Die 'dependency installation failed'
}

# ── Verify ───────────────────────────────────────────────────────────────────
Say 'Verifying'
& $PyExe @($PyArgs + @('verify_install.py'))
if ($LASTEXITCODE -ne 0) { Die 'verification failed - see output above' }

# ── Done ─────────────────────────────────────────────────────────────────────
Say 'Installed'
if (-not $User) {
    Write-Host @"
    Activate the environment in each new shell:

        $RepoDir\.venv\Scripts\Activate.ps1

"@
}
Write-Host @'
    Try:
        python -m ValaQuenta --info
        jupyter lab notebooks/

    Start at notebooks/engines/ or wiki/00_index.md.
'@
