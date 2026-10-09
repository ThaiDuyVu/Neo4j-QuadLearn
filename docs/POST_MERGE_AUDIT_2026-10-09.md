# Rà soát tổng thể sau khi merge 3 domain — 09/10/2026

## 1. Kết luận

Project đúng hướng kiến trúc bài tập Neo4j: Streamlit host, một database local, feature folders, contracts, composition root và graph nhiều cấp. **Chưa đáp ứng toàn bộ SRS v1.1 và chưa đủ nghiệm thu MVP.** Các test sau merge chỉ xác nhận phần đã triển khai; không chứng minh các Must còn TODO hoặc NFR đã đạt.

Nguồn đọc: file DOCX SRS v1.1 trong Downloads (FR, 5 UC, dữ liệu §4, screens, 56 PB, A/Q, NFR/DoD), README root/3 domain, workflow chung và từng người, ARCHITECTURE, GRAPH_SCHEMA, DOMAIN_OWNERSHIP, FEATURE_INTEGRATION, SRS_TRACEABILITY, OPEN_QUESTIONS, tài liệu Vũ và merge Sơn. 86 FR gốc đều có mặt trong SRS_TRACEABILITY; ownership không bị mất sau merge. Stack thương mại của SRS chỉ tham khảo; Neo4j/Streamlit vẫn theo yêu cầu đồ án, không thêm SQL/Redis/LLM trả phí.

Baseline rà soát: main `ae03ca0`, chứa merge Vũ #3, Đạt #1, Sơn #2. Sửa kiểm toán nằm trên branch `fix/post-merge-integration-audit`; không tự merge main trong đợt rà soát. Một số lỗi đã tồn tại trong branch riêng, chỉ bộc lộ khi nối runtime, không quy mọi lỗi cho Git merge.

## 2. Các lỗi đã sửa trong đợt rà soát

| ID / mức | Trước sửa / tác động | Sửa tại đâu / kiểm chứng |
|---|---|---|
| F1 — Cao | Bootstrap không truyền quyền Vũ vào AssessmentService. ID string có thể gọi writers, demo read-only vẫn ghi quiz/chat, import/preview không enforce admin ở facade. | `core/bootstrap.py` bind IdentityActions; `assessment_ai/services/assessment.py` guard writes/admin/own reads. Unbound facade từ chối writes. UI demo disable persistent actions. 24 biến thể deny-write + admin/read tests, integration demo và user bị block. |
| F2 — Cao | Son content helper nuốt Exception, tự dựng bài khi không có ID/DB; topic_id flat sai graph, có thể đọc draft qua helper. | `learning_geometry/repositories/content.py`: bỏ fake fallback, missing→None, lỗi driver truyền lên; helpers dùng reader graph chung. Published filter + metadata áp dụng nhất quán catalog/content và projection completion. Integration draft parent excluded. |
| F3 — Vừa | AI link `/learning?lesson_id=...` không chọn nguồn, luôn mở mặc định lớp 8/bài đầu. | Son overview đọc query param, chọn đúng grade/ID, kiểm quyền cấp độ nếu có ctx.progress. AppTest link lớp 7 chọn đúng bài. |
| F4 — Vừa | lesson_view dùng `ctx.progress_writer` không tồn tại; xem return None của ProgressWriter như thất bại và có thông báo demo giả “đã gửi”. | Dùng ctx.progress, thành công khi không exception, disable guest/demo; test void contract. Trang này vẫn chưa registered, không gọi toàn bộ lesson UI hoàn tất. |
| F5 — Vừa | Hình thang: a=8 → slider b có min=9 nhưng default=7, Streamlit ném lỗi. | default=max(a+1,7), AppTest biên a=8. |
| F6 — Vừa | Kéo đỉnh D bị tính lại từ A/B/C nên bỏ qua tọa độ người dùng đưa vào. | geometry_core giữ D và giải C=B+D−A, unit test D(2,3)→C(6,3). Helper chưa là canvas UI. |
| F7 — Vừa | Content importer không có driver vẫn trả True/demo_success; runtime có EssayReview/AIQuotaDay nhưng constraints file chưa khai báo. | Import không DB báo lỗi; bổ sung uniqueness constraints chung. Chưa sửa toàn workflow import, xem R1. |
| F8 — Nhẹ | main bắt mọi ValueError thành lỗi Neo4j, người học không thấy lỗi phân quyền/nghiệp vụ thật. | ValueError hiện thông báo nghiệp vụ; driver errors vẫn hiện hướng dẫn kết nối. |

