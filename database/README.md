# Database local

Neo4j Community `5.26.0-community`, không APOC. Python driver chính thức chạy scripts với thông tin `.env`; không truyền mật khẩu bằng CLI.

```
python -m scripts.db check
python -m scripts.db init
python -m scripts.db queries
```

`init`: verify connection → constraints → indexes → seed. Mỗi file seed một transaction; DDL riêng. Chạy lại không tăng bản ghi/cạnh nhưng SET lại dữ liệu demo. Không dùng seed để migrate dữ liệu thật. `examples.cypher`: mỗi câu kết thúc bằng **dòng riêng `;`**; helper chỉ hỗ trợ quy ước này, không parser Cypher tổng quát. Không đặt dòng chỉ `;` bên trong string literal.

Sau seed, `init` cũng chạy `taxonomy_conditions.cypher` để ghi điều kiện đủ vào `IS_A.condition_vi`. Với database đã có dữ liệu, dùng `python -m scripts.db annotate` để chỉ cập nhật chú thích 9 cạnh mẫu, giữ nguyên bài học/tài khoản/tiến độ; không cần seed hoặc reset lại.

Browser: http://localhost:7474, Bolt bolt://localhost:7687, username neo4j, mật khẩu do bạn đặt trong `.env`. `NEO4J_DATABASE` mặc định neo4j; giữ tên mặc định cho nhóm. Community một database ứng dụng, không multi-tenant từ xa.

Reset có chủ đích: `python -m scripts.db reset --yes` chỉ chạy ở APP_ENV=development, **xóa node demo=true và mọi cạnh nối**, sau đó seed lại. Nó không xóa node khác, nhưng cạnh dữ liệu thật nối demo cũng mất; không trộn dữ liệu thật với demo. `reset_dev.cypher` paste trực tiếp không có guard CLI, cẩn thận.

`docker compose stop`/`down` không xóa volume. **`docker compose down -v` xóa toàn bộ volume/data dự án**, không dùng khi dừng thường. Đổi mật khẩu `.env` không đổi password volume Neo4j đã khởi tạo; giữ mật khẩu cũ hoặc đổi bằng Neo4j Browser và cập nhật `.env`. Không reset volume để “sửa lỗi” trước khi sao lưu.

Schema/owner/ID/cardinality: [GRAPH_SCHEMA](../docs/GRAPH_SCHEMA.md). Constraints uniqueness không tự validate grade/relationship. Chỉ tạo index phù hợp skeleton, chưa tối ưu tải sản phẩm.

## Bộ demo mở rộng

Sau graph nền, chạy `python -m scripts.demo_data` để thêm học liệu và tài khoản đăng nhập. Dữ liệu nguồn ở `demo/content.json`; [DEMO_DATA.md](../docs/DEMO_DATA.md) giải thích từng tài khoản, đáp án và phạm vi reset. Chạy lại giữ trạng thái các tài khoản đã tạo. `db init` cập nhật seed gốc nên chạy tiếp `demo_data` nếu muốn nội dung mở rộng.
