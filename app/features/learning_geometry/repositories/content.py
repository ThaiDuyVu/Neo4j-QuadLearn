# DOMAIN OWNER: SON · learning_geometry
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
from app.shared.contracts.ports import QueryExecutor
from app.shared.models.dto import LessonSummary

FIELDS = "l.id AS id, l.title_vi AS title, l.grade AS grade, t.id AS topic_id, l.content_vi AS content"

class ContentRepository:
    def __init__(self, db: QueryExecutor):
        self.db = db

    def lessons(self, grade: int):
        return [LessonSummary(**row) for row in self.db.read("""
            MATCH (:Level {grade: $grade})-[:HAS_CHAPTER]->(:Chapter)-[:HAS_TOPIC]->(t:Topic)-[:HAS_LESSON]->(l:Lesson)
            WHERE l.status = 'published'
            RETURN """ + FIELDS + " ORDER BY l.order, l.id", grade=grade)]

    def prerequisites(self, lesson_id: str):
        return [LessonSummary(**row) for row in self.db.read("""
            MATCH (:Lesson {id: $id})-[:REQUIRES*1..8]->(l:Lesson)<-[:HAS_LESSON]-(t:Topic)
            WHERE l.status = 'published'
            RETURN DISTINCT """ + FIELDS + " ORDER BY l.grade, l.id", id=lesson_id)]

    def ai_context(self, lesson_id: str):
        return [LessonSummary(**row) for row in self.db.read("""
            MATCH (source:Lesson {id: $id})
            MATCH (source)-[:REQUIRES|RELATED_TO*0..3]->(l:Lesson)<-[:HAS_LESSON]-(t:Topic)
            WHERE l.status = 'published'
            RETURN DISTINCT """ + FIELDS + " ORDER BY l.grade, l.id LIMIT 8", id=lesson_id)]
