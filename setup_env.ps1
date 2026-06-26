#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Set up the qec-ftqc-portfolio Python environment using venv (no conda).
    Run this script once to create and populate the virtual environment.

.USAGE
    # From the project root:
    .\setup_env.ps1

.NOTES
    Requires Python 3.11+ to be installed and on your PATH.
    To check: python --version
#>

Write-Host "=== QEC-FTQC Portfolio — Environment Setup ===" -ForegroundColor Cyan
Write-Host "Using Python venv (no conda required)" -ForegroundColor Green
Write-Host ""

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "Detected: $pythonVersion"
if ($pythonVersion -notmatch "3\.1[1-9]|3\.[2-9]\d") {
    Write-Warning "Python 3.11+ is recommended. Found: $pythonVersion"
    Write-Warning "Proceeding anyway — some packages may not install."
}

# Create virtual environment
if (-Not (Test-Path ".venv")) {
    Write-Host "`nCreating virtual environment at .venv ..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "`n.venv already exists — skipping creation." -ForegroundColor Yellow
}

# Activate
Write-Host "`nActivating virtual environment ..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "`nUpgrading pip ..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install project in editable mode (installs all dependencies from pyproject.toml)
Write-Host "`nInstalling qec-ftqc-portfolio and all dependencies ..." -ForegroundColor Yellow
pip install -e ".[dev]"

# Verify key imports
Write-Host "`nVerifying key package imports ..." -ForegroundColor Yellow
$imports = @("numpy", "scipy", "stim", "pymatching", "ldpc", "qiskit", "pytest")
foreach ($pkg in $imports) {
    $result = python -c "import $pkg; print('  ✓ $pkg', $pkg.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host $result -ForegroundColor Green
    } else {
        Write-Host "  ✗ $pkg — FAILED TO IMPORT" -ForegroundColor Red
    }
}

# Run initial tests
Write-Host "`nRunning initial test suite ..." -ForegroundColor Yellow
pytest tests/ -v --tb=short

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the environment in future sessions:" -ForegroundColor White
Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "To run tests:" -ForegroundColor White
Write-Host "  pytest tests/ -v" -ForegroundColor Yellow
Write-Host ""
Write-Host "To start Jupyter:" -ForegroundColor White
Write-Host "  jupyter notebook examples/" -ForegroundColor Yellow
