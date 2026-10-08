#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
printf '%s\n' 'Đặt mật khẩu riêng trong .env, sau đó docker compose up -d --wait và .venv/bin/python -m scripts.db init.'
