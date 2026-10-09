# Đạt – assessment_ai

> Audit sau merge: [trạng thái SRS và vấn đề cần owner review](../../../docs/POST_MERGE_AUDIT_2026-10-09.md). Thay đổi audit ở branch `fix/post-merge-integration-audit`; chưa merge main.

## 1. Owner và mục tiêu

Đạt sở hữu `app/features/assessment_ai/`. Assessment & AI: bài làm chi tiết, tự luận và trợ lý qua provider. Domain này hiện có luồng trắc nghiệm, tự luận, import và chat mock. Checklist mục 7 phản ánh phần đã triển khai; các FR đầy đủ vẫn cần kiểm thử với Neo4j/UI và phối hợp contract trước khi nghiệm thu.

## 2. FR liên quan và ưu tiên SRS

| FR-ID | Công việc nghiệp vụ | Ưu tiên | Trách nhiệm |
|---|---|---|---|
| FR-QZ-01 | Hiển thị danh sách bài trắc nghiệm theo cấp độ lớp, chủ đề và mức độ (Nhận biết, Thông hiểu, Vận dụng) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-02 | Câu hỏi 1 đáp án đúng; hỗ trợ nhiều đáp án và đúng/sai; có thể kèm hình minh họa | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-03 | Chế độ luyện tập: chấm từng câu, hiển thị giải thích ngay | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-04 | Chế độ kiểm tra: tính giờ, chấm cuối bài, không xem đáp án giữa chừng | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-05 | Chấm điểm tự động theo thang 10; hiển thị đúng/sai từng câu và giải thích | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-06 | Trộn thứ tự câu hỏi và đáp án | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-07 | Lưu nháp, cho phép tiếp tục bài đang làm dở | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-08 | Làm lại bài; lưu mọi lần làm | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-QZ-09 | Nút "Hỏi AI" ngay tại câu hỏi để giải thích sâu hơn | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-01 | Hiển thị đề tự luận kèm hình vẽ, giả thiết, kết luận | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-02 | Gợi ý lời giải theo từng bước, mở dần theo yêu cầu của HS (Gợi ý 1 → 2 → 3 → Lời giải đầy đủ) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-03 | Mỗi bước gợi ý có thể gắn minh họa trên hình động (vẽ thêm đường phụ, tô góc bằng nhau) | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-04 | HS nhập bài làm (văn bản, công thức) và tự đối chiếu với lời giải mẫu | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-05 | HS tự đánh giá mức độ hiểu (Đã hiểu / Cần xem lại) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-06 | Ghi nhận số gợi ý đã dùng để phục vụ thống kê điểm yếu | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-ES-07 | Độ khó theo cấp độ: lớp 6 dùng bài toán thực tế/tính toán đơn giản; bài chứng minh bắt đầu từ lớp 7–8 và tăng dần | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-01 | Khung chat hỏi đáp bằng tiếng Việt hoặc tiếng Anh theo ngôn ngữ người dùng | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-02 | Chatbot giải thích lời giải bài tập, khái niệm, tính chất tứ giác ở mức phù hợp với lớp của HS (lớp 6: ngôn ngữ trực quan, ví dụ đời thường; lớp 8–9: thuật ngữ và lập luận chứng minh) | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-03 | Chatbot nhận ngữ cảnh: bài học hoặc câu hỏi HS đang xem để trả lời đúng trọng tâm | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-04 | Giới hạn phạm vi: từ chối lịch sự câu hỏi ngoài chủ đề; không trả lời nội dung không phù hợp lứa tuổi | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-05 | Công thức toán hiển thị đúng định dạng trong câu trả lời | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-06 | Lưu lịch sử hội thoại theo từng phiên; HS có thể xóa | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-07 | HS đánh giá câu trả lời (hữu ích / không hữu ích) và báo lỗi | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-08 | Giới hạn số lượt hỏi mỗi HS mỗi ngày (cấu hình được); hiển thị số lượt còn lại | M | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-09 | Ưu tiên dẫn nguồn là nội dung trong hệ thống (liên kết về bài lý thuyết liên quan); nên dùng kiến trúc truy xuất nội dung (RAG) | S | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-AI-10 | Chatbot ưu tiên dẫn dắt HS tự suy nghĩ (gợi mở) thay vì chỉ đưa đáp án khi HS đang làm bài kiểm tra | C | Chủ trì; TODO đầy đủ; skeleton chỉ tạo điểm mở rộng, không hoàn tất FR. |
| FR-PG-02 | Lịch sử làm bài: ngày giờ, bài, điểm, thời gian; xem lại bài và đáp án đã chọn | M | Phối hợp, không ghi hộ owner; Đạt sở hữu Attempt/Answer; Vũ hiển thị qua AssessmentReader. |
| FR-AD-02 | Import hàng loạt từ Excel (.xlsx) và JSON: chủ đề, bài lý thuyết, câu trắc nghiệm, đề tự luận, bước gợi ý, kèm nhãn lớp, mức nhận thức và kiến thức tiên quyết | M | Phối hợp, không ghi hộ owner; Sơn điều phối; Đạt validate/ghi Question, Option, Essay, Hint. |
| FR-AD-03 | Kiểm tra dữ liệu trước khi nhập (validate): báo lỗi theo dòng/ô, không nhập nếu lỗi nghiêm trọng | M | Phối hợp, không ghi hộ owner; Mỗi domain validate phần mình; Sơn tổng hợp báo cáo. |
| FR-AD-04 | Tải file mẫu import cho từng loại nội dung | M | Phối hợp, không ghi hộ owner; Sơn mẫu lesson; Đạt mẫu question/essay. |
| FR-AD-05 | Xem trước nội dung sau import; trạng thái Nháp / Đã xuất bản | M | Phối hợp, không ghi hộ owner; Sơn lesson; Đạt question/essay, không ghi chéo. |
| FR-AD-06 | Xuất bản, gỡ bản, sửa từng mục nội dung và lưu phiên bản | S | Phối hợp, không ghi hộ owner; Version thuộc owner từng loại nội dung. |
| FR-AD-11 | Cấu hình hệ thống: hạn mức hỏi AI, thời gian phiên | S | Chủ trì; Đạt quota AI; Vũ thời hạn session (hai cấu hình khác nhau). |
| FR-LV-11 | Bài kiểm tra xếp loại đầu vào để gợi ý cấp độ phù hợp | C | Phối hợp, không ghi hộ owner; Vũ chọn lớp gợi ý; Đạt đề/chấm bài đầu vào (TODO Could). |

