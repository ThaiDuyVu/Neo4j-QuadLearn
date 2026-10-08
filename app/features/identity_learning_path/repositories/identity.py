# DOMAIN OWNER: VU · identity_learning_path
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
from app.shared.contracts.ports import QueryExecutor
from app.shared.models.dto import CurrentUser

class IdentityRepository:
    def __init__(self, db: QueryExecutor):
        self.db = db

    def user_by_id(self, user_id: str) -> CurrentUser | None:
        rows = self.db.read("""
            MATCH (u:User {id: $id})-[:STUDIES_AT]->(l:Level)
            RETURN u.id AS id, u.name AS name, l.grade AS grade, u.role AS role
        """, id=user_id)
        return CurrentUser(**rows[0]) if rows else None
