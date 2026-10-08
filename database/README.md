# Database local

Neo4j Community `5.26.0-community`, không APOC. Python driver chính thức chạy scripts với thông tin `.env`; không truyền mật khẩu bằng CLI.

```
python -m scripts.db check
python -m scripts.db init
python -m scripts.db queries
```

`init`: verify connection → constraints → indexes → seed. Mỗi file seed một transaction; DDL riêng. Chạy lại không tăng bản ghi/cạnh nhưng SET lại dữ liệu demo. Không dùng seed để migrate dữ liệu thật. `examples.cypher`: mỗi câu kết thúc bằng **dòng riêng `;`**; helper chỉ hỗ trợ quy ước này, không parser Cypher tổng quát. Không đặt dòng chỉ `;` bên trong string literal.

Browser: http://localhost:7474, Bolt bolt://localhost:7687, username neo4j, mật khẩu do bạn đặt trong `.env`. `NEO4J_DATABASE` mặc định neo4j; giữ tên mặc định cho nhóm. Community một database ứng dụng, không multi-tenant từ xa.

Reset có chủ đích: `python -m scripts.db reset --yes` chỉ chạy ở APP_ENV=development, **xóa node demo=true và mọi cạnh nối**, sau đó seed lại. Nó không xóa node khác, nhưng cạnh dữ liệu thật nối demo cũng mất; không trộn dữ liệu thật với demo. `reset_dev.cypher` paste trực tiếp không có guard CLI, cẩn thận.

`docker compose stop`/`down` không xóa volume. **`docker compose down -v` xóa toàn bộ volume/data dự án**, không dùng khi dừng thường. Đổi mật khẩu `.env` không đổi password volume Neo4j đã khởi tạo; giữ mật khẩu cũ hoặc đổi bằng Neo4j Browser và cập nhật `.env`. Không reset volume để “sửa lỗi” trước khi sao lưu.

Schema/owner/ID/cardinality: [GRAPH_SCHEMA](../docs/GRAPH_SCHEMA.md). Constraints uniqueness không tự validate grade/relationship. Chỉ tạo index phù hợp skeleton, chưa tối ưu tải sản phẩm.
