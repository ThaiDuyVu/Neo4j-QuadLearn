from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

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

    class Config:
        arbitrary_types_allowed = True