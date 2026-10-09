# Sơn – learning_geometry

> Audit sau merge: [trạng thái SRS và vấn đề cần owner review](../../../docs/POST_MERGE_AUDIT_2026-10-09.md). Thay đổi audit ở branch `fix/post-merge-integration-audit`; chưa merge main.

## 1. Owner và mục tiêu

Sơn sở hữu `app/features/learning_geometry/`. Learning Content & Geometry: catalog, nội dung, taxonomy và hình minh họa. Đây là skeleton, **không FR nào hoàn tất toàn bộ**. Service/repository/page demo hoạt động với Neo4j seed; các chức năng bên dưới TODO.

## 2. FR liên quan và ưu tiên SRS

| FR-ID | Công việc nghiệp vụ | Ưu tiên | Trách nhiệm |
|---|---|---|---|
| FR-LRN-01 | Hiển thị cây cấp độ (lớp) → chương → bài → mục theo lộ trình | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-02 | Hiển thị bài lý thuyết: định nghĩa, tính chất, dấu hiệu nhận biết, công thức (hỗ trợ công thức toán LaTeX) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-03 | Nhúng minh họa hình động trong bài (xem 3.3), có nút phát/dừng/đặt lại | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-04 | Sơ đồ quan hệ giữa các loại tứ giác (hình vuông ⊂ chữ nhật, thoi ⊂ bình hành…) có thể nhấn vào từng loại | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LRN-05 | Đánh dấu "đã học xong" từng bài; điều hướng bài trước/sau | M | Chủ trì; Sơn điều hướng; Vũ ghi COMPLETED qua ProgressWriter (TODO). |
| FR-LRN-06 | Ghi chú cá nhân trên bài học | C | Chủ trì; Sơn sở hữu ghi chú; User chỉ là tham chiếu. |
| FR-LRN-07 | Tìm kiếm bài học và thuật ngữ | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-01 | Bảng vẽ tương tác: tạo điểm, đoạn thẳng, đường thẳng, đường tròn | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-02 | Tạo nhanh các loại tứ giác (hình thang, thang cân, bình hành, chữ nhật, thoi, vuông, nội tiếp) với ràng buộc hình học đúng | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-03 | Kéo thả đỉnh; hình giữ đúng tính chất (ví dụ kéo đỉnh hình bình hành thì cạnh đối vẫn song song) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-04 | Hiển thị số đo: độ dài cạnh, góc, đường chéo, chu vi, diện tích; cập nhật theo thời gian thực | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-05 | Công cụ: trung điểm, đường vuông góc, đường song song, phân giác, giao điểm | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-06 | Bật/tắt hiển thị tính chất (hai đường chéo, góc bằng nhau, cạnh bằng nhau bằng ký hiệu) | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-07 | Hoàn tác / làm lại (Undo/Redo), xóa, đặt lại bảng | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-08 | Bài thực hành có hướng dẫn: đề yêu cầu "kéo hình để quan sát…", hệ thống kiểm tra kết quả | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-09 | Lưu và tải lại hình vẽ của HS; xuất ảnh PNG | C | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-GEO-10 | Hỗ trợ cảm ứng (kéo, phóng to/thu nhỏ) trên thiết bị di động | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AD-02 | Import hàng loạt từ Excel (.xlsx) và JSON: chủ đề, bài lý thuyết, câu trắc nghiệm, đề tự luận, bước gợi ý, kèm nhãn lớp, mức nhận thức và kiến thức tiên quyết | M | Chủ trì; Sơn điều phối; Đạt validate/ghi Question, Option, Essay, Hint. |
| FR-AD-03 | Kiểm tra dữ liệu trước khi nhập (validate): báo lỗi theo dòng/ô, không nhập nếu lỗi nghiêm trọng | M | Chủ trì; Mỗi domain validate phần mình; Sơn tổng hợp báo cáo. |
| FR-AD-04 | Tải file mẫu import cho từng loại nội dung | M | Chủ trì; Sơn mẫu lesson; Đạt mẫu question/essay. |
| FR-AD-05 | Xem trước nội dung sau import; trạng thái Nháp / Đã xuất bản | M | Chủ trì; Sơn lesson; Đạt question/essay, không ghi chéo. |
| FR-AD-06 | Xuất bản, gỡ bản, sửa từng mục nội dung và lưu phiên bản | S | Chủ trì; Version thuộc owner từng loại nội dung. |
| FR-AD-07 | Quản lý hình động: nhập cấu hình hình (JSON mô tả hình học) kèm bài học | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AD-08 | Nhật ký import (người thực hiện, thời gian, số bản ghi thành công/lỗi) | S | Chủ trì; Sơn sở hữu ImportLog; domain khác báo kết quả qua contract TODO. |
| FR-I18-01 | Chuyển đổi Việt/Anh ở mọi màn hình; ghi nhớ lựa chọn theo tài khoản | M | Chủ trì; Sơn bộ dịch UI; Vũ ghi User.language; mỗi owner dịch page mình. |
| FR-I18-02 | Nội dung học có trường song ngữ (vi, en); nếu thiếu bản Anh thì hiển thị bản Việt kèm thông báo | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-I18-03 | Định dạng ngày, số theo ngôn ngữ | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-03 | Lộ trình hiển thị theo cấp độ; mỗi chủ đề/bài/câu hỏi gắn nhãn lớp và mức nhận thức | M | Phối hợp, không ghi hộ owner; Vũ hiển thị lộ trình; Sơn metadata; Đạt metadata câu hỏi. |
| FR-LV-04 | Cùng một loại tứ giác hiển thị nội dung khác nhau theo cấp độ (lớp 6: mô tả trực quan; lớp 7–8: tính chất; lớp 8–9: chứng minh) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-LV-07 | Mỗi bài hiển thị kiến thức tiên quyết (liên kết về bài nền ở cấp dưới) | S | Phối hợp, không ghi hộ owner; Vũ hiển thị/gợi ý; Sơn ghi REQUIRES. |
| FR-LV-08 | Khi điểm một chủ đề < 5/10, gợi ý ôn các bài tiên quyết ở cấp thấp hơn | S | Phối hợp, không ghi hộ owner; Vũ gợi ý; Đạt cung cấp điểm; Sơn cung cấp tiên quyết. |
| FR-LV-09 | Bộ công cụ hình học động thích ứng theo cấp độ (lớp 6 rút gọn, các cấp cao mở thêm công cụ) | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |

