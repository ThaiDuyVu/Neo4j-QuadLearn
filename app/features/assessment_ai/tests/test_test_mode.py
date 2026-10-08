import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from app.features.assessment_ai.models.quiz import Option, Question
from app.features.assessment_ai.services.quiz import QuizService


QUESTIONS = [
    Question("question:1", "topic:8:x", 8, "recognize", "single", "Hình chữ nhật?", "E1",
             (Option("option:a", "A", True), Option("option:b", "B", False))),
    Question("question:2", "topic:8:x", 8, "understand", "multiple", "Đường chéo?", "E2",
             (Option("option:c", "C", True), Option("option:d", "D", False))),
]


class FakeRepository:
    def __init__(self):
        self.draft = None
        self.completed = None

    def questions(self, grade, topic_id, difficulty):
        return QUESTIONS

    def questions_for_attempt(self, topic_id, ids):
        return [q for q in QUESTIONS if q.id in ids]

    def start_test(self, user_id, grade, topic_id, attempt_id, question_ids,
                   option_orders, started_at, duration_seconds):
        self.owner = user_id
        self.draft = {"id": attempt_id, "topic_id": topic_id,
                      "question_ids": question_ids, "option_orders": option_orders,
                      "started_at": started_at, "duration_seconds": duration_seconds,
                      "selections": {}}

    def test_draft(self, user_id, attempt_id):
        if user_id != getattr(self, "owner", None) or self.draft is None:
            return None
        return self.draft

    def save_test_draft(self, user_id, attempt_id, selections):
        assert user_id == self.owner and attempt_id == self.draft["id"]
        self.draft["selections"] = selections

    def complete_test(self, user_id, result):
        assert user_id == self.owner
        self.completed = result
        self.draft = None


class TestModeTests(unittest.TestCase):
    def test_start_shuffle_public_view_and_resume(self):
        repo = FakeRepository()
        service = QuizService(repo)
        session = service.start_test("user:1", 8, "topic:8:x", 600)
        self.assertEqual({q.id for q in session.questions}, {q.id for q in QUESTIONS})
        self.assertEqual({q.id for q in service.resume_test("user:1", session.id).questions},
                         {q.id for q in QUESTIONS})
        self.assertFalse(hasattr(session.questions[0].options[0], "correct"))
        self.assertFalse(hasattr(session.questions[0], "explanation"))
        self.assertEqual(service.seconds_left(
            session, datetime.fromisoformat(session.started_at) + timedelta(seconds=601)), 0)

    def test_seconds_left_accepts_neo4j_fractional_timestamp(self):
        repo = FakeRepository()
        service = QuizService(repo)
        session = service.start_test("user:1", 8, "topic:8:x", 600)
        session = replace(session, started_at="2026-10-08T17:37:00.05611+00:00[UTC]")
        now = datetime(2026, 10, 8, 17, 37, 1, tzinfo=timezone.utc)
        self.assertEqual(service.seconds_left(session, now), 600)

    def test_save_draft_and_submit_grades_unanswered_as_wrong(self):
        repo = FakeRepository()
        service = QuizService(repo)
        session = service.start_test("user:1", 8, "topic:8:x", 600)
        service.save_test_draft("user:1", session, {"question:1": ("option:a",)})
        resumed = service.resume_test("user:1", session.id)
        self.assertEqual(resumed.selections["question:1"], ("option:a",))
        result = service.submit_test("user:1", session.id)
        self.assertEqual(result.score, 5)
        self.assertEqual(sum(answer.correct for answer in result.answers), 1)
        self.assertEqual(repo.completed.id, session.id)

    def test_wrong_user_and_invalid_selection_rejected(self):
        repo = FakeRepository()
        service = QuizService(repo)
        session = service.start_test("user:1", 8, "topic:8:x", 600)
        with self.assertRaises(ValueError):
            service.resume_test("user:2", session.id)
        with self.assertRaises(ValueError):
            service.save_test_draft("user:1", session,
                                    {"question:1": ("option:unknown",)})
        self.assertEqual(repo.draft["selections"], {})


if __name__ == "__main__":
    unittest.main()
