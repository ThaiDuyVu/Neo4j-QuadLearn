import unittest

from app.features.assessment_ai.repositories.assessment import AssessmentRepository


class FakeDb:
    def __init__(self, rows=()):
        self.rows = list(rows)
        self.calls = []

    def read(self, query, **params):
        self.calls.append((query, params))
        return self.rows


class RepositoryTests(unittest.TestCase):
    def test_question_filters_are_parameters_and_option_maps_are_read(self):
        db = FakeDb([{
            "id": "question:1", "topic_id": "topic:8:x", "grade": 8,
            "difficulty": "recognize", "kind": "single", "text": "Q",
            "explanation": "E", "image_url": "", "options": [
                {"id": "option:1", "text": "A", "correct": True}],
        }])
        questions = AssessmentRepository(db).questions(8, "topic:8:x", "recognize")
        self.assertEqual(questions[0].options[0].id, "option:1")
        query, params = db.calls[0]
        self.assertIn("q.status = 'published'", query)
        self.assertEqual(params, {"grade": 8, "topic_id": "topic:8:x", "difficulty": "recognize"})

    def test_attempt_detail_is_scoped_to_user(self):
        db = FakeDb()
        AssessmentRepository(db).attempt_detail("user:1", "attempt:1")
        query, params = db.calls[0]
        self.assertIn("User {id:$user_id}", query)
        self.assertIn("selected_options", query)
        self.assertIn("correct_options", query)
        self.assertEqual(params, {"user_id": "user:1", "attempt_id": "attempt:1"})

    def test_attempt_history_exposes_grade_and_timestamps_for_reader(self):
        db = FakeDb()
        AssessmentRepository(db).attempt_history("user:1")
        query, params = db.calls[0]
        self.assertIn("t.grade AS grade", query)
        self.assertIn("started_at", query)
        self.assertIn("finished_at", query)
        self.assertIn("duration_seconds", query)
        self.assertIn("a.status='completed'", query)
        self.assertEqual(params, {"user_id": "user:1"})

    def test_essay_reviews_are_scoped_to_user(self):
        db = FakeDb()
        AssessmentRepository(db).essay_reviews("user:1")
        query, params = db.calls[0]
        self.assertIn("User {id:$user_id}", query)
        self.assertEqual(params, {"user_id": "user:1"})

    def test_preview_is_scoped_to_topic(self):
        db = FakeDb()
        preview = AssessmentRepository(db).preview_assessment("topic:8:x")
        self.assertEqual(preview, {"questions": [], "essays": []})
        self.assertEqual(len(db.calls), 2)
        self.assertTrue(all(params == {"topic_id": "topic:8:x"}
                            for _, params in db.calls))

    def test_placement_queries_only_published_questions_and_use_parameters(self):
        db = FakeDb()
        repository = AssessmentRepository(db)
        repository.placement_questions((6, 7, 8, 9))
        repository.placement_questions_by_ids(("question:6", "question:7"))
        self.assertEqual(db.calls[0][1], {"grades": [6, 7, 8, 9]})
        self.assertEqual(db.calls[1][1], {"ids": ["question:6", "question:7"]})
        self.assertTrue(all("q.status='published'" in query and "t.status='published'" in query
                            for query, _ in db.calls))


if __name__ == "__main__":
    unittest.main()