M = Must, S = Should, C = Could của sản phẩm. Bảng trên là phân công gốc; tiến độ triển khai nằm ở checklist mục 7. Ánh xạ toàn bộ: `docs/SRS_TRACEABILITY.md`; stories/acceptance: `docs/PRODUCT_BACKLOG.md`. Giữ đúng business rules ở hai tài liệu này, không suy ra từ mock.

## 3. Màn hình

SCR-07/08/09/10; chi tiết lịch sử SCR-11, phần assessment import SCR-14/15. `pages/overview.py` hiện chứa luồng luyện tập, kiểm tra, tự luận và chat mock. Màn hình Admin import vẫn do Sơn tích hợp.

## 4. Graph ownership và queries

Question, Option, EssayProblem, EssayHint, Attempt, AttemptAnswer, ChatSession, ChatMessage; HAS_QUESTION/OPTION/ESSAY/HINT, ATTEMPTED, FOR_TOPIC, HAS_ANSWER, ANSWERS, SELECTED, HAS_CHAT/MESSAGE, CONTEXT_LESSON. Xem `docs/GRAPH_SCHEMA.md` cho endpoint/cardinality và ID. Queries cần làm: Questions/options theo topic; tạo UUID Attempt+Answer atomic; SELECTED option thuộc question; history theo user/time; essay hints ORDER BY order; chat theo session; đếm messages theo ngày khi quota thật. Không sửa User/Topic/Lesson hay COMPLETED.

Không ghi node/cạnh owner khác. Các cạnh tham chiếu User/Topic chỉ được ghi theo bảng ownership. Query tham số `$id/$grade`, MATCH endpoint tồn tại trước MERGE; constraint không tự validate business.

## 5. Services và file bắt đầu

AssessmentService, QuizService, EssayService, ChatService, AssessmentImportService, score() và MockAIProvider nằm trong domain. Quota được quản lý trong ChatService/AssessmentRepository; chưa có provider LLM thật.

Mở các file: `registry.py; pages/overview.py; models/ai.py; services/assessment.py; services/mock_ai.py; repositories/assessment.py; tests/test_assessment.py` (tương đối trong folder này). Thêm page/service/repository/model/test trong thư mục tương ứng; thêm PageSpec ở `registry.py`. Không phải sửa `app/main.py`. Tests/fakes đọc ports chung; không dùng query database thật trong unit.

