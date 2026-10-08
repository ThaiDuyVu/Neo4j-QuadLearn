import streamlit as st
from .common import action
from ..models.errors import IdentityError


def render(ctx):
    st.title("Lộ trình học · Vũ")
    user = ctx.identity.current_user()
    if not user or not ctx.progress:
        st.info("Vào trang Tài khoản để đăng nhập hoặc chọn demo chỉ đọc.")
        return
    grade = st.selectbox("Lớp xem lộ trình", [6, 7, 8, 9], index=user.grade - 6)
    try:
        catalog = ctx.progress.catalog_for(user.id, grade)
    except IdentityError as error:
        st.warning(str(error))
        return
    if not catalog:
        st.info("Chưa có bài published ở cấp độ này.")
        return
    chapters = {}
    for row in catalog:
        chapters.setdefault((row.chapter_id, row.chapter_title), {}).setdefault(
            row.topic_title, []
        ).append(row)
    for (_, chapter), topics in chapters.items():
        with st.expander(chapter, expanded=True):
            for topic, rows in topics.items():
                st.write(f"**{topic}**")
                st.write(
                    [
                        f"{r.lesson.title} · lớp {r.lesson.grade} · {r.cognitive_level}"
                        for r in rows
                    ]
                )
    selected = st.selectbox("Bài học", catalog, format_func=lambda r: r.lesson.title)
    lesson = selected.lesson
    st.write(lesson.content)
    st.subheader("Kiến thức tiên quyết")
    prerequisites = ctx.content.prerequisites(lesson.id)
    st.table([{"Bài nền": p.title, "Lớp": p.grade, "ID": p.id} for p in prerequisites])
    st.caption(
        "ID nguồn dùng liên kết kiến thức; không tự sửa REQUIRES của Sơn. Đây là trang lộ trình, nội dung đầy đủ ở Learning & Geometry."
    )
    if user.demo:
        st.info("Demo chỉ đọc, không lưu tiến độ.")
        return
    if st.button("Bắt đầu / tiếp tục bài này"):
        action(
            lambda: ctx.progress.start_lesson(user.id, lesson.id),
            "Đã lưu bài đang học.",
        )
    if st.button("Tôi đã học xong bài này"):
        action(
            lambda: ctx.progress.complete_lesson(user.id, lesson.id),
            "Đã ghi hoàn thành; bấm lại không nhân đôi.",
        )
