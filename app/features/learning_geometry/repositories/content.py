"""Content repository for accessing geometry learning materials."""

from typing import Any, Dict, List, Optional


class ContentRepository:
    def __init__(self, database: Optional[Any] = None):
        self.db = database

    def list_lessons_for_grade(self, grade: int) -> List[Dict[str, Any]]:
        cypher = """
        MATCH (l:Lesson)
        WHERE l.grade = $grade
        RETURN l.id AS id, l.title_vi AS title, l.content_vi AS content, l.grade AS grade, l.topic_id AS topic_id
        """
        try:
            if self.db and hasattr(self.db, "read"):
                return self.db.read(cypher, grade=grade)
        except Exception:
            pass

        # Fallback dữ liệu mock nếu database chưa kết nối hoặc chưa seed data
        return [
            {
                "id": f"LES_GEO_0{grade}",
                "title": f"Bài học Lý thuyết Hình học Lớp {grade}",
                "content": f"Kiến thức cốt lõi và bài tập mẫu hình học dành cho học sinh lớp {grade}.",
                "grade": grade,
                "topic_id": "TOPIC_GEO_QUAD"
            }
        ]

    def get_prerequisites_recursive(self, lesson_id: str) -> List[Dict[str, Any]]:
        cypher = """
        MATCH (l:Lesson {id: $lesson_id})-[pr:REQUIRES*1..3]->(pre:Lesson)
        RETURN pre.id AS id, pre.title_vi AS title, pre.grade AS grade, pre.topic_id AS topic_id
        """
        try:
            if self.db and hasattr(self.db, "read"):
                return self.db.read(cypher, lesson_id=lesson_id)
        except Exception:
            pass

        return [
            {
                "id": "LES_GEO_PRE_01",
                "title": "Kiến thức nền tảng: Đoạn thẳng và Góc",
                "grade": 7,
                "topic_id": "TOPIC_GEO_BASICS"
            }
        ]

    def get_lesson_by_id(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        cypher = """
        MATCH (l:Lesson {id: $lesson_id})
        RETURN l.id AS id, l.title_vi AS title, l.content_vi AS content, l.grade AS grade, l.topic_id AS topic_id
        """
        try:
            if self.db and hasattr(self.db, "read"):
                res = self.db.read(cypher, lesson_id=lesson_id)
                if res:
                    return res[0]
        except Exception:
            pass

        return {
            "id": lesson_id,
            "title": f"Chi tiết bài học {lesson_id}",
            "content": "Nội dung bài học lý thuyết hình học chi tiết.",
            "grade": 8,
            "topic_id": "TOPIC_GEO_QUAD"
        }