## 6. Input/output contracts và dependencies

Cung cấp AssessmentReader.attempts(user_id) → AttemptSummary[]. Nhận IdentityReader/ContentReader.ai_context; AIRequest → AIProvider.respond → str. Không ghi Progress, Vũ tự tổng hợp qua reader.

DTO ở `app/shared/models/dto.py`, ports ở `app/shared/contracts/ports.py`. Empty list/None có nghĩa không có dữ liệu; lỗi kết nối không được đổi thành dữ liệu giả. `core/bootstrap.py` nối implementation. Không import repository/service domain khác; readers truyền qua AppContext. Shared API mới phải cả nhóm review và có test consumer/provider trước merge.

## 7. Thứ tự triển khai và checklist

Đọc SRS mapping → chốt câu hỏi domain → bổ sung model/repository → test service qua fake ports → thêm page/registry → chạy test domain → demo Neo4j → PR. Làm Must trước Should/Could; chia PR nhỏ theo chức năng, không đánh dấu checklist chỉ vì có placeholder.

### Must

- [x] Tạo query danh sách published questions theo grade/topic/difficulty.
- [x] Chấm single/multiple/true-false theo thang 10; validate không chọn và option sai question.
- [x] Ghi mọi lần làm UUID mới, answer/selected/score/timestamps cùng transaction.
- [x] Hiển thị kết quả/giải thích và trả history DTO cho Vũ, không ghi Progress.
- [x] Tạo đề tự luận với giả thiết/kết luận/hình và mở hint lần lượt.
- [x] Thêm self-evaluation essay và test difficulty theo lớp; chứng minh không áp xuống lớp 6.
- [x] Giữ AIProvider có mock rõ nhãn; context truy xuất qua ContentReader không qua content repo.
- [x] Quota theo ngày atomic, timeout/lỗi không trừ; lọc phạm vi/lứa tuổi trước provider và có test hard timeout. Provider hiện là mock theo phạm vi đồ án.
- [x] Validate/import assessment nhận payload JSON/XLSX từ Sơn, correct thuộc option; cung cấp entrypoint qua AssessmentService và không ghi ImportLog trực tiếp.
- [x] Viết test score boundary, attempts ownership, context lớp/ngôn ngữ và mock không gọi mạng.

### Should

- [x] Làm timer/shuffle/draft/resume; không lộ đáp án giữa kỳ kiểm tra. Đã kiểm thử Neo4j round trip và Streamlit AppTest dùng repository thật cho draft, khóa xem lời giải và nộp bài.
- [x] Thêm Hỏi AI từ question context, chat nhiều lượt/history/delete/feedback và deep link nguồn sang trang bài học.
- [x] Thêm hint minh họa/số hint đã dùng cho thống kê qua reader.
- [x] Nhập bài làm tự luận và đối chiếu lời giải mẫu; lưu bài làm cùng lần tự đánh giá.
- [x] Cung cấp `attempt_history` nội bộ gồm grade/topic/score/status/timestamps/thời lượng cho Vũ; giữ nguyên shared DTO để không sửa contract của thành viên khác.

### Could

- [x] Gợi mở AI ở chế độ kiểm tra bằng purpose riêng; mock không lặp nội dung lời giải/context và có test theo lớp/ngôn ngữ.
- [x] Cung cấp đề xếp loại công khai không lộ đáp án và điểm theo từng lớp cho Vũ; không gợi ý hoặc tự cập nhật lớp.

## 8. Tiêu chí hoàn thành

Hiện đã có luồng luyện tập với câu hỏi đã xuất bản, chấm điểm, ghi attempt trong một transaction và xem lại chi tiết trong page của Đạt. Đề tự luận seed có thể xem, nhập bài làm và mở gợi ý từng bước; người học xem song song bài làm với lời giải mẫu. Tự đánh giá lưu node `EssayReview` cùng bài làm và số gợi ý đã dùng, qua `User-REVIEWED_ESSAY->EssayReview-FOR_ESSAY->EssayProblem`; đây là phần mở rộng schema thuộc Đạt, cần nhóm review trước merge. Repository ghi attempt dùng write transaction của Neo4j driver do `QueryExecutor` chung hiện chỉ có `read`; không sửa core/shared hoặc dữ liệu domain khác.

