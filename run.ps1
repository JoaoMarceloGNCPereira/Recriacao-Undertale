<#
.SYNOPSIS
Prepara o ambiente Python e inicia o jogo.
#>

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
        throw "Python não encontrado. Instale Python 3.12, 3.13 ou 3.14 e marque 'Add Python to PATH'."
    }
    Write-Host "Criando ambiente virtual..."
    & py -m venv .venv
}

& $venvPython -c "import sys; raise SystemExit(0 if (3, 12) <= sys.version_info < (3, 15) else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "Este projeto precisa de Python 3.12, 3.13 ou 3.14."
}

Write-Host "Instalando/atualizando dependências..."
& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Não foi possível instalar as dependências." }

& $venvPython Main.py
