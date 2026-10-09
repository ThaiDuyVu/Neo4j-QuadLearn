# DOMAIN OWNER: DAT · assessment_ai
# Giao diện hỗ trợ học; truy cập domain khác chỉ qua AppContext/contracts.
import streamlit as st
from app.core.context import AppContext


def render(ctx, user, readonly):
    from ..models.essay import reveal_hint

    st.subheader("Bài tự luận")
    essays = ctx.assessment.essays(user.grade)
    if essays:
        essay = st.selectbox("Chọn đề", essays, format_func=lambda e: e.prompt)
        reviews = [item for item in ctx.assessment.essay_reviews(user.id)
                   if item["essay_id"] == essay.id]
        if reviews:
            latest = reviews[0]
            st.caption(f"Lần tự đánh giá gần nhất: {latest['rating']} · "
                       f"{latest['hints_used']} gợi ý")
        st.write(essay.prompt)
        st.write("Giả thiết:", essay.assumptions)
        st.write("Kết luận:", essay.conclusion)
        if essay.image_url:
            st.image(essay.image_url)
        key = f"essay:hints:{user.id}:{essay.id}"
        revealed = st.session_state.get(key, 0)
        if st.button("Mở gợi ý tiếp", disabled=revealed >= len(essay.hints)):
            revealed += 1
            st.session_state[key] = revealed
        for hint in reveal_hint(essay, revealed):
            st.markdown(f"**Gợi ý {hint.order}:** {hint.text}")
            if hint.image_url:
                st.image(hint.image_url)
        answer_text = st.text_area(
            "Bài làm của em (văn bản hoặc công thức LaTeX)",
            key=f"essay:answer:{user.id}:{essay.id}", max_chars=10000)
        if st.button("Xem lời giải đầy đủ"):
            st.markdown("**Bài làm của em**")
            st.markdown(answer_text or "_Chưa nhập bài làm_")
            st.markdown("**Lời giải mẫu**")
            st.markdown(essay.solution)
        rating = st.radio("Tự đánh giá", ["Chưa chọn", "Đã hiểu", "Cần xem lại"],
                          key=f"essay:review:{user.id}:{essay.id}")
        if st.button("Lưu tự đánh giá", disabled=readonly):
            if rating == "Chưa chọn":
                st.error("Chọn mức tự đánh giá trước khi lưu.")
            else:
                value = "understood" if rating == "Đã hiểu" else "review_again"
                try:
                    ctx.assessment.save_essay_review(
                        user.id, essay.id, value, revealed, answer_text)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.success("Đã lưu tự đánh giá và số gợi ý đã dùng.")
    else:
        st.info("Chưa có bài tự luận cho lớp của bạn.")
