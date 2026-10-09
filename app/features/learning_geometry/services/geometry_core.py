"""Geometry constraint engine preventing degenerate shapes during interaction."""

import math
from typing import Dict
from app.features.learning_geometry.models.content import GeometryPoint, GeometryShapeModel


class GeometryCoreEngine:
    """Core geometry calculation & shape constraint engine."""

    @staticmethod
    def update_parallelogram_vertex(
        vertices: Dict[str, GeometryPoint],
        dragged_vertex: str,
        new_x: float,
        new_y: float
    ) -> GeometryShapeModel:
        updated = {k: GeometryPoint(x=v.x, y=v.y) for k, v in vertices.items()}
        updated[dragged_vertex] = GeometryPoint(x=new_x, y=new_y)

        # Đỉnh D đang kéo phải được giữ, giải C = B + D - A.
        if dragged_vertex == 'D':
            A, B, D = updated['A'], updated['B'], updated['D']
            updated['C'] = GeometryPoint(x=B.x + D.x - A.x, y=B.y + D.y - A.y)
        A, B, C = updated['A'], updated['B'], updated['C']

        # D = C + A - B
        D_x = C.x + (A.x - B.x)
        D_y = C.y + (A.y - B.y)
        updated['D'] = GeometryPoint(x=D_x, y=D_y)

        area = GeometryCoreEngine.calculate_polygon_area(updated)
        if area < 1e-4:
            return GeometryShapeModel(
                shape_type="parallelogram",
                vertices=vertices,
                is_valid=False,
                error_message="Hình bị suy biến: Diện tích quá nhỏ hoặc các đỉnh trùng nhau!"
            )

        return GeometryShapeModel(
            shape_type="parallelogram",
            vertices=updated,
            is_valid=True
        )

    @staticmethod
    def calculate_distance(p1: GeometryPoint, p2: GeometryPoint) -> float:
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    @staticmethod
    def calculate_polygon_area(vertices: Dict[str, GeometryPoint]) -> float:
        pts = [vertices['A'], vertices['B'], vertices['C'], vertices['D']]
        n = len(pts)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += pts[i].x * pts[j].y
            area -= pts[j].x * pts[i].y
        return abs(area) / 2.0
