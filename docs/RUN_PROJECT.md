# Chạy và quản lý dự án

Lần đầu làm SETUP_WINDOWS.md hoặc SETUP_MACOS.md. Mỗi người có `.env`, Docker volume và DB local độc lập. Chạy lệnh ở root.

## Chạy lại

```bash
# macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Các lệnh sau giống nhau trên hai OS:

```
docker compose up -d --wait
python -m scripts.db check
python -m streamlit run app/main.py
```

Không phải seed mỗi lần; chỉ `python -m scripts.db init` lần đầu hoặc sau thay đổi fixtures đã review. Streamlit http://localhost:8501. Browser http://localhost:7474 → neo4j / password trong .env; không đưa password vào URL.

## Kiểm tra / test

```
docker compose ps
docker compose logs --tail 100 neo4j
python -m pip check
python -m compileall -q app scripts
python -m pytest -m "not integration"
python -m pytest -m integration
python -m scripts.db queries
```

Integration yêu cầu DB và seed; bật bằng `QUADLEARN_INTEGRATION=1` (biến test tùy chọn, không config ứng dụng):

```bash
QUADLEARN_INTEGRATION=1 python -m pytest -m integration
```

```powershell
$env:QUADLEARN_INTEGRATION="1"
python -m pytest -m integration
Remove-Item Env:QUADLEARN_INTEGRATION
```

Nếu không bật biến, test integration SKIP để không vô tình ghi DB. Test có reseed idempotency chỉ nên dùng DB demo local. Unit/smoke không cần DB; page tests inject fake contracts.

`docker compose config --quiet` kiểm tra cấu hình nhưng cần .env có password. Tránh in `docker compose config` đầy đủ vì chứa secret. `check` thất bại thì kiểm tra `.env`, Docker logs, chưa được xem là PASS. Lỗi chưa có data: chạy init.

## Dừng / reset

Ctrl+C dừng Streamlit; `deactivate` thoát venv. `docker compose stop` dừng Neo4j, giữ dữ liệu; `docker compose start` bật lại; `docker compose down` gỡ container/network, giữ named volumes.

**Xóa demo có chủ đích**: `python -m scripts.db reset --yes` ở APP_ENV=development xóa mọi node demo và cạnh nối rồi seed. Không dùng với dữ liệu thật nối fixture. **`docker compose down -v` xóa toàn bộ dữ liệu volumes**, không phải lệnh stop thường. Reset CLI không reset password/volume. Backup trước thao tác phá hủy; hướng dẫn production backup chưa thuộc skeleton.

## Khi vừa pull/merge thay đổi Python core

Nếu Streamlit đang chạy từ bản code cũ, dừng process bằng Ctrl+C rồi chạy lại `python -m streamlit run app/main.py`. Rerun/refresh trình duyệt không đảm bảo Python modules và đối tượng `st.cache_resource` đã được nạp lại. Lỗi `Database object has no attribute transaction` có thể do driver object từ phiên trước merge; source hiện tại có phương thức transaction. Restart ứng dụng không xóa database/volume.

Giao diện dùng tên chức năng; tên thành viên chỉ nằm trong source comments và tài liệu phân công. Admin local đã được tạo trên máy hiện tại: `admin@quadlearn.local`. Tài khoản này không nằm trong seed chung; máy thành viên khác dùng CLI create-admin trong tài liệu Vũ để tạo riêng.

## Chuẩn bị dữ liệu để demo

Chạy `python -m scripts.demo_data` sau lần `db init` đầu tiên. Xem [DEMO_DATA.md](DEMO_DATA.md) để lấy bảy tài khoản thử nghiệm và [DEMO_GUIDE.md](DEMO_GUIDE.md) để thao tác. Lệnh `python -m scripts.demo_data --reset-demo-users --yes` xóa và tạo lại **chỉ tài khoản fixture và lịch sử riêng của chúng**; không cần xóa volume/database.
