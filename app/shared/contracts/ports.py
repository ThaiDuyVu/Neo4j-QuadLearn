"""Hợp đồng tối thiểu. Thay đổi cần cả nhóm review; không chứa Cypher."""
from typing import Protocol
from app.shared.models.dto import CurrentUser, LessonSummary, AttemptSummary

class QueryExecutor(Protocol):
    def read(self, query: str, **params) -> list[dict]: ...

class IdentityReader(Protocol):
    def current_user(self) -> CurrentUser | None: ...

class ContentReader(Protocol):
    def lessons(self, grade: int) -> list[LessonSummary]: ...
    def prerequisites(self, lesson_id: str) -> list[LessonSummary]: ...
    def ai_context(self, lesson_id: str) -> list[LessonSummary]: ...

class AssessmentReader(Protocol):
    def attempts(self, user_id: str) -> list[AttemptSummary]: ...

# TODO Vũ: triển khai ProgressWriter.complete_lesson(user_id, lesson_id),
# chỉ sau khi kiểm tra danh tính, xác thực email và quyền truy cập.
# TODO Sơn/Đạt: hợp đồng import riêng theo loại nội dung; không ghi hộ domain khác.
