# DOMAIN OWNER: SON · learning_geometry
# Page chỉ tổ chức các khu vực học tập; bảng vẽ ở interactive_board.py.
import streamlit as st
from app.core.context import AppContext
from .interactive_board import render_geometry_board

SHAPES = ["Hình chữ nhật", "Hình vuông", "Hình bình hành", "Hình thoi", "Hình thang cân"]


def _title(lesson):
    return getattr(lesson, "title", getattr(lesson, "title_vi", "Bài học"))


def render(ctx: AppContext):
    st.title("Nội dung & Hình học")
    st.caption("Chọn bài học, tìm hiểu kiến thức và thực hành với hình vẽ tương tác.")

    # Link bài nguồn từ trợ lý vẫn phải chọn đúng bài và cấp độ.
    requested = st.query_params.get("lesson_id")
    requested_lesson = ctx.content.get_lesson(requested) if requested and hasattr(ctx.content, "get_lesson") else None
    if requested and requested_lesson is None:
        st.warning("Bài nguồn không tồn tại hoặc chưa xuất bản.")
    default_grade = requested_lesson.grade if requested_lesson else 8
    with st.container(border=True):
        st.subheader("Chọn nội dung học")
        grade_col, lesson_col = st.columns([1, 3])
        with grade_col:
            grade = st.selectbox("Chọn khối lớp:", [6, 7, 8, 9], index=default_grade - 6)
        user = ctx.identity.current_user()
        if user and ctx.progress and not ctx.progress.access(user.id, grade):
            st.warning("Cấp độ đang khóa. Vào Hồ sơ và cấp độ để xem điều kiện hoặc xác nhận học vượt.")
            return
        lessons = ctx.content.lessons(grade)
        lesson = None
        with lesson_col:
            if lessons:
                default_index = next((i for i, item in enumerate(lessons) if item.id == requested), 0)
                lesson = st.selectbox("Chọn bài học lý thuyết:", lessons, index=default_index, format_func=_title)
            else:
                st.info(f"Chưa có bài học đã xuất bản cho Lớp {grade}.")

    theory, foundations, practice = st.tabs(["📖 Lý thuyết", "🔗 Kiến thức nền", "📐 Thực hành hình học"])
    with theory:
        with st.container(border=True):
            if lesson:
                st.subheader(_title(lesson))
                st.caption(f"Lớp {grade} · Nội dung bài học")
                content = getattr(lesson, "content", getattr(lesson, "content_vi", "Nội dung đang cập nhật..."))
                # Seed có tiêu đề Markdown; page đã hiển thị tiêu đề trong khu vực này.
                heading = f"## {_title(lesson)}"
                if content.splitlines() and content.splitlines()[0].strip() == heading:
                    content = "\n".join(content.splitlines()[1:]).lstrip()
                st.markdown(content)
            else:
                st.info("Chọn lớp có bài học để xem lý thuyết.")
        st.caption("Muốn ghi nhận đã học xong hoặc tiếp tục bài đang học, mở Lộ trình học trong thanh bên.")
    with foundations:
        with st.container(border=True):
            st.subheader("Kiến thức cần ôn trước")
            if lesson:
                st.caption(f"Các bài nền liên quan đến {_title(lesson)}.")
                prerequisites = ctx.content.prerequisites(lesson.id)
                if prerequisites:
                    st.dataframe([
                        {"Bài học": _title(item), "Lớp": item.grade}
                        for item in prerequisites
                    ], hide_index=True, use_container_width=True)
                else:
                    st.info("Bài học này chưa có bài tiên quyết được liên kết.")
            else:
                st.info("Chọn bài học để xem kiến thức nền.")
    with practice:
        with st.container(border=True):
            st.subheader("Khám phá hình tứ giác")
            st.caption("Chọn hình ban đầu, chỉnh thông số hoặc kéo các đỉnh để quan sát.")
            shape_type = st.radio("Chọn hình tứ giác ban đầu:", SHAPES, horizontal=True)
        render_geometry_board(shape_type)


render_overview_page = render
