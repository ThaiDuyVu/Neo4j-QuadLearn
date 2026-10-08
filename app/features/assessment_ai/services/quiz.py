from datetime import datetime, timezone
from random import SystemRandom
import re
from uuid import uuid4

from ..models.quiz import (AnswerResult, AttemptResult, Question, TestOption,
                           TestQuestion, TestSession)
from .scoring import score


def grade_answer(question: Question, selected_ids: tuple[str, ...]) -> AnswerResult:
    if question.kind not in {"single", "multiple", "true_false"}:
        raise ValueError("Loại câu hỏi không hợp lệ")
    option_ids = {option.id for option in question.options}
    correct_ids = {option.id for option in question.options if option.correct}
    if not option_ids or not correct_ids or correct_ids == option_ids:
        raise ValueError("Câu hỏi thiếu đáp án hợp lệ")
    if question.kind in {"single", "true_false"} and len(correct_ids) != 1:
        raise ValueError("Câu hỏi phải có đúng một đáp án")
    if question.kind == "true_false" and len(option_ids) != 2:
        raise ValueError("Câu đúng/sai phải có hai lựa chọn")
    chosen = set(selected_ids)
    if not chosen or len(chosen) != len(selected_ids) or not chosen <= option_ids:
        raise ValueError("Lựa chọn trống, trùng hoặc không thuộc câu hỏi")
    if question.kind != "multiple" and len(chosen) != 1:
        raise ValueError("Chỉ được chọn một đáp án")
    return AnswerResult(question.id, tuple(selected_ids), chosen == correct_ids,
                        tuple(option.id for option in question.options if option.correct),
                        question.explanation)


