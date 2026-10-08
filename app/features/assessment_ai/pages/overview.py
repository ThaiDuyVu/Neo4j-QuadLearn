# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
import streamlit as st
from app.shared.components.status import skeleton_notice
from app.core.context import AppContext
from ..models.ai import AIRequest
from ..services.mock_ai import MockAIProvider

def render(ctx: AppContext):
    st.title("Assessment & AI · Đạt")
    skeleton_notice("Đạt")
    user = ctx.identity.current_user()
    if user:
        st.table([{"Attempt": x.id, "Điểm": x.score, "Trạng thái": x.status} for x in ctx.assessment.attempts(user.id)])
    st.subheader("AIProvider demo · mock cố định")
    lessons = ctx.content.lessons(8)
    if lessons:
        lesson = st.selectbox("Ngữ cảnh bài học", lessons, format_func=lambda x: x.title)
        language = st.selectbox("Ngôn ngữ mock", ["vi", "en"])
        question = st.text_input("Câu hỏi thử contract")
        if st.button("Gọi mock"):
            context = tuple(ctx.content.ai_context(lesson.id))
            st.write(MockAIProvider().respond(AIRequest(question, user.grade if user else 8, language, context)))
            st.write("Nguồn ngữ cảnh:", [item.id for item in context])
    st.caption("TODO: quiz, tự luận, lưu câu trả lời, chat history, hạn mức và bộ lọc. Mock không kiểm chứng chất lượng AI.")
