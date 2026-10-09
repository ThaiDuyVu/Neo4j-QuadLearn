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
    def geometry_graph(self, executor):
        """Một query lấy cả node cô lập và cạnh thật; không suy diễn thêm quan hệ."""
        rows = executor.read("""
            MATCH (q:Quadrilateral) WHERE q.id IS NOT NULL
            OPTIONAL MATCH (q)-[r:IS_A]->(parent:Quadrilateral)
            WHERE parent.id IS NOT NULL
            RETURN collect(DISTINCT {id:q.id,name:coalesce(q.name_vi,q.id)}) AS nodes,
                   collect(DISTINCT CASE WHEN r IS NOT NULL THEN {
                       id:elementId(r),source:q.id,target:parent.id,type:type(r)
                   } END) AS edges
        """)
        return rows[0] if rows else {"nodes": [], "edges": []}
