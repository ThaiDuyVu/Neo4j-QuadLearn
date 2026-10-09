"""Round trips against the opted-in local seeded Neo4j demo database."""

import os

import pytest
from streamlit.testing.v1 import AppTest

from app.core.config import Settings
from app.core.context import AppContext
from app.core.database import Database
from app.features.assessment_ai.repositories.assessment import AssessmentRepository
from app.features.assessment_ai.services.assessment import AssessmentService
from app.features.assessment_ai.services.essay import EssayService
from app.features.assessment_ai.services.quiz import QuizService
from app.shared.models.dto import CurrentUser
from tests.fakes import FakeContent


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.getenv("QUADLEARN_INTEGRATION") != "1",
                       reason="Requires explicit local seeded Neo4j demo opt-in"),
]


_integration_context = None


def integration_context():
    return _integration_context


class DemoIdentity:
    def current_user(self):
        return CurrentUser("user:demo-student", "Demo", 8, "student")


def test_practice_timed_test_and_essay_review_round_trip():
    global _integration_context
    db = Database(Settings.load())
    attempt_ids = []
    review_ids = []
    try:
        db.verify()
        repository = AssessmentRepository(db)
        quiz = QuizService(repository)
        user_id = "user:demo-student"
        topic_id = "topic:8:rectangle"
        question = next(q for q in quiz.questions(8, topic_id)
                        if q.id == "question:8:rectangle:1")
        correct = next(option.id for option in question.options if option.correct)

        practice = quiz.submit(user_id, topic_id, {question.id: (correct,)})
        attempt_ids.append(practice.id)
        assert practice.score == 10
        assert repository.attempt_detail(user_id, practice.id)[0]["selected_ids"] == [correct]

        test = quiz.start_test(user_id, 8, topic_id, 300)
        attempt_ids.append(test.id)
        assert not hasattr(test.questions[0].options[0], "correct")
        quiz.save_test_draft(user_id, test, {question.id: (correct,)})
        assert quiz.resume_test(user_id, test.id).selections[question.id] == (correct,)
        _integration_context = AppContext(DemoIdentity(), FakeContent(),
                                          AssessmentService(repository))
        page = AppTest.from_string("""
from app.features.assessment_ai.tests.test_integration_assessment import integration_context
from app.features.assessment_ai.pages.overview import render
render(integration_context())
""").run(timeout=20)
        assert not page.exception
        assert next(button for button in page.button
                    if button.label == "Kiểm tra câu").disabled
        assert not any(box.label == "Xem lại lần làm" for box in page.selectbox)
        assert not any("Đáp án đúng" in item.value for item in page.markdown)
        next(button for button in page.button
             if button.label == "Nộp bài kiểm tra").click().run(timeout=20)
        assert not page.exception
        assert any("Điểm kiểm tra: 10.0/10" in item.value for item in page.success)
        assert repository.attempts(user_id)[0].score == 10
        assert all(item["id"] != test.id for item in repository.test_drafts(user_id))

        essay = repository.essays(8, topic_id)[0]
        review_id = EssayService(repository).save_review(
            user_id, essay.id, "understood", 1, "$S=4\\times3=12$")
        review_ids.append(review_id)
        assert next(row for row in repository.essay_reviews(user_id)
                    if row["id"] == review_id)["answer_text"] == "$S=4\\times3=12$"
    finally:
        try:
            with db.driver.session(database=db.database) as session:
                for attempt_id in attempt_ids:
                    session.run("""
                        MATCH (a:Attempt {id:$id})-[:HAS_ANSWER]->(x:AttemptAnswer)
                        DETACH DELETE x
                    """, id=attempt_id).consume()
                    session.run("MATCH (a:Attempt {id:$id}) DETACH DELETE a",
                                id=attempt_id).consume()
                for review_id in review_ids:
                    session.run("MATCH (r:EssayReview {id:$id}) DETACH DELETE r",
                                id=review_id).consume()
        finally:
            _integration_context = None
            db.close()
