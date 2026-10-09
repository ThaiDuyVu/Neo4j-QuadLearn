# ==================================================
# ĐIỂM KHỞI CHẠY CHÍNH CỦA DỰ ÁN
# KHÔNG khai báo toàn bộ chức năng tại đây.
# VŨ: app/features/identity_learning_path/
# SƠN: app/features/learning_geometry/
# ĐẠT: app/features/assessment_ai/
# Navigation tập hợp từ feature registry.
# Không sửa file này nếu không thực sự cần thiết.
# ==================================================
from pathlib import Path
import sys
# Streamlit chạy file trực tiếp; bảo đảm import app từ thư mục root trên cả hai OS.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import atexit
import streamlit as st
from neo4j.exceptions import Neo4jError, DriverError
from app.core.config import Settings
from app.core.database import Database
from app.core.bootstrap import build_context
from app.core.navigation import discover_pages

st.set_page_config(page_title="QuadLearn · Neo4j", page_icon="📐", layout="wide")

@st.cache_resource
def get_database():
    db = Database(Settings.load())
    atexit.register(db.close)
    return db

def home():
    st.title("QuadLearn – Học Tứ giác lớp 6–9")
    st.write("Đồ án NoSQL · Neo4j · Vũ, Sơn, Đạt")
    st.warning("PROJECT SKELETON: tài khoản demo không phải đăng nhập; AI mock không phải LLM.")
    st.write("Chọn một domain ở sidebar để xem dữ liệu graph mẫu.")
    if st.button("Kiểm tra kết nối Neo4j"):
        try:
            get_database().verify()
            st.success("Kết nối Neo4j thành công")
        except (ValueError, Neo4jError, DriverError, OSError):
            st.error("Chưa kết nối được. Kiểm tra .env, Docker và docs/RUN_PROJECT.md.")

def render_feature(spec):
    try:
        spec.render(build_context(get_database(), session_state=st.session_state))
    except (ValueError, Neo4jError, DriverError, OSError):
        st.error("Không đọc được dữ liệu Neo4j. Khởi động database và chạy seed; xem docs/RUN_PROJECT.md.")

pages = [st.Page(home, title="Home", default=True)]
for spec in discover_pages():
    # Gắn spec qua default argument để không bị late-binding khi thêm page.
    def render(spec=spec):
        render_feature(spec)
    render.__name__ = f"page_{spec.path.replace('-', '_')}"
    pages.append(st.Page(render, title=spec.title, url_path=spec.path))
st.navigation(pages).run()