`AssessmentImportService.import_batch(topic_id, grade, payload)` nhận JSON theo [mẫu](examples/assessment_import.json). `import_xlsx(topic_id, grade, data)` nhận bytes `.xlsx` gồm sheet `questions`, `options`, `essays`, `hints`. `questions`/`essays` có cột `key`; `options.question_key` và `hints.essay_key` nối đúng dòng cha; các cột nội dung cùng tên key JSON. Validator báo loại sheet/dòng/cột lỗi và từ chối toàn batch; writer tạo Question/Option/Essay/Hint trong một transaction, mặc định trạng thái `draft`. `preview(topic_id)` đọc câu hỏi/đề và trạng thái, gồm đáp án đúng nên chỉ workflow Admin của Sơn được hiển thị kết quả này. Sơn vẫn sở hữu upload/preview UI/ImportLog; chưa có nút import hoặc kiểm tra quyền Admin ở page Đạt. Mock vẫn là provider duy nhất, và contract review với Vũ/Sơn còn TODO. Các mục chưa đủ tiêu chí FR vẫn để trống ở checklist.

Theo lựa chọn của người dùng cho đồ án hiện tại, provider giữ ở dạng mock. Mock AI đi qua `ChatService` và `ScreenedAIProvider`: lọc quy tắc trước/sau provider, hạn mức mặc định 10 lượt/ngày theo UTC+7 (đổi bằng `QUADLEARN_AI_DAILY_LIMIT`), đặt trước lượt trong transaction và hoàn lượt khi provider lỗi hoặc vượt hard timeout 30 giây. Thành công tạo hoặc nối tiếp ChatSession và lưu cặp ChatMessage trong cùng transaction tăng lượt; xóa phiên chat không hoàn lượt. Node `AIQuotaDay` và unique constraint được tạo khi dùng quota lần đầu, nên tài khoản Neo4j cần quyền tạo constraint. Đây là mở rộng schema thuộc Đạt cần nhóm review; bộ lọc quy tắc không đủ thay cho kiểm duyệt LLM production. Nếu sau này thay provider thật, provider vẫn nên có I/O timeout riêng để giải phóng request nền sau khi service đã trả timeout.

Chế độ kiểm tra tạo Attempt `draft` riêng, lưu thứ tự câu/đáp án đã trộn và lựa chọn nháp. `resume_test` chỉ trả nội dung câu/đáp án, không trả cờ đúng hay giải thích; sau khi nộp mới tạo AttemptAnswer và điểm. Lưu nháp sau thời hạn bị chặn, nộp trễ chấm bản nháp đã lưu. `AssessmentReader.attempts()` chỉ trả bài `completed` để Vũ không cộng nháp vào tiến độ.

Quiz: đủ loại, chấm đúng, lưu mọi answer/history và draft/test mode khi làm Should. Essay: hint tuần tự, tự đánh giá, metadata grade đúng. AI: mock chỉ nghiệm thu contract; provider thật phải quota/filter/context/timeouts/sources và bộ ≥100 câu hỏi theo SRS trước phát hành. Không gọi mock là LLM hay RAG production.

Placement: `placement_form(grades, per_grade)` trả câu hỏi đã ẩn đáp án; `grade_placement(question_ids, selections)` trả điểm theo từng lớp. Kết quả không có `recommended_grade` và không ghi User/Progress; Vũ sở hữu quyết định gợi ý lớp.

Mỗi nhóm chức năng cần PR review, tests happy/error/boundary và demo đúng tiêu chí FR/PB liên quan. Ghi TODO phần chưa làm. DoD staging/70% coverage/UAT của SRS là mục tiêu sản phẩm, chưa được skeleton chứng nhận; đừng ghi “PASS SRS” chỉ vì unit tests nền pass.

File mẫu import có cả [JSON](examples/assessment_import.json) và [Excel](examples/assessment_import.xlsx). File Excel gồm bốn sheet `questions`, `options`, `essays`, `hints`; cột `key` của dòng cha được liên kết bằng `question_key` hoặc `essay_key` ở dòng con.

Workflow Admin của Sơn có thể gọi `ctx.assessment.import_assessment_batch(topic_id, grade, payload)`, `import_assessment_xlsx(topic_id, grade, data)` và `preview_assessment(topic_id)` qua AppContext. Kết quả preview gồm đáp án đúng; caller phải kiểm tra quyền Admin trước khi gọi/hiển thị. Domain Đạt không ghi ImportLog hoặc tạo UI Admin.

## 9. Test riêng

