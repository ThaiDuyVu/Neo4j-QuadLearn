# DOMAIN OWNER: DAT · assessment_ai
# Bổ sung chức năng trong domain này; dữ liệu domain khác đi qua shared contracts.
# TODO: xem checklist và FR-ID trong README.md của feature trước khi mở rộng.
import streamlit as st
from urllib.parse import quote
from app.core.context import AppContext
from ..models.ai import AIRequest
from ..services.mock_ai import MockAIProvider
from ..services.ai_safety import ScreenedAIProvider


def _source_links(source_ids) -> str:
    links = [f"[Mở nguồn {index}](/learning?lesson_id={quote(source_id, safe='')})"
             for index, source_id in enumerate(source_ids, 1) if source_id]
    return " · ".join(links)

def render(ctx: AppContext):
    st.title("Assessment & AI · Đạt")
    st.caption("Trắc nghiệm, tự luận và trợ lý mock cho đồ án hiện tại.")
    user = ctx.identity.current_user()
    readonly = bool(user and user.demo)
    if readonly:
        st.info("Demo chỉ đọc: không lưu bài làm, chat, đánh giá hoặc thay đổi dữ liệu.")
    drafts = (ctx.assessment.test_drafts(user.id)
              if user and hasattr(ctx.assessment, "test_drafts") else [])
    if user:
        if hasattr(ctx.assessment, "attempt_history"):
            st.table(ctx.assessment.attempt_history(user.id))
        else:
            st.table([{"Attempt": x.id, "Điểm": x.score, "Trạng thái": x.status}
                      for x in ctx.assessment.attempts(user.id)])
    st.subheader("AIProvider demo · mock cố định")
    lessons = ctx.content.lessons(user.grade if user else 8)
    language = "vi"
    if lessons:
        lesson = st.selectbox("Ngữ cảnh bài học", lessons, format_func=lambda x: x.title)
        language = st.selectbox("Ngôn ngữ mock", ["vi", "en"])
        question = st.text_input("Câu hỏi thử contract")
        resume_session = None
        if user and not drafts and hasattr(ctx.assessment, "chat_sessions"):
            available = [item for item in ctx.assessment.chat_sessions(user.id)
                         if item.get("lesson_id") == lesson.id]
            resume_session = st.selectbox(
                "Phiên hội thoại", [None] + available,
                format_func=lambda item: "Phiên mới" if item is None else item["id"])
        if user and hasattr(ctx.assessment, "remaining_ai_questions"):
            st.caption(f"Lượt hỏi mock còn lại hôm nay: {ctx.assessment.remaining_ai_questions(user.id)}")
        if st.button("Gọi mock", disabled=bool(drafts) or readonly):
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
    st.caption("AI hiện là mock cố định. Bộ lọc quy tắc chỉ là lớp bảo vệ ban đầu; chưa có LLM thật.")
    if user and not drafts and hasattr(ctx.assessment, "chat_sessions"):
        sessions = ctx.assessment.chat_sessions(user.id)
        if sessions:
            session = st.selectbox("Lịch sử chat", sessions,
                                   format_func=lambda s: s.get("lesson_title") or s["id"])
            for message in ctx.assessment.chat_messages(user.id, session["id"]):
                st.markdown(f"**{message['role']}**: {message['content']}")
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
    if user and hasattr(ctx.assessment, "questions"):
        st.subheader("Luyện tập trắc nghiệm")
        if drafts:
            st.info("Đang có bài kiểm tra tính giờ: tạm khóa chấm luyện tập và xem đáp án cũ.")
        questions = ctx.assessment.questions(user.grade)
        if not questions:
            st.info("Chưa có câu hỏi đã xuất bản cho lớp này.")
        else:
            topic_ids = sorted({question.topic_id for question in questions})
            topic_id = st.selectbox("Chủ đề", topic_ids)
            selected_questions = [q for q in questions if q.topic_id == topic_id]
            selections = {}
            for question in selected_questions:
                st.markdown(f"**{question.text}**")
                if question.image_url:
                    st.image(question.image_url)
                labels = {option.id: option.text for option in question.options}
                if question.kind == "multiple":
                    chosen = st.multiselect("Chọn các đáp án", list(labels),
                                            format_func=labels.get, key=f"q:{question.id}")
                    selections[question.id] = tuple(chosen)
                else:
                    chosen = st.radio("Chọn đáp án", [""] + list(labels),
                                      format_func=lambda key: labels.get(key, "Chưa chọn"),
                                      key=f"q:{question.id}")
                    selections[question.id] = (chosen,) if chosen else ()
                feedback_key = f"feedback:{user.id}:{question.id}"
                if st.button("Kiểm tra câu", key=f"check:{question.id}",
                             disabled=bool(drafts) or readonly):
                    from ..services.quiz import grade_answer

                    try:
                        answer = grade_answer(question, selections[question.id])
                    except ValueError as exc:
                        st.error(str(exc))
                    else:
                        st.session_state[feedback_key] = (selections[question.id], answer)
                feedback = st.session_state.get(feedback_key)
                if not drafts and feedback and feedback[0] == selections[question.id]:
                    answer = feedback[1]
                    st.write("Đúng" if answer.correct else "Sai")
                    st.write("Đáp án đúng:", ", ".join(labels[key] for key in answer.correct_ids))
                    st.markdown(answer.explanation)
                if st.button("Hỏi AI về câu này", key=f"ask:{question.id}",
                             disabled=bool(drafts) or readonly):
                    lesson_for_question = next(
                        (item for item in lessons if item.topic_id == question.topic_id), None)
                    if lesson_for_question is None:
                        st.error("Chưa có bài học ngữ cảnh cho câu hỏi này.")
                    else:
                        context = tuple(ctx.content.ai_context(lesson_for_question.id))
                        request = AIRequest(
                            f"{question.text} — {lesson_for_question.title}", user.grade, language,
                            context, lesson_for_question.id)
                        try:
                            response = ctx.assessment.ask_ai(user.id, request)
                        except (ValueError, TimeoutError) as exc:
                            st.error(str(exc))
                        else:
                            st.markdown(response.text)
                            source_links = _source_links(response.source_ids)
                            if source_links:
                                st.markdown("Nguồn: " + source_links)
            if st.button("Nộp bài luyện tập", disabled=bool(drafts) or readonly):
                try:
                    result = ctx.assessment.submit(user.id, topic_id, selections)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.success(f"Điểm: {result.score}/10")
                    option_labels = {option.id: option.text
                                     for question in selected_questions for option in question.options}
                    for item in result.answers:
                        st.write(f"{item.question_id}: {'Đúng' if item.correct else 'Sai'}")
                        st.write("Đã chọn:", ", ".join(option_labels.get(key, key)
                                                     for key in item.selected_ids))
                        st.write("Đáp án đúng:", ", ".join(option_labels.get(key, key)
                                                          for key in item.correct_ids))
                        st.markdown(item.explanation)
        attempts = ctx.assessment.attempts(user.id)
        if attempts and not drafts and hasattr(ctx.assessment, "attempt_detail"):
            chosen_attempt = st.selectbox("Xem lại lần làm", attempts,
                                          format_func=lambda a: f"{a.id} · {a.score}/10")
            for detail in ctx.assessment.attempt_detail(user.id, chosen_attempt.id):
                st.markdown(f"**{detail['question']}** — "
                            f"{'Đúng' if detail['correct'] else 'Sai'}")
                selected = [item.get("text") or item["id"]
                            for item in detail.get("selected_options", []) if item["id"]]
                correct = [item.get("text") or item["id"]
                           for item in detail.get("correct_options", []) if item["id"]]
                st.write("Đã chọn:", ", ".join(selected) or "Chưa chọn")
                st.write("Đáp án đúng:", ", ".join(correct))
                st.markdown(detail.get("explanation") or "")
        st.subheader("Kiểm tra tính giờ")
        if questions:
            test_topic = st.selectbox("Chủ đề kiểm tra", topic_ids)
            duration = st.selectbox("Thời lượng (phút)", [5, 10, 15, 30])
            if st.button("Bắt đầu bài kiểm tra", disabled=bool(drafts) or readonly):
                try:
                    new_session = ctx.assessment.start_test(
                        user.id, user.grade, test_topic, duration * 60)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.session_state["assessment:active_test"] = new_session.id
                    st.rerun()
        if drafts:
            draft_ids = [item["id"] for item in drafts]
            active = st.session_state.get("assessment:active_test")
            selected_id = st.selectbox("Tiếp tục bài đang làm", draft_ids,
                                       index=draft_ids.index(active) if active in draft_ids else 0)
            session = ctx.assessment.resume_test(user.id, selected_id)
            remaining = ctx.assessment.test_seconds_left(session)
            st.caption(f"Còn {remaining // 60}:{remaining % 60:02d}. Đáp án chỉ hiện sau khi nộp.")
            test_selections = {}
            for test_question in session.questions:
                st.markdown(f"**{test_question.text}**")
                if test_question.image_url:
                    st.image(test_question.image_url)
                labels = {option.id: option.text for option in test_question.options}
                saved = session.selections.get(test_question.id, ())
                if test_question.kind == "multiple":
                    chosen = st.multiselect("Chọn các đáp án", list(labels),
                                            default=list(saved), format_func=labels.get,
                                            key=f"test:{session.id}:{test_question.id}")
                    test_selections[test_question.id] = tuple(chosen)
                else:
                    chosen = st.radio("Chọn đáp án", [""] + list(labels),
                                      index=([""] + list(labels)).index(saved[0]) if saved else 0,
                                      format_func=lambda key: labels.get(key, "Chưa chọn"),
                                      key=f"test:{session.id}:{test_question.id}")
                    test_selections[test_question.id] = (chosen,) if chosen else ()
                if st.button("Gợi mở AI", key=f"test-hint:{session.id}:{test_question.id}", disabled=readonly):
                    request = AIRequest(
                        f"Gợi mở cách nghĩ về {test_question.text} trong hình học tứ giác",
                        user.grade, "vi", (), purpose="assessment_hint")
                    try:
                        hint = ctx.assessment.ask_ai(user.id, request)
                    except (ValueError, TimeoutError) as exc:
                        st.error(str(exc))
                    else:
                        st.markdown(hint.text)
            if st.button("Lưu nháp", disabled=remaining == 0 or readonly):
                try:
                    ctx.assessment.save_test_draft(user.id, session, test_selections)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.success("Đã lưu bài đang làm.")
            if st.button("Nộp bài kiểm tra", disabled=readonly):
                try:
                    if remaining > 0:
                        ctx.assessment.save_test_draft(user.id, session, test_selections)
                    result = ctx.assessment.submit_test(user.id, session.id)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.success(f"Điểm kiểm tra: {result.score}/10")
                    for answer in result.answers:
                        st.write(f"{answer.question_id}: {'Đúng' if answer.correct else 'Sai'}")
                        st.markdown(answer.explanation)
    if user and not drafts and hasattr(ctx.assessment, "essays"):
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
