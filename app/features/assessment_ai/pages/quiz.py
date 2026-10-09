"""DOMAIN OWNER: DAT. Luồng chọn bài → làm bài → kết quả; chấm/lưu qua contract."""
from uuid import uuid4
from urllib.parse import quote
import streamlit as st


def topic_names(lessons, topic_ids):
    names = {lesson.topic_id: lesson.title for lesson in lessons}
    return {topic: names.get(topic, f"Chủ đề {index}") for index, topic in enumerate(topic_ids, 1)}


def answer_input(question, key, saved=(), disabled=False):
    labels = {option.id: option.text for option in question.options}
    if question.image_url:
        st.image(question.image_url)
    if question.kind == "multiple":
        st.caption("Chọn tất cả đáp án đúng; có thể chọn nhiều đáp án.")
        return tuple(st.multiselect("Chọn các đáp án", list(labels), default=list(saved),
                                    format_func=labels.get, key=key, disabled=disabled))
    chosen = st.radio("Chọn một đáp án", list(labels),
                      index=list(labels).index(saved[0]) if saved and saved[0] in labels else None,
                      format_func=labels.get, key=key, disabled=disabled)
    return (chosen,) if chosen else ()


def show_result(result, questions, lessons):
    st.subheader("Kết quả bài làm")
    correct = sum(answer.correct for answer in result.answers)
    points, count = st.columns(2)
    points.metric("Điểm", f"{result.score:g}/10")
    count.metric("Câu trả lời đúng", f"{correct}/{len(result.answers)}")
    st.success("Đã lưu bài làm. Bạn có thể xem lại trong mục Lịch sử.")
    by_id = {question.id: question for question in questions}
    for index, answer in enumerate(result.answers, 1):
        question = by_id.get(answer.question_id)
        with st.expander(f"Câu {index} · {'Đúng' if answer.correct else 'Cần xem lại'}", expanded=not answer.correct):
            if question:
                st.markdown(question.text)
                labels = {option.id: option.text for option in question.options}
                st.write("Bạn đã chọn:", ", ".join(labels.get(key, key) for key in answer.selected_ids) or "Chưa trả lời")
                st.write("Đáp án đúng:", ", ".join(labels.get(key, key) for key in answer.correct_ids))
            st.markdown(answer.explanation)
    lesson = next((item for item in lessons if item.topic_id == result.topic_id), None)
    if lesson:
        st.markdown(f"[Ôn lại lý thuyết: {lesson.title}](/learning?lesson_id={quote(lesson.id, safe='')})")