```text
python -m pytest app/features/assessment_ai/tests -q
python -m pytest tests/test_boundaries.py tests/test_navigation.py -q
python -m unittest app.features.assessment_ai.tests.test_quiz app.features.assessment_ai.tests.test_test_mode app.features.assessment_ai.tests.test_essay app.features.assessment_ai.tests.test_essay_review app.features.assessment_ai.tests.test_repository app.features.assessment_ai.tests.test_repository_writes app.features.assessment_ai.tests.test_import_assessment app.features.assessment_ai.tests.test_import_xlsx app.features.assessment_ai.tests.test_mock_ai_unittest app.features.assessment_ai.tests.test_ai_safety app.features.assessment_ai.tests.test_chat -q
```

Test domain không cần Neo4j. Khi DB demo đã seed và sẵn sàng, bật `QUADLEARN_INTEGRATION=1` và chạy integration theo docs/RUN_PROJECT.md; `test_integration_assessment.py` thử ghi/đọc bài luyện tập, bài tính giờ và tự luận rồi dọn các node đã tạo. Smoke pages dùng fake contracts; kiểm UI thật thêm qua sidebar. Test không phải full FR acceptance.

Trên Windows, đặt `PYTHONUTF8=1` trước khi chạy toàn bộ pytest vì `tests/test_boundaries.py` đọc mã UTF-8 theo encoding mặc định của Python.

## 10. Demo

Khi có Neo4j demo, mở trang Đạt để thử luyện tập, kiểm tra, tự luận và chat mock với lesson/question context. Hướng dẫn demo chung: `docs/DEMO_GUIDE.md`. Nếu DB chưa chạy, page báo lỗi hướng dẫn; không báo kết nối PASS giả.

## 11. Giới hạn sửa file

Được sửa folder mình và các file mới trong đó. Không sửa folder hai bạn khác, không trực tiếp query/ghi nội bộ họ. `app/core`, `app/shared`, `database`, `.env.example`, `compose.yaml`, dependencies và docs kiến trúc là vùng chung: thông báo cả nhóm, giải thích tương thích, review trước merge. File `.env` local không commit. Registry path không trùng; không hardcode secret/data HS thật. Git cá nhân: GIT_WORKFLOW.md.

## Giao diện học sinh sau khi tổ chức lại

Trang `/assessment` có bốn mục: **Trắc nghiệm**, **Tự luận**, **Trợ lý học tập**, **Lịch sử**. Chỉ mục đang chọn được render; không tải và xếp toàn bộ chức năng thành một cột dài.

- `pages/overview.py`: entry point, kiểm tra người dùng, điều hướng hoạt động; khi có bài kiểm tra nháp thì ưu tiên tiếp tục bài, khóa xem lời giải cũ.
- `pages/quiz.py`: chọn bài theo tên, luyện tập từng câu, giữ lựa chọn trước/sau, kiểm tra riêng câu trong vùng hỗ trợ tùy chọn, nộp bài và màn hình kết quả; kiểm tra tính giờ có form lưu nháp/nộp bài. Callback nộp luyện tập chuyển trạng thái trước render để tránh nộp lặp khi rerun.
- `pages/history.py`: danh sách bài đã nộp với tên bài, điểm và thời điểm; xem chi tiết đáp án/lời giải, không đưa ID kỹ thuật vào bộ chọn.
- `pages/essay.py`: đề tự luận, gợi ý theo bước, lời giải mẫu và tự đánh giá.
- `pages/support.py`: hỏi bài, nguồn kiến thức, hội thoại và đánh giá; ghi rõ provider mô phỏng.

Chấm điểm/lưu Neo4j vẫn qua `ctx.assessment` → `services/assessment.py` → `services/quiz.py` → repository. Giao diện không tự ghi Cypher hoặc đổi schema. Bài luyện tập chưa nộp giữ trong Streamlit session, có thể mất nếu tải lại trình duyệt. Bài kiểm tra cần **Lưu nháp** để giữ trong Neo4j; thời gian vẫn chạy sau khi rời trang. Khi hết giờ chỉ chấm đáp án đã lưu. Nên lưu nháp trước khi mở gợi mở cách nghĩ.

Test luồng người dùng: `python -m pytest app/features/assessment_ai/tests/test_page.py app/features/assessment_ai/tests/test_quiz_flow.py tests/test_assessment_multiple_questions.py`. Bao gồm giữ lựa chọn từng câu, không tự chọn đáp án, không nộp thiếu câu, lưu form kiểm tra trước khi chấm, giới hạn hết giờ và xem lại kết quả không tạo thêm bài làm.
