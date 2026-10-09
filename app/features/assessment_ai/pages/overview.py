# DOMAIN OWNER: DAT · assessment_ai
# Giao diện hỗ trợ học; truy cập domain khác chỉ qua AppContext/contracts.
import streamlit as st
from app.core.context import AppContext
from .support import render_chat, _source_links  # Giữ helper link tương thích.
from .essay import render as render_essay
from .quiz import render as render_quiz
from .history import render as render_history


def render(ctx: AppContext):
    st.title("Bài tập và trợ lý học tập")
    st.caption("Chọn hoạt động phù hợp: luyện tập, tự luận, hỏi bài hoặc xem kết quả đã làm.")
    user = ctx.identity.current_user()
    readonly = bool(user and user.demo)
    lessons = ctx.content.lessons(user.grade if user else 8)
    drafts = ctx.assessment.test_drafts(user.id) if user and hasattr(ctx.assessment, "test_drafts") else []
    if readonly:
        st.info("Bạn đang xem thử. Đăng nhập tài khoản học sinh để lưu bài làm và tiến độ.")
    if drafts:
        st.warning("Bạn có bài kiểm tra đang làm. Hãy tiếp tục và nộp bài trước khi chuyển hoạt động.")
        render_quiz(ctx, user, readonly, drafts, lessons)
        return
    section = st.radio("Bạn muốn làm gì?", ["Trắc nghiệm", "Tự luận", "Trợ lý học tập", "Lịch sử"],
                       horizontal=True, key=f"assessment:section:{user.id if user else 'guest'}")
    if section == "Trợ lý học tập":
        render_chat(ctx, user, readonly, drafts, lessons)
        return
    if not user:
        st.info("Đăng nhập để làm bài và xem lịch sử học tập của bạn.")
        st.markdown("[Đến trang đăng nhập](/identity-account)")
        return
    if section == "Trắc nghiệm":
        render_quiz(ctx, user, readonly, drafts, lessons)
    elif section == "Tự luận":
        render_essay(ctx, user, readonly)
    else:
        render_history(ctx, user, lessons)
