"""DOMAIN OWNER: DAT. Lịch sử dành cho người học, không hiển thị ID kỹ thuật."""
from datetime import datetime
import streamlit as st
from .quiz import topic_names


def render(ctx, user, lessons):
    st.subheader("Lịch sử bài làm")
    attempts = ctx.assessment.attempts(user.id)
    if not attempts:
        st.info("Bạn chưa có bài đã nộp. Bắt đầu ở mục Trắc nghiệm để luyện tập.")
        return
    names = topic_names(lessons, [item.topic_id for item in attempts])
    history = ctx.assessment.attempt_history(user.id) if hasattr(ctx.assessment, "attempt_history") else []
    records = {row["id"]: row for row in history}
    for row in history:
        if row.get("topic"):
            names[row["topic_id"]] = row["topic"]
    rows = []
    for index, item in enumerate(attempts, 1):
        timestamp = records.get(item.id, {}).get("finished_at")
        try:
            date = datetime.fromisoformat(timestamp.split("[")[0].replace("Z", "+00:00")).astimezone().strftime("%d/%m/%Y %H:%M") if timestamp else "—"
        except ValueError:
            date = "—"
        rows.append({"Lần làm": index, "Bài học": names[item.topic_id], "Điểm / 10": item.score, "Nộp lúc": date})
    st.caption("Lần làm gần nhất được hiển thị trước. Chọn một lần bên dưới để xem đáp án và lời giải.")
    st.dataframe(rows, hide_index=True, use_container_width=True)
    if hasattr(ctx.assessment, "attempt_detail"):
        chosen = st.selectbox("Chọn lần làm để xem lời giải", range(len(attempts)),
            format_func=lambda i: f"Lần {i+1} · {names[attempts[i].topic_id]} · {attempts[i].score:g}/10")
        for index, detail in enumerate(ctx.assessment.attempt_detail(user.id, attempts[chosen].id), 1):
            with st.expander(f"Câu {index} · {'Đúng' if detail['correct'] else 'Cần xem lại'}", expanded=not detail['correct']):
                st.markdown(detail['question'])
                for label, field in [("Bạn đã chọn", "selected_options"), ("Đáp án đúng", "correct_options")]:
                    options = [item.get('text') or 'Đáp án không còn nội dung' for item in detail.get(field, []) if item.get('id')]
                    st.write(label + ":", ", ".join(options) or "Chưa trả lời")
                st.markdown(detail.get('explanation') or '')
