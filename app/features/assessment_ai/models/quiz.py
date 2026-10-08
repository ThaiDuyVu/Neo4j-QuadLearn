from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    id: str
    text: str
    correct: bool


@dataclass(frozen=True)
class Question:
    id: str
    topic_id: str
    grade: int
    difficulty: str
    kind: str
    text: str
    explanation: str
    options: tuple[Option, ...]
    image_url: str = ""


@dataclass(frozen=True)
class AnswerResult:
    question_id: str
    selected_ids: tuple[str, ...]
    correct: bool
    correct_ids: tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class AttemptResult:
    id: str
    topic_id: str
    score: float
    answers: tuple[AnswerResult, ...]
    started_at: str
    finished_at: str


@dataclass(frozen=True)
class TestOption:
    id: str
    text: str


@dataclass(frozen=True)
class TestQuestion:
    id: str
    kind: str
    text: str
    image_url: str
    options: tuple[TestOption, ...]


@dataclass(frozen=True)
class TestSession:
    id: str
    topic_id: str
    started_at: str
    duration_seconds: int
    questions: tuple[TestQuestion, ...]
    selections: dict[str, tuple[str, ...]]
