import unittest
from unittest.mock import patch

from app.features.assessment_ai.models.ai import AIRequest
from app.features.assessment_ai.services.mock_ai import MockAIProvider
from app.shared.models.dto import LessonSummary


class MockAITests(unittest.TestCase):
    def test_mock_label_and_context_in_both_languages(self):
        context = (LessonSummary("lesson:8:x", "Rectangle", 8, "topic:8:x"),)
        provider = MockAIProvider()
        for language in ("vi", "en"):
            with self.subTest(language=language):
                reply = provider.respond(AIRequest("Explain", 8, language, context))
                self.assertIn("MOCK", reply)
                self.assertIn("Rectangle", reply)

    def test_invalid_grade_or_language(self):
        for grade, language in ((5, "vi"), (8, "fr")):
            with self.subTest(grade=grade, language=language), self.assertRaises(ValueError):
                MockAIProvider().respond(AIRequest("?", grade, language, ()))

    def test_mock_does_not_open_network_socket(self):
        with patch("socket.socket", side_effect=AssertionError("network called")):
            reply = MockAIProvider().respond(AIRequest("Hình chữ nhật", 8, "vi", ()))
        self.assertIn("MOCK", reply)

    def test_grade_changes_guidance_without_identity_data(self):
        lower = MockAIProvider().respond(AIRequest("Hình chữ nhật", 6, "vi", ()))
        upper = MockAIProvider().respond(AIRequest("Hình chữ nhật", 8, "vi", ()))
        self.assertIn("quan sát", lower)
        self.assertIn("lập luận", upper)
        self.assertNotEqual(lower, upper)

    def test_test_mode_hint_withholds_correct_option(self):
        request = AIRequest("Gợi mở cách nghĩ về hình chữ nhật trong hình học tứ giác",
                            8, "vi", (), purpose="assessment_hint")
        reply = MockAIProvider().respond(request)
        self.assertIn("Chỉ gợi mở", reply)
        self.assertNotIn("4 góc vuông", reply)

    def test_test_hint_never_repeats_solution_context(self):
        provider = MockAIProvider()
        for grade in (6, 7, 8, 9):
            for language in ("vi", "en"):
                with self.subTest(grade=grade, language=language):
                    context = (LessonSummary(
                        "lesson:secret", "Nguồn", grade, "topic:x",
                        "SECRET_ANSWER: option B; S=12"),)
                    reply = provider.respond(AIRequest(
                        "Gợi mở bài hình chữ nhật" if language == "vi"
                        else "Give a rectangle hint",
                        grade, language, context, purpose="assessment_hint"))
                    self.assertNotIn("SECRET_ANSWER", reply)
                    self.assertNotIn("option B", reply)
                    self.assertNotIn("S=12", reply)


if __name__ == "__main__":
    unittest.main()
