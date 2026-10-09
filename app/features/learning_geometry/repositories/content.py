"""Content repository for accessing geometry learning materials."""

from typing import Any, Dict, List, Optional
from app.shared.models.dto import LessonSummary

FIELDS = "l.id AS id, l.title_vi AS title, l.grade AS grade, t.id AS topic_id, l.content_vi AS content"


class ContentRepository:
    def __init__(self, database: Optional[Any] = None):
        if database is None or not hasattr(database, "read"):
            raise ValueError("ContentRepository cần database có read(); không tự tạo nội dung giả.")
        self.db = database

    def list_lessons_for_grade(self, grade: int) -> List[Dict[str, Any]]:
        from dataclasses import asdict
        return [asdict(lesson) for lesson in self.lessons(grade)]

    def get_prerequisites_recursive(self, lesson_id: str) -> List[Dict[str, Any]]:
        from dataclasses import asdict
        return [asdict(lesson) for lesson in self.prerequisites(lesson_id)]

    def get_lesson_by_id(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.read("""
            MATCH (l:Lesson {id:$id})<-[:HAS_LESSON]-(t:Topic)
                  <-[:HAS_TOPIC]-(c:Chapter)<-[:HAS_CHAPTER]-(v:Level)
            WHERE l.status='published' AND t.status='published'
              AND coalesce(c.status,'published')='published' AND v.grade=l.grade
            RETURN """ + FIELDS + " LIMIT 1", id=lesson_id)
        return rows[0] if rows else None

    def lessons(self, grade: int):
        return [LessonSummary(**row) for row in self.db.read("""
            MATCH (:Level {grade: $grade})-[:HAS_CHAPTER]->(c:Chapter)-[:HAS_TOPIC]->(t:Topic)-[:HAS_LESSON]->(l:Lesson)
            WHERE l.status = 'published' AND t.status='published'
              AND coalesce(c.status,'published')='published' AND l.grade=$grade AND t.grade=$grade
            RETURN """ + FIELDS + " ORDER BY l.order, l.id", grade=grade)]

    def prerequisites(self, lesson_id: str):
        return [LessonSummary(**row) for row in self.db.read("""
            MATCH (:Lesson {id: $id})-[:REQUIRES*1..8]->(l:Lesson)<-[:HAS_LESSON]-(t:Topic)<-[:HAS_TOPIC]-(c:Chapter)
            WHERE l.status = 'published' AND t.status='published' AND coalesce(c.status,'published')='published'
            RETURN DISTINCT """ + FIELDS + " ORDER BY l.grade, l.id", id=lesson_id)]

    def ai_context(self, lesson_id: str):
        return [LessonSummary(**row) for row in self.db.read("""
            MATCH (source:Lesson {id: $id,status:'published'})
            MATCH (source)-[:REQUIRES|RELATED_TO*0..3]->(l:Lesson)<-[:HAS_LESSON]-(t:Topic)<-[:HAS_TOPIC]-(c:Chapter)
            WHERE l.status = 'published' AND t.status='published' AND coalesce(c.status,'published')='published'
            RETURN DISTINCT """ + FIELDS + " ORDER BY l.grade, l.id LIMIT 8", id=lesson_id)]
