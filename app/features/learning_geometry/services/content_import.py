"""Service executing transactional lesson imports."""

from typing import Dict, Any, Tuple
from app.features.learning_geometry.services.import_validation import ImportValidationService
from app.features.learning_geometry.repositories.import_log import ImportLogRepository


class ContentImportService:
    def __init__(self, validator: ImportValidationService, log_repo: ImportLogRepository, db_driver=None):
        self.validator = validator
        self.log_repo = log_repo
        self.driver = db_driver

    def import_lessons(self, payload: Dict[str, Any], user_id: str) -> Tuple[bool, Dict[str, Any]]:
        report = self.validator.validate_lessons_payload(payload)
        if not report.is_valid:
            self.log_repo.create_import_log(user_id, 0, len(report.errors), report.errors)
            return False, {"errors": report.errors, "warnings": report.warnings}

        lessons = payload.get("lessons", [])
        if not self.driver:
            raise ValueError("Chưa kết nối database; không có nội dung nào được nhập.")

        query = """
        UNWIND $lessons AS item
        MATCH (t:Topic {id: item.topic_id})
        MERGE (l:Lesson {id: item.id})
        SET l.title_vi = item.title.vi,
            l.title_en = item.title.en,
            l.content_vi = item.content.vi,
            l.content_en = item.content.en,
            l.grade = item.grade,
            l.status = 'draft'
        MERGE (t)-[:HAS_LESSON]->(l)
        WITH l, item
        UNWIND item.prerequisites AS prereq_id
        MATCH (p:Lesson {id: prereq_id})
        MERGE (l)-[:REQUIRES]->(p)
        """
        with self.driver.session() as session:
            session.run(query, lessons=lessons)

        self.log_repo.create_import_log(user_id, len(lessons), 0, [])
        return True, {"imported_count": len(lessons), "warnings": report.warnings}