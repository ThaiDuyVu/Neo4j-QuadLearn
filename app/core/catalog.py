"""Shared read adapter: cây published content qua contract, không ghi catalog của Sơn.
Thêm để Vũ có metadata Chapter/Topic mà không sửa implementation feature Sơn.
Nhóm review; Sơn có thể chuyển adapter về ContentService khi mở rộng API.
"""

from app.shared.models.dto import CatalogLesson, LessonSummary


class GraphLearningCatalog:
    def __init__(self, db):
        self.db = db

    def catalog(self, grade):
        rows = self.db.read(
            """
            MATCH (:Level {grade:$grade})-[:HAS_CHAPTER]->(c:Chapter)-[:HAS_TOPIC]->(t:Topic)-[:HAS_LESSON]->(l:Lesson)
            WHERE l.status='published' AND t.status='published'
              AND coalesce(c.status,'published')='published' AND l.grade=$grade AND t.grade=$grade
            RETURN l.id AS id,l.title_vi AS title,l.grade AS grade,l.content_vi AS content,
              t.id AS topic_id,c.id AS chapter_id,c.name_vi AS chapter_title,t.name_vi AS topic_title,
              coalesce(t.cognitive_level,'') AS cognitive_level
            ORDER BY c.order,t.order,l.order,l.id
        """,
            grade=grade,
        )
        return [
            CatalogLesson(
                LessonSummary(
                    r["id"], r["title"], r["grade"], r["topic_id"], r["content"]
                ),
                r["chapter_id"],
                r["chapter_title"],
                r["topic_title"],
                r["cognitive_level"],
            )
            for r in rows
        ]
