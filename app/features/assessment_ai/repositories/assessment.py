# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
from app.shared.contracts.ports import QueryExecutor
from app.shared.models.dto import AttemptSummary

class AssessmentRepository:
    def __init__(self, db: QueryExecutor):
        self.db = db

    def attempts(self, user_id: str):
        return [AttemptSummary(**r) for r in self.db.read("""
            MATCH (:User {id: $id})-[:ATTEMPTED]->(a:Attempt)-[:FOR_TOPIC]->(t:Topic)
            RETURN a.id AS id, t.id AS topic_id, a.score AS score, a.status AS status
            ORDER BY a.started_at DESC, a.id
        """, id=user_id)]
