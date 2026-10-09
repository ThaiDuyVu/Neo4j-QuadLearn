from streamlit.testing.v1 import AppTest
import pytest

SOURCE = """
import streamlit as st
from app.core.context import AppContext
from app.core.navigation import discover_pages
from app.features.identity_learning_path.tests.fakes import MemoryIdentityRepository,MemoryProgressRepository,Clock,Content,Assessment
from app.features.identity_learning_path.services.auth import AuthService
from app.features.identity_learning_path.services.identity import IdentityService
from app.features.identity_learning_path.services.learning_path import LearningPathService
if 'test_repo' not in st.session_state:
    st.session_state['test_repo']=MemoryIdentityRepository()
    st.session_state['test_clock']=Clock()
    st.session_state['test_progress']=MemoryProgressRepository()
repo=st.session_state['test_repo'];clock=st.session_state['test_clock']
identity=IdentityService(repo,st.session_state,clock=clock)
content=Content();assessment=Assessment()
ctx=AppContext(identity,content,assessment,AuthService(repo,clock=clock),LearningPathService(st.session_state['test_progress'],identity,content,assessment,content))
page=next(p for p in discover_pages() if p.path==PATH)
page.render(ctx)
"""


def element(items, label):
    return next(item for item in items if item.label == label)


@pytest.mark.parametrize(
    "path", ["identity-account", "identity-path", "identity-profile", "identity-admin"]
)
def test_new_pages_render_for_guest(path):
    at = AppTest.from_string(SOURCE.replace("PATH", repr(path))).run()
    assert not at.exception and len(at.title) == 1


def test_registration_activation_login_forms_end_to_end_without_db():
    at = AppTest.from_string(SOURCE.replace("PATH", repr("identity-account"))).run()
    for label, value in [
        ("Họ tên", "Student test"),
        ("Email đăng ký", "student@example.invalid"),
        ("Mật khẩu mới", "TestPass123"),
        ("Nhập lại mật khẩu", "TestPass123"),
        ("Email người giám hộ (bắt buộc nếu dưới 16 tuổi)", "guardian@example.invalid"),
    ]:
        element(at.text_input, label).set_value(value)
    element(at.button, "Tạo tài khoản").click().run()
    assert not at.exception
    tokens = at.session_state["vu_dev_delivery"]
    for kind in ["verify", "guardian"]:
        element(at.selectbox, "Loại xác thực").set_value(kind)
        element(at.text_input, "Mã kích hoạt").set_value(tokens[kind])
        element(at.button, "Kích hoạt").click().run()
        assert not at.exception
    element(at.text_input, "Email đăng nhập").set_value("student@example.invalid")
    element(at.text_input, "Mật khẩu đăng nhập").set_value("TestPass123")
    element(at.button, "Đăng nhập").click().run()
    assert not at.exception
    assert at.session_state["vu_session"]
    assert any("Đang dùng:" in item.value for item in at.markdown)
    element(at.button, "Đăng xuất").click().run()
    assert not at.exception
    assert "vu_session" not in at.session_state.filtered_state