FakeIdentity trong test authenticated hiện ghi rõ demo=False; demo-readonly được test riêng với demo=True. Test admin import phải inject fake admin; không bỏ kiểm quyền để làm test pass. Không import nội bộ feature khác để kiểm quyền.

## 3. Rủi ro/khoảng trống còn lại — cần owner xử lý

| ID / mức / owner | Bằng chứng source và tác động | Việc cần làm |
|---|---|---|
| R1 — Cao — Sơn | `services/content_import.py`: validator không kiểm Topic/prereq tồn tại trong graph; MATCH thiếu endpoint âm thầm bỏ row nhưng trả imported_count=len(payload). Prereq mới cùng batch xử lý theo thứ tự chưa đảm bảo. Không xóa REQUIRES cũ khi sửa. Log ghi transaction riêng; string title được validator chấp nhận nhưng query dùng map title.vi. | Chốt schema import (topic_code/id), normalize, validate graph toàn batch trong transaction, reject mọi endpoint thiếu, count thực tế, cycle trên graph hiện có, log cùng transaction. UI hiện chỉ parse JSON nên không được công bố UC-03 hoàn tất. |
| R2 — Cao nếu nối ghi — Sơn/Vũ/Đạt | `pages/admin_import.py` chưa có role guard, confirmation/preview/write; ContentImportService/ImportLogRepository chưa bind identity runtime. Dat facade giờ đã guard admin nhưng chưa có port CMS tổng hợp. | Trước khi register write UI: require_user(admin=True), ctx hợp đồng import, templates/schema chung và test student/guest denied. Không trực tiếp gọi subservice/repository để bỏ facade guard. |
| R3 — Vừa — cả nhóm | `ports.AssessmentReader` chỉ có attempts trong khi implementation đã có history/detail/placement/import nhiều hàm; Vũ README nói thiếu timestamps nhưng Đạt đã có attempt_history. `ContentReader` chưa khai báo get_lesson mà implementation có. | Review mở rộng ports/DTO có kiểu rõ; consumer tests; nối PG-02/03 và placement theo contract, không query repository Đạt từ Vũ. |
| R4 — Vừa — Đạt/Vũ | Guard identity kiểm trước transaction assessment, nhưng các tx repository không recheck status/verified/auth_version. Admin khóa đúng lúc giữa guard và commit vẫn là race. Raw subservices dùng trong test không tự kiểm quyền. | Recheck active/consent/version trong tx writer theo authorization contract, hoặc policy session snapshot shared; test concurrent revoke. Hiện đã chặn phiên bị khóa trước thao tác, chưa chứng nhận chống race production. |
| R5 — Vừa — Sơn | Registry chỉ overview. lesson_view/learning_tree/geometry_board/admin_import là file không có route riêng; TranslationService chưa được pages dùng đồng bộ. Geometry đầy đủ vẫn chưa nối. | PR từng màn hình có permission/navigation/contract test; không thêm registry entry cho import trước khi R1/R2 giải quyết. |
| R6 — Vừa — Đạt/Vũ | Quiz writers kiểm Topic.grade bằng User current STUDIES_AT, UI chỉ user.grade. Xem bài cấp dưới được nhưng làm bài cấp dưới phải đổi current grade; không có chọn grade assessment độc lập. | Chốt access tới quiz theo available level; test chuyển cấp giữ draft/history và luyện tập cấp dưới. Không tự đổi A7/Q4. |
| R7 — Vừa — Vũ | Progress average_score là snapshot, Dat submit không cập nhật projection ngay. levels/access tính live nên đúng, Browser đọc Progress có thể thấy điểm cũ tới refresh/complete. | Document source of truth, refresh qua ProgressWriter sau kết quả nếu muốn; không cho Dat ghi Progress. Ngưỡng/all/latest vẫn policy tạm thời. |
| R8 — Nhẹ — shared | Hai PageSpec (navigation dataclass và shared Pydantic) + adapter; Chapters seed thiếu status nên đọc dùng coalesce(...,'published'). | Chốt một PageSpec khi refactor có review. Chốt migration Chapter.status; hiện không tự migrate nội dung ngoài fixture. |

