# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
import os
from .scoring import score

class AssessmentService:
    def __init__(self, repository):
        self.repository = repository
        from .quiz import QuizService
        from .essay import EssayService
        from .chat import ChatService
        from .import_assessment import AssessmentImportService
        from .placement import PlacementService
        from .mock_ai import MockAIProvider
        self.quiz = QuizService(repository)
        self.essay = EssayService(repository)
        self.chat = ChatService(
            repository, MockAIProvider(),
            daily_limit=int(os.getenv("QUADLEARN_AI_DAILY_LIMIT", "10")),
        )
        self.importer = AssessmentImportService(repository)
        self.placement = PlacementService(repository)

    def import_assessment_batch(self, topic_id: str, grade: int, payload: dict):
        """Domain entrypoint for Sơn's authorized Admin import workflow."""
        return self.importer.import_batch(topic_id, grade, payload)

    def import_assessment_xlsx(self, topic_id: str, grade: int, data: bytes):
        return self.importer.import_xlsx(topic_id, grade, data)

    def preview_assessment(self, topic_id: str):
        """Includes correct answers; caller must enforce Admin authorization."""
        return self.importer.preview(topic_id)

    def placement_form(self, grades: tuple[int, ...] = (6, 7, 8, 9),
                       per_grade: int = 3):
        return self.placement.form(grades, per_grade)

    def grade_placement(self, question_ids: tuple[str, ...], selections: dict):
        return self.placement.grade(question_ids, selections)

    def attempts(self, user_id: str):
        return self.repository.attempts(user_id)

    def attempt_history(self, user_id: str):
        return self.repository.attempt_history(user_id)

    def questions(self, grade: int, topic_id: str | None = None,
                  difficulty: str | None = None):
        return self.quiz.questions(grade, topic_id, difficulty)

    def submit(self, user_id: str, topic_id: str, selections: dict[str, tuple[str, ...]]):
        return self.quiz.submit(user_id, topic_id, selections)

    def start_test(self, user_id: str, grade: int, topic_id: str,
                   duration_seconds: int = 900):
        return self.quiz.start_test(user_id, grade, topic_id, duration_seconds)

    def test_drafts(self, user_id: str):
        return self.repository.test_drafts(user_id)

    def resume_test(self, user_id: str, attempt_id: str):
        return self.quiz.resume_test(user_id, attempt_id)

    def save_test_draft(self, user_id: str, session, selections):
        return self.quiz.save_test_draft(user_id, session, selections)

    def submit_test(self, user_id: str, attempt_id: str):
        return self.quiz.submit_test(user_id, attempt_id)

    def test_seconds_left(self, session):
        return self.quiz.seconds_left(session)

    def attempt_detail(self, user_id: str, attempt_id: str):
        return self.repository.attempt_detail(user_id, attempt_id)

    def essays(self, grade: int, topic_id: str | None = None):
        return self.repository.essays(grade, topic_id)

    def save_essay_review(self, user_id: str, essay_id: str, rating: str,
                          hints_used: int, answer_text: str = ""):
        return self.essay.save_review(user_id, essay_id, rating, hints_used, answer_text)

    def essay_reviews(self, user_id: str):
        if not user_id:
            raise ValueError("Thiếu người học")
        return self.repository.essay_reviews(user_id)

    def remaining_ai_questions(self, user_id: str) -> int:
        return self.chat.remaining(user_id)

    def ask_ai(self, user_id: str, request, session_id: str | None = None):
        return self.chat.ask(user_id, request, session_id=session_id)

    def chat_sessions(self, user_id: str):
        return self.chat.sessions(user_id)

    def chat_messages(self, user_id: str, session_id: str):
        return self.chat.messages(user_id, session_id)

    def delete_chat(self, user_id: str, session_id: str):
        return self.chat.delete_session(user_id, session_id)

    def chat_feedback(self, user_id: str, message_id: str, rating: str,
                      report: bool = False):
        return self.chat.feedback(user_id, message_id, rating, report)
