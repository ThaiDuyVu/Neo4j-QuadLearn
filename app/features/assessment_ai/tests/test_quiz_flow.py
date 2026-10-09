"""Verify user navigation, preserved answers and submission state transitions."""
from streamlit.testing.v1 import AppTest
from app.core.context import AppContext
from app.features.assessment_ai.tests.test_page import FakeAssessment
from app.features.assessment_ai.models.quiz import Question, Option, AttemptResult
from app.features.assessment_ai.services.quiz import grade_answer
from tests.fakes import FakeContent, FakeIdentity


class FlowAssessment(FakeAssessment):
    submits = 0

    def questions(self, grade):
        return super().questions(grade) + [
            Question('question:2', 'topic:test', 8, 'recognize', 'single',
                     'Hình chữ nhật có mấy đường chéo?', 'Có hai đường chéo.',
                     (Option('option:two', '2', True), Option('option:four', '4', False)))]

    def submit(self, user_id, topic_id, selections):
        self.submits += 1
        answers = tuple(grade_answer(q, selections[q.id]) for q in self.questions(8))
        return AttemptResult('attempt:flow', topic_id, sum(a.correct for a in answers)*5,
                             answers, '', '')


assessment = FlowAssessment()

def context(): return AppContext(FakeIdentity(), FakeContent(), assessment)

def page():
    return AppTest.from_string('''
from app.features.assessment_ai.tests.test_quiz_flow import context
from app.features.assessment_ai.pages.overview import render
render(context())
''').run()

def button(app, label): return next(item for item in app.button if item.label == label)
def answer(app): return next(item for item in app.radio if item.label == 'Chọn một đáp án')


def test_practice_keeps_answers_when_switching_questions_and_submits_once():
    assessment.submits = 0
    app = page()
    assert not app.exception
    assert app.selectbox[0].format_func('topic:test') == 'Rectangle'
    button(app, 'Bắt đầu luyện tập').click().run()
    assert answer(app).value is None
    answer(app).set_value('option:4').run()
    button(app, 'Câu tiếp →').click().run()
    assert answer(app).value is None
    answer(app).set_value('option:four').run()
    button(app, '← Câu trước').click().run()
    assert answer(app).value == 'option:4'
    button(app, 'Nộp bài luyện tập').click().run()
    assert not app.exception
    assert assessment.submits == 1
    assert [metric.value for metric in app.metric] == ['5/10', '1/2']
    app.run()
    assert not any(item.label == 'Nộp bài luyện tập' for item in app.button)
    app.run()
    assert assessment.submits == 1
    button(app, 'Chọn bài khác / Làm lại').click().run()
    button(app, 'Bắt đầu luyện tập').click().run()
    assert answer(app).value is None


def test_unanswered_practice_is_not_saved_and_sections_are_separate():
    assessment.submits = 0
    app = page()
    button(app, 'Bắt đầu luyện tập').click().run()
    button(app, 'Nộp bài luyện tập').click().run()
    assert not app.exception
    assert assessment.submits == 0
    assert any('chưa trả lời' in item.value for item in app.warning)
    assert not app.text_input and not app.text_area

from app.features.assessment_ai.tests.test_page import DraftAssessment

class TimedFlow(DraftAssessment):
    submitted = False
    saved = None
    remaining = 200

    def test_drafts(self, user_id):
        return [] if self.submitted else super().test_drafts(user_id)

    def test_seconds_left(self, session): return self.remaining

    def save_test_draft(self, user_id, session, selections): self.saved = selections

    def submit_test(self, user_id, attempt_id):
        self.submitted = True
        original = self.questions(8)[0]
        choices = (self.saved or {}).get(original.id) or ('option:4',)
        result = grade_answer(original, choices)
        return AttemptResult(attempt_id, 'topic:test', 10 if result.correct else 0,
                             (result,), '', '')

timed = TimedFlow()
def timed_context(): return AppContext(FakeIdentity(), FakeContent(), timed)
def timed_page():
    return AppTest.from_string('''
from app.features.assessment_ai.tests.test_quiz_flow import timed_context
from app.features.assessment_ai.pages.overview import render
render(timed_context())
''').run()


def test_timed_submit_saves_current_form_answers_before_grading():
    timed.submitted, timed.saved, timed.remaining = False, None, 200
    app = timed_page()
    assert not any(item.label == 'Bạn muốn làm gì?' for item in app.radio)
    answer(app).set_value('option:2')
    button(app, 'Nộp bài kiểm tra').click().run()
    assert not app.exception
    assert timed.saved == {'question:1': ('option:2',)}
    assert app.metric[0].value == '0/10'


def test_expired_test_disables_edits_and_does_not_overwrite_saved_answers():
    timed.submitted, timed.saved, timed.remaining = False, None, 0
    app = timed_page()
    assert answer(app).disabled
    assert button(app, 'Lưu nháp').disabled
    button(app, 'Nộp bài kiểm tra').click().run()
    assert not app.exception
    assert timed.saved is None