Các mục email/OAuth, guardian thực tế, xóa account liên domain, canvas/touch, i18n toàn hệ thống, CMS/versioning, LLM thật và NFR/UAT là **chưa triển khai**, không phải conflict Git cần “chọn ours/theirs”. Không tự hoàn thiện tất cả FR trong audit.

## 4. Luồng end-to-end đã kiểm chứng

`tests/test_post_merge_integration.py` tạo user UUID giả rồi dùng **build_context thật**: register/activate/login Vũ → get_lesson/context Sơn → quiz submit/detail Đạt → start/complete/resume/projection/unlock Vũ → chat mock/sources/feedback Đạt. Kiểm own read/admin denial, revoke khi User blocked, demo denied writes. Cleanup chỉ dữ liệu user/UUID fixture, không reset seed/volume.

`tests/test_post_merge_contracts.py` kiểm boundary bằng fake ports + Streamlit AppTest: spoof user, admin permissions, DB error/no invented content, link nguồn đúng, void progress contract, slider biên, kéo D, import không DB. Đây là test lỗi quan sát được, không thay cho full UAT/NFR.

## 5. Neo4j dữ liệu local

Kiểm tra đọc tổng hợp sau test; không xuất tên/email/hash/token. Kết quả:

| Kiểm tra | Số trường hợp |
|---|---|
| `content_grade_mismatch` | 0 |
| `prerequisite_cycles_up_to_8` | 0 |
| `prerequisite_higher_grade` | 0 |
| `multiple_or_missing_current_level` | 0 |
| `selected_option_wrong_question` | 0 |
| `duplicate_completed_pairs` | 0 |
| `orphan_attempts` | 0 |
| `orphan_chat_messages` | 0 |
| `draft_lessons` | 0 |

Cycle query giới hạn 8 cạnh, phù hợp query reader hiện tại; 0 không chứng minh graph mọi độ dài không vòng. Database hiện chỉ có dataset local, không đại diện tất cả dữ liệu 3 máy thành viên. AIQuotaDay dùng user_id property vì truy vấn theo cặp user/ngày, EssayReview là node riêng vì nhiều lần đánh giá; thuộc Đạt, không sửa User/Progress. Constraint migration đã chạy IF NOT EXISTS, không xóa dữ liệu.

## 6. Bảng đối chiếu toàn bộ 86 FR

LOCAL = có nghiệp vụ chạy/test trong môi trường đồ án; MỘT PHẦN = chỉ một phần hoặc service/mock chưa đủ UI; TODO = chưa có workflow theo FR. **Không có nhãn “PASS toàn bộ SRS”**. Ưu tiên M/S/C giữ nguyên từ DOCX; skeleton ban đầu được phép hoãn Must phức tạp.

