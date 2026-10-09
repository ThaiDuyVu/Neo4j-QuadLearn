"""Lesson view rendering page (SCR-05)."""

import streamlit as st
from app.features.learning_geometry.services.content import ContentService
from app.features.learning_geometry.services.translation import TranslationService


def render_lesson_view_page(app_ctx):
    st.title("📚 Bài học Lý thuyết Hình học")

    content_service: ContentService = getattr(app_ctx, "content", None) or getattr(app_ctx, "content_service", None)
    identity_reader = getattr(app_ctx, "identity", None) or getattr(app_ctx, "identity_reader", None)
    progress_writer = getattr(app_ctx, "progress", None)

    user = identity_reader.current_user() if (identity_reader and hasattr(identity_reader, "current_user")) else None
    user_id = user.id if user else "GUEST_USER"

    lesson_id = st.query_params.get("lesson_id") or st.session_state.get("current_lesson_id", "")
    lesson = content_service.get_lesson(lesson_id) if (content_service and hasattr(content_service, "get_lesson")) else None

    if not lesson and content_service:
        lessons = content_service.lessons(8)
        lesson = lessons[0] if lessons else None

    if not lesson:
        st.error(f"Không tìm thấy bài học với ID: {lesson_id}")
        return

    st.header(lesson.title)
    st.markdown(lesson.content)

    st.subheader("📐 Công thức & Tính chất cốt lõi")
    st.latex(r"S = a \times h_a")
    st.latex(r"P = 2 \times (a + b)")

    st.divider()

    col1, _ = st.columns([1, 1])
    with col1:
        readonly = not user or user.demo or progress_writer is None
        if st.button("Đánh dấu đã học xong", type="primary", disabled=readonly):
            try:
                progress_writer.complete_lesson(user_id, lesson.id)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.success("Đã ghi nhận hoàn thành bài học!")
        if readonly:
            st.info("Đăng nhập tài khoản đã kích hoạt để lưu tiến độ; demo chỉ đọc.")
