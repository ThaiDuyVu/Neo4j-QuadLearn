# DOMAIN OWNER: SON · learning_geometry
# Page chỉ đọc qua ContentReader; không chứa Cypher ghi hoặc dữ liệu hình hardcode.
import streamlit as st
from app.core.context import AppContext
from ..services.knowledge_graph import focus_graph, graph_dot

DIRECTIONS = {
    "Loại tổng quát hơn": "parents",
    "Các hình thuộc loại này": "children",
    "Cả hai hướng": "both",
}


def render(ctx: AppContext):
    st.title("Sơ đồ tri thức hình học")
    st.caption("Khám phá các loại tứ giác và quan hệ phân loại được lưu trong Neo4j.")
    graph = ctx.content.geometry_graph()
    if not graph["nodes"]:
        st.info("Chưa có dữ liệu các loại tứ giác. Hãy thêm học liệu trước khi xem sơ đồ.")
        return
    nodes = sorted(graph["nodes"], key=lambda node: node["name"])
    names = {node["id"]: node["name"] for node in nodes}
    selected = None
    with st.container(border=True):
        view_col, layout_col, refresh_col = st.columns([2, 2, 1])
        with view_col:
            view = st.radio("Phạm vi hiển thị", ["Toàn bộ sơ đồ", "Tập trung một hình"], horizontal=True)
        with layout_col:
            layout = st.selectbox("Bố cục sơ đồ", ["Từ dưới lên", "Từ trái sang phải"])
        with refresh_col:
            # Streamlit rerun khi nhấn; graph được truy vấn lại, không cache dữ liệu.
            st.button("Làm mới dữ liệu", use_container_width=True)
        if view == "Tập trung một hình":
            shape_col, direction_col, depth_col = st.columns([2, 2, 1])
            with shape_col:
                selected = st.selectbox("Hình cần khám phá", list(names), format_func=names.get)
            with direction_col:
                direction = st.selectbox("Hướng khám phá", list(DIRECTIONS), index=2)
            with depth_col:
                depth = st.slider("Số bước quan hệ", 1, 8, 2)
            visible = focus_graph(graph, selected, DIRECTIONS[direction], depth)
        else:
            visible = graph
    count_col, edge_col = st.columns(2)
    count_col.metric("Loại hình đang hiển thị", len(visible["nodes"]))
    edge_col.metric("Quan hệ đang hiển thị", len(visible["edges"]))
    diagram, explanation = st.columns([3, 1])
    dot = graph_dot(visible, selected, "BT" if layout == "Từ dưới lên" else "LR")
    with diagram:
        with st.container(border=True):
            st.subheader("Mối quan hệ giữa các hình")
            st.graphviz_chart(dot, use_container_width=True)
            if not visible["edges"]:
                st.info("Các hình đang chọn chưa có quan hệ nối với nhau trong DB.")
    with explanation:
        with st.container(border=True):
            st.subheader("Cách đọc sơ đồ")
            st.markdown("**A → B** nghĩa là **A là một loại B**. Mũi tên đi từ hình cụ thể đến hình tổng quát hơn.")
            st.write("IS_A là tên quan hệ phân loại trong Neo4j.")
            st.write("Một hình có thể thuộc nhiều loại; sơ đồ không bắt buộc là cây có một cha.")
            if selected:
                st.info(f"Hình được tô xanh: {names[selected]}")
            st.caption("Mỗi đường nối là một quan hệ trực tiếp trong DB. Quan hệ gián tiếp được đọc theo đường đi nhiều bước.")
        st.download_button("Tải sơ đồ DOT", dot, "quadlearn-geometry.dot", "text/vnd.graphviz", use_container_width=True)
    with st.expander("Xem danh sách quan hệ đang hiển thị"):
        if visible["edges"]:
            st.dataframe([
                {"Hình cụ thể": names[edge["source"]], "Quan hệ": edge["type"],
                 "Loại tổng quát": names[edge["target"]]}
                for edge in visible["edges"]
            ], hide_index=True, use_container_width=True)
        else:
            st.write("Chưa có quan hệ trong phạm vi này.")
    with st.expander("Đối chiếu trong Neo4j Browser"):
        st.caption("Chạy truy vấn này trong Neo4j Browser để xem cùng các node và quan hệ, kể cả hình chưa có liên kết.")
        st.code("""MATCH (q:Quadrilateral)
OPTIONAL MATCH (q)-[r:IS_A]->(parent:Quadrilateral)
RETURN q, r, parent;""", language="cypher")
