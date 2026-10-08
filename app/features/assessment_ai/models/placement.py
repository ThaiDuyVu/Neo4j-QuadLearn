from dataclasses import dataclass

from .quiz import TestQuestion


@dataclass(frozen=True)
class PlacementForm:
    questions: tuple[TestQuestion, ...]


@dataclass(frozen=True)
class PlacementGradeScore:
    grade: int
    correct: int
    total: int
    score: float


@dataclass(frozen=True)
class PlacementResult:
    scores: tuple[PlacementGradeScore, ...]