class QuizService:
    def __init__(self, repository):
        self.repository = repository

    def questions(self, grade: int, topic_id: str | None = None, difficulty: str | None = None):
        if grade not in (6, 7, 8, 9):
            raise ValueError("Lớp không hợp lệ")
        if difficulty is not None and difficulty not in {"recognize", "understand", "apply"}:
            raise ValueError("Mức độ không hợp lệ")
        return self.repository.questions(grade, topic_id, difficulty)

    def submit(self, user_id: str, topic_id: str, selections: dict[str, tuple[str, ...]],
               started_at: datetime | None = None) -> AttemptResult:
        if not user_id or not topic_id or not selections:
            raise ValueError("Thiếu người học, chủ đề hoặc câu trả lời")
        questions = self.repository.questions_for_attempt(topic_id, tuple(selections))
        by_id = {question.id: question for question in questions}
        if set(selections) != set(by_id) or len(by_id) != len(questions):
            raise ValueError("Câu hỏi không thuộc chủ đề hoặc chưa xuất bản")
        answers = tuple(grade_answer(by_id[qid], chosen) for qid, chosen in selections.items())
        finished = datetime.now(timezone.utc)
        started = started_at or finished
        if started.tzinfo is None or started > finished:
            raise ValueError("Thời gian bắt đầu không hợp lệ")
        result = AttemptResult(f"attempt:{uuid4()}", topic_id,
                               score(sum(item.correct for item in answers), len(answers)),
                               answers, started.isoformat(), finished.isoformat())
        self.repository.save_attempt(user_id, result)
        return result

    def start_test(self, user_id: str, grade: int, topic_id: str,
                   duration_seconds: int = 900) -> TestSession:
        if not user_id or not topic_id or not 60 <= duration_seconds <= 3600:
            raise ValueError("Người học, chủ đề hoặc thời lượng không hợp lệ")
        questions = self.questions(grade, topic_id)
        if not questions or any(question.topic_id != topic_id for question in questions):
            raise ValueError("Chủ đề chưa có câu hỏi đã xuất bản")
        rng = SystemRandom()
        question_ids = [question.id for question in questions]
        rng.shuffle(question_ids)
        option_orders = {}
        for question in questions:
            option_orders[question.id] = [option.id for option in question.options]
            rng.shuffle(option_orders[question.id])
        attempt_id = f"attempt:{uuid4()}"
        started_at = datetime.now(timezone.utc).isoformat()
        self.repository.start_test(user_id, grade, topic_id, attempt_id,
                                   question_ids, option_orders, started_at,
                                   duration_seconds)
        return self.resume_test(user_id, attempt_id)

    def resume_test(self, user_id: str, attempt_id: str) -> TestSession:
        row = self.repository.test_draft(user_id, attempt_id)
        if row is None:
            raise ValueError("Không tìm thấy bài kiểm tra đang làm")
        questions = self.repository.questions_for_attempt(
            row["topic_id"], tuple(row["question_ids"]))
        by_id = {question.id: question for question in questions}
        if set(by_id) != set(row["question_ids"]):
            raise ValueError("Nội dung bài kiểm tra đã thay đổi")
        public = []
        for question_id in row["question_ids"]:
            question = by_id[question_id]
            options = {option.id: option for option in question.options}
            order = row["option_orders"][question_id]
            if set(options) != set(order):
                raise ValueError("Đáp án bài kiểm tra đã thay đổi")
            public.append(TestQuestion(
                question.id, question.kind, question.text, question.image_url,
                tuple(TestOption(options[key].id, options[key].text) for key in order)))
        return TestSession(row["id"], row["topic_id"], row["started_at"],
                           row["duration_seconds"], tuple(public),
                           {key: tuple(value) for key, value in row["selections"].items()})

    @staticmethod
    def seconds_left(session: TestSession, now: datetime | None = None) -> int:
        started_at = session.started_at.split("[")[0].replace("Z", "+00:00")
        started_at = re.sub(
            r"\.(\d+)(?=[+-]\d{2}:\d{2}$)",
            lambda match: "." + match.group(1)[:6].ljust(6, "0"),
            started_at,
        )
        started = datetime.fromisoformat(started_at)
        if started.tzinfo is None:
            raise ValueError("Thời gian bài kiểm tra thiếu múi giờ")
        now = now or datetime.now(timezone.utc)
        return max(0, session.duration_seconds - int((now - started).total_seconds()))

    def save_test_draft(self, user_id: str, session: TestSession,
                        selections: dict[str, tuple[str, ...]]) -> None:
        session = self.resume_test(user_id, session.id)
        if self.seconds_left(session) == 0:
            raise ValueError("Bài kiểm tra đã hết giờ")
        allowed = {question.id: {option.id for option in question.options}
                   for question in session.questions}
        if not set(selections) <= set(allowed):
            raise ValueError("Câu hỏi không thuộc bài kiểm tra")
        for question_id, chosen in selections.items():
            if len(chosen) != len(set(chosen)) or not set(chosen) <= allowed[question_id]:
                raise ValueError("Đáp án không thuộc câu hỏi hoặc bị trùng")
            kind = next(question.kind for question in session.questions
                        if question.id == question_id)
            if kind != "multiple" and len(chosen) > 1:
                raise ValueError("Câu hỏi này chỉ được chọn một đáp án")
        self.repository.save_test_draft(user_id, session.id, selections)

    def submit_test(self, user_id: str, attempt_id: str) -> AttemptResult:
        session = self.resume_test(user_id, attempt_id)
        questions = self.repository.questions_for_attempt(
            session.topic_id, tuple(question.id for question in session.questions))
        by_id = {question.id: question for question in questions}
        answers = []
        for question in session.questions:
            chosen = session.selections.get(question.id, ())
            if chosen:
                answers.append(grade_answer(by_id[question.id], chosen))
            else:
                original = by_id[question.id]
                answers.append(AnswerResult(question.id, (), False,
                                            tuple(option.id for option in original.options
                                                  if option.correct), original.explanation))
        finished_at = datetime.now(timezone.utc).isoformat()
        result = AttemptResult(attempt_id, session.topic_id,
                               score(sum(answer.correct for answer in answers), len(answers)),
                               tuple(answers), session.started_at, finished_at)
        self.repository.complete_test(user_id, result)
        return result