def render(ctx, user, readonly, drafts, lessons):
    result_key = f"quiz:result:{user.id}"
    if not drafts and st.session_state.get(result_key):
        result, questions = st.session_state[result_key]
        show_result(result, questions, lessons)
        st.button("Chọn bài khác / Làm lại", type="primary",
                  on_click=lambda: st.session_state.pop(result_key, None))
        return
    st.subheader("Luyện tập trắc nghiệm" if not drafts else "Bài kiểm tra đang làm")
    if drafts:
        render_test(ctx, user, readonly, drafts, lessons)
        return
    mode = st.radio("Hình thức làm bài", ["Luyện tập", "Kiểm tra tính giờ"], horizontal=True)
    if mode == "Kiểm tra tính giờ":
        render_test(ctx, user, readonly, drafts, lessons)
        return
    state_key = f"quiz:practice:{user.id}:{user.grade}"
    state = st.session_state.get(state_key)
    if state is None:
        questions = ctx.assessment.questions(user.grade) if hasattr(ctx.assessment, "questions") else []
        if not questions:
            st.info("Chưa có bài trắc nghiệm cho lớp của bạn.")
            return
        topics = list(dict.fromkeys(question.topic_id for question in questions))
        names = topic_names(lessons, topics)
        with st.container(border=True):
            st.markdown("### 1. Chọn bài luyện tập")
            topic = st.selectbox("Bài học", topics, format_func=names.get)
            selected = tuple(question for question in questions if question.topic_id == topic)
            st.write(f"Lớp {user.grade} · {len(selected)} câu hỏi · Không giới hạn thời gian")
            st.caption("Làm từng câu, kiểm tra lựa chọn rồi nộp bài để xem điểm và lời giải.")
            def start():
                st.session_state[state_key] = {"topic": topic, "questions": selected, "index": 0,
                                               "answers": {}, "run": uuid4().hex, "title": names[topic]}
            st.button("Bắt đầu luyện tập", type="primary", disabled=readonly, on_click=start)
        return
    questions = state["questions"]
    index = state["index"]
    st.markdown(f"### {state['title']}")
    st.caption("Lựa chọn được giữ khi chuyển câu. Bài luyện tập được lưu vào lịch sử sau khi nộp.")
    question = questions[index]
    with st.container(border=True):
        st.markdown(f"#### Câu {index + 1}/{len(questions)}")
        st.markdown(question.text)
        state["answers"][question.id] = answer_input(question, f"practice:{state['run']}:{question.id}",
                                                    state["answers"].get(question.id, ()), readonly)
    answered = sum(bool(state["answers"].get(item.id)) for item in questions)
    st.progress(answered / len(questions), text=f"Đã trả lời {answered}/{len(questions)} câu")
    with st.expander("Hỗ trợ câu đang làm (không nộp bài)"):
        st.caption("Có thể kiểm tra riêng một câu khi luyện tập. Kết quả chỉ được lưu vào lịch sử khi nộp cả bài.")
        feedback_key = f"practice-help:{state['run']}:{question.id}"
        if st.button("Kiểm tra câu", disabled=readonly):
            from ..services.quiz import grade_answer
            try:
                answer = grade_answer(question, state["answers"][question.id])
            except ValueError:
                st.warning("Chọn đáp án trước khi kiểm tra câu.")
            else:
                st.session_state[feedback_key] = (state["answers"][question.id], answer)
        feedback = st.session_state.get(feedback_key)
        if feedback and feedback[0] == state["answers"][question.id]:
            st.write("Đúng" if feedback[1].correct else "Cần xem lại")
            labels = {option.id: option.text for option in question.options}
            st.write("Đáp án đúng:", ", ".join(labels[item] for item in feedback[1].correct_ids))
            st.markdown(feedback[1].explanation)
        if st.button("Hỏi trợ lý về câu này", disabled=readonly):
            from ..models.ai import AIRequest
            from .support import _source_links
            lesson = next((item for item in lessons if item.topic_id == question.topic_id), None)
            if lesson is None:
                st.info("Chưa có bài học để hỗ trợ câu hỏi này.")
            else:
                request = AIRequest(f"{question.text} — {lesson.title}", user.grade, "vi",
                                    tuple(ctx.content.ai_context(lesson.id)), lesson.id)
                try:
                    response = ctx.assessment.ask_ai(user.id, request)
                except (ValueError, TimeoutError) as exc:
                    st.error(str(exc))
                else:
                    st.caption("Phản hồi từ trợ lý mô phỏng.")
                    st.markdown(response.text)
                    st.markdown(_source_links(response.source_ids))
    previous, following = st.columns(2)
    if previous.button("← Câu trước", disabled=index == 0, use_container_width=True):
        state["index"] -= 1
        st.rerun()
    if following.button("Câu tiếp →", disabled=index == len(questions) - 1, use_container_width=True):
        state["index"] += 1
        st.rerun()
    with st.expander("Đi đến câu hỏi"):
        destination = st.selectbox("Câu cần xem", range(len(questions)),
            format_func=lambda i: f"Câu {i+1} · {'Đã chọn' if state['answers'].get(questions[i].id) else 'Chưa trả lời'}")
        if st.button("Đến câu này"):
            state["index"] = destination
            st.rerun()
    def submit_practice():
        # Callback chạy trước render: đồng bộ cả lựa chọn vừa thay đổi rồi chấm một lần.
        current = st.session_state.get(f"practice:{state['run']}:{question.id}")
        state["answers"][question.id] = tuple(current or ()) if question.kind == "multiple" else ((current,) if current else ())
        missing = sum(not state["answers"].get(item.id) for item in questions)
        if missing:
            state["error"] = f"Còn {missing} câu chưa trả lời. Hãy hoàn thành trước khi nộp."
            return
        try:
            result = ctx.assessment.submit(user.id, state["topic"], state["answers"])
        except ValueError as exc:
            state["error"] = str(exc)
        else:
            st.session_state[result_key] = (result, questions)
            del st.session_state[state_key]
    st.button("Nộp bài luyện tập", type="primary", disabled=readonly, on_click=submit_practice)
    if state.get("error"):
        st.warning(state.pop("error"))
    st.caption("Luyện tập đang làm chỉ giữ trong phiên truy cập này; tải lại trình duyệt có thể mất lựa chọn chưa nộp.")
    with st.expander("Đổi bài luyện tập"):
        st.warning("Đổi bài sẽ bỏ các lựa chọn chưa nộp của bài này.")
        if st.button("Bỏ lựa chọn và chọn bài khác"):
            del st.session_state[state_key]
            st.rerun()


