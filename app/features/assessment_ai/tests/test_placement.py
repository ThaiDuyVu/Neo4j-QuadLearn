import unittest

from app.features.assessment_ai.models.quiz import Option, Question
from app.features.assessment_ai.services.placement import PlacementService


def question(grade: int, correct: str = "a") -> Question:
    return Question(
        f"question:{grade}", f"topic:{grade}", grade, "recognize", "single",
        f"Câu lớp {grade}", "Giải thích",
        (Option(f"option:{grade}:a", "A", correct == "a"),
         Option(f"option:{grade}:b", "B", correct == "b")),
    )


QUESTIONS = tuple(question(grade) for grade in (6, 7, 8, 9))


class FakeRepository:
    def placement_questions(self, grades):
        return [item for item in QUESTIONS if item.grade in grades]

    def placement_questions_by_ids(self, ids):
        return [item for item in QUESTIONS if item.id in ids]


class MissingGradeRepository(FakeRepository):
    def placement_questions(self, grades):
        return list(QUESTIONS[:-1])


class PlacementTests(unittest.TestCase):
    def test_form_covers_grades_without_exposing_answers(self):
        form = PlacementService(FakeRepository()).form((6, 7, 8, 9), per_grade=2)
        self.assertEqual({int(item.id.split(":")[1]) for item in form.questions},
                         {6, 7, 8, 9})
        self.assertTrue(all(not hasattr(option, "correct")
                            for item in form.questions for option in item.options))
        self.assertTrue(all(not hasattr(item, "explanation") for item in form.questions))

    def test_grade_returns_breakdown_without_recommending_or_updating_grade(self):
        ids = tuple(item.id for item in QUESTIONS)
        selections = {item.id: (f"option:{item.grade}:a",) for item in QUESTIONS}
        result = PlacementService(FakeRepository()).grade(ids, selections)
        self.assertEqual([(item.grade, item.score) for item in result.scores],
                         [(6, 10.0), (7, 10.0), (8, 10.0), (9, 10.0)])
        self.assertFalse(hasattr(result, "recommended_grade"))

    def test_missing_grade_or_tampered_answers_are_rejected(self):
        service = PlacementService(FakeRepository())
        with self.assertRaises(ValueError):
            service.form((5, 6))
        with self.assertRaisesRegex(ValueError, "Chưa đủ"):
            PlacementService(MissingGradeRepository()).form((6, 7, 8, 9))
        with self.assertRaises(ValueError):
            service.grade(("question:6",), {})
        with self.assertRaises(ValueError):
            service.grade(("question:missing",), {"question:missing": ("option:x",)})


if __name__ == "__main__":
    unittest.main()
