"""Repository for managing ImportLog nodes."""

import datetime
from typing import List


class ImportLogRepository:
    def __init__(self, db_driver=None):
        self.driver = db_driver

    def create_import_log(self, imported_by: str, success_count: int, error_count: int, details: List[str]) -> bool:
        if not self.driver:
            return False
        query = """
        CREATE (log:ImportLog {
            id: randomUUID(),
            imported_by: $imported_by,
            timestamp: $timestamp,
            success_count: $success_count,
            error_count: $error_count,
            details: $details
        })
        RETURN log.id AS log_id
        """
        with self.driver.session() as session:
            session.run(
                query,
                imported_by=imported_by,
                timestamp=datetime.datetime.now().isoformat(),
                success_count=success_count,
                error_count=error_count,
                details=details
            )
            return True