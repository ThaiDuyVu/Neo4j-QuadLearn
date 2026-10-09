import streamlit as st
from app.features.learning_geometry.services.geometry_core import GeometryCoreEngine
from app.features.learning_geometry.models.content import GeometryPoint

def render_geometry_board_page(ctx):
    st.title("📐 Bảng vẽ Hình học Tương tác")
    st.write("Công cụ dựng hình và kiểm tra ràng buộc hình học.")