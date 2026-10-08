# Setup macOS

1. Cài Git, Python 3.11+ và Docker Desktop. Máy Intel/Apple Silicon chọn Docker Desktop đúng CPU. Image dùng tag Community có manifest amd64/arm64; không ép `platform`. Bật Docker Desktop, dành khoảng 2 GB RAM cho Neo4j và bảo đảm cổng 7474/7687 chưa bị dùng.
2. Clone repo thực tế (thay URL mẫu của nhóm):

```bash
git clone <URL_REPO_GITHUB_CUA_NHOM>
cd QuadLearn
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

3. Mở `.env`, đặt `NEO4J_PASSWORD` riêng ít nhất 8 ký tự. Giữ NEO4J_USER=neo4j, database=neo4j và URI local. Chọn mật khẩu chữ/số để tránh ký tự `$` được Docker Compose nội suy. Không commit `.env`. `.env.example` không có mật khẩu sử dụng được.
4. Chạy:

```bash
docker compose up -d --wait
python -m scripts.db init
python -m scripts.db check
python -m streamlit run app/main.py
```

5. Mở http://localhost:8501 và Browser http://localhost:7474. Nếu muốn scripts tương đương: `bash scripts/setup.sh`, sửa `.env`, start/seed rồi `bash scripts/run.sh`. Script setup chỉ tạo venv/dependencies/env, không tự chọn password.

Lỗi `python3` không tồn tại: cài Python từ python.org hoặc quản lý Python bạn dùng, mở Terminal mới. `ModuleNotFoundError`: activate đúng venv, dùng `python -m pip`. Không có Docker daemon: mở Docker Desktop, `docker info`. Cổng bị chiếm: dừng container/app xung đột; không tự xóa volume. DB đang khởi động: `docker compose logs --tail 100 neo4j`. Đăng nhập sai sau đổi `.env`: password volume cũ không đổi theo env; xem database/README.md. Pip lỗi với Python mới: dùng Python 3.11/3.12 đã cài thay vì Python mới hơn chưa được bộ dependencies hỗ trợ.

Lần sau xem RUN_PROJECT.md; kiểm chứng Intel/macOS browser đầy đủ xem VERIFICATION.md.
