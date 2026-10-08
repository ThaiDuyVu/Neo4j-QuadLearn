"""Internal models for Learning Content & Geometry domain."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LocalizedText(BaseModel):
    vi: str
    en: Optional[str] = None


class LessonDetailModel(BaseModel):
    id: str
    title: LocalizedText
    content: LocalizedText
    latex_formulas: List[str] = Field(default_factory=list)
    grade: int
    topic_id: str
    cognitive_level: str = "KNOW"  # KNOW | UNDERSTAND | APPLY | ANALYZE
    status: str = "draft"  # draft | published
    prerequisites: List[str] = Field(default_factory=list)


class GeometryPoint(BaseModel):
    x: float
    y: float


class GeometryShapeModel(BaseModel):
    shape_type: str  # parallelogram | rectangle | rhombus | square
    vertices: Dict[str, GeometryPoint]  # A, B, C, D
    is_valid: bool = True
    error_message: Optional[str] = None


class ImportValidationReport(BaseModel):
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    total_records: int = 0