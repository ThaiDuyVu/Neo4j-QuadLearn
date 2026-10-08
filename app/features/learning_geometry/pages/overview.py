# DOMAIN OWNER: SON · learning_geometry
import streamlit as st
import streamlit.components.v1 as components
from app.core.context import AppContext
from ..services.geometry import rectangle


def render(ctx: AppContext):
    st.title("📐 Tổng quan Nội dung & Mô phỏng Hình học")
    st.caption("Khám phá chương trình học lý thuyết và công cụ tương tác hình học trực quan.")

    grade = st.selectbox("Chọn khối lớp:", [6, 7, 8, 9], index=2)
    lessons = ctx.content.lessons(grade)

    if lessons:
        lesson = st.selectbox(
            "Chọn bài học lý thuyết:", 
            lessons, 
            format_func=lambda x: getattr(x, "title", getattr(x, "title_vi", "Bài học"))
        )
        
        st.subheader(f"📖 {getattr(lesson, 'title', getattr(lesson, 'title_vi', 'Chi tiết bài học'))}")
        st.markdown(getattr(lesson, "content", getattr(lesson, "content_vi", "Nội dung đang cập nhật...")))

        st.markdown("#### 🔗 Bài học tiên quyết")
        prereqs = ctx.content.prerequisites(lesson.id)
        if prereqs:
            st.table([
                {
                    "Mã bài học": x.id, 
                    "Tên bài học": getattr(x, "title", getattr(x, "title_vi", "")), 
                    "Khối lớp": getattr(x, "grade", grade)
                } 
                for x in prereqs
            ])
        else:
            st.info("Bài học này không có kiến thức tiên quyết bắt buộc.")
    else:
        st.info(f"Chưa tìm thấy bài học cho Lớp {grade} trong hệ thống.")

    st.divider()

    st.subheader("📐 Mô phỏng Tứ giác Động Tương tác (Lớp 6 - 9)")
    
    # Chọn loại tứ giác phù hợp chương trình Lớp 6 - 9
    shape_type = st.radio(
        "Chọn hình tứ giác mô phỏng:", 
        ["Hình chữ nhật", "Hình vuông", "Hình bình hành", "Hình thoi", "Hình thang cân"], 
        horizontal=True
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        if shape_type == "Hình vuông":
            side = st.slider("Cạnh (a):", 1, 10, 5)
            st.latex(r"S = a^2 \quad | \quad P = 4 \times a")
            st.metric("Diện tích (S)", f"{side**2} unit²")
            st.metric("Chu vi (P)", f"{4*side} unit")
            svg_content = f'''
                <rect x="60" y="30" width="{side*18}" height="{side*18}" fill="#3b82f622" stroke="#2563eb" stroke-width="3"/>
                <text x="{60 + side*9}" y="20" fill="#1e293b" font-weight="bold" text-anchor="middle">a = {side}</text>
            '''

        elif shape_type == "Hình chữ nhật":
            width = st.slider("Chiều dài (a):", 1, 10, 6)
            height = st.slider("Chiều rộng (b):", 1, 10, 3)
            _, area, perimeter = rectangle(width, height)
            st.latex(r"S = a \times b \quad | \quad P = 2 \times (a + b)")
            st.metric("Diện tích (S)", f"{area} unit²")
            st.metric("Chu vi (P)", f"{perimeter} unit")
            svg_content = f'''
                <rect x="40" y="30" width="{width*20}" height="{height*20}" fill="#3b82f622" stroke="#2563eb" stroke-width="3"/>
                <text x="{40 + width*10}" y="20" fill="#1e293b" font-weight="bold" text-anchor="middle">a = {width}</text>
                <text x="{30 + width*20}" y="{30 + height*10}" fill="#1e293b" font-weight="bold" text-anchor="start">b = {height}</text>
            '''

        elif shape_type == "Hình bình hành":
            a = st.slider("Cạnh đáy (a):", 1, 10, 6)
            h = st.slider("Chiều cao (h):", 1, 10, 4)
            st.latex(r"S = a \times h")
            st.metric("Diện tích (S)", f"{a*h} unit²")
            svg_content = f'''
                <polygon points="40,{30+h*18} {40+a*18},{30+h*18} {70+a*18},30 70,30" fill="#10b98122" stroke="#059669" stroke-width="3"/>
                <line x1="70" y1="30" x2="70" y2="{30+h*18}" stroke="#ef4444" stroke-width="2" stroke-dasharray="4"/>
                <text x="{40 + a*9}" y="{45 + h*18}" fill="#1e293b" font-weight="bold" text-anchor="middle">a = {a}</text>
                <text x="63" y="{30 + h*9}" fill="#ef4444" font-weight="bold" text-anchor="end">h = {h}</text>
            '''

        elif shape_type == "Hình thoi":
            d1 = st.slider("Đường chéo 1 (d1):", 2, 10, 6)
            d2 = st.slider("Đường chéo 2 (d2):", 2, 10, 4)
            st.latex(r"S = \frac{1}{2} \times d_1 \times d_2")
            st.metric("Diện tích (S)", f"{0.5 * d1 * d2:.1f} unit²")
            cx, cy = 150, 100
            hx, hy = d1 * 12, d2 * 12
            svg_content = f'''
                <polygon points="{cx},{cy-hy} {cx+hx},{cy} {cx},{cy+hy} {cx-hx},{cy}" fill="#8b5cf622" stroke="#7c3aed" stroke-width="3"/>
                <line x1="{cx-hx}" y1="{cy}" x2="{cx+hx}" y2="{cy}" stroke="#6d28d9" stroke-width="2" stroke-dasharray="4"/>
                <line x1="{cx}" y1="{cy-hy}" x2="{cx}" y2="{cy+hy}" stroke="#6d28d9" stroke-width="2" stroke-dasharray="4"/>
                <text x="{cx}" y="{cy - hy - 8}" fill="#1e293b" font-weight="bold" text-anchor="middle">d1 = {d1}</text>
                <text x="{cx + hx + 10}" y="{cy + 4}" fill="#1e293b" font-weight="bold" text-anchor="start">d2 = {d2}</text>
            '''

        else:  # Hình thang cân
            a = st.slider("Đáy nhỏ (a):", 1, 8, 3)
            b = st.slider("Đáy lớn (b):", a + 1, 10, 7)
            h = st.slider("Chiều cao (h):", 1, 8, 4)
            st.latex(r"S = \frac{(a + b) \times h}{2}")
            st.metric("Diện tích (S)", f"{((a + b) * h) / 2:.1f} unit²")
            shift = (b - a) * 10
            svg_content = f'''
                <polygon points="40,{30+h*18} {40+b*20},{30+h*18} {40+shift+a*20},30 {40+shift},30" fill="#f59e0b22" stroke="#d97706" stroke-width="3"/>
                <line x1="{40+shift}" y1="30" x2="{40+shift}" y2="{30+h*18}" stroke="#ef4444" stroke-width="2" stroke-dasharray="4"/>
                <text x="{40 + shift + a*10}" y="20" fill="#1e293b" font-weight="bold" text-anchor="middle">a = {a}</text>
                <text x="{40 + b*10}" y="{48 + h*18}" fill="#1e293b" font-weight="bold" text-anchor="middle">b = {b}</text>
                <text x="{33 + shift}" y="{30 + h*9}" fill="#ef4444" font-weight="bold" text-anchor="end">h = {h}</text>
            '''

    with col2:
        components.html(
            f'''
            <svg viewBox="0 0 500 250" style="background:#f8fafc; border-radius:8px; border:1px solid #e2e8f0;">
                {svg_content}
            </svg>
            ''', 
            height=260
        )


render_overview_page = render