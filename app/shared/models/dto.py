from dataclasses import dataclass
from typing import Any, Callable, List, Optional
from pydantic import BaseModel, ConfigDict, Field


@dataclass(frozen=True)
class CurrentUser:
    id: str
    name: str
    grade: int
    role: str
    demo: bool = True


@dataclass(frozen=True)
class LessonSummary:
    id: str
    title: str
    grade: int
    topic_id: str
    content: str = ""


@dataclass(frozen=True)
class AttemptSummary:
    id: str
    topic_id: str
    score: float
    status: str


@dataclass(frozen=True)
class CatalogLesson:
    lesson: LessonSummary
    chapter_id: str
    chapter_title: str
    topic_title: str
    cognitive_level: str


@dataclass(frozen=True)
class LevelSummary:
    grade: int
    total: int
    completed: int
    completion: float
    average_score: float | None
    unlocked: bool


class LessonDTO(BaseModel):
    id: str
    title_vi: str
    title_en: Optional[str] = None
    content_vi: str
    content_en: Optional[str] = None
    grade: int = 8
    topic_id: str = "TOPIC_UNKNOWN"
    status: str = "published"
    prerequisites: List[str] = Field(default_factory=list)

class PageSpec(BaseModel):
    """Specification for registering UI pages in navigation registry."""
    page_id: str
    title: str
    render_fn: Callable[..., Any]
    requires_auth: bool = False
    allowed_roles: Optional[List[str]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
