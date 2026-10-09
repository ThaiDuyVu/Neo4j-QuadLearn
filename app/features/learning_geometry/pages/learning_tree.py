import streamlit as st

def render_learning_tree_page(ctx):
    st.title("🗺️ Lộ trình & Cây bài học Hình học")
    grade = st.selectbox("Chọn khối lớp:", [6, 7, 8, 9], index=2)
    content_service = getattr(ctx, "content", None) or getattr(ctx, "content_service", None)
    if not content_service:
        st.info("Mẫu cây bài học (Demo):")
        st.markdown(f"### Lớp {grade}\n- **Chương 1: Tứ giác**\n  - [x] Bài 1: Hình bình hành")
        return
    lessons = content_service.lessons(grade)
    for l in lessons:
        st.write(f"📖 **[{l.id}]** {l.title} (Lớp {l.grade})")