M = Must, S = Should, C = Could của sản phẩm; skeleton hoãn cả các Must phức tạp. Ánh xạ toàn bộ: `docs/SRS_TRACEABILITY.md`; stories/acceptance: `docs/PRODUCT_BACKLOG.md`. Giữ đúng business rules ở hai tài liệu này, không suy ra từ mock.

## 3. Màn hình

SCR-05/06/14/15; nội dung cây SCR-04 phối hợp Vũ. Page hiện tại chỉ là overview/demo, không phải toàn bộ màn hình SRS. Tạo thêm page riêng và đăng ký trong registry của mình.

## 4. Graph ownership và queries

Level, Chapter, Topic, Lesson, Quadrilateral, GeometryConfig, ImportLog; HAS_CHAPTER/TOPIC/LESSON, REQUIRES, RELATED_TO, IS_A, ABOUT, ILLUSTRATED_BY. Xem `docs/GRAPH_SCHEMA.md` cho endpoint/cardinality và ID. Queries cần làm: Cây Level→Chapter→Topic→Lesson; REQUIRES đa cấp, bài cùng ABOUT shape, IS_A đa cha, context published; import MATCH endpoints+MERGE tránh vòng. Không query User progress hoặc Option correct trong content repo.

Không ghi node/cạnh owner khác. Các cạnh tham chiếu User/Topic chỉ được ghi theo bảng ownership. Query tham số `$id/$grade`, MATCH endpoint tồn tại trước MERGE; constraint không tự validate business.

## 5. Services và file bắt đầu

ContentService/rectangle demo đang có; ImportValidationService/ContentImportService/TranslationService/GeometryAdapter (TODO).

Mở các file: `registry.py; pages/overview.py; pages/interactive_board.py; services/content.py; services/geometry.py; repositories/content.py; examples/; tests/test_content.py` (tương đối trong folder này). Thêm page/service/repository/model/test trong thư mục tương ứng; thêm PageSpec ở `registry.py`. Không phải sửa `app/main.py`. Tests/fakes đọc ports chung; không dùng query database thật trong unit.

