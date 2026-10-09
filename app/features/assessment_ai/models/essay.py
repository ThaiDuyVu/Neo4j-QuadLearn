from dataclasses import dataclass


@dataclass(frozen=True)
class EssayHint:
    order: int
    text: str
    image_url: str = ""


@dataclass(frozen=True)
class EssayProblem:
    id: str
    topic_id: str
    grade: int
    prompt: str
    assumptions: str
    conclusion: str
    solution: str
    hints: tuple[EssayHint, ...]
    image_url: str = ""
    kind: str = "calculation"


def validate_essay(essay: EssayProblem) -> None:
    if essay.grade not in (6, 7, 8, 9):
        raise ValueError("Lớp không hợp lệ")
    if essay.grade == 6 and essay.kind == "proof":
        raise ValueError("Bài chứng minh không dành cho lớp 6")
    if not essay.prompt.strip() or not essay.solution.strip():
        raise ValueError("Thiếu đề hoặc lời giải")
    orders = [hint.order for hint in essay.hints]
    if orders != list(range(1, len(orders) + 1)):
        raise ValueError("Gợi ý phải liên tiếp từ bước 1")


def reveal_hint(essay: EssayProblem, revealed: int) -> tuple[EssayHint, ...]:
    validate_essay(essay)
    if revealed < 0 or revealed > len(essay.hints):
        raise ValueError("Số gợi ý không hợp lệ")
    return essay.hints[:revealed]
