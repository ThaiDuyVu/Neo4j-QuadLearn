# DOMAIN OWNER: VU. UI chỉ nhập dữ liệu/gọi contract, không Cypher/hash password.
import streamlit as st
from .common import action


def render(ctx):
    st.title("Tài khoản")
    if ctx.auth is None:
        st.info("Chức năng tài khoản chưa sẵn sàng.")
        return
    user = ctx.identity.current_user()
    if user:
        st.write(
            f"Đang dùng: {user.name} · {user.role}"
            + (" · demo chỉ đọc" if user.demo else "")
        )
        if st.button("Đăng xuất"):
            ctx.identity.logout()
            st.rerun()
    login, register, verify, reset = st.tabs(
        ["Đăng nhập", "Đăng ký", "Kích hoạt tài khoản", "Quên / đặt lại mật khẩu"]
    )
    with login:
        with st.form("vu_login"):
            email = st.text_input("Email đăng nhập")
            password = st.text_input("Mật khẩu đăng nhập", type="password")
            submit = st.form_submit_button("Đăng nhập")
        if submit:
            ok, token = action(
                lambda: ctx.auth.login(email, password), "Đăng nhập thành công."
            )
            if ok:
                ctx.identity.login(token)
                st.rerun()
        if st.button("Dùng demo chỉ đọc"):
            ok, _ = action(ctx.identity.enter_demo, "Đã bật demo chỉ đọc.")
            if ok:
                st.rerun()
    with register:
        with st.form("vu_register"):
            name = st.text_input("Họ tên")
            email = st.text_input("Email đăng ký")
            password = st.text_input("Mật khẩu mới", type="password")
            confirmation = st.text_input("Nhập lại mật khẩu", type="password")
            grade = st.selectbox("Lớp khởi đầu", [6, 7, 8, 9])
            age = st.number_input("Tuổi khai báo", 10, 100, 13)
            guardian = st.text_input("Email người giám hộ (bắt buộc nếu dưới 16 tuổi)")
            submit = st.form_submit_button("Tạo tài khoản")
        if submit:
            if password != confirmation:
                st.error("Mật khẩu nhập lại không khớp.")
            else:
                ok, result = action(
                    lambda: ctx.auth.register(
                        name, email, password, grade, age, guardian
                    ),
                    "Đã tạo tài khoản. Dùng mã bên dưới tại tab Kích hoạt tài khoản để hoàn tất.",
                )
                if ok:
                    st.session_state["vu_dev_delivery"] = result[1]
        delivery = st.session_state.get("vu_dev_delivery", {})
        if delivery:
            st.caption(
                "Mã kích hoạt hiển thị tại đây vì bản chạy trên máy chưa gửi email."
            )
            for kind, token in delivery.items():
                st.write("Mã xác thực tài khoản" if kind == "verify" else "Mã xác nhận người giám hộ")
                st.code(token)
    with verify:
        st.write(
            "Nhập mã nhận được sau khi đăng ký. Người học dưới 16 tuổi cần thêm mã xác nhận người giám hộ. Bản local hiển thị mã trực tiếp, chưa gửi email."
        )
        with st.form("vu_verify"):
            kind = st.selectbox("Loại xác thực", ["verify", "guardian"])
            token = st.text_input("Mã kích hoạt", type="password")
            submit = st.form_submit_button("Kích hoạt")
        if submit:
            action(
                lambda: ctx.auth.activate(token, kind),
                "Đã xác nhận mã. Khi đủ các bước xác thực, bạn có thể đăng nhập.",
            )
    with reset:
        with st.form("vu_reset_request"):
            email = st.text_input("Email cần đặt lại")
            submit = st.form_submit_button("Yêu cầu mã đặt lại mật khẩu")
        if submit:
            ok, token = action(
                lambda: ctx.auth.request_reset(email),
                "Nếu tài khoản hợp lệ, mã đặt lại sẽ hiển thị bên dưới. Bản local chưa gửi email.",
            )
            if ok and token:
                st.code(token)
        with st.form("vu_reset_apply"):
            token = st.text_input("Mã đặt lại mật khẩu", type="password")
            password = st.text_input("Mật khẩu mới sau đặt lại", type="password")
            submit = st.form_submit_button("Đặt lại mật khẩu")
        if submit:
            ok, _ = action(
                lambda: ctx.auth.reset_password(token, password),
                "Đã đổi mật khẩu. Vui lòng đăng nhập lại.",
            )
            if ok:
                ctx.identity.logout()
