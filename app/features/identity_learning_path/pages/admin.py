import streamlit as st
from .common import action
from ..models.errors import IdentityError


def render(ctx):
    st.title("Quản lý người dùng · Vũ")
    try:
        ctx.identity.require_user(admin=True)
    except (IdentityError, AttributeError):
        st.warning("Cần tài khoản admin đã đăng nhập.")
        return
    term = st.text_input("Tìm theo tên/email")
    users = ctx.identity.search_users(term)
    st.metric("Người dùng trong kết quả (tối đa 100)", len(users))
    st.table(users)
    if users:
        uid = st.selectbox(
            "Tài khoản cần quản lý",
            users,
            format_func=lambda u: f"{u['name']} · {u['email']}",
        )["id"]
        blocked = st.checkbox("Khóa tài khoản được chọn", value=False)
        if st.button("Áp dụng khóa / mở khóa"):
            ok, _ = action(
                lambda: ctx.identity.set_blocked(uid, blocked),
                "Đã cập nhật trạng thái và vô hiệu session cũ.",
            )
            if ok:
                st.rerun()
    st.caption(
        "Admin cấp bằng CLI local, không cho tự chọn role khi đăng ký. TODO: thống kê toàn hệ thống, bảo vệ admin nâng cao, cấu hình phiên qua UI."
    )