| FR-ID | Ưu tiên SRS | Chủ trì/phối hợp | Trạng thái | Đối chiếu thực tế |
|---|---|---|---|---|
| FR-AUTH-01 | M | Vũ | LOCAL | AuthService/IdentityService; Argon2, token/session, lockout đã test. Session raw ở Streamlit, chưa remember-me browser. |
| FR-AUTH-02 | M | Vũ | LOCAL | AuthService/IdentityService; Argon2, token/session, lockout đã test. Session raw ở Streamlit, chưa remember-me browser. |
| FR-AUTH-03 | M | Vũ | MỘT PHẦN | Token lifecycle local; chưa gửi email thật, guardian dev không chứng minh đồng ý phụ huynh thực tế. |
| FR-AUTH-04 | M | Vũ | LOCAL | AuthService/IdentityService; Argon2, token/session, lockout đã test. Session raw ở Streamlit, chưa remember-me browser. |
| FR-AUTH-05 | M | Vũ | TODO | OAuth/liên kết account và xóa toàn bộ dữ liệu cá nhân chưa có workflow. |
| FR-AUTH-06 | M | Vũ | MỘT PHẦN | Token lifecycle local; chưa gửi email thật, guardian dev không chứng minh đồng ý phụ huynh thực tế. |
| FR-AUTH-07 | M | Vũ | LOCAL | AuthService/IdentityService; Argon2, token/session, lockout đã test. Session raw ở Streamlit, chưa remember-me browser. |
| FR-AUTH-08 | M | Vũ | LOCAL | AuthService/IdentityService; Argon2, token/session, lockout đã test. Session raw ở Streamlit, chưa remember-me browser. |
| FR-AUTH-09 | S | Vũ | MỘT PHẦN | Tên, language, avatar URL và chuyển lớp có; upload/i18n toàn UI chưa có. |
| FR-AUTH-10 | S | Vũ | LOCAL | AuthService/IdentityService; Argon2, token/session, lockout đã test. Session raw ở Streamlit, chưa remember-me browser. |
| FR-AUTH-11 | S | Vũ | TODO | OAuth/liên kết account và xóa toàn bộ dữ liệu cá nhân chưa có workflow. |
| FR-AUTH-12 | M | Vũ | MỘT PHẦN | Token lifecycle local; chưa gửi email thật, guardian dev không chứng minh đồng ý phụ huynh thực tế. |
| FR-LRN-01 | M | Sơn/Vũ | MỘT PHẦN | Lộ trình Vũ + content Sơn + completion có; lesson page riêng chưa đăng ký, điều hướng trước/sau và nội dung đầy đủ TODO. |
| FR-LRN-02 | M | Sơn/Vũ | MỘT PHẦN | Lộ trình Vũ + content Sơn + completion có; lesson page riêng chưa đăng ký, điều hướng trước/sau và nội dung đầy đủ TODO. |
| FR-LRN-03 | M | Sơn/Vũ | TODO | Chưa có minh họa play/pause/reset, taxonomy click, notes hoặc search UI theo FR. |
| FR-LRN-04 | S | Sơn/Vũ | TODO | Chưa có minh họa play/pause/reset, taxonomy click, notes hoặc search UI theo FR. |
| FR-LRN-05 | M | Sơn/Vũ | MỘT PHẦN | Lộ trình Vũ + content Sơn + completion có; lesson page riêng chưa đăng ký, điều hướng trước/sau và nội dung đầy đủ TODO. |
| FR-LRN-06 | C | Sơn/Vũ | TODO | Chưa có minh họa play/pause/reset, taxonomy click, notes hoặc search UI theo FR. |
| FR-LRN-07 | S | Sơn/Vũ | TODO | Chưa có minh họa play/pause/reset, taxonomy click, notes hoặc search UI theo FR. |
| FR-GEO-01 | M | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-GEO-02 | M | Sơn | MỘT PHẦN | Slider/SVG 5 loại, S/P vài hình, geometry helper; chưa đủ 7 loại hoặc kéo thả UI/ràng buộc/đo góc. |
| FR-GEO-03 | M | Sơn | MỘT PHẦN | Slider/SVG 5 loại, S/P vài hình, geometry helper; chưa đủ 7 loại hoặc kéo thả UI/ràng buộc/đo góc. |
| FR-GEO-04 | M | Sơn | MỘT PHẦN | Slider/SVG 5 loại, S/P vài hình, geometry helper; chưa đủ 7 loại hoặc kéo thả UI/ràng buộc/đo góc. |
| FR-GEO-05 | S | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-GEO-06 | S | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-GEO-07 | M | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-GEO-08 | S | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-GEO-09 | C | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-GEO-10 | M | Sơn | TODO | Chưa có canvas/công cụ/undo/thực hành/lưu hình/touch theo SRS; không gọi slider là canvas đạt chuẩn. |
| FR-QZ-01 | M | Đạt | MỘT PHẦN | Có service/filter/draft/trộn trong timed test; UI difficulty, trộn luyện tập, tự lưu nháp practice chưa đủ. |
| FR-QZ-02 | M | Đạt | LOCAL | Quiz/test service + UI, chấm/feedback/history; test timed không lộ correct fields trong DTO công khai. Chưa UAT SRS. |
| FR-QZ-03 | M | Đạt | LOCAL | Quiz/test service + UI, chấm/feedback/history; test timed không lộ correct fields trong DTO công khai. Chưa UAT SRS. |
| FR-QZ-04 | S | Đạt | LOCAL | Quiz/test service + UI, chấm/feedback/history; test timed không lộ correct fields trong DTO công khai. Chưa UAT SRS. |
| FR-QZ-05 | M | Đạt | LOCAL | Quiz/test service + UI, chấm/feedback/history; test timed không lộ correct fields trong DTO công khai. Chưa UAT SRS. |
| FR-QZ-06 | S | Đạt | MỘT PHẦN | Có service/filter/draft/trộn trong timed test; UI difficulty, trộn luyện tập, tự lưu nháp practice chưa đủ. |
| FR-QZ-07 | S | Đạt | MỘT PHẦN | Có service/filter/draft/trộn trong timed test; UI difficulty, trộn luyện tập, tự lưu nháp practice chưa đủ. |
| FR-QZ-08 | M | Đạt | LOCAL | Quiz/test service + UI, chấm/feedback/history; test timed không lộ correct fields trong DTO công khai. Chưa UAT SRS. |
| FR-QZ-09 | S | Đạt | MỘT PHẦN | Nút hỏi AI truyền context chạy với mock; không LLM thật. |
| FR-ES-01 | M | Đạt | MỘT PHẦN | Đề/hints/solution theo dữ liệu mẫu và ảnh; minh họa động từng bước và nội dung 4 lớp chưa đủ. |
| FR-ES-02 | M | Đạt | MỘT PHẦN | Đề/hints/solution theo dữ liệu mẫu và ảnh; minh họa động từng bước và nội dung 4 lớp chưa đủ. |
| FR-ES-03 | S | Đạt | MỘT PHẦN | Đề/hints/solution theo dữ liệu mẫu và ảnh; minh họa động từng bước và nội dung 4 lớp chưa đủ. |
| FR-ES-04 | S | Đạt | LOCAL | Bài làm text/LaTeX, đối chiếu lời giải, tự đánh giá + hints_used lưu EssayReview. |
| FR-ES-05 | M | Đạt | LOCAL | Bài làm text/LaTeX, đối chiếu lời giải, tự đánh giá + hints_used lưu EssayReview. |
| FR-ES-06 | S | Đạt | LOCAL | Bài làm text/LaTeX, đối chiếu lời giải, tự đánh giá + hints_used lưu EssayReview. |
| FR-ES-07 | M | Đạt | MỘT PHẦN | Đề/hints/solution theo dữ liệu mẫu và ảnh; minh họa động từng bước và nội dung 4 lớp chưa đủ. |
| FR-AI-01 | M | Đạt/Sơn | MỘT PHẦN | Mock + bộ lọc từ khóa + nguồn + hint; chưa chat panel/LLM/RAG production hoặc đánh giá chất lượng theo lớp. |
| FR-AI-02 | M | Đạt/Sơn | MỘT PHẦN | Mock + bộ lọc từ khóa + nguồn + hint; chưa chat panel/LLM/RAG production hoặc đánh giá chất lượng theo lớp. |
| FR-AI-03 | M | Đạt/Sơn | LOCAL | Context, công thức mock, chat/history/xóa/feedback/quota UTC+7; giới hạn mock không chứng nhận chất lượng LLM. |
| FR-AI-04 | M | Đạt/Sơn | MỘT PHẦN | Mock + bộ lọc từ khóa + nguồn + hint; chưa chat panel/LLM/RAG production hoặc đánh giá chất lượng theo lớp. |
| FR-AI-05 | M | Đạt/Sơn | LOCAL | Context, công thức mock, chat/history/xóa/feedback/quota UTC+7; giới hạn mock không chứng nhận chất lượng LLM. |
| FR-AI-06 | S | Đạt/Sơn | LOCAL | Context, công thức mock, chat/history/xóa/feedback/quota UTC+7; giới hạn mock không chứng nhận chất lượng LLM. |
| FR-AI-07 | S | Đạt/Sơn | LOCAL | Context, công thức mock, chat/history/xóa/feedback/quota UTC+7; giới hạn mock không chứng nhận chất lượng LLM. |
| FR-AI-08 | M | Đạt/Sơn | LOCAL | Context, công thức mock, chat/history/xóa/feedback/quota UTC+7; giới hạn mock không chứng nhận chất lượng LLM. |
| FR-AI-09 | S | Đạt/Sơn | MỘT PHẦN | Mock + bộ lọc từ khóa + nguồn + hint; chưa chat panel/LLM/RAG production hoặc đánh giá chất lượng theo lớp. |
| FR-AI-10 | C | Đạt/Sơn | MỘT PHẦN | Mock + bộ lọc từ khóa + nguồn + hint; chưa chat panel/LLM/RAG production hoặc đánh giá chất lượng theo lớp. |
| FR-PG-01 | M | Vũ/Đạt | LOCAL | % lớp/chương/topic, resume, stats và ôn tiên quyết; average all/latest là policy tạm thời. |
| FR-PG-02 | M | Vũ/Đạt | MỘT PHẦN | Đạt đã có history/detail đầy đủ; Vũ vẫn dùng summary contract cũ, dashboard chung chưa hợp nhất chi tiết. |
| FR-PG-03 | S | Vũ/Đạt | TODO | Biểu đồ timeline trong Vũ chưa nối attempt_history. |
| FR-PG-04 | S | Vũ/Đạt | LOCAL | % lớp/chương/topic, resume, stats và ôn tiên quyết; average all/latest là policy tạm thời. |
| FR-PG-05 | M | Vũ/Đạt | LOCAL | % lớp/chương/topic, resume, stats và ôn tiên quyết; average all/latest là policy tạm thời. |
| FR-PG-06 | C | Vũ/Đạt | LOCAL | % lớp/chương/topic, resume, stats và ôn tiên quyết; average all/latest là policy tạm thời. |
| FR-AD-01 | M | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-02 | M | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-03 | M | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-04 | M | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-05 | M | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-06 | S | chung theo ownership | TODO | Chưa publish/unpublish/version workflow hay quản lý hình động theo SRS. |
| FR-AD-07 | M | chung theo ownership | TODO | Chưa publish/unpublish/version workflow hay quản lý hình động theo SRS. |
| FR-AD-08 | S | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-09 | S | chung theo ownership | LOCAL | Admin search/lock/unlock có role guard và revoke session; giới hạn 100 kết quả, không tổng số toàn hệ thống. |
| FR-AD-10 | S | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-AD-11 | S | chung theo ownership | MỘT PHẦN | Có role/local user admin, validators/templates/import assessment/preview/log helpers/env; chưa CMS unified hoặc admin security nâng cao. Xem R1/R2. |
| FR-I18-01 | M | Sơn + mỗi owner | MỘT PHẦN | Preference/translation helper và một số metadata en; pages không dùng đồng bộ preference/fallback toàn hệ thống. |
| FR-I18-02 | M | Sơn + mỗi owner | MỘT PHẦN | Preference/translation helper và một số metadata en; pages không dùng đồng bộ preference/fallback toàn hệ thống. |
| FR-I18-03 | S | Sơn + mỗi owner | TODO | Chưa định dạng locale đồng bộ. |
| FR-LV-01 | M | Vũ/Sơn/Đạt | LOCAL | Cấp bắt đầu, tiến độ từng lớp, cấp dưới, threshold/skip và review; A7/Q4/average chưa được chốt sản phẩm. |
| FR-LV-02 | M | Vũ/Sơn/Đạt | LOCAL | Cấp bắt đầu, tiến độ từng lớp, cấp dưới, threshold/skip và review; A7/Q4/average chưa được chốt sản phẩm. |
| FR-LV-03 | M | Vũ/Sơn/Đạt | MỘT PHẦN | Metadata/cây/prereqs có; links/UI placement recommendation/công cụ và nội dung thích ứng chưa đồng bộ. Đạt có placement service. |
| FR-LV-04 | M | Vũ/Sơn/Đạt | MỘT PHẦN | Metadata/cây/prereqs có; links/UI placement recommendation/công cụ và nội dung thích ứng chưa đồng bộ. Đạt có placement service. |
| FR-LV-05 | M | Vũ/Sơn/Đạt | LOCAL | Cấp bắt đầu, tiến độ từng lớp, cấp dưới, threshold/skip và review; A7/Q4/average chưa được chốt sản phẩm. |
| FR-LV-06 | S | Vũ/Sơn/Đạt | LOCAL | Cấp bắt đầu, tiến độ từng lớp, cấp dưới, threshold/skip và review; A7/Q4/average chưa được chốt sản phẩm. |
| FR-LV-07 | S | Vũ/Sơn/Đạt | MỘT PHẦN | Metadata/cây/prereqs có; links/UI placement recommendation/công cụ và nội dung thích ứng chưa đồng bộ. Đạt có placement service. |
| FR-LV-08 | S | Vũ/Sơn/Đạt | LOCAL | Cấp bắt đầu, tiến độ từng lớp, cấp dưới, threshold/skip và review; A7/Q4/average chưa được chốt sản phẩm. |
| FR-LV-09 | S | Vũ/Sơn/Đạt | MỘT PHẦN | Metadata/cây/prereqs có; links/UI placement recommendation/công cụ và nội dung thích ứng chưa đồng bộ. Đạt có placement service. |
| FR-LV-10 | M | Vũ/Sơn/Đạt | LOCAL | Cấp bắt đầu, tiến độ từng lớp, cấp dưới, threshold/skip và review; A7/Q4/average chưa được chốt sản phẩm. |
| FR-LV-11 | C | Vũ/Sơn/Đạt | MỘT PHẦN | Metadata/cây/prereqs có; links/UI placement recommendation/công cụ và nội dung thích ứng chưa đồng bộ. Đạt có placement service. |

