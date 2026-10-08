# DOMAIN OWNER: SON · learning_geometry
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
import streamlit as st
import streamlit.components.v1 as components
from app.shared.components.status import skeleton_notice
from app.core.context import AppContext
from ..services.geometry import rectangle

def render(ctx: AppContext):
    st.title("Learning & Geometry · Sơn")
    skeleton_notice("Sơn")
    grade = st.selectbox("Lớp", [6, 7, 8, 9], index=2)
    lessons = ctx.content.lessons(grade)
    if lessons:
        lesson = st.selectbox("Bài lý thuyết demo", lessons, format_func=lambda x: x.title)
        st.write(lesson.content)
        st.write("Tiên quyết nhiều cấp:")
        st.table([{"Bài": x.title, "Lớp": x.grade} for x in ctx.content.prerequisites(lesson.id)])
    else:
        st.info("Chưa có nội dung demo ở lớp này.")
    st.subheader("Vị trí tích hợp hình động · hình chữ nhật demo")
    st.latex(r"S = a \times b")
    width = st.slider("Chiều dài", 1, 10, 4)
    height = st.slider("Chiều rộng", 1, 10, 3)
    _, area, perimeter = rectangle(width, height)
    components.html(f'<svg viewBox="0 0 500 250" role="img" aria-label="Hình chữ nhật minh họa"><rect x="20" y="20" width="{width*20}" height="{height*20}" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/></svg>', height=250)
    st.write(f"Diện tích: {area}; chu vi: {perimeter} (đơn vị demo).")
    st.caption("TODO: kéo đỉnh, công cụ dựng hình, import JSON/Excel và giao diện Việt/Anh đầy đủ.")
