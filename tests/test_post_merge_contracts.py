"""Hồi quy các lỗi ở ranh giới ba domain sau merge."""
from types import SimpleNamespace
import pytest
from streamlit.testing.v1 import AppTest
from app.features.assessment_ai.services.assessment import AssessmentService
from app.features.learning_geometry.repositories.content import ContentRepository
from app.shared.models.dto import CurrentUser


class Identity:
    def __init__(self, user): self.user = user
    def current_user(self): return self.user
    def require_user(self, user_id=None, admin=False):
        u = self.user
        if not u or u.demo or (user_id and user_id != u.id) or (admin and u.role != 'admin'):
            raise ValueError('Unauthorized')
        return u


WRITES = [
    ('submit', ('user:test', 'topic:test', {})),
    ('start_test', ('user:test', 8, 'topic:test')),
    ('save_test_draft', ('user:test', None, {})),
    ('submit_test', ('user:test', 'attempt:test')),
    ('save_essay_review', ('user:test', 'essay:test', 'understood', 0)),
    ('ask_ai', ('user:test', None)),
    ('delete_chat', ('user:test', 'chat:test')),
    ('chat_feedback', ('user:test', 'message:test', 'helpful')),
]


@pytest.mark.parametrize('method,args', WRITES)
@pytest.mark.parametrize('user', [None, CurrentUser('user:test','Demo',8,'student',True),
                                  CurrentUser('user:other','Other',8,'student',False)])
def test_assessment_denies_writes_before_repository(method, args, user):
    service = AssessmentService(object(), identity=Identity(user))
    with pytest.raises(ValueError, match='Unauthorized'):
        getattr(service, method)(*args)


@pytest.mark.parametrize('method,args', [
    ('import_assessment_batch', ('topic:test',8,{})),
    ('import_assessment_xlsx', ('topic:test',8,b'')),
    ('preview_assessment', ('topic:test',)),
])
def test_admin_contract_denies_student_and_unbound_service(method,args):
    for identity in [None, Identity(CurrentUser('user:test','Student',8,'student',False))]:
        with pytest.raises(ValueError):
            getattr(AssessmentService(object(),identity=identity),method)(*args)


def test_assessment_read_cannot_spoof_another_user():
    service = AssessmentService(object(),identity=Identity(CurrentUser('user:test','Student',8,'student',False)))
    with pytest.raises(ValueError,match='quyền đọc'):
        service.attempts('user:other')


class EmptyDatabase:
    def read(self,*args,**kwargs): return []


def test_content_missing_id_returns_none_no_fabricated_lesson():
    repo = ContentRepository(EmptyDatabase())
    assert repo.get_lesson_by_id('missing') is None
    assert repo.list_lessons_for_grade(8) == []
    assert repo.get_prerequisites_recursive('missing') == []


def test_content_database_error_is_not_mock_success():
    class Broken:
        def read(self,*args,**kwargs): raise RuntimeError('database unavailable')
    with pytest.raises(RuntimeError,match='database unavailable'):
        ContentRepository(Broken()).get_lesson_by_id('lesson:test')
    with pytest.raises(ValueError,match='database'):
        ContentRepository()


def test_learning_ai_source_link_selects_exact_grade_and_lesson():
    source = '''
import streamlit as st
from app.core.context import AppContext
from tests.fakes import FakeIdentity,FakeAssessment
from app.shared.models.dto import LessonSummary
from app.features.learning_geometry.pages.overview import render
class Content:
    def lessons(self,grade):
        return [LessonSummary('first','First',grade,'topic:test','First body'),
                LessonSummary('source:7','Linked source',grade,'topic:test','Linked body')]
    def get_lesson(self,id): return self.lessons(7)[1] if id=='source:7' else None
    def prerequisites(self,id): return []
st.query_params['lesson_id']='source:7'
render(AppContext(FakeIdentity(),Content(),FakeAssessment()))
'''
    page = AppTest.from_string(source).run()
    assert not page.exception
    assert page.selectbox[0].value == 7
    assert page.selectbox[1].value.id == 'source:7'
    assert any(x.value == 'Linked body' for x in page.markdown)


def test_son_lesson_completion_uses_context_progress_void_contract():
    source = '''
import streamlit as st
from app.core.context import AppContext
from tests.fakes import FakeIdentity,FakeContent,FakeAssessment
from app.features.learning_geometry.pages.lesson_view import render_lesson_view_page
class Progress:
    def complete_lesson(self,user_id,lesson_id):
        st.session_state['recorded']=(user_id,lesson_id)
        # ProgressWriter returns None on success, raises ValueError on failure.
render_lesson_view_page(AppContext(FakeIdentity(),FakeContent(),FakeAssessment(),progress=Progress()))
'''
    page = AppTest.from_string(source).run()
    assert not page.exception
    page.button[0].click().run()
    assert not page.exception
    assert page.session_state['recorded'] == ('user:test','lesson:test')
    assert any('Đã ghi nhận' in x.value for x in page.success)


@pytest.mark.parametrize('shape', ['Hình chữ nhật','Hình vuông','Hình bình hành','Hình thoi','Hình thang cân'])
def test_geometry_practice_renders_interactive_canvas_for_each_shape(shape):
    source = """
from tests.fakes import context
from app.features.learning_geometry.pages.overview import render
render(context())
"""
    page = AppTest.from_string(source).run()
    page.radio[0].set_value(shape).run()
    assert not page.exception
    assert [tab.label for tab in page.tabs] == ['📖 Lý thuyết','🔗 Kiến thức nền','📐 Thực hành hình học']
    html = page.get('iframe')[0].proto.srcdoc
    assert f'const mode = "{shape}";' in html
    assert 'Hình vẽ tương tác' in html and 'Thông số hình' in html


def test_locked_learning_grade_does_not_render_content_or_board():
    source = """
from tests.fakes import FakeIdentity,FakeAssessment
from app.core.context import AppContext
from app.features.learning_geometry.pages.overview import render
class Content:
    def lessons(self, grade): raise AssertionError('Locked grade must not fetch content')
class Progress:
    def access(self, user_id, grade): return False
render(AppContext(FakeIdentity(),Content(),FakeAssessment(),progress=Progress()))
"""
    page = AppTest.from_string(source).run()
    assert not page.exception
    assert any('Cấp độ đang khóa' in warning.value for warning in page.warning)
    assert not page.get('iframe')


def test_parallelogram_dragging_d_keeps_requested_position():
    from app.features.learning_geometry.models.content import GeometryPoint
    from app.features.learning_geometry.services.geometry_core import GeometryCoreEngine
    pts = {k:GeometryPoint(x=x,y=y) for k,(x,y) in
           {'A':(0,0),'B':(4,0),'C':(5,2),'D':(1,2)}.items()}
    shape = GeometryCoreEngine.update_parallelogram_vertex(pts,'D',2,3)
    assert shape.is_valid
    assert shape.vertices['D'] == GeometryPoint(x=2,y=3)
    assert shape.vertices['C'] == GeometryPoint(x=6,y=3)


def test_import_without_db_does_not_report_success():
    from app.features.learning_geometry.services.content_import import ContentImportService
    from app.features.learning_geometry.services.import_validation import ImportValidationService
    from app.features.learning_geometry.repositories.import_log import ImportLogRepository
    service = ContentImportService(ImportValidationService(),ImportLogRepository())
    payload = {'lessons':[{'id':'lesson:test','grade':8,'topic_id':'topic:test',
                          'title':{'vi':'Title'},'content':{'vi':'Content'},'prerequisites':[]}]}
    with pytest.raises(ValueError,match='database'):
        service.import_lessons(payload,'user:test')
