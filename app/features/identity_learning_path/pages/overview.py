# DOMAIN OWNER: VU · identity_learning_path
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
import streamlit as st
from app.shared.components.status import skeleton_notice
from app.core.context import AppContext

def render(ctx: AppContext):
    st.title("Identity & Learning Path · Vũ")
    skeleton_notice("Vũ")
    user = ctx.identity.current_user()
    if user is None:
        st.warning("Chưa có tài khoản demo. Chạy python -m scripts.db init.")
        return
    st.write(f"Học sinh demo: {user.name} · Lớp {user.grade} · {user.role}")
    grade = st.selectbox("Xem lộ trình mẫu theo lớp (chưa kiểm soát mở khóa)", [6, 7, 8, 9], index=user.grade-6)
    lessons = ctx.content.lessons(grade)
    st.table([{"Bài": item.title, "ID": item.id} for item in lessons])
    st.subheader("Lịch sử từ contract AssessmentReader")
    st.table([{"Lần làm": a.id, "Chủ đề": a.topic_id, "Điểm": a.score} for a in ctx.assessment.attempts(user.id)])
    st.caption("TODO: AUTH, hồ sơ, progress thực tế, tiếp tục học và mở khóa theo ngưỡng.")
