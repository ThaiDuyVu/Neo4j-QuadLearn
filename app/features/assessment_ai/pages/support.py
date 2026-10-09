# DOMAIN OWNER: DAT · assessment_ai
# Giao diện hỗ trợ học; truy cập domain khác chỉ qua AppContext/contracts.
import streamlit as st
from app.core.context import AppContext
from urllib.parse import quote
from ..models.ai import AIRequest
from ..services.mock_ai import MockAIProvider
from ..services.ai_safety import ScreenedAIProvider

def _source_links(source_ids) -> str:
    links = [f"[Mở nguồn {index}](/learning?lesson_id={quote(source_id, safe='')})"
             for index, source_id in enumerate(source_ids, 1) if source_id]
    return " · ".join(links)

def render_chat(ctx, user, readonly, drafts, lessons):
    st.subheader("Trợ lý học tập · bản mô phỏng")
    language = "vi"
    if lessons:
        lesson = st.selectbox("Ngữ cảnh bài học", lessons, format_func=lambda x: x.title)
        language = st.selectbox("Ngôn ngữ trả lời", ["vi", "en"], format_func=lambda value: "Tiếng Việt" if value == "vi" else "English")
        question = st.text_input("Câu hỏi của bạn")
        resume_session = None
        if user and not drafts and hasattr(ctx.assessment, "chat_sessions"):
            available = [item for item in ctx.assessment.chat_sessions(user.id)
                         if item.get("lesson_id") == lesson.id]
            resume_session = st.selectbox(
                "Phiên hội thoại", [None] + available,
                format_func=lambda item: "Phiên mới" if item is None else f"Hội thoại {available.index(item) + 1}")
        if user and hasattr(ctx.assessment, "remaining_ai_questions"):
            st.caption(f"Lượt hỏi còn lại hôm nay: {ctx.assessment.remaining_ai_questions(user.id)}")
        if st.button("Gửi câu hỏi", disabled=bool(drafts) or readonly):
            context = tuple(ctx.content.ai_context(lesson.id))
            try:
                request = AIRequest(question, user.grade if user else 8, language, context,
                                    lesson.id)
                if user and hasattr(ctx.assessment, "ask_ai"):
                    response = ctx.assessment.ask_ai(
                        user.id, request,
                        session_id=resume_session["id"] if resume_session else None)
                    reply = response.text
                else:
                    reply = ScreenedAIProvider(MockAIProvider()).respond(request)
            except ValueError as exc:
                st.error(str(exc))
            except TimeoutError as exc:
                st.error(str(exc))
            else:
                st.markdown(reply)
                source_links = _source_links(item.id for item in context)
                if source_links:
                    st.markdown("Nguồn ngữ cảnh: " + source_links)
    st.caption("Trợ lý hiện dùng câu trả lời mô phỏng, chưa kết nối mô hình AI trực tuyến.")
    if user and not drafts and hasattr(ctx.assessment, "chat_sessions"):
        sessions = ctx.assessment.chat_sessions(user.id)
        if sessions:
            session = st.selectbox("Lịch sử chat", sessions,
                                   format_func=lambda s: f"{s.get('lesson_title') or 'Hội thoại'} · lần {sessions.index(s) + 1}")
            for message in ctx.assessment.chat_messages(user.id, session["id"]):
                st.markdown(f"**{'Trợ lý' if message['role'] == 'assistant' else 'Bạn'}**: {message['content']}")
                if message["role"] == "assistant":
                    source_links = _source_links(message.get("sources") or [])
                    if source_links:
                        st.markdown("Nguồn: " + source_links)
                    rating = st.selectbox("Đánh giá câu trả lời",
                                          ["Chưa chọn", "Hữu ích", "Không hữu ích"],
                                          index={"helpful": 1, "unhelpful": 2}.get(
                                              message.get("feedback"), 0),
                                          key=f"feedback:{message['id']}")
                    report = st.checkbox("Báo lỗi", value=bool(message.get("report")),
                                         key=f"report:{message['id']}")
                    if st.button("Lưu đánh giá", key=f"save-feedback:{message['id']}", disabled=readonly):
                        if rating == "Chưa chọn":
                            st.error("Chọn mức đánh giá trước khi lưu.")
                        else:
                            ctx.assessment.chat_feedback(
                                user.id, message["id"],
                                "helpful" if rating == "Hữu ích" else "unhelpful", report)
                            st.success("Đã lưu đánh giá.")
            if st.button("Xóa phiên chat", disabled=readonly):
                ctx.assessment.delete_chat(user.id, session["id"])
                st.rerun()
