import streamlit as st
from .common import signed_in, action


def render(ctx):
    st.title("Hồ sơ và cấp độ · Vũ")
    user = signed_in(ctx)
    if not user:
        return
    profile = ctx.identity.profile()
    st.write(f"Email: {profile['email']} · Lớp hiện tại: {user.grade}")
    with st.form("vu_profile"):
        name = st.text_input("Tên", value=profile["name"])
        language = st.selectbox(
            "Ngôn ngữ hồ sơ",
            ["vi", "en"],
            index=1 if profile["language"] == "en" else 0,
        )
        avatar = st.text_input("URL ảnh đại diện", value=profile["avatar_url"] or "")
        submit = st.form_submit_button("Lưu hồ sơ")
    if submit:
        action(lambda: ctx.identity.update_profile(name, language, avatar))
    st.caption(
        "Lưu preference ngôn ngữ; chuyển toàn bộ UI Việt/Anh thuộc phần phối hợp với Sơn, chưa hoàn tất."
    )
    if ctx.progress:
        levels = ctx.progress.levels(user.id)
        st.table(
            [
                dict(
                    lop=x.grade,
                    hoan_thanh=round(x.completion, 2),
                    diem_tb=x.average_score,
                    da_mo=x.unlocked,
                )
                for x in levels
            ]
        )
        grade = st.selectbox("Chuyển sang lớp", [6, 7, 8, 9], index=user.grade - 6)
        st.warning(
            "Học vượt khi chưa đạt ngưỡng có thể thiếu kiến thức tiên quyết. Xem các bài nền trước khi tiếp tục."
        )
        confirmed = st.checkbox(
            "Tôi đã đọc cảnh báo và xác nhận học vượt nếu chưa đạt ngưỡng"
        )
        if st.button("Xác nhận đổi cấp độ"):
            ok, _ = action(
                lambda: ctx.progress.change_level(grade, confirmed),
                "Đã chuyển cấp độ, tiến độ lớp cũ được giữ nguyên.",
            )
            if ok:
                st.rerun()
    with st.form("vu_password_change"):
        old = st.text_input("Mật khẩu hiện tại", type="password")
        new = st.text_input("Mật khẩu thay thế", type="password")
        submit = st.form_submit_button("Đổi mật khẩu")
    if submit:
        ok, _ = action(
            lambda: ctx.auth.change_password(ctx.identity, old, new),
            "Đã đổi mật khẩu và đăng xuất các session cũ.",
        )
        if ok:
            st.rerun()
    st.caption(
        "TODO: xóa tài khoản cần contract xóa dữ liệu bài làm/chat của Đạt; không DETACH DELETE dữ liệu domain khác."
    )
