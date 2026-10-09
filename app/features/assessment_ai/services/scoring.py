"""Shared score calculation for assessment workflows."""


def score(correct: int, total: int) -> float:
    """Chấm thang 10 cho bài trắc nghiệm."""
    if total <= 0 or not 0 <= correct <= total:
        raise ValueError("Số câu không hợp lệ")
    return round(correct / total * 10, 2)