## 7. Use Cases, screens, backlog và kiến trúc

- UC-01: practice submit/feedback/history chạy, login permission facade đã nối; nháp tự động/offline ngoại lệ chưa có. QZ-07/PB-32 mới ở timed test; offline vẫn câu hỏi phạm vi Q trong SRS.
- UC-02: context, quota UTC+7, timeout/refund, chat/feedback/source chạy **mock**. Chưa LLM/RAG quality hay streaming. PB-26/31/39/40 chưa đủ nghiệm thu.
- UC-03: validators/templates/Dat draft import là nền; Son page chỉ parse JSON. Preview→confirm→transaction/log→publish chưa nối. PB-08/10/25/53 chưa hoàn tất.
- UC-04: slider/SVG và core helper, chưa canvas kéo/touch/undo theo SRS; PB-13…18/35/42 chưa đạt.
- UC-05: cấp đầu, threshold/skip, lower levels, per-level progress có; UI mở khóa chưa đầy đủ notifications/placement và policy Q4 chưa duyệt. PB-49 local, PB-56 service Đạt chưa workflow gợi ý Vũ.

Screens đã có route: Home; 5 trang Vũ; overview Learning; Assessment tổng hợp quiz/results/essay/chat/history. Không phải 17 screens đầy đủ; UI Streamlit gộp screens là trade-off, không bỏ business. 56 PB vẫn được lưu ở PRODUCT_BACKLOG; bảng baseline chưa tự chuyển thành completed sau merge. NFR-PERF/SEC/REL/COMP, mobile360/WCAG/touch/Safari/500 users và UAT12HS chưa kiểm chứng. Không thu thập trẻ em thật, không đánh giá pháp lý trong code audit.

