"""Repository for quadrilateral taxonomy operations."""

from typing import Dict, Any, List


class TaxonomyRepository:
    def __init__(self, db_driver=None):
        self.driver = db_driver

    def get_shape_taxonomy_chain(self, shape_id: str) -> List[Dict[str, Any]]:
        """Lấy chuỗi quan hệ IS_A (ví dụ: Hình vuông IS_A Hình chữ nhật IS_A Hình bình hành)."""
        if not self.driver:
            return []
        query = """
        MATCH (q:Quadrilateral {id: $shape_id})-[:IS_A*1..3]->(parent:Quadrilateral)
        RETURN parent.id AS id, parent.name_vi AS name_vi, parent.description_vi AS description
        """
        with self.driver.session() as session:
            result = session.run(query, shape_id=shape_id)
            return [dict(record) for record in result]