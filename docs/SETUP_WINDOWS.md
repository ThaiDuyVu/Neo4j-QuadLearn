# Setup Windows 10/11 (PowerShell)

1. Cài Git for Windows. Cài Python 3.11 từ python.org, chọn Python Launcher và Add Python to PATH. Cài Docker Desktop với WSL2 backend; bật virtualization, WSL2 theo hướng dẫn Docker Desktop, reboot nếu yêu cầu. Mở Docker Desktop; kiểm tra `docker info` và `docker compose version` trong PowerShell.
2. Clone repo thực tế (thay URL mẫu):

```powershell
git clone <URL_REPO_GITHUB_CUA_NHOM>
cd QuadLearn
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Nếu Activate bị policy chặn, dùng `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` cho cửa sổ hiện tại rồi activate. Có thể bỏ activate và gọi `.\.venv\Scripts\python.exe` thay `python` trong mọi lệnh. Không cần thay policy toàn máy.

3. Đặt `NEO4J_PASSWORD` riêng ≥8 ký tự; giữ user neo4j, database neo4j, URI bolt://localhost:7687. Mật khẩu chữ/số tránh Compose nội suy `$`. Không commit `.env`.
4. Start/seed/run:

```powershell
docker compose up -d --wait
python -m scripts.db init
python -m scripts.db check
python -m streamlit run app/main.py
```

5. Mở http://localhost:8501 và http://localhost:7474. Script thay bước venv/dependency/env: `.\scripts\setup.ps1`; sau khi đặt password, start/seed như trên, chạy `.\scripts\run.ps1`. Script dùng `py -3.11`; nếu chỉ cài 3.12, tạo venv bằng `py -3.12` thủ công. Script dùng UTF-8 và lệnh không phụ thuộc bash; khuyến nghị PowerShell 7 cho hiển thị tiếng Việt, Windows PowerShell 5 có thể hiển thị ký tự khác nhưng đường dẫn/lệnh vẫn ASCII.

Lỗi `py`/`python` không tìm thấy: cài Python Launcher, mở PowerShell mới, kiểm tra Windows App Execution Aliases. `ModuleNotFoundError`: dùng đúng venv. Docker daemon không chạy: mở Docker Desktop/WSL2. Neo4j chưa ready: `docker compose logs --tail 100 neo4j`; đợi healthcheck. Nếu `--wait` không hỗ trợ, cập nhật Docker Compose v2 hoặc `docker compose up -d`, kiểm tra `docker compose ps`, rồi `python -m scripts.db check` đến khi kết nối được. Port đã dùng: kiểm tra container khác trước khi đổi cổng; URI phải khớp Bolt host port. Password sai trên volume cũ: env không đổi password DB đã khởi tạo; xem database/README.md.

Windows chưa được chạy trực tiếp trên máy nghiệm thu hiện tại; xem VERIFICATION.md. Không dùng `down -v` khi dừng thường.
