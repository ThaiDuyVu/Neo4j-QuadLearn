import json
import streamlit as st

def render_admin_import_page(ctx):
    st.title("⚙️ Import Nội dung Bài học (Admin)")
    uploaded_file = st.file_uploader("Tải lên file JSON bài học:", type=["json"])
    if uploaded_file is not None:
        try:
            payload = json.load(uploaded_file)
            st.success("Đã đọc file JSON thành công!")
        except Exception as e:
            st.error(f"Lỗi cấu trúc JSON: {str(e)}")