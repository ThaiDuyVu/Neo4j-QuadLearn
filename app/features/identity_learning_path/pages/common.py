"""Hiển thị lỗi nghiệp vụ; lỗi driver tiếp tục lên bộ xử lý main."""

import streamlit as st
from ..models.errors import IdentityError


def action(call, message="Đã lưu."):
    try:
        result = call()
        st.success(message)
        return True, result
    except IdentityError as error:
        st.error(str(error))
        return False, None


def signed_in(ctx):
    user = ctx.identity.current_user()
    if not user or user.demo:
        st.warning(
            "Cần đăng nhập tài khoản local đã kích hoạt. Vào trang Tài khoản của Vũ."
        )
        return None
    return user
