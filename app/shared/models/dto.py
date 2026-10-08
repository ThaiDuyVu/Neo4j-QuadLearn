from dataclasses import dataclass

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