Import boundary và cycle test có PASS, không circular Python imports theo AST trong scope app; các cross-feature implementation chỉ được bootstrap import. Repositories vẫn có một số direct driver session ngoài WriteExecutor abstraction; cần chốt contracts khi mở rộng, chưa cần event bus/microservices.

## 8. Các bước nhóm nên làm tiếp

1. Sơn xử lý R1/R2 trước CMS writes, sau đó nối lesson screen/translation/taxonomy; sửa trong domain riêng.
2. Đạt review facade authorization/readonly, chốt AssessmentReader history/detail/placement, race revoke và access level.
3. Vũ review guard contract và nguồn Progress live/projection; nối history qua contract mới, xác nhận threshold/average.
4. Shared review bootstrap/contracts/schema và report; chạy tests rồi PR branch audit vào main. Không force push main.

## 9. Kết quả kiểm thử cuối đợt

| Lệnh/kiểm tra | Kết quả thực tế |
|---|---|
| `python -m pytest -m "not integration" -q` | PASS: **173**, gồm boundary/import cycle/navigation/AppTest và 35 hồi quy mới |
| `QUADLEARN_INTEGRATION=1 python -m pytest -m integration -q` | PASS: **12**, gồm 3 test mới xuyên domain/draft/demo |
| `python -m pip check` | PASS |
| `python -m compileall -q app scripts` | PASS cú pháp; import runtime được exercised qua tests/bootstrap |
| `docker compose config --quiet` | PASS |
| Constraints + aggregate graph integrity local | PASS lệnh thực thi, kết quả tại mục 5 |
| `git diff --check` | PASS |
| Windows/Intel/Safari/mobile/UAT/production | **CHƯA KIỂM CHỨNG** |

Neo4j driver có DeprecationWarning trên Python 3.14. Không che warning và không kết luận hỗ trợ Python 3.16. Không có load test hoặc chứng nhận bảo mật production.

## 10. Giới hạn bằng chứng

Graph MCP reindex fast đầu đợt 2026-10-09T03:30:14Z; watcher đã refresh full, coverage generation cuối 2026-10-09T03:40:32Z, project `Users-thaivu-Documents-LapTrinh-HUIT-YEAR4-NoSQL-Neo4j-QuadLearn`; search + snippet + trace và coverage cho đường dẫn vật chất. Graph trace có thể giải sai dynamic method nên kết luận dựa source đọc trực tiếp và tests, không dựa degree để tuyên bố hết lỗi. Docs/scripts/examples excluded, mock_ai.py bị excluded ở chỉ mục fast đầu đợt (đã có metadata trong full cuối đợt) và pytest.ini partial line5: đã đọc các nguồn có liên quan trực tiếp. Không penetration test, fuzz toàn bộ imports, stress concurrent writers hoặc kiểm toán tất cả NFR. Không có bảo đảm project không còn bug sau audit.
