import unittest

from app.features.assessment_ai.services.essay import EssayService


class FakeRepository:
    def __init__(self):
        self.saved = []

    def save_essay_review(self, *args):
        self.saved.append(args)


class EssayReviewTests(unittest.TestCase):
    def test_review_saves_rating_and_hint_count(self):
        repo = FakeRepository()
        review_id = EssayService(repo).save_review(
            "user:1", "essay:1", "understood", 2, "  S = a × b  ")
        self.assertTrue(review_id.startswith("essay-review:"))
        self.assertEqual(repo.saved[0][:5], ("user:1", "essay:1", review_id,
                                           "understood", 2))
        self.assertEqual(repo.saved[0][-1], "S = a × b")

    def test_invalid_review_does_not_write(self):
        repo = FakeRepository()
        for rating, hints_used in (("maybe", 0), ("understood", -1),
                                   ("understood", True)):
            with self.subTest(rating=rating, hints_used=hints_used), self.assertRaises(ValueError):
                EssayService(repo).save_review("user:1", "essay:1", rating, hints_used)
        self.assertEqual(repo.saved, [])

    def test_oversized_answer_does_not_write(self):
        repo = FakeRepository()
        with self.assertRaises(ValueError):
            EssayService(repo).save_review("user:1", "essay:1", "understood", 0,
                                           "x" * 10001)
        self.assertEqual(repo.saved, [])


if __name__ == "__main__":
    unittest.main()
