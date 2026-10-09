import unittest

from app.features.assessment_ai.models.essay import (
    EssayHint, EssayProblem, reveal_hint, validate_essay,
)


def essay(grade=8, kind="proof", orders=(1, 2)):
    return EssayProblem("essay:1", "topic:8:x", grade, "Đề", "GT", "KL", "Lời giải",
                        tuple(EssayHint(order, str(order)) for order in orders), kind=kind)


class EssayTests(unittest.TestCase):
    def test_hints_reveal_sequentially(self):
        problem = essay()
        self.assertEqual(reveal_hint(problem, 0), ())
        self.assertEqual([hint.order for hint in reveal_hint(problem, 1)], [1])
        self.assertEqual([hint.order for hint in reveal_hint(problem, 2)], [1, 2])

    def test_invalid_essay_metadata(self):
        for problem in (essay(6), essay(8, orders=(1, 3)), essay(5)):
            with self.subTest(problem=problem), self.assertRaises(ValueError):
                validate_essay(problem)

    def test_grade_six_calculation_allowed(self):
        validate_essay(essay(6, "calculation"))

    def test_cannot_skip_past_last_hint(self):
        with self.assertRaises(ValueError):
            reveal_hint(essay(), 3)


if __name__ == "__main__":
    unittest.main()
