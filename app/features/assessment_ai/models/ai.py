from dataclasses import dataclass
from typing import Protocol
from app.shared.models.dto import LessonSummary

@dataclass(frozen=True)
class AIRequest:
    question: str
    grade: int
    language: str
    context: tuple[LessonSummary, ...]

class AIProvider(Protocol):
    def respond(self, request: AIRequest) -> str: ...