def render_test(ctx, user, readonly, drafts, lessons):
    if not drafts:
        questions = ctx.assessment.questions(user.grade) if hasattr(ctx.assessment, "questions") else []
        if not questions:
            st.info("Chưa có bài kiểm tra cho lớp của bạn.")
            return
        topics = list(dict.fromkeys(question.topic_id for question in questions))
        names = topic_names(lessons, topics)
        with st.container(border=True):
            st.markdown("### Chọn bài kiểm tra")
            topic = st.selectbox("Bài học kiểm tra", topics, format_func=names.get)
            duration = st.selectbox("Thời lượng (phút)", [5, 10, 15, 30])
            st.caption("Đáp án chỉ hiện sau khi nộp. Có thể lưu nháp để tiếp tục; thời gian vẫn tính từ lúc bắt đầu.")
            if st.button("Bắt đầu bài kiểm tra", type="primary", disabled=readonly):
                try:
                    session = ctx.assessment.start_test(user.id, user.grade, topic, duration * 60)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.session_state["assessment:active_test"] = session.id
                    st.rerun()
        return
    names = topic_names(lessons, [draft["topic_id"] for draft in drafts])
    active = st.session_state.get("assessment:active_test")
    draft_ids = [item["id"] for item in drafts]
    selected = st.selectbox("Tiếp tục bài đang làm", draft_ids,
        index=draft_ids.index(active) if active in draft_ids else 0,
        format_func=lambda key: names[next(item["topic_id"] for item in drafts if item["id"] == key)])
    session = ctx.assessment.resume_test(user.id, selected)
    remaining = ctx.assessment.test_seconds_left(session)
    st.markdown(f"### {names[session.topic_id]}")
    st.info(f"Thời gian còn lại: {remaining // 60}:{remaining % 60:02d} · {len(session.questions)} câu")
    st.caption("Thời gian cập nhật khi bạn thao tác. Lưu nháp để giữ đáp án; câu bỏ trống khi nộp được tính sai.")
    if remaining == 0:
        st.warning("Đã hết giờ. Nộp bài để chấm các lựa chọn đã lưu nháp; lựa chọn chưa lưu sẽ không được tính.")
    answers = {}
    with st.form(f"test-form:{session.id}"):
        for index, question in enumerate(session.questions, 1):
            with st.container(border=True):
                st.markdown(f"#### Câu {index}/{len(session.questions)}")
                st.markdown(question.text)
                answers[question.id] = answer_input(question, f"test:{session.id}:{question.id}",
                    session.selections.get(question.id, ()), readonly or remaining == 0)
        save_col, submit_col = st.columns(2)
        save = save_col.form_submit_button("Lưu nháp", disabled=readonly or remaining == 0, use_container_width=True)
        submit = submit_col.form_submit_button("Nộp bài kiểm tra", type="primary", disabled=readonly, use_container_width=True)
    if save or submit:
        try:
            if remaining > 0:
                ctx.assessment.save_test_draft(user.id, session, answers)
            if submit:
                result = ctx.assessment.submit_test(user.id, session.id)
                st.session_state[f"quiz:result:{user.id}"] = (result, session.questions)
                st.session_state.pop("assessment:active_test", None)
                st.rerun()
            else:
                st.success("Đã lưu nháp. Bạn có thể tiếp tục từ các lựa chọn này.")
        except ValueError as exc:
            st.error(str(exc))
    with st.expander("Cần gợi mở cách nghĩ?"):
        st.caption("Trợ lý mô phỏng chỉ gợi mở trong lúc kiểm tra; không cung cấp đáp án.")
        chosen = st.selectbox("Câu cần hỗ trợ", session.questions, format_func=lambda q: q.text)
        if st.button("Gợi mở cách nghĩ", disabled=readonly or remaining == 0):
            from ..models.ai import AIRequest
            request = AIRequest(f"Gợi mở cách nghĩ về {chosen.text} trong hình học tứ giác",
                                user.grade, "vi", (), purpose="assessment_hint")
            try:
                reply = ctx.assessment.ask_ai(user.id, request)
            except (ValueError, TimeoutError) as exc:
                st.error(str(exc))
            else:
                st.markdown(reply.text)
