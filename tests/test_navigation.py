import pytest
from app.core.navigation import discover_pages
from streamlit.testing.v1 import AppTest

def test_registry_discovers_all_domains_unique_paths():
    pages = discover_pages()
    assert {p.path for p in pages} == {"identity", "identity-account", "identity-path", "identity-profile", "identity-admin", "learning", "assessment"}
    assert all(callable(p.render) for p in pages)

@pytest.mark.parametrize("path", ["identity", "learning", "assessment"])
def test_feature_pages_render_and_widgets(path):
    source = f"""
from tests.fakes import context
from app.core.navigation import discover_pages
page = next(p for p in discover_pages() if p.path == {path!r})
page.render(context())
"""
    at = AppTest.from_string(source).run(timeout=20)
    assert not at.exception
    assert len(at.title) == 1
    if path == "learning":
        at.slider[0].set_value(8).run()
        assert not at.exception
        assert next(m for m in at.metric if m.label == "Diện tích (S)").value == "24 unit²"
        assert next(m for m in at.metric if m.label == "Chu vi (P)").value == "22 unit"
    if path == "assessment":
        at.text_input[0].set_value("Giải thích hình chữ nhật")
        at.button[0].click().run()
        assert not at.exception
        assert any("MOCK" in item.value for item in at.markdown)

def test_main_home_opens_without_database():
    at = AppTest.from_file("app/main.py").run(timeout=20)
    assert not at.exception
    assert "QuadLearn" in at.title[0].value
