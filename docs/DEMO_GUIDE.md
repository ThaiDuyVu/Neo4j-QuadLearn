# Demo skeleton (5–7 phút)

1. `docker compose up -d --wait`, `python -m scripts.db init`, `python -m scripts.db check`, chạy Streamlit. Nói rõ skeleton, dữ liệu giả và AI mock.
2. Home → kiểm tra kết nối; sidebar có 3 domain. Không đăng ký/đăng nhập thật.
3. Vũ → tài khoản demo lớp 8; đổi dropdown xem lớp 6–9 không ghi User, không enforce unlock; xem lịch sử score từ AssessmentReader. Nêu AUTH/progress TODO.
4. Sơn → lớp 8, chọn “Hình chữ nhật và tính chất”; đọc lý thuyết và tiên quyết lớp 8→7→6; slider đổi hình chữ nhật, quan sát diện tích/chu vi. Không gọi slider là canvas kéo đỉnh hoàn chỉnh.
5. Đạt → xem attempt seed điểm 10; chọn context bài, nhập câu hỏi và gọi mock; nhãn “CHỈ LÀ MOCK”; danh sách source ids từ graph, không phải LLM thật. Quiz submit/essay/quota chưa làm.
6. Neo4j Browser: `MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100`; chạy từng câu database/examples.cypher cho REQUIRES nhiều cấp và IS_A đa cha. Chạy `python -m scripts.db init` lại, integration test kiểm count không đổi.
7. Trình bày folder owner, registry độc lập, contracts và README checklist. Mở docs/VERIFICATION.md để phân biệt đã kiểm chứng/chưa kiểm chứng.

Nếu DB không chạy, Home vẫn mở và feature báo lỗi hướng dẫn; không hiển thị dữ liệu fake như query thành công. Không dùng failover giả để tuyên bố Neo4j PASS.
