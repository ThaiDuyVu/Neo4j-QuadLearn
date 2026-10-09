"""Regression: each question retains its own labels across Streamlit reruns."""
from streamlit.testing.v1 import AppTest
from app.core.context import AppContext
from app.features.assessment_ai.tests.test_page import FakeAssessment
from app.features.assessment_ai.models.quiz import Question,Option
from tests.fakes import FakeContent,FakeIdentity


class MultipleQuestions(FakeAssessment):
    def questions(self,grade):
        return super().questions(grade)+[
            Question('question:area','topic:test',8,'apply','single',
                     'Diện tích hình chữ nhật 4 × 3?','12',
                     (Option('option:12','12',True),Option('option:7','7',False)))
        ]


def context():
    return AppContext(FakeIdentity(),FakeContent(),MultipleQuestions())


def test_each_radio_preserves_distinct_labels_and_selected_answers():
    app=AppTest.from_string('''
from tests.test_assessment_multiple_questions import context
from app.features.assessment_ai.pages.overview import render
render(context())
''').run(timeout=20)
    assert not app.exception
    next(item for item in app.button if item.label == 'Bắt đầu luyện tập').click().run()
    first=next(item for item in app.radio if item.label == 'Chọn một đáp án')
    assert first.options==['4','2']
    first.set_value('option:4').run()
    next(item for item in app.button if item.label == 'Câu tiếp →').click().run()
    second=next(item for item in app.radio if item.label == 'Chọn một đáp án')
    assert second.options==['12','7']
    second.set_value('option:12').run()
    next(item for item in app.button if item.label == '← Câu trước').click().run()
    assert not app.exception
    assert next(item for item in app.radio if item.label == 'Chọn một đáp án').value=='option:4'
    next(item for item in app.button if item.label == 'Câu tiếp →').click().run()
    assert next(item for item in app.radio if item.label == 'Chọn một đáp án').value=='option:12'
