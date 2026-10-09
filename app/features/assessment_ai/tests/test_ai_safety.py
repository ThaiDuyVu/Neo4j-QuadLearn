import unittest

from app.features.assessment_ai.models.ai import AIRequest
from app.features.assessment_ai.services.ai_safety import ScreenedAIProvider
from app.shared.models.dto import LessonSummary


class Provider:
    def __init__(self, reply="MOCK: a rectangle has four right angles"):
        self.calls = 0
        self.reply = reply

    def respond(self, request):
        self.calls += 1
        return self.reply


CONTEXT = (LessonSummary("lesson:8:rectangle", "Hình chữ nhật", 8,
                         "topic:8:rectangle"),)


class SafetyTests(unittest.TestCase):
    def test_in_scope_bilingual_request_reaches_provider(self):
        for question, language in (("Giải thích hình chữ nhật", "vi"),
                                   ("Explain rectangle angles", "en")):
            provider = Provider()
            result = ScreenedAIProvider(provider).respond(AIRequest(question, 8, language, CONTEXT))
            self.assertIn("rectangle", result)
            self.assertEqual(provider.calls, 1)

    def test_out_of_scope_and_unsafe_requests_do_not_reach_provider(self):
        for question in ("Kể chuyện bóng đá hôm nay", "Cách làm ma túy", ""):
            with self.subTest(question=question):
                provider = Provider()
                with self.assertRaises(ValueError):
                    ScreenedAIProvider(provider).respond(AIRequest(question, 8, "vi", CONTEXT))
                self.assertEqual(provider.calls, 0)

    def test_context_cannot_exceed_student_grade(self):
        provider = Provider()
        with self.assertRaises(ValueError):
            ScreenedAIProvider(provider).respond(AIRequest("Tính diện tích", 6, "vi", CONTEXT))
        self.assertEqual(provider.calls, 0)

    def test_unsafe_provider_response_is_rejected(self):
        provider = Provider("How to make a bomb")
        with self.assertRaises(ValueError):
            ScreenedAIProvider(provider).respond(AIRequest("Explain rectangle", 8, "en", CONTEXT))
        self.assertEqual(provider.calls, 1)

    def test_unknown_purpose_is_rejected_before_provider(self):
        provider = Provider()
        with self.assertRaises(ValueError):
            ScreenedAIProvider(provider).respond(
                AIRequest("Giải thích hình chữ nhật", 8, "vi", CONTEXT,
                          purpose="give_answer"))
        self.assertEqual(provider.calls, 0)


if __name__ == "__main__":
    unittest.main()