## 6. Input/output contracts và dependencies

Cung cấp ContentReader → lessons/prerequisites/ai_context; nhận IdentityReader để quyền/ngôn ngữ. Ghi completion phải qua ProgressWriter của Vũ (TODO). Import assessment qua contract Đạt (TODO).

DTO ở `app/shared/models/dto.py`, ports ở `app/shared/contracts/ports.py`. Empty list/None có nghĩa không có dữ liệu; lỗi kết nối không được đổi thành dữ liệu giả. `core/bootstrap.py` nối implementation. Không import repository/service domain khác; readers truyền qua AppContext. Shared API mới phải cả nhóm review và có test consumer/provider trước merge.

## 7. Thứ tự triển khai và checklist

Đọc SRS mapping → chốt câu hỏi domain → bổ sung model/repository → test service qua fake ports → thêm page/registry → chạy test domain → demo Neo4j → PR. Làm Must trước Should/Could; chia PR nhỏ theo chức năng, không đánh dấu checklist chỉ vì có placeholder.

### Must

- [ ] Thêm repository catalog có thứ tự Chapter/Topic/Lesson và trạng thái draft/published.
- [ ] Soạn lớp 8 lõi sau khi chốt SGK, metadata cognitive và bản Việt bắt buộc.
- [ ] Hiển thị định nghĩa/tính chất/công thức bằng LaTeX và điều hướng bài trước/sau.
- [ ] Thêm validated JSON importer: topic tồn tại, grade hợp lệ, tiên quyết cùng/lớp dưới và không vòng.
- [ ] Tạo preview/báo lỗi theo dòng, ghi draft transaction và ImportLog.
- [ ] Dựng geometry spike giữ ràng buộc hình và chống suy biến; phân biệt mô phỏng hiện tại với công cụ dựng hình đầy đủ.
- [ ] Thêm fallback Anh→Việt có thông báo, UI labels song ngữ qua shared convention.
- [ ] Gọi ProgressWriter khi đánh dấu đã học; không tự ghi COMPLETED.
- [ ] Viết test grade sai, content unpublished bị loại, import thiếu Việt/prerequisite sai, geometry suy biến.

### Should

- [ ] Hiển thị taxonomy IS_A click đến bài phù hợp cấp độ.
- [ ] Thêm tìm kiếm bài/thuật ngữ, quản lý version/publish sau quyền admin.
- [ ] Chuẩn bị .xlsx parser/header và chuyển payload question/essay cho Đạt.
- [ ] Thêm công cụ trung điểm/song song/vuông góc theo lớp và bài thực hành có kiểm kết quả.

### Could

- [ ] Thiết kế lưu ghi chú cá nhân tham chiếu User; review schema trước.
- [ ] Lưu/tải hình và xuất PNG sau khi geometry core chạy đúng.

## 8. Tiêu chí hoàn thành

Content: cây đúng metadata/trạng thái, công thức Việt/Anh và fallback có test. Import: lỗi không ghi, preview→draft→publish có permission và log, không ghi assessment. Geometry: ràng buộc đúng khi kéo và không suy biến, demo cảm ứng; canvas hiện chưa đủ nghiệm thu GEO. Không công bố full content lớp 6–9 với bộ bài demo.

Mỗi nhóm chức năng cần PR review, tests happy/error/boundary và demo đúng tiêu chí FR/PB liên quan. Ghi TODO phần chưa làm. DoD staging/70% coverage/UAT của SRS là mục tiêu sản phẩm, chưa được skeleton chứng nhận; đừng ghi “PASS SRS” chỉ vì unit tests nền pass.

## 9. Test riêng

```text
python -m pytest app/features/learning_geometry/tests -q
python -m pytest tests/test_boundaries.py tests/test_navigation.py -q
```

Test domain không cần Neo4j. Khi DB demo sẵn, bật `QUADLEARN_INTEGRATION=1` và chạy integration theo docs/RUN_PROJECT.md. Smoke pages dùng fake contracts; kiểm UI thật thêm qua sidebar. Test không phải full FR acceptance.

## 10. Demo

