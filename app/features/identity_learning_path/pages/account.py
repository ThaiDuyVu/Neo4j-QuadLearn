# DOMAIN OWNER: VU. UI chỉ nhập dữ liệu/gọi contract, không Cypher/hash password.
import streamlit as st
from .common import action


def render(ctx):
    st.title("Tài khoản · Vũ")
    if ctx.auth is None:
        st.info("Chưa cấu hình Authentication contract.")
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
    st.warning(
        "AUTH local: có băm mật khẩu và session Neo4j. Email/OAuth thật chưa tích hợp. Chỉ dùng dữ liệu thử nghiệm."
    )
    login, register, verify, reset = st.tabs(
        ["Đăng nhập", "Đăng ký", "Xác thực local", "Quên / đặt lại mật khẩu"]
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
                    "Đã tạo tài khoản pending; chưa được đăng nhập.",
                )
                if ok:
                    st.session_state["vu_dev_delivery"] = result[1]
        delivery = st.session_state.get("vu_dev_delivery", {})
        if delivery:
            st.caption(
                "Token thử nghiệm chỉ hiển thị trong browser này; KHÔNG phải email đã gửi. Không lưu/chụp token vào Git."
            )
            for kind, token in delivery.items():
                st.write(kind)
                st.code(token)
    with verify:
        st.write(
            "Nhập token local ở trên. Dưới 16 tuổi cần cả verify và guardian mới active. Đây chưa phải xác minh danh tính/email thực tế."
        )
        with st.form("vu_verify"):
            kind = st.selectbox("Loại xác thực", ["verify", "guardian"])
            token = st.text_input("Token kích hoạt", type="password")
            submit = st.form_submit_button("Xác nhận token local")
        if submit:
            action(
                lambda: ctx.auth.activate(token, kind),
                "Đã xác nhận token. Nếu đủ điều kiện, tài khoản đã active.",
            )
    with reset:
        with st.form("vu_reset_request"):
            email = st.text_input("Email cần đặt lại")
            submit = st.form_submit_button("Yêu cầu token reset local")
        if submit:
            ok, token = action(
                lambda: ctx.auth.request_reset(email),
                "Nếu tài khoản hợp lệ, có thể dùng token local bên dưới; chưa gửi email.",
            )
            if ok and token:
                st.code(token)
        with st.form("vu_reset_apply"):
            token = st.text_input("Token reset", type="password")
            password = st.text_input("Mật khẩu sau reset", type="password")
            submit = st.form_submit_button("Đặt lại mật khẩu")
        if submit:
            ok, _ = action(
                lambda: ctx.auth.reset_password(token, password),
                "Đã đổi mật khẩu; các session cũ không còn hợp lệ.",
            )
            if ok:
                ctx.identity.logout()
