"""Content service implementing ContentReader protocol."""

from typing import Any, Dict, List, Optional
from app.shared.models.dto import LessonSummary
from app.features.learning_geometry.repositories.content import ContentRepository


class ContentService:
    """Service providing content reading capabilities matching ContentReader Protocol."""

    ALLOWED_GRADES = {6, 7, 8, 9}

    def __init__(self, repository: Optional[Any] = None):
        self.repo = repository or ContentRepository()

    def lessons(self, grade: int) -> List[LessonSummary]:
        """Fetch lessons for a grade strictly validated between 6 and 9."""
        if not isinstance(grade, int) or grade not in self.ALLOWED_GRADES:
            raise ValueError(f"Khối lớp {grade} không hợp lệ. Chỉ chấp nhận các số nguyên từ 6 đến 9.")

        if hasattr(self.repo, "lessons"):
            return self.repo.lessons(grade)

        raw_items = self.repo.list_lessons_for_grade(grade)
        return [self._map_to_summary(item) for item in raw_items]

    def prerequisites(self, lesson_id: str) -> List[LessonSummary]:
        """Get prerequisite lessons mapped to LessonSummary."""
        if hasattr(self.repo, "prerequisites"):
            return self.repo.prerequisites(lesson_id)

        raw_items = self.repo.get_prerequisites_recursive(lesson_id)
        return [self._map_to_summary(item) for item in raw_items]

    def ai_context(self, lesson_id: str) -> List[LessonSummary]:
        """Get theory context data for AI generation."""
        if hasattr(self.repo, "ai_context"):
            return self.repo.ai_context(lesson_id)

        lesson = self.repo.get_lesson_by_id(lesson_id)
        if not lesson:
            return []
        return [self._map_to_summary(lesson)]

    def geometry_graph(self) -> Dict[str, List[dict]]:
        """Cung cấp taxonomy thật qua contract; lỗi DB phải được báo, không thay bằng mock."""
        from ..repositories.taxonomy import TaxonomyRepository
        executor = getattr(self.repo, "db", None)
        if executor is None:
            raise ValueError("Chưa cấu hình Neo4j để đọc sơ đồ tri thức.")
        return TaxonomyRepository().geometry_graph(executor)

    def get_lesson(self, lesson_id: str) -> Optional[LessonSummary]:
        """Helper method to fetch single lesson as LessonSummary."""
        data = self.repo.get_lesson_by_id(lesson_id)
        if not data:
            return None
        return self._map_to_summary(data)

    def _map_to_summary(self, data: Any) -> LessonSummary:
        """Map raw dict/object data to shared LessonSummary dataclass."""
        if isinstance(data, LessonSummary):
            return data

        if isinstance(data, dict):
            return LessonSummary(
                id=data.get("id", ""),
                title=data.get("title_vi", data.get("title", "")),
                grade=data.get("grade", 8),
                topic_id=data.get("topic_id", "TOPIC_UNKNOWN"),
                content=data.get("content_vi", data.get("content", ""))
            )

        return LessonSummary(
            id=getattr(data, "id", ""),
            title=getattr(data, "title", getattr(data, "title_vi", "")),
            grade=getattr(data, "grade", 8),
            topic_id=getattr(data, "topic_id", "TOPIC_UNKNOWN"),
            content=getattr(data, "content", getattr(data, "content_vi", ""))
        )
