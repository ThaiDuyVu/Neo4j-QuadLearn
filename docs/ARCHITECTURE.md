# Kiến trúc skeleton

> Trạng thái sau merge 3 domain và audit 09/10/2026: xem [báo cáo đối chiếu 86 FR, lỗi tích hợp và kiểm chứng](POST_MERGE_AUDIT_2026-10-09.md). Các bảng skeleton bên dưới là baseline; không dùng TODO cũ để kết luận phần đã triển khai hiện tại.

> Cập nhật domain Vũ: nghiệp vụ local đã phát triển sau baseline skeleton. Trạng thái mới, shared changes, tests và TODO nằm trong [VU_NGHIEP_VU_VA_GIAI_THICH_CODE.md](VU_NGHIEP_VU_VA_GIAI_THICH_CODE.md). Các kết quả/TODO skeleton bên dưới là mốc nghiệm thu ban đầu, không dùng để kết luận trạng thái hiện tại của Vũ.

Một tiến trình Streamlit chạy trên host, gọi Python service → repository → Neo4j driver → Neo4j Community trong Docker. Không REST server, microservice, Redis, SQL, queue hay event bus.

```
app/main.py → core/navigation.py → feature/registry.py → feature/pages/
                        core/bootstrap.py
                  ↙ identity  ↓ content  ↘ assessment
                         shared/contracts
                          core/database.py → Neo4j
```

`bootstrap.py` là composition root duy nhất nối implementation giữa domain. Page nhận `AppContext` có `IdentityReader`, `ContentReader`, `AssessmentReader`; không import service/repository của feature khác. Repository nhận `QueryExecutor`, không biết Streamlit. DTO bất biến; Cypher nằm trong owner repository. Test dùng fake port, không cần Docker.

`navigation.discover_pages()` tự duyệt package trong app/features và đọc `registry.PAGES`. Mỗi owner thêm `PageSpec(title, path, render)` ở registry mình. `path` duy nhất và ổn định, không phải sửa main. Feature mới phải có registry; lỗi cấu hình registry cần sửa/test, không bị âm thầm bỏ qua. Import chỉ khai báo, không mở DB. Driver được cache resource, mỗi query có session riêng và đóng driver khi process kết thúc. Không cache dữ liệu học sinh.

## Trade-off so với SRS

- Streamlit rerun thuận tiện demo Python, không cung cấp canvas kéo thả 30fps hay panel nổi sẵn. Slider/SVG là ví dụ tối thiểu. Sơn cần thử Streamlit component + thư viện geometry trước khi chọn; chưa chọn giấy phép GeoGebra.
- Session Streamlit chưa phải phiên AUTH 7 ngày. OAuth/email, RBAC, password hashing, guardian consent vẫn TODO; không dùng UI ẩn như bảo vệ quyền. Không thu thập dữ liệu trẻ em thật trong demo.
- Neo4j lưu quan hệ tiên quyết, taxonomy, history và nguồn AI bằng graph; metadata song ngữ là property. Không dùng Redis cho quota; thiết kế đếm ChatMessage theo ngày và transaction khi Đạt làm quota thật.
- Không LLM, embeddings hay RAG production. `MockAIProvider` trả cố định kèm nguồn context, không hiểu câu hỏi và không đảm bảo bộ lọc.
- Một DB local riêng mỗi người; shared schema thay đổi cần review. Cơ chế migrate dữ liệu/phiên bản sẽ thêm khi cần, hiện CLI idempotent.
- Neo4j Community uniqueness constraint không tự đảm bảo cardinality, grade, RBAC, REQUIRES acyclic; service và transaction phải kiểm tra.

## Mức hoàn thành

Có Home, ba page đọc demo, service/repository mẫu mỗi domain, protocols, constraints/indexes/seed và test nền. Không FR nào được đánh dấu hoàn thành toàn bộ. Danh sách đầy đủ: SRS_TRACEABILITY.md, PRODUCT_BACKLOG.md; quyết định chưa chốt: OPEN_QUESTIONS.md.

## Nguồn kỹ thuật

Navigation callable theo [Streamlit st.Page](https://docs.streamlit.io/1.46.0/develop/api-reference/navigation/st.page) và [st.navigation](https://docs.streamlit.io/1.44.0/develop/api-reference/navigation/st.navigation). Cấu hình Neo4j theo [Docker manual](https://neo4j.com/docs/operations-manual/current/docker/) và [initial authentication](https://neo4j.com/docs/operations-manual/current/docker/introduction/). Pin phiên bản là baseline đồ án đã chọn, không tuyên bố phiên bản mới nhất.
