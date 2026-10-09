# DOMAIN OWNER: VU. Dashboard chỉ gọi contracts, không ghi dữ liệu assessment/content.
import streamlit as st
from .common import action


def render(ctx):
    st.title("Tiến độ học tập")
    user = ctx.identity.current_user()
    if user is None:
        st.info("Vào Tài khoản để đăng nhập hoặc bật demo chỉ đọc.")
        return
    st.write(
        f"{user.name} · Lớp {user.grade} · {user.role}"
        + (" · DEMO chỉ đọc" if user.demo else "")
    )
    if ctx.progress:
        levels = ctx.progress.levels(user.id)
        st.table(
            [
                {
                    "Lớp": x.grade,
                    "Bài đã xong": x.completed,
                    "Bài đã xuất bản": x.total,
                    "% hoàn thành": round(x.completion, 2),
                    "Điểm TB": x.average_score,
                    "Đã mở": x.unlocked,
                }
                for x in levels
            ]
        )
        resume = ctx.progress.resume_lesson(user.id)
        if resume:
            st.info(
                f"Tiếp tục: {resume.title} ({resume.id}). Vào Lộ trình học để mở bài này."
            )
        if not user.demo and st.button("Tính lại và lưu tiến độ"):
            action(lambda: ctx.progress.refresh(user.id))
        grade = st.selectbox(
            "Chi tiết chương/chủ đề", [6, 7, 8, 9], index=user.grade - 6
        )
        if ctx.progress.access(user.id, grade):
            st.table(ctx.progress.breakdown(user.id, grade))
        else:
            st.warning(
                "Lớp này đang khóa. Vào Hồ sơ và cấp độ để xem điều kiện/học vượt."
            )
        st.subheader("Điểm mạnh/yếu theo chủ đề")
        st.table(ctx.progress.topic_statistics(user.id))
        st.subheader("Bài nền nên ôn")
        st.table(
            [
                {"Bài": x.title, "Lớp": x.grade, "ID": x.id}
                for x in ctx.progress.review_lessons(user.id)
            ]
        )
    else:
        st.table(
            [{"Bài": x.title, "ID": x.id} for x in ctx.content.lessons(user.grade)]
        )
    st.subheader("Lịch sử bài làm")
    st.table(
        [
            {
                "Lần làm": a.id,
                "Chủ đề": a.topic_id,
                "Điểm": a.score,
                "Trạng thái": a.status,
            }
            for a in ctx.assessment.attempts(user.id)
        ]
    )
    st.caption(
        "Xem chi tiết và đáp án trong Bài tập và trợ lý học tập."
    )
