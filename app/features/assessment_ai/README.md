# Đạt – assessment_ai

## 1. Owner và mục tiêu

Đạt sở hữu `app/features/assessment_ai/`. Assessment & AI: bài làm chi tiết, tự luận và trợ lý qua provider. Đây là skeleton, **không FR nào hoàn tất toàn bộ**. Service/repository/page demo hoạt động với Neo4j seed; các chức năng bên dưới TODO.

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

M = Must, S = Should, C = Could của sản phẩm; skeleton hoãn cả các Must phức tạp. Ánh xạ toàn bộ: `docs/SRS_TRACEABILITY.md`; stories/acceptance: `docs/PRODUCT_BACKLOG.md`. Giữ đúng business rules ở hai tài liệu này, không suy ra từ mock.

## 3. Màn hình

SCR-07/08/09/10; chi tiết lịch sử SCR-11, phần assessment import SCR-14/15. Page hiện tại chỉ là overview/demo, không phải toàn bộ màn hình SRS. Tạo thêm page riêng và đăng ký trong registry của mình.

## 4. Graph ownership và queries

Question, Option, EssayProblem, EssayHint, Attempt, AttemptAnswer, ChatSession, ChatMessage; HAS_QUESTION/OPTION/ESSAY/HINT, ATTEMPTED, FOR_TOPIC, HAS_ANSWER, ANSWERS, SELECTED, HAS_CHAT/MESSAGE, CONTEXT_LESSON. Xem `docs/GRAPH_SCHEMA.md` cho endpoint/cardinality và ID. Queries cần làm: Questions/options theo topic; tạo UUID Attempt+Answer atomic; SELECTED option thuộc question; history theo user/time; essay hints ORDER BY order; chat theo session; đếm messages theo ngày khi quota thật. Không sửa User/Topic/Lesson hay COMPLETED.

Không ghi node/cạnh owner khác. Các cạnh tham chiếu User/Topic chỉ được ghi theo bảng ownership. Query tham số `$id/$grade`, MATCH endpoint tồn tại trước MERGE; constraint không tự validate business.

## 5. Services và file bắt đầu

AssessmentService, score(), MockAIProvider (đang có); QuizService/AttemptService/EssayService/ChatService/QuotaService/AssessmentImportService (TODO).

Mở các file: `registry.py; pages/overview.py; models/ai.py; services/assessment.py; services/mock_ai.py; repositories/assessment.py; tests/test_assessment.py` (tương đối trong folder này). Thêm page/service/repository/model/test trong thư mục tương ứng; thêm PageSpec ở `registry.py`. Không phải sửa `app/main.py`. Tests/fakes đọc ports chung; không dùng query database thật trong unit.

## 6. Input/output contracts và dependencies

Cung cấp AssessmentReader.attempts(user_id) → AttemptSummary[]. Nhận IdentityReader/ContentReader.ai_context; AIRequest → AIProvider.respond → str. Không ghi Progress, Vũ tự tổng hợp qua reader.

DTO ở `app/shared/models/dto.py`, ports ở `app/shared/contracts/ports.py`. Empty list/None có nghĩa không có dữ liệu; lỗi kết nối không được đổi thành dữ liệu giả. `core/bootstrap.py` nối implementation. Không import repository/service domain khác; readers truyền qua AppContext. Shared API mới phải cả nhóm review và có test consumer/provider trước merge.

## 7. Thứ tự triển khai và checklist

Đọc SRS mapping → chốt câu hỏi domain → bổ sung model/repository → test service qua fake ports → thêm page/registry → chạy test domain → demo Neo4j → PR. Làm Must trước Should/Could; chia PR nhỏ theo chức năng, không đánh dấu checklist chỉ vì có placeholder.

### Must

- [ ] Tạo query danh sách published questions theo grade/topic/difficulty.
- [ ] Chấm single/multiple/true-false theo thang 10; validate không chọn và option sai question.
- [ ] Ghi mọi lần làm UUID mới, answer/selected/score/timestamps cùng transaction.
- [ ] Hiển thị kết quả/giải thích và trả history DTO cho Vũ, không ghi Progress.
- [ ] Tạo đề tự luận với giả thiết/kết luận/hình và mở hint lần lượt.
- [ ] Thêm self-evaluation essay và test difficulty theo lớp; chứng minh không áp xuống lớp 6.
- [ ] Giữ AIProvider có mock rõ nhãn; context truy xuất qua ContentReader không qua content repo.
- [ ] Thiết kế quota theo ngày atomic, timeout/lỗi không trừ, ngoài phạm vi/lứa tuổi có bộ test trước provider thật.
- [ ] Thêm validate/import assessment nhận payload từ Sơn, correct thuộc option; không ghi ImportLog trực tiếp.
- [ ] Viết test score boundary, attempts ownership, context lớp/ngôn ngữ và mock không gọi mạng.

### Should

- [ ] Làm timer/shuffle/draft/resume; không lộ đáp án giữa kỳ kiểm tra.
- [ ] Thêm Hỏi AI từ question context, chat history/delete/feedback và dẫn nguồn.
- [ ] Thêm hint minh họa/số hint đã dùng cho thống kê qua reader.
- [ ] Mở rộng reader grade/timestamp khi Vũ cần, cùng review DTO.

### Could

- [ ] Gợi mở AI ở chế độ kiểm tra và bộ test không đưa đáp án trực tiếp.
- [ ] Hỗ trợ bài xếp loại theo contract cùng Vũ, không tự cập nhật lớp.

## 8. Tiêu chí hoàn thành

Quiz: đủ loại, chấm đúng, lưu mọi answer/history và draft/test mode khi làm Should. Essay: hint tuần tự, tự đánh giá, metadata grade đúng. AI: mock chỉ nghiệm thu contract; provider thật phải quota/filter/context/timeouts/sources và bộ ≥100 câu hỏi theo SRS trước phát hành. Không gọi mock là LLM hay RAG production.

Mỗi nhóm chức năng cần PR review, tests happy/error/boundary và demo đúng tiêu chí FR/PB liên quan. Ghi TODO phần chưa làm. DoD staging/70% coverage/UAT của SRS là mục tiêu sản phẩm, chưa được skeleton chứng nhận; đừng ghi “PASS SRS” chỉ vì unit tests nền pass.

## 9. Test riêng

```text
python -m pytest app/features/assessment_ai/tests -q
python -m pytest tests/test_boundaries.py tests/test_navigation.py -q
```

Test domain không cần Neo4j. Khi DB demo sẵn, bật `QUADLEARN_INTEGRATION=1` và chạy integration theo docs/RUN_PROJECT.md. Smoke pages dùng fake contracts; kiểm UI thật thêm qua sidebar. Test không phải full FR acceptance.

## 10. Demo

Xem Attempt seed điểm 10; gọi mock với lesson context, kiểm nhãn và sources; không giả lập full quiz submit. Hướng dẫn demo chung: `docs/DEMO_GUIDE.md`. Nếu DB chưa chạy, page báo lỗi hướng dẫn; không báo kết nối PASS giả.

## 11. Giới hạn sửa file

Được sửa folder mình và các file mới trong đó. Không sửa folder hai bạn khác, không trực tiếp query/ghi nội bộ họ. `app/core`, `app/shared`, `database`, `.env.example`, `compose.yaml`, dependencies và docs kiến trúc là vùng chung: thông báo cả nhóm, giải thích tương thích, review trước merge. File `.env` local không commit. Registry path không trùng; không hardcode secret/data HS thật. Git cá nhân: GIT_WORKFLOW.md.