Chọn lớp 8, đọc hình chữ nhật và REQUIRES qua lớp 7/6; mở tab Thực hành hình học, nhập thông số hoặc kéo đỉnh để xem S/P; Browser xem square IS_A rectangle/rhombus. Hướng dẫn demo chung: `docs/DEMO_GUIDE.md`. Nếu DB chưa chạy, page báo lỗi hướng dẫn; không báo kết nối PASS giả.

## 11. Giới hạn sửa file

Được sửa folder mình và các file mới trong đó. Không sửa folder hai bạn khác, không trực tiếp query/ghi nội bộ họ. `app/core`, `app/shared`, `database`, `.env.example`, `compose.yaml`, dependencies và docs kiến trúc là vùng chung: thông báo cả nhóm, giải thích tương thích, review trước merge. File `.env` local không commit. Registry path không trùng; không hardcode secret/data HS thật. Git cá nhân: GIT_WORKFLOW.md.

### Tổ chức giao diện Nội dung & Hình học

`pages/overview.py` giữ bộ chọn lớp/bài và ba tab Lý thuyết, Kiến thức nền, Thực hành hình học. `pages/interactive_board.py` chứa component HTML/SVG/JS: hình vẽ, thông số, nhận diện và kết quả. File `pages/geometry_board.py` cũ được giữ nguyên cho điểm tích hợp riêng. Khi chỉnh bố cục component responsive, chuyển tọa độ chuột qua SVG screen matrix để kéo đỉnh đúng vị trí. Mô phỏng hiện chưa giữ ràng buộc hình khi kéo tự do, chưa hỗ trợ đầy đủ touch/chống suy biến.

Kiểm chứng bố cục ngày 09/10/2026: 184 unit/UI tests PASS; trang render bằng AppTest với Neo4j thật; JavaScript chạy năm cấu hình hình mẫu với kết quả S/P đúng. Chưa kiểm chứng trực quan bằng trình duyệt trong lần này do công cụ browser gặp lỗi. Kéo đỉnh sau khi đổi kích thước hiển thị dùng SVG screen matrix; nhận diện là mô phỏng gần đúng, chưa nghiệm thu đầy đủ GEO.

### Trang Sơ đồ tri thức hình học

Mở `/geometry-knowledge` từ menu. `pages/knowledge_graph.py` tổ chức giao diện và gọi `ctx.content.geometry_graph()` qua contract ContentReader. `services/content.py` nối repository taxonomy, `repositories/taxonomy.py` đọc node Quadrilateral cùng cạnh IS_A trong một Cypher query. `services/knowledge_graph.py` lọc phạm vi/số bước trên graph đã đọc và tạo DOT an toàn. Không hardcode danh sách hình, không tạo quan hệ bắc cầu hoặc ghi DB từ page.

Chế độ toàn bộ giữ cả node cô lập. Chế độ một hình có hướng lên loại tổng quát, xuống các hình cụ thể hoặc cả hai. Một số bước theo cả hai hướng có thể đưa vào các hình cùng chung loại tổng quát; đây là vùng liên quan, không khẳng định tất cả đều là cha/con của hình đang chọn. Mũi tên luôn giữ hướng nguồn → đích của DB. Có thể tải DOT hoặc đối chiếu bằng Cypher trong expander. Streamlit dựng sơ đồ từ chuỗi DOT; không thêm dependency hoặc cần cài Graphviz binary trên host.

Test riêng: `python -m pytest -q app/features/learning_geometry/tests/test_knowledge_graph.py`.
### Chú thích điều kiện trên sơ đồ

`TaxonomyRepository.geometry_graph()` đọc `IS_A.condition_vi`; `services/knowledge_graph.py` đưa chú thích lên đường nối và tooltip; `pages/knowledge_graph.py` giải thích chiều đọc và hiển thị bảng điều kiện. Dấu `+` là điều kiện đủ để hình tổng quát trở thành hình đặc biệt, ngược chiều mũi tên IS_A. Điều kiện thuộc dữ liệu Neo4j, không hardcode trong giao diện. Nguồn demo: `database/taxonomy_conditions.cypher`; cập nhật database cũ bằng `python -m scripts.db annotate`. Khi bổ sung quan hệ mới, lưu chú thích cùng cạnh.
