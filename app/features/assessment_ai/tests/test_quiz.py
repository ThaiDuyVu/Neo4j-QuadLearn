import unittest
from datetime import datetime, timezone

from app.features.assessment_ai.models.quiz import Option, Question
from app.features.assessment_ai.services.quiz import QuizService, grade_answer
from app.features.assessment_ai.services.assessment import score


def question(kind="single", correct=("a",), topic="topic:8:x"):
    return Question("question:1", topic, 8, "recognize", kind, "Q?", "Because",
                    tuple(Option(key, key, key in correct) for key in ("a", "b", "c")))


class FakeRepository:
    def __init__(self, questions):
        self.items = questions
        self.saved = []

    def questions_for_attempt(self, topic_id, ids):
        return [q for q in self.items if q.id in ids and q.topic_id == topic_id]

    def save_attempt(self, user_id, result):
        self.saved.append((user_id, result))


class QuizTests(unittest.TestCase):
    def test_score_boundaries(self):
        self.assertEqual([score(n, 5) for n in (0, 3, 5)], [0, 6, 10])
        for correct, total in ((0, 0), (-1, 5), (6, 5)):
            with self.subTest(correct=correct, total=total), self.assertRaises(ValueError):
                score(correct, total)

    def test_grading_types(self):
        cases = [("single", ("a",), ("a",), True),
                 ("single", ("a",), ("b",), False),
                 ("multiple", ("a", "b"), ("a", "b"), True),
                 ("multiple", ("a", "b"), ("a",), False)]
        for kind, correct, selected, expected in cases:
            with self.subTest(kind=kind, selected=selected):
                self.assertEqual(grade_answer(question(kind, correct), selected).correct, expected)

    def test_invalid_single_selection(self):
        for selected in ((), ("x",), ("a", "a"), ("a", "b")):
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                grade_answer(question(), selected)

    def test_true_false_requires_two_options(self):
        with self.assertRaises(ValueError):
            grade_answer(question("true_false"), ("a",))

    def test_submit_creates_new_attempt_every_time_with_all_answers(self):
        repo = FakeRepository([question()])
        service = QuizService(repo)
        first = service.submit("user:1", "topic:8:x", {"question:1": ("a",)},
                               datetime(2026, 1, 1, tzinfo=timezone.utc))
        second = service.submit("user:1", "topic:8:x", {"question:1": ("b",)})
        self.assertNotEqual(first.id, second.id)
        self.assertEqual((first.score, second.score), (10, 0))
        self.assertEqual([row[0] for row in repo.saved], ["user:1", "user:1"])
        self.assertEqual(first.answers[0].selected_ids, ("a",))

    def test_submit_rejects_question_outside_topic_without_writing(self):
        repo = FakeRepository([question(topic="topic:8:other")])
        with self.assertRaises(ValueError):
            QuizService(repo).submit("user:1", "topic:8:x", {"question:1": ("a",)})
        self.assertEqual(repo.saved, [])


if __name__ == "__main__":
    unittest.main()
