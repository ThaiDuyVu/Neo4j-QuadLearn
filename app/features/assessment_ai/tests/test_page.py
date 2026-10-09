"""Exercise the expanded assessment page with fake domain ports."""

from streamlit.testing.v1 import AppTest

from app.core.context import AppContext
from app.features.assessment_ai.models.essay import EssayHint, EssayProblem
from app.features.assessment_ai.services.chat import ChatReply
from app.features.assessment_ai.pages.overview import _source_links
from app.features.assessment_ai.models.quiz import (
    Option, Question, TestOption as PublicOption,
    TestQuestion as PublicQuestion, TestSession as PublicSession,
)
from app.shared.models.dto import AttemptSummary
from tests.fakes import FakeContent, FakeIdentity


class FakeAssessment:
    def attempts(self, user_id):
        return []

    def questions(self, grade):
        return [Question("question:1", "topic:test", 8, "recognize", "single",
                         "Hình chữ nhật có mấy góc vuông?", "Có bốn góc vuông.",
                         (Option("option:4", "4", True),
                          Option("option:2", "2", False)))]

    def test_drafts(self, user_id):
        return []

    def essays(self, grade):
        return [EssayProblem("essay:1", "topic:test", 8, "Tính diện tích hình chữ nhật",
                             "Chiều dài 4, rộng 2", "Diện tích", "$S=4\\times2=8$",
                             (EssayHint(1, "Dùng công thức $S=a\\times b$."),))]

    def essay_reviews(self, user_id):
        return []

    def save_essay_review(self, user_id, essay_id, rating, hints_used, answer_text):
        self.saved = (user_id, essay_id, rating, hints_used, answer_text)


assessment = FakeAssessment()


def context():
    return AppContext(FakeIdentity(), FakeContent(), assessment)


class DraftAssessment(FakeAssessment):
    def attempts(self, user_id):
        return [AttemptSummary("attempt:old", "topic:test", 10, "completed")]

    def attempt_detail(self, user_id, attempt_id):
        raise AssertionError("Đáp án cũ không được đọc trong bài kiểm tra")

    def test_drafts(self, user_id):
        return [{"id": "attempt:draft", "topic_id": "topic:test"}]

    def resume_test(self, user_id, attempt_id):
        question = PublicQuestion("question:1", "single", "Hình chữ nhật?", "",
                                  (PublicOption("option:4", "4"),
                                   PublicOption("option:2", "2")))
        return PublicSession(attempt_id, "topic:test", "2026-01-01T00:00:00+00:00",
                             300, (question,), {})

    def test_seconds_left(self, session):
        return 200


def draft_context():
    return AppContext(FakeIdentity(), FakeContent(), DraftAssessment())


class ChatAssessment(FakeAssessment):
    def chat_sessions(self, user_id):
        return [{"id": "chat:existing", "lesson_id": "lesson:test",
                 "lesson_title": "Rectangle"}]

    def chat_messages(self, user_id, session_id):
        return [{"id": "message:existing", "role": "assistant",
                 "content": "MOCK", "sources": [], "feedback": "helpful",
                 "report": True}]

    def ask_ai(self, user_id, request, session_id=None):
        self.followup_id = session_id
        return ChatReply("MOCK", 9, (), session_id or "chat:new")


chat_assessment = ChatAssessment()


def chat_context():
    return AppContext(FakeIdentity(), FakeContent(), chat_assessment)


def test_assessment_page_renders_quiz_and_essay_without_database():
    source = """
from app.features.assessment_ai.tests.test_page import context
from app.features.assessment_ai.pages.overview import render
render(context())
"""
    app = AppTest.from_string(source).run(timeout=20)
    assert not app.exception
    assert any("Luyện tập trắc nghiệm" in item.value for item in app.subheader)
    assert any("Bài tự luận" in item.value for item in app.subheader)
    assert len(app.text_area) == 1


def test_source_links_navigate_to_learning_page_and_encode_id():
    links = _source_links(["lesson:8/rectangle", "lesson:8:x y"])
    assert "/learning?lesson_id=lesson%3A8%2Frectangle" in links
    assert "lesson%3A8%3Ax%20y" in links


def test_essay_answer_is_passed_to_review_service():
    source = """
from app.features.assessment_ai.tests.test_page import context
from app.features.assessment_ai.pages.overview import render
render(context())
"""
    app = AppTest.from_string(source).run(timeout=20)
    app.text_area[0].set_value("$S=4\\times2=8$").run()
    review_button = next(button for button in app.button if button.label == "Lưu tự đánh giá")
    app.radio[-1].set_value("Đã hiểu").run()
    review_button = next(button for button in app.button if button.label == "Lưu tự đánh giá")
    review_button.click().run()
    assert not app.exception
    assert assessment.saved == ("user:test", "essay:1", "understood", 0,
                                "$S=4\\times2=8$")


def test_active_test_hides_practice_answers_and_attempt_detail():
    source = """
from app.features.assessment_ai.tests.test_page import draft_context
from app.features.assessment_ai.pages.overview import render
render(draft_context())
"""
    app = AppTest.from_string(source).run(timeout=20)
    assert not app.exception
    assert next(button for button in app.button
                if button.label == "Kiểm tra câu").disabled
    assert next(button for button in app.button
                if button.label == "Nộp bài luyện tập").disabled
    assert next(button for button in app.button
                if button.label == "Gửi câu hỏi").disabled
    assert next(button for button in app.button
                if button.label == "Bắt đầu bài kiểm tra").disabled
    assert not any(box.label == "Xem lại lần làm" for box in app.selectbox)
    assert not any("Bài tự luận" in item.value for item in app.subheader)
    assert not any("Đáp án đúng" in item.value for item in app.markdown)


def test_chat_page_resumes_session_and_shows_saved_feedback():
    source = """
from app.features.assessment_ai.tests.test_page import chat_context
from app.features.assessment_ai.pages.overview import render
render(chat_context())
"""
    app = AppTest.from_string(source).run(timeout=20)
    feedback = next(box for box in app.selectbox if box.label == "Đánh giá câu trả lời")
    assert feedback.value == "Hữu ích"
    assert next(box for box in app.checkbox if box.label == "Báo lỗi").value
    next(box for box in app.selectbox
         if box.label == "Phiên hội thoại").set_value(
             {"id": "chat:existing", "lesson_id": "lesson:test",
              "lesson_title": "Rectangle"}).run()
    next(box for box in app.text_input if box.label == "Câu hỏi của bạn").set_value(
        "Hình chữ nhật có tính chất gì?").run()
    next(button for button in app.button if button.label == "Gửi câu hỏi").click().run()
    assert not app.exception
    assert chat_assessment.followup_id == "chat:existing"
