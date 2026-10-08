from datetime import datetime, timezone
from uuid import uuid4


class EssayService:
    def __init__(self, repository):
        self.repository = repository

    def save_review(self, user_id: str, essay_id: str, rating: str,
                    hints_used: int, answer_text: str = "") -> str:
        if not user_id or not essay_id:
            raise ValueError("Thiếu người học hoặc đề tự luận")
        if rating not in {"understood", "review_again"}:
            raise ValueError("Mức tự đánh giá không hợp lệ")
        if not isinstance(hints_used, int) or isinstance(hints_used, bool) or hints_used < 0:
            raise ValueError("Số gợi ý không hợp lệ")
        if not isinstance(answer_text, str) or len(answer_text.strip()) > 10000:
            raise ValueError("Bài làm không hợp lệ hoặc quá 10000 ký tự")
        review_id = f"essay-review:{uuid4()}"
        self.repository.save_essay_review(user_id, essay_id, review_id, rating,
                                          hints_used, datetime.now(timezone.utc).isoformat(),
                                          answer_text.strip())
        return review_id
