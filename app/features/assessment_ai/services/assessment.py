# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
class AssessmentService:
    def __init__(self, repository):
        self.repository = repository

    def attempts(self, user_id: str):
        return self.repository.attempts(user_id)

def score(correct: int, total: int) -> float:
    """Chấm thang 10; workflow lưu bài làm sẽ do Đạt triển khai."""
    if total <= 0 or not 0 <= correct <= total:
        raise ValueError("Số câu không hợp lệ")
    return round(correct / total * 10, 2)
