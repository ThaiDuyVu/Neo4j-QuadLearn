$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
py -3.11 -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "Cài Python 3.11 và Python Launcher trước." }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Cài dependencies thất bại." }
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
Write-Host "Đặt mật khẩu riêng trong .env; chạy docker compose up -d --wait và python -m scripts.db init."
