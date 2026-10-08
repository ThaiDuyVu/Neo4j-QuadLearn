$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
& .\.venv\Scripts\python.exe -m streamlit run app/main.py
if ($LASTEXITCODE -ne 0) { throw "Streamlit dừng với lỗi." }
