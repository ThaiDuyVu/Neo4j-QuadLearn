# Tích hợp feature

> Trạng thái sau merge 3 domain và audit 09/10/2026: xem [báo cáo đối chiếu 86 FR, lỗi tích hợp và kiểm chứng](POST_MERGE_AUDIT_2026-10-09.md). Các bảng skeleton bên dưới là baseline; không dùng TODO cũ để kết luận phần đã triển khai hiện tại.

## Contract đang chạy

`app/shared/contracts/ports.py` định nghĩa Protocol; `app/shared/models/dto.py` có DTO bất biến. `app/core/context.py` gom readers. Composition root `app/core/bootstrap.py` là nơi duy nhất nối implementation.

```python
# Trong một page bất kỳ: chỉ dùng context/DTO, không import domain khác.
user = ctx.identity.current_user()       # CurrentUser | None; demo=True hiện tại
lessons = ctx.content.lessons(8)         # list[LessonSummary], published, thứ tự ổn định
prereqs = ctx.content.prerequisites(lessons[0].id)  # tối đa 8 bước
history = ctx.assessment.attempts(user.id) if user else []
context = ctx.content.ai_context(lessons[0].id)    # nguồn id + nội dung, tối đa 8 bài
```

Không có HTTP API; đây là Python API nội bộ. Danh sách không có dữ liệu trả `[]`, user không tồn tại trả `None`; sai grade ValueError; lỗi database truyền lên page và hiển thị hướng dẫn. Không nuốt lỗi thành danh sách trống giả. Readers không ghi dữ liệu. Demo không phải session thật; trước khi phát triển write, cần thay identity và kiểm tra quyền ở service.

## Learning Content ↔ Learning Path

Sơn sở hữu catalog, published status, metadata grade/cognitive và REQUIRES. Vũ đọc ContentReader để dựng path, tính mẫu số bài xuất bản và tìm nền tảng. Nếu lesson unpublished, không được tính hoàn thành tự động. Sơn không ghi progress khi bấm “đã học”; đề xuất contract tiếp theo (TODO, chưa chạy):

```python
class ProgressWriter(Protocol):
    def complete_lesson(self, user_id: str, lesson_id: str) -> None: ...
    def resume_lesson(self, user_id: str) -> LessonSummary | None: ...
```

Vũ kiểm tra verified account/consent/quyền truy cập, id tồn tại, ghi COMPLETED idempotent và cập nhật projection trong transaction. Sơn chỉ gọi sau khi contract được review. Mở khóa dùng threshold cấu hình, chưa bật trong skeleton.

## Assessment ↔ Progress

Đạt ghi Attempt + Answer + SELECTED trong transaction, UUID mới mỗi lần làm. AssessmentReader hiện trả lịch sử gồm topic, score, status. Vũ chỉ đọc `completed` khi tính trung bình. Không event bus: Vũ truy vấn lại reader khi mở dashboard hoặc sau lần submit. Khi cần aggregate grade/timestamps, mở rộng DTO/reader có review; không query trực tiếp Attempt từ repository Vũ. Chốt latest/all attempts trước khi triển khai (OPEN_QUESTIONS). Bài thi/nháp không tính điểm như completed.

## Content ↔ AI

Đạt nhận lesson ID từ page, lấy `ai_context()` của Sơn. `AIRequest` chỉ mang question, grade, language, context DTO; không email/tên HS. Mock trả cố định có nhãn, không suy luận. Sources là lesson IDs để liên kết về lý thuyết sau này. Question context và sources có route thật TODO. Quota/lọc đầu vào-đầu ra/chat persistence phải do Đạt làm, không nằm trong ContentReader.

## Identity ↔ các module

Mọi domain gọi IdentityReader, xử lý None; không đặt user ID hardcode ngoài identity demo service/fixtures. Khi AUTH thật, `CurrentUser.demo=False`, roles phải được server/service kiểm tra. Các service viết không chỉ tin `CurrentUser` từ UI. Hiện không có trang admin ghi, không được gọi mock là xác thực thật.

## Import và admin chung

Sơn giữ workflow preview/validate/report/ImportLog. Đạt cung cấp validator + writer cho question/essay, Vũ cung cấp quyền admin. Chưa có contract import hoàn chỉnh: chốt batch atomic hay theo loại trước. Không cho content importer tạo Question trực tiếp. Các mẫu ở learning_geometry/examples là cấu trúc tham khảo; chưa có importer runtime.

## Thêm page không sửa main

1. Tạo `pages/profile.py` trong feature mình với `render(ctx)`.
2. Trong `registry.py` feature, import render và thêm `PageSpec("Hồ sơ", "identity-profile", render)`.
3. URL path duy nhất toàn app; chạy pytest navigation và AppTest page riêng.
4. Service/repository mới ở feature mình, dependency chỉ shared/core + nội bộ. Muốn thêm port hoặc context thì báo nhóm/review.

Không dùng `st.session_state` như database history; chỉ trạng thái UI. Mỗi lần Streamlit rerun có thể đọc dữ liệu mới. Không tạo shared contract “generic write(query)” cho pages vì sẽ phá quyền sở hữu.

## Cập nhật tích hợp Vũ

`ctx.auth` và `ctx.progress` có implementation local; `ctx.identity` lấy session_state riêng browser, default guest, demo explicit chỉ đọc. ProgressWriter.start_lesson/complete_lesson/resume_lesson chạy và kiểm quyền. AuthSession/AuthToken mới thuộc Vũ. GraphLearningCatalog shared adapter chỉ đọc metadata chapter/topic; không sửa feature Sơn. Không thay signature readers cũ; AppContext fields mới optional. Xem tài liệu giải thích Vũ để biết status/TODO hiện tại; đề xuất TODO ở phần baseline phía trên được thay bởi implementation local này. Timestamps/detail answers/deletion/placement vẫn cần Đạt mở rộng contract.

## Runtime sau audit 3 domain

Bootstrap bind `AssessmentService(repository, identity=identity)`. Facade kiểm `IdentityActions.require_user` trước mọi thao tác ghi và require admin trước import/preview; readers user-specific kiểm current_user ID. Unbound facade không được ghi. Không gọi thẳng QuizService/ChatService/importer từ domain khác để bỏ guard. Các subservices/repository là implementation nội bộ, test riêng không tương đương authenticated runtime.

Demo có thể đọc fixture; không lưu bài làm/chat/essay/feedback. Son lesson page dùng `ctx.progress.complete_lesson(...) -> None`: không exception nghĩa thành công, không kiểm bool. Identity/Content/Assessment contracts cũ vẫn dùng; history/placement/get_lesson đã có implementation nhưng port cần review mở rộng theo R3 audit. `Progress.average_score` là snapshot, `levels/access` tính live từ completed attempts; không để Đạt ghi Progress.
