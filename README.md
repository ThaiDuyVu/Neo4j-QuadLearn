# QuadLearn – Neo4j project skeleton

Ứng dụng hỗ trợ học Tứ giác theo cấp độ lớp 6–9, dựng cho bài tập nhóm NoSQL. Mục tiêu hiện tại: nền chạy được, minh họa graph và chia domain để Vũ, Sơn, Đạt phát triển song song. **Không phải hệ thống SRS hoàn chỉnh**. Demo identity không phải AUTH; AI mock không phải LLM. Đã đọc toàn bộ SRS v1.1, ánh xạ 86 FR/56 PB trong docs.

## Thành viên và stack

| Người | Domain / folder | Phụ thuộc qua contracts |
|---|---|---|
| Vũ | `app/features/identity_learning_path/` | Identity provider; đọc content và assessment để tiến độ |
| Sơn | `app/features/learning_geometry/` | Content provider; đọc identity; completion writer của Vũ TODO |
| Đạt | `app/features/assessment_ai/` | Assessment provider; đọc identity/content cho AI |

Python 3.11+, Streamlit 1.46.1, Neo4j driver 5.28.2, python-dotenv, pytest. Neo4j Community 5.26.0 trong Docker Compose, named volumes; Python chạy host. Không SQL/Redis/React/LLM API hay hạ tầng production.

## Cấu trúc

```text
QuadLearn/
├── app/main.py
├── app/core/                 # config, database, context/bootstrap, navigation
├── app/shared/               # models, contracts, components, utils
├── app/features/
│   ├── identity_learning_path/ # Vũ
│   ├── learning_geometry/     # Sơn (+ examples import)
│   └── assessment_ai/         # Đạt
│       # Mỗi feature: registry.py, pages/services/repositories/models/tests,
│       # README.md và GIT_WORKFLOW.md
├── database/                 # constraints, indexes, seed, reset_dev, examples Cypher
├── docs/                     # setup, kiến trúc, phân công, SRS mapping, nghiệm thu
├── scripts/                  # setup/run sh + ps1, db.py CLI
├── tests/                    # smoke, boundaries, navigation, integration
├── compose.yaml
├── requirements.txt
├── pytest.ini
└── .env.example
```

Tạo tại workspace hiện tại, không lồng thêm folder quadlearn-neo4j. Mỗi thành viên sửa registry/page/service/test feature mình. Core/shared/database thay đổi cần thông báo/review.

## Quick Start macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Quick Start Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

**Trước bước tiếp** mở `.env`, đặt NEO4J_PASSWORD riêng ≥8 ký tự, giữ user/database neo4j. Docker Desktop phải chạy. Không commit .env. Các lệnh chung hai OS:

```text
docker compose up -d --wait
python -m scripts.db init
python -m scripts.db check
python -m streamlit run app/main.py
```

Ứng dụng http://localhost:8501; Neo4j Browser http://localhost:7474, login neo4j/password `.env`; Bolt bolt://localhost:7687. Script thay bước setup: `bash scripts/setup.sh` / `.\scripts\setup.ps1`, script run tương ứng; không tự tạo password. Windows activation policy/cài đặt: xem tài liệu setup.

## Lệnh thường dùng

```text
python -m pytest -m "not integration"
python -m pip check
python -m scripts.db queries
docker compose config --quiet
docker compose logs --tail 100 neo4j
docker compose stop
docker compose start
```

`init` idempotent nhưng SET lại fixture. Reset demo có chủ đích: `python -m scripts.db reset --yes` (APP_ENV=development), **xóa nodes demo/cạnh nối**. Stop/down thường giữ volume; **down -v xóa toàn bộ dữ liệu**, không dùng như stop. Đổi password env không tự đổi password volume cũ.

## Tài liệu

- [Setup Windows](docs/SETUP_WINDOWS.md), [Setup macOS](docs/SETUP_MACOS.md), [Run project](docs/RUN_PROJECT.md)
- [Git/GitHub workflow](docs/GIT_GITHUB_WORKFLOW.md)
- [Architecture](docs/ARCHITECTURE.md), [Graph schema](docs/GRAPH_SCHEMA.md), [Database scripts](database/README.md)
- [Domain ownership](docs/DOMAIN_OWNERSHIP.md), [Feature integration](docs/FEATURE_INTEGRATION.md)
- [SRS traceability – 86 FR](docs/SRS_TRACEABILITY.md), [Product backlog – 56 stories](docs/PRODUCT_BACKLOG.md)
- [Open questions](docs/OPEN_QUESTIONS.md), [Demo guide](docs/DEMO_GUIDE.md), [Verification](docs/VERIFICATION.md)
- [Vũ bắt đầu](app/features/identity_learning_path/README.md), [Sơn bắt đầu](app/features/learning_geometry/README.md), [Đạt bắt đầu](app/features/assessment_ai/README.md)

Phạm vi TODO: AUTH/OAuth/email/consent, toàn bộ lesson lớp 6–9, canvas đầy đủ, quiz/essay workflows, progress/unlock ghi thật, import runtime, I18N đầy đủ, quota/chat persistence, provider LLM, cloud và NFR sản phẩm. Không đánh đồng smoke tests với nghiệm thu SRS.
